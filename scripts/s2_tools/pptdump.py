"""Dumps, per ULIP, the PT/PPT evidence for the pay-term re-read: v5 codes, the deep JSON values, and the text of the cited pages.
python3 -I scripts/s2_tools/pptdump.py <UIN prefix> > out.txt"""
import csv, json, glob, re, subprocess, sys, collections
pre = sys.argv[1]
idx = collections.defaultdict(list)
for r in csv.DictReader(open('index.csv')): idx[r['uin']].append(r)
v5 = collections.defaultdict(dict)
for r in csv.DictReader(open('analysis/product_features_ulip_v5.csv')):
    if r['feature'] in ('ppt_single_pay', 'ppt_limited_pay', 'ppt_regular_pay'): v5[r['uin']][r['feature'][4:]] = r['code']
def pdf_for(uin, label):
    for r in idx[uin]:
        if r['website_label'] == label or r['file_path'].endswith(label): return r['file_path']
    for r in idx[uin]:
        if label and label.split('.')[0][:20].lower() in (r['source_url'] + r['website_label']).lower(): return r['file_path']
    return None
KW = re.compile(r'premium pay|payment term|\bppt\b|policy term|single|regular|limited|pay(ing)? term|\bpt\b', re.I)
for f in sorted(glob.glob(f'features/ulip/{pre}*.json')):
    d = json.load(open(f)); u = d['product']['uin']['value']; e = d['eligibility']
    print('=' * 100); print(u, d['product']['product_name']['value'], '| v5', v5[u])
    pages = set()
    for k in ('policy_term_options', 'ppt_options', 'premium_min_single'):
        v = e.get(k, {}); print(f'  {k}: {json.dumps(v.get("value"))[:400]} | {v.get("doc")} p{v.get("page")}')
        if v.get('page'): pages.add((v.get('doc'), v.get('page')))
    for doc, p in sorted(pages, key=str):
        path = pdf_for(u, doc)
        if not path: print('  [no file for', doc, ']'); continue
        t = subprocess.run(['pdftotext', '-layout', '-f', str(p), '-l', str(p), path, '-'], capture_output=True, text=True).stdout.split('\n')
        keep = set()
        for i, l in enumerate(t):
            if KW.search(l): keep.update(range(max(0, i - 2), i + 4))
        print(f'  --- {path} p{p} ---')
        for i in sorted(keep):
            if i < len(t) and t[i].strip(): print('   |', t[i][:170])
