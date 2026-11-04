#!/usr/bin/env python3
"""Stage a commit that covers only the given insurers (plus the ones already committed), so each push holds
one insurer and index.csv never lists files that are not in the repo yet.

    python3 -I scripts/stage_insurers.py lic sbi-life        # then: git commit ...

Writes filtered copies of index.csv, results/light_discovery_results.csv, results/manual_checklist.csv and a
coverage.md built from them straight into the git index (the working tree keeps the full files), and
`git add`s docs/<slug> and text/<slug> for each slug given, plus master_list.csv and scripts/.
"""
import csv, io, os, subprocess, sys, tempfile, shutil
slugs = set(sys.argv[1:])
M = list(csv.DictReader(open('master_list.csv')))
slug_of_ins = {m['insurer']: m['insurer_slug'] for m in M}
slug_of_row = {m['row_id']: m['insurer_slug'] for m in M}
# insurers already in HEAD's results file count as committed
try:
    head = subprocess.run(['git', 'show', 'HEAD:results/light_discovery_results.csv'], capture_output=True, text=True, check=True).stdout
    slugs |= {slug_of_row[r['row_id']] for r in csv.DictReader(io.StringIO(head))}
except subprocess.CalledProcessError:
    pass
now = set(sys.argv[1:])
def head_rows(path):
    try: return list(csv.DictReader(io.StringIO(subprocess.run(['git', 'show', f'HEAD:{path}'], capture_output=True, text=True, check=True).stdout)))
    except subprocess.CalledProcessError: return []
def filt(path, key):
    rows = list(csv.DictReader(open(path))); cols = list(rows[0].keys()) if rows else open(path).readline().strip().split(',')
    # insurers committed in this call: working-tree rows; other committed insurers: rows exactly as in HEAD
    keep = [r for r in rows if key(r) in now] + [r for r in head_rows(path) if key(r) in slugs - now]
    order = {m['row_id']: i for i, m in enumerate(M)}
    keep.sort(key=lambda r: order.get(r.get('row_id', ''), 0) if 'row_id' in r else 0)
    s = io.StringIO(); w = csv.DictWriter(s, fieldnames=cols, lineterminator='\r\n'); w.writeheader(); w.writerows(keep)
    return s.getvalue()
files = {
    'index.csv': filt('index.csv', lambda r: slug_of_ins.get(r['insurer'])),
    'results/light_discovery_results.csv': filt('results/light_discovery_results.csv', lambda r: slug_of_row.get(r['row_id'])),
    'results/manual_checklist.csv': filt('results/manual_checklist.csv', lambda r: slug_of_ins.get(r['insurer'])),
}
d = tempfile.mkdtemp()
try:
    os.makedirs(os.path.join(d, 'results'))
    for k, v in files.items(): open(os.path.join(d, k), 'w', newline='').write(v)
    shutil.copy('master_list.csv', d)
    subprocess.run([sys.executable, '-I', os.path.abspath('scripts/build_coverage.py')], cwd=d, check=True, stdout=subprocess.DEVNULL)
    files['coverage.md'] = open(os.path.join(d, 'coverage.md')).read()
finally:
    shutil.rmtree(d)
for k, v in files.items():
    sha = subprocess.run(['git', 'hash-object', '-w', '--stdin'], input=v.encode(), capture_output=True, check=True).stdout.decode().strip()
    subprocess.run(['git', 'update-index', '--add', '--cacheinfo', f'100644,{sha},{k}'], check=True)
paths = [p for s in sys.argv[1:] for p in (f'docs/{s}', f'text/{s}') if os.path.exists(p)]
subprocess.run(['git', 'add', '--', *paths, 'master_list.csv', 'scripts/'], check=True)
print('staged for', sorted(slugs))
