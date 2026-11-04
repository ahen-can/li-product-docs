import sys; sys.path.insert(0, 'scripts'); sys.path.insert(0, 'scripts/ulip_specs')
from ulip_json import F, NS, build
import axis_funds
P, B = 'Policy Contract', 'Prospectus'
parsed = axis_funds.parse('104L084V20')
extra = [('BSE 500 Value 50 Index Fund II', None, 1.35), ('India Sector Leaders Opportunities Fund', None, 1.35), ('Rising India Manufacturing Fund', 'ULIF05007/09/26RISINGINDM104', 1.35), ('Flexi Cap Fund', None, 1.35), ('Secure Plus Fund', None, 0.90)]
FUNDS = [dict(f, asset_allocation='see prospectus fund table', risk_label=None) for f in parsed] + [{'name': n, 'SFIN': s, 'FMC_pct': v, 'asset_allocation': 'see prospectus fund table', 'risk_label': None} for n, s, v in extra if n not in [f['name'] for f in parsed]]
RIDERS = ['Axis Max Life Critical Illness and Disability Secure Rider (104A034V02)', 'Axis Max Life Smart Ultra Protect Rider (104A049V03)']
spec = {
 'product': {
  'uin': F('104L084V20', 'n/a', P, None, 'UIN: 104L084V20'),
  'uin_in_brochure': F('104L084V20', 'n/a', B, None, 'UIN: 104L084V20'),
  'product_name': F('Axis Max Life Shiksha Plus Super', 'n/a', B, None, 'AXIS MAX LIFE SHIKSHA PLUS SUPER AT A GLANCE'),
  'irdai_description_line': F('A Unit-Linked Non-Participating Individual Life Insurance Plan', 'n/a', B, None, 'A Unit-Linked Non-Participating Individual Life Insurance Plan'),
  'launch_or_version_date': NS(),
  'target_segment_stated': F('parents: the policyholder must have a child aged 0 days to 18 years (own or legally adopted)', 'n/a', B, None, 'The Policyholder (who shall also be the Life Insured) should have'),
  'variants_or_plan_options': F(['5 Pay (10-year term)', 'Regular Pay (15 to 25 year term)'], 'optional (at inception)', B, None, '5 years (5 Pay) / 15 to 25 years (Regular Pay)'),
  'online_offline': NS(),
 },
 'eligibility': {
  'entry_age_min': F(21, 'n/a', B, None, 'Minimum 21 years'),
  'entry_age_max': F(47, 'n/a', B, None, 'Maximum 47 years'),
  'maturity_age_min': NS(),
  'maturity_age_max': F({'5 pay': 57, 'regular pay': 65}, 'n/a', B, None, '5 Pay Variant 57 years', quote_2='Regular Pay Variant 65 years'),
  'policy_term_options': F({'5 pay': 10, 'regular pay': '15 to 25'}, 'n/a', B, None, '5 Pay Variant 10 year Policy Term', quote_2='Regular Pay Variant 15 to 25 year Policy Term'),
  'ppt_options': F({'5 pay': 5, 'regular pay': '15 to 25'}, 'n/a', B, None, '5 years (5 Pay) / 15 to 25 years (Regular Pay)'),
  'premium_min_annual': F({'5 pay': 250000, 'regular pay': 250000}, 'n/a', B, None, 'Minimum Annualised Premium 5 Pay Rs 2,50,000', quote_2='Regular Pay Rs 2,50,000 for all modes'),
  'premium_min_single': NS(),
  'premium_max': F('no limit', 'n/a', B, None, 'Maximum Annualised Premium No Limit'),
  'sum_assured_rule': F({'multiple': '7 or 10 x annualised premium', 'minimum sum assured': 1750000}, 'built-in', B, None, 'Sum Assured Multiple 7 or 10', quote_2='Rs 17,50,000 (for both'),
  'premium_modes': F('annual, semi-annual, quarterly, monthly', 'n/a', B, None, 'Premium Payment Mode Annual, Semi-annual, Quarterly, Monthly'),
  'life_cover_multiple_choice': F('7 or 10 times annualised premium', 'optional (at inception)', B, None, 'Sum Assured Multiple 7 or 10'),
 },
 'charges': {
  'premium_allocation_charge': F({'5 pay': {'Y1': '5%', 'Y2': '4%', 'Y3-5': '3%'}, 'regular pay': {'Y1': '5%', 'Y2': '4%', 'Y3-10': '3%', 'Y11+': '0%'}}, 'built-in', B, None, '1 5% 5%', 'table on prospectus pp.21-22', quote_2='2 4% 4% 3-5 3% 3% 6 - 10 NA 3% 11 & above NA 0%'),
  'policy_administration_charge': F({'annual mode': '0.32% a month of annualised premium, compounding 5% a year from year 6, cap Rs 500 a month', 'non-annual modes': '0.22% a month, compounding 5% a year from year 6, cap Rs 500 a month'}, 'built-in', B, None,
                                    '0.32% p.m. compounding at 5% per annum from sixth Policy year', quote_2='0.22% p.m. compounding at 5% per annum from sixth Policy year'),
  'fund_management_charge': F({'1.35%': 'BSE Dividend Stability Index, BSE 500 Value 50 Index II, India Sector Leaders Opportunities, Rising India Manufacturing, Flexi Cap', '1.25%': 'other equity, index and thematic funds', '1.10%': 'Balanced Fund', '1.00%': 'Nifty Smallcap Quality Index Fund', '0.90%': 'Conservative, Secure and Secure Plus', '0.50%': 'Discontinuance Policy Fund'}, 'built-in', B, None,
                              'Balanced Fund (SFIN: ULIF00225/06/04LIFEBALANC104) 1.10%', 'full list in the funds group', quote_2='Conservative Fund (SFIN: ULIF00325/06/04LIFECONSER104) 0.90%', quote_3='Secure Plus Fund (only available with Systematic Transfer Plan) 0.90%'),
  'mortality_charge': F({'basis': 'unisex rate per 1,000 sum at risk on attained age', 'sum at risk': 'higher of sum assured, 105% of premiums paid and 0.5 x term x annualised premium, plus present value of family income and funded premiums at 6.5%', 'sample_rates': {'age 25': 0.98, 'age 30': 1.06, 'age 35': 1.28, 'age 40': 1.80, 'age 45': 2.87, 'age 50': 4.95}}, 'built-in', B, None,
                        'Age Risk) 25 0.98 30 1.06 35 1.28 40 1.80 45 2.87 50 4.95', 'sample ages; the Policy Contract p.21 prints the attained-age table'),
  'discontinuance_charge': F({'annualised premium above Rs 50,000': {'Y1': 'lower of 6% of annualised premium, 6% of fund value, Rs 6,000', 'Y2': '4%, Rs 5,000', 'Y3': '3%, Rs 4,000', 'Y4': '2%, Rs 2,000', 'Y5+': 'nil'}, 'annualised premium up to Rs 50,000': {'Y1': '20%, Rs 3,000', 'Y2': '15%, Rs 2,000', 'Y3': '10%, Rs 1,500', 'Y4': '5%, Rs 1,000', 'Y5+': 'nil'}}, 'built-in', B, None,
                             '1 Lower of 6% of Annualised Premium or 6% of Fund Value or ` 6,000', 'prospectus pp.23-24', quote_2='2 Lower of 4% of Annualised Premium or 4% of Fund Value or ` 5,000 3 Lower of 3% of Annualised Premium or 3% of Fund Value or ` 4,000',
                             quote_3='4 Lower of 2% of Annualised Premium or 2% of Fund Value or ` 2,000 5 & Above Nil', quote_4='1 Lower of 20% of annualised premium or 20% of Fund Value or ` 3,000'),
  'switching_charge': F('nil; 12 free switches a year', 'built-in', B, None, 'Maximum of twelve (12) Switches are allowed in a Policy Year and they are free of charge.'),
  'partial_withdrawal_charge': F('nil', 'built-in', B, None, 'There is no charge on Partial Withdrawals.'),
  'premium_redirection_charge': F('nil; up to 6 a year', 'built-in', B, None, 'A maximum of six (6) Premium Redirections are allowed in a Policy year and all are free of charge.'),
  'miscellaneous_charge': NS(), 'guarantee_charge': NS(), 'rider_charges': NS(), 'any_charge_returned': F(None, 'not offered', note='no return of charges'),
 },
 'benefits': {
  'death_benefit_formula': F('lump sum of the higher of sum assured, 105% of premiums paid and 0.5 x term x annualised premium; plus Family Income Benefit of 10% of sum assured on each policy anniversary (max 10, min 3 payments); plus the company funds all future premiums and pays the fund value at maturity', 'built-in', B, None,
                             'Higher of [Sum Assured or 105% of the total premiums paid till the date of death or (0.5 times Policy Term times Annualised Premium)] shall be payable immediately on death.', quote_2='A Family Income Benefit equal to 10% of the Sum Assured will be paid on each Policy', quote_3='Funding of Premium (FOP) - Under this Benefit, the Company will fund all future outstanding'),
  'maturity_benefit': F('fund value at maturity; settlement option', 'built-in', B, None, 'equal to the Fund Value, where the Fund Value will be calculated as:'),
  'loyalty_additions': F({'rate': '0.20% of fund value at the end of each policy year from year 11, rising 0.02% (absolute) a year', 'applies': 'regular pay variant, premium-paying policies and policies where the company funds premiums after death'}, 'built-in', B, None,
                         '0.20% of Fund Value shall be added to the Fund by creation of additional Units, at the end of every Policy year starting from 11th Policy year.', quote_2='It should be noted that the loyalty additions are only payable in case of Regular Pay variant.'),
  'wealth_boosters_or_guaranteed_additions': NS(), 'return_of_mortality_charges': NS(), 'return_of_premium_allocation_charges': NS(), 'return_of_policy_admin_charges': NS(), 'other_additions': NS(),
 },
 'flexibility': {
  'fund_switching': F('12 free switches a year; minimum Rs 5,000', 'optional (during term)', B, None, 'subject to a minimum Switch amount of ` 5,000.'),
  'premium_redirection': F('up to 6 free redirections a year', 'optional (during term)', B, None, 'A maximum of six (6) Premium Redirections are allowed in a Policy year and all are free of charge.'),
  'partial_withdrawals': F({'from': 'after 5 policy years', 'frequency': 'up to 2 a year', 'minimum': 'Rs 5,000', 'maximum': '50% of fund value in a policy year; fund must stay at least one annualised premium'}, 'optional (during term)', B, None,
                           'a maximum of two Partial Withdrawals are allowed in a Policy year.', quote_2='is ` 5,000. In a policy year, the maximum amount that can be partially withdrawn is 50%'),
  'systematic_withdrawal_plan': NS(), 'top_up_premiums': F('not available', 'n/a', B, None, 'Top Up Not available in this plan'),
  'settlement_option': NS(), 'premium_holiday_or_offset': NS(),
  'increase_decrease_cover': F('reduce premium by up to 50% after the 5-year lock-in, once; sum assured, family income and funded premiums fall in proportion', 'optional (during term)', B, None, 'The policyholder has an option to decrease the premium up to 50% of the original'),
  'change_ppt_or_term': NS(), 'policy_loan': F('not available', 'n/a', B, None, 'Policy Loan Not available in this plan'),
  'auto_portfolio_strategies': F([{'name': 'Systematic Transfer Plan', 'mechanics': 'Secure Plus Fund transfers into growth funds'}, {'name': 'Dynamic Fund Allocation', 'mechanics': 'Growth Super Fund and Secure Fund in a split that moves to Secure Fund as maturity nears: 70/30 with 8 to 10 years left, 50/50, 30/70 with 0 to 3 years left'}], 'optional (at inception)', B, None,
                                 '8 - 10 years 70% 30% 4 - 7 years 50% 50% 0 - 3 years 30% 70%'),
 },
 'funds': {
  'fund_count': F(len(FUNDS) - 1, 'n/a', note='count from the prospectus charge table, excluding the Discontinuance Policy Fund'),
  'fund_list': F(FUNDS, 'n/a', B, None, 'Balanced Fund (SFIN: ULIF00225/06/04LIFEBALANC104) 1.10%', 'name, SFIN and FMC from the prospectus charge table; some funds print no SFIN in this table'),
  'index_or_thematic_funds': F('Midcap Momentum Index, Nifty Alpha 50, Nifty 500 Momentum 50, Nifty Momentum Quality 50, Sustainable Wealth 50 Index, Nifty 500 Multifactor 50 Index, BSE 500 Value 50 Index, BSE 500 Dividend Leaders 50 Index, BSE Dividend Stability Index, Nifty Smallcap Quality Index funds', 'n/a', B, None, 'BSE Dividend Stability Index Fund (SFIN: 1.35%'),
  'discontinued_policy_fund': F({'name': 'Discontinuance Policy Fund', 'SFIN': 'ULIF02021/06/13LIFEDISCON104', 'FMC': '0.50%'}, 'built-in', B, None, 'Discontinuance Policy Fund (SFIN:'),
 },
 'protection_add_ons': {
  'waiver_of_premium_inbuilt': F('the company funds all future premiums after the death of the life insured', 'built-in', B, None, 'Funding of Premium (FOP) - Under this Benefit, the Company will fund all future outstanding'),
  'critical_illness': F('via rider', 'rider', B, None, 'Axis Max Life Critical Illness and Disability Secure Rider (UIN: 104A034V02)'),
  'accidental_death': F('via rider (Smart Ultra Protect, variants 2 and 3)', 'rider', B, None, 'Rider benefit variant 2 - Accidental Death Benefit'),
  'terminal_illness': F('via rider (Smart Ultra Protect, variant 1)', 'rider', B, None, 'Term Booster with Accelerated Terminal Illness'),
  'spouse_or_child_cover': NS(),
  'riders_available': F(RIDERS, 'rider', B, None, 'Axis Max Life Smart Ultra Protect Rider (UIN: 104A049V03)'),
 },
 'surrender_revival': {'lock_in_years': F(5, 'built-in', B, None, 'No Partial Withdrawals are allowed in the first five Policy years'), 'discontinuance_rules': NS(), 'revival_period': NS(), 'surrender_value_rule': NS()},
}
build('104L084V20', spec,
  new_features=[{'feature': 'Family Income Benefit plus funded premiums', 'description': 'On the parent\'s death: lump sum, 10% of sum assured on each anniversary (3 to 10 times), and the company pays all future premiums', 'quote': 'A Family Income Benefit equal to 10% of the Sum Assured will be paid on each Policy', 'doc': B, 'page': None},
                {'feature': 'Child-linked eligibility', 'description': 'Policyholder must have a child aged 0 to 18 (self-declaration)', 'quote': 'The Policyholder (who shall also be the Life Insured) should have', 'doc': B, 'page': None}],
  not_public=[])
