from rider_json import L
SLUG = 'tata-aia'
Q = 'An exclusive rider designed for the Proposer of the base plan'
NC = 'The rider is a premium waiver for the proposer only.'
SPEC = {
 'rider': {
  'name': L('Tata AIA Life Insurance Waiver of Premium Plus (Linked) Rider', 'n/a', 'brochure', 'Waiver of Premium Plus (Linked) Rider'),
  'uin': L('110A025V03', 'n/a', 'brochure', 'UIN: 110A025V03', 'The rider page publishes V03. ULIP product pages name V02 and V03 or later. V02 documents were not found.'),
  'linked_or_non_linked': L('linked rider, individual health insurance rider; charge cancelled from units', 'n/a', 'brochure', 'Linked, Individual, Health Insurance Rider'),
  'attached_to_ulips': L('see results/ulip_rider_map.csv', 'n/a', None, None, 'Not available with the Future Secure and Family Secure plan options of i Systematic.'),
 },
 'benefits': {
  'waiver_of_premium': L('If the proposer (who is different from the life assured) dies or becomes totally and permanently disabled by accident or sickness, all future premiums of the basic plan are waived and the rider charge stops, for the rest of the premium paying term or until the proposer reaches 70.', 'covered as an option', 'brochure', 'Then we will waive all the future premiums of the basic plan', 'Unambiguous: "basic plan". Premium payer is the proposer, not the life assured.'),
  'waiver_on_death_of_life_assured': L('not covered (events are those of the proposer)', 'not covered', 'brochure', Q, NC),
  'waiver_on_death_or_illness_of_proposer': L('Death of the proposer, or total and permanent disability of the proposer (12 months continuous), waives the base plan premiums. No critical illness trigger.', 'covered as an option', 'brochure', '2. Death of the Proposer'),
  'critical_illness': L('not covered', 'not covered', 'brochure', Q, NC),
  'accidental_death': L('not covered', 'not covered', 'brochure', Q, NC),
  'accidental_disability': L('No payout. Disability of the proposer only triggers the waiver.', 'not covered', 'brochure', Q, NC),
  'term_cover': L('not covered', 'not covered', 'brochure', Q, NC),
  'hospital_cash': L('not covered', 'not covered', 'brochure', Q, NC),
  'other': L('not stated', 'not stated'),
 },
 'terms': {
  'rider_term': L('Minimum 5 years. Maximum: until the end of the base plan premium payment term or proposer age 70, whichever is earlier.', 'n/a', 'brochure', 'Till premium payment term of the'),
  'premium_paying_rules': L('Rider charge deducted for the maximum rider coverage term. Rider term equals the base plan premium payment term.', 'n/a', 'brochure', 'with rider coverage term equal to the premium paying term'),
  'entry_age': L('18 to 65 years; maximum maturity age 70', 'n/a', 'brochure', 'Maximum Age at entry 65 years'),
  'sum_assured_limits': L('Sum of all future premiums of the basic plan to be waived.', 'n/a', 'brochure', 'Sum of all the future premiums'),
  'premium_deduction': L('Charge recovered monthly by cancellation of units from the unit fund of the base policy.', 'n/a', 'brochure', 'The charge for the rider will be recovered monthly by cancellation'),
 },
}
