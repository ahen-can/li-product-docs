from rider_json import L
SLUG = 'tata-aia'
OPT = 'Five benefit options: term benefit with accelerated terminal illness, accidental death, accidental total and permanent disability, Criticare Plus and Criticare.'
SPEC = {
 'rider': {
  'name': L('Tata AIA Life Insurance Linked Comprehensive Protection Rider', 'n/a', 'brochure', 'Linked Comprehensive Protection Rider'),
  'uin': L('110A032V05', 'n/a', 'brochure', 'UIN: 110A032V05', 'Rider page publishes V05. ULIP product pages name V02 to V04. Earlier versions were not found on the site.'),
  'linked_or_non_linked': L('linked rider, individual health rider; charge cancelled from units of the base policy', 'n/a', 'policy', 'Individual Health Rider', 'Policy text says unit-deduction rider cannot be combined with Vitality Protect Plus.'),
  'attached_to_ulips': L('see results/ulip_rider_map.csv', 'n/a', None, None, ''),
 },
 'benefits': {
  'waiver_of_premium': L('A benefit payout option (regular pay, without return of balance premium) on the insured events. On the event, all future premiums are waived for the rest of the premium payment term and the waiver sum assured equals the outstanding premiums under the base plan and riders at inception of the benefit option.', 'covered as an option', 'brochure', 'the sum assured shall be equal to the outstanding premium under the base plan', 'The sum assured clause names the base plan and riders, so the waiver covers the ULIP premium. The sentence stating what is waived loses words in the text extraction ("all future premiums that would have been payable under ... shall be waived"). Re-read the page image to quote it in full.'),
  'waiver_on_death_of_life_assured': L('The insured event for the waiver payout can be death or terminal illness (term benefit option), accidental death, ATPD or critical illness, as chosen.', 'covered as an option', 'brochure', 'Waiver of future premiums'),
  'waiver_on_death_or_illness_of_proposer': L('The rider allows cover on a spouse or loved one as a separate life insured. Whether the waiver follows the policyholder is not stated in the text read.', 'not stated'),
  'critical_illness': L('Criticare Plus: Insured Amount paid on first diagnosis of any of 40 critical illnesses (survive 30 days). Criticare: also 40 illnesses. Benefit once per life. Renewable for 5 years at maturity.', 'covered as an option', 'brochure', 'The Insured Amount under the Benefit Option is payable if the Life Insured survives for a period of 30 days following the first', 'Brochure states 40 critical illnesses including cancer and cardiac conditions.'),
  'accidental_death': L('Insured Amount on death by accident within 180 days. Enhanced accidental benefit: an extra amount equal to the sum assured (up to Rs 5 crore) for accidents in public transport, lifts, public building fires or commercial flights.', 'covered as an option', 'brochure', 'Enhanced Accidental Benefit'),
  'accidental_disability': L('Accidental total and permanent disability within 180 days: the insured amount, with the same enhanced accidental benefit.', 'covered as an option', 'brochure', 'Accidental Total and Permanent Disability Benefit'),
  'term_cover': L('Term benefit with accelerated terminal illness: Insured Amount payable on death or diagnosis of terminal illness. Minimum Rs 5,00,000.', 'covered as an option', 'brochure', 'The Insured Amount under this option is payable on earlier of'),
  'hospital_cash': L('not covered', 'not covered', 'brochure', 'risk covers) including death, accidental death', OPT),
  'other': L('Return of balance premium on maturity option; benefit as lump sum, income, income for a surviving partner or waiver; renewability option for 5 years for Criticare and Criticare Plus.', 'covered as an option', 'brochure', 'Option to receive return of balance premiums on maturity'),
 },
 'terms': {
  'rider_term': L('Single pay: term benefit 6 months to 67 years; accidental death and ATPD 1 month to 82 years; Criticare and Criticare Plus 12 months to 5 years. See the brochure table for limited and regular pay.', 'n/a', 'brochure', 'Single Pay:'),
  'premium_paying_rules': L('Single, limited and regular pay as available per benefit option; waiver payout only as regular pay without return of balance premium. Options can be added at inception or any policy anniversary.', 'n/a', 'brochure', 'Waiver of future premium as benefit payout option is available'),
  'entry_age': L('18 to 65 years for all options; maximum maturity age 85 (term, accidental death, ATPD) or 75 (Criticare options)', 'n/a', 'brochure', 'T&TI 18 65 85 500,000'),
  'sum_assured_limits': L('Minimums: term benefit Rs 5,00,000; accidental death and ATPD Rs 1,00,000; Criticare options Rs 2,00,000. Maximum subject to underwriting and not above the base plan death benefit.', 'n/a', 'brochure', 'Rider Sum Assured cannot exceed the Death Benefit at'),
  'premium_deduction': L('not stated', 'not stated', None, None, 'The rider is labelled linked; the Waiver of Premium and ADDL riders state unit cancellation. The text read for this rider does not state it. Needs a second read.'),
 },
}
