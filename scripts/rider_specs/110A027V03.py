from rider_json import L
SLUG = 'tata-aia'
Q = 'ADDL (Long Scale) benefit:'
SPEC = {
 'rider': {
  'name': L('Tata AIA Life Insurance Accidental Death and Dismemberment (Long Scale) (ADDL) Linked Rider', 'n/a', 'brochure', 'Accidental Death and Dismemberment'),
  'uin': L('110A027V03', 'n/a', 'brochure', 'UIN: 110A027V03', 'Rider page publishes V03; ULIP product pages name V02 and V03 or later.'),
  'linked_or_non_linked': L('linked rider, individual health insurance rider; charge cancelled from units', 'n/a', 'brochure', 'Linked, Individual, Health Insurance Rider'),
  'attached_to_ulips': L('see results/ulip_rider_map.csv', 'n/a', None, None, ''),
 },
 'benefits': {
  'waiver_of_premium': L('not covered', 'not covered', 'brochure', Q, 'Accidental death and dismemberment only.'),
  'waiver_on_death_of_life_assured': L('not covered', 'not covered', 'brochure', Q),
  'waiver_on_death_or_illness_of_proposer': L('not covered', 'not covered', 'brochure', Q),
  'critical_illness': L('not covered', 'not covered', 'brochure', Q),
  'accidental_death': L('100% of rider sum assured on loss of life by accident.', 'covered as an option', 'brochure', 'Loss of Life 100%'),
  'accidental_disability': L('Scheduled percentages of rider sum assured for dismemberment: 100% for loss of both eyes or two limbs, 50% for one eye or one limb, 75% hearing in both ears, 50% speech, down to 5% for a joint.', 'covered as an option', 'brochure', 'Loss of or Loss of Use of two Limbs 100%'),
  'term_cover': L('not covered', 'not covered', 'brochure', Q),
  'hospital_cash': L('not covered', 'not covered', 'brochure', Q),
  'other': L('not stated', 'not stated'),
 },
 'terms': {
  'rider_term': L('Maximum: base plan term or 70 minus age at entry, whichever is earlier.', 'n/a', 'brochure', 'Maximum Rider'),
  'premium_paying_rules': L('not stated', 'not stated', None, None, 'Not extracted. Rider charge deduction term follows the rider term.'),
  'entry_age': L('Minimum: base plan minimum or 18, whichever is higher. Maximum: base plan or 60, whichever is lower. Maximum maturity age: base plan or 70, whichever is lower.', 'n/a', 'brochure', 'As per base plan or 60 years'),
  'sum_assured_limits': L('Minimum Rs 50,000 or the base plan minimum; maximum the sum assured chosen for the base plan.', 'n/a', 'brochure', 'Minimum Sum Assured'),
  'premium_deduction': L('Charge taken by cancellation of units of the base policy.', 'n/a', 'brochure', 'cancellation of units of the base'),
 },
}
