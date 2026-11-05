from rider_json import L
SLUG = 'absli'
Q0 = 'Protection against up to 64 Critical Illnesses (CIs)'
NC = 'The rider pays a lump sum on critical illness only.'
SPEC = {
 'rider': {
  'name': L('ABSLI Comprehensive Critical Illness Rider', 'n/a', 'brochure', 'ABSLI COMPREHENSIVE CRITICAL ILLNESS RIDER'),
  'uin': L('109A041V01', 'n/a', 'policy', '109A041V01'),
  'linked_or_non_linked': L('individual linked non-participating rider; rider premium', 'n/a', 'brochure', 'An Individual Linked Non-Participating Rider'),
  'attached_to_ulips': L('see results/ulip_rider_map.csv', 'n/a', None, None, 'Named by 7 of 10 ABSLI ULIPs.'),
 },
 'benefits': {
  'waiver_of_premium': L('not covered', 'not covered', 'brochure', Q0, NC),
  'waiver_on_death_of_life_assured': L('not covered', 'not covered', 'brochure', Q0, NC),
  'waiver_on_death_or_illness_of_proposer': L('not covered', 'not covered', 'brochure', Q0, NC),
  'critical_illness': L('Three options: Silver (10 critical illnesses), Gold (25), Platinum (64). Minor critical illness (5 minor conditions): the lower of 25% of rider sum assured or Rs 5,00,000, and the rider continues for the balance. Major: 100% of rider sum assured less minor claims paid, lump sum if the life survives 14 days; the rider then ends.', 'covered as an option', 'brochure', 'Minor CI: Lower of 25% of Rider Sum Assured or R5,00,000'),
  'accidental_death': L('not covered', 'not covered', 'brochure', Q0, NC),
  'accidental_disability': L('not covered', 'not covered', 'brochure', Q0, NC),
  'term_cover': L('not covered', 'not covered', 'brochure', Q0, NC),
  'hospital_cash': L('not covered', 'not covered', 'brochure', Q0, NC),
  'other': L('not stated', 'not stated'),
 },
 'terms': {
  'rider_term': L('Limited pay: minimum PPT + 1, maximum the base policy term. Regular pay: same as the base policy term, minimum 5 years; 5 to 30 years overall.', 'n/a', 'brochure', 'Same as policy term of base'),
  'premium_paying_rules': L('Limited pay 5 to 20 years or regular pay. All premium frequencies. Can be opted at inception or at any policy anniversary.', 'n/a', 'brochure', 'Flexibility to opt for limited pay or regular pay option as per your'),
  'entry_age': L('18 to 55 years; cover ceases at age 70', 'n/a', 'brochure', '18 to 55 years'),
  'sum_assured_limits': L('Minimum Rs 1,00,000. Maximum Rs 1.5 crore, subject to underwriting; not above the base sum assured.', 'n/a', 'brochure', 'R1,50,00,000'),
  'premium_deduction': L('not stated', 'not stated', None, None, 'Not stated in the brochure text read. Needs a second read.'),
 },
}
