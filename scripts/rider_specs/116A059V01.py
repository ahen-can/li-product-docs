from rider_json import L
SLUG = 'bajaj-life'
NC = 'The rider gives OPD benefits, an ATPD lump sum and a waiver of its own premium on ATPD only.'
Q0 = 'The following benefits are available under each rider option:'
SPEC = {
 'rider': {
  'name': L('Bajaj Life Care Plus Rider (linked)', 'n/a', 'brochure', 'Care Plus Rider'),
  'uin': L('116A059V01', 'n/a', 'policy', '116A059V01'),
  'linked_or_non_linked': L('linked-base, non-participating, individual pure risk health rider; separate rider premium', 'n/a', 'brochure', 'A Non-Participating, Linked, Individual, Pure Risk Health Rider'),
  'attached_to_ulips': L('see results/ulip_rider_map.csv', 'n/a', None, None, ''),
 },
 'benefits': {
  'waiver_of_premium': L('Only the rider\'s own future premiums are waived, for the rest of the rider premium paying term, after an accidental total permanent disability. The base policy premium is not waived.', 'not covered', 'brochure', 'the rider premiums will be waived off for the remaining rider premium paying', 'The waiver covers this rider only, so it is not a waiver of the ULIP premium.'),
  'waiver_on_death_of_life_assured': L('not covered', 'not covered', 'brochure', Q0, NC),
  'waiver_on_death_or_illness_of_proposer': L('not covered', 'not covered', 'brochure', Q0, NC),
  'critical_illness': L('not covered', 'not covered', 'brochure', Q0, NC),
  'accidental_death': L('not covered', 'not covered', 'brochure', Q0, NC),
  'accidental_disability': L('Accidental total permanent disability: an additional lump sum, in each of the five rider options. Sum assured is 1.25 times the rider premium for single pay and 10 times for limited or regular pay.', 'covered', 'brochure', 'an additional lump sum is paid to provide financial security'),
  'term_cover': L('not covered', 'not covered', 'brochure', Q0, NC),
  'hospital_cash': L('Out-patient benefits only (doctor consultation, lab tests, pharmacy, gym, nutritionist, preventive check-up, dental); no hospital cash.', 'not covered', 'brochure', 'Out-Patient Department (OPD) benefits', 'Not a daily hospital cash benefit.'),
  'other': L('OPD benefits grouped as health, fitness and wellness, in five rider options: Prime, Pro, Ultra, Prestige, Optima. Pharmacy and dental only under Prestige and Optima.', 'covered', 'brochure', 'There are 5 Rider options available:'),
 },
 'terms': {
  'rider_term': L('Single premium: 1 year. Limited premium: PPT + 1 year. Regular premium: 1 year for non-annual modes, 2 years for annual. Maximum 20 years, within the base policy term.', 'n/a', 'brochure', 'Maximum Rider Term'),
  'premium_paying_rules': L('Premium paying term 1 year minimum, at most equal to the rider term and consistent with the base policy. Modes follow the base policy. Rider premium is collected along with the base premium and guaranteed.', 'n/a', 'brochure', 'Minimum Premium Paying Term:'),
  'entry_age': L('18 to 65 years or the base policy maximum, whichever is lower; maturity age 19 to 75', 'n/a', 'brochure', 'Maximum Entry Age'),
  'sum_assured_limits': L('ATPD sum assured: 1.25 times rider premium (single pay), 10 times (limited or regular pay).', 'n/a', 'brochure', 'Limited/Regular Premium 10 times rider premium'),
  'premium_deduction': L('Separate rider premium collected with the base policy premium. Not deducted from the fund.', 'n/a', 'brochure', 'the rider premium as per the rider option chosen will be collected individually along with base policy premium'),
 },
}
