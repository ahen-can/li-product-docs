"""Build deliverables/02_universal_product_list.xlsx and deliverables/03_light_discovery.xlsx
from the repo's own data files. Usage: python3 -I scripts/build_deliverables.py <repo_dir>"""
import csv, re, sys, os, collections as C
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

R = sys.argv[1]
OUT = os.path.join(R, 'deliverables')
os.makedirs(OUT, exist_ok=True)
HEAD = PatternFill('solid', fgColor='1F3864'); HF = Font(bold=True, color='FFFFFF')
WRAP = Alignment(wrap_text=True, vertical='top')


def rd(p):
    with open(os.path.join(R, p), newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))


def sheet(wb, title, header, rows, widths=None, note=None):
    ws = wb.create_sheet(title)
    r0 = 1
    if note:
        ws.cell(1, 1, note).font = Font(italic=True)
        r0 = 3
    for j, h in enumerate(header, 1):
        c = ws.cell(r0, j, h); c.fill = HEAD; c.font = HF; c.alignment = WRAP
    for i, row in enumerate(rows, r0 + 1):
        for j, v in enumerate(row, 1):
            ws.cell(i, j, v)
    for j in range(1, len(header) + 1):
        ws.column_dimensions[get_column_letter(j)].width = (widths or {}).get(j, 18)
    ws.freeze_panes = ws.cell(r0 + 1, 1)
    ws.auto_filter.ref = f"A{r0}:{get_column_letter(len(header))}{r0 + len(rows)}"
    return ws


def text_sheet(wb, title, lines):
    ws = wb.create_sheet(title, 0)
    ws.column_dimensions['A'].width = 140
    for i, l in enumerate(lines, 1):
        c = ws.cell(i, 1, l); c.alignment = Alignment(wrap_text=True, vertical='top')
        if i == 1: c.font = Font(bold=True, size=14)
        elif l.isupper() or l.endswith(':'): c.font = Font(bold=True)
    return ws


master = rd('master_list.csv')
light = {r['uin']: r for r in rd('results/light_discovery_results.csv')}
pf = {r['uin']: r for r in rd('analysis/product_features_v1.csv')}
council = rd('sources/life-council/council_rows_parsed.csv')
disc = rd('sources/websites/discrepancies.csv')

# ---------------- 02 universal product list ----------------
wb = Workbook(); wb.remove(wb.active)
prod_hdr = ['#', 'Insurer', 'Product name', 'UIN', 'Linked flag (UIN)', 'Council category (verbatim)', 'Source of row',
            'Saral / POS tag', 'IRDAI description line (from brochure)', 'Par flag', 'Market category', 'PD category',
            'Sub-segment', 'Brochure found?', 'Product page', 'Notes']
rows = []
for m in master:
    p = pf.get(m['uin'], {}); l = light.get(m['uin'], {})
    rows.append([int(m['row_id']), m['insurer'], m['product_name'], m['uin'], m['linked_flag_uin'], m['council_category'],
                 m['list_source'], m['standard_or_pos_tag'], p.get('irdai_description_line') or l.get('irdai_description_line', ''),
                 p.get('par_flag', ''), p.get('market_category', ''), p.get('pd_category', ''), p.get('sub_segment_v1', ''),
                 l.get('status', ''), m['website_product_page_url'], m['notes']])
sheet(wb, 'Products', prod_hdr, rows, {1: 5, 2: 18, 3: 45, 4: 13, 6: 22, 7: 26, 9: 50, 15: 45, 16: 40})

# discrepancies
D = []
# A. official lists vs Council
cbyc = C.defaultdict(list)
for c in council:
    if c['lob'].lower().startswith('individual') and c['uin']:
        cbyc[c['uin'][:7]].append(c)
for m in master:
    if not m['list_source'].startswith(('ICICI official', 'Bharti official')):
        continue
    cs = cbyc.get(m['uin'][:7], [])
    if not cs:
        D.append(['A. Official list vs Council', m['insurer'], m['product_name'], '', m['uin'], 'On the official list, not on the Council list (new product)', 'Added to the product list'])
        continue
    c = cs[0]
    if c['uin'] != m['uin']:
        D.append(['A. Official list vs Council', m['insurer'], m['product_name'], c['uin'], m['uin'], f"Version differs: Council {c['uin']}, official list {m['uin']}", 'Official list used'])
    if re.sub(r'\W+', ' ', c['name']).strip().lower() != re.sub(r'\W+', ' ', m['product_name']).strip().lower():
        D.append(['A. Official list vs Council', m['insurer'], m['product_name'], c['uin'], m['uin'], f"Name differs: Council \"{c['name']}\"", 'Official (website) name used'])
# B. document vs list version
for u, l in light.items():
    d = l.get('uin_in_document', '')
    if l['status'] == 'ok' and d and d != u:
        D.append(['B. Document vs list (UIN version)', l['insurer'], l['product_name'], u, d, f'Brochure prints {d}; list has {u}', 'Kept as found; to confirm with insurer site'])
# C. other list flags
for m in master:
    if m['notes']:
        D.append(['C. List flags', m['insurer'], m['product_name'], m['uin'], '', m['notes'], ''])
for u, l in light.items():
    if 'withdrawn' in l.get('notes', '').lower():
        D.append(['C. List flags', l['insurer'], l['product_name'], u, '', l['notes'], 'In for-your-attention/please_check.md'])
# D. website scrape audit trail
for d in disc:
    D.append(['D. Website scrape vs Council (audit trail)', d['insurer'], d['product_name_website'] or d['product_name_council'],
              d['uin_council'], d['uin_website'], d['discrepancy'], 'Not applied: lower confidence (see note at top)'])
sheet(wb, 'Discrepancies', ['Type', 'Insurer', 'Product', 'UIN (Council / list)', 'UIN (official list / website / document)', 'What differs', 'What we did'],
      D, {1: 30, 2: 18, 3: 45, 4: 16, 5: 18, 6: 70, 7: 40},
      note='A-C were checked and applied or flagged. D is the raw website-scrape comparison (3 Nov); the user\'s official ICICI and Bharti lists later showed the Council list is accurate and most D rows are scraper noise (old pages, menu items), so D is kept only as an audit trail.')

# counts per insurer
cnt = C.defaultdict(C.Counter)
for m in master:
    p = pf.get(m['uin'], {}); l = light.get(m['uin'], {})
    cnt[m['insurer']]['Products'] += 1
    cnt[m['insurer']][p.get('market_category') or 'Category not yet known'] += 1
    cnt[m['insurer']]['Brochure ' + (l.get('status') or 'n/a')] += 1
cats = ['Protection', 'Non-Par Savings', 'Par', 'ULIP', 'Annuity', 'Category not yet known']
crow = [[k, v['Products']] + [v[c] for c in cats] + [v['Brochure ok'], v['Brochure manual'], v['Brochure not found']] for k, v in sorted(cnt.items())]
crow.append(['TOTAL'] + [sum(r[i] for r in crow) for i in range(1, len(crow[0]))])
sheet(wb, 'Counts by insurer', ['Insurer', 'Products'] + cats + ['Brochure found', 'Manual (blocked site)', 'Not found'], crow, {1: 24})
ex = rd('sources/excluded_out_of_scope.csv')
sheet(wb, 'Excluded (out of scope)', list(ex[0].keys()), [list(r.values()) for r in ex], {2: 50, 3: 30},
      note='Individual products on the Council list excluded by the Council\'s own label (Health, Accident, Micro). Riders (UIN B/A) and govt/combi (G/Y) are also excluded.')
text_sheet(wb, 'README', [
    'Universal product list: individual life products in force (v3, 4 Nov 2026)',
    f'{len(master)} in-scope individual products from 25 life insurers.',
    'HOW IT WAS BUILT:',
    '1. Backbone: Life Insurance Council in-force products list, Sep-2026 (xls export), individual products only.',
    '2. Replaced by the insurer\'s official list where the client supplied one: ICICI Life (38) and Bharti Life (26). ICICI names follow the website (the "ICICI Pru" to "ICICI Life" renames).',
    '3. Added from the insurer website where the Council list had no individual products: SBI Life (27, product pages) and Bajaj Life (31, "Plans currently on sale").',
    '4. Scope: excludes Health, Accident and Micro (Council label), riders (UIN B/A) and govt/combi (G/Y). Saral and POS products are kept and tagged.',
    '5. Categories are never taken from product names. Market category, PD category and par flag come from the IRDAI description line printed on the brochure (light discovery). Blank = brochure not yet obtained (blocked site).',
    'TABS:',
    'Products: one row per product. Discrepancies: everything that did not match between sources (A official lists vs Council, B document vs list version, C list flags, D website-scrape audit trail). Counts by insurer. Excluded (out of scope).',
    'Source files in the repo: master_list.csv, sources/life-council/, sources/official-lists/, sources/websites/.'])
wb.save(os.path.join(OUT, '02_universal_product_list.xlsx'))
print('02 products', len(rows), 'discrepancies', len(D), C.Counter(d[0] for d in D))

# ---------------- 03 light discovery ----------------
wb = Workbook(); wb.remove(wb.active)
idx = {}
for r in rd('index.csv'):
    if r['doc_type'] in ('brochure', 'policy', 'leaflet') and r['uin'] not in idx:
        idx[r['uin']] = r
LR = []
for m in master:
    l = light.get(m['uin'], {}); p = pf.get(m['uin'], {}); i = idx.get(m['uin'], {})
    LR.append([m['insurer'], m['product_name'], m['uin'], l.get('status', ''), l.get('doc_type', ''), l.get('uin_in_document', ''),
               l.get('irdai_description_line', ''), p.get('par_flag', ''), p.get('market_category', ''), l.get('pages', ''),
               p.get('text_quality', ''), l.get('source_url', ''), l.get('found_on_page_url', ''), i.get('file_path', ''), l.get('notes', '')])
sheet(wb, 'Products', ['Insurer', 'Product', 'UIN', 'Status', 'Document stored', 'UIN printed in document', 'IRDAI description line',
                       'Par flag', 'Market category', 'Pages', 'Text quality', 'Source URL (exact file)', 'Found on page', 'Repo path', 'Notes'],
      LR, {2: 42, 7: 50, 12: 50, 13: 40, 14: 34, 15: 40})
st = C.defaultdict(C.Counter)
for m in master:
    st[m['insurer']][light.get(m['uin'], {}).get('status', 'n/a')] += 1
srows = [[k, sum(v.values()), v['ok'], v['not found'], v['manual'],
          f"{v['ok'] / (v['ok'] + v['not found']):.0%}" if v['ok'] + v['not found'] else 'blocked site'] for k, v in sorted(st.items())]
tot = [sum(r[i] for r in srows) for i in range(1, 5)]
srows.append(['TOTAL'] + tot + [f"{tot[1] / (tot[1] + tot[2]):.1%}"])
sheet(wb, 'Counts by insurer', ['Insurer', 'Products', 'Brochure found', 'Not found', 'Manual (blocked site)', 'Hit rate on readable sites'], srows, {1: 24})
mc = rd('results/manual_checklist.csv')
sheet(wb, 'Manual & not found', list(mc[0].keys()), [list(r.values()) for r in mc], {3: 45, 4: 50, 5: 45})
F = []
for u, l in light.items():
    n = l.get('notes', ''); d = l.get('uin_in_document', '')
    if l['status'] != 'ok':
        continue
    if d and d != u: F.append([l['insurer'], l['product_name'], u, 'UIN version differs', f'document prints {d}'])
    if 'OCR' in n: F.append([l['insurer'], l['product_name'], u, 'Read by OCR', n])
    if 'not verified' in n: F.append([l['insurer'], l['product_name'], u, 'Policy document used (brochure not verified)', n])
    if pf.get(u, {}).get('text_quality', 'ok') != 'ok': F.append([l['insurer'], l['product_name'], u, 'Garbled text', pf[u]['text_quality']])
    if 'withdrawn' in n.lower(): F.append([l['insurer'], l['product_name'], u, 'Possibly withdrawn', n])
sheet(wb, 'Flags', ['Insurer', 'Product', 'UIN', 'Flag', 'Detail'], F, {2: 45, 4: 34, 5: 80})
Q = []
for line in open(os.path.join(R, 'results/site_quirks.md'), encoding='utf-8'):
    mm = re.match(r'- \*\*(.+?)\*\*\s*(.*)', line.strip())
    if mm and not line.startswith('## '):
        Q.append([mm.group(1).rstrip('.'), mm.group(2)])
    if line.startswith('## Scope'):
        break
ws = sheet(wb, 'Site notes', ['Insurer / topic', 'Where documents live and quirks'], Q, {1: 26, 2: 140})
for r in ws.iter_rows(min_row=2):
    for c in r: c.alignment = WRAP
text_sheet(wb, 'README', [
    'Light discovery (brochure pass): what we did and what we found (4 Nov 2026)',
    'GOAL: get the official sales brochure of every in-scope product, read the IRDAI description line printed on it, and use that (not the product name) to set the category. Also a first keyword scan of features, used for feature list v1.',
    'METHOD:',
    '1. Input: the universal product list (633 products, deliverable 02).',
    '2. For each product, the script opened the insurer\'s own product page (or sitemap / documents page) and downloaded the brochure; policy document if no brochure; leaflet only if nothing else.',
    '3. Checks on every file: real PDF (%PDF header, opens in pdfinfo), and the product\'s UIN printed in the text. Scanned files were OCRed.',
    '4. Every file is stored in the GitHub repo with the exact source URL and the page it was found on (index.csv). Only insurer websites were used.',
    '5. Sites that block automated access (ICICI, Kotak, Star Union Dai-ichi, Go Digit) were not contacted; their 106 products are on the manual list.',
    f'RESULT: {tot[1]} of {tot[0]} products have a verified document ({tot[1] / (tot[1] + tot[2]):.1%} of products on readable sites); {tot[2]} not found; {tot[3]} manual (blocked sites).',
    'TABS: Products (one row each, with status, description line, category, source URL). Counts by insurer. Manual & not found (what the user should download and where). Flags (version differences, OCR, garbled text, possibly withdrawn). Site notes (where each insurer keeps documents).',
    'Source files in the repo: results/light_discovery_results.csv, results/light_discovery_summary.md, results/site_quirks.md, index.csv.'])
wb.save(os.path.join(OUT, '03_light_discovery.xlsx'))
print('03 rows', len(LR), 'flags', len(F), 'site notes', len(Q), 'totals', tot)
