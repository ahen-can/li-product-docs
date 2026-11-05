"""Universal rider list from the Life Insurance Council in-force list (Sep-2026), for a later tally
against S2's rider lists. Council fields are copied verbatim; nothing is classified from rider names.
Inputs: sources/life-council/council_rows_parsed.csv, master_list.csv (insurer short names),
briefs/ulip_riders_named.csv and results/ulip_rider_map.csv (riders our 84 ULIPs name).
Outputs: analysis/riders/rider_list_council.csv and .xlsx
Usage: python3 -I analysis/scripts/build_rider_list_council.py <repo_dir>"""
import csv, os, re, sys, collections as C
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

R = sys.argv[1]
council = list(csv.DictReader(open(os.path.join(R, 'sources/life-council/council_rows_parsed.csv'), encoding='utf-8')))
short = {}
for r in csv.DictReader(open(os.path.join(R, 'master_list.csv'), encoding='utf-8')):
    short.setdefault(r['uin'][:3], r['insurer'])
for r in council:
    short.setdefault(r['uin'][:3], r['insurer'])

# riders named by the 84 wave-1 ULIPs
named = C.defaultdict(set)
for r in csv.DictReader(open(os.path.join(R, 'briefs/ulip_riders_named.csv'), encoding='utf-8')):
    for u in re.findall(r'\d{3}[AB]\d{3}V\d{2}', r['rider_uins_named']):
        named[u].add(r['ulip_uin'])
mp = os.path.join(R, 'results/ulip_rider_map.csv')
if os.path.exists(mp):
    for r in csv.DictReader(open(mp, encoding='utf-8')):
        if r['rider_uin']:
            named[r['rider_uin']].add(r['ulip_uin'])
base = lambda u: u[:7]   # UIN without version

rows = []
cbase = C.defaultdict(list)
for r in council:
    if r['section'] != 'Riders':
        continue
    u = r['uin']
    t = u[3]
    exact = sorted(named.get(u, []))
    other_ver = sorted({x for k, v in named.items() if base(k) == base(u) and k != u for x in v})
    rows.append({'insurer': short.get(u[:3], r['insurer']), 'insurer_council_name': r['insurer'], 'rider_name': r['name'], 'uin': u,
                 'linked_flag_uin': {'A': 'A (linked rider)', 'B': 'B (non-linked rider)'}.get(t, t),
                 'line_of_business': r['lob'], 'council_category': r['category'],
                 'named_by_wave1_ulips': len(exact) or '', 'ulips_naming_it': '; '.join(exact),
                 'other_version_named_by_ulips': '; '.join(other_ver),
                 'source': 'Life Insurance Council in-force list, Sep-2026 (provisional), Riders section'})
    cbase[base(u)].append(u)
rows.sort(key=lambda x: (x['insurer'], x['line_of_business'] != 'Individual', x['uin']))

# ULIP-named riders missing from the Council list
missing = []
for u, ul in sorted(named.items()):
    if any(r['uin'] == u for r in rows):
        continue
    missing.append({'uin': u, 'insurer': short.get(u[:3], ''), 'ulips_naming_it': '; '.join(sorted(ul)),
                    'council_versions_of_same_rider': '; '.join(cbase.get(base(u), [])) or 'none',
                    'note': 'version differs from Council' if cbase.get(base(u)) else 'not in Council list'})

os.makedirs(os.path.join(R, 'analysis/riders'), exist_ok=True)
with open(os.path.join(R, 'analysis/riders/rider_list_council.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)

# summary per insurer
summ = C.defaultdict(C.Counter)
for r in rows:
    s = summ[r['insurer']]
    s['total'] += 1
    s[r['line_of_business']] += 1
    if r['line_of_business'] == 'Individual':
        s['ind_' + r['linked_flag_uin'][0]] += 1
    if r['named_by_wave1_ulips']:
        s['named'] += 1

wb = Workbook(); wb.remove(wb.active)
HEAD = PatternFill('solid', fgColor='1F3864'); HF = Font(bold=True, color='FFFFFF'); WR = Alignment(wrap_text=True, vertical='top')
def sheet(title, header, data, widths=None, note=None):
    ws = wb.create_sheet(title); r0 = 1
    if note:
        ws.cell(1, 1, note).alignment = WR; ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=min(len(header), 8))
        ws.row_dimensions[1].height = 60; r0 = 3
    for j, h in enumerate(header, 1):
        c = ws.cell(r0, j, h); c.fill = HEAD; c.font = HF; c.alignment = WR
    for i, row in enumerate(data, r0 + 1):
        for j, v in enumerate(row, 1):
            ws.cell(i, j, v).alignment = WR
    for j in range(1, len(header) + 1):
        ws.column_dimensions[get_column_letter(j)].width = (widths or {}).get(j, 16)
    ws.freeze_panes = ws.cell(r0 + 1, 1)
    ws.auto_filter.ref = f'A{r0}:{get_column_letter(len(header))}{r0 + len(data)}'

ind = [r for r in rows if r['line_of_business'] == 'Individual']
sheet('README', ['Item', 'Detail'], [
    ['What', 'Every rider in the Life Insurance Council in-force list (Sep-2026, provisional), Riders section. Built to tally against S2\'s universal and relevant rider lists.'],
    ['Counts', f'{len(rows)} riders: {len(ind)} individual ({sum(r["linked_flag_uin"][0] == "A" for r in ind)} linked "A", {sum(r["linked_flag_uin"][0] == "B" for r in ind)} non-linked "B"), {len(rows) - len(ind)} group. {len(summ)} insurers.'],
    ['Linked flag', 'From the UIN\'s 4th character (IRDAI code): A = linked rider, B = non-linked rider. A ULIP can attach only an A rider, unless the rider document says otherwise.'],
    ['Category', 'Council category copied as written (Health, Accident, Term, Traditional, Others...). Not re-classified. Rider names are not used to classify.'],
    ['Wave 1 link', 'named_by_wave1_ulips: how many of our 84 ULIPs name this exact UIN (deep data plus S2\'s rider map). other_version_named_by_ulips: the ULIP names a different version of the same rider.'],
    ['Known gaps', 'The Council list is self-reported and provisional. In the product section it showed no individual products for SBI, Bajaj, Edelweiss and Canara HSBC; check their riders against S2\'s list. Withdrawn riders are not in it.'],
    ['Next', 'When S2 pushes its universal rider list, tally by UIN: in both, Council only, S2 only, version differs.'],
], {1: 18, 2: 120})
sheet('Summary by insurer', ['Insurer', 'Riders', 'Individual', 'Individual linked (A)', 'Individual non-linked (B)', 'Group', 'Named by our ULIPs'],
      [[k, v['total'], v['Individual'], v['ind_A'], v['ind_B'], v['Group'], v['named']] for k, v in sorted(summ.items())], {1: 28})
H = ['Insurer', 'Rider name', 'UIN', 'Linked flag (UIN)', 'Line of business', 'Council category', 'Named by wave 1 ULIPs', 'ULIPs naming it', 'Other version named by ULIPs', 'Insurer (Council name)']
K = ['insurer', 'rider_name', 'uin', 'linked_flag_uin', 'line_of_business', 'council_category', 'named_by_wave1_ulips', 'ulips_naming_it', 'other_version_named_by_ulips', 'insurer_council_name']
W = {1: 22, 2: 55, 3: 13, 4: 18, 6: 18, 8: 40, 9: 30, 10: 40}
sheet('Individual riders', H, [[r[k] for k in K] for r in ind], W)
sheet('Linked riders (A)', H, [[r[k] for k in K] for r in rows if r['linked_flag_uin'][0] == 'A'], W, note='Riders a ULIP can attach. Includes group riders where the Council marks them linked.')
sheet('All riders', H, [[r[k] for k in K] for r in rows], W)
sheet('ULIP riders not in Council', ['UIN', 'Insurer', 'ULIPs naming it', 'Council versions of the same rider', 'Note'],
      [[m[k] for k in ('uin', 'insurer', 'ulips_naming_it', 'council_versions_of_same_rider', 'note')] for m in missing], {3: 40, 4: 30, 5: 30},
      note='Rider UINs our ULIP documents name that the Council list does not carry in that version. Check on the insurer site.')
wb.save(os.path.join(R, 'analysis/riders/rider_list_council.xlsx'))
# ---------- tally against S2's universal list (results/riders_universal.csv) ----------
up = os.path.join(R, 'results/riders_universal.csv')
if os.path.exists(up):
    s2 = {r['rider_uin']: r for r in csv.DictReader(open(up, encoding='utf-8')) if r['rider_uin']}
    cu = {r['uin']: r for r in rows}
    s2_ins = {r['insurer'] for r in s2.values()}
    T = []
    for u in sorted(set(s2) | {u for u, r in cu.items() if r['insurer'] in s2_ins}):
        a, b = cu.get(u), s2.get(u)
        if a and b: st = 'in both'
        elif b:
            vers = cbase.get(base(u), [])
            st = 'S2 only, Council has ' + ', '.join(vers) if vers else 'S2 only'
        else:
            s2v = [x for x in s2 if base(x) == base(u)]
            st = 'Council only, S2 has ' + ', '.join(s2v) if s2v else 'Council only'
        r0 = a or {}; r1 = b or {}
        T.append([r0.get('insurer') or r1.get('insurer'), r1.get('rider_name') or r0.get('rider_name'), u, st,
                  r0.get('line_of_business', ''), r0.get('council_category', ''), r1.get('base_type', ''), r1.get('download_status', ''), r1.get('source_page_url', '')])
    cnt = C.Counter(t[3].split(',')[0] for t in T)
    sheet('Tally vs S2', ['Insurer', 'Rider name', 'UIN', 'Result', 'Council line of business', 'Council category', 'S2 base type', 'S2 download status', 'S2 source page'], T,
          {1: 20, 2: 50, 3: 13, 4: 30, 7: 22, 8: 18, 9: 50},
          note=f"S2's universal list covers the 10 wave 1 insurers only, so this tally is limited to them. {dict(cnt)}. 'S2 only' or 'Council only' with another version named = same rider, different version.")
    wb.save(os.path.join(R, 'analysis/riders/rider_list_council.xlsx'))
    print('tally', dict(cnt))
print(len(rows), 'riders;', len(ind), 'individual;', 'named by ULIPs:', sum(1 for r in rows if r['named_by_wave1_ulips']), '; missing from Council:', len(missing))
for m in missing: print(' ', m)
