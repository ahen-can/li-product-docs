"""Wave 1 cross-check of every ULIP JSON against the deep set, the index and the stored files."""
import csv, json, os, hashlib, re, subprocess, collections
deep = [r for r in csv.DictReader(open('briefs/ulip_deep_set.csv')) if r['wave'].startswith('Wave 1')]
idx = list(csv.DictReader(open('index.csv'))); inv = list(csv.DictReader(open('results/deep_ulip_docs.csv')))
by_uin = collections.defaultdict(list)
for r in idx: by_uin[r['uin']].append(r)
problems = []; rows = []
for d in deep:
    uin = d['uin']; p = f'features/ulip/{uin}.json'
    if not os.path.exists(p): problems.append((uin, 'no JSON')); continue
    j = json.load(open(p))
    if j['product']['uin']['value'] != uin: problems.append((uin, 'JSON uin differs'))
    nm = j['product']['product_name']['value']
    types = collections.Counter(); notes = []
    for r in by_uin[uin]:
        if not r['file_path']: continue
        types[r['doc_type']] += 1
        if not os.path.exists(r['file_path']): problems.append((uin, f"missing file {r['file_path']}")); continue
        b = open(r['file_path'], 'rb').read()
        if hashlib.sha256(b).hexdigest() != r['sha256']: problems.append((uin, f"sha256 differs {r['file_path']}"))
        if not b.startswith(b'%PDF'): problems.append((uin, f"not a PDF {r['file_path']}"))
        if r['status'] not in ('ok',): notes.append(f"{r['doc_type']} status={r['status']}")
        t = r['text_path']
        if t and os.path.exists(t):
            txt = open(t, errors='ignore').read()
            pgs = max(1, int(r['pages'] or 1))
            if len(txt) / pgs < 200 and r['is_scanned'] != 'Y': problems.append((uin, f"thin text, not marked scanned: {r['file_path']}"))
            if r['doc_type'] in ('policy', 'brochure', 'cis') and uin not in txt.replace(' ', '') and uin[:7] not in txt.replace(' ', ''): notes.append(f"{r['doc_type']}: UIN not printed")
    for need in ('policy', 'brochure', 'cis'):
        if types[need] == 0: notes.append(f'no {need}')
    nd = len(j.get('data_not_public', [])); ns = sum(1 for g in ('product', 'eligibility', 'charges', 'benefits', 'flexibility', 'funds', 'protection_add_ons', 'surrender_revival') for f in j[g].values() if isinstance(f, dict) and f.get('status') == 'not stated in public documents')
    nq = sum(1 for g in ('product', 'eligibility', 'charges', 'benefits', 'flexibility', 'funds', 'protection_add_ons', 'surrender_revival') for f in j[g].values() if isinstance(f, dict) and f.get('quote'))
    rows.append((d['insurer'], uin, nm, dict(types), ns, nq, notes))
tot = collections.Counter()
for ins, uin, nm, t, ns, nq, notes in rows:
    for k, v in t.items(): tot[(ins, k)] += v
print('products checked:', len(rows), '| problems:', len(problems))
for pr in problems: print('  PROBLEM', pr)
print()
for ins in dict.fromkeys(r[0] for r in rows):
    sub = [r for r in rows if r[0] == ins]
    print(f"{ins}: {len(sub)} products; docs " + ', '.join(f'{k} {tot[(ins, k)]}' for k in ('policy', 'cis', 'brochure', 'bi', 'fund_factsheet', 'leaflet') if tot[(ins, k)]))
    for r in sub:
        print(f"   {r[1]} {r[2][:48]:48} not-stated {r[4]:2} quoted {r[5]:2} {'; '.join(r[6])}")
