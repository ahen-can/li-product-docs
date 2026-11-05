from rider_json import L
SLUG = 'ageas-federal'
Q0 = 'Choose between two variants: Critical Protect covering 30 illnesses or'
NC = 'The rider pays a lump sum on critical illness only.'
SPEC = {
 'rider': {
  'name': L('Ageas Federal Life Insurance Linked Critical Shield Rider', 'n/a', 'brochure', 'Linked Critical Shield Rider'),
  'uin': L('135A038V01', 'n/a', 'brochure', '(UIN: 135A038V01)'),
  'linked_or_non_linked': L('linked individual health pure risk rider; rider premium', 'n/a', 'brochure', 'A Linked Individual Health Pure Risk Rider'),
  'attached_to_ulips': L('see results/ulip_rider_map.csv', 'n/a', None, None, 'Named by 4 of the 6 Ageas ULIPs. The policy document is linked from a different storage account than the other rider files.'),
 },
 'benefits': {
  'waiver_of_premium': L('not covered', 'not covered', 'brochure', Q0, NC),
  'waiver_on_death_of_life_assured': L('not covered', 'not covered', 'brochure', Q0, NC),
  'waiver_on_death_or_illness_of_proposer': L('not covered', 'not covered', 'brochure', Q0, NC),
  'critical_illness': L('Lump sum on diagnosis of a covered critical illness. Two variants: Critical Protect (30 illnesses) and Critical Protect Plus (50 illnesses).', 'covered as an option', 'brochure', 'Critical Protect covering 30 illnesses or'),
  'accidental_death': L('not covered', 'not covered', 'brochure', Q0, NC),
  'accidental_disability': L('not covered', 'not covered', 'brochure', Q0, NC),
  'term_cover': L('not covered', 'not covered', 'brochure', Q0, NC),
  'hospital_cash': L('not covered', 'not covered', 'brochure', Q0, NC),
  'other': L('not stated', 'not stated'),
 },
 'terms': {
  'rider_term': L('Minimum 12 months (single and regular pay) or 60 months (limited pay); maximum 240 months. Within the base policy term.', 'n/a', 'brochure', 'Max: 240 months'),
  'premium_paying_rules': L('Single, limited (36 to 180 months) or regular pay (up to 240 months). Payment mode as the base plan. Total rider premium at most 100% of base plan premiums.', 'n/a', 'brochure', 'The total Rider Premium shall not exceed 100% of premiums'),
  'entry_age': L('18 to 65 years; maturity age 19 to 75', 'n/a', 'brochure', 'Maximum 65 years'),
  'sum_assured_limits': L('Minimum Rs 50,000. No maximum, subject to underwriting; not above the base product sum assured.', 'n/a', 'brochure', 'The Rider Sum Assured cannot be higher than Sum'),
  'premium_deduction': L('not stated', 'not stated', None, None, 'The brochure text read does not say whether the rider premium is separate or from units. The Accident Care rider says it is payable in addition to the base premium.'),
 },
}
