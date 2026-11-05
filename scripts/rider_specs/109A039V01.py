from rider_json import L
SLUG = 'absli'
Q0 = 'ABSLI Waiver of Premium Rider'
NC = 'The rider is a premium waiver only.'
SPEC = {
 'rider': {
  'name': L('ABSLI Waiver of Premium Rider (linked)', 'n/a', 'brochure', 'Aditya Birla Sun Life Insurance Waiver of Premium rider'),
  'uin': L('109A039V01', 'n/a', 'policy', '109A039V01'),
  'linked_or_non_linked': L('linked rider (brochure carries the linked-products risk statement); separate rider premium', 'n/a', 'brochure', 'Linked Insurance Products do not offer any liquidity'),
  'attached_to_ulips': L('see results/ulip_rider_map.csv', 'n/a', None, None, 'Named by 9 of 10 ABSLI ULIPs; shown as not applicable in Smart Wealth Pension Plan.'),
 },
 'benefits': {
  'waiver_of_premium': L('If the proposer becomes completely disabled by illness or accident, is diagnosed with one of 4 specified critical illnesses (heart attack, cancer and others), or dies (if not the life insured), the benefits under the base policy and all riders remain intact with no future premiums payable, for the rest of the policy term or until the proposer reaches 70. Only possible when taken at policy issue. Cover under this rider ends after a claim.', 'covered as an option', 'brochure', 'no future premiums payable by you throughout the rest of the policy term', 'Unambiguous: the benefits "under the base policy and all riders" stay intact with no future premiums payable. The events are the proposer\'s.'),
  'waiver_on_death_of_life_assured': L('not covered', 'not covered', 'brochure', Q0, NC),
  'waiver_on_death_or_illness_of_proposer': L('Death of the proposer (if not the life insured), the proposer\'s total and permanent disability (180 days) or one of 4 critical illnesses (survive 30 days).', 'covered as an option', 'brochure', 'Death of the proposer (if not the life insured)'),
  'critical_illness': L('No payout. Four listed major critical illnesses only trigger the waiver.', 'not covered', 'brochure', 'We cover 4 major illnesses under this benefit', 'See waiver_of_premium.'),
  'accidental_death': L('not covered', 'not covered', 'brochure', Q0, NC),
  'accidental_disability': L('No payout. Disability of the proposer only triggers the waiver.', 'not covered', 'brochure', Q0, NC),
  'term_cover': L('not covered', 'not covered', 'brochure', Q0, NC),
  'hospital_cash': L('not covered', 'not covered', 'brochure', Q0, NC),
  'other': L('not stated', 'not stated'),
 },
 'terms': {
  'rider_term': L('Same as the base policy or until the proposer is 70, whichever is earlier.', 'n/a', 'brochure', 'whichever is earlier'),
  'premium_paying_rules': L('Premium paying term same as the rider term. Pay mode as the base policy. Can be opted only at policy issue.', 'n/a', 'brochure', 'You may opt for this rider only at the time of policy issue.'),
  'entry_age': L('18 to 65 years; age at the end of the rider term at most 70', 'n/a', 'brochure', '18 – 65 years'),
  'sum_assured_limits': L('not stated', 'not stated', None, None, 'No separate rider sum assured in the brochure; the benefit is the waived future premium.'),
  'premium_deduction': L('not stated', 'not stated', None, None, 'The brochure and policy text read do not say whether the rider premium is separate or from units. Needs a second read.'),
 },
}
