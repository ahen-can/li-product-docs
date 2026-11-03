"""Turn fetched website pages into website product rows.
Usage: analyze_site.py <S> <out.csv>
Rules:
 - product pages (type=product): product UIN = the insurer-prefix N/L UIN code that occurs most often on the page
   (ties -> highest version). Name = og:title / h1 / <title>. Status 'current' (a live product page).
 - listing pages (type current*): every insurer-prefix N/L UIN found -> status 'current-listed' with surrounding text.
 - withdrawn pages: every UIN found -> status 'withdrawn' with surrounding text; text lines kept for name matching.
 - IRDAI description line captured verbatim when the page contains one.
Category is NEVER inferred from names: only the verbatim description line / site category text is recorded."""
import sys, os, re, json, glob, csv, collections, datetime

S, OUT = sys.argv[1], sys.argv[2]
PREFIX = {'lic': '512', 'sbi-life': '111', 'hdfc-life': '101', 'icici-life': '105', 'axis-max-life': '104', 'tata-aia': '110',
          'bajaj-life': '116', 'absli': '109', 'kotak-life': '107', 'pnb-metlife': '117', 'canara-hsbc': '136', 'indiafirst': '143',
          'sud-life': '142', 'indusind-nippon': '121', 'shriram-life': '128', 'ageas-federal': '135', 'generali-central': '133',
          'bharti-life': '130', 'edelweiss-life': '147', 'pramerica-life': '140', 'aviva-life': '122', 'bandhan-life': '138',
          'go-digit-life': '165', 'acko-life': '164', 'creditaccess-life': '163'}
DESC = re.compile(r'(?:an?\s+)?(?:unit[\s-]*linked|non[\s-]*linked|linked)[ ,]+(?:non[\s-]*participating|participating|non[\s-]*par|par)?[^.\n]{0,160}?'
                  r'(?:savings|protection|term|annuity|pension|endowment|whole life|money back|insurance)\s*(?:plan|product)', re.I)

def uin_re(pre): return re.compile(pre + r'\s*([NL])\s*(\d{3})\s*V\s*(\d{2})', re.I)

rows = []; NOUIN = []
for slug, pre in PREFIX.items():
    U = uin_re(pre)
    files = sorted(glob.glob(f'{S}/sites/{slug}/text/*.json'))
    pagecount = collections.Counter(); nprod = 0
    for f in files:
        r = json.load(open(f))
        if r.get('type') != 'product' or r.get('status') != 200: continue
        nprod += 1
        b = r.get('text', '')
        for c in {f'{pre}{a.upper()}{x}' for a, x, _ in U.findall(b)}: pagecount[c] += 1
    def nurl(u): return re.sub(r'^https?://(www\.)?', '', u.split('#')[0].split('?')[0]).rstrip('/').lower()
    LINKED = set()
    for f in files:
        r = json.load(open(f))
        if 'current' in r.get('type', '') and r.get('status') == 200:
            LINKED |= {nurl(u) for u, _ in r.get('links', [])}
    BOILER = {c for c, n in pagecount.items() if nprod >= 8 and n >= 5 and n > 0.3 * nprod}
    if BOILER: print(slug, 'boilerplate codes ignored:', sorted(BOILER))
    for f in files:
        r = json.load(open(f))
        if r.get('status') != 200:
            continue
        txt = r.get('text', ''); blob = txt + ' ' + r.get('script_text', '') + ' ' + ' '.join(u for u, _ in r.get('links', []))
        found = [f'{pre}{a.upper()}{b}V{c}' for a, b, c in U.findall(blob)]
        if r.get('type') == 'product':
            found = [f'{pre}{a.upper()}{b}V{c}' for a, b, c in U.findall(txt)]
            found_nb = [u for u in found if u[:7] not in BOILER]
            if not found_nb:
                nm = (r.get('og_title') or (r.get('h1') or [''])[0] or r.get('title') or '').strip()
                NOUIN.append({'slug': slug, 'page_url': r.get('final_url') or r['url'], 'name_site': nm[:150], 'h1': ' | '.join(r.get('h1') or [])[:150],
                              'fetched_utc': r.get('fetched_utc', ''), 'withdrawn_hint': bool(re.search(r'withdrawn|discontinued', nm + ' '.join(r.get('h1') or []), re.I))})
        if not found:
            continue
        typ = r.get('type', '')
        desc = DESC.search(txt)
        desc = re.sub(r'\s+', ' ', desc.group(0)).strip() if desc else ''
        base = {'slug': slug, 'page_url': r.get('final_url') or r['url'], 'page_type': typ, 'fetched_utc': r.get('fetched_utc', '')}
        if typ == 'product':
            codes = collections.Counter(u[:7] for u in found if u[:7] not in BOILER)
            title_all = ' '.join([r.get('og_title', ''), r.get('title', '')] + (r.get('h1') or []))
            if not codes:
                continue
            top, n = codes.most_common(1)[0]
            if len(codes) > 4 and n < 3:   # page lists many products (article/listing) -> treat as listing
                typ = 'current-listing-like'
            else:
                ver = max(u for u in found if u[:7] == top)
                name = (r.get('og_title') or (r.get('h1') or [''])[0] or r.get('title') or '').strip()
                st = 'withdrawn' if re.search(r'withdrawn|discontinued', title_all, re.I) else (
                    'current' if nurl(base['page_url']) in LINKED or nurl(r['url']) in LINKED else 'page live, not in current plan listings')
                rows.append({**base, 'uin': ver, 'name_site': name[:150], 'status_site': st,
                             'context': '', 'irdai_description_line': desc[:200], 'other_codes_on_page': ' '.join(sorted(set(codes) - {top}))[:120]})
                continue
        status = 'withdrawn' if typ == 'withdrawn' else ('listed, status not stated' if '+' in typ else 'current-listed')
        if re.search(r'form|brochure|download|resource', base['page_url'], re.I) and typ != 'withdrawn':
            status = 'listed, status not stated'
        if slug == 'tata-aia' and '+' in typ:
            # IRDAI-format table: ... name, UIN, open date, [close date], status
            L = [x.strip() for x in txt.split('\n')]
            for i, ln in enumerate(L):
                m = re.fullmatch(pre + r'([NL])(\d{3})V(\d{2})', ln)
                if not m: continue
                tail = ' '.join(L[i + 1:i + 4]); name = L[i - 1] if i else ''
                st = 'withdrawn' if re.search(r'withdrawn', tail, re.I) else 'current-listed'
                rows.append({**base, 'uin': ln, 'name_site': name[:150], 'status_site': st, 'context': (name + ' | ' + tail)[:220],
                             'irdai_description_line': '', 'other_codes_on_page': ''})
            continue
        lines = txt.split('\n')
        for u in sorted(set(found)):
            ctx = ''
            for i, ln in enumerate(lines):
                if U.search(ln) and ''.join(U.search(ln).groups()).upper() == u[3:].replace('V', ''):
                    pass
                m = U.search(ln)
                if m and f'{pre}{m.group(1).upper()}{m.group(2)}V{m.group(3)}' == u:
                    ctx = ' | '.join(x.strip() for x in lines[max(0, i - 2):i + 2] if x.strip())[:220]
                    break
            rows.append({**base, 'uin': u, 'name_site': '', 'status_site': status, 'context': ctx,
                         'irdai_description_line': '', 'other_codes_on_page': ''})
with open(OUT.replace('.csv', '_nouin_pages.csv'), 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=['slug', 'page_url', 'name_site', 'h1', 'fetched_utc', 'withdrawn_hint']); w.writeheader(); w.writerows(NOUIN)
with open(OUT, 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
c = collections.Counter((r['slug'], r['status_site']) for r in rows)
for s in PREFIX:
    print(f"{s:18}", {k[1]: v for k, v in c.items() if k[0] == s})
