from rider_json import L
SLUG = 'tata-aia'
Q = 'ensures your insurance benefits continue, if you are unable to'
NC = 'The rider is a premium waiver on total and permanent disability only.'
SPEC = {
 'rider': {
  'name': L('Tata AIA Life Insurance Waiver of Premium (Linked) Rider', 'n/a', 'brochure', 'Waiver of Premium (Linked) Rider'),
  'uin': L('110A026V03', 'n/a', 'brochure', 'UIN: 110A026V03', 'The rider page publishes V03. The ULIP product pages and i Systematic name V02 (one of V02 or V03 or later by product page). V02 documents were not found on the site.'),
  'linked_or_non_linked': L('linked rider, individual health insurance rider; charge cancelled from units', 'n/a', 'brochure', 'Linked, Individual, Health Insurance Rider'),
  'attached_to_ulips': L('see results/ulip_rider_map.csv', 'n/a', None, None, 'Named on the product pages of Wealth Pro, Fortune Pro, Fortune Maxima, Wealth Maxima, Smart SIP, Smart Fortune Plus, Smart Sampoorna Raksha Pro and others.'),
 },
 'benefits': {
  'waiver_of_premium': L('Waives the sum of all future premiums of the basic plan if the life insured becomes totally and permanently disabled (unable to work for 12 months, loss of use of two limbs or both eyes or one of each, or unable to do 3 of 6 daily tasks).', 'covered as an option', 'brochure', 'pay the premiums in the event of Total and Permanent Disability', 'Unambiguous: "basic plan". Disability only. No waiver on death or critical illness in this rider (death is covered by Waiver of Premium Plus for a proposer who is not the life insured).'),
  'waiver_on_death_of_life_assured': L('not covered', 'not covered', 'brochure', Q, NC),
  'waiver_on_death_or_illness_of_proposer': L('not covered. The life insured must be the premium payer. See Waiver of Premium Plus 110A025 for a different proposer.', 'not covered', 'brochure', Q, NC),
  'critical_illness': L('not covered', 'not covered', 'brochure', Q, NC),
  'accidental_death': L('not covered', 'not covered', 'brochure', Q, NC),
  'accidental_disability': L('No payout. Total and permanent disability only triggers the waiver.', 'not covered', 'brochure', Q, NC),
  'term_cover': L('not covered', 'not covered', 'brochure', Q, NC),
  'hospital_cash': L('not covered', 'not covered', 'brochure', Q, NC),
  'other': L('not stated', 'not stated'),
 },
 'terms': {
  'rider_term': L('Minimum 5 years. Maximum: until the end of the base plan premium payment term or age 65, whichever is earlier.', 'n/a', 'brochure', 'basic plan or until the Insured'),
  'premium_paying_rules': L('Rider charge is deducted for the maximum rider coverage term.', 'n/a', 'brochure', 'Same as Maximum Rider'),
  'entry_age': L('Minimum: the base product minimum or 18 years, whichever is higher. Maximum: the base product maximum or 60 years, whichever is lower. Maximum maturity age: end of premium payment term or 65.', 'n/a', 'brochure', 'Maximum age at entry under Base product or 60 years whichever is lower'),
  'sum_assured_limits': L('Sum of all future premiums of the basic plan to be waived (no separate minimum or maximum).', 'n/a', 'brochure', 'Sum of all the future premiums'),
  'premium_deduction': L('Charge recovered monthly by cancellation of units from the unit fund of the base policy.', 'n/a', 'brochure', 'The charge for the rider will be recovered monthly by cancellation'),
 },
}
