import sys; sys.path.insert(0, 'scripts'); sys.path.insert(0, 'scripts/ulip_specs')
from ulip_json import F, NS, build
from ageas_common import funds, mortality
B = 'Prospectus'
P = 'Sample Policy Document'
MORT = mortality('text/ageas-federal/135L047V06/policy.txt', 'The mortality rates are as given in the following table')
DIS = mortality('text/ageas-federal/135L047V06/policy.txt', 'The disability rates are as under')
FMC = {k: 1.35 for k in ['Equity Growth Fund', 'Midcap Fund', 'Multicap Fund', 'Enhanced Value Fund', 'Bond Fund', 'Income Fund', 'Pure Fund', 'Aggressive Asset Allocator Fund', 'Moderate Asset Allocator Fund', 'Cautious Asset Allocator Fund', 'Large Cap Quality Fund', 'IndiGenius Fund']}
RISK = {'Equity Growth Fund': 'returns likely high, risk high', 'Midcap Fund': 'returns likely high, risk high', 'Multicap Fund': 'risk moderate to high', 'Enhanced Value Fund': 'returns likely high, risk high',
        'Bond Fund': 'returns likely moderate, risk moderate', 'Income Fund': 'returns related to short-term rates, risk low', 'Pure Fund': 'returns likely high, risk high', 'Aggressive Asset Allocator Fund': 'returns high, risk high',
        'Moderate Asset Allocator Fund': 'returns high, risk high, lower than Aggressive', 'Large Cap Quality Fund': 'returns likely high, risk high', 'IndiGenius Fund': 'returns likely high, risk high'}
ALLOC = {'Equity Growth Fund': 'equity 50-100%, cash and money market 0-50%', 'Midcap Fund': 'mid cap stocks 50-100%, large cap 0-50%, cash and money market 0-50%', 'Multicap Fund': 'equity 50-100%, cash and money market 0-50%',
         'Enhanced Value Fund': 'equity 90-100%, cash and money market 0-10%', 'Bond Fund': 'fixed income 20-100%, cash and money market 0-80%', 'Income Fund': 'fixed income 25-100%, cash and money market 0-75%',
         'Pure Fund': 'equity 80-100%, cash and money market 0-20%', 'Aggressive Asset Allocator Fund': 'equity 50-100%, money market 0-50%, fixed income 0-50%',
         'Moderate Asset Allocator Fund': 'fixed income 50-100%, money market 0-50%, equity 0-50%', 'Cautious Asset Allocator Fund': 'fixed income 75-100%'}
spec = {
 'product': {
  'uin': F('135L047V06', 'n/a', B, None, 'Product UIN No. 135L047V06.'),
  'uin_in_brochure': F('135L047V06', 'n/a', B, None, 'Product UIN No. 135L047V06.'),
  'product_name': F('Ageas Federal Life Insurance Wealth Gain Insurance Plan', 'n/a', B, None, 'Ageas Federal Wealth Gain Insurance Plan'),
  'irdai_description_line': F('Unit Linked, Non-Participating, Individual Life Insurance Plan', 'n/a', B, None, 'Unit Linked, Non-Participating, Individual Life Insurance Plan'),
  'launch_or_version_date': NS(), 'target_segment_stated': NS(), 'variants_or_plan_options': NS(),
  'online_offline': F('also sold online, at a lower allocation and administration charge', 'n/a', B, None, 'If you buy this plan Online (also applicable for staff'),
 },
 'eligibility': {
  'entry_age_min': F(5, 'n/a', B, None, 'Age at entry 5 years 60 years (as on last birthday)'),
  'entry_age_max': F(60, 'n/a', B, None, 'Age at entry 5 years 60 years (as on last birthday)'),
  'maturity_age_min': F(18, 'n/a', B, None, 'Age at maturity of plan 18 years 74 years (as on last birthday)'),
  'maturity_age_max': F(74, 'n/a', B, None, 'Age at maturity of plan 18 years 74 years (as on last birthday)'),
  'policy_term_options': F('10, 15 or 20 years', 'n/a', B, None, 'Policy Term (PT) 10 / 15 / 20 years'),
  'ppt_options': F({'age below 50': '5, 10, 15 or 20 years', 'age 50 and above': '10, 15 or 20 years'}, 'n/a', B, None, 'For ages below 50 years : 5 / 10 / 15/ 20 years', quote_2='For age 50 years and above : 10 / 15/ 20 years'),
  'premium_min_annual': F({'yearly': 30000, 'monthly': 2500}, 'n/a', B, None, 'Yearly – Rs. 30,000', quote_2='Monthly – Rs. 2,500'),
  'premium_min_single': F(None, 'not offered', note='regular and limited pay only'),
  'premium_max': F({'yearly, PPT 5 or 10': '10,00,000 a year', 'yearly, PPT 15 or 20': '6,00,000 a year', 'monthly, PPT 5 or 10': '83,000 a month', 'monthly, PPT 15 or 20': '50,000 a month'}, 'n/a', B, None,
                   '5, 10 10,00,000 p.a.', quote_2='15, 20 6,00,000 p.a.', quote_3='5, 10 83,000 p.m.', quote_4='15, 20 50,000 p.m.'),
  'sum_assured_rule': F('death sum assured is the higher of 10 times the annualized premium and 0.5 x policy term x annualized premium', 'built-in', B, None, '10 times the Annualized Premium or', quote_2='0.5 x Policy Term x Annualized Premium'),
  'premium_modes': F(['annual', 'monthly'], 'n/a', B, None, 'Premium Payment Frequency (PPF) Monthly and Annually'),
  'life_cover_multiple_choice': F(None, 'not offered', note='the death sum assured follows from the premium and policy term'),
 },
 'charges': {
  'premium_allocation_charge': F({'regular': {'policy year 1': '3.00%', 'policy years 2 to 5': '1.50%', 'policy year 6 onwards': '1.00%'}, 'online and staff': {'policy years 1 to 5': '1.50%', 'policy year 6 onwards': '1.00%'}}, 'built-in', B, None,
                                 '1 3.00%', quote_2='2-5 1.50%', quote_3='6+ 1.00%'),
  'policy_administration_charge': F({'regular': '3.5% of annual premium a year throughout the term', 'online and staff': '1.75% a year throughout the term', 'cap': 'Rs 500 a month'}, 'built-in', B, None,
                                    'premium is 3.5% p.a. throughout the policy term', quote_2='premium will be 1.75% p.a. throughout the policy term', quote_3='maximum of Rs.500 per month'),
  'fund_management_charge': F({k: f'{v:.2f}%' for k, v in FMC.items()} | {'Discontinued Policy Fund': '0.50%'}, 'built-in', B, None, 'Fund management charges are 1.35% p.a. for all the investment funds available.', quote_2='Fund Management Charge: 0.50% p.a.'),
  'mortality_charge': F({'basis': '1/12 of the annual rate per 1,000 sum at risk, by age and gender; female lives get a discount', 'rate_per_1000_sum_at_risk_by_age': {'male': MORT['male'], 'female': MORT['female']}}, 'built-in', P, None,
                        '5 1.16 2.68 32 1.19 1.09 59 11.57 9.24', 'full table from the policy document; the table prints no row for age 61 and ends at age 79', quote_2='17 0.80 0.60 44 2.84 2.13 72 33.32 25.79'),
  'discontinuance_charge': F({'annualized premium up to Rs 50,000': {'Y1': 'lower of 20% of AP or FV, max Rs 3,000', 'Y2': '15%, Rs 2,000', 'Y3': '10%, Rs 1,500', 'Y4': '5%, Rs 1,000', 'Y5+': 'nil'},
                              'annualized premium above Rs 50,000': {'Y1': 'lower of 6%, max Rs 6,000', 'Y2': '4%, Rs 5,000', 'Y3': '3%, Rs 4,000', 'Y4': '2%, Rs 2,000', 'Y5+': 'nil'}}, 'built-in', B, None,
                             'Lower of 20%* (AP or FV) subject to a Lower of 6%* (AP or FV) subject to a', quote_2='Lower of 15%* (AP or FV) subject to a Lower of 4%* (AP or FV) subject to a', quote_3='Lower of 10%* (AP or FV) subject to a Lower of 3%* (AP or FV) subject to a', quote_4='Lower of 5%* (AP or FV) subject to a Lower of 2%* (AP or FV) subject to a'),
  'switching_charge': F('nil', 'built-in', B, None, 'switch between funds any number of times free of charge'),
  'partial_withdrawal_charge': NS(), 'premium_redirection_charge': NS(),
  'miscellaneous_charge': F({'name': 'Waiver of premium on disability charge', 'basis': '1/12 of the annual rate per 1,000 of outstanding future premiums, by age and gender; none after the premium paying term or once disability is reported', 'rate_per_1000_by_age': {'male': DIS['male'], 'female': DIS['female']}}, 'built-in', P, None,
                            '20 0.21 0.21 41 0.29 0.23 62 4.43 3.10', 'full table from the policy document, ages 18 to 74', quote_2='33 0.20 0.19 54 1.53 1.00'),
  'guarantee_charge': NS(), 'rider_charges': NS(), 'any_charge_returned': NS(),
 },
 'benefits': {
  'death_benefit_formula': F('higher of death sum assured, fund value and 105% of premiums paid; the sum assured is reduced by withdrawals in the 2 years before death', 'built-in', B, None, '105% of the Total Premiums paid till the date of', quote_2='The Death Benefit is higher of Death Sum Assured or'),
  'maturity_benefit': F('fund value including guaranteed loyalty additions at maturity', 'built-in', B, None, 'Maturity benefit is equal to the fund value including'),
  'loyalty_additions': F({'name': 'Guaranteed Loyalty Additions', 'rate': '1% of the average fund value in the last 36 months', 'timing': 'end of the 10th policy year and every 5 years after'}, 'built-in', B, None,
                         'This is 1% of', quote_2='guaranteed loyalty additions at the end of the 10th'),
  'wealth_boosters_or_guaranteed_additions': NS(),
  'return_of_mortality_charges': NS(), 'return_of_premium_allocation_charges': NS(), 'return_of_policy_admin_charges': NS(), 'other_additions': NS(),
 },
 'flexibility': {
  'fund_switching': F('free and unlimited', 'optional (during term)', B, None, 'switch between funds any number of times free of charge'),
  'premium_redirection': F('premium redirection is offered; the brochure gives no rules', 'optional (during term)', B, None, 'redirect premiums to maximize returns as per your'),
  'partial_withdrawals': F({'from': 'after the 5-year lock-in', 'maximum': '20% of the fund value at the start of the policy year, each year', 'minimum': 'Rs 10,000, leaving at least one year of annualized premium in the fund'}, 'optional (during term)', B, None,
                           'cannot exceed 20% of the fund value at the', quote_2='The minimum amount of a partial withdrawal is', note='the brochure states the Rs 10,000 minimum in the line quoted'),
  'systematic_withdrawal_plan': NS(), 'top_up_premiums': NS(),
  'settlement_option': F('maturity proceeds paid in annual instalments over 2 to 5 years', 'optional (during term)', B, None, 'Settlement period can range from two to five years.'),
  'premium_holiday_or_offset': NS(), 'increase_decrease_cover': NS(), 'change_ppt_or_term': NS(), 'policy_loan': NS(),
  'auto_portfolio_strategies': F([{'name': 'Leave-it-to-us', 'mechanics': 'the company manages the mix at a risk level chosen from Cautious, Moderate or Aggressive'},
                                  {'name': 'Systematic Allocator', 'mechanics': 'moves from Equity Growth Fund to income funds as maturity nears: 80% equity with 15 or more years left, 5% with 1 year left'}], 'optional (at inception)', B, None,
                                 'Cautious, Moderate and Aggressive', quote_2='15 and above 80.00% 20.00%'),
 },
 'funds': {
  'fund_count': F(12, 'n/a', B, None, 'Choose from the 12 fund options available'),
  'fund_list': F(funds(FMC, RISK, ALLOC), 'n/a', B, None, 'SFIN: ULIF04111/01/08EQOPP135', 'SFINs as printed; FMCs from the charges section. Asset allocation for the Cautious Asset Allocator, Large Cap Quality and IndiGenius funds is not copied, see the brochure fund table; the Cautious fund shows only its fixed income range', quote_2='SFIN: ULIF04011/01/08BOND135'),
  'index_or_thematic_funds': F('Large Cap Quality Fund, Enhanced Value Fund, IndiGenius Fund, Pure Fund', 'n/a', B, None, 'ULIF083071125ENVF135', quote_2='ULIF088010326LARGEQLTY135', quote_3='ULIF08901/07/26INDIGENIUS135'),
  'discontinued_policy_fund': F({'name': 'Discontinued Policy Fund', 'fmc': '0.50%', 'guaranteed rate': '4% a year'}, 'built-in', B, None, 'Fund Management Charge: 0.50% p.a.', quote_2='minimum guaranteed interest rate of 4% p.a.'),
 },
 'protection_add_ons': {'waiver_of_premium_inbuilt': F('on total and permanent disability during the premium paying term the company pays future premiums, life cover continues and loyalty additions continue', 'built-in', B, None, 'Waiver of Premium on Disability', quote_2='Future premiums will be paid by the company on'),
                        'critical_illness': F('Ageas Federal Life Insurance Linked Critical Shield Rider (UIN 135A038V01)', 'rider', B, None, '135A038V01'),
                        'accidental_death': F('Ageas Federal Life Insurance Linked Accident Care Rider (UIN 135A036V01)', 'rider', B, None, '135A036V01'),
                        'terminal_illness': NS(), 'spouse_or_child_cover': NS(),
                        'riders_available': F(['Ageas Federal Life Insurance Linked Accident Care Rider, UIN 135A036V01', 'Ageas Federal Life Insurance Linked Critical Shield Rider, UIN 135A038V01'], 'rider', B, None, '135A036V01', quote_2='135A038V01')},
 'surrender_revival': {
  'lock_in_years': F(5, 'built-in', B, None, 'completely or partially until the end of the fifth year.'),
  'discontinuance_rules': NS(), 'revival_period': NS(),
  'surrender_value_rule': F('after the lock-in, at least the unit fund value on the surrender date', 'built-in', B, None, 'the surrender value shall be at least equal to the unit'),
 },
}
build('135L047V06', spec,
  new_features=[{'feature': 'Waiver of premium on total and permanent disability', 'description': 'Built in: on disability the company pays future premiums, cover and loyalty additions continue, with a separate disability charge', 'quote': 'Waiver of Premium on Disability', 'doc': B, 'page': None},
                {'feature': 'Leave-it-to-us risk levels', 'description': 'The company manages the fund mix at a Cautious, Moderate or Aggressive level', 'quote': 'Cautious, Moderate and Aggressive', 'doc': B, 'page': None}],
  not_public=[])
