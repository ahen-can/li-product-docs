#!/usr/bin/env python3
"""Append a note to products' rows in results/light_discovery_results.csv and index.csv.
    python3 -I scripts/add_note.py 251,265 "HDFC site lists this product only under withdrawn policy documents"
"""
import csv, os, sys
rows, note = set(sys.argv[1].split(',')), sys.argv[2]
M = {m['row_id']: m for m in csv.DictReader(open('master_list.csv'))}
keys = {(M[r]['uin'], M[r]['product_name']) for r in rows}
def upd(path, match):
    R = list(csv.DictReader(open(path))); cols = list(R[0].keys()); n = 0
    for r in R:
        if match(r) and note not in r['notes']:
            r['notes'] = '; '.join(x for x in (r['notes'], note) if x); n += 1
    with open(path + '.tmp', 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(R)
    os.replace(path + '.tmp', path); return n
print('results', upd('results/light_discovery_results.csv', lambda r: r['row_id'] in rows),
      'index', upd('index.csv', lambda r: (r['uin'], r['product_name']) in keys))
