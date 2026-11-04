import sys; sys.path.insert(0, 'scripts'); sys.path.insert(0, 'scripts/ulip_specs')
from ulip_json import F, NS, build
B = 'click here'
V = 'from the V04 sales literature; the deep set lists V11 and no V11 document is linked'
spec = {
 'product': {
  'uin': F('110L164V11 (deep set); the only document prints 110L164V04', 'n/a', B, None, 'UIN: 110L164V04', 'version mismatch: the product page (a separate "bo" microsite) links only the V04 sales literature'),
  'uin_in_brochure': F('110L164V04', 'n/a', B, None, 'UIN: 110L164V04'),
  'product_name': F('Tata AIA i Systematic Insurance Plan (iSIP)', 'n/a', B, None, 'Tata AIA i Systematic Insurance Plan (iSIP)'),
  'irdai_description_line': F('Unit Linked, Individual Life Insurance Savings plan', 'n/a', B, None, 'Unit Linked, Individual Life Insurance Savings plan'),
  'launch_or_version_date': NS(),
  'variants_or_plan_options': F(['iSIP Wealth', 'iSIP Young Genius (company funds future premiums after death)'], 'optional (at inception)', B, None, 'Option 2: iSIP Young Genius', V),
  'target_segment_stated': NS(), 'online_offline': NS(),
 },
 'eligibility': {
  'entry_age_min': F('30 days (iSIP Wealth); 18 years (Young Genius)', 'n/a', B, None, 'iSIP Wealth: 0 years (30 days) iSIP Young Genius: 18 years', V),
  'maturity_age_min': F('18 years (Wealth); 28 years (Young Genius)', 'n/a', B, None, 'iSIP Wealth: 18 years iSIP young genius: 28 years', V),
  'ppt_options': F('single; limited 5 to 20 years; regular (equal to term)', 'n/a', B, None, 'Limited Pay – 5 - 20years', V),
  'premium_min_annual': F('Rs 1,200 (Wealth); Rs 6,000 (Young Genius)', 'n/a', B, None, 'Rs 1,000 Rs 1,200 p.a.', V),
  'premium_min_single': F('Rs 1,000 (Wealth)', 'n/a', B, None, 'Rs 1,000 Rs 1,200 p.a.', V),
  'premium_modes': F('single, annual, semi-annual, quarterly, monthly', 'n/a', B, None, 'Single, Annual, Semi-Annual, Quarterly, Monthly', V),
  'sum_assured_rule': F('single: 1.25x SP (up to 49) or 1.10x; regular/limited: 7x or 5x AP; maximum up to 30x by age and term', 'built-in', B, None, 'For Regular / Limited Pay – 7 times Annualised Premium', V),
 },
 'charges': {
  'premium_allocation_charge': F('nil', 'built-in', B, None, 'zero premium allocation and policy administration charges', V),
  'policy_administration_charge': F('nil', 'built-in', B, None, 'zero premium allocation and policy administration charges', V),
 },
 'benefits': {
  'death_benefit_formula': F({'iSIP Wealth': 'highest of SA, fund value, 105% of premiums', 'Young Genius': 'higher of SA or 105% now; company funds future premiums'}, 'built-in', B, None,
                             'TATA AIA Life Insurance shall fund all future premiums as and when they are due after the date of death of the Life Insured.', V),
  'maturity_benefit': F('fund value including top-up fund', 'built-in', B, None, 'You get the Fund Value, including Top-Up Premium Fund Value, if any', V),
  'return_of_mortality_charges': F('stated as a key benefit; details not read', 'built-in', B, None, 'Enjoy extra allocation of units with the Return of mortality charges', V),
  'wealth_boosters_or_guaranteed_additions': F('Smart Lady extra allocation for women; wealth boosters', 'built-in', B, None, 'Smart Lady : Extra allocation in the first', V),
 },
 'protection_add_ons': {'waiver_of_premium_inbuilt': F('Young Genius: company funds future premiums after death', 'optional (at inception)', B, None, 'TATA AIA Life Insurance shall fund all future premiums as and when they are due after the date of death of the Life Insured.', V),
                        'riders_available': F('Vitality riders mentioned', 'rider', B, None, 'Wellness benefit with the Vitality Riders', V)},
}
build('110L164V11', spec, new_features=[],
  not_public=[{'item': 'policy document, CIS and charges for V11', 'doc': B, 'where_referenced': None, 'quote': None, 'note': 'the product page is a microsite that links only the V04 sales literature; the policy document and CIS were not found'}],
  extra_notes=['All values come from the V04 sales literature. Fields left "not stated" were not read from it. A V11 policy document should be requested or looked for on the main Tata AIA site.'])
