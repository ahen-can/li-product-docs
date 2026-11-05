from rider_json import L
SLUG = 'bajaj-life'
Q0 = 'Protection against up to 60 major Critical Illnesses (CIs)'
NC = 'The rider pays a lump sum on critical illness only.'
SPEC = {
 'rider': {
  'name': L('Bajaj Life Linked New Critical Illness Benefit Rider', 'n/a', 'brochure', 'Linked New Critical Illness Benefit Rider'),
  'uin': L('116A060V01', 'n/a', 'policy', '116A060V01'),
  'linked_or_non_linked': L('linked-base, non-participating, individual pure risk health rider; separate rider premium', 'n/a', 'brochure', 'A Linked, Non-Participating, Individual, Pure Risk Health Rider'),
  'attached_to_ulips': L('see results/ulip_rider_map.csv', 'n/a', None, None, ''),
 },
 'benefits': {
  'waiver_of_premium': L('not covered', 'not covered', 'brochure', Q0, NC),
  'waiver_on_death_of_life_assured': L('not covered', 'not covered', 'brochure', Q0, NC),
  'waiver_on_death_or_illness_of_proposer': L('not covered', 'not covered', 'brochure', Q0, NC),
  'critical_illness': L('Lump sum of the rider sum assured on first diagnosis of a listed critical illness, if the life assured survives 14 days. Three options: Critical (10 conditions), Enhanced (25 conditions), Comprehensive (60 conditions).', 'covered as an option', 'brochure', 'Critical (10 major CIs), Enhanced (25 major CIs), and Comprehensive (60 major CIs)'),
  'accidental_death': L('not covered', 'not covered', 'brochure', Q0, NC),
  'accidental_disability': L('not covered', 'not covered', 'brochure', Q0, NC),
  'term_cover': L('not covered', 'not covered', 'brochure', Q0, NC),
  'hospital_cash': L('not covered', 'not covered', 'brochure', Q0, NC),
  'other': L('Rider termination value under single premium payment; none under regular pay.', 'covered', 'brochure', 'Rider Termination Value'),
 },
 'terms': {
  'rider_term': L('Minimum 1 year, maximum 30 years, within the base policy term.', 'n/a', 'brochure', 'Maximum Rider Term'),
  'premium_paying_rules': L('Premium paying term 1 to 10, 12, 15, 20 years, pay till age 60, or equal to the rider term, as per the base policy.', 'n/a', 'brochure', 'Pay till Age 60 and Equal to Rider Term'),
  'entry_age': L('18 to 65 years; maturity age 19 to 80', 'n/a', 'brochure', 'Maximum Entry Age 65 years'),
  'sum_assured_limits': L('Minimum Rs 50,000. Maximum: not above the base policy sum assured, subject to underwriting.', 'n/a', 'brochure', 'Minimum Sum Assured (Rs.) Rs. 50,000'),
  'premium_deduction': L('not stated', 'not stated', None, None, 'The text read does not say how the premium is collected. The Care Plus and Accident rider brochures say it is collected with the base premium. Needs a second read.'),
 },
}
