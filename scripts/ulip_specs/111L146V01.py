import sys; sys.path.insert(0, 'scripts'); sys.path.insert(0, 'scripts/ulip_specs')
from ulip_json import F, NS, build
from sbi_common import funds, SFIN
P, B = 'Policy Document', 'Product Brochure/Prospectus'
SFIN['Equity Elite Fund II'] = 'ULIF019100210EQTELI2FND111'
FMC = {'Equity Elite Fund II': 1.25, 'Balanced Fund': 1.25, 'Bond Fund': 1.00, 'Money Market Fund': 0.25, 'Bond Optimiser Fund': 1.15, 'Pure Fund': 1.35, 'Midcap Fund': 1.35, 'Corporate Bond Fund': 1.15,
       'Bluechip Fund': 1.35, 'Equity Fund': 1.35, 'Equity Optimiser Fund': 1.35, 'Growth Fund': 1.35, 'Top 300 Fund': 1.35, 'Flexicap Fund': 1.35, 'Large Cap Fund': 1.35}
spec = {
 'product': {
  'uin': F('111L146V01', 'n/a', P, None, '111L146V01'),
  'uin_in_brochure': F('111L146V01', 'n/a', B, None, '111L146V01'),
  'product_name': F('SBI Life – Smart Elite Plus', 'n/a', P, None, 'SBI Life – Smart Elite Plus'),
  'irdai_description_line': F('An Individual, Unit Linked, Non-Participating, Life Insurance Saving Product (light pass reading of the brochure)', 'n/a', note='description line as recorded in the light pass'),
  'launch_or_version_date': F('policy document Form No 862; site file dated 28-10-2026', 'n/a', P, None, 'Policy Document Form No: 862'),
  'variants_or_plan_options': F([{'name': 'Gold Option', 'description': 'death benefit = highest of fund value, sum assured less APW, 105% of premiums'}, {'name': 'Platinum Option', 'description': 'death benefit = higher of fund value plus sum assured, or 105% of premiums'}],
                                'optional (at inception)', P, None, 'The product provides two Plan Options: Gold Option and Platinum Option. Only one of these options is to be chosen at the inception of the Policy.'),
  'target_segment_stated': NS(), 'online_offline': NS(),
 },
 'eligibility': {
  'entry_age_min': F('18 years', 'n/a', B, None, 'Age1 at Entry Minimum: Maximum: 18 years Limited Pay: 55 years Single Pay: 60 years'),
  'entry_age_max': F('55 (limited pay), 60 (single pay)', 'n/a', B, None, 'Age1 at Entry Minimum: Maximum: 18 years Limited Pay: 55 years Single Pay: 60 years'),
  'maturity_age_min': NS(), 'maturity_age_max': F('70 years', 'n/a', B, None, 'Maximum Age1 70 years at Maturity'),
  'policy_term_options': F('limited pay 15-30 years; single pay 5-30 years', 'n/a', B, None, 'Limited Pay 15 – 30 (both inclusive) 7 / 10/ 12'),
  'ppt_options': F('limited 7, 10 or 12 years; single pay', 'n/a', B, None, 'Limited Pay 15 – 30 (both inclusive) 7 / 10/ 12'),
  'premium_min_annual': F('limited pay: Rs 2,50,000 yearly / 1,25,000 half-yearly / 62,500 quarterly / 21,000 monthly', 'n/a', B, None, 'Yearly : 2,50,000'),
  'premium_min_single': F('Rs 2,50,000', 'n/a', B, None, 'Single Pay 2,50,000'),
  'premium_max': F('no limit, subject to board-approved underwriting policy', 'n/a', B, None, 'No Limit, subject to board approved underwriting policy'),
  'sum_assured_rule': F('limited pay: 7 x annualised premium; single pay: 1.25 x single premium', 'built-in', B, None, 'Sum Assured Limited Pay: 7 x Annualized Premium'),
  'premium_modes': F('single, yearly, half-yearly, quarterly, monthly', 'n/a', B, None, 'Single/ Yearly / Half-yearly / Quarterly / Monthly'),
  'life_cover_multiple_choice': F(None, 'not offered', note='fixed by pay type; Platinum adds sum assured on top of fund value'),
 },
 'charges': {
  'premium_allocation_charge': F({'limited pay (PPT 7/10/12)': {'Y1-5': '3.00%', 'Y6+': 'nil'}, 'single pay': '2.00% once'}, 'built-in', P, None, 'For Limited Pay Policies: Policy Year PPT 7 Years PPT 10 Years PPT 12 Years 1 to 5 3.00% 3.00% 3.00% 6 years onwards Nil Nil Nil'),
  'policy_administration_charge': F('Rs 50 a month (single pay), Rs 100 a month (limited pay); cap Rs 500', 'built-in', P, None, 'For Single Pay policies: Rs.50 per month. 27.1.2. For Limited Pay policies: Rs.100 per month'),
  'fund_management_charge': F({'min': '0.25% (Money Market Fund)', 'max': '1.35%', 'discontinued_policy_fund': '0.50%'}, 'built-in', P, None, 'Fund Options FMC (p.a.) Equity Elite Fund II 1.25% Balanced Fund 1.25% Bond Fund 1.00% Money Market Fund 0.25%'),
  'mortality_charge': F('per Rs 1,000 sum at risk by attained age, monthly; full table published', 'built-in', P, None, 'Monthly Mortality Charges = Sum-at-risk × (Annual Mortality Charge per unit Sum-at-risk / 12 )'),
  'discontinuance_charge': F('separate tables for limited and single pay (IRDAI caps), nil from year 5', 'built-in', P, None, 'For Limited Pay policies, the Discontinuance Charges will be as per the following table:'),
  'switching_charge': F('2 free a year, then Rs 100 per switch (cap Rs 500)', 'built-in', P, None, 'We will charge You Rs.100 per Switch from 3rd Switch onwards in the same Policy Year.'),
  'partial_withdrawal_charge': F('Rs 100 for the second withdrawal in a year (cap Rs 500)', 'built-in', P, None, 'We will charge Rs.100 for the second Partial Withdrawal in any Policy Year.'),
  'premium_redirection_charge': F('first free each year, then Rs 100 per redirection (cap Rs 500)', 'built-in', P, None, 'We will charge Rs.100 per Premium Re-direction from the second Premium Re-direction in the same Policy Year'),
  'miscellaneous_charge': NS(), 'guarantee_charge': F(None, 'n/a'),
  'rider_charges': F('Accident Benefit charge: Rs 0.60 per Rs 1,000 Accident Benefit Sum Assured a year, deducted monthly', 'built-in', P, None, 'where the Annual Rate is Rs 0.60 per 1,000 Accident Benefit Sum Assured.', 'in-built accident benefit, not a separate rider'),
  'any_charge_returned': F(None, 'not offered'),
 },
 'benefits': {
  'death_benefit_formula': F('Gold: highest of fund value, sum assured less APW, 105% of premiums. Platinum: higher of fund value plus sum assured, or 105% of premiums', 'built-in', P, None, 'Platinum Option: Higher of 1.1.2.1. Fund Value as on date of the intimation of the death claim to Us plus Sum Assured or 1.1.2.2. 105% of the Total Premiums Paid upto the date of death'),
  'maturity_benefit': F('fund value as a lump sum', 'built-in', P, None, 'If the Life Assured is alive on the Date of Maturity, We will pay Your Fund Value as the Maturity Benefit in lump-sum as on the Date of Maturity.'),
  'loyalty_additions': F(None, 'not offered'), 'wealth_boosters_or_guaranteed_additions': F(None, 'not offered'), 'return_of_mortality_charges': F(None, 'not offered'),
  'return_of_premium_allocation_charges': F(None, 'not offered'), 'return_of_policy_admin_charges': F(None, 'not offered'), 'other_additions': F(None, 'not offered'),
 },
 'flexibility': {
  'fund_switching': F('2 free a year, then Rs 100; minimum Rs 5,000; allowed during the settlement period too', 'optional (during term)', P, None, 'You can Switch Your Chosen Funds during the Policy Term and also during the Settlement Period, subject to all of the following:'),
  'premium_redirection': F('from year 2; first free each year, then Rs 100', 'optional (during term)', P, None, 'We will allow Premium Re-direction only from the beginning of the second Policy Year.', quote_2='Option of Premium Re-direction from 2nd Policy Year onwards. Part C (II) (14)', page_2=7),
  'partial_withdrawals': F('from year 6; 2 a year, 10 in the term; Rs 5,000 minimum, 15% of fund value maximum', 'optional (during term)', P, None, 'We will allow a maximum of 10 Partial Withdrawals in the entire Policy Term.'),
  'systematic_withdrawal_plan': F(None, 'not offered'),
  'top_up_premiums': F(None, 'not offered', P, None, 'Top up Premiums are not allowed under Your Policy.'),
  'settlement_option': F('on death: the claimant may take the death benefit in instalments, staying invested', 'optional (during term)', P, None, 'On death of the Life Assured, the Claimant may choose to get the Death Benefit in instalments during the Settlement Period, provided that the Policy is In-Force or Reduced Paid-Up on the date of death.'),
  'premium_holiday_or_offset': NS(), 'increase_decrease_cover': NS(), 'change_ppt_or_term': NS(),
  'policy_loan': F(None, 'not offered', P, None, 'Your Policy will not be eligible for any loans.'), 'auto_portfolio_strategies': F(None, 'not offered', note='no investment strategies; fund choice only'),
 },
 'funds': {
  'fund_count': F('15 funds plus the Discontinued Policy Fund', 'n/a', P, None, 'There are fifteen Segregated Funds as listed below available under the Policy, each of which have different riskreturn profiles.'),
  'fund_list': F(funds(FMC), 'n/a', P, None, 'Equity Elite Fund II (SFIN: ULIF019100210EQTELI2FND111)'),
  'index_or_thematic_funds': F('Pure Fund, Midcap Fund, Flexicap Fund, Large Cap Fund; no index fund', 'n/a', P, None, 'Large Cap Fund 1.35%', 'themes inferred from fund names'),
  'discontinued_policy_fund': F({'name': 'Discontinued Policy Fund', 'FMC': '0.50%'}, 'built-in', P, None, 'Discontinued Policy Fund 0.50%'),
 },
 'protection_add_ons': {
  'waiver_of_premium_inbuilt': F(None, 'not offered', note='rider only'),
  'critical_illness': NS(),
  'accidental_death': F('in-built: on accidental death, death benefit plus the Accident Benefit Sum Assured; accidental total permanent disability pays it in 10 yearly instalments', 'built-in', P, None, 'an additional benefit equal to the Accident Benefit Sum Assured'),
  'terminal_illness': NS(), 'spouse_or_child_cover': NS(),
  'riders_available': F([{'name': 'SBI Life - Waiver of Premium Rider - Linked', 'UIN': '111A049V01'}], 'rider', B, None, 'SBI Life – Waiver of Premium Rider – Linked (UIN: 111A049V01)', 'the brochure\'s eligibility table prints the rider UIN as "111AXXXV01" (placeholder)'),
 },
 'surrender_revival': {
  'lock_in_years': F(5, 'built-in', P, None, 'You can withdraw post commencement of the 6th Policy Year.', quote_2='Lock-In Period: 5 years from the Date of Commencement of Part B Definition', page_2=7),
  'discontinuance_rules': F('IRDAI rules: in lock-in to the Discontinued Policy Fund, after lock-in reduced paid-up', 'built-in', P, None, 'If death occurs during the Lock-In Period and after the Date of Discontinuance in any of the following circumstances, the Death Benefit payable would be equal to Accumulated Value of Your Discontinued Policy Fund'),
  'revival_period': NS(), 'surrender_value_rule': F('surrender allowed any time; value per clause 7', 'built-in', P, None, 'You may Surrender Your Policy any time during the Policy Term.'),
 },
}
build('111L146V01', spec,
  new_features=[{'feature': 'Built-in accident benefit inside a ULIP', 'description': 'accidental death adds the Accident Benefit Sum Assured; ATPD pays it in 10 instalments; charged at Rs 0.60 per 1,000 a year', 'quote': 'Accident Benefit Sum Assured in 10 equal yearly instalments where each instalment is equal to 10% of the Accident Benefit Sum Assured.', 'doc': P, 'page': None},
                {'feature': 'Death benefit settlement option', 'description': 'nominee can take the death benefit in instalments while staying invested', 'quote': 'The Death Benefit payable shall continue to be invested in the same proportion of the Chosen Funds as it was maintained at the time of death.', 'doc': P, 'page': None}],
  not_public=[])
