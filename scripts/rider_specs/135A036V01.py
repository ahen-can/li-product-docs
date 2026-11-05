from rider_json import L
SLUG = 'ageas-federal'
Q0 = 'One out of the following two Rider Options can be selected by Policyholder:'
NC = 'Two options only: accidental death benefit, or comprehensive benefit (accidental death, accidental total and permanent disability and related accident benefits).'
SPEC = {
 'rider': {
  'name': L('Ageas Federal Life Insurance Linked Accident Care Rider', 'n/a', 'brochure', 'Linked Accident Care Rider'),
  'uin': L('135A036V01', 'n/a', 'brochure', '(UIN: 135A036V01)'),
  'linked_or_non_linked': L('linked-base, non-participating, individual pure risk premium life insurance rider; level rider premium', 'n/a', 'brochure', 'Linked, Non-Participating, Individual, Pure Risk Premium, Life Insurance Rider'),
  'attached_to_ulips': L('see results/ulip_rider_map.csv', 'n/a', None, None, 'Named by 4 of the 6 Ageas ULIPs. The brochure says it attaches to unit-linked non-participating individual products.'),
 },
 'benefits': {
  'waiver_of_premium': L('not covered', 'not covered', 'brochure', Q0, NC),
  'waiver_on_death_of_life_assured': L('not covered', 'not covered', 'brochure', Q0, NC),
  'waiver_on_death_or_illness_of_proposer': L('not covered', 'not covered', 'brochure', Q0, NC),
  'critical_illness': L('not covered', 'not covered', 'brochure', Q0, NC),
  'accidental_death': L('Accidental death benefit option: the rider sum assured as a lump sum. 2X benefit (200%) on death in an airplane or train accident. Comprehensive option adds transport of mortal remains (1%, up to Rs 50,000) and family travel for NRIs (2%, up to Rs 1,00,000).', 'covered as an option', 'brochure', 'benefit equal to Rider Sum Assured shall be'),
  'accidental_disability': L('Comprehensive option: accidental total and permanent disability pays 100% of rider sum assured, plus monthly income of 1% for 12 months (cap Rs 6,00,000), plus lifestyle support for rehabilitation (10%, cap Rs 10,00,000).', 'covered as an option', 'brochure', 'Total & Permanent Disability Benefit'),
  'term_cover': L('not covered', 'not covered', 'brochure', Q0, NC),
  'hospital_cash': L('not covered', 'not covered', 'brochure', Q0, NC),
  'other': L('Events must happen within 180 days of the accident.', 'covered', 'brochure', 'within 180'),
 },
 'terms': {
  'rider_term': L('Minimum: single pay 1 month, limited pay 60 months, regular pay 12 months. Maximum: 480 months for accidental death, 360 months for comprehensive. Not beyond the base policy term.', 'n/a', 'brochure', 'Accidental Death Benefit – 480 Months'),
  'premium_paying_rules': L('Single, limited (36 to 240 months) or regular pay. Modes: single, yearly, half-yearly, monthly. Can be added at inception or any policy anniversary during the base premium payment term.', 'n/a', 'brochure', 'Single, Yearly, Half Yearly, Monthly'),
  'entry_age': L('18 to 65 years; maturity age 18 to 75', 'n/a', 'brochure', 'Maximum 65 years'),
  'sum_assured_limits': L('Minimum Rs 5,000. Maximum 150% of the base sum assured for the accidental death option, 100% for the comprehensive option.', 'n/a', 'brochure', 'Accidental Death Benefit: 150% of Base Sum Assured'),
  'premium_deduction': L('Level rider premium payable in addition to the base premium. Not deducted from the fund.', 'n/a', 'brochure', 'The premium for the rider is level premium and will'),
 },
}
