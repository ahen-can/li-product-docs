"""Build qa/s3_v3/v3_qa_workbook.xlsx: every feature-list v3 cell for Bharti's 7 ULIPs, plus the Bharti summary
claim for each feature, for S3 to check against the documents. Usage: python3 -I qa/s3_v3/build_v3_qa_workbook.py <repo>"""
import sys, os, csv, re, glob
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter
R = sys.argv[1]
src = openpyxl.load_workbook(os.path.join(R, 'analysis/feature_list_ulip_v3.xlsx'), read_only=True)
mx = list(src['Matrix'].iter_rows(values_only=True)); hdr = mx[0]
bi = [i for i, h in enumerate(hdr) if h and str(h).startswith('Bharti')]
names = {i: str(hdr[i]).split(' | ')[1].replace('Bharti AXA Life ', '') + ' (' + str(hdr[i]).split(' | ')[2] + ')' for i in bi}
feat = {r[1]: r for r in src['Features'].iter_rows(min_row=2, values_only=True) if r[1]}
ev = {}
for r in csv.DictReader(open(os.path.join(R, 'analysis/product_features_ulip_v3.csv'), encoding='utf-8')):
    if r['uin'].startswith('130'): ev[(r['feature'], r['uin'])] = r
HEAD = PatternFill('solid', fgColor='1F3864'); HF = Font(bold=True, color='FFFFFF'); Y = PatternFill('solid', fgColor='FFF2CC'); WR = Alignment(wrap_text=True, vertical='top')
wb = Workbook(); wb.remove(wb.active)
def sheet(name, note, header, rows, widths):
    ws = wb.create_sheet(name); ws.cell(1, 1, note).alignment = WR
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=len(header) + 3); ws.row_dimensions[1].height = 75
    for j, h in enumerate(header + ['Correct value / status', 'PASS / FAIL / UNSURE', 'Comment (document, page, quote)'], 1):
        c = ws.cell(3, j, h); c.fill = HEAD; c.font = HF; c.alignment = WR
    for i, row in enumerate(rows, 4):
        for j, v in enumerate(row, 1): ws.cell(i, j, re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', str(v)) if v is not None else '').alignment = WR
        for k in range(3): ws.cell(i, len(header) + 1 + k).fill = Y
    for j, w in enumerate(widths + [30, 14, 50], 1): ws.column_dimensions[get_column_letter(j)].width = w
    ws.freeze_panes = 'C4'
    return len(rows)
# A: one row per feature, Bharti summary claim
A = []
for r in mx[1:]:
    f, g = r[0], r[1]
    if not f: continue
    fr = feat.get(f, ())
    codes = '; '.join(f"{names[i]}: {r[i] if r[i] not in (None, '') else 'blank'}" for i in bi)
    A.append([g, f, fr[2] if len(fr) > 2 else '', fr[5] if len(fr) > 5 else '', fr[11] if len(fr) > 11 else '', codes])
nA = sheet('A_Bharti_claims', 'A. For each feature row in feature list v3, is the "Bharti" claim right across all 7 Bharti ULIPs? Read the definition, then check each product\'s policy bond and brochure (docs/bharti-life/<UIN>/). Codes: B built-in, O optional, R rider, N not offered, ? not stated, Y mentioned in brochure (v1 keyword), - not found, blank = not found in the documents, a value = the value shown. Watch for: features delivered through a rider; "not stated" read as "lacks"; counts that should be 6 of 7, not 7; channel-specific terms (online, staff, women); v1 keyword rows that only show a mention.',
          ['Group', 'Feature id', 'Definition', 'All 84: has it', 'Bharti claim in v3', 'Code per Bharti product'], A, [16, 28, 40, 12, 40, 70])
# B: one row per Bharti product x status-type feature cell
B = []
for r in mx[1:]:
    f, g = r[0], r[1]
    if not f: continue
    for i in bi:
        u = str(hdr[i]).split(' | ')[2]
        e = ev.get((f, u), {})
        B.append([names[i], f, g, r[i] if r[i] not in (None, '') else 'blank', (e.get('value') or '')[:200], e.get('doc', ''), e.get('page', ''), (e.get('quote') or '')[:300]])
nB = sheet('B_Bharti_cells', 'B. Every v3 cell for the 7 Bharti ULIPs, with the evidence we hold. Check the code against the document. Blank or "?" cells are the most likely errors: search the document before agreeing that the feature is absent.',
          ['Product', 'Feature id', 'Group', 'Code in v3', 'Value', 'Document', 'Page', 'Quote'], B, [30, 28, 16, 10, 40, 16, 6, 60])
# C: riders
C = [['Bharti AXA Life Linked Complete Shield Rider', '130A012V02', 'Wealth Pro, Growth Shield Plus, Dream Shield Plus, Grow Wealth (and others: check)', 'Does it include waiver of premium? Critical illness? Accidental death or disability? Which options?'],
     ['Bharti AXA Life Cover Plus Linked Term Rider', '130A034V01', 'Wealth Pro (check others)', 'What does it cover?']]
nC = sheet('C_Bharti_riders', 'C. Riders. Download each rider\'s brochure and policy document from bhartiaxa.com (rider pages or the products\' download sections) into manual-uploads/bharti-life/ with sources.csv rows, as for ICICI. Record what each rider covers, so the rider-delivered features in A and B can be coded correctly. Add any other rider a Bharti ULIP names.',
          ['Rider', 'UIN', 'Attached to', 'Questions'], C, [40, 14, 40, 50])
ws = wb.create_sheet('Summary', 0); ws.column_dimensions['A'].width = 30
ws.cell(1, 1, 'Feature list v3 QA, Bharti first').font = Font(bold=True, size=14)
for j, h in enumerate(['Tab', 'Rows', 'PASS', 'FAIL', 'UNSURE'], 1):
    c = ws.cell(3, j, h); c.fill = HEAD; c.font = HF
for k, (t, n, col) in enumerate([('A_Bharti_claims', nA, 'H'), ('B_Bharti_cells', nB, 'J'), ('C_Bharti_riders', nC, 'F')], 4):
    ws.cell(k, 1, t); ws.cell(k, 2, n)
    for j, v in zip((3, 4, 5), ('PASS', 'FAIL', 'UNSURE')): ws.cell(k, j, f'=COUNTIF(\'{t}\'!{col}4:{col}{n + 3},"{v}")')
wb.save(os.path.join(R, 'qa/s3_v3/v3_qa_workbook.xlsx')); print(nA, nB, nC)
