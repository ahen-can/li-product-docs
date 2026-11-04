"""Write calc/params/ulip/<UIN>.json for the pilot ULIPs. Charges and additions are typed in from
features/ulip/<UIN>.json (deep discovery, quote-validated); mortality rates come from the policy text
via extract_mortality.py. Usage: python3 -I calc/tools/make_ulip_params.py <repo>"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract_mortality import extract
R = sys.argv[1]
STD = {'age': 30, 'ap': 100000, 'ppt': 10, 'pt': 20}
P = {
 '130L100V03': dict(product='Bharti AXA Life Wealth Pro', slug='bharti-life', variant_used='Growth variant, other channels (not online), annual mode, equity fund',
   sum_assured_multiple=10, fmc_pct=1.35, allocation_charge_pct=[[1, 1, 9.0], [2, 2, 7.0], [3, 3, 5.0], [4, 4, 3.0], [5, None, 2.0]],
   admin={'basis': 'pct_ap', 'schedule': [[1, 5, 0.15], [6, 10, 0.45], [11, None, 0.0]], 'cap_per_month': 500},
   additions=[{'name': 'Wealth Booster yr 5', 'type': 'pct_fv_end_of_year', 'years': [5], 'pct': 0.25},
              {'name': 'Wealth Booster at maturity', 'type': 'pct_fv_at_maturity_before_refunds', 'pct': 1.25},
              {'name': 'Return of mortality + allocation charges', 'type': 'refund_at_maturity', 'charges': ['mort', 'pac']}],
   sources='Policy Bond p.13 (allocation, admin, FMC, mortality basis), p.3-4 (boosters, RoMC, RoPAC), p.2-3 (eligibility, 10x AP cover)'),
 '130L128V01': dict(product='Bharti AXA Life Grow Wealth Ultra', slug='bharti-life', variant_used='Plan Option 2 Wealth Plan, limited pay, death benefit multiple 10, equity fund; EmpowHer, ECS and existing-customer boosters not applied',
   sum_assured_multiple=10, fmc_pct=1.35, allocation_charge_pct=[],
   admin={'basis': 'pct_ap', 'schedule': [[1, 5, 0.51], [6, 10, 0.26], [11, None, 0.10]], 'cap_per_month': 500},
   additions=[{'name': 'Loyalty Booster 5% of 60-month average fund', 'type': 'pct_avg_fv', 'years': [20], 'avg_months': 60, 'pct': 5.0},
              {'name': 'Return of allocation, admin and mortality charges', 'type': 'refund_at_maturity', 'charges': ['pac', 'admin', 'mort']}],
   standard_profile={**STD, 'ap': 250000}, note='Minimum annual premium is Rs 2,50,000, so the standard profile uses that instead of Rs 1,00,000.',
   sources='Policy Bond p.18 (admin table), p.18-19 (FMC), p.20 (mortality basis), p.5-6 (Loyalty Booster, refunds of charges); brochure p.2-3 (eligibility, minimum premium)'),
 '130L121V01': dict(product='Bharti AXA Life Wealth Maximizer', slug='bharti-life', variant_used='Limited pay 10, policy term 20, equity fund',
   sum_assured_multiple=10, fmc_pct=1.35, allocation_charge_pct=[[1, 1, 2.0], [2, 3, 6.0], [4, 6, 5.5], [7, 8, 4.5], [9, 10, 3.5]],
   admin={'basis': 'pct_ap', 'schedule': [[1, None, 0.0625]], 'cap_per_month': 500},
   additions=[{'name': 'Loyalty Addition 0.20% of fund each year after premium term', 'type': 'pct_fv_end_of_year', 'years': list(range(11, 21)), 'pct': 0.20},
              {'name': 'Refund of 118% of all charges of the premium term, over 5 years', 'type': 'refund_spread', 'years': [11, 12, 13, 14, 15], 'scope': 'ppt', 'charges': ['pac', 'admin', 'mort', 'fmc'], 'multiple': 1.18}],
   sources='Policy Bond p.11 (allocation, admin), p.12 (FMC, mortality), p.3 (118% refund, loyalty additions), p.2 (eligibility, 10x AP)'),
 '111L147V01': dict(product='SBI Life eWealth Plus', slug='sbi-life', variant_used='Active Strategy, Equity fund, limited pay 10, policy term 20',
   sum_assured_multiple=10, fmc_pct=1.35, allocation_charge_pct=[],
   admin={'basis': 'flat', 'schedule': [[1, None, 100.0]], 'cap_per_month': 500},
   additions=[], sources='Policy Document p.39 (allocation nil, admin Rs 100 a month), p.40 (FMC), p.41-42 (mortality table), p.5 (eligibility, 10x AP)'),
 '101L133V03': dict(product='HDFC Life Click 2 Wealth', slug='hdfc-life', variant_used='Invest Plus Option, limited pay 10, equity fund, cover 10x AP (minimum is 7x)',
   sum_assured_multiple=10, fmc_pct=1.35, allocation_charge_pct=[], admin={'basis': 'flat', 'schedule': []},
   additions=[{'name': 'Special Additions 1% of AP for 5 years', 'type': 'pct_ap_at_allocation', 'years': [1, 2, 3, 4, 5], 'pct': 1.0},
              {'name': 'Return of mortality charges at maturity', 'type': 'refund_at_maturity', 'charges': ['mort']}],
   sources='Policy Document p.19 (allocation and admin nil, FMC), Appendix 1 (mortality), p.12 (special additions, return of mortality charges); brochure p.2 (cover multiple)'),
 '101L180V01': dict(product='HDFC Life Sampoorn Nivesh Plus', slug='hdfc-life', variant_used='Classic (Life Option), limited pay 10, annual mode, premium band 2 (Rs 1 lakh to 4,99,999), equity fund, cover 10x AP; direct-channel Loyalty Reward not applied',
   sum_assured_multiple=10, fmc_pct=1.35, allocation_charge_pct=[[1, 5, 6.0], [6, None, 3.0]],
   admin={'basis': 'pct_ap', 'schedule': [[1, 5, 0.0], [6, None, 0.35]], 'escalation_pa': 0.05, 'escalation_from_year': 6, 'cap_per_month': 500},
   additions=[{'name': 'Loyalty Addition 1.2% of 12-month average fund, alternate years from year 11', 'type': 'pct_avg_fv', 'years': [11, 13, 15, 17, 19], 'avg_months': 12, 'pct': 1.2}],
   sources='Policy Document p.19 (allocation by band), p.20 (admin, FMC, mortality basis), p.11 (loyalty additions), mortality table in the appendix'),
}
for u, d in P.items():
    pol = os.path.join(R, 'text', d.pop('slug'), u, 'policy.txt')
    b = extract(pol)[0]
    d['mortality_per_1000'] = {str(k): v for k, v in b['table'].items()}
    d['mortality_source'] = f"policy.txt lines {b['lines']}, PDF page(s) {b['pages']}, ages {b['ages']} (male / unisex table, age last birthday)"
    d['uin'] = u
    d.setdefault('standard_profile', STD)
    json.dump(d, open(os.path.join(R, 'calc', 'params', 'ulip', f'{u}.json'), 'w'), indent=1)
    print(u, d['mortality_source'])
