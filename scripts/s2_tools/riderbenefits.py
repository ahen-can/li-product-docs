"""Rebuilds results/ulip_rider_benefits.csv from results/ulip_rider_map.csv and features/riders/*.json."""
import csv, glob, json, collections
WAIVES = {'111A049V01': 'yes', '101A035V01': 'yes', '110A026V03': 'yes', '110A025V03': 'yes', '110A032V05': 'yes (payout option)',
          '110A048V04': 'yes (payout option)', '109A039V01': 'yes', '104A049V03': 'yes (payor benefit, death or terminal illness only)',
          '130A012V02': 'unclear (wording says "base cover")'}
R = {json.load(open(f))['rider']['uin']['value']: json.load(open(f)) for f in glob.glob('features/riders/*.json')}
by = collections.OrderedDict()
for r in csv.DictReader(open('results/ulip_rider_map.csv')):
    by.setdefault((r['ulip_uin'], r['ulip_name']), [])
    if r['rider_uin']: by[(r['ulip_uin'], r['ulip_name'])].append(r['rider_uin'])
keys = ['critical_illness', 'accidental_death', 'accidental_disability', 'term_cover', 'hospital_cash']
with open('results/ulip_rider_benefits.csv', 'w', newline='') as o:
    w = csv.writer(o); w.writerow(['ulip_uin', 'ulip_name', 'riders_stored', 'waiver_of_ulip_premium_through'] + keys)
    for (u, n), rs in sorted(by.items()):
        w.writerow([u, n, '; '.join(rs), '; '.join(f'{x}: {WAIVES[x]}' for x in rs if x in WAIVES) or 'none through a named rider'] +
                   ['; '.join(x for x in rs if R[x]['benefits'][k]['status'].startswith('covered')) for k in keys])
print(len(by), 'ULIPs')
