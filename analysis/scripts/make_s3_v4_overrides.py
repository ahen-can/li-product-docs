"""Turn S3's v4 QA FAILs (qa/s3_v4/v4_qa_workbook.xlsx, tabs C to F, plus two tab B notes) into
analysis/v4/s3_v4_overrides.csv. Tab A FAILs are peer counts that follow from the cell fixes, so they are not rows here.
UNSURE rows are not applied. Code "blank" clears a cell.
Usage: python3 -I analysis/scripts/make_s3_v4_overrides.py <repo_dir>"""
import csv, os, re, sys
import openpyxl

R = sys.argv[1]
wb = openpyxl.load_workbook(os.path.join(R, 'qa/s3_v4/v4_qa_workbook.xlsx'), read_only=True)
PF = {(r['uin'], r['feature']): r for r in csv.DictReader(open(os.path.join(R, 'analysis/product_features_ulip_v4.csv'), encoding='utf-8'))}
DOCRX = re.compile(r'(rider brochure|rider policy|brochure(?:-\d)?|policy|CIS|sales brochure(?:-\d)?)\s+p\s?(\d+)', re.I)
CODES = {'B', 'O', 'R', 'N', '?', 'Y', '-'}
out = []


def add(uin, feat, code, value, comment, tab):
    m = DOCRX.search(comment or '')
    out.append({'uin': uin, 'feature': feat, 'old_code': PF.get((uin, feat), {}).get('code', ''), 'code': code, 'value': value,
                'doc': m.group(1) if m else 'see quote', 'page': m.group(2) if m else '', 'quote': (comment or '')[:600], 'source': f'S3 v4 QA, tab {tab}'})


def split(correct):
    c = str(correct).strip()
    if c.lower() == 'blank': return 'blank', ''
    m = re.match(r'^([BORNY?-])(?:\s*[;(]\s*(.*?)\)?)?$', c, re.S)
    if m and m.group(1) in CODES: return m.group(1), (m.group(2) or '').strip()
    return None, c


for r in list(wb['C_additions_basis'].iter_rows(values_only=True))[3:]:
    if r[-2] != 'FAIL': continue
    uin, basis = r[3], r[4]
    feat = 'additions_pct_of_premium' if 'premium' in basis else 'additions_pct_of_fund'
    code, rest = split(r[-3])
    old = PF.get((uin, feat), {}).get('value', '')
    old = re.sub(r'^Only for: [^.]*\. ', '', old)
    val = ((rest[0].upper() + rest[1:]) if rest else '') + ((' | ' + old) if old and code != 'blank' else '')
    add(uin, feat, code or 'B', val.strip(' |'), r[-1], 'C')

for r in list(wb['D_funds'].iter_rows(values_only=True))[3:]:
    if r[-2] != 'FAIL': continue
    uin, feat = r[3], r[4]
    code, rest = split(r[-3])
    if feat == 'index_fund_offered':
        add(uin, feat, code, (r[-1] or '')[:200], r[-1], 'D')
    elif str(r[-3]).startswith('none'):
        add(uin, feat, '?', str(r[-3]), r[-1], 'D')
    else:
        add(uin, feat, 'v', str(r[-3]), r[-1], 'D')

for r in list(wb['E_rules_and_scans'].iter_rows(values_only=True))[3:]:
    if r[-2] != 'FAIL': continue
    code, rest = split(r[-3])
    add(r[3], r[4], code, rest, r[-1], 'E')

for r in list(wb['F_peer_patterns'].iter_rows(values_only=True))[3:]:
    if r[-2] != 'FAIL': continue
    code, rest = split(r[-3])
    add(r[4], r[5], code, rest, r[-1], 'F')

# Tab B notes (PASS rows with a correction in the comment)
add('101L133V03', 'critical_illness_inbuilt_or_option', 'R', 'via rider 101A037V01 (Protect Plus Rider - Linked): cancer cover only', 'S3 tab B note: Click 2 Wealth\'s only CI rider is cancer cover.', 'B')
add('110L172V03', 'disability_benefit', 'R', 'via the accidental death and disability rider named in the policy (p3)', 'S3 tab B note: Tata Smart Sampoorna Raksha Pro names the ADD rider (policy p3).', 'B')

p = os.path.join(R, 'analysis/v4/s3_v4_overrides.csv')
with open(p, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
print(len(out), 'overrides ->', p)
