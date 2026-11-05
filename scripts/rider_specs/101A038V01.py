from rider_json import L
SLUG = 'hdfc-life'
LINKED_ULIPS = ['101L180V01 Sampoorn Nivesh Plus', '101L187V04 Smart Protect Plus', '101L191V02 Click 2 Invest Plus']
NC = 'The rider pays a monthly income on accidental total permanent disability and nothing else.'
Q0 = 'In the event of Total Permanent Disability due to accident, you will be paid a regular monthly income equal to 1% of Sum Assured for a fixed period of 10 years.'
SPEC = {
 'rider': {
  'name': L('HDFC Life Income Benefit on Accidental Disability Rider - Linked', 'n/a', 'brochure', 'Income Benefit on Accidental Disability Rider-Linked'),
  'uin': L('101A038V01', 'n/a', 'policy', '101A038V01'),
  'linked_or_non_linked': L('linked-base rider, non-participating, pure risk premium, individual life rider; separate rider premium', 'n/a', 'brochure', 'A Linked, Non- Participating, Pure risk premium, Individual Life rider'),
  'attached_to_ulips': L(LINKED_ULIPS + ['101L133V03 Click 2 Wealth'], 'n/a', None, None, 'Linked from the product pages of these four ULIPs. See results/ulip_rider_map.csv.'),
 },
 'benefits': {
  'waiver_of_premium': L('not covered', 'not covered', 'brochure', Q0, NC),
  'waiver_on_death_of_life_assured': L('not covered', 'not covered', 'brochure', Q0, NC),
  'waiver_on_death_or_illness_of_proposer': L('not covered', 'not covered', 'brochure', Q0, NC),
  'critical_illness': L('not covered', 'not covered', 'brochure', Q0, NC),
  'accidental_death': L('not covered. If the life assured dies while income payments are outstanding, the nominee keeps receiving them.', 'not covered', 'brochure', 'In case the death of the life assured occurs while the benefit payments are outstanding then the nominee will continue to receive the outstanding monthly benefit payments.'),
  'accidental_disability': L('Monthly income of 1% of sum assured for 10 years on accidental total permanent disability (inability to work, or loss of two limbs, both eyes, or one limb and one eye). Benefit starts after 6 months of continuous disability, immediately for loss by severance of limbs. No waiting period. No partial disability benefit.', 'covered', 'brochure', Q0),
  'term_cover': L('not covered', 'not covered', 'brochure', Q0, NC),
  'hospital_cash': L('not covered', 'not covered', 'brochure', Q0, NC),
  'other': L('not stated', 'not stated'),
 },
 'terms': {
  'rider_term': L('Minimum 5 years; maximum consistent with the base policy. Cannot exceed the outstanding base policy term.', 'n/a', 'brochure', 'Minimum: 5 years'),
  'premium_paying_rules': L('Premium payment term at most the outstanding premium payment term of the base plan. Can be taken at inception or on a later policy anniversary. Frequency follows the base policy.', 'n/a', 'brochure', 'Less than or equal to the premium payment term of the base plan'),
  'entry_age': L('18 to 65 years; maturity age up to 75', 'n/a', 'brochure', 'Entry age (last birthday) 18 years to 65 years'),
  'sum_assured_limits': L('Minimum Rs 1,00,000. No maximum, subject to underwriting; may not exceed the base policy sum assured.', 'n/a', 'brochure', 'Minimum Sum Assured Rs 100,000'),
  'premium_deduction': L('Separate rider premium collected in addition to the base policy premium. Not deducted from the fund.', 'n/a', 'brochure', 'The rider premium shall be collected in addition to the premium payable under the base policy.'),
 },
}
