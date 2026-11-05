"""Adds rows to results/ulip_rider_map.csv for one insurer: python3 -I scripts/s2_tools/ridermap.py SLUG
Finds the page of each ULIP document where a rider UIN is named. Rider names and benefit lists come from RIDERS below."""
import csv, os, re, subprocess, sys
slug = sys.argv[1]
OUT = 'results/ulip_rider_map.csv'
H = ['ulip_uin', 'ulip_name', 'rider_uin', 'rider_name', 'link_stated_in', 'benefits_covered']
RIDERS = {
 '130A012V02': ('Bharti AXA Life Linked Complete Shield Rider', 'waiver of premium (option, on accidental total and permanent disability or critical illness); critical illness (standard, comprehensive, cancer care); accidental death; accidental disability (total and permanent, partial)'),
 '130A034V01': ('Bharti AXA Life Cover Plus Linked Term Rider', 'term cover (death from any cause); no waiver, critical illness or disability'),
}
ulips = [r for r in csv.DictReader(open('briefs/ulip_riders_named.csv')) if r['ulip_uin'] in {x['uin'] for x in csv.DictReader(open('index.csv')) if x['file_path'].startswith(f'docs/{slug}/')}]
done = {(r['ulip_uin'], r['rider_uin']) for r in csv.DictReader(open(OUT))} if os.path.exists(OUT) else set()
new = not os.path.exists(OUT)
rows = []
for u in ulips:
    found = False
    for dt in ('brochure', 'policy', 'cis'):
        pdf = f'docs/{slug}/{u["ulip_uin"]}/{dt}.pdf'
        if not os.path.exists(pdf): continue
        pages = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout.split('\f')
        for ruin, (rname, ben) in RIDERS.items():
            for i, p in enumerate(pages, 1):
                if ruin in re.sub(r'\s', '', p) or ruin in p:
                    if (u['ulip_uin'], ruin) not in done:
                        rows.append([u['ulip_uin'], u['ulip_name'], ruin, rname, f'{dt}, page {i}', ben]); done.add((u['ulip_uin'], ruin)); found = True
                    break
    if not any(r[0] == u['ulip_uin'] for r in rows) and not any(k[0] == u['ulip_uin'] for k in done):
        rows.append([u['ulip_uin'], u['ulip_name'], '', '', '', 'no rider named in the documents'])
with open(OUT, 'a', newline='') as o:
    w = csv.writer(o)
    if new: w.writerow(H)
    w.writerows(rows)
print(len(rows), 'rows')
