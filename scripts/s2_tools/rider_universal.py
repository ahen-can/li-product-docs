"""Rebuilds results/riders_universal.csv: every rider in the Life Council Sep-2026 list (analysis/riders/rider_list_council.csv),
plus riders found on insurer sites that are not in it, with what is stored for each. python3 -I scripts/s2_tools/rider_universal.py"""
import csv, collections, os
council = list(csv.DictReader(open('analysis/riders/rider_list_council.csv')))
docs = collections.defaultdict(list); names = {}; ins_of = {}; found_on = {}
for r in csv.DictReader(open('index.csv')):
    if '/riders/' in r['file_path']:
        docs[r['uin']].append(r['doc_type'].replace('rider_', '')); names.setdefault(r['uin'], r['product_name']); ins_of[r['uin']] = r['insurer']
        found_on.setdefault(r['uin'], r['found_on_page_url'])
old = {r['rider_uin']: r for r in csv.DictReader(open('results/riders_universal.csv'))} if os.path.exists('results/riders_universal.csv') else {}
BLOCKED = {'ICICI Life', 'Kotak Mahindra Life', 'Star Union Dai-ichi Life'}
base = collections.defaultdict(set)
for u in docs: base[u[:7]].add(u)
def status(ins, u):
    d = docs.get(u, [])
    if d:
        has = set(t.split('-')[0] for t in d)
        if {'brochure', 'policy'} <= has: return 'downloaded (brochure and policy)', d
        return 'downloaded (partial: ' + ', '.join(sorted(has)) + ')', d
    other = sorted(base.get(u[:7], set()) - {u})
    if other: return 'other version stored: ' + ', '.join(other), []
    if ins in BLOCKED: return 'not downloaded (site blocks automation; manual)', []
    return 'not downloaded', []
H = ['insurer', 'rider_uin', 'rider_name', 'linked_flag', 'line_of_business', 'in_council_list', 'named_by_wave1_ulips', 'download_status', 'documents_stored', 'source_page', 'notes']
rows = []; seen = set()
for c in council:
    st, d = status(c['insurer'], c['uin'])
    rows.append([c['insurer'], c['uin'], c['rider_name'], c['linked_flag_uin'], c['line_of_business'], 'yes', c['named_by_wave1_ulips'], st, '; '.join(sorted(d)), found_on.get(c['uin'], ''), old.get(c['uin'], {}).get('notes', '')])
    seen.add(c['uin'])
for u in sorted(docs):
    if u in seen: continue
    st, d = status(ins_of[u], u)
    rows.append([ins_of[u], u, names[u], 'A (linked rider)' if u[3] == 'A' else 'B (non-linked rider)', '', 'no (other version or not listed)', '', st, '; '.join(sorted(d)), found_on.get(u, ''), 'Found on the insurer site; the Council list has another version or none.'])
    seen.add(u)
for u, r in old.items():
    if u and u not in seen and not any(u[:7] == s[:7] for s in seen):
        rows.append([r['insurer'], u, r['rider_name'], r.get('base_type', ''), '', 'no', '', r['download_status'], '', r.get('source_page_url', ''), r.get('notes', '')])
rows.sort(key=lambda x: (x[0], x[1]))
csv.writer(open('results/riders_universal.csv', 'w', newline='')).writerows([H] + rows)
c = collections.Counter(r[7].split(' (')[0].split(':')[0] for r in rows)
print(len(rows), 'riders;', dict(c))
byins = collections.defaultdict(lambda: [0, 0])
for r in rows:
    byins[r[0]][0] += 1; byins[r[0]][1] += r[7].startswith('downloaded')
for k, v in sorted(byins.items()): print(f'  {k}: {v[1]} of {v[0]}')
