from rider_json import L
SLUG = 'sbi-life'
SPEC = {
 'rider': {
  'name': L('SBI Life - Waiver of Premium Rider - Linked', 'n/a', 'brochure', 'Waiver of Premium Rider-Linked'),
  'uin': L('111A049V01', 'n/a', 'brochure', 'UIN: 111A049V01'),
  'linked_or_non_linked': L('linked-base rider, non-participating pure risk rider; separate rider premium', 'n/a', 'brochure', 'An Individual, Linked, Non-Participating, Pure Risk Health Insurance rider', 'The document calls it a health insurance rider.'),
  'attached_to_ulips': L(['111L142V01 Smart Fortune Builder', '111L143V01 Smart Privilege Plus', '111L146V01 Smart Elite Plus', '111L147V01 eWealth Plus', '111L153V01 Smart Invest Builder'], 'n/a', None, None, 'Linked from each of these five ULIP product pages and named in their brochures. Smart Scholar Plus (waiver built in) and Retire Smart Plus link no rider.'),
 },
 'benefits': {
  'waiver_of_premium': L('The rider is the waiver. If the proposer and life assured are the same: on accidental total permanent disability or diagnosis of a covered critical illness. If they differ: on death of the proposer, or the proposer\'s ATPD or critical illness. From the event, all future premiums under the base policy are paid by the company, including extra premiums and any other rider premium, excluding the waiver rider\'s own premium.', 'covered', 'brochure', 'All the future premium under the base policy will be paid by Us on Your behalf on the Premium Payment Due Dates.', 'Unambiguous: the brochure says "base policy" and defines the waived premiums as those under the SBI Life base policy. 90 day waiting period and 30 day survival period for critical illness. Not available with a single premium base policy.'),
  'waiver_on_death_of_life_assured': L('not covered when proposer and life assured are the same (only ATPD and critical illness trigger)', 'not covered', 'brochure', 'If Proposer and Life Assured are same under the Base Policy:'),
  'waiver_on_death_or_illness_of_proposer': L('Death, ATPD or critical illness of the proposer, when the proposer is not the life assured', 'covered', 'brochure', 'Death of the Proposer'),
  'critical_illness': L('No lump sum. Diagnosis of any of 20 covered conditions only triggers the premium waiver.', 'not covered', 'brochure', 'Diagnosis of any one of the covered Critical Illness (CI) of the Proposer', 'Counted 20: cancer, myocardial infarction, open chest CABG, heart valve surgery, coma, kidney failure, stroke, major organ or bone marrow transplant, permanent paralysis, motor neuron disease, multiple sclerosis, benign brain tumour, blindness, end stage lung failure, end stage liver failure, loss of speech, loss of limbs, major head trauma, primary pulmonary hypertension, third degree burns. See waiver_of_premium.'),
  'accidental_death': L('not covered', 'not covered', 'brochure', 'On occurrence of specified contingencies as mentioned above in relation to the proposer under the base policy during the rider term, future premiums'),
  'accidental_disability': L('No payout. Accidental total permanent disability only triggers the waiver.', 'not covered', 'brochure', 'Accidental Total Permanent Disability (ATPD)', 'See waiver_of_premium.'),
  'term_cover': L('not covered', 'not covered', 'brochure', 'No Maturity benefit is payable under this rider.'),
  'hospital_cash': L('not covered', 'not covered', 'brochure', 'On occurrence of specified contingencies as mentioned above in relation to the proposer under the base policy during the rider term, future premiums'),
  'other': L('No maturity benefit, no surrender value, no paid-up value, no loan.', 'not covered', 'brochure', 'On Surrender during rider term, no benefit is payable.'),
 },
 'terms': {
  'rider_term': L('Opted at inception: same as the base policy premium payment term, minimum 5 years. Opted at a later anniversary: the outstanding premium payment term, minimum 5 years.', 'n/a', 'brochure', 'subject to a minimum of 5 years'),
  'premium_paying_rules': L('Rider premium payment term is the same as the rider term. Modes follow the base policy (annual, half-yearly, quarterly, monthly). Not available with a single premium base policy. Premium under all health riders together may not exceed 100% of the base premium.', 'n/a', 'brochure', 'This rider cannot be opted with Single Premium base policy.'),
  'entry_age': L('18 to 65 years; maturity age 23 to 70', 'n/a', 'brochure', 'Minimum - 18 Maximum - 65'),
  'sum_assured_limits': L('Minimum Rs 10,000, maximum Rs 1,00,00,000. Rider sum assured is the present value of future premiums and may not exceed the base policy sum assured.', 'n/a', 'brochure', 'Minimum Rider Sum Assured: INR 10,000'),
  'premium_deduction': L('Separate rider premium, payable in addition to the base premium and on the same due date and mode. Not deducted from the fund.', 'n/a', 'brochure', 'Rider premium shall be payable in addition to the premium payable under the base policy.'),
 },
}
