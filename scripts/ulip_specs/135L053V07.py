import sys; sys.path.insert(0, 'scripts'); sys.path.insert(0, 'scripts/ulip_specs')
from ulip_json import F, NS, build
from ageas_common import funds, mortality
B = 'Prospectus'
P = 'Sample Policy Document'
MORT = mortality('text/ageas-federal/135L053V07/policy.txt', 'The mortality charge are as given')
FMC = {'Equity Growth Fund': 1.35, 'Midcap Fund': 1.35, 'Multicap Fund': 1.35, 'Momentum Growth Fund': 1.35, 'India Sector Leaders Fund': 1.35, 'Enhanced Value Fund': 1.35, 'Pure Fund': 1.35,
       'Aggressive Asset Allocator Fund': 1.35, 'Moderate Asset Allocator Fund': 1.35, 'Large Cap Quality Fund': 1.35, 'IndiGenius Fund': 1.35, 'Bond Fund II': 1.25}
RISK = {'Equity Growth Fund': 'returns likely high, risk high', 'Midcap Fund': 'returns likely high, risk high', 'Multicap Fund': 'risk moderate to high', 'Momentum Growth Fund': 'returns likely high, risk high',
        'India Sector Leaders Fund': 'returns likely high, risk high', 'Pure Fund': 'returns likely high, risk high', 'Bond Fund II': 'returns likely moderate, risk moderate',
        'Aggressive Asset Allocator Fund': 'returns high, risk high', 'Moderate Asset Allocator Fund': 'returns high, risk high, lower than Aggressive', 'Large Cap Quality Fund': 'returns likely high, risk high', 'IndiGenius Fund': 'returns likely high, risk high'}
ALLOC = {'Equity Growth Fund': 'equity 50-100%, cash and money market 0-50%', 'Midcap Fund': 'mid cap stocks 50-100%, large cap 0-50%, cash and money market 0-50%', 'Multicap Fund': 'equity 50-100%, cash and money market 0-50%',
         'Momentum Growth Fund': 'equity 90-100%, cash and money market 0-10%', 'India Sector Leaders Fund': 'equity 90-100%, cash and money market 0-10%', 'Enhanced Value Fund': 'equity 90-100%',
         'Pure Fund': 'equity 80-100%, cash and money market 0-20%', 'Bond Fund II': 'fixed income 50-100%, money market 0-50%', 'Aggressive Asset Allocator Fund': 'equity 50-100%, money market 0-50%, fixed income 0-50%',
         'Moderate Asset Allocator Fund': 'fixed income 50-100%, money market 0-50%, equity 0-50%', 'Large Cap Quality Fund': 'equity 80-100%, cash and money market 0-10%', 'IndiGenius Fund': 'equity 80-100%, cash and money market 0-20%'}
spec = {
 'product': {
  'uin': F('135L053V07', 'n/a', B, None, 'UIN: 135L053V07'),
  'uin_in_brochure': F('135L053V07', 'n/a', B, None, 'Product UIN: 135L053V07'),
  'product_name': F('Ageas Federal Life Insurance Smart Growth Plan', 'n/a', B, None, 'Ageas Federal Life Insurance Smart Growth Plan'),
  'irdai_description_line': F('Unit Linked, Non-Participating, Individual Life Insurance Plan', 'n/a', B, None, 'Unit Linked, Non-Participating, Individual Life Insurance Plan'),
  'launch_or_version_date': NS(), 'target_segment_stated': NS(),
  'variants_or_plan_options': F(['Option 1 - Prime', 'Option 2 - Plus'], 'n/a', B, None, 'Option 1 - Prime', quote_2='Option 2 - Plus'),
  'online_offline': F('also sold online', 'n/a', B, None, 'For staff and online sales policies:'),
 },
 'eligibility': {
  'entry_age_min': F('1 month', 'n/a', B, None, 'Age at entry 1 month#'),
  'entry_age_max': F({'Prime': 55, 'Plus': 45}, 'n/a', B, None, 'Option 1 - Prime – 55 years', quote_2='Option 2 - Plus – 45 years'),
  'maturity_age_min': F(18, 'n/a', B, None, 'Age at maturity 18 years'),
  'maturity_age_max': F({'Prime': 70, 'Plus': 60}, 'n/a', B, None, 'Option 1 - Prime – 70 years', quote_2='Option 2 - Plus – 60 years'),
  'policy_term_options': F('10, 15, 20 or 25 years', 'n/a', B, None, 'Policy Term 10/15/20/25 years'),
  'ppt_options': F({'policy term 10 and 15': '5 or 6 years', 'all policy terms': '10, 15 or 20 years'}, 'n/a', B, None, 'Policy Term 10 & 15 - 5 years & 6 years', quote_2='For all Policy Terms - 10/15/20 years'),
  'premium_min_annual': F({'PPT 5 or 6 years, annual mode': 50000, 'PPT 10, 15 or 20 years, annual mode': 35000, 'other modes': '2,25,000 a year'}, 'n/a', B, None, '₹50,000 annually', quote_2='₹35,000 annually', quote_3='₹2,25,000 p.a'),
  'premium_min_single': F(None, 'not offered', note='regular and limited pay only'),
  'premium_max': F('no limit', 'n/a', B, None, 'No Limit'),
  'sum_assured_rule': F('death sum assured is the higher of 10 times the annualized premium and 0.5 x policy term x annualized premium', 'built-in', B, None, '10 times the Annualized Premium, or', quote_2='0.5 X PT X Annualized Premium'),
  'premium_modes': F(['annual', 'semi-annual', 'monthly'], 'n/a', B, None, 'Annual/ Semi-Annual/ Monthly'),
  'life_cover_multiple_choice': F(None, 'not offered', note='the death sum assured follows from the premium and policy term'),
 },
 'charges': {
  'premium_allocation_charge': F({'policy year 1': '4.00%', 'policy years 2 to 5': '3.00%', 'policy year 6 onwards': '2.00%', 'staff and online sales': {'year 1': '0.50%', 'years 2 to 5': '0.35%', 'year 6 onwards': '0.30%'}}, 'built-in', B, None,
                                 '1 4.00%', quote_2='2-5 3.00%', quote_3='6+ 2.00%', quote_4='0.50% 0.35% 0.30%'),
  'policy_administration_charge': F({'policy years 1 to 5': '3.60% of annualized premium a year', 'policy years 6 to 10': '3.00%', 'policy year 11 onwards': '1.25%', 'cap': 'Rs 500 a month, deducted monthly in advance'}, 'built-in', B, None,
                                    '1-5 3.60%', quote_2='6-10 3.00%', quote_3='11+ 1.25%', quote_4='subject to a maximum of Rs.500'),
  'fund_management_charge': F({k: f'{v:.2f}%' for k, v in FMC.items()} | {'Discontinued Policy Fund': '0.50%'}, 'built-in', B, None, '1.35% p.a.', quote_2='Bond Fund II 1.25% p.a.', quote_3='Discontinued Policy Fund 0.50% p.a.'),
  'mortality_charge': F({'basis': '1/12 of the annual rate per 1,000 sum at risk, by attained age and gender', 'rate_per_1000_sum_at_risk_by_age': {'male': MORT['male'], 'female': MORT['female']}}, 'built-in', P, None,
                        '0 3.50 3.50 21 0.78 0.69 42 1.89 1.46 63 12.68 10.06', 'full table, ages 0 to 75, from the policy document', quote_2='12 0.39 0.39 33 1.00 0.90 54 6.36 4.84 75 34.78 26.92'),
  'discontinuance_charge': F({'annualized premium up to Rs 50,000': {'Y1': 'lower of 20% of AP or FV, max Rs 3,000', 'Y2': '15%, Rs 2,000', 'Y3': '10%, Rs 1,500', 'Y4': '5%, Rs 1,000', 'Y5+': 'nil'},
                              'annualized premium above Rs 50,000': {'Y1': 'lower of 6%, max Rs 6,000', 'Y2': '4%, Rs 5,000', 'Y3': '3%, Rs 4,000', 'Y4': '2%, Rs 2,000', 'Y5+': 'nil'}}, 'built-in', B, None,
                             'Lower of 20%* (AP or FV) subject to a Lower of 6%* (AP or FV) subject to a', quote_2='Lower of 15%* (AP or FV) subject to a Lower of 4%* (AP or FV) subject to a', quote_3='Lower of 10%* (AP or FV) subject to a Lower of 3%* (AP or FV) subject to a', quote_4='Lower of 5%* (AP or FV) subject to a Lower of 2%* (AP or FV) subject to a'),
  'switching_charge': F('nil', 'built-in', B, None, 'switching between funds any number of times free of charge'),
  'partial_withdrawal_charge': F('nil', 'built-in', B, None, 'There is no partial withdrawal charge.'),
  'premium_redirection_charge': F('nil', 'built-in', B, None, 'Premium redirection is allowed free of charge as many times as required.'),
  'miscellaneous_charge': NS(), 'guarantee_charge': NS(), 'rider_charges': NS(), 'any_charge_returned': NS(),
 },
 'benefits': {
  'death_benefit_formula': F({'Option 1 - Prime': 'highest of death sum assured, fund value and 105% of premiums paid', 'Option 2 - Plus': 'higher of (death sum assured plus fund value) and 105% of premiums paid'}, 'built-in', B, None,
                             'Sum Assured on Death (Death Sum Assured) , or', quote_2='Sum Assured on Death (Death Sum Assured)1 plus', quote_3='105% of the total Premiums paid up to the date of'),
  'maturity_benefit': F('fund value including guaranteed loyalty additions at maturity', 'built-in', B, None, 'Fund value including Guaranteed Loyalty Additions'),
  'loyalty_additions': F({'name': 'Guaranteed Loyalty Additions', 'rate': '0.5% of the average fund value over the last 36 months', 'timing': 'end of the 10th policy year and every 5 years after, including the last policy year'}, 'built-in', B, None,
                         'Guaranteed Loyalty Additions will be 0.5% of the average fund value over the last 36 months', quote_2='at the end of the 10th policy'),
  'wealth_boosters_or_guaranteed_additions': NS(),
  'return_of_mortality_charges': NS(), 'return_of_premium_allocation_charges': NS(), 'return_of_policy_admin_charges': NS(), 'other_additions': NS(),
 },
 'flexibility': {
  'fund_switching': F('free and unlimited', 'optional (during term)', B, None, 'switching between funds any number of times free of charge'),
  'premium_redirection': F('free, any number of times; at least 15% of the annualized premium in any fund', 'optional (during term)', B, None, 'Premium redirection is allowed free of charge as many times as required.', quote_2='should be at least 15% of the Annualized Premium'),
  'partial_withdrawals': F({'from': 'after the 5-year lock-in', 'maximum': '20% of the fund value at the start of the policy year, each year', 'minimum': 'Rs 10,000, leaving at least one annualized premium in the fund'}, 'optional (during term)', B, None,
                           'not more than 20% of the Fund Value as at the beginning', quote_2='The minimum amount of any partial withdrawal is Rs. 10,000'),
  'systematic_withdrawal_plan': NS(), 'top_up_premiums': NS(),
  'settlement_option': F('maturity proceeds paid in instalments over 2 to 5 years', 'optional (during term)', B, None, 'maximum of 5 years from the', quote_2='at the least 3 months before the maturity date'),
  'premium_holiday_or_offset': NS(), 'increase_decrease_cover': NS(), 'change_ppt_or_term': NS(), 'policy_loan': NS(),
  'auto_portfolio_strategies': F([{'name': 'AutoSwitcher', 'mechanics': 'fixed amount switched monthly from one fund to another, at least Rs 500 for at least 6 months'},
                                  {'name': 'Systematic Allocator', 'mechanics': 'moves from Equity Growth Fund to Bond Fund II as maturity nears: 80% equity with 15 or more years left, 5% with 1 year left'}], 'optional (at inception)', B, None,
                                 'Transfer Amount ₹ 500', quote_2='15 and above 80.00% 20.00%', quote_3='1 5.00% 95.00%'),
 },
 'funds': {
  'fund_count': F(12, 'n/a', B, None, 'choose from 12 investment'),
  'fund_list': F(funds(FMC, RISK, ALLOC), 'n/a', B, None, 'ULIF04111/01/ 08EQOPP135', 'SFINs as printed in the policy document (the brochure wraps them across lines; some are printed without slashes); FMCs from the charges table; Enhanced Value Fund has no description in the brochure'),
  'index_or_thematic_funds': F('Momentum Growth Fund (Nifty 500 Momentum 50), India Sector Leaders Fund (BSE India Sector Leaders), Large Cap Quality Fund (BSE Large Cap 100 Quality 30), Pure Fund, IndiGenius Fund', 'n/a', B, None,
                               'Nifty 500 Momentum', quote_2='BSE India Sector Leaders Index', quote_3='BSE Large Cap 100 Quality 30 Index'),
  'discontinued_policy_fund': F({'name': 'Discontinued Policy Fund', 'fmc': '0.50%', 'guaranteed rate': '4% a year'}, 'built-in', B, None, 'Discontinued Policy Fund 0.50% p.a.', quote_2='4% per annum'),
 },
 'protection_add_ons': {'waiver_of_premium_inbuilt': NS(), 'critical_illness': NS(), 'accidental_death': NS(), 'terminal_illness': NS(), 'spouse_or_child_cover': NS(),
                        'riders_available': F('optional riders are offered; the brochure names none', 'rider', B, None, 'Enhance protection with Rider options')},
 'surrender_revival': {
  'lock_in_years': F(5, 'built-in', B, None, 'till the end of the fifth year'),
  'discontinuance_rules': NS(),
  'revival_period': F('3 years from the first unpaid premium', 'built-in', B, None, 'revival period of three years'),
  'surrender_value_rule': F('after the lock-in, at least the unit fund value on the surrender date; during the lock-in, the fund value less discontinuance charge goes to the Discontinued Policy Fund and is paid at the end of the lock-in', 'built-in', B, None,
                            'the surrender value shall be at least equal to the unit fund value as on'),
 },
}
build('135L053V07', spec,
  new_features=[{'feature': 'Systematic Allocator glide path', 'description': 'Moves the fund mix from Equity Growth Fund to Bond Fund II by years left to maturity', 'quote': '15 and above 80.00% 20.00%', 'doc': B, 'page': None},
                {'feature': 'AutoSwitcher', 'description': 'Programmed monthly switch of a fixed amount between funds', 'quote': 'AutoSwitcher can be used to make programmed switches every', 'doc': B, 'page': None}],
  not_public=[])
