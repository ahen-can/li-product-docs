from rider_json import L
SLUG = 'axis-max-life'
Q0 = 'You can choose one or more rider benefit variants (risk covers) including *Death &'
NC = 'Four variants: term booster with accelerated terminal illness, accidental death, accidental total and permanent disability, and payor benefit.'
SPEC = {
 'rider': {
  'name': L('Axis Max Life Smart Ultra Protect Rider', 'n/a', 'brochure', 'Axis Max Life Smart Ultra Protect Rider'),
  'uin': L('104A049V03', 'n/a', 'brochure', 'UIN: 104A049V03'),
  'linked_or_non_linked': L('unit-linked base, individual health insurance rider; level rider premium, not a charge from the fund', 'n/a', 'brochure', 'Unit-Linked Individual Health Insurance Rider'),
  'attached_to_ulips': L('see results/ulip_rider_map.csv', 'n/a', None, None, 'Named by all 9 Axis Max ULIPs.'),
 },
 'benefits': {
  'waiver_of_premium': L('Payor Benefit (variant 4): on the death or terminal illness of the policyholder, the company funds all future premiums under the base policy and waives all future premiums under attached riders. Applies only when the policyholder and the life insured are different people. Not triggered by disability or critical illness.', 'covered as an option', 'brochure', 'Fund all future outstanding premiums, as and when due, under the base policy and', 'Unambiguous: "under the base policy". Once accepted, the present value of future premiums (at 5.50% a year) is paid on termination of the base policy.'),
  'waiver_on_death_of_life_assured': L('not covered. Death of the life insured is covered by the term booster option.', 'not covered', 'brochure', Q0, NC),
  'waiver_on_death_or_illness_of_proposer': L('Death or diagnosis of terminal illness of the policyholder (payor). No disability or critical illness trigger.', 'covered as an option', 'brochure', 'In the case of death of policyholder, the company shall:'),
  'critical_illness': L('not covered. Terminal illness only, as part of the term booster and payor benefit.', 'not covered', 'brochure', Q0, NC),
  'accidental_death': L('Accidental Death Benefit: rider sum assured on death by accident of the life insured, up to 75 years maturity age. Return of premium option available.', 'covered as an option', 'brochure', 'Benefit payable on death due to accident of Life Insured'),
  'accidental_disability': L('Accidental Total and Permanent Disability: rider sum assured on accidental TPD of the life insured. Return of premium option available.', 'covered as an option', 'brochure', 'Benefit payable on Accidental Total & Permanent Disability of Life Insured'),
  'term_cover': L('Term Booster with Accelerated Terminal Illness: benefit on the earlier of death or diagnosis of terminal illness of the life insured, as a lump sum. Return of premium option available.', 'covered as an option', 'brochure', 'Benefit payable on earlier of death or diagnosis of terminal illness of Life'),
  'hospital_cash': L('not covered', 'not covered', 'brochure', Q0, NC),
  'other': L('Return of premium option on variants 1 to 3 (not for payor benefit); a non-ROP and ROP option of the same variant cannot be taken together.', 'covered as an option', 'brochure', 'Rider Benefit Variant 1, 2 and 3 have a Return of Premium Option as well'),
 },
 'terms': {
  'rider_term': L('Term booster 1 to 62 years; accidental death 1 to 57 years (with ROP minimum 10); see the brochure table for the others.', 'n/a', 'brochure', 'Term Booster with Accelerated'),
  'premium_paying_rules': L('Limited pay, regular pay or single pay as per the base plan.', 'n/a', 'brochure', 'Flexibility of premium payment'),
  'entry_age': L('18 to 65 years; maturity age from 19 up to 80 (term booster, payor benefit) or 75 (accidental death, ATPD)', 'n/a', 'brochure', 'Maximum Entry Age (age as on last'),
  'sum_assured_limits': L('As per the maximum sum assured under each rider benefit variant, subject to the board-approved underwriting policy.', 'n/a', 'brochure', 'As per maximum Sum Assured under rider benefit variant'),
  'premium_deduction': L('Level rider premium in addition to the base premium, not a rider charge deducted from unit funds.', 'n/a', 'brochure', 'the rider premiums shall be levied through level rider premium'),
 },
}
