# Coding rules for feature list v3 (proposed 5 Nov 2026, waiting for the user)

S3's v3 QA marked 17 Bharti cells UNSURE. Each needs a rule, because the definition allows two answers. Every rule below applies to all 84 ULIPs, not only Bharti. Once the user accepts a rule, S1 codes the cells through an overrides file and rebuilds.

## 1. Child or payor waiver (`child_payor_benefit`), 6 cells
**What S3 found.** The waiver option in Bharti's Linked Complete Shield Rider can be taken "by the policyholder, only if life insured and policyholder are different" (rider brochure p5). The rider policy clause 2 still names the trigger as an event to "the Life Insured". So it is unclear whether a parent buying for a child gets the premiums waived when the parent falls ill.

**Proposed rule.** Code payor waiver only when the document says the event that triggers the waiver happens to the policyholder or proposer (the payer), not the life insured. Who may opt in does not count. Under this rule the 6 Bharti cells become "?" with a note. Separately, the Bharti waiver never covers death, so it is not a full payor benefit even if the trigger question resolves in Bharti's favour.

**Decision for the user.** Accept the rule. Optionally ask a Bharti contact: "Under the Linked Complete Shield Rider, if the policyholder and life insured differ, whose disability or critical illness triggers the waiver?"

## 2. Milestone benefits: guaranteed additions or wealth boosters (`scheduled_guaranteed_additions`), 2 cells
**What S3 found.** Dream Shield Plus credits 1.5% to 2.5% of the fund value at years 10, 15, 20, 25, 30 and 35 (brochure p4). Grow Wealth Ultra credits 5% to 20% of the 60-month average fund every 5th year from year 10 (brochure p5). v3 codes both as wealth boosters only. They also fit "additions on a fixed schedule".

**Why it matters.** The decks say "Bharti has no guaranteed additions (20 of 84)". Today that row counts products whose documents use the word "guaranteed". Under ULIP rules every addition written into the contract is payable once its conditions are met, so the label is marketing, not a difference in design.

**Two options.**
- (a) Keep the label rule. The row means "the insurer calls it guaranteed". Both cells stay blank. The deck line stays true but says little.
- (b) Recommended. Split the row by what the addition is a percentage of. "Additions as a % of premium" fixes the rupee amount at the start. "Additions as a % of fund value" depends on the market. Drop the word "guaranteed". Dream Shield Plus and Grow Wealth Ultra go under "% of fund value", next to Wealth Pro's boosters. The line "Bharti has no guaranteed additions" then becomes "Bharti's additions are all a % of fund value; X of 84 products add a fixed % of premium".

**Decision for the user.** Choose (a) or (b). Option (b) means S1 re-reads the 20 current matches plus every wealth booster row (about 60 products) for the basis.

## 3. Loyalty design variants (`loyalty_design_variants`), 2 cells
**What S3 found.** Dream Shield Plus (3.5% to 11% of the 3-year average fund at maturity) and Grow Wealth Ultra (5% of the 5-year average) have the same design as Growth Shield Plus: one large loyalty credit at maturity. v3 codes Growth Shield Plus as B and the other two as blank.

**Proposed rule.** The same design gets the same code. Both become B.

**Decision for the user.** None needed unless you disagree. This is a consistency fix.

## 4. Online terms: customer type or online purchase (`customer_type_boosters` vs `lower_charges_online`), 2 cells
**What S3 found.** Grow Wealth and Wealth Pro charge less when bought online. The definition of `customer_type_boosters` includes "direct buyers", so the same fact could go in two rows.

**Proposed rule.** Online or direct purchase goes only in `lower_charges_online`, which is now B for both, from S3's FAILs. `customer_type_boosters` covers who the customer is: women, staff, existing customers, auto-pay or ECS payers, family purchases. "Direct buyers" is removed from its definition. The two Bharti cells stay blank. S1 checks the peers coded under customer type for online-only reasons and moves them.

**Decision for the user.** None needed unless you disagree.

## 5. Index or low-cost funds (`index_or_low_cost_funds`), 5 cells
**What S3 found.** Only Grow Wealth Ultra has index funds (Nifty 100 Index and Nifty 5Y SDL Index, 0.90%), already coded B. The other five cells are UNSURE because "low-cost fund" has no threshold. Bharti's Stability Plus Money Fund charges 0.80% a year, which is less than the 0.90% on Grow Wealth Ultra's index funds. A money-market fund is cheap because it holds cash-like assets, not because it is a low-cost way to hold equity.

**Proposed rule.** Replace the yes/no row with three rows:
- "Index fund offered" (yes/no): the fund tracks a named index (Nifty 50, BSE 500 Quality 50 and so on). Bharti: Grow Wealth Ultra only.
- "Lowest FMC on an equity fund" (a number).
- "Lowest FMC on any fund" (a number).

The comparison then shows the cost directly and needs no threshold.

**Decision for the user.** Accept the rule, or name a threshold if you want a yes/no (for example "an equity fund at 1.00% or less").
