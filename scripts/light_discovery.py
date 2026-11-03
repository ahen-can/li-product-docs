#!/usr/bin/env python3
"""Light discovery: for each product in master_list.csv find + download its BROCHURE (sales literature),
verify it, extract text, read the IRDAI description line and run a keyword feature scan.

Run from the repo root:
    python3 -I scripts/light_discovery.py --insurer bharti-life            # one insurer
    python3 -I scripts/light_discovery.py --insurer all --skip-blocked     # everything except blocked sites
    python3 -I scripts/light_discovery.py --insurer hdfc-life --limit 3 --dry-run   # no downloads, show candidates

Writes (append/update, safe to re-run; products already 'ok' are skipped):
    docs/<slug>/<UIN>/brochure.pdf (or policy.pdf if only a policy document was found)
    text/<slug>/<UIN>/<doc_type>.txt
    index.csv                         one row per stored document (see README schema)
    results/light_discovery_results.csv   one row per product: status, description line, flags, features
    results/manual_checklist.csv      products whose brochure could not be found automatically
Rules: CLAUDE.md (1 request/second per domain, insurer's own site only, never invent URLs, keep bytes).
"""
import argparse, csv, datetime, hashlib, html, os, re, subprocess, sys, time, urllib.parse

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
ROOT = os.getcwd()
BLOCKED = {'icici-life', 'kotak-life', 'sud-life', 'go-digit-life'}

# Insurer document/download pages that list brochures (seed pages). Product page URL from master_list is tried first.
SEEDS = {
    'lic': ['https://licindia.in/products'],
    'hdfc-life': ['https://www.hdfclife.com/brochures', 'https://www.hdfclife.com/policy-documents',
                  'https://www.hdfclife.com/life-insurance-plans', 'https://www.hdfclife.com/pdf-sitemap.xml'],
    'axis-max-life': ['https://www.axismaxlife.com/all-insurance-plans'],
    'tata-aia': ['https://www.tataaia.com/active-and-withdrawn-product-status.html'],
    'bajaj-life': ['https://www.bajajlifeinsurance.com/on-sale-plans.html'],
    'absli': ['https://lifeinsurance.adityabirlacapital.com/forms-and-downloads/brochures-and-specimen-contracts/'],
    'pnb-metlife': ['https://www.pnbmetlife.com/life-insurance-plans.html', 'https://www.pnbmetlife.com/downloads.html'],
    'canara-hsbc': ['https://www.canarahsbclife.com/product-list'],
    'indiafirst': ['https://www.indiafirstlife.com/life-insurance-plans', 'https://www.indiafirstlife.com/pdf-sitemap.xml'],
    'indusind-nippon': ['https://www.indusindnipponlife.com/all-plans'],
    'shriram-life': ['https://www.shriramlife.com/life-insurance', 'https://www.shriramlife.com/child-plans'],
    'ageas-federal': ['https://www.ageasfederal.com/brochures-list'],
    'generali-central': ['https://www.generalicentrallife.com/insurance-plans'],
    'bharti-life': ['https://www.bhartiaxa.com/protection-plans', 'https://www.bhartiaxa.com/savings-plans',
                    'https://www.bhartiaxa.com/investment-plans', 'https://www.bhartiaxa.com/retirement-plans',
                    'https://www.bhartiaxa.com/child-education-plans'],
    'edelweiss-life': ['https://www.edelweisslife.in/product-listing'],
    'pramerica-life': ['https://pramericalife.in/saving-plans', 'https://pramericalife.in/term-plans', 'https://pramericalife.in/'],
    'aviva-life': ['https://www.avivaindia.com/form-and-resource-help-desk', 'https://www.avivaindia.com/life-insurance-plans'],
    'bandhan-life': ['https://www.bandhanlife.com/find-your-plan', 'https://www.bandhanlife.com/savings-plans'],
    'sbi-life': [],
    'acko-life': ['https://www.acko.com/life/download/', 'https://www.acko.com/life-insurance/'],
    'creditaccess-life': ['https://www.creditaccesslife.in/savings_product.php'],
}
BROCHURE_WORDS = re.compile(r'brochure|sales[-_ ]?lit|prospectus|leaflet|\bsl\b|_sl_|-sl-|one[-_ ]?pager|product[-_ ]?info', re.I)
POLICY_WORDS = re.compile(r'policy[-_ ]?(doc|wording|bond|contract)|terms[-_ ]?and[-_ ]?conditions|specimen|\bpd\b|_pd_|-pd-', re.I)
BAD_WORDS = re.compile(r'hindi|marathi|tamil|telugu|kannada|gujarati|bengali|malayalam|odia|punjabi|regional|claim|form|proposal|'
                       r'fund[-_ ]?fact|factsheet|newsletter|withdrawn|rider', re.I)
D_ = r'\s*[-‐-―]?\s*'          # hyphen / en-dash / em-dash, with stray spaces ("Non –Linked", "Non- Linked")
PAR_ = r'(?:non' + D_ + r'(?:participating|par)\b|participating|par\b|with' + D_ + r'profits?)'
PARX_ = PAR_ + r'(?:\s*\([^()]{0,30}\))?[\s,]+(?:and\s+)?'   # "Non-Participating (without profits), " / "non-participating and "
DESC = re.compile(r'(?:an?\s+)?(?:individual[\s,]+)?(?:single premium[\s,]+)?(?:' + PARX_ + r')?(?:unit' + D_ + r'linked|non' + D_ + r'linked|linked)[\s,]+(?:' + PARX_ + r')?'
                  r'(?:individual|group)?(?:[^.()]|\([^()]{0,30}\)){0,140}?(?:plan|product|policy)\b', re.I)
FEATURES = {  # keyword scan only - presence of the phrase in the brochure, NOT a verified feature
    'return_of_premium': r'return of (total )?premium|\bROP\b|premium back',
    'whole_life': r'whole[- ]life|(up ?to|till) age (99|100)',
    'limited_pay': r'limited (premium )?pay',
    'single_pay': r'single (premium|pay)',
    'regular_income_option': r'(monthly|annual|regular) income|income (benefit|payout)',
    'lump_sum_option': r'lump ?sum',
    'guaranteed_additions': r'guaranteed addition',
    'loyalty_additions': r'loyalty addition',
    'cash_bonus_or_reversionary': r'cash bonus|reversionary bonus|simple reversionary',
    'terminal_illness': r'terminal illness',
    'critical_illness': r'critical illness',
    'waiver_of_premium': r'waiver of premium|premium waiver',
    'spouse_cover': r'spouse|joint life',
    'life_stage_increase': r'life ?stage|increase (the )?sum assured on (marriage|birth)',
    'zero_cost_exit': r'zero cost|special exit|smart exit',
    'partial_withdrawal': r'partial withdrawal',
    'top_up': r'top[- ]?up',
    'fund_switch': r'switch(es|ing)?\b',
    'premium_holiday': r'premium holiday',
    'return_of_purchase_price': r'return of purchase price|\bROP\b.*purchase',
    'deferred_annuity': r'deferred annuity|deferment period',
    'joint_life_annuity': r'joint life',
    'child_plan_payor_benefit': r'payor|waiver.*(proposer|parent)',
    'online_only': r'online (only|channel)|available online',
}

_last = {}
def polite(domain):
    t = _last.get(domain, 0)
    wait = 1.0 - (time.time() - t)
    if wait > 0: time.sleep(wait)
    _last[domain] = time.time()

def fetch(url, dest):
    polite(urllib.parse.urlparse(url).netloc)
    r = subprocess.run(['curl', '-sSL', '--compressed', '--max-time', '90', '-A', UA, '-H', 'Accept-Language: en-IN,en;q=0.9',
                        '-o', dest, '-w', '%{http_code}\t%{url_effective}', url], capture_output=True, text=True)
    code, eff = (r.stdout.split('\t') + [''])[:2]
    return (int(code) if code.isdigit() else 0), eff

_page_cache = {}
def page_links(url, tmp):
    if url in _page_cache: return _page_cache[url]
    p = os.path.join(tmp, hashlib.md5(url.encode()).hexdigest() + '.html')
    code, eff = fetch(url, p)
    links = []
    if code == 200 and os.path.exists(p):
        t = open(p, 'rb').read().decode('utf-8', 'ignore')
        t = t.replace('\\u002F', '/').replace('\\/', '/')                 # links inside embedded JSON (Nuxt/Next data)
        for m in re.finditer(r'href=["\']([^"\'#]+)["\'][^>]*>(.*?)</a>', t, re.S | re.I):
            links.append((urllib.parse.urljoin(eff or url, html.unescape(m.group(1)).strip()),
                          re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', m.group(2)))).strip()[:120]))
        for m in re.finditer(r'<loc>\s*([^<]+?\.pdf)\s*</loc>', t, re.I):     # PDF sitemaps (e.g. HDFC pdf-sitemap.xml)
            links.append((html.unescape(m.group(1)), ''))
        for m in re.finditer(r'["\']((?:https?:)?//[^"\'\s\\]+?\.pdf|/[^"\'\s\\]+?\.pdf)(\?[^"\'\s\\]*)?\\?["\']', t, re.I):   # PDFs in scripts/data
            links.append((urllib.parse.urljoin(eff or url, m.group(1)), ''))
    _page_cache[url] = links
    return links

def name_tokens(name):
    n = re.sub(r"\b(?:lic'?s|life|insurance|plan|the|sbi|hdfc|icici|bharti|axa|tata|aia|bajaj|absli|kotak|pnb|metlife|canara|hsbc|"
               r"indiafirst|sud|indusind|nippon|shriram|ageas|federal|generali|central|edelweiss|pramerica|aviva|bandhan|axis|max)\b",
               ' ', name.lower().replace('\u2019', "'"))
    return [w for w in re.findall(r'[a-z0-9]+', n) if len(w) > 2]

def score(url, text, prod, on_product_page=False):
    s = 0; u = urllib.parse.unquote(url).lower(); blob = u + ' ' + text.lower()
    if on_product_page and text and BROCHURE_WORDS.search(blob): s += 6     # 'Brochure' anchor on the product's own page
    if on_product_page and text and POLICY_WORDS.search(blob): s += 4       # 'Policy document' anchor on the product's own page
    if on_product_page and not text and (BROCHURE_WORDS.search(blob) or POLICY_WORDS.search(blob)): s += 3   # same, from embedded page data
    code = prod['product_code'].lower()
    if code and code in blob.replace(' ', ''): s += 6
    if prod['uin'] and prod['uin'].lower() in blob.replace(' ', ''): s += 2
    toks = name_tokens(prod['product_name'])
    if toks: s += 8 * sum(1 for t in toks if t in blob) / len(toks)
    slug = re.sub(r'[^a-z0-9]+', '-', prod['product_name'].lower().replace("'", '')).strip('-')
    if slug and re.search(r'(^|[/_-])' + re.escape(slug) + r'([._-]|$)', u.rsplit('/', 1)[-1] + '/' + u): s += 6   # full name as a file/folder slug
    if BROCHURE_WORDS.search(blob): s += 3
    if POLICY_WORDS.search(blob): s += 1
    if BAD_WORDS.search(blob): s -= 5
    if re.search(r'\bto\s+\d{1,2}[/.-]\d{1,2}[/.-]\d{2,4}|\bold\b|\bprevious\b|\barchive', text, re.I): s -= 3   # dated-out version (e.g. LIC 'From .. To ..')
    if re.search(r'onwards|latest|revised', text, re.I): s += 1
    if re.search(r'[-_/]live/', u): s += 2                                  # HDFC '...-live/' folders hold current files
    return s

def pdf_text(p):
    return subprocess.run(['pdftotext', '-layout', p, '-'], capture_output=True, text=True).stdout

WRONG_KIND = re.compile(r'customer information sheet|know your policy|benefit illustration|illustration of benefits|proposal form|'
                        r'mortality (rate|charge)s? (table|for)|fund fact ?sheet|premium rate(s)? table|annuity rate(s)? table|surrender value factor', re.I)
def doc_kind_problem(txt, prod):
    """Why this is not the product's brochure/policy document ('' if it looks right)."""
    pages = txt.split('\f')
    top = re.sub(r'\s+', ' ', ' '.join(pages[:2]))[:250]                 # titles only: brochures mention 'proposal form' in body text
    if WRONG_KIND.search(top): return 'looks like ' + WRONG_KIND.search(top).group(0).lower()
    toks = name_tokens(prod['product_name'])
    z = lambda x: x.replace('z', 's')                                   # Maximizer / Maximiser
    flat = z(' '.join(pages[:4]).lower().replace('\u2019', "'").replace("'", ''))
    words = set(re.findall(r'[a-z0-9]+', flat))
    need = -(-2 * len(toks) // 3)            # about two thirds of the name words (whole word, or a 5+ letter part of one)
    if toks and sum(1 for t in map(z, toks) if t in words or (len(t) >= 5 and t in flat)) < need:
        return 'product name not on first 4 pages'
    return ''

RIDER = re.compile(r'rider|benefit rider', re.I)
def find_desc(txt, pdf=None):
    """First description line in the first 3 pages (else anywhere) that is not a rider's line.
    Layout text first; then plain pdftotext output, which keeps two-column pages in reading order."""
    raw = subprocess.run(['pdftotext', pdf, '-'], capture_output=True, text=True).stdout if pdf and os.path.exists(pdf) else ''
    for part in (' '.join(txt.split('\f')[:3]), ' '.join(raw.split('\f')[:3]), txt, raw):
        flat = re.sub(r'\s+', ' ', part)
        for m in DESC.finditer(flat):
            d = m.group(0).strip()
            if not RIDER.search(d) and re.search(r'individual|life|pension|annuity|savings|term|risk|health|protection|endowment|micro', d, re.I): return d
    return ''

def tess(png):
    try: return subprocess.run(['tesseract', png, '-'], capture_output=True, text=True, timeout=120).stdout
    except subprocess.TimeoutExpired: return ''

def ocr_text(pdf, dpi='300'):
    """Full-document OCR (pdftoppm + tesseract), pages separated by form feeds like pdftotext."""
    import tempfile, glob
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(['pdftoppm', '-r', dpi, '-scale-to', str(int(dpi) * 12), '-png', pdf, os.path.join(d, 'p')], capture_output=True)
        return '\f'.join(tess(f) for f in sorted(glob.glob(os.path.join(d, 'p*.png'))))

def ocr_desc(pdf, pages=3):
    """Description line printed inside an image: OCR the first pages (tesseract) and search them.
    Tries 400 dpi, then 200 dpi (each misreads some layouts)."""
    import tempfile, glob
    for dpi in ('400', '200'):
        with tempfile.TemporaryDirectory() as d:
            subprocess.run(['pdftoppm', '-f', '1', '-l', str(pages), '-r', dpi, '-scale-to', str(int(dpi) * 12), '-png', pdf,
                            os.path.join(d, 'p')], capture_output=True)   # cap: huge pages would stall tesseract
            txt = '\f'.join(tess(f) for f in sorted(glob.glob(os.path.join(d, 'p*.png'))))
        desc = find_desc(txt)
        if desc and classify_desc(desc)[0] != 'not stated' or desc and 'unit' in desc.lower(): return desc
    return desc

def classify_desc(desc):
    d = re.sub(r'\s*[\u2010-\u2015-]\s*', '-', desc.lower())
    par = 'Non-Par' if re.search(r'non[\s-]*(participating|par\b)', d) else ('Par' if re.search(r'participating|\bpar\b', d) else 'not stated')
    linked = 'Linked' if re.search(r'unit[\s-]*linked|(?<!non[\s-])linked', d) and not re.search(r'non[\s-]*linked', d) else 'Non-Linked'
    ptype = next((t for t in ['pension', 'immediate annuity', 'deferred annuity', 'annuity', 'pure risk', 'term', 'protection', 'health',
                              'micro', 'savings', 'endowment', 'whole life', 'money back', 'variable']
                  if t in d), 'not stated')
    return par, linked, ptype

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--insurer', default='all'); ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--dry-run', action='store_true'); ap.add_argument('--skip-blocked', action='store_true')
    ap.add_argument('--tmp', default='/tmp/ld_cache')
    ap.add_argument('--results', default='results/light_discovery_results.csv', help='results file (use one per parallel process, then --merge)')
    ap.add_argument('--merge', nargs='*', help='merge these results files into --results and rebuild the manual checklist, then exit')
    ap.add_argument('--only', default='', help='comma list of row_ids to process (others untouched)')
    ap.add_argument('--reextract', action='store_true', help='recompute description lines and keyword hits from stored text')
    ap.add_argument('--redo', default='', help='comma list of row_ids to clear (result, index row, stored files) and fetch again')
    a = ap.parse_args(); os.makedirs(a.tmp, exist_ok=True); os.makedirs('results', exist_ok=True)
    M = list(csv.DictReader(open('master_list.csv')))
    resf = a.results
    idx_cols = open('index.csv').readline().strip().split(',')
    done = {r['row_id']: r for r in csv.DictReader(open(resf))} if os.path.exists(resf) else {}
    if a.reextract:   # recompute description line / flags / keyword hits from stored text, no downloads
        for r in done.values():
            if r['status'] != 'ok' or a.insurer not in ('all', next((m['insurer_slug'] for m in M if m['row_id'] == r['row_id']), '')): continue
            ix = next((x for x in csv.DictReader(open('index.csv')) if x['uin'] == r['uin'] and x['product_name'] == r['product_name']), None)
            if not ix or not os.path.exists(ix['text_path']): continue
            txt = open(ix['text_path']).read()
            desc = find_desc(txt, ix['file_path'])
            note = 'description line read by OCR from page image'
            if not desc:
                desc = ocr_desc(ix['file_path'])
                if desc and note not in r['notes']: r['notes'] = '; '.join(x for x in (r['notes'], note) if x)
            elif note in r['notes']:
                r['notes'] = '; '.join(x for x in r['notes'].split('; ') if x != note)
            par, linked, ptype = classify_desc(desc) if desc else ('', '', '')
            r.update(irdai_description_line=desc, par_flag_stated=par, linked_stated=linked, plan_type_stated=ptype,
                     features_keyword_hits=' '.join(k for k, rx in FEATURES.items() if re.search(rx, txt, re.I)))
        rows = list(csv.DictReader(open('index.csv')))
        for x in rows:
            r = next((v for v in done.values() if v['uin'] == x['uin'] and v['product_name'] == x['product_name'] and v['status'] == 'ok'), None)
            if r: x['irdai_description_line'] = r['irdai_description_line']; x['par_flag'] = r['par_flag_stated']; x['notes'] = r['notes']
        write_index(rows, idx_cols)
        save(resf, done, M, checklist=(resf == 'results/light_discovery_results.csv')); return
    if a.merge is not None:
        slug_of = {m['row_id']: m['insurer_slug'] for m in M}
        for f in a.merge:
            own = os.path.basename(f).rsplit('.', 1)[0]           # <slug>.csv: take only that insurer's rows
            for r in csv.DictReader(open(f)):
                if own in slug_of.values() and slug_of.get(r['row_id']) != own: continue
                if r['status'] == 'ok' or done.get(r['row_id'], {}).get('status') != 'ok': done[r['row_id']] = r
        save(resf, done, M); return
    idx_cols = open('index.csv').readline().strip().split(',')
    for rid in [x for x in a.redo.split(',') if x]:
        old = done.pop(rid, None)
        if not old: continue
        rows = list(csv.DictReader(open('index.csv')))
        drop = [r for r in rows if r['uin'] == old['uin'] and r['product_name'] == old['product_name']]
        keep = [r for r in rows if r not in drop]
        for r in drop:   # delete the stored file only if no other index row points to it
            if not any(k['file_path'] == r['file_path'] for k in keep):
                for f in (r['file_path'], r['text_path']):
                    if f and os.path.exists(f): os.remove(f)
        write_index(keep, idx_cols)
    targets = [r for r in M if (a.insurer == 'all' or r['insurer_slug'] in a.insurer.split(','))
               and not (a.skip_blocked and r['insurer_slug'] in BLOCKED) and done.get(r['row_id'], {}).get('status') != 'ok']
    if a.only: targets = [r for r in targets if r['row_id'] in a.only.split(',')]
    if a.limit: targets = targets[:a.limit]
    for prod in targets:
        slug = prod['insurer_slug']; now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        res = {'row_id': prod['row_id'], 'insurer': prod['insurer'], 'product_name': prod['product_name'], 'uin': prod['uin'],
               'status': '', 'doc_type': '', 'source_url': '', 'found_on_page_url': '', 'uin_in_document': '', 'irdai_description_line': '',
               'par_flag_stated': '', 'linked_stated': '', 'plan_type_stated': '', 'pages': '', 'features_keyword_hits': '', 'notes': '', 'checked_utc': now}
        if slug in BLOCKED:
            res.update(status='manual', notes='site blocks automated access'); done[prod['row_id']] = res; continue
        pages = [u for u in [prod.get('website_product_page_url', '')] if u] + SEEDS.get(slug, [])
        cands = {}
        prod_pages = set(pages[:1])
        for pg in pages:
            for u, t in page_links(pg, a.tmp):
                doclike = u.lower().split('?')[0].endswith('.pdf') or BROCHURE_WORDS.search(u + ' ' + t) or POLICY_WORDS.search(u + ' ' + t)
                if doclike and urllib.parse.urlparse(u).scheme in ('http', 'https'):
                    sc = score(u, t, prod, on_product_page=(pg in prod_pages))
                    if u not in cands or sc > cands[u][0]: cands[u] = (sc, pg, t)
            # also follow the product's own page if a seed page links to it by name (one hop)
            if pg in SEEDS.get(slug, []):
                toks = name_tokens(prod['product_name'])
                for u, t in page_links(pg, a.tmp):
                    if toks and not u.lower().endswith('.pdf') and not BROCHURE_WORDS.search(u) and sum(1 for k in toks if k in (u + ' ' + t).lower()) >= max(1, len(toks) - 1) \
                            and urllib.parse.urlparse(u).netloc == urllib.parse.urlparse(pg).netloc and u not in pages and len(pages) < 8:
                        pages.append(u); prod_pages.add(u)
        allr = sorted(((v[0], u, v[1], v[2]) for u, v in cands.items() if v[0] >= 4), reverse=True)
        is_pol = lambda u, t: bool(POLICY_WORDS.search(urllib.parse.unquote(u) + ' ' + t)) and not BROCHURE_WORDS.search(urllib.parse.unquote(u) + ' ' + t)
        # brochures first; a policy document only as a fallback (brief: same description line)
        ranked = [x for x in allr if not is_pol(x[1], x[3])][:8] + [x for x in allr if is_pol(x[1], x[3])][:3]
        if a.dry_run:
            print(prod['product_name'], prod['uin'], '->', [(round(s, 1), u[-80:]) for s, u, _, _ in ranked]); continue
        ok = False; big = ''; ocr_tries = 0
        for sc, u, pg, t in ranked:
            tmp = os.path.join(a.tmp, 'dl.pdf')
            code, eff = fetch(u, tmp)
            body = open(tmp, 'rb').read() if os.path.exists(tmp) else b''
            if code != 200 or body[:4] != b'%PDF': continue
            txt = pdf_text(tmp); ocr_used = ''
            npg = re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', tmp], capture_output=True, text=True).stdout)
            npg = int(npg.group(1)) if npg else 1
            code_seen = prod['product_code'] and re.search(''.join('[0O]' if c == '0' else c for c in prod['product_code']), re.sub(r'\s+', '', txt))
            scanned_like = len(txt.strip()) / npg < 200
            if npg <= 60 and ocr_tries < 2 and sc >= 9 and (scanned_like or (not code_seen and len(txt.strip()) / npg < 1500)):
                ocr_tries += 1                                        # one OCR attempt per product, strong candidates only
                txt = ocr_text(tmp, '200')                                   # scanned / image-heavy: read it by OCR
                ocr_used = 'scanned - text by OCR' if len(pdf_text(tmp).strip()) / npg < 200 else 'UIN and text read by OCR (image-heavy PDF)'
            flat = re.sub(r'\s+', '', txt)
            code_rx = ''.join('[0O]' if c == '0' else c for c in prod['product_code']) + r'V\d{2}'   # some PDFs print letter O for zero
            raw_uins = sorted(set(re.findall(code_rx, flat))) if prod['product_code'] else []
            uins = sorted(set(x[:4] + x[4:].replace('O', '0') for x in raw_uins))
            o_note = f"UIN printed as {','.join(x for x in raw_uins if 'O' in x[4:])} (letter O for zero)" if any('O' in x[4:] for x in raw_uins) else ''
            if prod['product_code'] and not uins: continue            # wrong document: product code not in text
            if doc_kind_problem(txt, prod): continue                  # CIS / BI / rate table / rider / other product
            if len(body) > 95 * 1024 * 1024:
                big = u; continue                                     # CLAUDE.md: never add a file over 95 MB
            if subprocess.run(['pdfinfo', tmp], capture_output=True).returncode != 0: continue   # pdfinfo must open it
            doc_type = 'brochure' if BROCHURE_WORDS.search(urllib.parse.unquote(u) + ' ' + t) or not POLICY_WORDS.search(urllib.parse.unquote(u) + ' ' + t) else 'policy'
            uin_dir = prod['uin'] or ('NOUIN-' + re.sub(r'[^a-z0-9]+', '-', prod['product_name'].lower())[:40])
            d_doc = os.path.join('docs', slug, uin_dir); d_txt = os.path.join('text', slug, uin_dir)
            os.makedirs(d_doc, exist_ok=True); os.makedirs(d_txt, exist_ok=True)
            fp = os.path.join(d_doc, doc_type + '.pdf'); tp = os.path.join(d_txt, doc_type + '.txt')
            sha = hashlib.sha256(body).hexdigest()
            dup = next((r for r in csv.DictReader(open('index.csv')) if r['sha256'] == sha and r['file_path']), None)
            if dup:                                                   # sha256 dedupe: one stored file, two index rows
                fp, tp = dup['file_path'], dup['text_path']
            else:
                open(fp, 'wb').write(body)
            pages_n = re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', fp], capture_output=True, text=True).stdout)
            pages_n = int(pages_n.group(1)) if pages_n else 0
            scanned = 'Y' if ocr_used.startswith('scanned') else 'N'
            if not dup: open(tp, 'w').write(txt)
            desc = find_desc(txt, fp); ocr_note = ''
            if not desc:
                desc = ocr_desc(fp); ocr_note = 'description line read by OCR from page image' if desc else ''
            par, linked, ptype = classify_desc(desc) if desc else ('', '', '')
            hits = [k for k, rx in FEATURES.items() if re.search(rx, txt, re.I)]
            row = {c: '' for c in idx_cols}
            row.update({'doc_id': f"{uin_dir}-{doc_type}", 'insurer': prod['insurer'], 'product_name': prod['product_name'], 'uin': prod['uin'],
                        'linked_flag': prod['linked_flag_uin'], 'par_flag': par, 'irdai_description_line': desc, 'market_category': '',
                        'pd_category': '', 'doc_type': doc_type, 'source_url': eff or u, 'found_on_page_url': pg, 'download_date_utc': now,
                        'http_status': code, 'sha256': hashlib.sha256(body).hexdigest(), 'bytes': len(body), 'pages': pages_n,
                        'is_scanned': scanned, 'file_path': fp, 'text_path': tp, 'status': 'ok',
                        'notes': '; '.join(x for x in [('' if prod['uin'] in uins else f"document shows {','.join(uins)}"),
                                                     ocr_used, o_note, ocr_note,
                                                     ('brochure not verified (UIN missing/different); policy document used' if doc_type == 'policy' else ''),
                                                     (f"same file as {dup['doc_id']}" if dup else '')] if x)})
            with open('index.csv', 'a', newline='') as fh: csv.DictWriter(fh, fieldnames=idx_cols).writerow(row)
            res.update(status='ok', doc_type=doc_type, source_url=eff or u, found_on_page_url=pg, uin_in_document=','.join(uins),
                       irdai_description_line=desc, par_flag_stated=par, linked_stated=linked, plan_type_stated=ptype, pages=pages_n,
                       features_keyword_hits=' '.join(hits), notes=row['notes'])
            ok = True; break
        if not ok:
            res.update(status='manual' if big else 'not found',
                       notes=(f'file over 95 MB, download by hand: {big}' if big else
                              f'{len(cands)} PDF links seen on {len(pages)} pages; none verified (product code not in text or no match)'))
        done[prod['row_id']] = res
        save(resf, done, M, checklist=False)
        print(f"{res['status']:9} {slug:16} {prod['uin']:11} {prod['product_name'][:45]:45} {res['irdai_description_line'][:70]}", flush=True)
    if a.dry_run: return
    save(resf, done, M, checklist=(resf == 'results/light_discovery_results.csv'))

def write_index(rows, cols):
    """Rewrite index.csv via a temp file, so a crash can never leave it empty."""
    with open('index.csv.tmp', 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)
    os.replace('index.csv.tmp', 'index.csv')

def save(resf, done, M, checklist=True):
    cols = list(next(iter(done.values())).keys()) if done else []
    order = {m['row_id']: i for i, m in enumerate(M)}
    rows = sorted(done.values(), key=lambda r: order.get(r['row_id'], 1e9))
    with open(resf + '.tmp', 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)
    os.replace(resf + '.tmp', resf)
    if not checklist: return
    with open('results/manual_checklist.csv', 'w', newline='') as fh:
        w = csv.writer(fh); w.writerow(['insurer', 'product_name', 'uin', 'reason', 'where_to_look'])
        for r in done.values():
            if r['status'] != 'ok':
                p = next((m for m in M if m['row_id'] == r['row_id']), {})
                w.writerow([r['insurer'], r['product_name'], r['uin'], r['notes'],
                            p.get('website_product_page_url') or (SEEDS.get(p.get('insurer_slug', ''), ['insurer website'])[0] if SEEDS.get(p.get('insurer_slug', '')) else 'insurer website')])

if __name__ == '__main__':
    main()
