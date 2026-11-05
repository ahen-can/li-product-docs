from rider_json import L
SLUG = 'tata-aia'
Q0 = 'choose multiple risk covers from a list of 5 which include disability'
SPEC = {
 'rider': {
  'name': L('Tata AIA Life Insurance Linked Comprehensive Health Rider', 'n/a', 'brochure', 'Tata AIA Life Insurance Linked Comprehensive Health Rider'),
  'uin': L('110A031V02', 'n/a', 'brochure', 'UIN: 110A031V02', 'Brochure supplied by the user. The site page for this rider was not found; ULIP product pages name V02 and V03. No policy document yet.'),
  'linked_or_non_linked': L('non-linked, non-participating individual health rider; separate premium', 'n/a', 'brochure', 'A Non-Linked, Non- Participating Individual Health rider', 'Named "Linked" because it attaches to linked ULIPs; the brochure calls it non-linked.'),
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
  'other': L('Return of balance premium option; benefits as lump sum, income up to 10 years or both; cover can be extended to loved ones.', 'covered as an option', 'brochure', 'Option to receive return of balance premiums on maturity'),
 },
 'terms': {
  'rider_term': L('Without return of balance premium: 5 to 57 years (cancer care to 70). With return of balance premium: 10 to 57 years (cancer care to 70). Not beyond the base plan term.', 'n/a', 'brochure', 'Benefit Option Terms and Premium Payment Options'),
  'premium_paying_rules': L('Single, limited or regular pay (see the brochure term table). Options can be added at inception or at a policy anniversary.', 'n/a', 'brochure', 'Benefit Option Terms and Premium Payment Options'),
  'entry_age': L('18 to 65 years (Multistage Cancer Care from age 5); maturity age 75', 'n/a', 'brochure', 'Partial Disability Benefit 18 65 75'),
  'sum_assured_limits': L('Rider sum assured is the maximum of the sum assured chosen under each benefit option; see the brochure for the formula (11 times annualised premium for limited and regular pay, 105% of premiums paid).', 'n/a', 'brochure', '105% of Total Premiums Paid'),
  'premium_deduction': L('not stated', 'not stated', None, None, 'The text read does not say whether the premium is separate or taken from units. Non-linked rider; assumed separate. Needs a second read.'),
 },
}
