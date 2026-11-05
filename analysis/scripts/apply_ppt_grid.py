"""S2's re-read of the PT/PPT grids for the 77 peer ULIPs (results/ppt_grid.csv) -> analysis/v5/ppt_grid_overrides.csv.
Y -> B, N -> N, ? -> ? (three cases wait for the user's overlap rule). Bharti's 7 were checked by S3 and are not in the file.
Usage: python3 -I analysis/scripts/apply_ppt_grid.py <repo_dir>"""
import csv, os, sys
R = sys.argv[1]
PF = {(r['uin'], r['feature']): r for r in csv.DictReader(open(os.path.join(R, 'analysis/product_features_ulip_v5.csv'), encoding='utf-8'))}
out = []
for g in csv.DictReader(open(os.path.join(R, 'results/ppt_grid.csv'), encoding='utf-8')):
    for col, feat in (('single_pay', 'ppt_single_pay'), ('limited_pay', 'ppt_limited_pay'), ('regular_pay', 'ppt_regular_pay')):
        v = g[col].strip()
        code = {'Y': 'B', 'N': 'N', '?': '?'}.get(v[:1], '?')
        detail = v[2:].strip(' ,') if len(v) > 1 else ''
        val = '; '.join(x for x in (detail, g['variants'], g['note'] if code == '?' else '') if x)
        out.append({'uin': g['uin'], 'feature': feat, 'old_code': PF.get((g['uin'], feat), {}).get('code', ''), 'code': code, 'value': val,
                    'doc': g['doc'], 'page': g['page'], 'quote': g['quote'], 'source': 'S2 pay-term grid re-read, 5 Nov 2026'})
p = os.path.join(R, 'analysis/v5/ppt_grid_overrides.csv')
with open(p, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
ch = [o for o in out if o['old_code'] != o['code']]
print(len(out), 'cells,', len(ch), 'changed;', sum(o['code'] == '?' for o in out), 'unclear')
