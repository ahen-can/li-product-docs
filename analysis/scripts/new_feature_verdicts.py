"""S1's review of analysis/v3/new_feature_candidates.csv (read by hand, 4 Nov 2026).
Each candidate row becomes Y or N with a reason. Writes analysis/v3/new_feature_verdicts.csv.
Usage: python3 -I analysis/scripts/new_feature_verdicts.py <repo>"""
import csv, os, sys, re
R = sys.argv[1]
N = {  # (group, uin): reason for rejecting the match
 ('allocation_above_100', '104L133V01'): 'extra allocation CHARGE for small premiums, not extra allocation',
 **{('allocation_above_100', u): 'staff-only additional allocation (counted under customer-type benefits)' for u in ['111L142V01', '111L143V01', '111L144V01', '111L146V01', '111L147V01', '111L153V01']},
 **{('customer_type_boosters', u): 'clause says female lives are charged the same; not a booster' for u in ['110L111V05', '110L113V09', '110L114V05']},
 ('customer_type_boosters', '116L209V08'): 'staff policies get no loyalty booster; a restriction, not a benefit',
 **{('customer_type_boosters', u): 'premium payment through ECS only; not a booster' for u in ['130L049V05', '130L100V03']},
 ('lower_charges_online', '101L164V09'): 'match is a discontinuance charge table',
 **{('value_added_services', u): 'health services belong to a rider, not the product' for u in ['101L191V02', '109L100V06', '109L129V03', '109L142V01', '109L147V02', '109L149V01', '110L164V11']},
 **{('min_fund_termination', u): 'standard clause: policy ends when fund value reaches zero' for u in ['104L075V11', '104L082V06', '104L084V20', '104L098V06', '104L115V04', '104L121V05', '104L131V03', '104L133V01']},
 **{('death_benefit_waiver_plus_income', u): 'premium funding comes from a rider' for u in ['111L142V01', '111L143V01', '111L146V01', '111L147V01', '111L153V01']},
 ('death_benefit_waiver_plus_income', '111L144V01'): 'built-in payor waiver (counted under built-in waiver)',
 ('death_benefit_waiver_plus_income', '104L121V05'): 'unclear whether the funded premiums come from a rider; not counted',
 **{('no_mortality_charge', u): 'clause about one deduction date; product does charge for cover' for u in ['111L135V02', '111L142V01', '111L143V01', '111L146V01', '111L147V01', '111L153V01']},
 **{('no_mortality_charge', u): 'no charge only until a minor\'s risk starts (counted under delayed risk start)' for u in ['101L180V01', '101L187V04', '101L191V02']},
 ('vesting_postponement', '101L192V02'): 'match is a definition of the accumulation period',
 ('builtin_accident_or_payor_waiver', '111L144V01'): None,  # keep (Y)
 **{('builtin_accident_or_payor_waiver', u): '"Family Benefit" is a discount for relatives of existing customers (counted under customer-type benefits)' for u in ['116L202V01', '116L204V01', '116L207V02', '116L213V02', '116L215V01', '116L218V01']},
 ('women_life_event_cover', '104L128V01'): 'match is an exclusion clause',
 ('women_life_event_cover', '110L182V09'): 'match is a definition in a rider or exclusion',
 ('refund_fmc_or_all_charges', '130L123V01'): 'heading says "return of all charges" but only allocation and mortality charges are returned',
 ('capital_or_vesting_guarantee', '116L211V02'): 'text says the strategy gives no guaranteed maturity benefit',
 ('capital_or_vesting_guarantee', '116L218V01'): 'text says the strategy gives no guaranteed maturity benefit',
 **{('decreasing_cover_option', u): 'alteration to increase or decrease cover (a different feature)' for u in ['110L174V02', '110L177V01', '110L182V09']},
 ('high_cover_multiple', '110L182V09'): 'match is a withdrawal amount, not a cover multiple',
 ('premium_step_up', '109L129V03'): 'match is about loyalty additions',
 ('mortality_as_ialm_share', '116L215V01'): 'plain 100% of IALM; not an age-banded share',
 **{('index_or_low_cost_funds', u): 'Nifty is the benchmark or the fund invests in index stocks; no index fund' for u in ['101L164V09', '101L180V01', '101L192V02', '512L354V01', '512L361V01']},
 **{('index_or_low_cost_funds', u): 'match is a worked hedging example' for u in ['104L075V11', '110L182V09']},
}
EXTRA = [  # features found while reviewing other groups
 ('delayed_risk_start_minor', '101L180V01', 'no mortality charge until the Risk Commencement Date (minor lives)'),
 ('delayed_risk_start_minor', '101L187V04', 'no mortality charge until the Risk Commencement Date (minor lives)'),
 ('delayed_risk_start_minor', '101L191V02', 'no mortality charge until the Risk Commencement Date (minor lives)'),
 *[('customer_type_boosters', u, 'Family Benefit: better terms for relatives of existing customers') for u in ['116L202V01', '116L204V01', '116L207V02', '116L213V02', '116L215V01', '116L218V01']],
]
rows = list(csv.DictReader(open(os.path.join(R, 'analysis/v3/new_feature_candidates.csv'), encoding='utf-8')))
out = []
for r in rows:
    reason = N.get((r['group'], r['uin']))
    out.append({**r, 'verdict': 'N' if reason else 'Y', 'reason': reason or 'read by S1: the text describes this feature in the product'})
cand = {(r['group'], r['uin']): r for r in rows}
for g, u, why in EXTRA:
    src = cand.get(('no_mortality_charge', u)) or cand.get(('builtin_accident_or_payor_waiver', u)) or {}
    out = [o for o in out if not (o['group'] == g and o['uin'] == u)]
    out.append({'uin': u, 'group': g, 'matches': src.get('matches', ''), 'doc': src.get('doc', ''), 'page': src.get('page', ''), 'snippet': src.get('snippet', ''), 'verdict': 'Y', 'reason': why})
with open(os.path.join(R, 'analysis/v3/new_feature_verdicts.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, ['uin', 'group', 'verdict', 'reason', 'matches', 'doc', 'page', 'snippet']); w.writeheader(); w.writerows(out)
import collections as C
print(C.Counter(o['verdict'] for o in out)); print(sorted(C.Counter(o['group'] for o in out if o['verdict'] == 'Y').items()))
