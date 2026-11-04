"""Build taxonomy sub-segments + feature_list_v1.xlsx from product_features_v1.csv.
Sub-segments use ONLY the description line and brochure feature evidence (f_* flags), never product names
(exception: the 'Saral' / 'POS' tag, which is the official standard-product name already carried as a tag).
Usage: python3 -I build_feature_list_v1.py <main_dir>"""
import csv, json, os, sys, re, statistics, collections
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter as CL

M = sys.argv[1]; A = os.path.join(M, 'analysis')
P = list(csv.DictReader(open(os.path.join(A, 'product_features_v1.csv'))))
E = list(csv.DictReader(open(os.path.join(A, 'feature_evidence_v1.csv'))))
CAT = json.load(open(os.path.join(A, 'feature_catalogue_v1.json')))
LOG = list(csv.DictReader(open(os.path.join(A, 'brochures_used_log.csv'))))
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE
def clean(d):
    for k, v in d.items():
        if isinstance(v, str): d[k] = ILLEGAL_CHARACTERS_RE.sub('', v)
for d in P + E + LOG: clean(d)
ev = {(e['uin'], e['feature']): e for e in E}
Y = lambda r, k: r.get('f_' + k) == 'Y'

# manual fix: Bajaj Guaranteed Pension Goal II has no description line in the downloaded document and no Council label
for r in P:
    if r['uin'] == '116N187V11' and not r['market_category']:
        r['market_category'], r['pd_category'], r['sub_basis'] = 'Annuity', 'Pension & Annuity', 'Bajaj on-sale page lists it under pension/annuity; description line missing in downloaded file - VERIFY'

def subseg(r):
    mc = r['market_category']; d = r['irdai_description_line'].lower(); tag = r['standard_or_pos_tag']
    if mc == 'Protection':
        if 'Saral' in tag: return 'Saral Jeevan Bima (standard term)'
        if re.search(r'loan|credit', d) or (Y(r, 'decreasing_cover') and not Y(r, 'whole_life_cover')): return 'Credit / loan / decreasing cover'
        if 'savings' in d and 'pure risk' in d: return 'Term with savings element (ROP-type)'
        if Y(r, 'return_of_premium'): return 'Term with ROP option'
        if Y(r, 'whole_life_cover'): return 'Pure term with whole-life option'
        return 'Pure term'
    if mc == 'Non-Par Savings':
        if 'Saral' in tag or 'POS' in tag: return 'Standard / POS savings'
        if Y(r, 'whole_life_income') and Y(r, 'guaranteed_income'): return 'Whole-life guaranteed income'
        if Y(r, 'guaranteed_income') and Y(r, 'lump_sum_maturity'): return 'Guaranteed income + lump-sum (multi-option)'
        if Y(r, 'guaranteed_income'): return 'Guaranteed income'
        return 'Guaranteed maturity (endowment)'
    if mc == 'Par':
        if r['pd_category'] == 'Pension & Annuity': return 'Par pension'
        if Y(r, 'survival_benefit_money_back'): return 'Par money-back'
        if Y(r, 'whole_life_income'): return 'Par whole life'
        if Y(r, 'cash_bonus') or Y(r, 'guaranteed_income'): return 'Par income'
        return 'Par endowment'
    if mc == 'ULIP':
        if r['pd_category'] == 'Pension & Annuity': return 'ULIP pension'
        if Y(r, 'return_of_mortality_charges'): return 'ULIP with return of mortality (TULIP-type)'
        if Y(r, 'child_payor_benefit'): return 'ULIP with payor / child benefit'
        return 'ULIP wealth'
    if mc == 'Annuity':
        if 'Saral' in tag: return 'Saral Pension (standard immediate annuity)'
        if 'immediate' in d and 'deferred' not in d: return 'Immediate annuity'
        if 'deferred' in d or Y(r, 'deferred_annuity'): return 'Deferred annuity / pension'
        return 'Annuity / pension (other)'
    return mc or 'unclassified'

for r in P: r['sub_segment_v1'] = subseg(r)

CATS = ['Protection', 'Non-Par Savings', 'Par', 'ULIP', 'Annuity']
NUM = [('entry_age_min', 'Min entry age (yrs)'), ('entry_age_max', 'Max entry age (yrs)'), ('maturity_age_max', 'Max maturity age (yrs)'),
       ('policy_term_min', 'Min policy term (yrs)'), ('policy_term_max', 'Max policy term (yrs)'), ('min_premium', 'Min premium (Rs)'),
       ('min_sum_assured', 'Min sum assured (Rs)'), ('ulip_fmc_min_pct', 'Lowest FMC % (ULIP)'), ('ulip_fmc_max_pct', 'Highest FMC % (ULIP)'),
       ('ulip_fund_count_sfin', 'No. of funds (SFIN codes listed)'), ('annuity_option_labels_found', 'Annuity option labels found')]

hf = Font(bold=True, color='FFFFFF'); hfill = PatternFill('solid', fgColor='1F3864'); bfill = PatternFill('solid', fgColor='FFF2CC')
gfill = PatternFill('solid', fgColor='E2EFDA'); rfill = PatternFill('solid', fgColor='FCE4D6')
def head(ws, row, vals, widths=None):
    for i, v in enumerate(vals, 1):
        c = ws.cell(row, i, v); c.font = hf; c.fill = hfill; c.alignment = Alignment(wrap_text=True, vertical='center')
    if widths:
        for i, w in enumerate(widths, 1): ws.column_dimensions[CL(i)].width = w

def bands(vals, key):
    if not vals: return ''
    if 'age' in key or 'term' in key:
        edges = [0, 1, 18, 30, 45, 60, 70, 80, 85, 99, 101]
    elif 'fmc' in key:
        edges = [0, 0.5, 1.0, 1.25, 1.35, 1.36]
    else:
        edges = [0, 10000, 25000, 50000, 100000, 500000, 2500000, 10**12]
    c = collections.Counter()
    for v in vals:
        for a, b in zip(edges, edges[1:]):
            if a <= v < b: c[f'{a:g}-<{b:g}'] += 1; break
    return '; '.join(f'{k}: {n}' for k, n in c.items())

wb = Workbook(); ws = wb.active; ws.title = 'README'
notes = [
 'Feature list v1 - built from 516 insurer brochures / policy documents (light-discovery pass, 4 Nov 2026)',
 'Coverage: 21 insurers. NOT covered yet: ICICI, Kotak, Star Union Dai-ichi, Go Digit (sites block automation; manual), 11 products with no document found.',
 'Category = IRDAI description line printed on the brochure (+ UIN linked flag); 5 products use the Council category label as fallback (marked). No category from product names.',
 'Sub-segment = rules on the description line + brochure feature evidence (see Taxonomy tab). Ambiguous products default to the generic sub-segment of their category.',
 "Feature flag 'Y' = the brochure DESCRIBES the feature (keyword + context match, legal boilerplate excluded). It may be inbuilt, optional, or via rider - v2 (deep pass) will split these.",
 'Every Y has an evidence snippet + page in the Evidence tab - use it to verify. Precision was spot-checked on samples per feature; some noise remains (see Method & limits).',
 'Numeric fields are filled only when a label and its number sit together in the text (e.g. "Maximum age at entry 65 years"). Grid tables are left blank on purpose; coverage n/N is shown.',
 'Counts: n = products in the category whose brochure describes the feature; N = products in the category. Bharti columns show whether any Bharti product in the category has it.',
]
for i, n in enumerate(notes, 1): ws.cell(i, 1, n)
ws.column_dimensions['A'].width = 160

# Taxonomy / coverage tab: insurer x sub-segment
t = wb.create_sheet('Coverage by sub-segment')
segs = sorted({(r['market_category'], r['sub_segment_v1']) for r in P if r['market_category'] in CATS})
insurers = sorted({r['insurer'] for r in P})
head(t, 1, ['Category', 'Sub-segment', 'Products (all)', 'Insurers offering'] + insurers, [16, 42, 10, 10] + [11] * len(insurers))
t.row_dimensions[1].height = 60
for i, (mc, sg) in enumerate(segs, 2):
    rows = [r for r in P if r['market_category'] == mc and r['sub_segment_v1'] == sg]
    c = collections.Counter(r['insurer'] for r in rows)
    vals = [mc, sg, len(rows), len(c)] + [c.get(ins, 0) or '' for ins in insurers]
    for j, v in enumerate(vals, 1):
        cell = t.cell(i, j, v)
        if insurers[j - 5:j - 4] == ['Bharti Life'] if j > 4 else False:
            cell.fill = bfill if v else rfill
t.freeze_panes = 'E2'

# per-category feature tabs
for mc in CATS:
    rows = [r for r in P if r['market_category'] == mc]; N = len(rows)
    br = [r for r in rows if r['insurer'] == 'Bharti Life']
    ws = wb.create_sheet(mc[:31])
    ws.cell(1, 1, f'{mc}: {N} products from {len({r["insurer"] for r in rows})} insurers; Bharti has {len(br)} product(s) in this category').font = Font(bold=True, size=12)
    head(ws, 3, ['Group', 'Feature', 'Definition (v1 rule)', 'n with feature', 'N', '% of products', 'Insurers with it', 'Bharti has it?',
                 'Bharti products with it', 'Example products (non-Bharti)'], [12, 30, 44, 9, 6, 9, 9, 10, 40, 60])
    rr = 4
    for f in CAT:
        if not (f['applies_to'] == 'ALL' or mc in f['applies_to'].split(',')): continue
        k = f['feature']; have = [r for r in rows if Y(r, k)]
        bh = [r for r in br if Y(r, k)]
        ex = [f"{r['insurer']} - {r['product_name']}" for r in have if r['insurer'] != 'Bharti Life'][:4]
        grp = 'Premium' if k.startswith(('ppt_', 'pay_', 'monthly')) else ('ULIP' if mc == 'ULIP' and f['applies_to'] != 'ALL' else ('Annuity' if mc == 'Annuity' and f['applies_to'] != 'ALL' else ('Common' if f['applies_to'] == 'ALL' else 'Benefit design')))
        vals = [grp, k, f['definition'], len(have), N, round(len(have) / N, 3) if N else '', len({r['insurer'] for r in have}),
                ('Y' if bh else 'N') if br else 'no Bharti product', '; '.join(r['product_name'] for r in bh)[:250], '; '.join(ex)]
        for j, v in enumerate(vals, 1):
            c = ws.cell(rr, j, v)
            if j == 6 and v != '': c.number_format = '0%'
            if j == 8: c.fill = gfill if v == 'Y' else (rfill if v == 'N' else PatternFill())
        rr += 1
    rr += 1
    ws.cell(rr, 1, 'Numeric fields (only label-adjacent values; grid tables blank)').font = Font(bold=True); rr += 1
    head(ws, rr, ['Group', 'Field', 'Bands (value: count)', 'n with value', 'N', 'Min', 'Median', 'Max', 'Bharti values', '']); rr += 1
    for key, label in NUM:
        vals = [float(r[key]) for r in rows if r.get(key) not in (None, '')]
        if not vals: continue
        bv = '; '.join(f"{r['product_name'][:30]}: {r[key]}" for r in br if r.get(key))
        for j, v in enumerate(['Eligibility' if 'age' in key or 'term' in key else ('Charges' if 'fmc' in key else 'Other'), label, bands(vals, key),
                               len(vals), N, min(vals), round(statistics.median(vals), 2), max(vals), bv], 1):
            ws.cell(rr, j, v)
        rr += 1
    ws.freeze_panes = 'C4'

# product x feature matrix
pm = wb.create_sheet('Products x features')
fkeys = [f['feature'] for f in CAT]
cols = ['insurer', 'product_name', 'uin', 'market_category', 'sub_segment_v1', 'pd_category', 'par_flag', 'irdai_description_line', 'sub_basis',
        'standard_or_pos_tag', 'doc_type'] + [k for k, _ in NUM] + ['f_' + k for k in fkeys]
head(pm, 1, cols, [18, 40, 12, 14, 30, 14, 8, 50, 16, 10, 8] + [9] * (len(cols) - 11))
for i, r in enumerate(sorted(P, key=lambda r: (r['market_category'], r['insurer'], r['product_name'])), 2):
    for j, c in enumerate(cols, 1):
        pm.cell(i, j, r.get(c, ''))
        if r['insurer'] == 'Bharti Life' and j <= 2: pm.cell(i, j).fill = bfill
pm.freeze_panes = 'C2'; pm.auto_filter.ref = pm.dimensions

ev_ws = wb.create_sheet('Evidence')
head(ev_ws, 1, ['insurer', 'uin', 'feature', 'page', 'evidence (brochure text)'], [18, 12, 30, 6, 160])
for i, e in enumerate(E, 2):
    for j, c in enumerate(['insurer', 'uin', 'feature', 'page', 'evidence'], 1): ev_ws.cell(i, j, e[c])
ev_ws.auto_filter.ref = ev_ws.dimensions

lg = wb.create_sheet('Brochures used (v1)')
lc = list(LOG[0].keys()); head(lg, 1, lc, [6, 11, 12, 18, 40, 9, 70, 20, 50])
for i, r in enumerate(LOG, 2):
    for j, c in enumerate(lc, 1): lg.cell(i, j, r[c])

ml = wb.create_sheet('Method & limits')
lim = ['Known limits of v1 (to fix in v2 / deep pass):',
       '- Y means "described in the brochure"; it does not yet distinguish inbuilt vs optional vs rider (e.g. critical illness, waiver of premium, accidental death are often riders).',
       '- Common words can still over-match in places (e.g. "policy loan" is mentioned in many surrender sections; "monthly" mode vs monthly income). Use the Evidence tab.',
       '- Numeric eligibility: only ~25-30% of products have label-adjacent values; the rest are in grid tables that need reading in the deep pass.',
       '- ULIP fund counts are only filled where SFIN codes are printed; FMC ranges come from percentages near "fund management charge".',
       '- Sub-segment rules are first-cut; a product with several options (e.g. income or lump sum) is put in a multi-option bucket.',
       '- 4 insurers (ICICI, Kotak, SUD, Go Digit) and 11 other products are not in v1.',
       'Files: analysis/product_features_v1.csv, feature_evidence_v1.csv, feature_catalogue_v1.json, brochures_used_log.csv, taxonomy.md; scripts in analysis/scripts/.']
for i, n in enumerate(lim, 1): ml.cell(i, 1, n)
ml.column_dimensions['A'].width = 160
wb.save(os.path.join(A, 'feature_list_v1.xlsx'))

with open(os.path.join(A, 'product_features_v1.csv'), 'w', newline='') as fh:
    cc = list(P[0].keys())
    w = csv.DictWriter(fh, fieldnames=cc); w.writeheader(); w.writerows(P)
c = collections.Counter((r['market_category'], r['sub_segment_v1']) for r in P)
for k, v in sorted(c.items()): print(f'{k[0]:16} {k[1]:46} {v}')
print('Bharti:', collections.Counter((r['market_category'], r['sub_segment_v1']) for r in P if r['insurer'] == 'Bharti Life'))
