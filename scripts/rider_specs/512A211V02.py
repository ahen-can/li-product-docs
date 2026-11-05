from rider_json import L
SLUG = 'lic'
Q0 = 'LIC’s Linked Accidental Death Benefit Rider is an Individual, Linked, Life'
NC = 'The rider pays an accidental death benefit only.'
SPEC = {
 'rider': {
  'name': L('LIC\'s Linked Accidental Death Benefit Rider', 'n/a', 'brochure', 'Linked Accidental Death Benefit Rider'),
  'uin': L('512A211V02', 'n/a', 'brochure', 'UIN: 512A211V02'),
  'linked_or_non_linked': L('linked rider, individual life rider; charge cancelled from units', 'n/a', 'brochure', '(An Individual, Linked, Life Rider)'),
  'attached_to_ulips': L('see results/ulip_rider_map.csv', 'n/a', None, None, 'Named by Nivesh Plus, SIIP, Index Plus and Protection Plus. New Pension Plus names none.'),
 },
 'benefits': {
  'waiver_of_premium': L('not covered', 'not covered', 'brochure', Q0, NC),
  'waiver_on_death_of_life_assured': L('not covered', 'not covered', 'brochure', Q0, NC),
  'waiver_on_death_or_illness_of_proposer': L('not covered', 'not covered', 'brochure', Q0, NC),
  'critical_illness': L('not covered', 'not covered', 'brochure', Q0, NC),
  'accidental_death': L('A sum equal to the accident benefit sum assured on death by accident within 180 days. The base policy must be in force at the time of the accident.', 'covered as an option', 'brochure', 'a sum equal to the Accident Benefit Sum'),
  'accidental_disability': L('not covered', 'not covered', 'brochure', Q0, NC),
  'term_cover': L('not covered', 'not covered', 'brochure', Q0, NC),
  'hospital_cash': L('not covered', 'not covered', 'brochure', Q0, NC),
  'other': L('No maturity, paid-up or surrender value. Can be cancelled any time but not re-opted.', 'covered', 'brochure', 'No maturity benefit is payable under this Rider'),
 },
 'terms': {
  'rider_term': L('(70 minus age at entry) years or the base plan policy term, whichever is less; minimum 5 years. Rider cover ceases at age 70.', 'n/a', 'brochure', 'Rider Covering Ceasing Age : 70 years'),
  'premium_paying_rules': L('No separate premium. Charged monthly through unit cancellation. Can be opted at commencement or at any time during the policy term.', 'n/a', 'brochure', 'This rider can be opted at any time during the term of the policy or'),
  'entry_age': L('18 years (completed) to 65 years (nearest birthday)', 'n/a', 'brochure', 'Maximum Age at entry : 65 years'),
  'sum_assured_limits': L('Minimum Rs 10,000, multiples of Rs 5,000. Maximum aggregate accident benefit across all LIC policies on one life: Rs 100 lakh (Rs 200 lakh including Jeevan Shiromani).', 'n/a', 'brochure', 'Minimum Accident Benefit Sum Assured'),
  'premium_deduction': L('Rs 0.40 per thousand accident benefit sum assured a year (Rs 0.80 for police duty), levied monthly by cancelling units out of the policyholder fund value.', 'n/a', 'brochure', 'by cancelling proportionate number'),
 },
}
