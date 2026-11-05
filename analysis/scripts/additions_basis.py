"""Rule 2 (option b, user 5 Nov 2026): classify each deep ULIP's additions by what they are a percentage of.
  pct_of_premium: the addition is a % of premium (annualised, single, instalment, first-year) or a multiple of AP.
                  The rupee amount is known at the start.
  pct_of_fund:    the addition is a % of fund value (current or an average). It moves with the market.
Charge refunds (mortality, allocation, admin, FMC) are not additions here; they have their own rows.
Fund-floor top-ups (Tata and Axis "Cover Continuance Booster") are not counted: they pay only when the fund falls low.
Reads benefits.loyalty_additions, wealth_boosters_or_guaranteed_additions and other_additions in features/ulip/*.json,
then applies the reviewed exclusions and additions below.
Output: analysis/v4/additions_basis.csv
Usage: python3 -I analysis/scripts/additions_basis.py <repo_dir>"""
import csv, glob, json, os, re, sys

R = sys.argv[1]
YESST = ('built-in', 'optional (at inception)', 'optional (during term)')
PREM = re.compile(r'(%|percent|per cent|\bx|times)\s*(of\s*)?(the\s*)?(one\s*)?(\(?annuali[sz]ed|annual|single|installment|instalment|regular|first[- ]year|modal|total)?\s*premium'
                  r'|\b(of|x)\s*(AP|SP)\b|\d\s*x\s*AP\b|allocation rate of 1\d\d|% of (the )?(single/annuali[sz]ed|annuali[sz]ed/single) premium', re.I)
FUND = re.compile(r'fund value|average fund|fund average|\bFV\b|of (the )?fund\b|premium fund value', re.I)
NOT_ADD = re.compile(r'cover continuance booster|tops? (the fund )?up|^cap\b|cap: |capped|settlement instalments|vesting benefit|guaranteed maturity benefit|periodic cash|return of|refund', re.I)
CONDITION = [(r'women|female|smart lady', 'women only'), (r'online|digital|direct', 'online or direct only'), (r'existing customer|family', 'existing customers or family'),
             (r'auto ?debit|ECS|auto pay', 'auto-pay only'), (r'staff|employee', 'staff only'), (r'band|lakh|AP of Rs|AP >|AP <', 'by premium band'),
             (r'single', 'single pay'), (r'DBM|SA > ?\d+x|multiple', 'high cover only')]
# Reviewed by S1 on 5 Nov 2026 (segment text -> keep / drop)
DROP = {('130L128V01', 'Wealth Affinity Plan: Milestone Benefit')}         # matched "AP < Rs 5 lakh" but the addition is a % of average fund
ADD = {'111L142V01': ('pct_of_premium', 'Guaranteed Additions as % of AP or SP at the end of years 10, 15, 20, 25, 30 (limited pay 10: 10/15/25/35/40%; regular: 15/15/30/40/50%); plus Guaranteed Addition on Maturity 0/5/10% of AP by premium band',
                      'Policy Document', 27, 'We will allot Guaranteed Additions as a percentage of the Annualized Premium or Single Premium in accordance with the table below')}


def segs(v, pre=''):
    if v is None: return []
    if isinstance(v, (str, int, float)): return [pre + str(v)]
    if isinstance(v, list): return [s for x in v for s in segs(x, pre)]
    return [s for k, x in v.items() for s in segs(x, pre + str(k) + ': ')]


out = []
for f in sorted(glob.glob(os.path.join(R, 'features/ulip/*.json'))):
    d = json.load(open(f, encoding='utf-8')); u = os.path.basename(f)[:-5]
    found = {'pct_of_premium': [], 'pct_of_fund': []}; anyadd = False; ev = {}
    for k in ['loyalty_additions', 'wealth_boosters_or_guaranteed_additions', 'other_additions']:
        o = d['benefits'].get(k, {}) or {}
        if o.get('status') not in YESST: continue
        for s in segs(o.get('value')):
            if NOT_ADD.search(s) or any(u == a and s.startswith(b) for a, b in DROP): continue
            if not re.search(r'\d', s) and not re.search(r'basis|fund value|premium', s, re.I): continue
            anyadd = True
            for key, rx in (('pct_of_premium', PREM), ('pct_of_fund', FUND)):
                if rx.search(s):
                    found[key].append(s); ev.setdefault(key, (o.get('doc'), o.get('page'), o.get('quote')))
    row = {'uin': u, 'product': d['product']['product_name']['value']}
    for key in ('pct_of_premium', 'pct_of_fund'):
        if u in ADD and ADD[u][0] == key:
            a = ADD[u]; row[key] = 'B'; row[key + '_detail'] = a[1]; row[key + '_conditions'] = ''
            row[key + '_doc'], row[key + '_page'], row[key + '_quote'] = a[2], a[3], a[4]; row[key + '_method'] = 'read by S1'
            continue
        segs_ = found[key]
        if segs_:
            txt = ' | '.join(segs_)
            # Decision 35: a condition goes on the part it applies to; "only for" on the whole row only if every part has it
            per = []
            for s_ in segs_:
                labs = sorted({lab for rx, lab in CONDITION if lab != 'single pay' and re.search(rx, s_, re.I)})
                per.append(labs)
            conds = set(per[0]).intersection(*per[1:]) if per else set()
            if all(re.search(r'\bsingle\b|\bSP\b', s) and not re.search(r'annual|regular|limited|instalment|installment|\bAP\b', s, re.I) for s in segs_):
                conds.add('single pay only')
            conds = sorted(conds)
            txt = ' | '.join(s_ + (f' [only for: {", ".join(l)}]' if l and set(l) - set(conds) else '') for s_, l in zip(segs_, per))
            row[key] = 'B'; row[key + '_detail'] = txt[:600]; row[key + '_conditions'] = '; '.join(conds)
            doc, pg, q = ev[key]; row[key + '_doc'], row[key + '_page'], row[key + '_quote'] = doc, pg, (q or '')[:400]
            row[key + '_method'] = 'deep value text'
        else:
            row[key] = '?' if anyadd and not (found['pct_of_premium'] or found['pct_of_fund']) else ''
            for x in ('_detail', '_conditions', '_doc', '_page', '_quote'): row[key + x] = ''
            row[key + '_method'] = 'additions found, basis not read' if row[key] == '?' else 'no such addition in deep data'
    out.append(row)
p = os.path.join(R, 'analysis/v4/additions_basis.csv')
os.makedirs(os.path.dirname(p), exist_ok=True)
with open(p, 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
print(len(out), 'products; % of premium:', sum(r['pct_of_premium'] == 'B' for r in out), '; % of fund:', sum(r['pct_of_fund'] == 'B' for r in out),
      '; basis unread:', [r['uin'] for r in out if r['pct_of_premium'] == '?'])
for r in out:
    if r['pct_of_premium'] == 'B': print(' P', r['uin'], r['product'][:35], '|', r['pct_of_premium_conditions'], '|', r['pct_of_premium_detail'][:90])
