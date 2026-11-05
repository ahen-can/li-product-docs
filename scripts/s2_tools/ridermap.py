"""Rebuilds results/ulip_rider_map.csv for the given insurer slugs (appending to other insurers' rows):
    python3 -I scripts/s2_tools/ridermap.py bharti-life sbi-life
For each ULIP of the insurer it finds the pages of its brochure, policy and CIS where a stored rider's UIN appears.
Rider names and the benefit list come from features/riders/<UIN>.json."""
import csv, glob, json, os, re, subprocess, sys
OUT = 'results/ulip_rider_map.csv'
H = ['ulip_uin', 'ulip_name', 'rider_uin', 'rider_name', 'link_stated_in', 'benefits_covered']
def benefits(d):
    names = {'waiver_of_premium': 'waiver of premium', 'critical_illness': 'critical illness', 'accidental_death': 'accidental death',
             'accidental_disability': 'accidental disability', 'term_cover': 'term cover', 'hospital_cash': 'hospital cash'}
    out = [n for k, n in names.items() if d['benefits'][k]['status'].startswith('covered')]
    return '; '.join(out) or 'none of the listed benefits'
slugs = sys.argv[1:]
keep = [r for r in csv.DictReader(open(OUT))] if os.path.exists(OUT) else []
ulip_slug = {}
for x in csv.DictReader(open('index.csv')):
    if x['file_path'].startswith('docs/') and '/riders/' not in x['file_path']: ulip_slug[x['uin']] = x['file_path'].split('/')[1]
named = {r['ulip_uin']: r for r in csv.DictReader(open('briefs/ulip_riders_named.csv'))}
new = []
MAN = 'scripts/s2_tools/ridermap_manual.csv'   # ulip_uin, rider_uin, link_stated_in: links found on the product page, not in the ULIP documents
manual = [r for r in csv.DictReader(open(MAN))] if os.path.exists(MAN) else []
for slug in slugs:
    riders = {}
    for f in glob.glob('features/riders/*.json'):
        d = json.load(open(f)); u = d['rider']['uin']['value']
        if os.path.isdir(f'docs/{slug}/riders/{u}'): riders[u] = (d['rider']['name']['value'], benefits(d))
    for uin, nm in named.items():
        if ulip_slug.get(uin) != slug: continue
        n0 = len(new)
        for dt in ('brochure', 'policy', 'cis'):
            pdf = f'docs/{slug}/{uin}/{dt}.pdf'
            if not os.path.exists(pdf): continue
            pages = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout.split('\f')
            for ruin, (rname, ben) in riders.items():
                if any(r[0] == uin and r[2] == ruin for r in new): continue
                for i, p in enumerate(pages, 1):
                    if ruin in p or ruin in re.sub(r'\s', '', p):
                        new.append([uin, nm['ulip_name'], ruin, rname, f'{dt}, page {i}', ben]); break
        for m in manual:
            if m['ulip_uin'] == uin and m['rider_uin'] in riders and not any(r[0] == uin and r[2] == m['rider_uin'] for r in new):
                new.append([uin, nm['ulip_name'], m['rider_uin'], riders[m['rider_uin']][0], m['link_stated_in'], riders[m['rider_uin']][1]])
        if len(new) == n0: new.append([uin, nm['ulip_name'], '', '', '', 'no rider named in the documents'])
rows = [[r[h] for h in H] for r in keep if ulip_slug.get(r['ulip_uin']) not in slugs] + new
rows.sort(key=lambda r: (r[0], r[2]))
with open(OUT, 'w', newline='') as o:
    w = csv.writer(o); w.writerow(H); w.writerows(rows)
print(len(new), 'rows for', slugs, '| total', len(rows))
