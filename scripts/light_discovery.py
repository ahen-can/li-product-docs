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
    'hdfc-life': ['https://www.hdfclife.com/life-insurance-plans'],
    'axis-max-life': ['https://www.axismaxlife.com/all-insurance-plans'],
    'tata-aia': ['https://www.tataaia.com/active-and-withdrawn-product-status.html'],
    'bajaj-life': ['https://www.bajajlifeinsurance.com/on-sale-plans.html'],
    'absli': ['https://lifeinsurance.adityabirlacapital.com/forms-and-downloads/brochures-and-specimen-contracts/'],
    'pnb-metlife': ['https://www.pnbmetlife.com/life-insurance-plans.html', 'https://www.pnbmetlife.com/downloads.html'],
    'canara-hsbc': ['https://www.canarahsbclife.com/product-list'],
    'indiafirst': ['https://www.indiafirstlife.com/life-insurance-plans'],
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
    'acko-life': ['https://www.acko.com/life-insurance/'],
    'creditaccess-life': ['https://www.creditaccesslife.in/savings_product.php'],
}
BROCHURE_WORDS = re.compile(r'brochure|sales[-_ ]?lit|prospectus|leaflet|\bsl\b|_sl_|-sl-|one[-_ ]?pager|product[-_ ]?info', re.I)
POLICY_WORDS = re.compile(r'policy[-_ ]?(doc|wording|bond|contract)|terms[-_ ]?and[-_ ]?conditions|specimen|\bpd\b|_pd_|-pd-', re.I)
BAD_WORDS = re.compile(r'hindi|marathi|tamil|telugu|kannada|gujarati|bengali|malayalam|odia|punjabi|regional|claim|form|proposal|'
                       r'fund[-_ ]?fact|factsheet|newsletter|withdrawn|rider', re.I)
DESC = re.compile(r'(?:an?\s+)?(?:unit[\s-]*linked|non[\s-]*linked|linked)[\s,]+(?:(?:non[\s-]*participating|participating|non[\s-]*par\b|par\b)[\s,]+)?'
                  r'(?:individual|group)?[^.]{0,120}?(?:plan|product)\b', re.I)
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
        for m in re.finditer(r'href=["\']([^"\'#]+)["\'][^>]*>(.*?)</a>', t, re.S | re.I):
            links.append((urllib.parse.urljoin(eff or url, html.unescape(m.group(1)).strip()),
                          re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', m.group(2)))).strip()[:120]))
        for m in re.finditer(r'["\']((?:https?:)?//[^"\'\s]+?\.pdf|/[^"\'\s]+?\.pdf)["\']', t, re.I):   # PDFs referenced in scripts/data
            links.append((urllib.parse.urljoin(eff or url, m.group(1)), ''))
    _page_cache[url] = links
    return links

def name_tokens(name):
    n = re.sub(r"lic'?s|life|insurance|plan|the|sbi|hdfc|icici|bharti|axa|tata|aia|bajaj|absli|kotak|pnb|metlife|canara|hsbc|"
               r"indiafirst|sud|indusind|nippon|shriram|ageas|federal|generali|central|edelweiss|pramerica|aviva|bandhan|axis|max", ' ', name.lower())
    return [w for w in re.findall(r'[a-z0-9]+', n) if len(w) > 2]

def score(url, text, prod, on_product_page=False):
    s = 0; u = urllib.parse.unquote(url).lower(); blob = u + ' ' + text.lower()
    if on_product_page and text and BROCHURE_WORDS.search(blob): s += 6     # 'Brochure' anchor on the product's own page
    if on_product_page and text and POLICY_WORDS.search(blob): s += 4       # 'Policy document' anchor on the product's own page
    code = prod['product_code'].lower()
    if code and code in blob.replace(' ', ''): s += 6
    if prod['uin'] and prod['uin'].lower() in blob.replace(' ', ''): s += 2
    toks = name_tokens(prod['product_name'])
    if toks: s += 4 * sum(1 for t in toks if t in blob) / len(toks)
    if BROCHURE_WORDS.search(blob): s += 3
    if POLICY_WORDS.search(blob): s += 1
    if BAD_WORDS.search(blob): s -= 5
    return s

def pdf_text(p):
    return subprocess.run(['pdftotext', '-layout', p, '-'], capture_output=True, text=True).stdout

def classify_desc(desc):
    d = desc.lower()
    par = 'Non-Par' if re.search(r'non[\s-]*(participating|par\b)', d) else ('Par' if re.search(r'participating|\bpar\b', d) else 'not stated')
    linked = 'Linked' if re.search(r'unit[\s-]*linked|(?<!non[\s-])linked', d) and not re.search(r'non[\s-]*linked', d) else 'Non-Linked'
    ptype = next((t for t in ['pension', 'annuity', 'term', 'protection', 'health', 'savings', 'endowment', 'whole life', 'money back']
                  if t in d), 'not stated')
    return par, linked, ptype

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--insurer', default='all'); ap.add_argument('--limit', type=int, default=0)
    ap.add_argument('--dry-run', action='store_true'); ap.add_argument('--skip-blocked', action='store_true')
    ap.add_argument('--tmp', default='/tmp/ld_cache')
    ap.add_argument('--redo', default='', help='comma list of row_ids to clear (result, index row, stored files) and fetch again')
    a = ap.parse_args(); os.makedirs(a.tmp, exist_ok=True); os.makedirs('results', exist_ok=True)
    M = list(csv.DictReader(open('master_list.csv')))
    resf = 'results/light_discovery_results.csv'
    done = {r['row_id']: r for r in csv.DictReader(open(resf))} if os.path.exists(resf) else {}
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
        with open('index.csv', 'w', newline='') as fh:
            w = csv.DictWriter(fh, fieldnames=idx_cols); w.writeheader(); w.writerows(keep)
    targets = [r for r in M if (a.insurer == 'all' or r['insurer_slug'] in a.insurer.split(','))
               and not (a.skip_blocked and r['insurer_slug'] in BLOCKED) and done.get(r['row_id'], {}).get('status') != 'ok']
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
        ranked = [x for x in allr if not is_pol(x[1], x[3])][:5] + [x for x in allr if is_pol(x[1], x[3])][:3]
        if a.dry_run:
            print(prod['product_name'], prod['uin'], '->', [(round(s, 1), u[-80:]) for s, u, _, _ in ranked]); continue
        ok = False; big = ''
        for sc, u, pg, t in ranked:
            tmp = os.path.join(a.tmp, 'dl.pdf')
            code, eff = fetch(u, tmp)
            body = open(tmp, 'rb').read() if os.path.exists(tmp) else b''
            if code != 200 or body[:4] != b'%PDF': continue
            txt = pdf_text(tmp); flat = re.sub(r'\s+', '', txt)
            code_rx = ''.join('[0O]' if c == '0' else c for c in prod['product_code']) + r'V\d{2}'   # some PDFs print letter O for zero
            raw_uins = sorted(set(re.findall(code_rx, flat))) if prod['product_code'] else []
            uins = sorted(set(x[:4] + x[4:].replace('O', '0') for x in raw_uins))
            o_note = f"UIN printed as {','.join(x for x in raw_uins if 'O' in x[4:])} (letter O for zero)" if any('O' in x[4:] for x in raw_uins) else ''
            if prod['product_code'] and not uins: continue            # wrong document: product code not in text
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
            scanned = 'Y' if pages_n and len(txt.strip()) / pages_n < 200 else 'N'
            if not dup: open(tp, 'w').write(txt)
            first = re.sub(r'\s+', ' ', ' '.join(txt.split('\f')[:3]))
            m = DESC.search(first) or DESC.search(re.sub(r'\s+', ' ', txt))
            desc = re.sub(r'\s+', ' ', m.group(0)).strip() if m else ''
            par, linked, ptype = classify_desc(desc) if desc else ('', '', '')
            hits = [k for k, rx in FEATURES.items() if re.search(rx, txt, re.I)]
            row = {c: '' for c in idx_cols}
            row.update({'doc_id': f"{uin_dir}-{doc_type}", 'insurer': prod['insurer'], 'product_name': prod['product_name'], 'uin': prod['uin'],
                        'linked_flag': prod['linked_flag_uin'], 'par_flag': par, 'irdai_description_line': desc, 'market_category': '',
                        'pd_category': '', 'doc_type': doc_type, 'source_url': eff or u, 'found_on_page_url': pg, 'download_date_utc': now,
                        'http_status': code, 'sha256': hashlib.sha256(body).hexdigest(), 'bytes': len(body), 'pages': pages_n,
                        'is_scanned': scanned, 'file_path': fp, 'text_path': tp, 'status': 'ok',
                        'notes': '; '.join(x for x in [('' if prod['uin'] in uins else f"document shows {','.join(uins)}"),
                                                     ('scanned - OCR needed' if scanned == 'Y' else ''), o_note,
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
        print(f"{res['status']:9} {slug:16} {prod['uin']:11} {prod['product_name'][:45]:45} {res['irdai_description_line'][:70]}", flush=True)
    if a.dry_run: return
    cols = list(next(iter(done.values())).keys()) if done else []
    with open(resf, 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(done.values())
    with open('results/manual_checklist.csv', 'w', newline='') as fh:
        w = csv.writer(fh); w.writerow(['insurer', 'product_name', 'uin', 'reason', 'where_to_look'])
        for r in done.values():
            if r['status'] != 'ok':
                p = next((m for m in M if m['row_id'] == r['row_id']), {})
                w.writerow([r['insurer'], r['product_name'], r['uin'], r['notes'],
                            p.get('website_product_page_url') or (SEEDS.get(p.get('insurer_slug', ''), ['insurer website'])[0] if SEEDS.get(p.get('insurer_slug', '')) else 'insurer website')])

if __name__ == '__main__':
    main()
