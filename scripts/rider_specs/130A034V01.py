from rider_json import L
SLUG = 'bharti-life'
NA = 'The rider pays a death benefit only. It has no waiver, critical illness, accident, disability or hospital cash benefit.'
Q = 'In the event of death of Life Insured, the Sum Assured under the Rider will be paid to the Policyholder/nominee in addition to the Sum Assured under the base policy'
SPEC = {
 'rider': {
  'name': L('Bharti AXA Life Cover Plus Linked Term Rider', 'n/a', 'brochure', 'Bharti AXA Life Cover Plus Linked Term Rider'),
  'uin': L('130A034V01', 'n/a', 'brochure', 'UIN: 130A034V01', 'Brochure carries advert no II-June-2025-5681'),
  'linked_or_non_linked': L('non-linked, non-participating individual life insurance rider; separate rider premium', 'n/a', 'brochure', 'A Non-Linked, Non- Participating Individual Life Insurance Rider', 'Name says "Linked" because it attaches to linked base policies.'),
  'attached_to_ulips': L(['130L100V03 Wealth Pro', '130L123V01 Growth Shield Plus', '130L125V01 Dream Shield Plus', '130L128V01 Grow Wealth Ultra'], 'n/a', 'docs/bharti-life/130L125V01/brochure.pdf', 'Cover Plus Linked 130A034V01', 'Named in these four ULIP brochures (see results/ulip_rider_map.csv).'),
 },
 'benefits': {
  'waiver_of_premium': L('not covered', 'not covered', 'brochure', 'Financial protection against Death:', NA),
  'waiver_on_death_or_illness_of_proposer': L('not covered', 'not covered', 'brochure', 'Financial protection against Death:', NA),
  'critical_illness': L('not covered', 'not covered', 'brochure', 'Financial protection against Death:', NA),
  'accidental_death': L('Death from any cause is covered by the term cover. There is no separate accidental death option.', 'covered', 'brochure', Q),
  'accidental_disability': L('not covered', 'not covered', 'brochure', 'Financial protection against Death:', NA),
  'term_cover': L('Rider sum assured is paid on death of the life assured, in addition to the base policy sum assured. The rider then ends. There is no maturity value.', 'covered', 'brochure', Q),
  'hospital_cash': L('not covered', 'not covered', 'brochure', 'Financial protection against Death:', NA),
  'other': L('Surrender value is an unexpired risk premium at 70% (single pay, immediately; limited pay, after two full years of premium).', 'covered', 'brochure', 'The Unexpired Risk Premium Factor (URPF) of 70%'),
 },
 'terms': {
  'rider_term': L('10, 15, 20, 25, 30, 35 or 40 years', 'n/a', 'brochure', '10, 15, 20, 25, 30, 35, 40'),
  'premium_paying_rules': L('Single pay (1 year), limited pay (5, 6, 7, 10, 12 or 15 years) or regular pay (10 to 40 years, equal to the term). Modes: single, annual, semi-annual, quarterly and monthly (quarterly and monthly through auto pay only).', 'n/a', 'brochure', 'Single, Annual, semi- annual, quarterly* & monthly*'),
  'entry_age': L('18 to 60 years; maximum age at maturity 100', 'n/a', 'brochure', 'Maximum age at entry 60 years'),
  'sum_assured_limits': L('Minimum Rs 25,000. No maximum, subject to the company\'s board-approved underwriting policy.', 'n/a', 'brochure', 'Minimum Sum Assured (Rs.) Rs. 25,000'),
  'premium_deduction': L('Separate rider premium. The ULIP brochure says the rider is availed by "paying additional premium". The rider documents do not mention deduction from the fund.', 'n/a', 'docs/bharti-life/130L125V01/brochure.pdf', 'the following rider can be availed by paying additional premium along with Bharti AXA Life'),
 },
}
