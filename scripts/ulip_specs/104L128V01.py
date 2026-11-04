import sys; sys.path.insert(0, 'scripts'); sys.path.insert(0, 'scripts/ulip_specs')
from ulip_json import F, NS, build
import axis_funds
P, B = 'Policy Contract', 'Policy Prospectus'
# Fund names are the 31 funds listed in Step 3; FMCs come from the prospectus charge table (values per name match the other Axis prospectuses).
FMC_BY_NAME = {f['name'].lower(): f['FMC_pct'] for f in axis_funds.parse('104L082V06')}
SFIN_BY_NAME = {f['name'].lower(): f['SFIN'] for f in axis_funds.parse('104L082V06')}
NAMES = ['High Growth Fund', 'NIFTY Smallcap Quality Index Fund', 'Nifty Alpha 50 Fund', 'Nifty 500 Momentum 50 Fund', 'Midcap Momentum Index Fund', 'Nifty Momentum Quality 50 Fund', 'Sustainable Wealth 50 Index Fund', 'Smart Innovation Fund',
         'Nifty 500 Multifactor 50 Index Fund', 'BSE 500 Value 50 Index Fund', 'BSE 500 Dividend leaders 50 Index Fund', 'High Growth Fund II', 'BSE Dividend Stability Index Fund', 'India Consumption Opportunities Fund', 'Growth Super Fund II',
         'Diversified Equity Fund II', 'BSE 500 Value 50 Index Fund II', 'India Sector Leaders Opportunities Fund', 'Rising India Manufacturing Fund', 'Flexi Cap Fund', 'Diversified Equity Fund', 'Growth Super Fund', 'Growth Fund',
         'Sustainable Equity Fund', 'Pure Growth Fund', 'Balanced Fund', 'Conservative Fund', 'Dynamic Bond Fund', 'Secure Fund', 'Secure Plus Fund', 'Money Market II Fund', 'Discontinuance Policy Fund']
FUNDS = [{'name': n, 'SFIN': SFIN_BY_NAME.get(n.lower()), 'FMC_pct': FMC_BY_NAME.get(n.lower()), 'asset_allocation': 'see prospectus fund table', 'risk_label': None} for n in NAMES]
assert all(f['FMC_pct'] is not None for f in FUNDS), [f['name'] for f in FUNDS if f['FMC_pct'] is None]
RIDERS = ['Axis Max Life Critical Illness and Disability Secure Rider (104A034V02)', 'Axis Max Life Smart Ultra Protect Rider (104A049V03)']
spec = {
 'product': {
  'uin': F('104L128V01', 'n/a', P, None, 'UIN: 104L128V01'),
  'uin_in_brochure': F('104L128V01', 'n/a', B, None, 'UIN: 104L128V01'),
  'product_name': F('Axis Max Life Smart Term with Additional Returns ULIP', 'n/a', B, None, 'AXIS MAX LIFE SMART TERM WITH ADDITIONAL RETURNS ULIP AT A GLANCE'),
  'irdai_description_line': F('Unit Linked Non Participating Individual Life Insurance Plan', 'n/a', B, None, 'Unit Linked Non Participating Individual Life Insurance Plan'),
  'launch_or_version_date': NS(), 'target_segment_stated': NS(),
  'variants_or_plan_options': F(['Life Secure Variant', '3D Life Secure Variant (monthly income plus 1, 2 or 3 times premium funding)', 'Wealth and Whole Life sub variants'], 'optional (at inception)', B, None, 'Step 4: Choose from the following two Product Variants'),
  'online_offline': NS(),
 },
 'eligibility': {
  'entry_age_min': F(18, 'n/a', B, None, 'Minimum Age of Life Insured at Entry (age as on 18 years'),
  'entry_age_max': F(60, 'n/a', B, None, 'Maximum Age of Life Insured at Entry (age as on 60 years'),
  'maturity_age_min': F({'wealth': 38, 'whole life': 100}, 'n/a', B, None, 'Wealth Variant: 38 years.', quote_2='Whole Life Variant: 100 years.'),
  'maturity_age_max': F({'wealth': 85, 'whole life': 100}, 'n/a', B, None, 'Wealth Variant: 85 years Whole Life Variant: 100 years'),
  'policy_term_options': F({'minimum': 20, 'wealth maximum': 67, 'whole life': '100 minus age at entry'}, 'n/a', B, None, 'Minimum: 20 years', quote_2='Wealth Variant: 67 years', quote_3='Whole Life Variant: Policy term is equal to 100 less age at entry'),
  'ppt_options': F({'wealth': {'limited pay': '5 to 15 years', 'regular pay': '20 to 67 years'}, 'whole life, limited pay': '5 to 15 years'}, 'n/a', B, None, 'Limited Pay: 5 years', quote_2='Limited Pay: 15 years', quote_3='Regular Pay: 20 years', quote_4='Regular Pay: 67 years'),
  'premium_min_annual': F({'standard': 20000, 'online and ISNP': 12000}, 'n/a', B, None, 'The minimum annualized premium is Rs. 20,000 per annum', quote_2='The minimum annualized premium shall be Rs. 12,000 for policies purchased via'),
  'premium_min_single': NS(),
  'premium_max': F('no limit, subject to underwriting', 'n/a', B, None, 'No limit, subject to the limits determined in accordance with the Board approved'),
  'sum_assured_rule': F({'rule': 'annualized premium times the cover multiple chosen at inception', 'minimum cover multiple': 10, 'minimum sum assured': 200000}, 'built-in', B, None, 'The Sum assured on death under the product is annualized premium times the cover', quote_2='Limited Pay/Regular Pay: Rs. 2,00,000', quote_3='Wealth Variant Limited/ Regular pay 10'),
  'premium_modes': F('annual, semi-annual, quarterly, monthly', 'n/a', B, None, 'Premium Payment mode Annual, Semi-Annual, Quarterly and Monthly.'),
  'life_cover_multiple_choice': F('cover multiple chosen at inception; examples in the prospectus use 120 times annualized premium', 'optional (at inception)', B, None, 'Cover Multiple: 120 times of'),
 },
 'charges': {
  'premium_allocation_charge': F({'Y1': '7%', 'Y2': '6%', 'Y3': '6%', 'Y4': '6%', 'Y5+': 'nil', 'female lives': 'first year charge falls by 0.50%'}, 'built-in', B, None, '1 7% 2 6% 3 6% 4 6%', quote_2='For female lives, first year’s allocation charge will reduce by 0.50%.'),
  'policy_administration_charge': F('0.41% of annualized premium (per month) from policy year 5, inflating 5% a year compounded, max Rs 500 per month', 'built-in', B, None, 'is 0.41% and will be deducted starting', quote_2='inflate by 5% per annum compounded annually subject to a maximum of Rs. 500 per month'),
  'fund_management_charge': F({'1.35%': 'High Growth II, Growth Super II, Diversified Equity II, BSE 500 Value 50 Index II, BSE Dividend Stability Index, India Sector Leaders Opportunities, Rising India Manufacturing, Flexi Cap', '1.25%': 'other equity, index and thematic funds', '1.10%': 'Balanced Fund', '1.00%': 'Nifty Smallcap Quality Index Fund', '0.90%': 'debt funds, Secure and Secure Plus', '0.50%': 'Discontinuance Policy Fund'},
                              'built-in', B, None, 'High Growth Fund II (SFIN: 1.35%', 'rates per fund in the funds group; the table prints the percentage on separate lines from some names', quote_2='BSE 500 Dividend leaders 50 Index Fund (SFIN: 1.25%'),
  'mortality_charge': F({'basis': 'attained-age rate on sum at risk; the Policy Contract prints the table', 'sum at risk': {'life secure': 'max(max(sum assured, 105% of premiums) less partial withdrawals, minus fund value, 0)', '3D life secure': 'higher of sum assured and 105% of premiums, plus present value of income benefit and funded premiums at 6.05%'}}, 'built-in', B, None,
                        'Max (Max (Sum Assured on death, 105% of total premiums paid) less applicable partial withdrawals –', 'attained-age table on Policy Contract p.38'),
  'discontinuance_charge': F({'annualized premium up to Rs 50,000': {'Y1': '20%, max Rs 3,000', 'Y2': '15%, max Rs 2,000', 'Y3': '10%, max Rs 1,500', 'Y4': '5%, max Rs 1,000', 'Y5+': 'nil'}, 'annualized premium above Rs 50,000': {'Y1': '6%, max Rs 6,000', 'Y2': '4%, max Rs 5,000', 'Y3': '3%, max Rs 4,000', 'Y4': '2%, max Rs 2,000', 'Y5+': 'nil'}}, 'built-in', B, None,
                             '1 20% 3000 6% 6000 2 15% 2000 4% 5000 3 10% 1500 3% 4000 4 5% 1000 2% 2000 5 and onwards Nil Nil'),
  'switching_charge': F('nil; unlimited free switches', 'built-in', B, None, 'All switches will be free of charge.'),
  'partial_withdrawal_charge': F('nil', 'built-in', B, None, 'Partial withdrawals are free of any charge.'),
  'premium_redirection_charge': F('nil', 'built-in', B, None, 'There is no charge for premium redirection.'),
  'miscellaneous_charge': F('none', 'built-in', B, None, 'There are no miscellaneous charges.'),
  'guarantee_charge': NS(), 'rider_charges': F('nil', 'built-in', B, None, '7. Rider Charge Nil'),
  'any_charge_returned': F({'mortality and morbidity charges': '200% of charges from the start of year 16 to the end of year 25, 300% from year 26, added monthly', 'premium allocation charges': '200% of the year 1 to 4 charges, added at the end of years 10 to 13', 'policy administration charges': '300% at maturity or at the end of policy year (85 minus age at entry)'}, 'built-in', B, None,
                           'From the start 16th year to the end of 25th year 200%', quote_2='At the end of the 10th,11th,12th and 13th policy years, 200% of the total premium allocation charges', quote_3='300% of policy administration charges shall be added back as Return of Policy Administration Charge'),
 },
 'benefits': {
  'death_benefit_formula': F({'life secure': 'highest of sum assured, fund value and 105% of premiums paid', '3D life secure': 'lump sum (higher of sum assured and 105% of premiums), plus income of 20% of annualized premium a month for 10 years, plus the company funds 1, 2 or 3 times the future premiums and pays the fund value at maturity'}, 'built-in', B, None,
                             'iii. 105% of the total premiums paid up to the date of death (reduced by applicable partial withdrawals, if any)', quote_2='An income benefit equal to 20% of annualized premium will be paid each month starting', quote_3='The Company will fund X times of all future outstanding premiums as and when due'),
  'maturity_benefit': F('fund value at maturity; settlement option', 'built-in', B, None, 'The maturity benefit is equal to'),
  'loyalty_additions': F({'timing': 'wealth variant: last 5 policy years; whole life: policy years (80 minus entry age plus 1) to (85 minus entry age)', 'rate': '0% to 11.30% of sum assured by entry age, cover multiple and maturity age (table on prospectus pp.7-8)', 'entry age 35 or below, multiple 10-50': '0.00%, 1.50%, 2.05%, 2.45%, 3.45%, 4.00%, 4.70% for maturity ages under 55, 55-60, 60-65, 65-70, 70-75, 75-80, 80+'}, 'built-in', B, None,
                         '<=35 150-200 0.00% 1.50% 2.05% 2.45% 2.80% 3.00% 3.00%', quote_2='10-50 0.00% 1.50% 2.05% 2.45% 3.45% 4.00% 4.70%', quote_3='GLA shall be added to the fund value during the last 5 policy years at the end of the policy'),
  'wealth_boosters_or_guaranteed_additions': F({'Guaranteed Wealth Booster': '3% of fund value at the end of year 20 and every 5 years after', 'Cover Continuance Booster': 'tops the fund up to 10% of annualized premium (years 1 to maturity) or to the fund implied by a target net yield, so cover does not lapse'}, 'built-in', B, None,
                                               'GWB as a percentage of fund value is 3%.', quote_2='Starting Policy Year 1 till maturity. Non-negative amounts called Cover Continuance Boosters(CCB)', quote_3='TGRIY at policy duration where the policyholder attains age of 84 or at end of the Policy Term, whichever is earlier, shall be, 4.10%.'),
  'return_of_mortality_charges': F('200% of mortality and morbidity charges added back monthly from year 16 (300% from year 26)', 'built-in', B, None, 'From the start 16th year to the end of 25th year 200%', quote_2='From the start of 26th year 300%'),
  'return_of_premium_allocation_charges': F('200% of the year 1 to 4 allocation charges, added at the end of years 10 to 13', 'built-in', B, None, 'At the end of the 10th,11th,12th and 13th policy years, 200% of the total premium allocation charges'),
  'return_of_policy_admin_charges': F('300% of administration charges at maturity or at the end of policy year (85 minus age at entry)', 'built-in', B, None, '300% of policy administration charges shall be added back as Return of Policy Administration Charge'),
  'other_additions': NS(),
 },
 'flexibility': {
  'fund_switching': F('unlimited free switches', 'optional (during term)', B, None, 'Unlimited Free Switches and Premium Redirections'),
  'premium_redirection': F('unlimited and free', 'optional (during term)', B, None, 'Unlimited Free Switches and Premium Redirections'),
  'partial_withdrawals': NS(),
  'systematic_withdrawal_plan': F('Smart Withdrawals: chosen at inception or any time in the term', 'optional (during term)', B, None, 'You may choose this option of ‘Smart'),
  'top_up_premiums': F('not available', 'n/a', B, None, 'Top Up Not available in this plan'),
  'settlement_option': NS(), 'premium_holiday_or_offset': NS(),
  'increase_decrease_cover': NS(),
  'change_ppt_or_term': F('no charge for changing premium, premium payment term or policy term', 'optional (during term)', B, None, 'No charge is applicable for any premium, premium payment term or policy term.'),
  'policy_loan': F('not available', 'n/a', B, None, 'Policy loan Provisions Not available in this plan'),
  'auto_portfolio_strategies': F([{'name': 'Self-Managed Portfolio Strategy'}, {'name': 'Systematic Transfer Plan', 'mechanics': 'annual premium goes to Secure Plus Fund; 1/12, 1/11 ... of the units move monthly to a chosen equity fund; annual mode only'}, {'name': 'Lifecycle Based Portfolio Strategy'}, {'name': 'Trigger Based Portfolio Strategy'}, {'name': 'Dynamic Fund Allocation strategy'}], 'optional (at inception)', B, None,
                                 '1) Self-Managed Portfolio Strategy 2) Systematic Transfer Plan (STP) 3) Lifecycle Based Portfolio Strategy 4) Trigger Based Portfolio Strategy 5) Dynamic Fund Allocation (DFA) strategy'),
 },
 'funds': {
  'fund_count': F(31, 'n/a', B, None, 'You may choose to invest in following Thirty-one (31) investment funds available in this plan.'),
  'fund_list': F(FUNDS, 'n/a', B, None, '31. Money Market II Fund', 'names from the prospectus Step 3 list; FMCs and SFINs match the same funds in the Fast Track Super prospectus because this prospectus prints them on separate lines'),
  'index_or_thematic_funds': F('NIFTY Smallcap Quality Index, Nifty Alpha 50, Nifty 500 Momentum 50, Midcap Momentum Index, Nifty Momentum Quality 50, Sustainable Wealth 50 Index, Nifty 500 Multifactor 50 Index, BSE 500 Value 50 Index, BSE 500 Dividend Leaders 50 Index, BSE Dividend Stability Index, BSE 500 Value 50 Index II funds; India Consumption Opportunities, Smart Innovation, Rising India Manufacturing', 'n/a', B, None, '2. NIFTY Smallcap Quality Index'),
  'discontinued_policy_fund': F({'name': 'Discontinuance Policy Fund', 'FMC': '0.50%'}, 'built-in', B, None, 'Discontinuance Policy Fund'),
 },
 'protection_add_ons': {
  'waiver_of_premium_inbuilt': F('3D Life Secure: the company funds 1, 2 or 3 times the future premiums after death, and after critical illness or dismemberment', 'optional (at inception)', B, None, 'Critical Illness and/or Dismemberment: Payable on occurrence of Critical illness and/or dismemberment'),
  'critical_illness': F('3D Life Secure variant: premiums funded on critical illness or dismemberment; also via rider', 'optional (at inception)', B, None, 'Critical illness and/or dismemberment to the Life Insured provided the risk cover under the'),
  'accidental_death': F('via rider (Smart Ultra Protect, variants 2 and 3)', 'rider', B, None, 'Rider benefit variant 2 - Accidental Death Benefit'),
  'terminal_illness': F('via rider (Smart Ultra Protect, variant 1)', 'rider', B, None, 'Term Booster with Accelerated Terminal Illness', quote_2='• Rider benefit variant 1 - Term Booster with Accelerated Terminal Illness:', page_2=3),
  'spouse_or_child_cover': NS(),
  'riders_available': F(RIDERS, 'rider', B, None, 'Axis Max Life Smart Ultra Protect Rider (UIN: 104A049V03)'),
 },
 'surrender_revival': {'lock_in_years': F(5, 'built-in', B, None, 'No Surrender/Discontinuance charge shall be levied from 5th Policy Year onwards.'), 'discontinuance_rules': NS(), 'revival_period': NS(), 'surrender_value_rule': NS()},
}
build('104L128V01', spec,
  new_features=[{'feature': 'Cover Continuance Booster', 'description': 'The company adds units whenever the fund falls below 10% of annualized premium (or below the fund implied by a target net yield), so cover does not lapse', 'quote': 'Starting Policy Year 1 till maturity. Non-negative amounts called Cover Continuance Boosters(CCB)', 'doc': B, 'page': None},
                {'feature': 'Return of charges above 100%', 'description': 'Mortality and morbidity charges returned at 200% to 300%, allocation charges at 200%, administration charges at 300%', 'quote': '300% of policy administration charges shall be added back as Return of Policy Administration Charge', 'doc': B, 'page': None},
                {'feature': '3D Life Secure variant', 'description': 'Death or critical illness or dismemberment: the company funds 1, 2 or 3 times the future premiums; on death also pays 20% of annualized premium a month for 10 years', 'quote': 'An income benefit equal to 20% of annualized premium will be paid each month starting', 'doc': B, 'page': None}],
  not_public=[])
