"""Build qa/s3/s3_qa_workbook.xlsx: random samples (fixed seed) from the project's outputs for S3 to check
against the source documents. Usage: python3 -I qa/s3/build_s3_workbook.py <repo>"""
import csv, json, glob, os, sys, random, re
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
R = sys.argv[1]; rnd = random.Random(20261104)
HEAD = PatternFill('solid', fgColor='1F3864'); HF = Font(bold=True, color='FFFFFF'); Y = PatternFill('solid', fgColor='FFF2CC'); WR = Alignment(wrap_text=True, vertical='top')
wb = Workbook(); wb.remove(wb.active)
def sheet(name, header, rows, widths, note):
    ws = wb.create_sheet(name)
    ws.cell(1, 1, note).alignment = WR; ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(header) + 2); ws.row_dimensions[1].height = 60
    for j, h in enumerate(header + ['PASS / FAIL / UNSURE', 'Comment (what you saw, page)'], 1):
        c = ws.cell(3, j, h); c.fill = HEAD; c.font = HF; c.alignment = WR
    for i, row in enumerate(rows, 4):
        for j, v in enumerate(row, 1):
            ws.cell(i, j, re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', v) if isinstance(v, str) else v).alignment = WR
        ws.cell(i, len(header) + 1).fill = Y; ws.cell(i, len(header) + 2).fill = Y
    for j, w in enumerate(widths + [14, 40], 1): ws.column_dimensions[get_column_letter(j)].width = w
    ws.freeze_panes = 'A4'
    return len(rows)
def flat(v):
    if v is None: return ''
    if isinstance(v, (dict, list)): return json.dumps(v, ensure_ascii=False)[:500]
    return str(v)
def docpath(u, doc_label):
    p = sorted(glob.glob(os.path.join(R, 'docs', '*', u, '*.pdf')))
    return '; '.join(os.path.relpath(x, R) for x in p)
counts = {}
# A. Deep discovery fields (S2): 15 products x 6 fields
deep = {os.path.basename(f)[:-5]: json.load(open(f, encoding='utf-8')) for f in glob.glob(os.path.join(R, 'features/ulip/*.json'))}
FIELDS = ['charges.premium_allocation_charge', 'charges.policy_administration_charge', 'charges.fund_management_charge', 'eligibility.entry_age_max',
          'eligibility.premium_min_annual', 'benefits.loyalty_additions', 'benefits.return_of_mortality_charges', 'flexibility.partial_withdrawals', 'surrender_revival.lock_in_years']
rows = []
for u in sorted(rnd.sample(sorted(deep), 15)):
    d = deep[u]
    for f in rnd.sample(FIELDS, 6):
        g, k = f.split('.'); o = d.get(g, {}).get(k, {}) or {}
        rows.append([u, d['product']['product_name']['value'], f, o.get('status'), flat(o.get('value')), o.get('doc'), o.get('page'), flat(o.get('quote'))[:300], docpath(u, o.get('doc'))])
counts['A'] = sheet('A_deep_fields', ['UIN', 'Product', 'Field', 'Status given', 'Value given', 'Document (site label)', 'Page', 'Quote given', 'PDF in repo'], rows,
      [12, 30, 26, 14, 50, 18, 6, 50, 40],
      'A. Deep discovery (S2). Open the PDF at the page. PASS = the value and the status (built-in / optional / rider / not offered / not stated) are right. If the status is "not stated", search the document; FAIL if the feature is in fact there.')
# B. New-feature verdicts (S1): all rejections + 30 random acceptances
V = list(csv.DictReader(open(os.path.join(R, 'analysis/v3/new_feature_verdicts.csv'), encoding='utf-8')))
rej = [v for v in V if v['verdict'] == 'N']; acc = rnd.sample([v for v in V if v['verdict'] == 'Y'], 30)
rows = [[v['uin'], deep.get(v['uin'], {}).get('product', {}).get('product_name', {}).get('value', ''), v['group'], v['verdict'], v['reason'], v['doc'], v['page'], v['snippet'][:400], docpath(v['uin'], '')] for v in rej + acc]
counts['B'] = sheet('B_new_feature_calls', ['UIN', 'Product', 'Feature group', 'S1 verdict', 'S1 reason', 'Doc', 'Page', 'Snippet', 'PDF in repo'], rows,
      [12, 30, 26, 8, 40, 8, 6, 60, 40],
      'B. New-feature calls (S1). Feature definitions are in analysis/feature_list_ulip_v2.xlsx, tab Features. PASS = you agree with the verdict (Y = the product has the feature; N = it does not, for the reason given).')
# C. Calculator inputs (S1): 6 products x key params
rows = []
for f in sorted(glob.glob(os.path.join(R, 'calc/params/ulip/*.json'))):
    p = json.load(open(f)); u = p['uin']
    for name, val in [('Allocation charge by year (%)', p['allocation_charge_pct']), ('Admin charge', p['admin']), ('FMC equity fund (%)', p['fmc_pct']),
                      ('Mortality per 1000, age 30 / 40 / 49', [p['mortality_per_1000'].get(str(a)) for a in (30, 40, 49)]), ('Additions and refunds', [a['name'] for a in p.get('additions', [])])]:
        rows.append([u, p['product'], p['variant_used'], name, flat(val), p['sources'] if name != 'Mortality per 1000, age 30 / 40 / 49' else p['mortality_source'], docpath(u, '')])
counts['C'] = sheet('C_calculator_inputs', ['UIN', 'Product', 'Variant', 'Input', 'Value used', 'Source given', 'PDF in repo'], rows, [12, 30, 40, 28, 50, 50, 40],
      'C. ULIP calculator inputs (calc/params/ulip). PASS = the value matches the policy document for the variant stated. These products already match insurer illustrations within 0.3%, so a FAIL here is important.')
# D. Bharti portfolio NBP (S1) vs KPI PDF
PP = [('Guaranteed Wealth Pro', 113.23), ('Wealth Pro', 81.55), ('Growth Shield Plus', 79.58), ('Dream Shield Plus', 50.91), ('Insta Gain Plan', 50.82), ('Guaranteed Bachat Plan', 46.56), ('Unnati', 43.85), ('Swabhimaan Retirement Plan', 38.21)]
rows = [[n, 'FY26', v, 'sources/bharti-kpi/product_performance_FY24_to_H2FY27.pdf, "Product Performance FY26" table, column C', 'deliverables/01, tab Bharti portfolio'] for n, v in PP]
counts['D'] = sheet('D_Bharti_NBP', ['Product', 'Period', 'NBP used (Rs cr)', 'Source', 'Where used'], rows, [30, 8, 14, 60, 30],
      'D. Bharti product NBP. PASS = the number matches the PDF. Also note in a comment if the products in the tab are mapped to the right category.')
# E. Universal list discrepancies (S1): 12 random rows of types A-C
import openpyxl
dws = openpyxl.load_workbook(os.path.join(R, 'deliverables/02_universal_product_list.xlsx'), read_only=True)['Discrepancies']
dr = [r for r in dws.iter_rows(min_row=4, values_only=True) if r[0] and r[0][0] in 'ABC']
rows = [list(r[:7]) for r in rnd.sample(dr, 12)]
counts['E'] = sheet('E_list_discrepancies', ['Type', 'Insurer', 'Product', 'UIN (Council)', 'UIN (other)', 'What differs', 'What we did'], rows, [28, 16, 40, 14, 16, 50, 30],
      'E. Universal product list, Discrepancies tab. PASS = the difference is real (check the insurer website or the PDF in docs/) and what we did is sensible.')
# F. v1 corrections (S1): 15 random
cws = openpyxl.load_workbook(os.path.join(R, 'analysis/feature_list_ulip_v2.xlsx'), read_only=True)['v1 corrections']
cr = [r for r in cws.iter_rows(min_row=4, values_only=True) if r[0]]
rows = [list(r[:7]) for r in rnd.sample(cr, 15)]
counts['F'] = sheet('F_v1_vs_deep', ['Insurer', 'Product', 'UIN', 'Feature', 'Difference', 'v1 brochure evidence', 'Deep quote'], rows, [16, 30, 12, 26, 30, 50, 50],
      'F. Where the v1 brochure scan and the deep data disagree. PASS = the deep data is right. FAIL = v1 was right after all.')
# Summary
ws = wb.create_sheet('Summary', 0)
ws.column_dimensions['A'].width = 34; ws.column_dimensions['B'].width = 10
ws.cell(1, 1, 'S3 QA workbook: summary').font = Font(bold=True, size=14)
for j, h in enumerate(['Tab', 'Rows', 'PASS', 'FAIL', 'UNSURE', 'Pass rate'], 1):
    c = ws.cell(3, j, h); c.fill = HEAD; c.font = HF
tabs = ['A_deep_fields', 'B_new_feature_calls', 'C_calculator_inputs', 'D_Bharti_NBP', 'E_list_discrepancies', 'F_v1_vs_deep']
for i, (t, k) in enumerate(zip(tabs, 'ABCDEF'), 4):
    n = counts[k]; col = {'A': 'J', 'B': 'J', 'C': 'H', 'D': 'F', 'E': 'H', 'F': 'H'}[k]
    ws.cell(i, 1, t); ws.cell(i, 2, n)
    rng = f"'{t}'!{col}4:{col}{n + 3}"
    ws.cell(i, 3, f'=COUNTIF({rng},"PASS")'); ws.cell(i, 4, f'=COUNTIF({rng},"FAIL")'); ws.cell(i, 5, f'=COUNTIF({rng},"UNSURE")')
    ws.cell(i, 6, f'=IF(C{i}+D{i}=0,"",C{i}/(C{i}+D{i}))').number_format = '0%'
wb.save(os.path.join(R, 'qa/s3/s3_qa_workbook.xlsx'))
print(counts)
