import sys; sys.path.insert(0, 'scripts'); sys.path.insert(0, 'scripts/ulip_specs')
from ulip_json import F, NS, build
from sbi_common import funds
P, B = 'Policy Document', 'Product Brochure/Prospectus'
FMC = {'Equity Fund': 1.35, 'Equity Optimiser Fund': 1.35, 'Growth Fund': 1.35, 'Balanced Fund': 1.25, 'Bond Fund': 1.00, 'Money Market Fund': 0.25, 'Top 300 Fund': 1.35, 'Bond Optimiser Fund': 1.15,
       'Pure Fund': 1.35, 'Bluechip Fund': 1.35, 'Midcap Fund': 1.35, 'Corporate Bond Fund': 1.15, 'Flexicap Fund': 1.35, 'Large Cap Fund': 1.35}
spec = {
 'product': {
  'uin': F('111L144V01', 'n/a', P, None, 'SBI Life – Smart Scholar Plus (UIN: 111L144V01)'),
  'uin_in_brochure': F('111L144V01', 'n/a', B, None, '111L144V01'),
  'product_name': F('SBI Life – Smart Scholar Plus', 'n/a', P, None, 'SBI Life – Smart Scholar Plus (UIN: 111L144V01)'),
  'irdai_description_line': F('An Individual, Unit Linked, Non-Participating, Life Insurance Savings Product', 'n/a', P, None, 'An Individual, Unit Linked, Non-Participating, Life Insurance Savings Product'),
  'launch_or_version_date': F('policy document Form No 863', 'n/a', P, None, 'Form No. 863'),
  'variants_or_plan_options': F([{'name': 'Regular / Limited / Single pay', 'description': 'child plan: parent is life assured, child is nominee; premium payor waiver on parent\'s death (not for single pay)'}], 'n/a', B, None, 'Premium Paying Single Pay: One time at policy inception'),
  'target_segment_stated': F('child (parent as life assured, child as nominee)', 'n/a', B, None, 'Parent (Life Assured): 18 years Parent (Life Assured): 50 Years'),
  'online_offline': NS(),
 },
 'eligibility': {
  'entry_age_min': F('parent 18; child 0', 'n/a', B, None, 'Parent (Life Assured): 18 years Parent (Life Assured): 50 Years'),
  'entry_age_max': F('parent 50; child 17', 'n/a', B, None, 'Parent (Life Assured): 18 years Parent (Life Assured): 50 Years'),
  'maturity_age_min': F('child 18', 'n/a', B, None, 'Child: 18 Years'),
  'maturity_age_max': F('parent 65; child 25', 'n/a', B, None, 'Child: 25 Years'),
  'policy_term_options': F('8-25 years, child at least 18 at maturity', 'n/a', B, None, 'Policy Term 8 years to 25 years'),
  'ppt_options': F('single; limited 5 years to PT minus 1; regular (= PT)', 'n/a', B, None, 'Limited Pay: 5 years to Policy term minus 1 year'),
  'premium_min_annual': F('Rs 50,000 yearly / 25,000 half-yearly / 15,000 quarterly / 5,500 monthly', 'n/a', B, None, 'Yearly 50,000'),
  'premium_min_single': F('Rs 75,000', 'n/a', B, None, 'Single Pay Single 75,000'),
  'premium_max': F('no limit, subject to board-approved underwriting policy', 'n/a', B, None, 'No Limit,'),
  'sum_assured_rule': F('limited/regular: 10 x annualised premium; single: 1.25 x single premium', 'built-in', B, None, 'Limited Pay / Regular Pay: 10 x Annualized Premium'),
  'premium_modes': F('single, yearly, half-yearly, quarterly, monthly', 'n/a', B, None, 'Half-Yearly 25,000'),
  'life_cover_multiple_choice': F(None, 'not offered'),
 },
 'charges': {
  'premium_allocation_charge': F({'regular/limited': {'Y1': '6.0%', 'Y2-3': '4.5%', 'Y4-5': '4.0%', 'Y6-10': '1.0%', 'Y11+': 'nil'}, 'single': '3.00% once'}, 'built-in', P, None, 'For Single Premium Policy: 3.00% (once at Date of Commencement of Policy)'),
  'policy_administration_charge': F('Rs 50 a month (single), Rs 75 a month (regular/limited); cap Rs 500', 'built-in', P, None, 'For Regular / Limited Pay policies: Rs.75 per month'),
  'fund_management_charge': F({'min': '0.25% (Money Market Fund)', 'max': '1.35%', 'discontinued_policy_fund': '0.50%'}, 'built-in', P, None, 'The FMC for all Segregated Funds except Discontinued Policy Fund, would be subject to a cap of 1.35%.'),
  'mortality_charge': F('per Rs 1,000 sum at risk by attained age; table published; stops after the parent\'s death', 'built-in', P, None, 'We will not deduct future Mortality Charges, PPWB Charges and AB Charges.'),
  'discontinuance_charge': F('IRDAI-cap tables for limited/regular and single pay', 'built-in', P, None, 'We will recover Discontinuance Charges from the Fund Value.'),
  'switching_charge': F('2 free a year, then Rs 100 per switch', 'built-in', P, None, 'Rs.100 will be levied per switch in excess of free Switches in the same Policy Year.'),
  'partial_withdrawal_charge': F('Rs 100 for the second withdrawal in a year (cap Rs 500)', 'built-in', P, None, 'We will charge Rs.100 for the second withdrawal in any Policy Year.'),
  'premium_redirection_charge': NS(), 'miscellaneous_charge': NS(), 'guarantee_charge': F(None, 'n/a'),
  'rider_charges': F({'Premium Payor Waiver Benefit (PPWB)': 'level monthly charge per Rs 1,000 AP, by parent\'s entry age and PPT; only during the premium term; not for single pay', 'Accident Benefit': 'Rs 0.60 per Rs 1,000 Accident Benefit Sum Assured a year'}, 'built-in', P, None,
                     'The fixed annual PPWB rate depends on the Age last Birthday of Life Assured at Date of Commencement of Policy and the Premium Paying Term.', 'PPWB rate table (clause 35.2.7) is published in the policy document; not transcribed here'),
  'any_charge_returned': F(None, 'not offered'),
 },
 'benefits': {
  'death_benefit_formula': F('on the parent\'s death (non-accident): higher of sum assured or 105% of premiums paid, paid as a lump sum; then the company pays future premiums into the fund and the policy continues to maturity (premium payor waiver)', 'built-in', P, None,
                             'We will pay the future Premiums payable under the Policy, into the Chosen Funds, as and when due.'),
  'maturity_benefit': F('fund value to the life assured, or to the child nominee if the parent has died', 'built-in', P, None, 'On the Date of Maturity, We will pay the Fund Value in lumpsum to the Life Assured if alive or to the child Nominee in case of death of the Life Assured during the Policy Term.'),
  'loyalty_additions': F('1% of the 24-month average fund value at the end of year 8, 9 or 10 (by policy term) and every 3 years after; continue after the parent\'s death', 'built-in', P, None,
                         'The Loyalty Addition amount at relevant Policy Year end will be equivalent to 1% × [Average Fund Value over the 1st day of the preceding 24 Policy months].'),
  'wealth_boosters_or_guaranteed_additions': F(None, 'not offered'), 'return_of_mortality_charges': F(None, 'not offered'), 'return_of_premium_allocation_charges': F(None, 'not offered'), 'return_of_policy_admin_charges': F(None, 'not offered'), 'other_additions': NS(),
 },
 'flexibility': {
  'fund_switching': F('2 free a year; then Rs 100 per switch', 'optional (during term)', P, None, 'Two Switches are allowed free of charge in a Policy Year. A Switching Charge of'),
  'premium_redirection': NS(),
  'partial_withdrawals': F('from year 6; 2 a year (1 free); 5 in the term (PT up to 10) or 10 (PT over 10); multiples of Rs 1,000', 'optional (during term)', P, None, 'We will allow maximum two Partial Withdrawals in one Policy Year, out of which one would be free of charge'),
  'systematic_withdrawal_plan': F(None, 'not offered'), 'top_up_premiums': NS(), 'settlement_option': NS(), 'premium_holiday_or_offset': NS(),
  'increase_decrease_cover': NS(), 'change_ppt_or_term': NS(), 'policy_loan': NS(), 'auto_portfolio_strategies': F(None, 'not offered'),
 },
 'funds': {
  'fund_count': F('14 funds plus the Discontinued Policy Fund', 'n/a', P, None, 'There are fourteen Segregated Funds as listed below available under the Policy, each of which have different risk-return'),
  'fund_list': F(funds(FMC), 'n/a', P, None, 'Fund Options FMC (p.a.) Equity Fund 1.35%'),
  'index_or_thematic_funds': F('Pure, Midcap, Flexicap and Large Cap Funds; no index fund', 'n/a', P, None, 'Flexicap Fund 1.35% Large Cap Fund 1.35%', 'themes inferred from names'),
  'discontinued_policy_fund': F({'name': 'Discontinued Policy Fund', 'FMC': '0.50%'}, 'built-in', P, None, 'Discontinued Policy Fund 0.50%'),
 },
 'protection_add_ons': {
  'waiver_of_premium_inbuilt': F('Premium Payor Waiver Benefit: on the parent\'s death the company pays the remaining premiums (not for single pay)', 'built-in', P, None, 'We will pay the future Premiums payable under the Policy, into the Chosen Funds, as and when due.'),
  'critical_illness': NS(),
  'accidental_death': F('in-built Accident Benefit, charged at Rs 0.60 per Rs 1,000 a year', 'built-in', P, None, 'annual rate is Rs 0.60 per 1,000 Accident Benefit Sum Assured.'),
  'terminal_illness': NS(), 'spouse_or_child_cover': F('child is the nominee and receives maturity proceeds after the parent\'s death', 'built-in', P, None, 'to the child Nominee in case of death of the Life Assured during the Policy Term.'),
  'riders_available': NS('no separate riders found; accident benefit and payor waiver are built in'),
 },
 'surrender_revival': {'lock_in_years': F(5, 'built-in', P, None, 'You can Withdraw post commencement of the 6th Policy Year.'), 'discontinuance_rules': NS(), 'revival_period': F('3 consecutive complete years from the first unpaid premium', 'built-in', P, None, 'is the period of three consecutive complete years from the date of first unpaid'), 'surrender_value_rule': F('in lock-in: discontinued fund proceeds paid after year 5; after lock-in: fund value on the date of the surrender request', 'built-in', P, None, 'If You opt to completely withdraw from the Policy, then Fund Value as on date of')},
}
build('111L144V01', spec,
  new_features=[{'feature': 'Child ULIP with built-in payor waiver and accident benefit', 'description': 'sum assured paid on the parent\'s death and future premiums paid in by the insurer; mortality and PPWB charges stop', 'quote': 'We will not deduct future Mortality Charges, PPWB Charges and AB Charges.', 'doc': P, 'page': None},
                {'feature': 'Loyalty additions continue after the parent\'s death', 'description': '1% of the 24-month average fund value every 3 years', 'quote': 'Loyalty Additions will continue in case of continuance of the Policy after the death of the Life Assured.', 'doc': P, 'page': None}],
  not_public=[])
