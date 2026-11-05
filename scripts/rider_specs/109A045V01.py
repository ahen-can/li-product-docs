from rider_json import L
SLUG = 'absli'
Q0 = 'Additional Life cover over and above the base policy at nominal premium'
NC = 'The rider is a term cover with terminal illness acceleration only.'
SPEC = {
 'rider': {
  'name': L('ABSLI Suraksha Term Rider Plus', 'n/a', 'brochure', 'SURAKSHA TERM RIDER PLUS'),
  'uin': L('109A045V01', 'n/a', 'policy', '109A045V01'),
  'linked_or_non_linked': L('linked-base term rider (UIN series A); rider premium paid with the base premium', 'n/a', 'brochure', 'Rider due premiums are required to be paid along with the base policy premium.'),
  'attached_to_ulips': L('see results/ulip_rider_map.csv', 'n/a', None, None, ''),
 },
 'benefits': {
  'waiver_of_premium': L('not covered', 'not covered', 'brochure', Q0, NC),
  'waiver_on_death_of_life_assured': L('not covered', 'not covered', 'brochure', Q0, NC),
  'waiver_on_death_or_illness_of_proposer': L('not covered', 'not covered', 'brochure', Q0, NC),
  'critical_illness': L('No critical illness benefit. Terminal illness accelerates the death benefit.', 'not covered', 'brochure', Q0, NC),
  'accidental_death': L('not covered separately; death from any cause is covered by the term cover.', 'not covered', 'brochure', Q0, NC),
  'accidental_disability': L('not covered', 'not covered', 'brochure', Q0, NC),
  'term_cover': L('On death or diagnosis of terminal illness, whichever is first, a lump sum of the higher of the rider sum assured or 105% of total rider premiums paid. Rider sum assured at most 100% of the base plan sum assured.', 'covered', 'brochure', 'Sum Assured on Death or terminal illness will be the highest of'),
  'hospital_cash': L('not covered', 'not covered', 'brochure', Q0, NC),
  'other': L('Lower premium for female lives. Inbuilt health management services.', 'covered', 'brochure', 'Lower premium for female lives'),
 },
 'terms': {
  'rider_term': L('Minimum 6 years, maximum 55 years; maximum maturity age 80.', 'n/a', 'brochure', 'Maximum: 55 Years'),
  'premium_paying_rules': L('Limited pay 5, 6, 7, 8, 10, 12, 15 or 20 years. Modes as the base plan. Can be opted at base policy inception. Rider premium may not exceed 30% of the base premium.', 'n/a', 'brochure', 'Limited Pay: 5'),
  'entry_age': L('18 to 65 years; maximum maturity age 80', 'n/a', 'brochure', '18 – 65 years'),
  'sum_assured_limits': L('Minimum Rs 5,00,000. Maximum per board-approved underwriting policy, at most 100% of the base plan sum assured.', 'n/a', 'brochure', 'Minimum: Rs. 5,00,000'),
  'premium_deduction': L('Separate rider premium paid along with the base policy premium.', 'n/a', 'brochure', 'Rider due premiums are required to be paid along with the base policy premium.'),
 },
}
