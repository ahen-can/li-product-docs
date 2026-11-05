from rider_json import L
SLUG = 'hdfc-life'
LINKED_ULIPS = ['101L180V01 Sampoorn Nivesh Plus', '101L187V04 Smart Protect Plus', '101L191V02 Click 2 Invest Plus']
NC = 'The rider covers critical illness (option A) or cancer (option B) only.'
Q0 = 'Flexibility to choose between comprehensive critical illness cover or cancer cover'
SPEC = {
 'rider': {
  'name': L('HDFC Life Health Plus Rider - Linked', 'n/a', 'brochure', 'HDFC Life Health Plus Rider - Linked'),
  'uin': L('101A034V01', 'n/a', 'brochure', 'UIN: 101A034V01', 'V02 is the newest version: the site publishes a V02 CIS (16 Sep 2026, stored as docs/hdfc-life/riders/101A034V02/cis.pdf) with the same benefits. The brochure and rider document on the site and the product pages still print V01, and those are what is stored here.'),
  'linked_or_non_linked': L('linked-base rider, non-participating, savings / pure risk premium, individual health rider; separate rider premium', 'n/a', 'brochure', 'A Linked, Non-Participating, Savings/ Pure risk premium, Individual Health rider'),
  'attached_to_ulips': L(LINKED_ULIPS, 'n/a', None, None, 'Linked from the product pages of these three ULIPs. See results/ulip_rider_map.csv.'),
 },
 'benefits': {
  'waiver_of_premium': L('The rider\'s own future premiums are waived for 3 years after a valid claim for early-stage cancer or carcinoma in situ (cancer option). Base policy premiums are not waived.', 'not covered', 'brochure', 'Future premiums shall be waived for a period of 3 years under this rider on a valid claim of Early Stage Cancer or Carcinoma-in-situ (CIS) diagnosis', 'Waives only this rider\'s premium, so it is not a waiver of the ULIP premium.'),
  'waiver_on_death_of_life_assured': L('not covered', 'not covered', 'brochure', Q0, NC),
  'waiver_on_death_or_illness_of_proposer': L('not covered', 'not covered', 'brochure', Q0, NC),
  'critical_illness': L('Option A: lump sum of the rider sum assured on diagnosis of any of 60 critical illnesses; the cover then ends. Option B, cancer: 100% on major cancer less earlier claims; 25% (up to Rs 12,50,000) on early-stage cancer or carcinoma in situ, at most two minor claims. Elite cover option raises the sum assured 5% a year. Return of premium option available. Only one of A and B can be chosen.', 'covered as an option', 'brochure', 'The Rider Sum Assured shall be paid as a lumpsum on diagnosis of any of the covered critical illnesses', 'Condition counts: 60 critical illnesses (stated in the brochure).'),
  'accidental_death': L('not covered', 'not covered', 'brochure', Q0, NC),
  'accidental_disability': L('not covered', 'not covered', 'brochure', Q0, NC),
  'term_cover': L('not covered', 'not covered', 'brochure', Q0, NC),
  'hospital_cash': L('not covered', 'not covered', 'brochure', Q0, NC),
  'other': L('Option to get back all premiums paid (return of premium). Elite cover increases the rider sum assured 5% a year.', 'covered as an option', 'brochure', 'Option to get back all premiums paid with Return of Premium option'),
 },
 'terms': {
  'rider_term': L('Minimum 5 years. Maximum 15 years for option A (critical illness) and 5 years for option B (cancer).', 'n/a', 'brochure', 'Option A (CI) - 15 years'),
  'premium_paying_rules': L('Single, limited (minimum 5 years, maximum policy term less 1 year) or regular pay. Cannot exceed the outstanding premium payment term of the base policy. Opted at inception or later during the premium payment term.', 'n/a', 'brochure', 'Limited Pay with Minimum Premium Payment Term of 5 years'),
  'entry_age': L('18 to 65 years; maturity age 23 to 85', 'n/a', 'brochure', 'Entry Age (last birthday) 18 years 65 years'),
  'sum_assured_limits': L('Minimum Rs 5,000. No maximum, subject to underwriting; may not exceed the base policy sum assured.', 'n/a', 'brochure', 'Minimum Rider Sum Assured Rs. 5,000'),
  'premium_deduction': L('Separate rider premium collected in addition to the base policy premium. Not deducted from the fund.', 'n/a', 'brochure', 'The rider premium shall be collected in addition to the premium payable under the base policy.'),
 },
}
