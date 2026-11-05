from rider_json import L
SLUG = 'hdfc-life'
LINKED_ULIPS = ['101L180V01 Sampoorn Nivesh Plus', '101L187V04 Smart Protect Plus', '101L191V02 Click 2 Invest Plus']
Q0 = 'Comprehensive protection against death, terminal illness and disability.'
SPEC = {
 'rider': {
  'name': L('HDFC Life LiveWell Rider - Linked', 'n/a', 'brochure', 'LiveWell Rider - Linked'),
  'uin': L('101A036V02', 'n/a', 'brochure', 'LiveWell Rider – Linked', 'The brochure from the product page does not print the UIN in this line; the site files and the product page name 101A036V02. The policy bond stored here prints 101A036V01, one version older.'),
  'linked_or_non_linked': L('linked-base rider, non-participating, individual, pure risk premium / savings, life/health rider; separate rider premium', 'n/a', 'brochure', 'A Linked, Non- Participating Individual, Pure Risk Premium/ Savings, Life/Health Insurance Rider'),
  'attached_to_ulips': L(LINKED_ULIPS, 'n/a', None, None, 'Linked from the product pages of these three ULIPs. The brochure also lists Sampoorn Nivesh Plus, Smart Protect Plus and Click to Invest Plus as available base products.'),
 },
 'benefits': {
  'waiver_of_premium': L('not covered', 'not covered', 'brochure', Q0, 'Options are death cover, accidental death, personal accident and daily hospital cash.'),
  'waiver_on_death_of_life_assured': L('not covered', 'not covered', 'brochure', Q0),
  'waiver_on_death_or_illness_of_proposer': L('not covered', 'not covered', 'brochure', Q0),
  'critical_illness': L('No critical illness benefit. Terminal illness acceleration of the death cover is paid for a life assured up to age 80, capped at Rs 2 crore.', 'not covered', 'brochure', 'the maximum amount of Rider Sum Assured that can be accelerated under this benefit is Rs 2 crore'),
  'accidental_death': L('Option B: accidental death, lump sum of the highest of the rider sum assured, 7 times the annualised rider premium (1.25 times for single pay) or 105% of rider premiums paid. Option C also pays accidental death. Can be paid as monthly income for 10 years.', 'covered as an option', 'brochure', 'Rider Sum Assured for Option B shall be a lump sum benefit which is the highest of:'),
  'accidental_disability': L('Option C, personal accident cover: monthly income of 1% of rider sum assured for 10 years on accidental total permanent disability; accidental partial permanent disability pays scheduled percentages (50% for loss of a hand or foot).', 'covered as an option', 'brochure', 'a regular monthly benefit equal to 1% of Rider Sum Assured, is payable to the Life Assured for'),
  'term_cover': L('Option A, death cover: on death of the life assured, the highest of the rider sum assured, 10 times the annualised rider premium (1.25 times for single pay) or 105% of total rider premiums paid. Return of premium option available. Includes terminal illness acceleration.', 'covered as an option', 'brochure', 'The death benefit is highest of'),
  'hospital_cash': L('Option D, daily hospitalisation cash and surgical care: 1% of rider sum assured a day (2% in ICU), up to 20 days a policy year and 100 days in total, plus surgical care benefit up to 100% of rider sum assured.', 'covered as an option', 'brochure', 'Hospitalization Benefit (Non-ICU): Benefit amount shall be equal to 1% of the Rider Sum Assured'),
  'other': L('Wellness benefits worth 100% of the annual rider premium, redeemable only through the Life Rewards app (OPD consultations, preventive health check-up, tele consultation, healthy living program). Double benefit if an accident happens in listed circumstances.', 'covered', 'brochure', 'Get double payout in case of accident occurs under listed circumstances with Double'),
 },
 'terms': {
  'rider_term': L('Minimum 5 years. Maximum for options A, B and C: the outstanding policy term of the base policy. Option D: 5 years.', 'n/a', 'brochure', 'Option D: 5 years'),
  'premium_paying_rules': L('Single, limited or regular pay (the 10 times and 1.25 times multiples in the benefit formulas refer to limited or regular and single pay). Opted at inception or on any premium due date of the base plan.', 'n/a', 'brochure', 'This rider can be opted at inception or subsequently on any premium due date of the base plan'),
  'entry_age': L('18 to 65 years; maturity age 23 minimum; maximum 85 (option A), 75 (options B and C), 70 (option D)', 'n/a', 'brochure', 'Option A: 85 years'),
  'sum_assured_limits': L('Minimum Rs 10,000 for options A, B and C; Rs 1,00,000 for option D. Maximum: up to the base policy sum assured for options A, C and D; up to three times the base policy sum assured for option B. Subject to board-approved underwriting.', 'n/a', 'brochure', 'Option B: Up to three times of'),
  'premium_deduction': L('Separate rider premium, payable along with the base premium. The brochure does not say the premium comes out of the fund.', 'n/a', 'brochure', 'as long as the premium due is paid along with the base premium', 'No sentence on fund deduction found.'),
 },
}
