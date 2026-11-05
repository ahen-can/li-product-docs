from rider_json import L
SLUG = 'hdfc-life'
LINKED_ULIPS = ['101L180V01 Sampoorn Nivesh Plus', '101L187V04 Smart Protect Plus', '101L191V02 Click 2 Invest Plus']
NC = 'Three options only: personal accident (A), accidental death (B) and cancer (C).'
Q0 = 'There are three benefit options available under the rider:'
SPEC = {
 'rider': {
  'name': L('HDFC Life Protect Plus Rider - Linked', 'n/a', 'brochure', 'Protect Plus Rider - Linked'),
  'uin': L('101A037V01', 'n/a', 'brochure', 'UIN:101A037V01'),
  'linked_or_non_linked': L('linked-base rider, non-participating, pure risk premium, individual life/health rider; separate rider premium', 'n/a', 'brochure', 'A Linked, Non- Participating, pure risk premium, Individual Life/Health rider'),
  'attached_to_ulips': L(LINKED_ULIPS + ['101L133V03 Click 2 Wealth'], 'n/a', None, None, 'Linked from the product pages of these four ULIPs. The brochure lists compatible base products (Click 2 Wealth, Sampoorn Nivesh and others). See results/ulip_rider_map.csv.'),
 },
 'benefits': {
  'waiver_of_premium': L('The rider\'s own premium is waived for three policy years after an early-stage cancer or carcinoma in situ claim (option C). Base policy premiums are not waived.', 'not covered', 'brochure', 'under this rider option will be waived for a period of three policy years', 'Waives only this rider\'s premium.'),
  'waiver_on_death_of_life_assured': L('not covered', 'not covered', 'brochure', Q0, NC),
  'waiver_on_death_or_illness_of_proposer': L('not covered', 'not covered', 'brochure', Q0, NC),
  'critical_illness': L('Option C, cancer cover only: lump sum on carcinoma in situ, early-stage or major cancer (25% of rider sum assured for early stage and carcinoma in situ; major cancer pays the balance). No cover for other critical illnesses.', 'covered as an option', 'brochure', 'Carcinoma-in-situ or Malignant cancer', 'Cancer only, not a general critical illness cover.'),
  'accidental_death': L('Option B: accidental death, rider sum assured to the nominee, death within 180 days of the injury. Option A also pays accidental death. A and B cannot be chosen together.', 'covered as an option', 'brochure', 'In an unforeseen event of death of the Life Assured due to accident during the rider term, 100% of the rider sum assured will be paid to the nominee.'),
  'accidental_disability': L('Option A, personal accident cover: accidental total permanent disability and accidental partial permanent disability, as well as accidental death.', 'covered as an option', 'brochure', 'Accidental Total Permanent Disability(ATPD) and/or'),
  'term_cover': L('not covered', 'not covered', 'brochure', Q0, NC),
  'hospital_cash': L('not covered', 'not covered', 'brochure', Q0, NC),
  'other': L('not stated', 'not stated'),
 },
 'terms': {
  'rider_term': L('Options A and B: minimum 1 month, maximum the outstanding policy term of the base policy. Option C: 60 months.', 'n/a', 'brochure', 'Option C – 60 months'),
  'premium_paying_rules': L('Options A and B: premium payment term from 1 month up to the outstanding premium payment term of the base policy. Option C: same as the rider term. Opted at inception or on any policy anniversary. Non-annual factors 0.51, 0.26, 0.0875.', 'n/a', 'brochure', 'Half-yearly 0.51'),
  'entry_age': L('18 to 74 years for options A and B (maturity age 75); 18 to 65 for option C (maturity age 85)', 'n/a', 'brochure', 'Option A & Option B - 74 years'),
  'sum_assured_limits': L('Minimum Rs 5,000 for options A and B, Rs 50,000 for option C. No maximum, subject to underwriting; currently at most the base policy sum assured.', 'n/a', 'brochure', 'Option A & Option B – Rs. 5,000'),
  'premium_deduction': L('Separate level rider premium. The brochure says only an additional level rider premium is charged for rider risk cover and no charge deduction is made.', 'n/a', 'brochure', 'Only an additional level rider premium will be charged for rider risk cover and no charge deduction will be made.'),
 },
}
