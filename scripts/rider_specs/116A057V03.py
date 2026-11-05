from rider_json import L
SLUG = 'bajaj-life'
Q0 = 'Choice of four cover options:'
NC = 'The rider covers accidental death and accidental total permanent disability, each with or without return of premium.'
SPEC = {
 'rider': {
  'name': L('Bajaj Life Linked Accident Protection Rider II', 'n/a', 'brochure', 'Linked Accident Protection Rider II'),
  'uin': L('116A057V03', 'n/a', 'policy', '116A057V03'),
  'linked_or_non_linked': L('linked-base, non-participating, individual pure risk rider offering health cover and savings; separate rider premium', 'n/a', 'brochure', 'A Non-Participating, Linked, Individual Pure Risk offering Health Cover and Savings Rider'),
  'attached_to_ulips': L('see results/ulip_rider_map.csv', 'n/a', None, None, ''),
 },
 'benefits': {
  'waiver_of_premium': L('not covered', 'not covered', 'brochure', Q0, NC),
  'waiver_on_death_of_life_assured': L('not covered', 'not covered', 'brochure', Q0, NC),
  'waiver_on_death_or_illness_of_proposer': L('not covered', 'not covered', 'brochure', Q0, NC),
  'critical_illness': L('not covered', 'not covered', 'brochure', Q0, NC),
  'accidental_death': L('Higher of the ADB sum assured or 105% of total premiums paid, as a lump sum, on death by accident (also if death follows within 180 days after the term ends). ADB cover up to 3 times the base policy sum assured. With ROP option, the premiums paid come back on survival to maturity.', 'covered as an option', 'brochure', 'higher of ADB Sum Assured or Guaranteed Benefit (i.e. 105% of Total Premiums Paid*) will be paid as a lumpsum'),
  'accidental_disability': L('Accidental total permanent disability benefit, with or without return of premium; ATPD sum assured at most the base policy sum assured.', 'covered as an option', 'brochure', 'Accidental Total Permanent Disability Benefit'),
  'term_cover': L('not covered', 'not covered', 'brochure', Q0, NC),
  'hospital_cash': L('not covered', 'not covered', 'brochure', Q0, NC),
  'other': L('Return of premium options on ADB and ATPD: total premiums paid on survival till maturity.', 'covered as an option', 'brochure', 'Return of Premium Option: Get back your Total Premiums Paid'),
 },
 'terms': {
  'rider_term': L('ADB and ATPD: 1 to 67 years. ADB with ROP and ATPD with ROP: 10 to 50 years. Aligned to the base policy term.', 'n/a', 'brochure', 'Minimum 1 year 10 years'),
  'premium_paying_rules': L('Single (1 year), limited (PPT 2 to 66, PT at least PPT + 1) or regular pay (PPT = PT, 2 to 67). For ROP options PPT 5 to 50 and PT at least PPT + 5. Frequency as base policy.', 'n/a', 'brochure', 'Limited Pay i.e. PPT < PT'),
  'entry_age': L('Up to 65 years (attained age); minimum maturity age 19 (28 with ROP), maximum 85', 'n/a', 'brochure', 'Maximum Entry Age 65 years (attained age)'),
  'sum_assured_limits': L('Minimum Rs 1,00,000 per cover option. Maximum subject to underwriting: ADB up to 3 times the base sum assured, ATPD up to the base sum assured.', 'n/a', 'brochure', 'for each cover option'),
  'premium_deduction': L('Collected over and above the base policy premium, as a separate rider premium. Not deducted from the fund.', 'n/a', 'brochure', 'Rider Premium would be collected over and above the base policy premium'),
 },
}
