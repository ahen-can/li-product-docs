"""Master list v2: website-first, Council as cross-check. No category inferred from names.
Usage: build_master_v2.py council_xls_rows.csv website_rows.csv out_dir
Outputs: master_list.csv, website_products.csv, discrepancies.csv, coverage_summary.csv"""
import csv, sys, os, collections, re

CF, WF, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
SLUG = {'101': 'hdfc-life', '104': 'axis-max-life', '105': 'icici-life', '107': 'kotak-life', '109': 'absli', '110': 'tata-aia', '111': 'sbi-life',
        '116': 'bajaj-life', '117': 'pnb-metlife', '121': 'indusind-nippon', '122': 'aviva-life', '128': 'shriram-life', '130': 'bharti-life',
        '133': 'generali-central', '135': 'ageas-federal', '136': 'canara-hsbc', '138': 'bandhan-life', '140': 'pramerica-life',
        '142': 'sud-life', '143': 'indiafirst', '147': 'edelweiss-life', '163': 'creditaccess-life', '164': 'acko-life', '165': 'go-digit-life', '512': 'lic'}
NAME = {'101': 'HDFC Life', '104': 'Axis Max Life', '105': 'ICICI Life (formerly ICICI Prudential)', '107': 'Kotak Mahindra Life', '109': 'Aditya Birla Sun Life',
        '110': 'Tata AIA Life', '111': 'SBI Life', '116': 'Bajaj Life', '117': 'PNB MetLife', '121': 'IndusInd Nippon Life', '122': 'Aviva Life',
        '128': 'Shriram Life', '130': 'Bharti Life', '133': 'Generali Central Life', '135': 'Ageas Federal Life', '136': 'Canara HSBC Life',
        '138': 'Bandhan Life', '140': 'Pramerica Life', '142': 'Star Union Dai-ichi Life', '143': 'IndiaFirst Life', '147': 'Edelweiss Life',
        '163': 'CreditAccess Life', '164': 'Acko Life', '165': 'Go Digit Life', '512': 'LIC'}
BLOCKED = {'105': 'site blocks automated access (403)', '107': 'site serves a bot-check page; not bypassed', '142': 'site blocks automated access (403)',
           '165': 'site blocks automated access (403)'}
WEAK = {'143': 'product pages do not show UINs; website check incomplete', '164': 'product pages not in sitemap; website check incomplete'}

C = list(csv.DictReader(open(CF)))
W = list(csv.DictReader(open(WF)))
council = {}
for r in C:
    if r['section'] == 'Products' and r['uin'][3] in 'NL':
        council[r['uin'][:7]] = r

ev = collections.defaultdict(lambda: {'current': {}, 'withdrawn': {}, 'unknown': {}, 'live': {}, 'names': set(), 'desc': set()})
for r in W:
    u = r['uin']
    if u[3] not in 'NL':
        continue
    e = ev[u[:7]]
    k = 'withdrawn' if r['status_site'] == 'withdrawn' else ('unknown' if 'not stated' in r['status_site'] else ('live' if r['status_site'].startswith('page live') else 'current'))
    e[k].setdefault(u, set()).add(r['page_url'])
    if r['name_site']: e['names'].add(r['name_site'])
    if r['irdai_description_line']: e['desc'].add(r['irdai_description_line'])

def vnum(u): return int(u[-2:])

master, disc = [], []
for code in sorted(set(council) | set(ev), key=lambda c: (c[:3], c)):
    pre = code[:3]
    if pre not in NAME or pre == '114':
        continue
    cr = council.get(code); e = ev.get(code)
    cur_v = max(e['current'], key=vnum) if e and e['current'] else ''
    wd_v = max(e['withdrawn'], key=vnum) if e and e['withdrawn'] else ''
    if pre in BLOCKED:
        wstat = 'website not readable'
    elif cur_v and (not wd_v or vnum(cur_v) >= vnum(wd_v)):
        wstat = 'current'
    elif wd_v and (not cr or vnum(wd_v) >= vnum(cr['uin'])):
        wstat = 'withdrawn'
    elif wd_v:
        wstat = 'older version withdrawn; current version not found on site'
    elif e and e['unknown']:
        wstat = 'listed on site, status not stated'
    elif e and e['live']:
        wstat = 'page live, not in current plan listings'
    elif pre in WEAK:
        wstat = 'not found (website check incomplete)'
    else:
        wstat = 'not found on website'
    in_c = cr is not None
    lob = cr['lob'] if cr else ''
    # scope: individual products. Council LoB is official; website-only rows have no LoB -> kept, flagged
    if in_c and lob != 'Individual':
        continue
    if not in_c and wstat != 'current':
        continue          # website-only rows are included only when the site shows them as current
    uin_site = cur_v or wd_v or (max(e['unknown'], key=vnum) if e and e['unknown'] else '') or (max(e['live'], key=vnum) if e and e['live'] else '')
    urls = sorted(set().union(*(e[k].get(uin_site, set()) for k in ('current', 'withdrawn', 'unknown', 'live')))) if e and uin_site else []
    notes = []
    if in_c and wstat == 'withdrawn':
        notes.append('Council lists in-force but website lists as WITHDRAWN')
    if in_c and wstat == 'not found on website':
        notes.append('On Council list, not found on website')
    if not in_c:
        notes.append('On website, not on Council list (line of business not stated)')
    if in_c and uin_site and cr['uin'] != uin_site:
        notes.append(f"UIN version differs: Council {cr['uin']} vs website {uin_site}")
    site_names = sorted(e['names']) if e else []
    row = {'insurer': NAME[pre], 'product_code': code, 'uin_council': cr['uin'] if cr else '', 'uin_website': uin_site,
           'product_name_council': cr['name'] if cr else '', 'product_name_website': ' || '.join(site_names)[:200],
           'line_of_business_council': lob, 'linked_flag_uin': code[3], 'category_council': cr['category'] if cr else '',
           'irdai_description_line_website': ' || '.join(sorted(e['desc']))[:250] if e else '',
           'in_council_sep2026': 'Y' if in_c else 'N', 'website_status': wstat,
           'website_note': BLOCKED.get(pre) or WEAK.get(pre, ''), 'website_source_urls': ' '.join(urls[:3]),
           'discrepancy': '; '.join(notes)}
    master.append(row)
    if notes:
        disc.append(row)

os.makedirs(OUT, exist_ok=True)
for name, data in (('master_list.csv', master), ('discrepancies.csv', disc)):
    with open(os.path.join(OUT, name), 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=list(master[0].keys())); w.writeheader(); w.writerows(data)
# website_products.csv: every website observation (product + status + page)
with open(os.path.join(OUT, 'website_products.csv'), 'w', newline='') as fh:
    cols = ['insurer', 'uin', 'name_site', 'status_site', 'irdai_description_line', 'page_type', 'page_url', 'fetched_utc', 'context']
    w = csv.DictWriter(fh, fieldnames=cols, extrasaction='ignore'); w.writeheader()
    for r in W:
        w.writerow({**r, 'insurer': NAME.get(r['uin'][:3], r['slug'])})
summ = collections.OrderedDict()
for r in master:
    s = summ.setdefault(r['insurer'], collections.Counter()); s['rows'] += 1; s[r['website_status']] += 1; s['in_council'] += r['in_council_sep2026'] == 'Y'
cols = ['rows', 'in_council', 'current', 'withdrawn', 'older version withdrawn; current version not found on site', 'listed on site, status not stated', 'page live, not in current plan listings', 'not found on website',
        'not found (website check incomplete)', 'website not readable']
with open(os.path.join(OUT, 'coverage_summary.csv'), 'w', newline='') as fh:
    w = csv.writer(fh); w.writerow(['insurer'] + cols)
    for k, v in summ.items(): w.writerow([k] + [v[c] for c in cols])
print(f"{'insurer':34}" + ''.join(f'{c[:10]:>11}' for c in cols))
for k, v in summ.items(): print(f'{k:34}' + ''.join(f'{v[c]:11}' for c in cols))
print('master rows', len(master), 'discrepancies', len(disc))
