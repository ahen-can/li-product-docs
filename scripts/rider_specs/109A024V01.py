from rider_json import L
SLUG = 'absli'
Q0 = 'ABSLI Accidental Death Benefit Rider Plus offers additional financial'
NC = 'The rider pays an accidental death benefit only.'
SPEC = {
 'rider': {
  'name': L('ABSLI Accidental Death Benefit Rider Plus (linked)', 'n/a', 'brochure', 'Accidental Death Beneﬁt Rider Plus'),
  'uin': L('109A024V01', 'n/a', 'policy', '109A024V01'),
  'linked_or_non_linked': L('linked rider (brochure carries the linked-products risk statement); rider premium', 'n/a', 'brochure', 'Linked Insurance Products do not offer any liquidity'),
  'attached_to_ulips': L('see results/ulip_rider_map.csv', 'n/a', None, None, 'Named by 9 of 10 ABSLI ULIPs.'),
 },
 'benefits': {
  'waiver_of_premium': L('not covered', 'not covered', 'brochure', 'Maturity Beneﬁt Not applicable', NC),
  'waiver_on_death_of_life_assured': L('not covered', 'not covered', 'brochure', 'Maturity Beneﬁt Not applicable', NC),
  'waiver_on_death_or_illness_of_proposer': L('not covered', 'not covered', 'brochure', 'Maturity Beneﬁt Not applicable', NC),
  'critical_illness': L('not covered', 'not covered', 'brochure', 'Maturity Beneﬁt Not applicable', NC),
  'accidental_death': L('100% of the rider sum assured to the nominee on death by accident within 180 days, if the rider is in force on the accident date. Premiums collected after the accident are refunded with interest.', 'covered as an option', 'brochure', 'we will pay 100% of the rider sum assured to the nominee'),
  'accidental_disability': L('not covered', 'not covered', 'brochure', 'Maturity Beneﬁt Not applicable', NC),
  'term_cover': L('not covered', 'not covered', 'brochure', 'Maturity Beneﬁt Not applicable', NC),
  'hospital_cash': L('not covered', 'not covered', 'brochure', 'Maturity Beneﬁt Not applicable', NC),
  'other': L('No maturity benefit. Reduced paid-up for limited pay if the base plan allows it. Surrender value after 2 full years of premiums (limited pay) or immediately (single pay).', 'covered', 'brochure', 'There is no surrender beneﬁt offered for regular pay option under this rider.'),
 },
 'terms': {
  'rider_term': L('Same as the base plan or until the life insured is 80, whichever is earlier. Minimum 5 years, maximum 62 years.', 'n/a', 'brochure', 'Maximum: 62 years'),
  'premium_paying_rules': L('Same as the base plan. Limited pay 5 to 61 years, regular pay 5 to 62 years, single pay.', 'n/a', 'brochure', 'Same as base plan (Single Pay | Limited Pay | Regular Pay)'),
  'entry_age': L('18 to 65 years; age at the end of the rider term at most 80', 'n/a', 'brochure', 'Maximum age at the end of rider term is 80 years'),
  'sum_assured_limits': L('Minimum Rs 1,00,000. Maximum Rs 2 crore, at most 300% of the base plan sum assured.', 'n/a', 'brochure', 'subject to maximum of 300% sum'),
  'premium_deduction': L('not stated', 'not stated', None, None, 'Not stated in the brochure text read. Needs a second read.'),
 },
}
