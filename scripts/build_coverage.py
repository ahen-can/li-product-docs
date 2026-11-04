#!/usr/bin/env python3
"""Rebuild coverage.md from master_list.csv, index.csv and results/light_discovery_results.csv.

    python3 -I scripts/build_coverage.py

Counts are taken straight from the files: an insurer that has not been run yet shows 'not run'.
'Not published' is only used where results say so (the product page has no such document link).
"""
import csv, collections, os

M = list(csv.DictReader(open('master_list.csv')))
I = [r for r in csv.DictReader(open('index.csv')) if r['status'] == 'ok']
try:
    R = {r['row_id']: r for r in csv.DictReader(open('results/light_discovery_results.csv'))}
except FileNotFoundError:
    R = {}
slug_of = {}
for m in M: slug_of[m['insurer']] = m['insurer_slug']
by = collections.OrderedDict()
for m in sorted(M, key=lambda x: x['insurer']):
    by.setdefault(m['insurer'], []).append(m)
docs = collections.defaultdict(set)
for r in I: docs[(r['insurer'], r['uin'], r['product_name'])].add(r['doc_type'])

out = ['# Coverage', '',
       '`scripts/build_coverage.py` builds this file from `results/light_discovery_results.csv` and `index.csv`.',
       'This pass (light discovery) looks for the **sales brochure** only. The script stores a policy document only when no',
       'brochure passes the checks. "Not found" means neither the script nor a manual look at the site found a file that passes.', '',
       '| Insurer | In-scope active products (master list) | Policy doc found | Brochure found | BI/CIS/leaflet found | Not found | Manual / unavailable | Not published | Not run yet |',
       '|---|---|---|---|---|---|---|---|---|']
manual = []
BLK = {}
if os.path.exists('results/manual_checklist_blocked_sites.csv'):
    BLK = {r['uin']: r['where_to_look'] for r in csv.DictReader(open('results/manual_checklist_blocked_sites.csv'))}
tot = collections.Counter()
for ins, rows in by.items():
    c = collections.Counter()
    for m in rows:
        d = docs.get((m['insurer'], m['uin'], m['product_name']), set())
        if 'policy' in d: c['policy'] += 1
        if 'brochure' in d: c['brochure'] += 1
        if d & {'bi', 'cis', 'leaflet'}: c['bicis'] += 1
        st = R.get(m['row_id'], {}).get('status', '')
        if st == 'not found': c['nf'] += 1
        elif st == 'manual': c['manual'] += 1
        elif st == 'not published': c['np'] += 1
        elif not st: c['notrun'] += 1
        if st in ('not found', 'manual'):
            manual.append((m, R[m['row_id']]))
    c['n'] = len(rows); tot.update(c)
    out.append(f"| {ins} | {c['n']} | {c['policy']} | {c['brochure']} | {c['bicis']} | {c['nf']} | {c['manual']} | {c['np']} | {c['notrun']} |")
out.append(f"| **Total** | {tot['n']} | {tot['policy']} | {tot['brochure']} | {tot['bicis']} | {tot['nf']} | {tot['manual']} | {tot['np']} | {tot['notrun']} |")
out += ['', '## Manual-download list',
        'The script could not fetch these products. Each line gives the product, its UIN, the page to visit and the missing document.', '']
for m, r in manual:
    page = m['website_product_page_url'] or BLK.get(m['uin']) or '(no product page found; see notes)'
    out.append(f"- **{m['insurer']}**: {m['product_name']} (`{m['uin']}`): brochure missing ({r['status']}). Visit {page}. {r['notes']}")
open('coverage.md', 'w').write('\n'.join(out) + '\n')
print('coverage.md written:', dict(tot))
