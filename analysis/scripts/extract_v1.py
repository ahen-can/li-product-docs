"""Feature extraction v1 from brochure text (light-discovery output).

Inputs : <branch>/results/light_discovery_results.csv, <branch>/index.csv, <branch>/text/..., <main>/master_list.csv
Outputs: analysis/product_features_v1.csv  (one row per product: classification + numeric fields + feature flags)
         analysis/feature_evidence_v1.csv  (one row per product x feature found: value, evidence snippet, page)
         analysis/brochures_used_log.csv   (iteration log)
Rules  : category comes ONLY from the IRDAI description line (fallback: Council category label, flagged) + UIN linked flag.
         Feature flags mean "the brochure describes X" (keyword + context), evidence kept for every hit.
Usage  : python3 -I extract_v1.py <branch_dir> <main_dir>
"""
import csv, re, sys, os, hashlib, datetime, collections

B, M = sys.argv[1], sys.argv[2]
OUT = os.path.join(M, 'analysis')
res = [r for r in csv.DictReader(open(os.path.join(B, 'results/light_discovery_results.csv'))) if r['status'] == 'ok']
idx = {(r['uin'], r['doc_type']): r for r in csv.DictReader(open(os.path.join(B, 'index.csv')))}
mast = {r['row_id']: r for r in csv.DictReader(open(os.path.join(M, 'master_list.csv')))}

# ---------------------------------------------------------------- classification
def norm_desc(d):
    d = d.lower().replace('–', '-').replace('ti', 'ti')
    d = re.sub(r'par\s*cipa\s*ng', 'participating', d)            # ligature loss "non-par cipa ng"
    return d

def classify(desc, uin, council_cat):
    d = norm_desc(desc)
    linked = uin[3] == 'L' if uin else bool(re.search(r'unit[\s-]*linked|(?<!non)[\s,]linked', d))
    nonpar = bool(re.search(r'non[\s-]*(participating|par\b)|without profit', d))
    par = not nonpar and bool(re.search(r'participating|\bpar\b|with profit', d))
    has = lambda *w: any(x in d for x in w)
    flags = []
    if has('micro'): return dict(market_category='OUT: micro', pd_category='', sub_basis='description line', par_flag='Non-Par' if nonpar else ('Par' if par else ''), flags='micro per description line')
    if has('health') and not has('savings', 'pure risk'): return dict(market_category='OUT: health', pd_category='', sub_basis='description line', par_flag='Non-Par', flags='health per description line')
    pension = has('pension'); annuity = has('annuity')
    if linked:
        mc = 'ULIP'; pd = 'Pension & Annuity' if pension else 'Linked'
    elif par:
        mc = 'Par'; pd = 'Pension & Annuity' if (pension or annuity) else 'Par Life'
    elif nonpar or not d:
        if has('pure risk', 'term', 'protection') and not has('annuity', 'pension'):
            mc = 'Protection'; pd = 'Non-Par Life'
        elif annuity or pension or has('immediate', 'deferred'):
            mc = 'Annuity'; pd = 'Pension & Annuity'
        elif has('savings', 'endowment', 'whole life', 'money back'):
            mc = 'Non-Par Savings'; pd = 'Non-Par Life'
        else:
            mc = ''; pd = ''
    else:
        mc = ''; pd = ''
    basis = 'description line'
    if not mc:   # fallback on the Council's own category label
        c = (council_cat or '').lower()
        basis = 'Council category (description line has no plan type)'
        if 'ulip' in c or 'unit' in c: mc, pd = 'ULIP', 'Linked'
        elif re.search(r'term|protection', c): mc, pd = 'Protection', 'Non-Par Life'
        elif re.search(r'annuity|pension', c): mc, pd = ('Par', 'Pension & Annuity') if par else ('Annuity', 'Pension & Annuity')
        elif c: mc, pd = ('Par', 'Par Life') if par else ('Non-Par Savings', 'Non-Par Life')
        else: basis = 'UNRESOLVED'; flags.append('no plan type in description line and no Council category')
    return dict(market_category=mc, pd_category=pd, sub_basis=basis, par_flag='Par' if par else ('Non-Par' if nonpar else ''), flags='; '.join(flags))

# ---------------------------------------------------------------- text helpers
def pages_of(path):
    t = open(path, errors='ignore').read()
    return t.split('\f')

def find(pgs, rx, flags=re.I, ctx=110, exclude=None):
    """first match -> (page_no, snippet)"""
    R = re.compile(rx, flags)
    for i, p in enumerate(pgs, 1):
        flat = re.sub(r'[ \t]+', ' ', p)
        for m in R.finditer(flat):
            s = flat[max(0, m.start() - ctx):m.end() + ctx].replace('\n', ' ')
            if exclude and re.search(exclude, s, re.I):
                continue
            if re.search(r'free[- ]?look|nominat|section 3[89]|section 45|ombudsman|grievance|assignment', s, re.I):
                continue
            return i, re.sub(r'\s+', ' ', s).strip()
    return None

def count_matches(pgs, rx):
    return len(re.findall(rx, '\n'.join(pgs), re.I))

def section(pgs, start_rx, n_lines=140):
    """lines following the first eligibility / plan-at-a-glance heading"""
    allt = '\n'.join(pgs); lines = allt.split('\n')
    for i, l in enumerate(lines):
        if re.search(start_rx, l, re.I):
            return lines[i:i + n_lines]
    return []

AGE = r'(\d{1,3})\s*(days?|months?|years?|yrs?)?'
def ages_in(line):
    out = []
    for m in re.finditer(r'(\d{1,3})\s*(days?|months?)?', line):
        v = int(m.group(1)); unit = (m.group(2) or '').lower()
        if unit.startswith('day'): out.append(round(v / 365, 2))
        elif unit.startswith('month'): out.append(round(v / 12, 2))
        elif 0 <= v <= 100: out.append(v)
    return out

def numeric_fields(pgs):
    """Only label-adjacent numbers (same line, <= 70 chars after the label). Grid tables are left blank on purpose."""
    out = {}
    lines = [re.sub(r'\s+', ' ', l).strip() for l in '\n'.join(pgs).split('\n')]
    def first(label_rx, num_rx, conv, lo, hi):
        for l in lines:
            m = re.search(label_rx + r'(?P<gap>[^0-9\n]{0,70}?)' + num_rx + r'(?!\s*[:)\]]\s*\d)(?!\s*:)', l, re.I)
            if m and not re.search(r'variant|option|ppt|premium payment|for\b|band|plan\b', m.group('gap'), re.I):
                v = conv(m)
                if v is not None and lo <= v <= hi:
                    return v, l[:200]
        return None
    agec = lambda m: (round(int(m.group('n')) / 365, 2) if (m.group('u') or '').lower().startswith('day') else
                      round(int(m.group('n')) / 12, 2) if (m.group('u') or '').lower().startswith('month') else int(m.group('n')))
    AGEN = r'(?P<n>\d{1,3})\s*(?P<u>days?|months?|years?|yrs?)?'
    spec = [('entry_age_min', r'(minimum|min\.?)\s*(age at entry|entry age|age)', AGEN, agec, 0, 70),
            ('entry_age_max', r'(maximum|max\.?)\s*(age at entry|entry age|age)(?! at maturity)(?!\s*at\s*maturity)', AGEN, agec, 1, 90),
            ('maturity_age_max', r'(maximum|max\.?)\s*(age at maturity|maturity age)', AGEN, agec, 18, 100),
            ('policy_term_min', r'(minimum|min\.?)\s*policy term', AGEN, agec, 1, 100),
            ('policy_term_max', r'(maximum|max\.?)\s*policy term', AGEN, agec, 1, 100),
            ('min_premium', r'minimum\s*(annual(ised|ized)?\s*|annual\s*|single\s*|basic\s*)?premium', r'(?:rs\.?|₹|inr|`)?\s*(?P<n>\d{1,3}(?:,\d{2,3})+|\d{4,})',
             lambda m: int(m.group('n').replace(',', '')), 500, 10**9),
            ('min_sum_assured', r'minimum\s*(basic\s*)?sum assured', r'(?:rs\.?|₹|inr|`)?\s*(?P<n>\d{1,3}(?:,\d{2,3})+|\d{4,})',
             lambda m: int(m.group('n').replace(',', '')), 1000, 10**10)]
    for key, lab, num, conv, lo, hi in spec:
        g = first(lab, num, conv, lo, hi)
        if g:
            out[key], out[key + '_evidence'] = g
    return out

# ---------------------------------------------------------------- feature catalogue
# (feature_key, applies_to categories or 'ALL', regex, optional exclude-context regex, definition)
F = [
 # premium payment
 ('ppt_single_pay', 'ALL', r'single (premium|pay)\b', None, 'Single premium payment option'),
 ('ppt_limited_pay', 'ALL', r'limited (premium|pay)', None, 'Limited premium payment option'),
 ('ppt_regular_pay', 'ALL', r'regular (premium|pay)', None, 'Regular premium payment option'),
 ('pay_till_60', 'Protection', r'pay till (age )?60|premium payment.{0,20}till age 60', None, 'Pay till age 60 option'),
 ('monthly_mode', 'ALL', r'\bmonthly\b', r'monthly income|monthly annuity|monthly payout', 'Monthly premium mode available'),
 # protection
 ('whole_life_cover', 'Protection', r'whole life|up ?to (age )?(99|100)|till (age )?(99|100)', None, 'Cover to age 99/100'),
 ('return_of_premium', 'Protection', r'return of (total )?premium|\bROP\b|premiums? (paid )?(back|returned) on (survival|maturity)', None, 'Return of premium on survival'),
 ('zero_cost_exit', 'Protection', r'zero cost|special exit|smart exit|exit option|early exit', None, 'Zero-cost / special exit (premiums back mid-term)'),
 ('increasing_cover', 'Protection', r'increasing (sum assured|cover|life cover)', None, 'Increasing cover option'),
 ('decreasing_cover', 'Protection', r'decreasing (sum assured|cover)|reducing cover', None, 'Decreasing / reducing cover option'),
 ('life_stage_increase', 'ALL', r'(increase|enhance)\w*.{0,50}(cover|sum assured).{0,80}(marriage|birth|child|home loan)|life ?stage (event|benefit|option|cover)|(marriage|childbirth|birth of).{0,60}(increase|enhance)', None, 'Increase cover at life events'),
 ('top_up_cover', 'Protection', r'top[- ]?up (sum assured|cover)', None, 'Top-up of cover'),
 ('spouse_joint_cover', 'Protection', r'(cover|insure|protect)\w*.{0,40}(spouse|joint life)|(spouse|joint life).{0,40}(cover|protection)', r'nominat',  'Spouse / joint life cover'),
 ('terminal_illness', 'ALL', r'terminal illness', None, 'Terminal illness benefit'),
 ('critical_illness_inbuilt_or_option', 'ALL', r'critical illness', None, 'Critical illness (inbuilt, option or rider)'),
 ('accidental_death_extra', 'ALL', r'accident(al)? death', None, 'Accidental death benefit (option or rider)'),
 ('disability_benefit', 'ALL', r'disabilit', None, 'Disability benefit / waiver'),
 ('waiver_of_premium', 'ALL', r'waiver of premium|premium waiver|wop\b', None, 'Waiver of premium (inbuilt/option/rider)'),
 ('death_benefit_as_income', 'ALL', r'(monthly|regular|annual) income.{0,40}(nominee|family|death)|death benefit.{0,60}(instal|income)', None, 'Death benefit payable as income / instalments'),
 ('women_specific_rates', 'Protection', r'(lower|discount|special|preferential).{0,30}(women|female)|(women|female).{0,30}(discount|lower premium|rates)', None, 'Discount / special rates for women'),
 ('non_smoker_rates', 'Protection', r'non[- ]?smoker|tobacco', None, 'Smoker / non-smoker differentiated rates'),
 ('online_discount', 'ALL', r'online.{0,30}discount|discount.{0,30}online', None, 'Online purchase discount'),
 ('high_sa_rebate', 'ALL', r'high sum assured (rebate|discount)|large sum assured', None, 'High sum-assured rebate'),
 ('salaried_discount', 'ALL', r'salaried', None, 'Salaried discount / variant'),
 ('free_health_checkup_wellness', 'ALL', r'health check|wellness|second (medical )?opinion', None, 'Health check-up / wellness services'),
 # savings (par + non-par)
 ('guaranteed_income', 'Non-Par Savings,Par', r'guaranteed (monthly |regular |annual )?income', None, 'Guaranteed income payouts'),
 ('lump_sum_maturity', 'Non-Par Savings,Par', r'lump ?sum.{0,60}(maturity|on survival|survival)|(maturity|survival) benefit.{0,80}lump ?sum', r'death benefit.{0,40}lump|nominee',  'Lump-sum maturity option'),
 ('income_plus_lumpsum', 'Non-Par Savings,Par', r'income.{0,40}(and|plus|\+).{0,20}lump ?sum|lump ?sum.{0,40}(and|plus|\+).{0,20}income', None, 'Income + lump-sum combination'),
 ('whole_life_income', 'Non-Par Savings,Par', r'(till|up ?to) (age )?(99|100)|whole life', None, 'Income/cover to age 99/100 (whole-life)'),
 ('immediate_income', 'Non-Par Savings,Par', r'(income|payout)s? (start|begin|from).{0,25}(1st|first|2nd|second) (policy )?year|immediate income|early income', None, 'Income starting from year 1-2'),
 ('deferment_choice', 'Non-Par Savings,Par', r'deferment period|deferred period', None, 'Choice of deferment period'),
 ('return_of_premiums_at_end', 'Non-Par Savings,Par', r'(return|refund) of (total |100% of )?premiums? (paid|payable)|premiums? (paid )?(returned|back) at (the end|maturity)', r'proportionate risk|objection|medical exam|stamp duty|death benefit|suicide|restricted',  'Premiums returned at end of income period'),
 ('guaranteed_additions', 'Non-Par Savings,Par', r'guaranteed addition', None, 'Guaranteed additions'),
 ('loyalty_additions', 'ALL', r'loyalty addition', None, 'Loyalty additions'),
 ('cash_bonus', 'Par', r'cash bonus', None, 'Cash bonus (par)'),
 ('reversionary_bonus', 'Par', r'reversionary bonus', None, 'Reversionary bonus (par)'),
 ('terminal_bonus', 'Par', r'terminal bonus', None, 'Terminal bonus (par)'),
 ('survival_benefit_money_back', 'Par,Non-Par Savings', r'survival benefits? (of|equal to|is|are|shall be|will be|payable).{0,80}(%|every|end of (each|the|policy year))|money ?back', r'no survival benefit|survival benefit:? (is )?(not|nil)', 'Periodic survival benefits (money-back)'),
 ('premium_offset_or_holiday', 'ALL', r'premium (offset|holiday)', None, 'Premium offset / premium holiday'),
 ('policy_loan', 'Non-Par Savings,Par,Annuity', r'policy loan|loan (facility|available|against)', None, 'Policy loan available'),
 ('child_payor_benefit', 'ALL', r'payor|parent.{0,30}(death|waiv)|(death|waiv).{0,30}parent|proposer.{0,30}death', None, 'Payor / parent waiver (inbuilt or via rider)'),
 # ULIP
 ('fund_switch', 'ULIP', r'switch', None, 'Fund switching'),
 ('free_switches_unlimited', 'ULIP', r'unlimited (free )?switch|switch(es)?.{0,30}unlimited|free of (any )?charge.{0,40}switch', None, 'Unlimited free switches'),
 ('premium_redirection', 'ULIP', r'premium redirection|redirect', None, 'Premium redirection'),
 ('partial_withdrawal', 'ULIP,Non-Par Savings', r'partial withdrawal', None, 'Partial withdrawals'),
 ('systematic_withdrawal', 'ULIP', r'systematic withdrawal|swp\b', None, 'Systematic withdrawal plan'),
 ('top_up_premium', 'ULIP', r'top[- ]?up premium', None, 'Top-up premiums'),
 ('return_of_mortality_charges', 'ULIP', r'return of mortality|mortality charges?.{0,30}(return|refund|added back)', None, 'Return of mortality charges (TULIP feature)'),
 ('return_of_allocation_charges', 'ULIP', r'return of (premium )?allocation|allocation charges?.{0,40}(return|refund|added back)', None, 'Return of premium allocation charges'),
 ('wealth_boosters', 'ULIP', r'wealth booster|booster', None, 'Wealth boosters'),
 ('auto_strategies', 'ULIP', r'systematic transfer|life ?cycle|auto(matic)? (asset|rebalanc|trigger)|stp\b|portfolio strateg|trigger', None, 'Automatic portfolio strategies (life-cycle, STP, triggers)'),
 ('settlement_option', 'ULIP', r'settlement option', None, 'Settlement option at maturity'),
 ('nil_premium_allocation_charge', 'ULIP', r'(premium allocation charge|allocation charge).{0,60}\b(nil|zero|0\s*%)', None, 'Nil premium allocation charge'),
 ('nil_policy_admin_charge', 'ULIP', r'(policy administration charge|admin(istration)? charge).{0,60}\b(nil|zero)', None, 'Nil policy admin charge'),
 ('pension_ulip_guaranteed_vesting', 'ULIP', r'vesting', None, 'Pension vesting (pension ULIP)'),
 # annuity
 ('annuity_life', 'Annuity', r'life annuity|annuity (for|payable for) life', None, 'Life annuity'),
 ('return_of_purchase_price', 'Annuity', r'return of (the )?purchase price|\bROP\b|purchase price.{0,30}(returned|refund)', None, 'Return of purchase price'),
 ('joint_life_annuity', 'Annuity', r'joint life', None, 'Joint life annuity'),
 ('increasing_annuity', 'Annuity', r'(increas|escalat)ing annuity|annuity (increas|escalat)', None, 'Increasing / escalating annuity'),
 ('deferred_annuity', 'Annuity', r'deferred annuity|deferment period', None, 'Deferred annuity'),
 ('nps_annuity', 'Annuity', r'\bNPS\b|national pension', None, 'NPS-linked annuity purchase'),
 ('critical_illness_rop_annuity', 'Annuity', r'critical illness', None, 'Purchase price back on critical illness'),
 ('top_up_annuity', 'Annuity', r'top[- ]?up', None, 'Top-up annuity'),
 # all
 ('riders_available', 'ALL', r'\brider', r'no riders?|riders? (are )?not (available|allowed)', 'Riders available'),
 ('tax_benefit_mention', 'ALL', r'tax benefit', None, 'Tax benefit stated'),
 ('nri_available', 'ALL', r'\bNRI\b|non[- ]resident', None, 'Available to NRIs / mentions NRI'),
 ('pos_variant', 'ALL', r'\bPOS\b|point of sales?', None, 'POS variant / channel'),
]

def applies(cat, scope):
    return scope == 'ALL' or cat in scope.split(',')

def ulip_numbers(pgs):
    allt = '\n'.join(pgs)
    sfin = sorted(set(re.findall(r'ULIF\d{3}\d{6}[A-Z0-9]{3,12}\d{3}', allt.replace(' ', ''))))
    fmc = [float(x) for m in re.finditer(r'fund management charge.{0,1200}', allt, re.I | re.S)
           for x in re.findall(r'(\d\.\d{1,2})\s*%', m.group(0))[:30] if 0 < float(x) <= 1.5]
    return {'ulip_fund_count_sfin': len(sfin) or '', 'ulip_fmc_min_pct': min(fmc) if fmc else '', 'ulip_fmc_max_pct': max(fmc) if fmc else ''}

def annuity_numbers(pgs):
    allt = '\n'.join(pgs)
    opts = set(re.findall(r'option\s*(\d{1,2}|[A-Z])\b', allt, re.I))
    return {'annuity_option_labels_found': len(opts) or ''}

# ---------------------------------------------------------------- run
rows, ev, log = [], [], []
now = datetime.date.today().isoformat()
for r in res:
    m = mast.get(r['row_id'], {})
    ix = idx.get((r['uin'], r['doc_type']), {})
    tp = os.path.join(B, ix.get('text_path', '')) if ix else ''
    if not tp or not os.path.exists(tp):
        continue
    pgs = pages_of(tp)
    words = re.findall(r'[A-Za-z]{3,}', ' '.join(pgs)[:20000])
    common = sum(1 for w in words if w.lower() in {'the', 'and', 'policy', 'premium', 'benefit', 'life', 'insurance', 'plan', 'of', 'for', 'sum', 'assured', 'death', 'term', 'will', 'shall', 'payable'})
    garbled = bool(words) and (common / len(words) < 0.04 or len(re.findall(r'[\]\[\\^]{2,}', ' '.join(pgs)[:20000])) > 30)
    c = classify(r['irdai_description_line'], r['uin'], m.get('council_category', ''))
    row = {'row_id': r['row_id'], 'insurer': r['insurer'], 'product_name': r['product_name'], 'uin': r['uin'],
           'uin_in_document': r['uin_in_document'], 'doc_type': r['doc_type'], 'irdai_description_line': r['irdai_description_line'],
           **c, 'standard_or_pos_tag': m.get('standard_or_pos_tag', ''), 'council_category': m.get('council_category', ''),
           'pages': len(pgs), 'text_quality': 'GARBLED - features not readable (needs OCR)' if garbled else 'ok'}
    row.update(numeric_fields(pgs))
    if c['market_category'] == 'ULIP': row.update(ulip_numbers(pgs))
    if c['market_category'] == 'Annuity': row.update(annuity_numbers(pgs))
    for key, scope, rx, excl, _ in F:
        if garbled:
            row['f_' + key] = '?'; continue
        if not applies(c['market_category'], scope):
            continue
        hit = find(pgs, rx, exclude=excl)
        row['f_' + key] = 'Y' if hit else 'N'
        if hit:
            ev.append({'uin': r['uin'], 'insurer': r['insurer'], 'feature': key, 'page': hit[0], 'evidence': hit[1][:260]})
    rows.append(row)
    log.append({'iteration': 'v1', 'date': now, 'uin': r['uin'], 'insurer': r['insurer'], 'product_name': r['product_name'],
                'doc_type': r['doc_type'], 'source_url': r['source_url'], 'sha256': ix.get('sha256', ''), 'text_path': ix.get('text_path', '')})

cols = []
for rr in rows:
    for k in rr:
        if k not in cols: cols.append(k)
os.makedirs(OUT, exist_ok=True)
for name, data, cc in (('product_features_v1.csv', rows, cols), ('feature_evidence_v1.csv', ev, ['uin', 'insurer', 'feature', 'page', 'evidence']),
                       ('brochures_used_log.csv', log, list(log[0].keys()))):
    with open(os.path.join(OUT, name), 'w', newline='') as fh:
        w = csv.DictWriter(fh, fieldnames=cc, extrasaction='ignore'); w.writeheader(); w.writerows(data)
import json
json.dump([{'feature': k, 'applies_to': s, 'regex': rx, 'exclude': ex, 'definition': d} for k, s, rx, ex, d in F],
          open(os.path.join(OUT, 'feature_catalogue_v1.json'), 'w'), indent=1)
print('products', len(rows), 'evidence rows', len(ev))
print(collections.Counter(r['market_category'] for r in rows))
print(collections.Counter(r['sub_basis'] for r in rows))
