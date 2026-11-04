#!/usr/bin/env python3
"""Check CLAUDE.md invariants: every docs/ file has an index row, every index row's files exist, doc_ids unique,
every ok result has exactly one index row, files start with %PDF and are under 95 MB.
    python3 -I scripts/check_consistency.py [results_file ...]
"""
import csv, collections, glob, os, sys
I = list(csv.DictReader(open('index.csv')))
files = set(glob.glob('docs/*/*/*.pdf'))
paths = collections.Counter(r['file_path'] for r in I)
ids = collections.Counter(r['doc_id'] for r in I)
bad = 0
for f in sorted(files - set(paths)): print('no index row:', f); bad += 1
for r in I:
    for k in ('file_path', 'text_path'):
        if not os.path.exists(r[k]): print('missing', k, r['doc_id'], r[k]); bad += 1
    if os.path.exists(r['file_path']):
        if open(r['file_path'], 'rb').read(4) != b'%PDF': print('not a PDF:', r['file_path']); bad += 1
        if os.path.getsize(r['file_path']) > 95 * 2**20: print('over 95 MB:', r['file_path']); bad += 1
for k, n in ids.items():
    if n > 1: print('duplicate doc_id', k, n); bad += 1
for f, n in paths.items():
    if n > 1:
        notes = [r['notes'] for r in I if r['file_path'] == f]
        if sum('same file as' in x for x in notes) != n - 1: print('file shared without dedupe note', f, n); bad += 1
for rf in sys.argv[1:] or ['results/light_discovery_results.csv']:
    keys = collections.Counter((r['uin'], r['product_name'], r['doc_type']) for r in I)   # the light pass keeps one file per product
    for r in csv.DictReader(open(rf)):
        if r['status'] == 'ok' and keys[(r['uin'], r['product_name'], r['doc_type'])] != 1:
            print(rf, 'ok result with', keys[(r['uin'], r['product_name'], r['doc_type'])], 'index rows of its doc type:', r['row_id'], r['product_name']); bad += 1
print('problems:', bad, '| index rows', len(I), '| files', len(files))
