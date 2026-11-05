from rider_json import L
SLUG = 'sbi-life'
NOT = 'Two benefit options only: accidental death and accidental partial permanent disability.'
Q2 = 'There are two benefit options under this rider.'
SPEC = {
 'rider': {
  'name': L('SBI Life - Accident Benefit Rider - Linked', 'n/a', 'brochure', 'Accident Benefit Rider – Linked'),
  'uin': L('111A042V01', 'n/a', 'brochure', 'UIN: 111A042V01'),
  'linked_or_non_linked': L('linked-base rider, non-participating pure risk rider; separate rider premium', 'n/a', 'brochure', 'An Individual, Linked, Non-Participating, Health Insurance Pure Risk Rider', 'The document calls it a health insurance rider.'),
  'attached_to_ulips': L(['111L142V01 Smart Fortune Builder', '111L143V01 Smart Privilege Plus', '111L147V01 eWealth Plus', '111L153V01 Smart Invest Builder'], 'n/a', None, None, 'Linked from each of these four ULIP product pages. Smart Elite Plus names only the waiver rider.'),
 },
 'benefits': {
  'waiver_of_premium': L('not covered', 'not covered', 'brochure', Q2, NOT),
  'waiver_on_death_or_illness_of_proposer': L('not covered', 'not covered', 'brochure', Q2, NOT),
  'critical_illness': L('not covered', 'not covered', 'brochure', Q2, NOT),
  'accidental_death': L('Option A. Rider sum assured paid on accidental death of the life assured within 180 days of the accident. Benefit is payable even if death falls after the rider term, if the accident happened while the rider was in force.', 'covered as an option', 'brochure', 'we will pay the Rider Sum Assured for AD Benefit'),
  'accidental_disability': L('Option B, partial permanent disability only. Percentage of rider sum assured by injury, for example 75% for loss of hearing in both ears, 50% for loss of one eye, 30% for hearing in one ear. Within 180 days of the accident. No total permanent disability option.', 'covered as an option', 'brochure', 'Hearing in both ears 75%'),
  'term_cover': L('not covered', 'not covered', 'brochure', Q2, NOT),
  'hospital_cash': L('not covered', 'not covered', 'brochure', Q2, NOT),
  'other': L('If a benefit option is already inbuilt in the base policy, the rider does not offer it. Can be added at a later policy anniversary for regular and limited pay policies.', 'covered', 'brochure', 'the same benefit option shall not be offered under the rider'),
 },
 'terms': {
  'rider_term': L('Minimum 1 year, maximum 75 less age at entry, and not beyond the outstanding base policy term. Rider premium payment term equals the base policy premium payment term (outstanding term if added later).', 'n/a', 'brochure', 'Maximum: 75 less Age at Entry'),
  'premium_paying_rules': L('Single, limited or regular, aligned with the base policy. Modes follow the base policy. Half-yearly 51%, quarterly 25.5%, monthly 8.5% of annual premium. Rider premium is level and guaranteed.', 'n/a', 'brochure', 'Monthly: 8.50% of annual premium'),
  'entry_age': L('18 to 65 years; maturity age 19 to 75', 'n/a', 'brochure', 'Minimum: 18 Maximum: 65'),
  'sum_assured_limits': L('Minimum Rs 50,000 or the base policy minimum if lower. Maximum Rs 2 crore for accidental death (at most 3 times the base sum assured) and Rs 1.5 crore for APPD (at most the base sum assured).', 'n/a', 'brochure', 'Accidental Death Benefit (AD Benefit) – `2,00,00,000'),
  'premium_deduction': L('Separate rider premium, payable in addition to the base premium with the same due date. Cannot be paid on its own. Not deducted from the fund.', 'n/a', 'brochure', 'Rider premium shall be payable in addition to the premium payable under the base policy.'),
 },
}
