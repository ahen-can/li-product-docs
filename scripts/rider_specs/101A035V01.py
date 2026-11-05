from rider_json import L
SLUG = 'hdfc-life'
LINKED_ULIPS = ['101L180V01 Sampoorn Nivesh Plus', '101L187V04 Smart Protect Plus', '101L191V02 Click 2 Invest Plus']
NC = 'The rider is a premium waiver only. Its benefits are waiver on death of the life assured, and waiver on disability or critical illness.'
Q0 = 'Continue to receive the benefits of the base policy without paying future premium'
SPEC = {
 'rider': {
  'name': L('HDFC Life Waiver of Premium Rider - Linked', 'n/a', 'brochure', 'Waiver of Premium Rider - Linked'),
  'uin': L('101A035V01', 'n/a', 'policy', 'UIN: 101A035V01'),
  'linked_or_non_linked': L('linked-base rider, non-participating, individual, pure risk premium, life/health rider; separate rider premium', 'n/a', 'brochure', 'A Linked, Non- Participating, Individual Pure Risk Premium, Life / Health rider'),
  'attached_to_ulips': L(LINKED_ULIPS + ['Click 2 Wealth page does not link it'], 'n/a', None, None, 'Linked from the product pages of these three ULIPs. See results/ulip_rider_map.csv.'),
 },
 'benefits': {
  'waiver_of_premium': L('Option A: on death of the life assured. Option B: on disability or diagnosis of any of 60 critical illnesses. The company waives all outstanding premiums of the base policy and of all other riders attached at inception of this rider.', 'covered as an option', 'brochure', 'The Company shall waive off all outstanding premiums of the Base Policy and all other riders attached to the base policy at inception of this rider, on the death of Life Assured', 'Unambiguous: the wording says "Base Policy". "Life Assured under the Rider shall mean the Policyholder under the Base policy", so the events are those of the premium payer.'),
  'waiver_on_death_of_life_assured': L('Option A, waiver on death. Available only if the life assured under the base policy is different from the policyholder; the policyholder opts for the rider.', 'covered as an option', 'brochure', 'Option A: Waiver of Premium on Death'),
  'waiver_on_death_or_illness_of_proposer': L('Yes. The rider\'s life assured is the policyholder of the base policy, so the waiver follows the payer\'s death, disability or critical illness.', 'covered', 'brochure', 'Life Assured under the Rider shall mean the Policyholder under the Base policy.'),
  'critical_illness': L('No payout. Diagnosis of any of 60 listed critical illnesses only triggers the waiver (Option B).', 'not covered', 'brochure', 'Diagnosis of 60 Critical Illnesses', 'See waiver_of_premium.'),
  'accidental_death': L('not covered', 'not covered', 'brochure', Q0, NC),
  'accidental_disability': L('No payout. Disability only triggers the waiver (Option B).', 'not covered', 'brochure', 'On the Life Assured being diagnosed with any of the Disability, subject to exclusions.', 'See waiver_of_premium.'),
  'term_cover': L('not covered', 'not covered', 'brochure', Q0, NC),
  'hospital_cash': L('not covered', 'not covered', 'brochure', Q0, NC),
  'other': L('not stated', 'not stated'),
 },
 'terms': {
  'rider_term': L('Minimum 5 years. Maximum: waiver on death, the outstanding premium payment term of the base policy; waiver on disability and critical illness, 15 years. Rider is not offered if its term exceeds the outstanding base policy term.', 'n/a', 'brochure', 'Waiver of Premium on Disability and Critical illness - 15 years'),
  'premium_paying_rules': L('Rider premium payment term is the same as the rider term. Can be opted at inception or on any premium due date of the base plan. Payment frequency follows the base policy. The rider ends when the base policy ends.', 'n/a', 'brochure', 'The premium payment frequency for the rider shall be same as the base policy.'),
  'entry_age': L('18 to 65 years; maturity age 23 to 85', 'n/a', 'brochure', 'Minimum: 18 years Maximum: 65 years'),
  'sum_assured_limits': L('Rider sum assured is the sum of all future premiums payable under the base policy, including optional benefits and other riders attached at inception of this rider, subject to the board-approved underwriting policy.', 'n/a', 'brochure', 'Sum of all future premiums due and payable under the Base Policy'),
  'premium_deduction': L('Separate rider premium collected in addition to the base policy premium. Not deducted from the fund.', 'n/a', 'brochure', 'The rider premium shall be collected in addition to the premium payable under the Base Policy.'),
 },
}
