"""Merge Council (Sep-2026) and IRDAI (Dec-2025) lists into master_list v1.
Usage: python3 -I build_master.py council_rows.csv irdai_rows.csv out.csv"""
import csv, sys, re, collections

INS = {  # UIN prefix -> insurer short name (current names)
    '101': 'HDFC Life', '104': 'Axis Max Life', '105': 'ICICI Prudential Life', '107': 'Kotak Mahindra Life',
    '109': 'Aditya Birla Sun Life', '110': 'Tata AIA Life', '111': 'SBI Life', '116': 'Bajaj Life', '117': 'PNB MetLife',
    '121': 'IndusInd Nippon Life', '122': 'Aviva Life', '127': 'Sahara Life', '128': 'Shriram Life', '130': 'Bharti Life',
    '133': 'Generali Central Life', '135': 'Ageas Federal Life', '136': 'Canara HSBC Life', '138': 'Bandhan Life',
    '140': 'Pramerica Life', '142': 'Star Union Dai-ichi Life', '143': 'IndiaFirst Life', '147': 'Edelweiss Life',
    '114': 'Exide Life (merged into HDFC Life)', '163': 'CreditAccess Life', '164': 'Acko Life', '165': 'Go Digit Life',
    '512': 'LIC'}

C = list(csv.DictReader(open(sys.argv[1])))
I = list(csv.DictReader(open(sys.argv[2])))

def code(u): return u[:7]           # insurer + type + product number (version-free)
def ver(u): return int(u[-2:])

# IRDAI: per product code, all versions; active = latest in-operation version
irdai = collections.defaultdict(list)
for r in I:
    if r['section'] == 'Products' and r['uin'][3] in 'NL':
        irdai[code(r['uin'])].append(r)
council = {}
for r in C:
    if r['section'] == 'Products' and r['uin'][3] in 'NL':
        council[code(r['uin'])] = r

def classify(linked, lob, cat, name):
    """Preliminary market category from UIN + Council category + name. Confirmed later from the brochure."""
    c = (cat or '').lower(); n = (name or '').lower()
    if lob == 'Group' or re.search(r'\bgroup\b', n):
        return 'OUT: group', 'high'
    if 'health' in c or re.search(r'cancer|heart|health|critical illness|\bci\b|diabet|cardiac', n) and 'ulip' not in c:
        return 'OUT: health', 'high' if 'health' in c else 'low (name only)'
    if 'accident' in c or 'micro' in c or re.search(r'micro|sukshm|sookshma', n):
        return 'OUT: accident/micro', 'high'
    if linked == 'L':
        return 'ULIP', 'high'
    if re.search(r'term|protection|credit life', c) and not re.search(r'endow|savings|annuity|pension', c):
        return 'Protection', 'high'
    if not c and re.search(r'\bterm\b|protect|loan|credit|saral jeevan bima|\bshield\b', n) and not re.search(r'saving|bachat|income|wealth|pension|annuity', n):
        return 'Protection', 'low (name only)'
    if re.search(r'annuity|pension', c):
        return 'Annuity', 'high'
    if not c and re.search(r'annuity|pension|retire', n):
        return 'Annuity', 'low (name only)'
    if re.search(r'non[- ]?par', c):
        return 'Non-Par Savings', 'high'
    if re.search(r'\(par\)|par whole|participating', c) and 'non' not in c:
        return 'Par', 'high'
    return 'Savings (Par / Non-Par to confirm)', 'low'

rows = []
for k in sorted(set(council) | set(irdai), key=lambda x: (x[:3], x)):
    cr = council.get(k)
    vers = sorted(irdai.get(k, []), key=lambda r: ver(r['uin']))
    active = [v for v in vers if v['status'] == 'in operation']
    first_open = vers[0]['opened'] if vers else ''
    latest = vers[-1] if vers else None
    in_c = cr is not None
    in_i_active = bool(active)
    if not in_c and not in_i_active:
        continue
    if k[:3] == '114':   # Exide Life merged into HDFC Life (2023); Council lists no Exide products
        continue  # withdrawn in IRDAI and absent from Council -> not current
    uin = cr['uin'] if cr else active[-1]['uin']
    name = cr['name'] if cr else active[-1]['name_en']
    lob = cr['lob'] if cr else ''
    cat = cr['category'] if cr else ''
    mc, conf = classify(uin[3], lob or ('Group' if re.search(r'\bgroup\b', name, re.I) else 'Individual?'), cat, name)
    note = []
    if cr and latest and ver(cr['uin']) != ver(latest['uin']):
        note.append(f"IRDAI latest version {latest['uin']}")
    if cr and vers and not active:
        note.append('IRDAI list shows withdrawn (Dec-2025) but Council lists in-force (Sep-2026)')
    if not cr:
        note.append('Not in Council Sep-2026 list: check insurer website (may be withdrawn, group, or Council gap)')
    rows.append({
        'insurer_code': k[:3], 'insurer': INS.get(k[:3], k[:3]), 'product_name': name, 'uin': uin, 'product_code': k,
        'linked_flag': uin[3], 'line_of_business': lob or ('Group?' if re.search(r'\bgroup\b', name, re.I) else 'Individual?'),
        'council_category': cat, 'market_category_prelim': mc, 'prelim_confidence': conf,
        'par_flag': '', 'irdai_description_line': '', 'market_category_final': '', 'pd_category': '',
        'first_launch_irdai': first_open, 'current_version_opened_irdai': (active[-1]['opened'] if active else ''),
        'versions_in_irdai': len(vers), 'in_council_sep2026': 'Y' if in_c else 'N',
        'in_irdai_active_dec2025': 'Y' if in_i_active else ('withdrawn' if vers else 'not listed'),
        'notes': '; '.join(note)})

with open(sys.argv[3], 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

ind = [r for r in rows if not r['market_category_prelim'].startswith('OUT')]
print('total current N/L product codes:', len(rows), '| in scope (prelim):', len(ind))
print(collections.Counter(r['market_category_prelim'] for r in rows))
print('source overlap (in scope):', collections.Counter((r['in_council_sep2026'], r['in_irdai_active_dec2025']) for r in ind))
t = collections.defaultdict(collections.Counter)
for r in ind: t[r['insurer']][r['market_category_prelim'][:12]] += 1
for k in sorted(t, key=lambda k: -sum(t[k].values())): print(f'{k:28} {sum(t[k].values()):3}', dict(t[k]))
