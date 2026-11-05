"""Builds results/ppt_grid.csv from scripts/s2_tools/ppt_rows.py (S2's re-read of the PT/PPT grids, briefs/ppt_grid_rescan_brief.md).
Each quote is checked on its cited PDF page (layout or raw text, spacing and ligatures normalised). Prints changes against v5."""
import csv, re, subprocess, sys, os, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ppt_rows import ROWS
def norm(s):
    s = s.replace('ﬁ', 'fi').replace('ﬂ', 'fl').replace('’', "'").replace('–', '-').replace('—', '-')
    return re.sub(r'\s+', ' ', s).strip().lower()
lab = {r['file_path']: r['website_label'] for r in csv.DictReader(open('index.csv'))}
v5 = collections.defaultdict(dict)
for r in csv.DictReader(open('analysis/product_features_ulip_v5.csv')):
    if r['feature'] in ('ppt_single_pay', 'ppt_limited_pay', 'ppt_regular_pay'): v5[r['uin']][r['feature'][4:-4]] = r['code']
YES = {'B', 'O', 'Y'}
bad = 0; out = []; changed = collections.Counter(); changes = []
for uin, single, limited, regular, variants, path, page, quote, note in ROWS:
    ok = False
    for mode in ('-layout', '-raw'):
        t = subprocess.run(['pdftotext', mode, '-f', str(page), '-l', str(page), path, '-'], capture_output=True, text=True).stdout
        if norm(quote) in norm(t): ok = True; break
    if not ok: print('QUOTE NOT FOUND', uin, page, quote[:80]); bad += 1
    out.append([uin, single, limited, regular, variants, lab.get(path, path), path, page, quote, note])
    for k, mine in (('single', single), ('limited', limited.split(',')[0].split(' ')[0]), ('regular', regular)):
        old = v5[uin].get(k, '')
        oldyn = 'Y' if old in YES else ('N' if old == 'N' else '?')
        m = mine[0]
        if m != oldyn: changed[k] += 1; changes.append(f'{uin} {k}: v5 {old or "blank"} -> {mine[:40]}')
with open('results/ppt_grid.csv', 'w', newline='') as o:
    w = csv.writer(o); w.writerow(['uin', 'single_pay', 'limited_pay', 'regular_pay', 'variants', 'doc', 'doc_path', 'page', 'quote', 'note']); w.writerows(out)
print(len(out), 'rows; quote problems', bad, '; changed vs v5', dict(changed))
for c in changes: print('  ', c)
