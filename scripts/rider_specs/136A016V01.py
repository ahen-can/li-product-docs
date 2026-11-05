from rider_json import L
SLUG = 'canara-hsbc'
Q0 = 'Op'
NC = 'The rider has two options only: accidental death and accidental total and permanent disability.'
Q1 = 'Keep their tomorrows safe with Accidental Death Benefit and'
SPEC = {
 'rider': {
  'name': L('Canara HSBC Life Insurance Accidental Benefit Rider (Linked)', 'n/a', 'brochure', 'Accidental Benefit Rider (Linked)'),
  'uin': L('136A016V01', 'n/a', 'policy', '136A016V01'),
  'linked_or_non_linked': L('named "Linked" because it attaches to linked base policies; the brochure header calls it an individual non-linked non-participating pure risk rider; separate rider premium', 'n/a', 'brochure', 'An Individual Non-Linked Non-Participating Pure Risk Insurance Rider'),
  'attached_to_ulips': L('see results/ulip_rider_map.csv', 'n/a', None, None, 'Named by 3 of the 8 Canara HSBC ULIPs (Wealth, Alpha Wealth, SecureInvest).'),
 },
 'benefits': {
  'waiver_of_premium': L('not covered', 'not covered', 'brochure', Q1, NC),
  'waiver_on_death_of_life_assured': L('not covered', 'not covered', 'brochure', Q1, NC),
  'waiver_on_death_or_illness_of_proposer': L('not covered', 'not covered', 'brochure', Q1, NC),
  'critical_illness': L('not covered', 'not covered', 'brochure', Q1, NC),
  'accidental_death': L('Lump sum on accidental death, up to 3 times the base sum assured. Return of premium available as a maturity benefit.', 'covered as an option', 'brochure', 'up to 3 '),
  'accidental_disability': L('Lump sum on accidental total and permanent disability.', 'covered as an option', 'brochure', 'Accidental Total & Permanent Disability Benefit'),
  'term_cover': L('not covered', 'not covered', 'brochure', Q1, NC),
  'hospital_cash': L('not covered', 'not covered', 'brochure', Q1, NC),
  'other': L('Return of premium: an amount equal to the total premiums paid on maturity.', 'covered as an option', 'brochure', 'Return of Premium means an amount equal to the Total Premiums Paid'),
 },
 'terms': {
  'rider_term': L('5 to 57 years (single or regular pay), 6 to 57 (limited pay).', 'n/a', 'brochure', 'Policy Term (in Yrs)'),
  'premium_paying_rules': L('Single, limited (up to 56 years) or regular pay (up to 57 years). Frequency as the base policy. Can be opted at inception only. Rider premium at most 30% of the base premium.', 'n/a', 'brochure', 'The Rider can be opted along with base policy at incep'),
  'entry_age': L('18 to 65 years; maturity age 23 to 75', 'n/a', 'brochure', 'Age at entry 18 65'),
  'sum_assured_limits': L('Minimum Rs 50,000. No maximum, subject to board-approved underwriting and regulations; up to 3 times the base sum assured for accidental death.', 'n/a', 'brochure', 'Sum Assured (Rs) 50,000'),
  'premium_deduction': L('not stated', 'not stated', None, None, 'Not stated in the brochure text read. Needs a second read.'),
 },
}
