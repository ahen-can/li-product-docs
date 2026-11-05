"""ULIP feature list v2: deep-discovery data (features/ulip/<UIN>.json) where it exists,
v1 brochure flags for every other ULIP. Re-run as more deep files arrive (that run is v3).
Usage: python3 -I analysis/scripts/build_ulip_v2.py <repo_dir>"""
import csv, json, glob, os, re, sys, collections as C
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

R = sys.argv[1]
A = os.path.join(R, 'analysis')

# ---------- inputs ----------
v1 = [r for r in csv.DictReader(open(os.path.join(A, 'product_features_v1.csv'), encoding='utf-8')) if r['market_category'] == 'ULIP']
ev1 = C.defaultdict(dict)
for r in csv.DictReader(open(os.path.join(A, 'feature_evidence_v1.csv'), encoding='utf-8')):
    ev1[r['uin']][r['feature']] = (r['page'], r['evidence'])
cat = {f['feature']: f for f in json.load(open(os.path.join(A, 'feature_catalogue_v1.json')))}
deep = {}
for f in sorted(glob.glob(os.path.join(R, 'features/ulip/*.json'))):
    deep[os.path.basename(f)[:-5]] = json.load(open(f, encoding='utf-8'))
master = {r['uin']: r for r in csv.DictReader(open(os.path.join(R, 'master_list.csv'), encoding='utf-8'))}

products = {}
for r in v1:
    key = r['uin'] or f"no-uin-{r['row_id']}"
    products[key] = {'uin': r['uin'], 'insurer': r['insurer'], 'name': r['product_name'], 'sub': r['sub_segment_v1'], 'v1': r}
for u, d in deep.items():
    if u not in products:
        m = master.get(u, {})
        products[u] = {'uin': u, 'insurer': m.get('insurer', ''), 'name': d['product']['product_name']['value'], 'sub': '', 'v1': None}
for k, p in products.items():
    p['src'] = 'deep' if k in deep else 'brochure'
    if not p['insurer'] and k in deep:
        p['insurer'] = master.get(k, {}).get('insurer', '')
    if k in deep and not p['name']:
        p['name'] = deep[k]['product']['product_name']['value']

ORDER = ['Bharti Life']
def sort_key(k):
    p = products[k]
    return (0 if p['insurer'] in ORDER else 1, 0 if p['src'] == 'deep' else 1, p['insurer'], p['name'])
keys = sorted(products, key=sort_key)
DEEP = [k for k in keys if products[k]['src'] == 'deep']
BRO = [k for k in keys if products[k]['src'] == 'brochure']

# ---------- status helpers ----------
CODE = {'built-in': 'B', 'optional (at inception)': 'O', 'optional (during term)': 'O', 'rider': 'R', 'not offered': 'N',
        'not stated in public documents': '?', 'n/a': 'n/a'}
YES = {'B', 'O', 'R'}


def fld(d, path):
    g, k = path.split('.')
    return d.get(g, {}).get(k, {}) or {}


def flat(v):
    if v is None: return ''
    if isinstance(v, str): return v
    if isinstance(v, (int, float)): return str(v)
    if isinstance(v, list):
        return '; '.join(flat(x.get('name', '') + (': ' + (x.get('description') or x.get('rule') or x.get('mechanics') or '') if isinstance(x, dict) else '')) if isinstance(x, dict) else flat(x) for x in v)
    return '; '.join(f"{a}: {flat(b)}" for a, b in v.items())


STOP = set('about above after again against all also amount annual annualised annualized any applicable based before being below between charge charges each every first from have into level month monthly other over paid payable per policy premium premiums rate same shall than their there these this through under until where which while will with within year years'.split())


def strength(code, val, doc, quote):
    """Does the quote show the value itself? strong / weak / n/a. Deep-data cells only."""
    if not quote or doc in (None, 'brochure') or code in ('K', 'Y', '-', ''):
        return ''
    if not val:
        return 'n/a (status only)'
    q = re.sub(r'(?<=\d),(?=\d)', '', quote.lower())
    v = re.sub(r'(?<=\d),(?=\d)', '', val.lower())
    nums = set(re.findall(r'\d+(?:\.\d+)?', v)) - {'0', '1', '2'}
    if nums:
        return 'strong' if any(re.search(r'(?<![\d.])' + re.escape(n) + r'(?![\d])', q) for n in nums) else 'weak'
    words = [w for w in re.findall(r'[a-z]{5,}', v) if w not in STOP]
    if not words:
        return 'n/a (status only)'
    return 'strong' if sum(w in q for w in words) >= min(2, len(words)) else 'weak'


def cell(d, path):
    o = fld(d, path)
    return CODE.get(o.get('status'), o.get('status') or '?'), flat(o.get('value')), o.get('doc'), o.get('page'), o.get('quote')


def from_value(d, path, rx, neg_rx=None):
    """Derive a yes/no from a value text (e.g. 'single' in ppt_options)."""
    o = fld(d, path); t = flat(o.get('value'))
    if not t: return '?', '', o.get('doc'), o.get('page'), o.get('quote')
    if neg_rx and re.search(neg_rx, t, re.I): return 'N', t, o.get('doc'), o.get('page'), o.get('quote')
    return ('B' if re.search(rx, t, re.I) else 'N'), t, o.get('doc'), o.get('page'), o.get('quote')


def nil_charge(d, path):
    o = fld(d, path); t = flat(o.get('value')).strip()
    if not t: return '?', '', o.get('doc'), o.get('page'), o.get('quote')
    if t.lower().strip('"') == 'nil': code = 'B'
    elif re.search(r'(option|plan|growth|secure|flexi-growth)[^;:]*:\s*nil(;|$)', t, re.I): code = 'O'
    else: code = 'N'
    return code, t, o.get('doc'), o.get('page'), o.get('quote')


def with_rider(d, path, rx):
    code, val, doc, pg, q = cell(d, path)
    if code in ('N', '?'):
        rv = fld(d, 'protection_add_ons.riders_available')
        if re.search(rx, flat(rv.get('value')), re.I):
            return 'R', flat(rv.get('value')), rv.get('doc'), rv.get('page'), rv.get('quote')
    return code, val, doc, pg, q


def pct_max(t, skip=r'discontinu'):
    vals = []
    t = re.sub(r'\(allocation rate[^)]*\)', '', t)
    for part in re.split(r';|\n', t):
        if re.search(skip, part, re.I): continue
        vals += [float(x) for x in re.findall(r'(\d+(?:\.\d+)?)\s*%', part)]
    return vals


# v1 feature -> how to read it from deep JSON. None = no deep field, brochure flag kept.
V1_MAP = {
    'ppt_single_pay': lambda d: from_value(d, 'eligibility.ppt_options', r'single', r'no single'),
    'ppt_limited_pay': lambda d: from_value(d, 'eligibility.ppt_options', r'limited|\b\d+ years|\b\d+, \d+'),
    'ppt_regular_pay': lambda d: from_value(d, 'eligibility.ppt_options', r'regular'),
    'monthly_mode': lambda d: from_value(d, 'eligibility.premium_modes', r'monthly'),
    'terminal_illness': lambda d: cell(d, 'protection_add_ons.terminal_illness'),
    'critical_illness_inbuilt_or_option': lambda d: with_rider(d, 'protection_add_ons.critical_illness', r'critical'),
    'accidental_death_extra': lambda d: with_rider(d, 'protection_add_ons.accidental_death', r'accident'),
    'waiver_of_premium': lambda d: with_rider(d, 'protection_add_ons.waiver_of_premium_inbuilt', r'waiver'),
    'loyalty_additions': lambda d: cell(d, 'benefits.loyalty_additions'),
    'premium_offset_or_holiday': lambda d: cell(d, 'flexibility.premium_holiday_or_offset'),
    'fund_switch': lambda d: cell(d, 'flexibility.fund_switching'),
    'free_switches_unlimited': lambda d: from_value(d, 'charges.switching_charge', r'unlimited|any number|^nil', r'\d+ free|free switches a year|first \d'),
    'premium_redirection': lambda d: cell(d, 'flexibility.premium_redirection'),
    'partial_withdrawal': lambda d: cell(d, 'flexibility.partial_withdrawals'),
    'systematic_withdrawal': lambda d: cell(d, 'flexibility.systematic_withdrawal_plan'),
    'top_up_premium': lambda d: cell(d, 'flexibility.top_up_premiums'),
    'return_of_mortality_charges': lambda d: cell(d, 'benefits.return_of_mortality_charges'),
    'return_of_allocation_charges': lambda d: cell(d, 'benefits.return_of_premium_allocation_charges'),
    'wealth_boosters': lambda d: cell(d, 'benefits.wealth_boosters_or_guaranteed_additions'),
    'auto_strategies': lambda d: cell(d, 'flexibility.auto_portfolio_strategies'),
    'settlement_option': lambda d: cell(d, 'flexibility.settlement_option'),
    'nil_premium_allocation_charge': lambda d: nil_charge(d, 'charges.premium_allocation_charge'),
    'nil_policy_admin_charge': lambda d: nil_charge(d, 'charges.policy_administration_charge'),
    'riders_available': lambda d: cell(d, 'protection_add_ons.riders_available'),
}

# Schema rows that v1 did not have (status rows and value rows)
NEW_SCHEMA = [
    ('Eligibility', 'entry_age_min', 'eligibility.entry_age_min', 'value'),
    ('Eligibility', 'entry_age_max', 'eligibility.entry_age_max', 'value'),
    ('Eligibility', 'maturity_age_max', 'eligibility.maturity_age_max', 'value'),
    ('Eligibility', 'policy_term_options', 'eligibility.policy_term_options', 'value'),
    ('Eligibility', 'ppt_options', 'eligibility.ppt_options', 'value'),
    ('Eligibility', 'premium_min_annual', 'eligibility.premium_min_annual', 'value'),
    ('Eligibility', 'premium_min_single', 'eligibility.premium_min_single', 'value'),
    ('Eligibility', 'premium_max', 'eligibility.premium_max', 'value'),
    ('Eligibility', 'premium_modes', 'eligibility.premium_modes', 'value'),
    ('Eligibility', 'sum_assured_rule', 'eligibility.sum_assured_rule', 'value'),
    ('Eligibility', 'life_cover_multiple_choice', 'eligibility.life_cover_multiple_choice', 'status'),
    ('Product', 'variants_or_plan_options', 'product.variants_or_plan_options', 'value'),
    ('Charges', 'premium_allocation_charge', 'charges.premium_allocation_charge', 'value'),
    ('Charges', 'policy_administration_charge', 'charges.policy_administration_charge', 'value'),
    ('Charges', 'fund_management_charge', 'charges.fund_management_charge', 'value'),
    ('Charges', 'mortality_charge', 'charges.mortality_charge', 'value'),
    ('Charges', 'discontinuance_charge', 'charges.discontinuance_charge', 'value'),
    ('Charges', 'switching_charge', 'charges.switching_charge', 'value'),
    ('Charges', 'partial_withdrawal_charge', 'charges.partial_withdrawal_charge', 'value'),
    ('Charges', 'premium_redirection_charge', 'charges.premium_redirection_charge', 'value'),
    ('Charges', 'miscellaneous_charge', 'charges.miscellaneous_charge', 'value'),
    ('Charges', 'guarantee_charge', 'charges.guarantee_charge', 'value'),
    ('Charges', 'any_charge_returned', 'charges.any_charge_returned', 'status'),
    ('Benefits', 'death_benefit_formula', 'benefits.death_benefit_formula', 'value'),
    ('Benefits', 'maturity_benefit', 'benefits.maturity_benefit', 'value'),
    ('Benefits', 'return_of_policy_admin_charges', 'benefits.return_of_policy_admin_charges', 'status'),
    ('Benefits', 'other_additions', 'benefits.other_additions', 'status'),
    ('Flexibility', 'increase_decrease_cover', 'flexibility.increase_decrease_cover', 'status'),
    ('Flexibility', 'change_ppt_or_term', 'flexibility.change_ppt_or_term', 'status'),
    ('Flexibility', 'policy_loan', 'flexibility.policy_loan', 'status'),
    ('Funds', 'fund_count', 'funds.fund_count', 'value'),
    ('Funds', 'index_or_thematic_funds', 'funds.index_or_thematic_funds', 'value'),
    ('Protection', 'spouse_or_child_cover', 'protection_add_ons.spouse_or_child_cover', 'status'),
    ('Surrender', 'lock_in_years', 'surrender_revival.lock_in_years', 'value'),
    ('Surrender', 'revival_period', 'surrender_revival.revival_period', 'value'),
    ('Surrender', 'surrender_value_rule', 'surrender_revival.surrender_value_rule', 'value'),
]

# New features found in the deep pass, grouped. Keyword = brochure/policy search used for all ULIPs (unverified hits).
NEW_FEAT = [
    ('refund_fmc_or_all_charges', 'Refund of fund management charges, or of all charges', [
        'Return of fund management charges', 'Refund of 118% of all charges, including FMC', 'Refund of all three main charges'],
     r'(return|refund)\w*\s+of\s+(all\s+)?(the\s+)?(fund management charges?|FMC)\b|refund of (all )?(the )?charges'),
    ('multiplied_charge_refunds', 'Charges returned at a multiple (2x, 3x, 118%)', [ 'Return of 4x allocation charges, 1-3x administration charges and 1-2x mortality charges', 'Return of policy administration charges at 1.5x or 2x', '2x return of premium allocation charges and 2x return of mortality charges', 'Return of 2X mortality charges', 'Up to 600% return of premium allocation charges', 'Return of policy administration charges above 100%', 'Return of charges above 100%', 'Return of mortality charges above 100%', 'Refund of 2x allocation charges',
        'Double return of premium allocation charges', 'Rising multiple of mortality charges returned', 'Return of 2x guarantee charges'],
     r'\b(2|3|two|three)\s*(x|times)\b.{0,60}(premium allocation|mortality|guarantee) charges'),
    ('capital_or_vesting_guarantee', 'Capital guarantee at maturity or assured vesting benefit', [
        'Capital guarantee on maturity', 'Assured vesting benefit'],
     r'assured vesting benefit|capital guarantee|guaranteed (maturity|vesting) benefit'),
    ('scheduled_guaranteed_additions', 'Guaranteed or special additions on a fixed schedule or by premium band', [ 'Guaranteed additions as a share of average fund value', 'Guaranteed Wealth Booster every 5 years', 'Elite guaranteed wealth booster', 'Fund Booster every 5 years', 'Guaranteed additions that rise to 15.5%', 'Guaranteed additions on a single premium', 'Whole life cover with limited premium paying term and guaranteed additions',
        'Guaranteed addition at maturity by premium band', 'Guaranteed additions every 5 years', 'Special additions on early premiums', 'Terminal addition on death and vesting'],
     r'guaranteed additions?|special additions?|terminal addition'),
    ('loyalty_design_variants', 'Loyalty additions with a special design (premium size, high cover, rising, large at maturity)', [ '3% loyalty additions from year 6', 'Loyalty additions and maturity booster in a pension ULIP', 'Value booster', 'Maturity booster', 'Loyalty additions that rise 0.05% a year (Milestone variant)', 'Rising loyalty additions', 'Loyalty additions that rise every year', 'Premium bands for additions', 'Maturity Booster', 'Fund Maintenance Booster', 'Loyalty addition only for large single premiums', 'High premium booster',
        'Loyalty additions only for larger premiums', 'Booster for high death benefit multiples', 'Rising loyalty additions on a 12-month average fund value', 'Large loyalty additions at maturity'],
     None),
    ('customer_type_boosters', 'Extra benefit or lower charges for a customer type (women, existing customers, ECS payers, direct buyers, staff)', [ 'Smart Lady extra allocation', 'Family benefit', 'Auto Debit Booster', 'Twin loyalty booster for combined purchase',
        'EmpowHer Booster for women', 'ECS payment benefit', 'Existing customer benefit', 'Loyalty reward for direct purchases', 'Reduced charges for staff'],
     r'existing customers? (will receive|benefit)|female (customers|lives).{0,80}(additional|booster)|\bstaff\b.{0,60}(charge|discount)|direct (channel|marketing|sales?).{0,80}(reward|additional)'),
    ('women_life_event_cover', 'Women-specific cover (pregnancy complications, childbirth, female cancers)', [
        'Women-specific event cover', 'Free switches and withdrawals after childbirth'],
     r'pregnancy complication|congenital|childbirth'),
    ('joint_life', 'Joint life cover', [ 'Spouse cover with a second life','Joint life ULIP (single pay)'], r'\bjoint life\b'),
    ('decreasing_cover_option', 'Decreasing life cover option', ['Decreasing cover after a level cover period'], r'decreasing (cover|sum assured|life cover)'),
    ('death_benefit_waiver_plus_income', 'Plan continues after death: insurer funds future premiums and/or pays a family income', [ 'Golden Waiver of Premium Option with Wealth Care Switcher', 'Premium funding benefit (Alpha Premium Plus)', 'Premium funding benefit (Promise4Care)', 'Premium funding benefit and income benefit (Shield)', 'Assured Option keeps the policy running after a death claim', 'Variant 2 Family Income Benefit', 'Family Income Benefit plus funded premiums','Death benefit with waiver plus monthly income'],
     r'classic waiver plus|waiver plus'),
    ('builtin_accident_or_payor_waiver', 'Built-in accident benefit or premium waiver inside the ULIP', [ 'Waiver of premium on total and permanent disability', 'Multiple premium waiver on death', 'Waiver of premium on accidental disability', 'Premium waiver on accidental disability in a pension plan',
        'Built-in accident benefit inside a ULIP', 'Child ULIP with built-in payor waiver and accident benefit', "Loyalty additions continue after the parent's death", 'Proposer premium waiver for a different life assured'],
     r'(in-?built|built-?in)\s+(accident|premium payor|premium waiver)|premium payor waiver'),
    ('restricted_withdrawals', 'Partial withdrawals limited to listed purposes or capped (amount or number)', [ 'Restricted partial withdrawals for named life events',
        'Partial withdrawal only for listed purposes', 'Purpose-restricted partial withdrawals', 'Withdrawal cap of 15% of fund value and 10 per term'],
     r'withdraw\w*.{0,250}(higher education|marriage of)|(higher education|marriage of).{0,250}partial withdraw'),
    ('premium_cap', 'Maximum premium cap, or monthly-only payment', ['Maximum premium cap', 'Monthly-only ULIP with a premium cap'], None),
    ('min_fund_termination', 'Policy ends if fund value falls below a set level after lock-in', ['Policy ends if fund value falls below one annualised premium after lock-in'],
     r'fund value.{0,80}(falls|less than|below).{0,80}terminat'),
    ('delayed_risk_start_minor', 'Risk cover for a minor starts later, with no mortality charge until then', ['Delayed risk start for minors'],
     r'deferred risk|delayed risk|risk (cover )?(shall|will) (commence|start) (on|from) .{0,60}(birthday|attain)'),
    ('uk_pension_transfer', 'Accepts UK pension transfers (QROPS/QOPS)', [ 'QROPS-eligible pension plan','QROPS/QOPS transfer of UK pension assets'], r'QROPS|QOPS'),
    ('mortality_rates_guaranteed', 'Mortality rates guaranteed for the term, or separate female table', [
        'Mortality rates guaranteed for the term', 'Separate male and female mortality tables'],
     r'mortality charges?\s+(are|is|will be|shall be)\s+guaranteed|rates of mortality charges are guaranteed'),
    ('allocation_above_100', 'Extra allocation: more than 100% of premium invested in some years', [ 'Early Investment Booster', 'First-year additional allocation', 'Extra allocation for women','Allocation rate above 100%'], r'allocation rate.{0,60}10[1-9](\.\d+)?\s*%'),
    ('lower_charges_online', 'Better terms for online purchase (lower charges or extra boosters)', [ 'Extra benefits for digital sales', 'Fund booster for online sales','Lower service charges online'], None),
    ('index_or_low_cost_funds', 'Index funds or low-FMC funds', [ 'Two index-based fund types','Index funds with lower FMC', 'Low-cost Money Market Fund'], r'\bindex fund\b|nifty\s*\d+\s*index'),
    ('admin_charge_waived_some_years', 'No admin charge for part of the term', ['Admin charge only for a limited period', 'No admin charge in years 1-4'], None),
    ('settlement_enhancer', 'Extra return on settlement instalments', ['Settlement instalments increased by 0.5%', 'Return Enhancer on settlement'], None),
    ('value_added_services', 'Non-insurance services (health management, partner loyalty rewards)', ['Third-party loyalty program reward', 'Health management services'], None),
    ('mortality_as_ialm_share', 'Mortality rates set as a share of the IALM standard table', ['Mortality rates set as a share of IALM by age band'], None),
    ('cover_continuance_booster', 'Booster for keeping the policy in force with cover', [ 'Cover Continuance Booster','Cover continuance booster', 'Cover continuance booster with yearly cap'], None),
    ('annuity_purchase_booster', 'Booster if the vesting fund buys an annuity from the same insurer', [ 'Annuity booster at vesting','Annuity purchase booster'], None),
    ('increasing_cover', 'Sum assured that steps up over time', ['Sum assured that steps up over time'], None),
    ('high_cover_multiple', 'Very high life cover multiple (30x to 125x annual premium, or 10x a single premium)', [ 'Life cover multiple up to 100 times the annualized premium', 'Sum assured up to 100 times the annualized premium', 'Single premium with up to 10 times death cover','Sum assured up to 30 times the annualized premium', 'Sum assured up to 125 times the annualized premium'], None),
    ('premium_step_up', 'Premium that steps up over time by design', ['Save More Tomorrow'], None),
    ('vesting_postponement', 'Pension vesting date can be postponed', ['Postponement of vesting date', 'Extend the vesting date'], None),
    ('no_mortality_charge', 'No life cover charge (pension ULIP without risk cover)', ['No mortality charge'], None),
]
EXISTING = {'Zero policy administration charge, wealth boosters and 8% loyalty additions': 'nil_policy_admin_charge', 'Systematic partial withdrawal': 'systematic_withdrawal', 'Top-up premiums with extra cover': 'top_up_premium', 'Systematic Allocator glide path': 'auto_strategies', 'AutoSwitcher': 'auto_strategies', 'Leave-it-to-us risk levels': 'auto_strategies', 'Child Wealth variant: eligibility and term': 'variants_or_plan_options', 'Child Wealth variant: premium and sum assured': 'variants_or_plan_options', 'Child Wealth variant: policy administration charge': 'variants_or_plan_options', 'Child Wealth variant: fund management charge': 'variants_or_plan_options', 'Joint Life Wealth variant: eligibility and term': 'variants_or_plan_options', 'Joint Life Wealth variant: charges': 'variants_or_plan_options', 'Milestone and systematic withdrawal options': 'systematic_withdrawal', 'Milestone withdrawal option': 'systematic_withdrawal', 'Zero premium allocation charge pension ULIP with maturity booster': 'nil_premium_allocation_charge', 'Zero allocation and administration charges': 'nil_premium_allocation_charge', 'Zero allocation and administration charges, 15 funds': 'nil_premium_allocation_charge', 'Three plan options with premium funding (Premium Plus) and cover to age 99 (Life Plus)': 'variants_or_plan_options', 'Increase or decrease of sum assured': 'increase_decrease_cover', 'Premium bands with falling allocation charge': 'premium_allocation_charge', 'Return of premium allocation and mortality charges at maturity': 'return_of_mortality_charges', 'Refund of all mortality charges at maturity': 'return_of_mortality_charges', 'Refund of mortality charges at maturity': 'return_of_mortality_charges', 'Return of Charges by premium band': 'any_charge_returned', 'Periodical return of mortality and WOP charges': 'return_of_mortality_charges', 'Return of mortality charges every 5 years': 'return_of_mortality_charges', 'Vesting Booster and Return of Allocation Charge': 'return_of_allocation_charges', 'Zero premium allocation charge and zero policy administration charge': 'nil_premium_allocation_charge', 'Zero allocation and administration charge': 'nil_premium_allocation_charge', 'Systematic transfer on a weekly basis': 'auto_strategies', 'Single premium with systematic transfer': 'auto_strategies', 'Systematic Transfer Plan and Dynamic Fund Allocation': 'auto_strategies', 'Target Asset Allocation Strategy': 'auto_strategies', 'Capital Preservation Oriented Strategy': 'auto_strategies', 'Return Optimiser option': 'auto_strategies', 'Four asset-mix fund types': 'auto_strategies', 'Gold, Platinum and Titanium variants': 'variants_or_plan_options', '3D Life Secure variant': 'variants_or_plan_options', 'Assure variant': 'variants_or_plan_options', 'Child Wealth variant': 'variants_or_plan_options', 'Nine premium-charge variants': 'variants_or_plan_options', 'Single-premium plan with two sum assured options': 'variants_or_plan_options', 'Whole-of-life plan': 'variants_or_plan_options', 'Whole Life variant with Smart Withdrawals': 'variants_or_plan_options', 'Child-linked eligibility': 'variants_or_plan_options', 'Smart Retire Income': 'systematic_withdrawal', 'Retired Life Income': 'systematic_withdrawal', 'Increase or decrease of basic sum assured': 'increase_decrease_cover', 'Top-up with its own sum assured': 'top_up_premium', 'Zero premium allocation charge': 'nil_premium_allocation_charge', 'Age-based automatic fund mix': 'auto_strategies', 'Target asset allocation strategy': 'auto_strategies', 'Trigger-based profit booking': 'auto_strategies', 'Chosen-rate and index-based withdrawal plans': 'systematic_withdrawal', 'Low-charge option with smaller refunds': 'variants_or_plan_options', 'Death benefit settlement option': 'death_benefit_as_income',
            'Two variants with different add-backs': 'variants_or_plan_options'}
nf_index = {n: g for g, _, names, _ in NEW_FEAT for n in names}

# ---------- text for keyword search ----------
def pages_for(uin):
    out = []
    for t in sorted(glob.glob(os.path.join(R, 'text', '*', uin, '*.txt'))):
        dt = os.path.basename(t)[:-4]
        if dt.startswith('cis'): continue
        for i, pg in enumerate(open(t, encoding='utf-8', errors='replace').read().split('\f'), 1):
            out.append((dt, i, re.sub(r'\s+', ' ', pg)))
    return out


def kw_hit(uin, rx):
    for dt, pg, txt in pages_for(uin):
        m = re.search(rx, txt, re.I)
        if m:
            s = max(0, m.start() - 80)
            return dt, pg, txt[s:m.end() + 80]
    return None

# ---------- build cells ----------
LOOSE = {'pension_ulip_guaranteed_vesting', 'tax_benefit_mention', 'nri_available', 'riders_available', 'disability_benefit'}
rows = []      # feature rows: dict
cells = {}     # (feature, product_key) -> (code, value, doc, page, quote)
corr = []

for f, c in cat.items():
    ap = c['applies_to']
    if not (ap == 'ALL' or 'ULIP' in ap):
        continue
    rows.append({'id': f, 'group': 'v1 feature', 'def': c['definition'], 'new': '', 'kind': 'status',
                 'source_note': ('deep field' if f in V1_MAP else 'brochure only (no deep field)') + ('; v1 keyword is loose (counts mentions, not the feature)' if f in LOOSE else '')})
    for k in keys:
        p = products[k]; v1row = p['v1'] or {}
        b = v1row.get('f_' + f, '')
        if p['src'] == 'deep' and f in V1_MAP:
            code, val, doc, pg, q = V1_MAP[f](deep[k])
            cells[(f, k)] = (code, val, doc, pg, q)
            if b:
                if b == 'Y' and code == 'N':
                    corr.append([p['insurer'], p['name'], k, f, 'v1 said yes, deep says not offered', ev1[k].get(f, ('', ''))[1][:200], q])
                elif b == 'N' and code in YES:
                    corr.append([p['insurer'], p['name'], k, f, f'v1 missed it (deep: {code})', '', q])
                elif b == 'Y' and code == '?':
                    corr.append([p['insurer'], p['name'], k, f, 'v1 brochure yes, deep not stated (kept as ?)', ev1[k].get(f, ('', ''))[1][:200], ''])
        else:
            e = ev1[k].get(f) if b == 'Y' else None
            cells[(f, k)] = ('Y' if b == 'Y' else ('-' if b else ''), '', 'brochure' if e else None, e[0] if e else None, e[1] if e else None)

for grp, fid, path, kind in NEW_SCHEMA:
    rows.append({'id': fid, 'group': grp, 'def': f'Deep schema field {path}', 'new': 'new in v2 (deep schema)', 'kind': kind, 'source_note': 'deep only'})
    for k in DEEP:
        cells[(fid, k)] = cell(deep[k], path)
    for k in BRO:
        v1row = products[k]['v1'] or {}
        alt = {'entry_age_min': 'entry_age_min', 'entry_age_max': 'entry_age_max', 'maturity_age_max': 'maturity_age_max',
               'premium_min_annual': 'min_premium', 'fund_management_charge': None, 'fund_count': 'ulip_fund_count_sfin'}.get(fid)
        if alt and v1row.get(alt):
            cells[(fid, k)] = ('v', v1row[alt], 'brochure', None, v1row.get(alt + '_evidence', ''))
        elif fid == 'fund_management_charge' and v1row.get('ulip_fmc_max_pct'):
            cells[(fid, k)] = ('v', f"{v1row['ulip_fmc_min_pct']}% to {v1row['ulip_fmc_max_pct']}% (brochure scan)", 'brochure', None, '')

newfeat_products = C.defaultdict(list)
unmapped = []
for k in DEEP:
    for n in deep[k].get('new_features_not_in_schema', []):
        g = nf_index.get(n['feature'])
        if g:
            newfeat_products[g].append((k, n))
        elif n['feature'] in EXISTING:
            pass
        else:
            unmapped.append((k, n))
kw_count = C.Counter()
VERDICT = {}
_vp = os.path.join(A, 'v3', 'new_feature_verdicts.csv')
if os.path.exists(_vp):
    for _r in csv.DictReader(open(_vp, encoding='utf-8')):
        if _r['verdict'] == 'Y':
            VERDICT[(_r['group'], _r['uin'])] = _r
for g, label, names, rx in NEW_FEAT:
    rows.append({'id': g, 'group': 'New feature (deep pass)', 'def': label, 'new': 'new in v2 (found in deep pass)', 'kind': 'status',
                 'source_note': 'deep; keyword search of brochures for the rest' if rx else 'deep only'})
    have = {k: n for k, n in newfeat_products[g]}
    for k in keys:
        if k in have:
            n = have[k]
            cells[(g, k)] = ('B', n['description'], n['doc'], n['page'], n['quote'])
        elif (g, k) in VERDICT:
            v = VERDICT[(g, k)]
            cells[(g, k)] = ('B', v['reason'], v['doc'], int(v['page']) if v['page'] else None, v['snippet'][:400])
        elif k in deep:
            cells[(g, k)] = ('', '', None, None, None)      # searched in its documents, not found
        elif rx and k:
            h = kw_hit(k, rx)
            if h:
                cells[(g, k)] = ('K', '', h[0], h[1], h[2]); kw_count[g] += 1
            else:
                cells[(g, k)] = ('', '', None, None, None)
        else:
            cells[(g, k)] = ('', '', None, None, None)

# ---------- riders (S2 rider discovery) ----------
# results/ulip_rider_benefits.csv says, per ULIP, which stored rider gives each benefit (from the rider JSONs).
# Upgrade: a feature the ULIP does not give itself but a named rider covers becomes R.
# Downgrade: an R that came only from a rider's name, where the stored rider documents show no such benefit,
# becomes "?" (the ULIP's own documents are silent). Skipped for a ULIP whose named riders were not all stored.
RB = {}
_bp = os.path.join(R, 'results', 'ulip_rider_benefits.csv')
if os.path.exists(_bp):
    RB = {r['ulip_uin']: r for r in csv.DictReader(open(_bp, encoding='utf-8'))}
NAMED = C.defaultdict(set)
_rp = os.path.join(R, 'results', 'ulip_rider_map.csv')
if os.path.exists(_rp):
    for _r in csv.DictReader(open(_rp, encoding='utf-8')):
        if _r['rider_uin']:
            NAMED[_r['ulip_uin']].add(_r['rider_uin'])
def _ids(t): return set(re.findall(r'\d{3}[AB]\d{3}V\d{2}', t or ''))
RIDER_APPLIED = []
for k in keys:
    rb = RB.get(k)
    if not rb:
        continue
    stored = _ids(rb['riders_stored'])
    complete = NAMED[k] <= stored
    w = rb['waiver_of_ulip_premium_through']
    wv = {u for u in _ids(w) if re.search(re.escape(u) + r': (yes|unclear)', w)}
    ad = _ids(rb['accidental_death']) - (_ids(rb['term_cover']) - _ids(rb['critical_illness']) - _ids(rb['accidental_disability']))
    want = {'waiver_of_premium': (wv, w),
            'critical_illness_inbuilt_or_option': (_ids(rb['critical_illness']), rb['critical_illness']),
            'accidental_death_extra': (ad, rb['accidental_death']),
            'disability_benefit': (_ids(rb['accidental_disability']), rb['accidental_disability'])}
    for f, (ids, txt) in want.items():
        old = cells.get((f, k), ('', '', None, None, None))
        if ids and old[0] not in YES:
            note = '; '.join(sorted(ids))
            if f == 'waiver_of_premium' and 'unclear' in w:
                note += ' (rider wording: "base cover"; unclear whether it waives the ULIP premium)'
            cells[(f, k)] = ('R', 'via rider ' + note, 'rider documents (results/ulip_rider_benefits.csv)', None, txt[:400])
            RIDER_APPLIED.append([products[k]['insurer'], products[k]['name'], k, f, old[0], 'R', note])
        elif not ids and old[0] == 'R' and complete and stored:
            cells[(f, k)] = ('?', 'named riders checked: none gives this' + (' (they waive only their own premium, or none)' if f == 'waiver_of_premium' else ''),
                             'rider documents (results/ulip_rider_benefits.csv)', None, ('riders stored: ' + rb['riders_stored'])[:400])
            RIDER_APPLIED.append([products[k]['insurer'], products[k]['name'], k, f, 'R', '?', 'rider documents show no such benefit'])

# ---------- QA overrides (S3, then any later rounds) ----------
OVR_APPLIED = []
for _op in sorted(glob.glob(os.path.join(A, 'v3', '*_overrides.csv'))):
    for o in csv.DictReader(open(_op, encoding='utf-8')):
        k, f = o['uin'], o['feature']
        old = cells.get((f, k), ('', '', None, None, None))
        code = o['code'] or (old[0] if old[0] not in ('?', '') else 'n/a')
        val = o['value'] or (old[1] if not o['code'] or o['code'] in YES else '')
        if o['code'] in YES and not o['value'] and old[0] not in YES:
            val = ''
        cells[(f, k)] = (code, val, o['doc'], int(o['page']) if o['page'] else None, o['quote'][:400])
        OVR_APPLIED.append([products[k]['insurer'], products[k]['name'], k, f, old[0], code, (o['value'] or '')[:200], os.path.basename(_op), o['source']])

# headline charge numbers (deep)
CH = []
for k in DEEP:
    d = deep[k]; p = products[k]
    pac = flat(fld(d, 'charges.premium_allocation_charge').get('value'))
    fmc = flat(fld(d, 'charges.fund_management_charge').get('value'))
    pv = pct_max(pac); fv = pct_max(fmc)
    CH.append([p['insurer'], p['name'], k, max(pv) if pv else (0.0 if re.search(r'nil', pac, re.I) else None), min(fv) if fv else None, max(fv) if fv else None,
               flat(fld(d, 'charges.policy_administration_charge').get('value')), flat(fld(d, 'charges.switching_charge').get('value')),
               flat(fld(d, 'charges.partial_withdrawal_charge').get('value')), flat(fld(d, 'charges.mortality_charge').get('value')),
               flat(fld(d, 'charges.any_charge_returned').get('value')), pac, fmc])

# ---------- counts ----------
nD, nB = len(DEEP), len(BRO)
bharti = [k for k in keys if products[k]['insurer'] == 'Bharti Life']
FR = []
for r in rows:
    f = r['id']
    dc = C.Counter(cells.get((f, k), ('', '', None, None, None))[0] for k in DEEP)
    bc = C.Counter(cells.get((f, k), ('', '', None, None, None))[0] for k in BRO)
    dy = sum(dc[x] for x in YES) + dc['Y']
    by = bc['Y'] + bc['B']
    kw = bc['K'] + dc['K']
    bh = [products[k]['name'].replace('Bharti AXA Life ', '').replace('Bharti Life ', '') for k in bharti if cells.get((f, k), ('', '', None, None, None))[0] in YES | {'Y'}]
    if r['kind'] == 'value':
        filled = sum(1 for k in DEEP if cells.get((f, k), ('', '', None, None, None))[1])
        FR.append([r['group'], f, r['def'], r['new'], r['source_note'], f'{filled} of {nD} filled', '', '', '', '', '', ''])
        continue
    FR.append([r['group'], f, r['def'], r['new'], r['source_note'],
               f'{dy} of {nD}', f"B {dc['B']} / O {dc['O']} / R {dc['R']}", f"{dc['N']} not offered, {dc['?']} not stated",
               f'{by} of {nB}' if r['group'] == 'v1 feature' else '', f'{kw}' if kw else '',
               f'{dy + by} of {nD + nB}' if r['group'] == 'v1 feature' else '',
               ('Has: ' + ', '.join(bh)) if bh else 'Lacks (in Bharti\'s 7 ULIPs)'])

# ---------- write xlsx ----------
HEAD = PatternFill('solid', fgColor='1F3864'); HF = Font(bold=True, color='FFFFFF')
FILL = {'B': 'C6EFCE', 'O': 'DDEBF7', 'R': 'FFF2CC', 'N': 'F8CBAD', '?': 'EDEDED', 'Y': 'E2EFDA', 'K': 'FFE699'}
ILLEGAL = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f]')
WR = Alignment(wrap_text=True, vertical='top')
wb = Workbook(); wb.remove(wb.active)


def sheet(title, header, data, widths=None, note=None):
    ws = wb.create_sheet(title)
    r0 = 3 if note else 1
    if note: ws.cell(1, 1, note).font = Font(italic=True)
    for j, h in enumerate(header, 1):
        c = ws.cell(r0, j, h); c.fill = HEAD; c.font = HF; c.alignment = WR
    for i, row in enumerate(data, r0 + 1):
        for j, v in enumerate(row, 1):
            ws.cell(i, j, ILLEGAL.sub('', v) if isinstance(v, str) else v)
    for j in range(1, len(header) + 1):
        ws.column_dimensions[get_column_letter(j)].width = (widths or {}).get(j, 16)
    ws.freeze_panes = ws.cell(r0 + 1, 3 if title == 'Matrix' else 1)
    return ws


ws = wb.create_sheet('README')
ws.column_dimensions['A'].width = 140
L = [
    'ULIP feature list v3 (4 Nov 2026): all 84 deep-discovery ULIPs',
    f'{nD + nB} ULIPs from {len(set(p["insurer"] for p in products.values()))} insurers. {nD} have deep-discovery data (policy document, CIS and brochure, read field by field); {nB} still use the v1 brochure keyword scan.',
    'Deep products so far: ' + ', '.join(sorted(set(products[k]['insurer'] for k in DEEP))) + '. The other wave 1 insurers (Tata AIA, Bajaj, Axis Max, LIC, ABSLI, Canara HSBC) and wave 2 (ICICI, Kotak) will turn this into v3.',
    'WHAT IS NEW IN V2:',
    f'1. For deep products every feature has a type: B built-in, O optional, R rider, N not offered, ? not stated in public documents. v1 only said "mentioned in the brochure".',
    f'2. {sum(1 for r in rows if r["group"] not in ("v1 feature", "New feature (deep pass)"))} new rows from the deep schema: exact charges, eligibility, fund count, lock-in, revival, policy loan, death benefit formula and more.',
    f'3. {len(NEW_FEAT)} new features found by reading policy documents (tab "New features"), each with the products that have it and a quote. These were not in v1.',
    '4. A "v1 corrections" tab lists every place where the deep data disagrees with the v1 brochure flag.',
    'CODES IN THE MATRIX:',
    'B built-in · O optional · R rider · N not offered · ? not stated in public documents · Y mentioned in brochure (v1, type unknown) · - not found in brochure · K keyword found in the brochure or policy text, not yet verified by reading.',
    'Counts for new features use deep products only (n of ' + str(nD) + '). K hits show where the feature may also exist; they are leads for the deep pass, not counts.',
    'TABS: Features (one row each, counts, Bharti has/lacks) · Matrix (products x features) · Charges (headline numbers) · New features · v1 corrections · Evidence · Products.',
    'NEW-FEATURE COUNTS: every deep product\'s policy document and brochure were searched for each new feature (analysis/v3/new_feature_candidates.csv); S1 read each match and kept or rejected it with a reason (analysis/v3/new_feature_verdicts.csv). For deep products a blank means searched and not found. Four groups have no search pattern and count only what S2 recorded: loyalty design variants, premium cap, admin charge waived in some years, increasing cover.',
    'EVIDENCE STRENGTH: on the Evidence tab, deep cells are marked strong (the quote shows the value) or weak (the quote is a label or nearby line; the value is still from the cited page). The Products tab counts both per product. Weak quotes get redone at the end of deep wave 1.',
    'Sources: features/ulip/<UIN>.json (deep, each value with document label, page and quote), analysis/product_features_v1.csv (brochure). Rebuild: python3 -I analysis/scripts/build_ulip_v2.py <repo>.',
]
for i, l in enumerate(L, 1):
    c = ws.cell(i, 1, l); c.alignment = WR
    if i == 1: c.font = Font(bold=True, size=14)
    elif l.endswith(':'): c.font = Font(bold=True)

sheet('Features', ['Group', 'Feature', 'Definition', 'New in v2?', 'Source', f'Deep: has it (of {nD})', 'Deep: type split', 'Deep: no / unknown',
                   f'Brochure only: mentioned (of {nB})', 'Keyword leads (K)', f'All ULIPs (of {nD + nB})', 'Bharti'],
      FR, {1: 18, 2: 30, 3: 50, 4: 24, 5: 22, 6: 12, 7: 18, 8: 22, 9: 14, 10: 10, 11: 12, 12: 60})

hdr = ['Feature', 'Group'] + [f"{products[k]['insurer']} | {products[k]['name']} | {k} | {products[k]['src']}" for k in keys]
data = []
for r in rows:
    data.append([r['id'], r['group']] + [(cells.get((r['id'], k), ('', '', None, None, None))[1] or cells.get((r['id'], k), ('', '', None, None, None))[0]) if r['kind'] == 'value' else cells.get((r['id'], k), ('', '', None, None, None))[0] for k in keys])
ws = sheet('Matrix', hdr, data, {1: 30, 2: 18})
for j in range(3, len(hdr) + 1):
    ws.column_dimensions[get_column_letter(j)].width = 14
ws.row_dimensions[1].height = 120
for row in ws.iter_rows(min_row=2):
    for c in row[2:]:
        if isinstance(c.value, str) and c.value in FILL:
            c.fill = PatternFill('solid', fgColor=FILL[c.value]); c.alignment = Alignment(horizontal='center')
        elif c.value:
            c.alignment = Alignment(wrap_text=False)

CH.sort(key=lambda x: (x[0] != 'Bharti Life', x[0], x[1]))
ws = sheet('Charges', ['Insurer', 'Product', 'UIN', 'Highest allocation charge in any year (%)', 'Lowest FMC (%)', 'Highest FMC (%)',
                       'Policy admin charge', 'Switching charge', 'Partial withdrawal charge', 'Mortality charge basis', 'Charges returned',
                       'Allocation charge (full)', 'FMC (full)'], CH,
           {2: 34, 7: 45, 8: 30, 9: 25, 10: 45, 11: 45, 12: 60, 13: 45},
           note='Deep products only. Best in class is green: lowest highest-allocation charge, lowest FMC. Numbers are read from the charge text; check the full text columns for conditions.')
for col in (4, 6):
    vals = [r[col - 1] for r in CH if isinstance(r[col - 1], (int, float))]
    if vals:
        best = min(vals)
        for i, r in enumerate(CH, 4):
            if r[col - 1] == best:
                ws.cell(i, col).fill = PatternFill('solid', fgColor='C6EFCE')

NF = []
for g, label, names, rx in NEW_FEAT:
    ps = newfeat_products[g]
    kws = [f"{products[k]['insurer']} {products[k]['name']} ({k})" for k in keys if cells.get((g, k), ('', '', None, None, None))[0] == 'K']
    for k, n in ps:
        NF.append([label, len(set(x[0] for x in ps)), products[k]['insurer'], products[k]['name'], k, n['feature'], n['description'], n['doc'], n['page'], n['quote'],
                   '; '.join(kws[:15]) + (f' (+{len(kws) - 15} more)' if len(kws) > 15 else '')])
for k, n in unmapped:
    NF.append(['Not yet grouped (S1 to map)', 1, products[k]['insurer'], products[k]['name'], k, n['feature'], n['description'], n['doc'], n['page'], n['quote'], ''])
sheet('New features', ['New feature (v2 row)', f'Deep products with it (of {nD})', 'Insurer', 'Product', 'UIN', 'As found', 'Description', 'Document', 'Page', 'Quote',
                       'Keyword leads in other ULIPs (unverified)'], NF, {1: 40, 4: 30, 6: 34, 7: 50, 10: 60, 11: 60})

sheet('v1 corrections', ['Insurer', 'Product', 'UIN', 'Feature', 'Difference', 'v1 brochure evidence', 'Deep quote'], corr,
      {2: 30, 4: 28, 5: 34, 6: 60, 7: 60},
      note='Deep data wins where they disagree. These rows show how far the v1 keyword scan can be trusted for products without deep data yet.')

sheet('QA overrides', ['Insurer', 'Product', 'UIN', 'Feature', 'Code before', 'Code after', 'Value after', 'File', 'Source'], OVR_APPLIED,
      {2: 30, 4: 30, 7: 60, 8: 22, 9: 22}, note='Corrections from QA rounds (analysis/v3/*_overrides.csv). They replace the cell built from the deep data. UNSURE items are not here: they wait for a coding rule.')
sheet('Rider recoding', ['Insurer', 'Product', 'UIN', 'Feature', 'Code before', 'Code after', 'Riders / note'], RIDER_APPLIED, {2: 30, 4: 30},
      note='From S2 rider discovery (results/ulip_rider_benefits.csv, built from features/riders/*.json). R = the ULIP gives the feature only through a rider it names. R to ? = an earlier R came from a rider name, but the rider documents show no such benefit.')
EV = []
WEAK = C.defaultdict(C.Counter)
for r in rows:
    for k in keys:
        c = cells.get((r['id'], k))
        if c and c[4]:
            stg = strength(c[0], c[1], c[2], c[4])
            if stg: WEAK[k][stg] += 1
            EV.append([products[k]['insurer'], products[k]['name'], k, r['id'], c[0], c[1][:300] if c[1] else '', c[2], c[3], c[4][:400], stg])
sheet('Evidence', ['Insurer', 'Product', 'UIN', 'Feature', 'Code', 'Value', 'Document', 'Page', 'Quote / snippet', 'Evidence strength (deep)'], EV, {2: 30, 4: 28, 6: 50, 9: 80, 10: 16},
      note='Evidence strength: strong = the quote shows the value. weak = the quote is a label or nearby line; the value is still read from the cited page, open the page to confirm. S2 is redoing weak quotes at the end of wave 1.')
sheet('Products', ['Insurer', 'Product', 'UIN', 'Data source', 'Sub-segment (v1)', 'Deep cells: strong quote', 'Deep cells: weak quote'],
      [[products[k]['insurer'], products[k]['name'], k, products[k]['src'], products[k]['sub'], WEAK[k]['strong'] or '', WEAK[k]['weak'] or ''] for k in keys], {1: 22, 2: 45, 5: 36})

out = os.path.join(A, 'feature_list_ulip_v3.xlsx')
wb.save(out)
with open(os.path.join(A, 'product_features_ulip_v3.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f); w.writerow(['uin', 'insurer', 'product', 'source', 'feature', 'code', 'value', 'doc', 'page', 'quote'])
    for r in rows:
        for k in keys:
            c = cells.get((r['id'], k), ('', '', None, None, None))
            w.writerow([k, products[k]['insurer'], products[k]['name'], products[k]['src'], r['id'], c[0], c[1], c[2] or '', c[3] or '', c[4] or ''])
print('products', nD + nB, 'deep', nD, 'rows', len(rows), 'evidence', len(EV), 'corrections', len(corr), 'kw leads', dict(kw_count))
print('overrides', len(OVR_APPLIED), 'rider recodes', len(RIDER_APPLIED))
print('unmapped new features:', [(k, n['feature']) for k, n in unmapped])
