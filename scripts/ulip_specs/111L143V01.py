import sys; sys.path.insert(0, 'scripts'); sys.path.insert(0, 'scripts/ulip_specs')
from ulip_json import F, NS, build
from sbi_common import funds
P, B = 'Policy Document', 'Product Brochure/Prospectus'
FMC = {'Equity Fund': 1.35, 'Pure Fund': 1.35, 'Midcap Fund': 1.35, 'Top 300 Fund': 1.35, 'Equity Optimiser Fund': 1.35, 'Growth Fund': 1.35, 'Balanced Fund': 1.25, 'Bond Fund': 1.00, 'Money Market Fund': 0.25,
       'Bond Optimiser Fund': 1.15, 'Corporate Bond Fund': 1.15, 'Bluechip Fund': 1.35, 'Flexicap Fund': 1.35, 'Large Cap Fund': 1.35}
spec = {
 'product': {
  'uin': F('111L143V01', 'n/a', P, None, 'SBI Life – Smart Privilege Plus (UIN:111L143V01)'),
  'uin_in_brochure': F('111L143V01', 'n/a', B, None, '111L143V01'),
  'product_name': F('SBI Life – Smart Privilege Plus', 'n/a', P, None, 'SBI Life – Smart Privilege Plus (UIN:111L143V01)'),
  'irdai_description_line': F('An Individual, Unit Linked, Non-Participating, Life Insurance, Savings Product', 'n/a', P, None, 'An Individual, Unit Linked, Non-Participating, Life Insurance, Savings Product'),
  'launch_or_version_date': F('policy document Form No 860', 'n/a', P, None, 'Policy Document Form No 860'),
  'variants_or_plan_options': F([{'name': 'Regular / Limited / Single pay', 'description': 'high minimum premium (Rs 6 lakh a year); loyalty additions from year 6'}], 'n/a', B, None, 'Plan Type Regular Pay / Limited Pay / Single Pay'),
  'target_segment_stated': NS('high minimum premium suggests HNI, but no segment is named in the pages read'),
  'online_offline': NS(),
 },
 'eligibility': {
  'entry_age_min': F('8 years (regular/limited), 13 years (single)', 'n/a', B, None, 'Limited Pay: 8 years'),
  'entry_age_max': F('55 years', 'n/a', B, None, 'Age at Entry Minimum: Maximum: Regular Pay/ 55 years'),
  'maturity_age_min': F('18 years', 'n/a', B, None, 'Age1 at Maturity Minimum: 18 years Maximum: 70 years'),
  'maturity_age_max': F('70 years', 'n/a', B, None, 'Age1 at Maturity Minimum: 18 years Maximum: 70 years'),
  'policy_term_options': F('regular 10-30; limited 15-30; single 5-30 years', 'n/a', B, None, 'Regular Pay 10 to 30 Same as Policy Term'),
  'ppt_options': F('regular (= PT); limited 5 years to PT minus 1; single', 'n/a', B, None, 'Max: Policy Term'),
  'premium_min_annual': F('Rs 6,00,000 yearly / 3,00,000 half-yearly / 1,50,000 quarterly / 50,000 monthly', 'n/a', B, None, 'Yearly: 6,00,000'),
  'premium_min_single': F('Rs 6,00,000', 'n/a', B, None, 'Single Pay 6,00,000'),
  'premium_max': F('no limit, subject to board-approved underwriting policy', 'n/a', B, None, 'No Limit, Subject to'),
  'sum_assured_rule': F('regular/limited: 7 x annualised premium; single: 1.25 x single premium', 'built-in', B, None, 'Regular Pay & Limited Pay 7 × Annualized Premium2'),
  'premium_modes': F('single, yearly, half-yearly, quarterly, monthly', 'n/a', B, None, 'Single/Yearly / Half – Yearly / Quarterly / Monthly'),
  'life_cover_multiple_choice': F(None, 'not offered'),
 },
 'charges': {
  'premium_allocation_charge': F({'regular/limited': {'Y1-5': '2.50%', 'Y6+': 'nil'}, 'single': '2.0% once'}, 'built-in', P, None, 'We will recover Premium Allocation Charges as a percentage of Premium as per the following table:'),
  'policy_administration_charge': F('Rs 100 per month (regular/limited), nil (single); cap Rs 500', 'built-in', P, None, 'All Policy Years Regular Pay/ Limited Pay Single Pay Rs.100 per month Nil'),
  'fund_management_charge': F({'min': '0.25% (Money Market Fund)', 'max': '1.35%', 'discontinued_policy_fund': '0.50%'}, 'built-in', P, None, 'The FMC for all Segregated Funds except Discontinued Policy Fund, would be subject to a cap of 1.35%.'),
  'mortality_charge': F('per Rs 1,000 sum at risk by attained age; table published', 'built-in', P, None, 'We will calculate Mortality Charges based on the attained Age of the Life Assured as on the date of deduction.'),
  'discontinuance_charge': F('IRDAI-cap tables (clause 29), nil from year 5', 'built-in', P, None, 'Discontinuance/Surrender Charges 29.1. We will recover Discontinuance Charges from the Fu'),
  'switching_charge': F('nil (cap Rs 500 if introduced)', 'built-in', P, None, 'Switching charge is currently NIL.', quote_2='30.2. If introduced, Switching charge would be subject to a cap of Rs.500 per switch. However, revision of charges', page_2=45),
  'partial_withdrawal_charge': F('2 free a year; Rs 100 for each one beyond that', 'built-in', P, None, 'We will charge Rs. 100 for every Partial Withdrawal in excess of'),
  'premium_redirection_charge': F('nil', 'built-in', P, None, 'We will not charge for Premium Re-direction.'),
  'miscellaneous_charge': NS(), 'guarantee_charge': F(None, 'n/a'), 'rider_charges': NS(), 'any_charge_returned': F(None, 'not offered'),
 },
 'benefits': {
  'death_benefit_formula': F('highest of: fund value; sum assured less APW (not for minors); 105% of premiums paid', 'built-in', P, None, 'APW equals Partial Withdrawals, if any, in the last 2 years immediately preceding the death of the Life Assured.'),
  'maturity_benefit': F('fund value as a lump sum', 'built-in', note='standard SBI maturity clause'),
  'loyalty_additions': F({'basis': '% of the 12-month average fund value', 'Y6': '1.0%', 'Y10': '2.5%', 'Y15': '3.5%', 'Y20': '5.0%', 'Y25': '6.0%', 'Y30': '7.0%'}, 'built-in', P, None,
                         'The Loyalty Additions would be calculated as a percentage of the average Fund Value.'),
  'wealth_boosters_or_guaranteed_additions': F(None, 'not offered'), 'return_of_mortality_charges': F(None, 'not offered'), 'return_of_premium_allocation_charges': F(None, 'not offered'), 'return_of_policy_admin_charges': F(None, 'not offered'), 'other_additions': NS(),
 },
 'flexibility': {
  'fund_switching': F('free, unlimited; also during settlement', 'built-in', P, None, 'There are no restrictions on the number of Switches during a particular Policy Year or during entire Policy Term and during the Settlement Period'),
  'premium_redirection': F('free from year 1; 14 days notice', 'optional (during term)', P, None, 'We will allow Premium Re-direction from thefirst Policy year onwards.', quote_2='least 14 days prior to the Premium Due Date on which the Premium Re-direction is to be applied. Allocation Percentage can only be in multiples of 1%.', page_2=35),
  'partial_withdrawals': F('from year 6 and age 18; 2 free a year, up to 4 a year; 10 in the term (PT up to 10) or 15 (PT over 10)', 'optional (during term)', P, None, 'We will allow two free Partial Withdrawals in a Policy Year.'),
  'systematic_withdrawal_plan': F(None, 'not offered'),
  'top_up_premiums': F(None, 'not offered', P, None, 'Top up Premiums are not allowed under Your Policy.'),
  'settlement_option': F('on death, in instalments to the claimant', 'optional (during term)', note='settlement-option clause present (clause 25 references "Date of payment under Settlement Option")'),
  'premium_holiday_or_offset': NS(), 'increase_decrease_cover': NS(), 'change_ppt_or_term': NS(),
  'policy_loan': F(None, 'not offered', P, None, 'Your Policy will not be eligible for any loans.'), 'auto_portfolio_strategies': F(None, 'not offered'),
 },
 'funds': {
  'fund_count': F('14 funds plus the Discontinued Policy Fund', 'n/a', P, None, 'There are fourteen Segregated Funds as listed below available under the Policy, each of which have different risk-return'),
  'fund_list': F(funds(FMC), 'n/a', P, None, 'Fund Options FMC (p.a.) Equity Fund 1.35%'),
  'index_or_thematic_funds': F('Pure, Midcap, Flexicap and Large Cap Funds; no index fund', 'n/a', P, None, 'Large Cap Fund 1.35%', 'themes inferred from names'),
  'discontinued_policy_fund': F({'name': 'Discontinued Policy Fund', 'FMC': '0.50%'}, 'built-in', P, None, 'Discontinued Policy fund 0.50%'),
 },
 'protection_add_ons': {
  'waiver_of_premium_inbuilt': F(None, 'not offered', note='rider only'), 'critical_illness': F('via Waiver of Premium Rider', 'rider', B, None, 'SBI Life - Waiver of Premium Rider- Linked (UIN: 111A049V01)'), 'terminal_illness': NS(), 'spouse_or_child_cover': NS(),
  'accidental_death': F('SBI Life - Accident Benefit Rider - Linked (111A042V01)', 'rider', B, None, 'Option A: Accidental Death Benefit (ADB)', quote_2='SBI Life - Accident Benefit Rider - Linked (UIN : 111A042V01) Option A: Accidental Death Benefit (ADB)', page_2=5),
  'riders_available': F([{'name': 'SBI Life - Accident Benefit Rider - Linked', 'UIN': '111A042V01'}, {'name': 'SBI Life - Waiver of Premium Rider - Linked', 'UIN': '111A049V01'}], 'rider', B, None, 'SBI Life - Accident Benefit Rider - Linked (UIN : 111A042V01)'),
 },
 'surrender_revival': {'lock_in_years': F(5, 'built-in', P, None, 'Lock-In Period: 5 years from the Date of Commencement of Policy.'), 'discontinuance_rules': NS(), 'revival_period': F('3 consecutive complete years from the first unpaid premium', 'built-in', P, None, 'is the period of three consecutive complete years from the date of first unpaid'), 'surrender_value_rule': F('in lock-in: discontinued fund proceeds paid after year 5; after lock-in: fund value on the date of the surrender request', 'built-in', P, None, 'You have an option to Surrender the Policy any time. Upon receipt of request for Surrender, the Fund')},
}
build('111L143V01', spec,
  new_features=[{'feature': 'Rising loyalty additions on a 12-month average fund value', 'description': '1% at year 6 rising to 7% at year 30', 'quote': 'The average Fund Value is the average of the Fund Values as on the 1st day of the last 12 Policy Months preceding the allocation of Loyalty Addition.', 'doc': P, 'page': None}],
  not_public=[])
