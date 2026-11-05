from rider_json import L
SLUG = 'tata-aia'
SPEC = {
 'rider': {
  'name': L('Tata AIA Vitality Protect Plus', 'n/a', 'brochure', 'Tata AIA Vitality Protect Plus'),
  'uin': L('110A048V04', 'n/a', 'brochure', 'UIN: 110A048V04', 'Rider page publishes V04; ULIP product pages name V03.'),
  'linked_or_non_linked': L('non-linked, non-participating individual health rider; not a unit-deduction rider', 'n/a', 'brochure', 'A Non-Linked, Non- Participating Individual Health rider', 'The policy text says a unit-deduction rider and this rider cannot be attached together, so the premium is separate.'),
  'attached_to_ulips': L('see results/ulip_rider_map.csv', 'n/a', None, None, ''),
 },
 'benefits': {
  'waiver_of_premium': L('Waiver of future premium is a payout option on the insured events (regular pay, without return of balance premium). The outstanding future premium under the base plan, riders and attached benefit options at inception is waived.', 'covered as an option', 'policy', 'The outstanding future Premium under the Base Plan, Rider/s and any attached Benefit', 'Unambiguous: "Base Plan".'),
  'waiver_on_death_of_life_assured': L('The waiver pays out on the insured event of the benefit option chosen: death or terminal illness (Term Booster), accidental death, ATPD or critical illness.', 'covered as an option', 'brochure', 'Income till survival of partner or Waiver of Premium'),
  'waiver_on_death_or_illness_of_proposer': L('not stated', 'not stated', None, None, 'The rider allows cover on the life of a partner under the same plan; payor events are not described in the text read.'),
  'critical_illness': L('CritiCare Plus: lump sum on first diagnosis of any of 40 critical illnesses including cancer and cardiac conditions. Accelerated CritiCare: the same 40 illnesses, paid as an acceleration of the Term Booster amount.', 'covered as an option', 'brochure', '40 Critical Illness including Cancer and'),
  'accidental_death': L('Insured amount on death by accident within 180 days; double the amount for accidents in public transport, lifts, public building fires and commercial flights.', 'covered as an option', 'brochure', 'Twice the amount of the above benefit will be payable'),
  'accidental_disability': L('Accidental total and permanent disability option within 180 days of the accident.', 'covered as an option', 'brochure', 'Accidental Total & Permanent Disability'),
  'term_cover': L('Term Booster: Insured Amount payable on earlier of death or diagnosis of terminal illness.', 'covered as an option', 'brochure', 'The Insured Amount under this option is payable on'),
  'hospital_cash': L('not covered', 'not covered', 'brochure', 'Details of benefits under each Benefit Option is as', 'Options are Term Booster, Accidental Death, ATPD, CritiCare Plus and Accelerated CritiCare.'),
  'other': L('Vitality wellness programme; return of balance premium option; payout as lump sum with income, income until a partner dies, or waiver.', 'covered', 'brochure', 'Option to receive return of balance premiums on'),
 },
 'terms': {
  'rider_term': L('Term Booster to 82 years; accidental death and ATPD to 67 years; CritiCare options 5 years. Minimum 13 to 14 months for regular and limited pay.', 'n/a', 'brochure', 'Term Booster 13 82'),
  'premium_paying_rules': L('Regular, limited or single pay, with or without return of balance premium (not for CritiCare options).', 'n/a', 'brochure', 'Without Return of Balance Premium'),
  'entry_age': L('18 to 65 years; maturity age 100 (Term Booster), 85 (accidental death, ATPD), 75 (CritiCare options)', 'n/a', 'brochure', 'Term Booster 18/65 100'),
  'sum_assured_limits': L('Minimum Rs 25,000 per option; maximum subject to underwriting and not above the base plan death benefit.', 'n/a', 'brochure', 'Term Booster 25,000'),
  'premium_deduction': L('Separate premium, not a unit-deduction rider.', 'n/a', 'policy', 'At no point both unit-deduction rider and this rider shall be allowed'),
 },
}
