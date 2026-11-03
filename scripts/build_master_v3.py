"""Master list v3: Council (Sep-2026) backbone + official insurer lists + SBI/Bajaj from websites.
No category inferred from names. Usage: build_master_v3.py <S> <repo>"""
import csv, json, re, sys, os, collections, openpyxl

S, R = sys.argv[1], sys.argv[2]
UIN = re.compile(r'^\d{3}[A-Z]\d{3}V\d{2}$')
NAME = {'101': 'HDFC Life', '104': 'Axis Max Life', '105': 'ICICI Life', '107': 'Kotak Mahindra Life', '109': 'Aditya Birla Sun Life',
        '110': 'Tata AIA Life', '111': 'SBI Life', '116': 'Bajaj Life', '117': 'PNB MetLife', '121': 'IndusInd Nippon Life', '122': 'Aviva Life',
        '128': 'Shriram Life', '130': 'Bharti Life', '133': 'Generali Central Life', '135': 'Ageas Federal Life', '136': 'Canara HSBC Life',
        '138': 'Bandhan Life', '140': 'Pramerica Life', '142': 'Star Union Dai-ichi Life', '143': 'IndiaFirst Life', '147': 'Edelweiss Life',
        '163': 'CreditAccess Life', '164': 'Acko Life', '165': 'Go Digit Life', '512': 'LIC'}
SLUG = {'101': 'hdfc-life', '104': 'axis-max-life', '105': 'icici-life', '107': 'kotak-life', '109': 'absli', '110': 'tata-aia', '111': 'sbi-life',
        '116': 'bajaj-life', '117': 'pnb-metlife', '121': 'indusind-nippon', '122': 'aviva-life', '128': 'shriram-life', '130': 'bharti-life',
        '133': 'generali-central', '135': 'ageas-federal', '136': 'canara-hsbc', '138': 'bandhan-life', '140': 'pramerica-life', '142': 'sud-life',
        '143': 'indiafirst', '147': 'edelweiss-life', '163': 'creditaccess-life', '164': 'acko-life', '165': 'go-digit-life', '512': 'lic'}
BLOCKED = {'105', '107', '142', '165'}
OUT_SCOPE = re.compile(r'health|accident|micro', re.I)

# website evidence (v2) for product page URLs
v2 = {r['product_code']: r for r in csv.DictReader(open(os.path.join(R, 'master_list.csv')))}
rows = []

def add(uin, name, source, council_cat='', council_lob='', page='', desc='', note='', pre=None):
    pre = pre or (uin[:3] if uin else '')
    rows.append({'insurer': NAME.get(pre, ''), 'insurer_slug': SLUG.get(pre, ''), 'product_name': name.strip(), 'uin': uin,
                 'product_code': uin[:7] if uin else '', 'linked_flag_uin': uin[3] if uin else '', 'council_category': council_cat,
                 'council_line_of_business': council_lob, 'list_source': source,
                 'standard_or_pos_tag': 'Saral (IRDAI standard)' if re.search(r'\bsaral\b', name, re.I) else ('POS' if re.search(r'\bPOS\b', name) else ''),
                 'website_product_page_url': page, 'website_blocked': 'Y' if pre in BLOCKED else '',
                 'brochure_url': '', 'irdai_description_line': desc, 'par_flag': '', 'market_category': '', 'pd_category': '',
                 'notes': note})

# 1) Council individual products (not ICICI / Bharti: replaced by official lists)
council = [r for r in csv.DictReader(open(os.path.join(R, 'sources/life-council/council_rows_parsed.csv')))
           if r['section'] == 'Products' and r['lob'] == 'Individual' and r['uin'][3] in 'NL']
ccode = {r['uin'][:7]: r for r in council}
excluded = []
for r in council:
    if r['uin'][:3] in ('105', '130'):
        continue
    if OUT_SCOPE.search(r['category']):
        excluded.append((r['uin'], r['name'], r['category'])); continue
    ev = v2.get(r['uin'][:7], {})
    add(r['uin'], r['name'], 'Life Council Sep-2026', r['category'], r['lob'], (ev.get('website_source_urls') or '').split(' ')[0])

# 2) Official lists supplied by the user (ICICI, Bharti): current individual products
wb = openpyxl.load_workbook(os.path.join(R, 'sources/official-lists/icici_bharti_official_lists_0411.xlsx'), read_only=True)
ic = list(wb['icici'].iter_rows(values_only=True))
start = next(i for i, r in enumerate(ic) if r[1] and str(r[1]).strip() == 'Products (Individual)')
end = next(i for i, r in enumerate(ic) if i > start and r[1] and str(r[1]).strip() == 'Products (Group)')
for r in ic[start:end]:
    u = str(r[2]).strip() if r[2] else ''
    if UIN.match(u) and u[3] in 'NL':
        c = ccode.get(u[:7], {})
        if OUT_SCOPE.search(c.get('category', '')):
            excluded.append((u, str(r[1]), c['category'])); continue
        note = '' if c else 'Not on Council list (new product)'
        if c and c['uin'] != u: note = f"Council has {c['uin']}"
        add(u, str(r[1]), 'ICICI official list (user, 04-Nov)', c.get('category', ''), c.get('lob', ''), '', '', note)
for r in wb['bharti'].iter_rows(values_only=True):
    v = [x for x in r if x is not None]
    if len(v) >= 5 and str(v[1]).strip() == 'Retail' and UIN.match(str(v[4]).strip()):
        u, n = str(v[4]).strip(), str(v[3])
    elif len(v) >= 3 and UIN.match(str(v[2]).strip()) and str(v[2])[3] in 'NL' and 'group' not in str(v[1]).lower():
        u, n = str(v[2]).strip(), str(v[1])     # rows marked "New" without a Retail/Group label
    else:
        continue
    c = ccode.get(u[:7], {})
    if OUT_SCOPE.search(c.get('category', '')):
        excluded.append((u, n, c['category'])); continue
    ev = v2.get(u[:7], {})
    add(u, n, 'Bharti official list (user, 04-Nov)', c.get('category', ''), c.get('lob', ''), (ev.get('website_source_urls') or '').split(' ')[0],
        '', '' if c else 'Not on Council list (marked New in official list)')

# 3) SBI: own product pages ("Know about SBI Life - X UIN: ...")
for u, d in json.load(open(os.path.join(S, 'web/sbi_products.json'))).items():
    if d['uin']:
        name = 'SBI Life - ' + ' '.join(w.capitalize() for w in d['slug'].replace('sbi-life-', '').split('-'))
        add(d['uin'], name, 'SBI website product page', '', '', u, '', 'Name from page URL; confirm from brochure')

# 4) Bajaj: official "Plans Currently On Sale" table (individual section)
bj = json.load(open(os.path.join(S, 'sites/bajaj-life/text/3e7d857bec.json')))
L = [x.strip() for x in bj['text'].split('\n') if x.strip()]
section = 0; prev = None
for i, l in enumerate(L):
    if l.isdigit() and i + 2 < len(L) and (UIN.match(L[i + 2]) or L[i + 2] == 'NA') and L[i + 1].startswith('Bajaj'):
        n = int(l)
        if n == 1: section += 1
        if section == 1:
            u = L[i + 2] if UIN.match(L[i + 2]) else ''
            add(u, L[i + 1], 'Bajaj website: Plans Currently On Sale', '', '', 'https://www.bajajlifeinsurance.com/on-sale-plans.html', '',
                '' if u else 'UIN shown as NA on the on-sale list', pre='116')

rows.sort(key=lambda r: (r['insurer'], r['product_name']))
for i, r in enumerate(rows, 1): r['row_id'] = i
cols = ['row_id'] + [k for k in rows[0] if k != 'row_id']
with open(os.path.join(R, 'master_list.csv'), 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)
with open(os.path.join(R, 'sources/excluded_out_of_scope.csv'), 'w', newline='') as fh:
    w = csv.writer(fh); w.writerow(['uin', 'name', 'council_category (reason)']); w.writerows(excluded)
c = collections.Counter(r['insurer'] for r in rows)
print('master rows', len(rows), '| excluded (health/accident/micro by Council label)', len(excluded))
print(dict(sorted(c.items())))
print('sources', dict(collections.Counter(r['list_source'] for r in rows)))
print('tags', dict(collections.Counter(r['standard_or_pos_tag'] for r in rows)))
