"""Turn S3's v3 QA FAILs (qa/s3_v3/v3_qa_workbook.xlsx, tab B) into analysis/v3/s3_overrides.csv.
build_ulip_features.py applies that file after it builds the cells. UNSURE rows are not applied:
they wait for a coding rule (analysis/v3/coding_rules.md).
Usage: python3 -I analysis/scripts/make_s3_overrides.py <repo_dir>"""
import csv, os, re, sys
import openpyxl

R = sys.argv[1]
wb = openpyxl.load_workbook(os.path.join(R, 'qa/s3_v3/v3_qa_workbook.xlsx'), read_only=True)
CODES = {'B', 'O', 'R', 'N', '?', 'Y', '-'}
DOCRX = re.compile(r'(rider brochure|rider policy|brochure|policy|CIS)\s+p\s?(\d+)', re.I)
out = []
for r in list(wb['B_Bharti_cells'].iter_rows(values_only=True))[3:]:
    if not r[0] or r[9] != 'FAIL':
        continue
    uin = re.search(r'\((\w+)\)', r[0]).group(1)
    correct = str(r[8]).strip()
    comment = str(r[10] or '').strip()
    m = DOCRX.search(comment)
    code, value = (correct, '') if correct in CODES else ('', correct)
    out.append({'uin': uin, 'feature': r[1], 'old_code': r[3] or '', 'code': code, 'value': value,
                'doc': m.group(1) if m else 'see comment', 'page': m.group(2) if m else '',
                'quote': comment, 'source': 'S3 v3 QA, 5 Nov 2026'})
p = os.path.join(R, 'analysis/v3/s3_overrides.csv')
with open(p, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
print(len(out), 'overrides ->', p)
