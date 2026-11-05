"""Removes harvested rider files that fail the harvester's rider tests (product document, or no "rider" in the name or
first page). Rewrites index.csv, results/riders_downloaded.csv and the harvest log outcome. python3 -I scripts/s2_tools/rider_prune.py"""
import csv, os, re, subprocess
bad = []
log = list(csv.DictReader(open('results/rider_harvest_log.csv')))
for r in log:
    if r['outcome'] != 'stored': continue
    fp = r['stored_path']; txt = subprocess.run(['pdftotext', '-layout', fp, '-'], capture_output=True, text=True).stdout
    code = r['rider_uin'][:3]; t = txt.replace(' ', '')
    rid = t.count(r['rider_uin']); allu = re.findall(code + r'[A-Z]\d{3}V\d{2}', t)
    top = max(set(allu), key=allu.count)
    first = re.sub(r'\s+', ' ', txt.split('\f')[0])[:800]
    name = r['url'].split('/')[-1]
    why = None
    if top[3] not in 'AB' and allu.count(top) >= rid: why = f'product document ({top})'
    elif not (re.search('rider', r['label'] + ' ' + name, re.I) or re.search('rider', first, re.I)): why = 'not a rider document'
    if why: bad.append((fp, why)); r['outcome'] = 'removed: ' + why; r['stored_path'] = ''
paths = {b[0] for b in bad}
for fp, why in bad:
    os.remove(fp); tp = fp.replace('docs/', 'text/').replace('.pdf', '.txt')
    if os.path.exists(tp): os.remove(tp)
    for d in (os.path.dirname(fp), os.path.dirname(tp)):
        if os.path.isdir(d) and not os.listdir(d): os.rmdir(d)
    print('removed', fp, why)
for f, col in (('index.csv', 'file_path'), ('results/riders_downloaded.csv', 'stored_path')):
    rows = list(csv.reader(open(f))); H = rows[0]; i = H.index(col)
    csv.writer(open(f, 'w', newline='')).writerows([H] + [x for x in rows[1:] if x[i] not in paths])
with open('results/rider_harvest_log.csv', 'w', newline='') as o:
    w = csv.DictWriter(o, fieldnames=list(log[0].keys())); w.writeheader(); w.writerows(log)
