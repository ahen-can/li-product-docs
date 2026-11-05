from rider_json import L
SLUG = 'canara-hsbc'
Q0 = 'Receive a lump sum amount when diagnosed with the specified 40'
NC = 'The rider pays a lump sum on critical illness only.'
SPEC = {
 'rider': {
  'name': L('Canara HSBC Life Insurance Linked Critical Illness Benefit Rider', 'n/a', 'policy', 'Critical Illness Benefit Rider'),
  'uin': L('136A018V01', 'n/a', 'policy', '136A018V01'),
  'linked_or_non_linked': L('rider for linked base policies; separate rider premium', 'n/a', 'brochure', 'Premium rates guaranteed for the'),
  'attached_to_ulips': L('see results/ulip_rider_map.csv', 'n/a', None, None, 'Named by 3 of the 8 Canara HSBC ULIPs (Wealth, Alpha Wealth, SecureInvest).'),
 },
 'benefits': {
  'waiver_of_premium': L('not covered', 'not covered', 'brochure', Q0, NC),
  'waiver_on_death_of_life_assured': L('not covered', 'not covered', 'brochure', Q0, NC),
  'waiver_on_death_or_illness_of_proposer': L('not covered', 'not covered', 'brochure', Q0, NC),
  'critical_illness': L('Lump sum of the critical illness sum assured on first diagnosis of any of 40 specified illnesses, if the life assured survives the survival period. 90 day waiting period. The rider then ends.', 'covered', 'brochure', 'Receive a lump sum amount when diagnosed with the specified 40'),
  'accidental_death': L('not covered', 'not covered', 'brochure', Q0, NC),
  'accidental_disability': L('not covered', 'not covered', 'brochure', Q0, NC),
  'term_cover': L('not covered', 'not covered', 'brochure', Q0, NC),
  'hospital_cash': L('not covered', 'not covered', 'brochure', Q0, NC),
  'other': L('not stated', 'not stated'),
 },
 'terms': {
  'rider_term': L('Limited pay 6 to 20 years; regular pay 5 to 20 years; not beyond the base policy term or age 70.', 'n/a', 'brochure', 'Limited Pay: 6 to 20 years'),
  'premium_paying_rules': L('Limited pay 5 to 19 years or regular pay (same as policy term). Annual, semi-annual, quarterly or monthly. Opted at inception only. Rider premium at most 100% of the base premium.', 'n/a', 'brochure', 'Limited Pay: 5 to 19 years'),
  'entry_age': L('18 to 65 years; maturity age 23 to 70', 'n/a', 'brochure', 'Entry Age 18 years to 65 years'),
  'sum_assured_limits': L('Minimum Rs 50,000. Maximum Rs 50,00,000 or the base policy sum assured, whichever is lower.', 'n/a', 'brochure', 'Minimum: `50,000'),
  'premium_deduction': L('not stated', 'not stated', None, None, 'Not stated in the brochure text read. Needs a second read.'),
 },
}
