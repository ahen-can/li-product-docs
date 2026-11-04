"""ULIP pilot comparison workbook: the 14 selected products side by side (analysis/ulip_selection.md).
Inputs: features/ulip/<UIN>.json (deep discovery), analysis/v3/new_feature_verdicts.csv, calc/results_ulip.csv,
calc/params/ulip/<UIN>.json. Output: analysis/ulip_comparison_pilot.xlsx (copied to deliverables/06).
Usage: python3 -I analysis/scripts/build_ulip_comparison.py <repo>"""
import csv, json, os, re, sys
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

R = sys.argv[1]
SEL = [('130L100V03', 'Bharti', True), ('130L123V01', 'Bharti', False), ('130L121V01', 'Bharti', False),
       ('111L142V01', 'SBI Life', True), ('111L147V01', 'SBI Life (online)', False), ('101L180V01', 'HDFC Life', True),
       ('101L133V03', 'HDFC Life (online)', False), ('110L179V02', 'Tata AIA', True), ('116L204V01', 'Bajaj Life', True),
       ('104L121V05', 'Axis Max Life', False), ('109L149V01', 'ABSLI', False), ('136L092V02', 'Canara HSBC', False),
       ('135L101V01', 'Ageas Federal', False), ('512L354V01', 'LIC (reference)', False)]
D = {u: json.load(open(os.path.join(R, 'features/ulip', u + '.json'), encoding='utf-8')) for u, _, _ in SEL}
RES = {r['uin']: r for r in csv.DictReader(open(os.path.join(R, 'calc/results_ulip.csv')))}
PAR = {u: json.load(open(os.path.join(R, 'calc/params/ulip', u + '.json'))) for u, _, _ in SEL if os.path.exists(os.path.join(R, 'calc/params/ulip', u + '.json'))}
VER = {}
for r in csv.DictReader(open(os.path.join(R, 'analysis/v3/new_feature_verdicts.csv'), encoding='utf-8')):
    if r['verdict'] == 'Y': VER[(r['group'], r['uin'])] = r
S2NEW = {}
s = open(os.path.join(R, 'analysis/scripts/build_ulip_features.py'), encoding='utf-8').read()
NEW_FEAT = eval(s[s.index('NEW_FEAT = [') + len('NEW_FEAT = '):s.index('\nEXISTING = {')])
name2g = {n: g for g, _, names, _ in NEW_FEAT for n in names}
for u in D:
    for n in D[u].get('new_features_not_in_schema', []):
        g = name2g.get(n['feature'])
        if g: S2NEW[(g, u)] = n

CODE = {'built-in': 'Built-in', 'optional (at inception)': 'Optional', 'optional (during term)': 'Optional', 'rider': 'Rider', 'not offered': 'Not offered',
        'not stated in public documents': 'Not stated', 'n/a': ''}
FILL = {'Built-in': 'C6EFCE', 'Optional': 'DDEBF7', 'Rider': 'FFF2CC', 'Not offered': 'F8CBAD', 'Not stated': 'EDEDED'}
BEST = PatternFill('solid', fgColor='00B050'); BESTF = Font(bold=True, color='FFFFFF')


def flat(v, n=160):
    if v is None: return ''
    if isinstance(v, str): t = v
    elif isinstance(v, (int, float)): t = str(v)
    elif isinstance(v, list): t = '; '.join(flat(x.get('name', '') + (': ' + str(x.get('description') or x.get('rule') or x.get('mechanics') or '') if (x.get('description') or x.get('rule') or x.get('mechanics')) else ''), 999) if isinstance(x, dict) else flat(x, 999) for x in v)
    else: t = '; '.join(f'{a}: {flat(b, 999)}' for a, b in v.items())
    return t if len(t) <= n else t[:n - 1] + '…'


def fld(u, path):
    g, k = path.split('.'); return D[u].get(g, {}).get(k, {}) or {}


def pcts(t, skip=r'discontinu|single'):
    t = re.sub(r'\(allocation rate[^)]*\)', '', t); out = []
    for part in re.split(r';|\n', t):
        if re.search(skip, part, re.I): continue
        out += [float(x) for x in re.findall(r'(\d+(?:\.\d+)?)\s*%', part)]
    return out


ROWS = []   # (section, label, kind, getter) ; getter(u) -> (display, status, numeric, evidence(doc,page,quote))
def deep_row(sec, label, path, kind='text', num=None, best=None):
    def get(u):
        o = fld(u, path); st = CODE.get(o.get('status'), o.get('status') or '')
        val = flat(o.get('value'))
        disp = val if kind == 'text' else (st + (': ' + val if val and st not in ('Not offered', 'Not stated') else '') if st else val)
        n = num(o, u) if num else None
        return disp or st, st, n, (o.get('doc'), o.get('page'), o.get('quote'))
    ROWS.append((sec, label, kind, get, best))

def calc_row(label, col, best, fmt=None):
    def get(u):
        r = RES.get(u)
        if not r: return 'not calculated (mortality rates not published)', '', None, (None, None, None)
        v = float(r[col]); return (fmt(v) if fmt else v), '', v, ('calc/results_ulip.csv', None, r['variant'])
    ROWS.append(('Returns (our calculator)', label, 'num', get, best))

def feat_row(sec, label, g):
    def get(u):
        v = VER.get((g, u)); n = S2NEW.get((g, u))
        if n: return 'Yes: ' + flat(n.get('description'), 140), 'Built-in', 1, (n.get('doc'), n.get('page'), n.get('quote'))
        if v: return 'Yes', 'Built-in', 1, (v['doc'], v['page'], v['snippet'][:300])
        return '', '', 0, (None, None, None)
    ROWS.append((sec, label, 'feat', get, None))

def first_num(t):
    m = re.search(r'(\d[\d,]*(?:\.\d+)?)', t.replace('Rs ', '')); return float(m.group(1).replace(',', '')) if m else None

# Basics
deep_row('Product', 'IRDAI description line', 'product.irdai_description_line')
deep_row('Product', 'Plan options / variants', 'product.variants_or_plan_options')
ROWS.append(('Product', 'Variant used in this comparison', 'text', lambda u: (PAR[u]['variant_used'] if u in PAR else 'Main option (no calculation)', '', None, (None, None, None)), None))
deep_row('Eligibility', 'Entry age (max)', 'eligibility.entry_age_max')
deep_row('Eligibility', 'Policy term options', 'eligibility.policy_term_options')
deep_row('Eligibility', 'Premium payment options', 'eligibility.ppt_options')
deep_row('Eligibility', 'Minimum annual premium', 'eligibility.premium_min_annual', num=lambda o, u: first_num(flat(o.get('value'), 999)), best='min')
deep_row('Eligibility', 'Life cover (sum assured) rule', 'eligibility.sum_assured_rule')
# Charges
deep_row('Charges', 'Premium allocation charge', 'charges.premium_allocation_charge',
         num=lambda o, u: (max(pcts(flat(o.get('value'), 9999))) if pcts(flat(o.get('value'), 9999)) else (0.0 if re.search(r'nil', flat(o.get('value'), 99), re.I) else None)), best='min')
deep_row('Charges', 'Policy administration charge', 'charges.policy_administration_charge')
deep_row('Charges', 'Fund management charge (FMC)', 'charges.fund_management_charge')
deep_row('Charges', 'Mortality charge basis', 'charges.mortality_charge')
ROWS.append(('Charges', 'Mortality rate, age 30 male (per Rs 1,000 sum at risk a year)', 'num', lambda u: ((PAR[u]['mortality_per_1000'].get('30'), '', PAR[u]['mortality_per_1000'].get('30'), ('policy document', None, PAR[u]['mortality_source'])) if u in PAR else ('not published', '', None, (None, None, None))), 'min'))
deep_row('Charges', 'Switching charge', 'charges.switching_charge')
deep_row('Charges', 'Partial withdrawal charge', 'charges.partial_withdrawal_charge')
deep_row('Charges', 'Discontinuance charge', 'charges.discontinuance_charge')
deep_row('Charges', 'Charges returned (summary)', 'charges.any_charge_returned', kind='status')
# Returns
calc_row('Net yield at 8%, excl. GST (as insurers illustrate)', 'net_yield_8_exGST', 'max', lambda v: f'{v:.2f}%')
calc_row('Net yield at 4%, excl. GST', 'net_yield_4_exGST', 'max', lambda v: f'{v:.2f}%')
calc_row('Net yield at 8%, incl. GST (what the customer gets)', 'net_yield_8_inclGST', 'max', lambda v: f'{v:.2f}%')
calc_row('Reduction in yield at 8%, excl. GST', 'riy_8_exGST', 'min', lambda v: f'{v:.2f}%')
calc_row('Maturity value at 8%, incl. GST (Rs)', 'maturity_8_inclGST', None, lambda v: f'{v:,.0f}')
ROWS.append(('Returns (our calculator)', 'Profile used', 'text', lambda u: ((f"male {RES[u]['age']}, Rs {int(RES[u]['annual_premium']):,} a year, pay {RES[u]['ppt']} yrs, term {RES[u]['pt']} yrs" + (f" ({PAR[u].get('note')})" if PAR[u].get('note') else '')), '', None, (None, None, None)) if u in RES else ('', '', None, (None, None, None)), None))
ROWS.append(('Returns (our calculator)', 'Checked against insurer figures?', 'text', lambda u: ((RES[u]['check_status'] if u in RES else ''), '', None, (None, None, None)), None))
# Additions
deep_row('Additions and refunds', 'Loyalty additions', 'benefits.loyalty_additions', kind='status')
deep_row('Additions and refunds', 'Wealth boosters / guaranteed additions', 'benefits.wealth_boosters_or_guaranteed_additions', kind='status')
deep_row('Additions and refunds', 'Return of mortality charges', 'benefits.return_of_mortality_charges', kind='status')
deep_row('Additions and refunds', 'Return of allocation charges', 'benefits.return_of_premium_allocation_charges', kind='status')
deep_row('Additions and refunds', 'Return of admin charges', 'benefits.return_of_policy_admin_charges', kind='status')
deep_row('Additions and refunds', 'Other additions', 'benefits.other_additions', kind='status')
# Flexibility
for lab, pth in [('Fund switching', 'flexibility.fund_switching'), ('Premium redirection', 'flexibility.premium_redirection'), ('Partial withdrawals', 'flexibility.partial_withdrawals'),
                 ('Systematic withdrawal', 'flexibility.systematic_withdrawal_plan'), ('Top-up premiums', 'flexibility.top_up_premiums'), ('Settlement option', 'flexibility.settlement_option'),
                 ('Automatic fund strategies', 'flexibility.auto_portfolio_strategies'), ('Increase / decrease cover', 'flexibility.increase_decrease_cover'), ('Policy loan', 'flexibility.policy_loan')]:
    deep_row('Flexibility', lab, pth, kind='status')
# Protection
for lab, pth in [('Waiver of premium (in-built)', 'protection_add_ons.waiver_of_premium_inbuilt'), ('Critical illness', 'protection_add_ons.critical_illness'), ('Accidental death', 'protection_add_ons.accidental_death'),
                 ('Spouse or child cover', 'protection_add_ons.spouse_or_child_cover'), ('Riders available', 'protection_add_ons.riders_available')]:
    deep_row('Protection', lab, pth, kind='status')
# Funds
deep_row('Funds', 'Number of funds', 'funds.fund_count', num=lambda o, u: first_num(flat(o.get('value'), 99)), best='max')
deep_row('Funds', 'Index or thematic funds', 'funds.index_or_thematic_funds')
deep_row('Surrender', 'Lock-in (years)', 'surrender_revival.lock_in_years')
# New features
for g, label, _, _ in NEW_FEAT:
    feat_row('Features found in policy documents', label, g)

# ---- write ----
wb = Workbook(); wb.remove(wb.active)
HEAD = PatternFill('solid', fgColor='1F3864'); HF = Font(bold=True, color='FFFFFF'); SECF = PatternFill('solid', fgColor='D9E1F2')
BH = PatternFill('solid', fgColor='FCE4D6'); WR = Alignment(wrap_text=True, vertical='top'); thin = Side(style='thin', color='D0D0D0')
ws = wb.create_sheet('Comparison')
ws.column_dimensions['A'].width = 22; ws.column_dimensions['B'].width = 34
hdr = ['Section', 'Row'] + [f"{ins}\n{D[u]['product']['product_name']['value'].replace('Bharti AXA Life ', '').replace('Life Insurance ', '')}\n{u}" + ('\n[deck]' if deck else '') for u, ins, deck in SEL]
for j, h in enumerate(hdr, 1):
    c = ws.cell(1, j, h); c.fill = HEAD; c.font = HF; c.alignment = Alignment(wrap_text=True, vertical='center', horizontal='center')
    if j > 2: ws.column_dimensions[get_column_letter(j)].width = 24
ws.row_dimensions[1].height = 78
EV = []; r = 2; prev = None
for sec, label, kind, get, best in ROWS:
    if sec != prev:
        ws.cell(r, 1, sec).font = Font(bold=True);
        for j in range(1, len(hdr) + 1): ws.cell(r, j).fill = SECF
        r += 1; prev = sec
    ws.cell(r, 1, sec).font = Font(color='808080', size=9); ws.cell(r, 2, label).alignment = WR
    vals = {}
    for j, (u, ins, deck) in enumerate(SEL, 3):
        disp, st, n, ev = get(u)
        c = ws.cell(r, j, disp if not isinstance(disp, float) else disp); c.alignment = WR; c.border = Border(bottom=thin)
        if st in FILL and kind in ('status', 'feat'): c.fill = PatternFill('solid', fgColor=FILL[st])
        if u.startswith('130') and not c.fill.fgColor.rgb not in (None, '00000000'): pass
        if n is not None: vals[j] = n
        if ev and ev[2]: EV.append([ins, D[u]['product']['product_name']['value'], u, sec, label, str(disp)[:300], ev[0], ev[1], str(ev[2])[:500]])
    if best and vals:
        target = (min if best == 'min' else max)(vals.values())
        for j, v in vals.items():
            if v == target: ws.cell(r, j).fill = BEST; ws.cell(r, j).font = BESTF
    if kind == 'feat':
        n_has = sum(1 for j, v in vals.items() if v)
        ws.cell(r, 2, f'{label}  ({n_has} of {len(SEL)})')
    r += 1
for j, (u, ins, deck) in enumerate(SEL, 3):
    if u.startswith('130'):
        ws.cell(1, j).fill = PatternFill('solid', fgColor='C00000')
ws.freeze_panes = 'C2'

# Returns tab with chart data
rt = wb.create_sheet('Returns')
rh = ['Insurer', 'Product', 'UIN', 'Pay / term', 'Annual premium', 'Net yield 4% excl GST', 'Net yield 8% excl GST', 'Reduction in yield 8% excl GST', 'Net yield 4% incl GST', 'Net yield 8% incl GST',
      'Maturity 8% incl GST', 'Allocation charges', 'Admin charges', 'Mortality charges', 'FMC', 'Additions and refunds', 'Checked?', 'Note']
for j, h in enumerate(rh, 1):
    c = rt.cell(1, j, h); c.fill = HEAD; c.font = HF; c.alignment = WR
i = 2
for u, ins, deck in sorted(SEL, key=lambda x: -float(RES[x[0]]['net_yield_8_exGST']) if x[0] in RES else 99):
    if u not in RES: continue
    x = RES[u]
    row = [ins, x['product'], u, f"{x['ppt']} / {x['pt']}", int(x['annual_premium']), float(x['net_yield_4_exGST']) / 100, float(x['net_yield_8_exGST']) / 100, float(x['riy_8_exGST']) / 100,
           float(x['net_yield_4_inclGST']) / 100, float(x['net_yield_8_inclGST']) / 100, int(x['maturity_8_inclGST']), int(x['alloc_charges']), int(x['admin_charges']), int(x['mortality_charges']), int(x['fmc']),
           int(x['additions_and_refunds']), x['check_status'], x['note']]
    for j, v in enumerate(row, 1):
        c = rt.cell(i, j, v)
        if j in (6, 7, 8, 9, 10): c.number_format = '0.00%'
        if j >= 11 and j <= 16: c.number_format = '#,##0'
        if u.startswith('130'): c.fill = BH
    i += 1
rt.cell(i + 1, 1, 'Tata AIA Smart Sampoorna Raksha Supreme is not calculated: Tata does not publish its mortality rates. Charges are excl. GST and summed over the term at 8% gross. Profile: male 30, Rs 1 lakh a year, 10-year pay, 20-year term, cover 10x, equity fund, unless the Pay / term column says otherwise.').alignment = WR
for j, w in enumerate([16, 34, 12, 10, 12, 10, 10, 10, 10, 10, 14, 12, 12, 12, 12, 14, 30, 50], 1): rt.column_dimensions[get_column_letter(j)].width = w

ev = wb.create_sheet('Evidence')
eh = ['Insurer', 'Product', 'UIN', 'Section', 'Row', 'Value shown', 'Document', 'Page', 'Quote or source']
for j, h in enumerate(eh, 1):
    c = ev.cell(1, j, h); c.fill = HEAD; c.font = HF
for i, row in enumerate(EV, 2):
    for j, v in enumerate(row, 1): ev.cell(i, j, re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', v) if isinstance(v, str) else v)
for j, w in enumerate([16, 30, 12, 20, 30, 40, 18, 6, 80], 1): ev.column_dimensions[get_column_letter(j)].width = w

rd = wb.create_sheet('README', 0); rd.column_dimensions['A'].width = 140
L = ['ULIP pilot comparison: Bharti vs peers (4 Nov 2026)',
     '14 ULIPs side by side: Bharti\'s three (Wealth Pro, Growth Shield Plus, Wealth Maximizer), one comparable product from each of SBI, HDFC, Tata AIA, Bajaj, Axis Max, ABSLI, Canara HSBC and Ageas Federal, two online benchmarks (SBI eWealth Plus, HDFC Click 2 Wealth) and LIC as a reference. The 5 marked [deck] are in the presentation. Why each was chosen: analysis/ulip_selection.md. ICICI is not included yet (documents pending).',
     'HOW TO READ:',
     'Comparison tab: one column per product, Bharti first (red headers). Cell colours for features: green Built-in, blue Optional, yellow Rider, orange Not offered, grey Not stated in public documents. Bright green with white text = best in class on that row (lowest charge, highest return, most funds).',
     'Returns tab: our calculator\'s results for the same customer (male 30, Rs 1 lakh a year, 10 years of premiums, 20-year term, cover 10x, equity fund), at the regulator\'s 4% and 8% gross returns, excluding GST (how insurers illustrate) and including GST (what the customer gets). Five products are checked against insurer quotes or illustrations within 0.3%; the others use the same method and are marked "not yet checked".',
     'Evidence tab: the document, page and quote behind every value.',
     'SOURCES: policy documents and brochures from each insurer\'s website (features/ulip/<UIN>.json, read field by field), new features checked by hand (analysis/v3/new_feature_verdicts.csv), calculator (calc/). Rebuild: python3 -I analysis/scripts/build_ulip_comparison.py <repo>.',
     'LIMITS: product-level sales are not public for peers, so "comparable product" means the closest design to Bharti\'s best sellers, not the peer\'s best seller. Growth Shield Plus needs a 30-year term with 10-year pay, and LIC Index Plus is regular pay only, so their yields are on a different profile (shown in the Returns tab). Tata does not publish mortality rates, so its returns cannot be calculated.']
for i, l in enumerate(L, 1):
    c = rd.cell(i, 1, l); c.alignment = WR
    if i == 1: c.font = Font(bold=True, size=14)
    elif l.endswith(':'): c.font = Font(bold=True)
out = os.path.join(R, 'analysis/ulip_comparison_pilot.xlsx'); wb.save(out)
print('rows', len(ROWS), 'evidence', len(EV))
