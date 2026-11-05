from rider_json import L
SLUG = 'axis-max-life'
Q0 = 'Comprehensive CI cover: Option to choose Gold variant (coverage of 22 CI) or Platinum variant'
NC = 'Five variants: Gold, Gold Plus, Platinum, Platinum Plus (critical illness, with or without TPD) and TPD only.'
SPEC = {
 'rider': {
  'name': L('Axis Max Life Critical Illness and Disability - Secure Rider', 'n/a', 'brochure', 'Axis Max Life Critical Illness and Disability - Secure Rider'),
  'uin': L('104A034V02', 'n/a', 'brochure', 'UIN:104A034V02'),
  'linked_or_non_linked': L('unit-linked base, non-participating, individual pure risk health rider; level rider premium, not a charge from the fund', 'n/a', 'brochure', 'Unit-Linked Non-Participating Individual Pure Risk Health Insurance Rider'),
  'attached_to_ulips': L('see results/ulip_rider_map.csv', 'n/a', None, None, 'Named by 8 of the 9 Axis Max ULIPs (not Forever Young Pension).'),
 },
 'benefits': {
  'waiver_of_premium': L('not covered. No premium waiver in the brochure; the Wellness (Max Fit) program is the other extra.', 'not covered', 'brochure', Q0, NC),
  'waiver_on_death_of_life_assured': L('not covered', 'not covered', 'brochure', Q0, NC),
  'waiver_on_death_or_illness_of_proposer': L('not covered', 'not covered', 'brochure', Q0, NC),
  'critical_illness': L('Gold: 22 critical illnesses. Platinum: 64. Rider sum assured paid on diagnosis of a listed illness. Each variant can add total and permanent disability.', 'covered as an option', 'brochure', 'Gold variant (coverage of 22 CI) or Platinum variant (coverage of 64 CI)'),
  'accidental_death': L('not covered', 'not covered', 'brochure', Q0, NC),
  'accidental_disability': L('Total and permanent disability variant (alone or added to Gold or Platinum); the brochure ties it to accidental bodily injury, sickness or disease.', 'covered as an option', 'brochure', 'Total and Permanent Disability variant: This rider offers coverage on Total and Permanent'),
  'term_cover': L('not covered', 'not covered', 'brochure', Q0, NC),
  'hospital_cash': L('not covered', 'not covered', 'brochure', Q0, NC),
  'other': L('Max Fit wellness benefit.', 'covered', 'brochure', 'Max Fit Program: A Wellness Benefit is available in this rider'),
 },
 'terms': {
  'rider_term': L('5 to 10 years, not above the base policy term. Limited pay: PPT 5 to 9, policy term (PPT + 1) to 10. Regular pay: 5 to 10.', 'n/a', 'brochure', 'Minimum Policy Terms 5 years'),
  'premium_paying_rules': L('Limited pay or regular pay as per the base plan. Modes as the base policy. Rider premium cannot exceed the base premium payment term.', 'n/a', 'brochure', 'Limited Pay & Regular Pay premium payment variants are'),
  'entry_age': L('18 to 65 years; maximum maturity age 75', 'n/a', 'brochure', 'Maximum Entry Age (age as on last'),
  'sum_assured_limits': L('Minimum Rs 1,00,000, maximum Rs 1 crore at inception, not above the base sum assured. Health and critical illness rider premiums together may not exceed 100% of the base premium.', 'n/a', 'brochure', 'Maximum initial Rider Sum Assured is Rs. 1 Crore'),
  'premium_deduction': L('Level rider premium in addition to the base premium, not a rider charge deducted from unit funds.', 'n/a', 'brochure', 'rider premiums shall be levied through level rider'),
 },
}
