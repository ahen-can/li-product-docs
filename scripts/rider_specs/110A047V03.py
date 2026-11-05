from rider_json import L
SLUG = 'tata-aia'
Q0 = 'choose multiple risk covers from a list of 5 which include disability'
SPEC = {
 'rider': {
  'name': L('Tata AIA Vitality Health Plus', 'n/a', 'brochure', 'Tata AIA Vitality Health Plus'),
  'uin': L('110A047V03', 'n/a', 'brochure', 'UIN: 110A047V03', 'Rider page publishes V03; ULIP product pages name V02.'),
  'linked_or_non_linked': L('non-linked, non-participating individual health rider; separate premium', 'n/a', 'brochure', 'A Non-Linked, Non- Participating Individual Health rider', 'Named on linked ULIP product pages even though the rider itself is non-linked.'),
  'attached_to_ulips': L('see results/ulip_rider_map.csv', 'n/a', None, None, ''),
 },
 'benefits': {
  'waiver_of_premium': L('not covered', 'not covered', 'brochure', Q0, 'Five options: accidental disability, multistage critical illness, cancer, cardiac and hospital cover. No premium waiver option found in the brochure.'),
  'waiver_on_death_of_life_assured': L('not covered', 'not covered', 'brochure', Q0),
  'waiver_on_death_or_illness_of_proposer': L('not covered', 'not covered', 'brochure', Q0),
  'critical_illness': L('Multistage CritiCare: 39 critical illnesses with minor stage claims at 25% and major at 100% of the insured amount, multiple claims. Cancer Care: early and late stage cancers. Cardiac Care: 14 minor and 8 major cardiac ailments. Lump sum, income up to 10 years, or both.', 'covered as an option', 'brochure', '39 Critical Illness covered'),
  'accidental_death': L('not covered', 'not covered', 'brochure', Q0),
  'accidental_disability': L('Accidental Disability Care: total and permanent disability 100%, partial permanent disability by schedule (arm 50 to 60%, leg 40 to 60%, each eye 50%, each ear 30%), multiple claims, double benefit in listed public accidents.', 'covered as an option', 'brochure', 'Total and Permanent Disability 100%'),
  'term_cover': L('not covered', 'not covered', 'brochure', Q0),
  'hospital_cash': L('HospiCare: fixed amount on hospitalisation, ICU benefit and a recuperation benefit for stays of 7 days or more.', 'covered as an option', 'brochure', 'Pays fixed amount on'),
  'other': L('Vitality wellness programme with rewards for healthy habits.', 'covered', 'brochure', 'Tata AIA Vitality'),
 },
 'terms': {
  'rider_term': L('Minimum policy period 12 to 14 months depending on pay mode; maximum 60 months across all options; not beyond the base plan term.', 'n/a', 'brochure', 'Across all benefit options: 60 months'),
  'premium_paying_rules': L('Regular, limited or single pay per option.', 'n/a', 'brochure', 'Regular Pay Limited Pay Single Pay'),
  'entry_age': L('18 to 65 years (Cancer Care from age 5); maturity age 75', 'n/a', 'brochure', 'Accidental 18 65 75'),
  'sum_assured_limits': L('Minimum Rs 25,000 per option; maximum subject to underwriting and not above the base plan death benefit.', 'n/a', 'brochure', 'Rider Sum Assured cannot exceed the Death Benefit at inception of'),
  'premium_deduction': L('not stated', 'not stated', None, None, 'The text read does not say whether the premium is separate or taken from units. Non-linked rider; assumed separate. Needs a second read.'),
 },
}
