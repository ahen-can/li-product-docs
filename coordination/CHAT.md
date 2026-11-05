# Coordination channel: S1 (main session) · S2 (second session) · USER

**How to use this file**
- **Newest entries at the top.** Never edit or delete old entries.
- **Before starting any work:** pull or fetch and read the top entries.
- **After each step:** add an entry.
- **Entry format:**
### 5 Nov 2026 · S1 · @S2 QA of the Bharti section of Neha's page, and product-focused additions
**Ask @S2:** follow `briefs/bharti_section_qa_brief.md`. Part 1: check 16 claims in section 2 of deliverable 08 and the decks' Bharti slide against the sources (Bharti's PDs are public on bhartiaxa.com; download what you need into sources/bharti-pd/). Part 2: propose up to 5 additions about Bharti's products (product-level trend, launches and withdrawals, white space, fund performance, exits by product). Output `qa/s2/bharti_section_qa.csv` and a short CHAT entry. Do not edit the page or decks.

### 5 Nov 2026 · S1 · @S2 pay-term grid applied; open items logged
**Done:** results/ppt_grid.csv applied to feature list v5 (analysis/v5/ppt_grid_overrides.csv; 231 cells, 21 changed, 3 kept as "?"). Counts: single pay 51, limited 75, regular 66 of 84. Your open items are logged for the user: the Bharti "base cover" wording (seniors Q22, actions 14), the overlap rule (seniors Q37, actions 15), the Tata rider uploads (actions 16) and the 49 undownloaded riders (actions 17). Decks 07, 09 and page 08 now mention the rider reading.

### 5 Nov 2026 · S2 · @S1 @USER open items waiting on the user
**Status:** these are with the user. Until they are answered, please keep the current codes and mark the cells as provisional.
1. **Bharti waiver wording.** The user will ask Bharti whether "future premiums for the base cover" (Linked Complete Shield Rider 130A012V02, policy document p4) waives the ULIP's own premium or only the rider's. "Base Policy" is defined on p1, but "base cover" is not defined anywhere. Until the answer comes, code Bharti's waiver as rider-delivered with a "to confirm" note.
2. **Three unclear pay-term cases** in `results/ppt_grid.csv`, coded "?":
   - Axis Online Savings Plan: limited pay.
   - ABSLI Wealth Aspire: regular pay.
   - Ageas Platinum Wealth Builder: regular pay.

   In each, the documents give overlapping PT and PPT ranges and no rule. I proposed a rule to the user: "if the ranges overlap and nothing forbids it, count it as allowed", which would make all three Y. That rule is waiting for the user's decision.
3. **Missing Tata AIA rider documents:** OPD Care (110A166V01), 110A167V02, and the Linked Comprehensive Health Rider policy document. The user may upload them to `uploads/tata-aia/riders/`. Until then, treat these riders' cover as "not stated".
4. **The other 49 riders** in `results/riders_universal.csv` (published by the insurers, not named by any of the 84 ULIPs) stay "not downloaded" unless the user asks for them.

### 5 Nov 2026 · S2 · @S1 pay-term grids re-read: 21 changes in 18 ULIPs
**Done:** `briefs/ppt_grid_rescan_brief.md` for the 77 peer ULIPs. Output `results/ppt_grid.csv` (one row per ULIP: single, limited, regular as Y / N / ?, limited PPTs, variants, document, page and quote). Built by `scripts/s2_tools/ppt_grid_build.py` from `scripts/s2_tools/ppt_rows.py`; it checks every quote on its page and lists the changes against v5. Helper `scripts/s2_tools/pptdump.py <UIN prefix>` prints the deep values and the cited pages.

**Changes against v5 (`ppt_single_pay`, `ppt_limited_pay`, `ppt_regular_pay`):** 3 single, 11 limited, 7 regular, in 18 products. 18 go from N to Y and 3 from N to ?.
- Single N to Y: Tata Smart SIP and Shubh SIP (single pay for Wealth/Goal Secure, not for Future/Family Secure), Axis Online Savings Plan Plus (Wealth variant).
- Limited N to Y: Bajaj LongLife Goal III, Goal Assure IV, Goal Based Saving III, Magnum Fortune Plus III, GAIN; Axis Fast Track Super and Shiksha Plus Super (5 Pay on a 10-year term); LIC Protection Plus; ABSLI Salaried Suraksha and Param Suraksha (PPT 6 to 12 on PT 15 to 30).
- Regular N to Y: Bajaj Future Wealth Gain IV and Goal Based Saving III (PPT 10 with PT 10), LIC Index Plus ("same as policy term"), Ageas Wealth Gain and Smart Growth (PPT 20 with PT 20).
- N to ?: Axis Online Savings Plan limited pay (PT and PPT given as the same ranges; policy wording mentions a "Limited Premium" option); ABSLI Wealth Aspire and Ageas Platinum Wealth Builder regular pay (overlapping PT and PPT ranges, no rule either way).
- Every other v5 value held. SBI, HDFC and Canara HSBC had no changes.

**Your two small items:** `__pycache__/` is now in `.gitignore` and the committed `.pyc` files are removed from the index. HDFC Health Plus Rider - Linked: V02 is the newest, but the site publishes it only as a CIS (16 Sep 2026); the brochure and rider document on the site still print V01. The V02 CIS shows the same benefits. Stored as `docs/hdfc-life/riders/101A034V02/cis.pdf`.

### 5 Nov 2026 · S1 · @S3 v4 QA applied (v5); @S2 pay-term grid re-read
**@S3:** thank you. All 87 cell corrections are applied (`analysis/v4/s3_v4_overrides.csv`), and the causes are fixed in code: payor riders now come from the rider JSONs (37 ULIPs), disability waivers count as disability benefit (provisional), admin charge waived some years is derived from the admin charge, flexibility "N" with no evidence is now "?", and a scan picks up online or direct terms. Your five rule questions plus one of mine are in for-your-attention/questions_for_seniors.md (31-36), with provisional answers. Feature list v5 is deliverable 05.
**Ask @S2:** re-read the PT and PPT grids for the 77 peer ULIPs: `briefs/ppt_grid_rescan_brief.md`. Output `results/ppt_grid.csv`. Short task, no downloads.

### 5 Nov 2026 · S3 · @S1 feature list v4 QA done: qa/s3_v4/v4_qa_workbook.xlsx
**Status:** all six tabs filled on branch s3-bharti-analysis (main merged first). Pass rate = PASS / (PASS + FAIL): A 89.5% (94 PASS / 11 FAIL / 1 UNSURE), B 100% (123 / 0), C 83.3% (140 / 28), D 87.6% (219 / 31 / 2), E 99.3% (140 / 1), F 72.8% (67 / 25 / 5). Overall 89.1% (783 / 96 / 8). Every Bharti claim in tab A is right; the tab A FAILs are peer counts that tabs B to F show to be wrong. Each row cites the document, page and quote.
**Riders (tab B):** all 123 PASS. Every rider is named in the ULIP documents and every benefit is in the rider PDF. Notes: HDFC Click 2 Wealth's only CI rider is cancer cover (the value should say so); Tata ULIPs name older rider versions and swap the 110A031/110A032 labels; Tata Smart Sampoorna Raksha Pro names the ADD rider (policy p3), so its disability_benefit should be R.
**FAILs by pattern:**
- Rule 1 was applied only to Axis. 28 more ULIPs name a waiver rider that the payer's own event triggers, and they are still "-" or "Y": HDFC 101A035V01 (3 ULIPs), ABSLI 109A039V01 (9), Tata 110A025V03 (11), SBI 111A049V01 (5). HDFC Click 2 Wealth and SBI Smart Scholar Plus have inbuilt payer waivers coded "Y". child_payor_benefit is about 43 of 84, not 13.
- Pay-term grids (pattern 4) are still wrong in 10 of 25 sampled cells (1 more UNSURE: Ageas Platinum Wealth Builder gives no PT and PPT combination table). Regular pay is missed where PPT can equal PT (LIC SIIP "Same as Policy Term", LIC Protection Plus, Bajaj Goal Assure IV, GAIN, Smart Wealth Goal VII, Axis Online Savings Plan, HDFC Smart Pension). Single pay is missed for Tata Smart Fortune Plus and Bajaj Smart Wealth Goal VII; limited pay for Future Wealth Gain IV. The three pay rows need a full rescan.
- Additions by basis. Missed % of premium: Axis Flexi Wealth Advantage (0.75% auto-debit booster), Axis Smart Term (GLA as % of sum assured), Axis Online Savings Plan Plus (women 1% of AP, existing customers 2.5% or 5%), ABSLI Wealth Secure and Wealth Aspire (2% or 2.5% of premiums paid in 60 months, the design you coded for Fortune Wealth), Bajaj Smart Wealth Goal VII (1.08% additional allocation), Canara Promise4Wealth (1% value booster). Missed % of fund: Tata Fortune Pro ("?"), Smart Raksha, Shubh Wealth. Wrong "only for": Tata Wealth Pro, Fortune Pro, Fortune Maxima and Wealth Maxima pay loyalty additions to everyone, and only the Fund Booster is online; Shubh SIP's "Family Secure" is a plan option, not family customers; Fast Track Super and Shiksha Plus loyalty is regular pay only; GBS III additional allocation is not single-pay only; Magnum Fortune Plus III maturity booster is for existing, auto-pay, online and staff buyers (policy p12). Grow Wealth Ultra's detail misses the Milestone Benefit.
- Funds. Index detection by name misses 11 products: HDFC (5, funds "aligned to the constituents of index"), Ageas (5, funds that "will track" a named index) and Tata Smart Pension Secure. Tata Whole Life Aggressive Growth is 50-80% equity, so the lowest equity FMC in 12 Tata products is 1.20%, not 1.10%. Smart SIP got the shared Tata fund list (its own lowest is 1.20% for any fund). Tata Smart Pension Secure has per-fund FMCs (0.80% Income Pension, 1.25% Future Equity Pension). Axis Platinum Wealth has the NIFTY Smallcap Quality Index at 1.00%. LIC equity was taken by name although the asset ranges are given.
- Online and staff terms (rule 4) missed: Ageas ProGrow and Golden Years ("staff and online"), HDFC Smart Pension, Bajaj LongLife Goal III and Magnum Fortune Plus III have lower_charges_online blank (and online_discount "-" for the last three).
- admin_charge_waived_some_years: 7 of 10 sampled blanks should be B. Derive the row from policy_administration_charge.
- Silence coded N: ABSLI Param Suraksha and Wealth Infinia top-up should be "?". SBI Smart Scholar Plus policy_loan should be N ("Your Policy will not be eligible for any loans").
- Single cells: LIC New Pension Plus is a pension product ("A Non-par, Linked, Pension, Individual Savings Plan"), so its pension row is "?", not "not a pension product". Bajaj Fortune Gain II waiver_of_premium has the code "n/a".
**Rules that need a decision (@USER, via S1):**
1. Equity fund threshold. The 60% equity minimum excludes LIC's Growth (40-80%) and Flexi Growth (40-100%) funds and Ageas Golden Years' two equity funds (50-100%), so those products have no "equity fund". Keep the rule, or use the fund objective or the maximum?
2. restricted_withdrawals. "Capped (amount or number)" fits most ULIPs; my own v3 call coded Future Invest B for 2 a year. Set a threshold, or narrow it to purpose lists.
3. disability_benefit. The definition says "benefit / waiver", but v4 counts only payouts, not disability-triggered waivers (ABSLI, HDFC and Tata waiver riders).
4. Rule 1 edge case. In child variants where the life assured is the paying parent (Bajaj Smart Wealth Goal VII Child Wealth, Axis Shiksha Plus Super, SBI Smart Scholar Plus), does the inbuilt waiver count as payor benefit?
5. "Only for" tags. v4 sometimes tags a condition that applies to one component and sometimes leaves it out (SBI Smart Fortune Builder vs Smart Invest Builder have the same design). Pick one convention.

  `### 5 Nov 2026 · S3 · @S1 feature list v3 QA (Bharti) done: qa/s3_v3/v3_qa_workbook.xlsx
**Status:** all three tabs filled on branch s3-bharti-analysis (main merged first). Pass rate = PASS / (PASS + FAIL): A 70.4% (69 PASS / 29 FAIL / 5 UNSURE), B 91.1% (641 / 63 / 17), C 100% (3 / 0). Rider PDFs and sources.csv rows are in manual-uploads/bharti-life/ (130A012V02, 130A034V01, plus 130B005V05 to rule it out). Summary tab notes give the method and the two coding rules I used.
**Answer to your "to confirm":** waiver of premium via rider is confirmed. Rider 130A012V02 brochure p1: "The Waiver of Premium benefit is also available for event arising due ATPD, SCI and CCI-major conditions option." It attaches to 6 of 7 ULIPs (all but Future Invest). Premium Waiver Rider 130B005V05 is for non-linked products only.
**FAILs (feature: product, correct value):**
- Riders. waiver_of_premium: DSP, GW, GWU, GSP, WM, WP R; FI ? (not N). disability_benefit: same six R. critical_illness: DSP, GW, GWU, GSP, WM R (WP already R). accidental_death_extra: GWU, WM R. riders_available: WM R (brochure p11).
- Payment terms. ppt_single_pay: WP B (Growth variant). ppt_regular_pay: DSP N (PPT 6-12 vs PT 15-40); GW B (PT 20 / PPT 20); GSP B (PPT 30/30 and 40/40).
- v1 keywords. pension_ulip_guaranteed_vesting: DSP, FI, GW, GWU, WM N (quote is the fund table). tax_benefit_mention: DSP, GWU Y. online_discount: GW, WP Y.
- New features. high_cover_multiple: DSP, GSP B (up to 100x AP); GW, WP B (10x single premium). mortality_as_ialm_share: DSP, GSP, GWU B (100% IALM 2012-14), WM B (84.5%). lower_charges_online: GW, WP B. min_fund_termination: FI, GWU B (so all 7). admin_charge_waived_some_years: FI, WP B. restricted_withdrawals: FI B (max 2 a year). refund_fmc_or_all_charges: GWU N (FMC not returned).
- Flags and values. policy_loan: FI, GW N (CIS "Not Applicable"). auto_strategies: FI ? not N. change_ppt_or_term: GWU ? (evidence is about plan option). nil_policy_admin_charge: GWU O (Wealth option, AP Rs 50 lakh+). partial_withdrawal_charge and surrender_value_rule: WM filled (any number free; standard lock-in rule). discontinuance_charge: DSP has an above-Rs 50,000 column (6/4/3/2%). sum_assured_rule: GW regular/limited is higher of 10x AP or 0.5 x PT x AP. GWU entry_age_min, entry_age_max, maturity_age_max: columns are DBM 5/7/10, not PPT; maturity values for DBM 7 are 80-90 and for DBM 10 are 75-85. premium_modes: GWU quarterly and monthly are both auto pay only.
**UNSURE (needs a rule from S1 or USER):** child_payor_benefit (rider WoP can be opted by a policyholder who is not the life insured, but the trigger names the life insured); scheduled_guaranteed_additions vs wealth_boosters for DSP and GWU milestone benefits; loyalty_design_variants for DSP and GWU (same maturity design as GSP, which is B); customer_type_boosters vs lower_charges_online for online terms; index_or_low_cost_funds (no FMC threshold; Stability Plus Money Fund is 0.80%).
**Patterns likely to affect peers:** (1) rider-delivered WoP, disability and CI coded N or '-'; check every peer whose brochure has a rider table. (2) v1 keyword rows that match fund tables or boilerplate (pension, tax). (3) "Has" lists that drop products whose feature sits in the policy bond but not the brochure highlight (min fund termination, IALM basis, admin waived some years). (4) Grid misreads: regular pay is PPT = PT, which v3 missed in two products. (5) Table column labels copied wrong (DBM read as PPT). (6) Policy loan left '?' when the CIS says "Not Applicable".

### 5 Nov 2026 · S1 · @S3 feature list v4 QA: qa/s3_v4/s3_v4_qa_brief.md
**Status:** feature list v4 is built (deliverable 05, now `05_feature_list_ulip_v4.xlsx`). It is a draft until your QA. It has your 63 Bharti corrections, the rider coding from S2's 30 rider documents, the user's coding rules (additions split by % of premium or % of fund; payor waiver needs the payer's own event; online terms in one row; index funds and lowest fund charges) and scans of all 84 for your patterns.
**Ask @S3:** QA v4 per the brief: `qa/s3_v4/v4_qa_workbook.xlsx`, 887 rows in 6 tabs. Tab B (riders) first, then C and D (new rows), then E, F, A. Merge main into your branch first.

### 5 Nov 2026 · S1 · @S2 riders merged and coded into v3
**Status:** S2's branch (all 10 insurers, 30 riders) merged into main. Feature list v3 and the comparison (deliverables 05, 06) rebuilt.
**Done:** build_ulip_features.py now reads results/ulip_rider_benefits.csv. 112 cells moved to R: 19 Bharti cells that S3 had already corrected, plus 93 peer cells (waiver 12, critical illness 18, accidental death 16, disability 47). 5 earlier R codes came only from a rider name and are now "?": SBI's waiver rider waives premium on CI but pays no CI benefit (4 SBI ULIPs), and Bajaj Magnum Fortune Plus III's rider waives only its own premium. S3's 63 Bharti overrides are applied. Counts over the 84: waiver 60 (built-in 11, option 17, rider 32), critical illness 55, accidental death 67, disability 53. A term rider alone does not count as accidental death cover.
**Tally (analysis/riders/rider_list_council.xlsx, tab "Tally vs S2"):** 54 riders in both lists. Every linked (A) rider the Council lists for the 10 insurers is in S2's list, except HDFC Health Plus Rider, where the Council has V02 and S2 has V01. The 46 Council-only riders are non-linked (20 individual, 25 group), so ULIPs cannot use them. 8 are S2-only (the 3 on the Tata retry list, Bharti 130B010V01, and versions).
**@S2 small things:** scripts/rider_specs/__pycache__/ got committed; please delete it and add __pycache__/ to .gitignore. Check whether HDFC Health Plus Rider - Linked V02 is the current version.

### <date time IST> · <S1|S2|USER> · <topic>` then **Status**, **Done**, **Asks / blockers**, **Answers to earlier asks**.
- **Where it lives:** S1 writes on `main`. S2 writes on its own branch (S1 merges S2's branch into main regularly, so both see one history). If an entry needs action from the other session, start it with `@S1` or `@S2`.
- **Decisions belong to the USER.** If a session needs one, write `@USER` and also tell the user in chat.

---

### 5 Nov 2026 · S1 · @S2 rider JSON format approved; @S3 v3 QA received
**@S2:** the rider format is approved. Go ahead with the peers. Two small changes for consistency:
1. Use one status set for benefits: "covered", "covered as an option", "not covered", "not stated". Use "n/a" (not "covered") for the terms fields (rider term, premium rules, entry age, sum assured, deduction). Bharti currently mixes "not offered" and "not covered".
2. Where the waiver wording leaves it unclear whether it waives the ULIP's premium or only the rider's (your "base cover" point), keep a note field saying so for every rider with that wording. We will ask the user's contacts.
Two sets of Bharti rider PDFs now exist (yours in docs/bharti-life/riders/, S3's in manual-uploads/bharti-life/). Keep yours as the source; S3's stay as QA evidence.
**@S3:** thank you. All FAILs will be applied by S1 to feature list v3 (next session). The UNSURE items need rules; S1 will propose them to the user.

### 5 Nov 2026 · S2 · @S1 Tata AIA rider uploads read: one useful, one is the wrong insurer
**Done:** the user uploaded 4 Tata AIA files in `uploads/tata-aia/riders/`.
- Vitality Health Plus v3 and Vitality Protect Plus v4 brochures are byte-identical to the ones already stored (110A047V03, 110A048V04).
- **Linked Comprehensive Health Rider 110A031V02** was missing. Stored as `docs/tata-aia/riders/110A031V02/brochure.pdf` (user upload, no policy document), with `features/riders/110A031V02.json`. Its ULIP documents name this exact version. It has the same five options as Vitality Health Plus (accidental disability, multistage critical illness with 39 conditions, cancer care, cardiac care, HospiCare). It has no waiver of premium.
- **OPD Care is the wrong insurer.** The file is a Tata AIG General Insurance health rider (UIN TATHLIA25035V012425), not Tata AIA Life's 110A166V01. Not stored. 110A166V01 and 110A167V02 remain on the retry list.
- Map, benefits table and summary updated (31 riders, 61 documents).
- `scripts/rider_collect.py` now takes `upload:PATH` for user-supplied files.

### 5 Nov 2026 · S2 · @S1 rider discovery done for all 10 wave 1 insurers
**Status:** done, pushed on my branch. The two lists you and the user asked for are in `results/`.

**Done:**
- 30 riders, 60 documents (brochure and policy each) in `docs/<insurer>/riders/<UIN>/` with `index.csv` rows (`rider_brochure`, `rider_policy`) and text. `check_consistency.py`: 0 problems.
- 30 rider JSONs in `features/riders/`, every quote checked on its page by `scripts/rider_json.py`. Your two changes are applied (statuses covered / covered as an option / not covered / not stated; terms n/a; a note on every waiver saying whether it waives the ULIP premium).
- `results/ulip_rider_map.csv` (219 rows, all 84 ULIPs), `results/ulip_rider_benefits.csv` (per ULIP: which riders give waiver, critical illness, accident, term, hospital cash), `results/rider_summary.md`.
- **Two lists:** `results/riders_downloaded.csv` (one row per document) and `results/riders_universal.csv` (80 riders the insurers publish, 30 downloaded, rest marked for later).

**What the riders show:** 44 of 84 ULIPs name a rider that waives the ULIP's own premium (SBI, HDFC, Tata, ABSLI, Axis Max as payor benefit on death or terminal illness only). Bajaj, Canara HSBC, Ageas and LIC have none. Bharti's is unclear (wording "base cover"). HDFC's Protect Plus and Health Plus and Bajaj's Care Plus waive only the rider's own premium. 54 ULIPs name a critical illness rider and 64 an accident rider. Tata AIA's linked riders take their charge from units; SBI, HDFC, Bajaj, Axis and ABSLI riders use a separate premium.

**Asks / blockers:**
- @S1 recode the rider-delivered features in v3 from the JSONs and `ulip_rider_benefits.csv`. Note Tata's ULIP documents name older rider versions (V02) than the site publishes (V03 to V05).
- Retry list: Tata Linked Comprehensive Health Rider, OPD Care, 110A167V02. Several `premium_deduction` fields say "not stated" and need a second read.
- @USER the Bharti waiver wording ("future premiums for the base cover") needs an answer from Bharti, as S1 said.

### 5 Nov 2026 · S2 · @S1 @S3 Bharti riders done: documents, JSONs and map are pushed
**Status:** Bharti first pass of `briefs/rider_discovery_brief.md` is done. Peers next, in the wave 1 order.

**Done:**
- 2 riders, 4 documents (brochure and policy each) in `docs/bharti-life/riders/<UIN>/`, with `index.csv` rows (`rider_brochure`, `rider_policy`) and text. Linked Complete Shield Rider 130A012V02 and Cover Plus Linked Term Rider 130A034V01. `check_consistency.py` reports 0 problems.
- `features/riders/130A012V02.json` and `130A034V01.json`: every value has document, page and a quote the builder found on that page (`scripts/rider_json.py`).
- `results/ulip_rider_map.csv`: 11 rows for the 7 Bharti ULIPs. Future Invest names no rider.
- `results/riders_downloaded.csv`: the running list of riders downloaded (one row per document). `results/rider_summary.md` has the Bharti section.

**Answer to the brief's example:** waiver of premium is inside the Linked Complete Shield Rider, as an option on accidental total and permanent disability, a standard critical illness or a major comprehensive CI condition. Not on death. It is paid as a separate rider premium. So Bharti does have waiver of premium, as a rider on 6 of 7 ULIPs. Feature list v3 codes it "N", and also codes the rider's accident death, critical illness and disability differently across Bharti products. Details in `qa/s2/s2_qa_workbook.xlsx`, tab "Bharti lacks audit". Wealth Pro (online allocation charge 6% vs 9%) and Grow Wealth (online admin 0.10% vs 0.15%) also have online terms that v3 misses.

**Open point:** the waiver wording says "future premiums for the base cover". The rider defines "Base Policy" as the ULIP, so it may waive the ULIP premium or only the rider's. The documents do not settle it.

**Asks / blockers:**
- @S3 you can skip your own rider download for Bharti.
- @S1 please recode the rider-delivered Bharti features in v3 from the two JSONs.

### 5 Nov 2026 · S1 · @S2 rider documents for the 84 ULIPs
**Ask @S2:** follow briefs/rider_discovery_brief.md. Rider list: briefs/ulip_riders_named.csv. Bharti first (130A012V02, 130A034V01 and any other Bharti rider); push and post here when Bharti is done.
**@S3:** once S2 posts that Bharti's riders are in, use them for tab C of your v3 QA instead of downloading them yourself.

### 5 Nov 2026 · S1 · Merged S2 and S3; new QA task for S3
**Status:** S2's walkthrough page, restyled deck and QA workbook, and S3's Bharti trend analysis, are merged into main. The Field Guide is renumbered to deliverable 10. Fixed in both decks (07 and 09) per S2's audit: free switches 6 of 7, loyalty 6 products, top-ups "not stated", online terms in Wealth Pro and Grow Wealth. The waiver-of-premium-via-rider point is marked "to confirm": Wealth Pro's brochure describes the Complete Shield Rider only as additional sum assured on a covered event.
**Ask @S3:** QA feature list v3, Bharti first: qa/s3_v3/s3_v3_qa_brief.md. Start by downloading Bharti's rider documents.

### 5 Nov 2026 · S3 · @S1 Bharti portfolio fix re-checked: PASS
**Status:** checked deliverable 01 at aee8017. Every figure in the FY26 reconciliation matches the PDs and Product Performance (937.21, 309.28, 212.04, 97.24, 627.93, 292.67, 335.26, 504.71, 131.38, 1,068.60). The 90% claim, the Rs 3.3 cr split and the old shares are gone; shares use Rs 937.21 cr; FY24/FY25 coverage caveat is in the notes. Recorded in qa/s3/s3_qa_workbook.xlsx tab D as FAIL found ad hoc, with the reconciliation and this re-check.
**One minor item (pre-dates your fix):** the "PD category Non-Par Life: Rs 2,084 cr = 0.47% / 0.97%" headers (rows 42 and 93) use non-par life + pension + annuity, while Summary and Mapping define Non-Par Life as NL only (Bharti Rs 2,021 cr; 0.70% of industry, 1.10% of private). Non-par pension Rs 62.9 cr then also appears in the Pension & Annuity header (Rs 64 cr). Suggest the NL-only figures.
**FYI:** deliverable 01 stores no cached formula values (1,225 formulas, also true before your fix). Excel and LibreOffice recalculate on open; viewers that do not recalculate show blank shares.

### 5 Nov 2026 · S3 · QA round done: @S1 results in qa/s3/s3_qa_workbook.xlsx
**Status:** all 255 checks filled on branch s3-bharti-analysis (main merged in first). Pass rate = PASS / (PASS + FAIL): A 97.8% (87/2/1 UNSURE), B 98.0% (97/2/1), C 100% (30/0), D 100% (8/0), E 100% of 5 checked (7 ICICI rows UNSURE: iciciprulife.com returns 403), F 71.4% (10/4/1). F is below the 95% target.
**Top 3 FAILs:**
1. F row 15 and 16: ppt flags wrong. Bharti Grow Wealth (130L088V04) has regular pay (brochure PT/PPT table: 5/5, 10/10, 15/15, 20/20), deep says not offered; Bajaj Smart Wealth Goal VII (116L218V01) has single pay (Joint Life Wealth variant). These change Bharti's gap analysis.
2. B rows 4 and 12: S1 rejected features the products have. HDFC Smart Pension Plan has lower online allocation charges (4% vs 12% in year 1); HDFC Click 2 Retire Plus II allows vesting postponement to age 75. Also F rows 6 and 18: Axis Forever Young Pension "Save More Tomorrow" is a premium step-up, not a portfolio strategy; Tata Smart Fortune Plus has an accidental death rider (110A027V02).
3. A row 23: Tata Wealth Maxima (110L114V05) minimum partial withdrawal is Rs 5,000 (policy p7), deep says Rs 1,000 (copied from Smart Fortune Plus).
**Found ad hoc (bottom of tabs):** D: the Bharti portfolio tab treats the 8 products as 90% of FY26 NBP (total about Rs 561 cr); they are the current FY27 list and were 53.9% of FY26 individual NBP (Rs 937 cr, PD L-38), so the "other products" remainder is understated by about Rs 430 cr. A: SBI Smart Fortune Builder misses its periodic Guaranteed Additions (years 10-30). E: HDFC YoungStar Udaan shows as discontinued on its product page but active on the all-products page.

### 5 Nov 2026 · S3 · Bharti analysis done: @S1 please merge s3-bharti-analysis
**Status:** all four brief steps are pushed on branch s3-bharti-analysis. No PR opened.
**Files (analysis/bharti/):** document_inventory.csv (61 rows), bharti_trend_data.csv (2,258 rows), bharti_analysis.xlsx (tabs Notes, Bharti trend, Bharti KPIs, Bharti product trend, Peer view FY26, Sources), bharti_findings_FY21_to_FY27.md (15 observations, gaps, 7 questions), scripts/build_trend_data.py and scripts/build_excel.py (run in that order; build_excel needs openpyxl). The user asked for a descriptive name instead of findings.md.
**For S1:** copy the five data tabs into deliverable 01 next to "Bharti portfolio", and keep the Notes tab: it carries sources, rounding notes, the EoM / forbearance / show-cause quotes, and the IRDAI distribution-reform consultation paper (Sep 2026) with Bharti implications. Product NBP for FY24-FY26 and FY27 periods can replace the estimated values in "Bharti portfolio". PROJECT_MEMORY section 5 is confirmed; FY24 linked share of individual NBP is 17.9%. please_check.md "Bharti analysis (S3)" items are all resolved by the user.

### 5 Nov 2026 · S3 · Bharti analysis step 3: Excel
**Status:** analysis/bharti/bharti_analysis.xlsx pushed on s3-bharti-analysis, built by scripts/build_excel.py from bharti_trend_data.csv (now 2,251 rows incl. peers). Next: findings file.
**Done:** tabs Notes, Bharti trend, Bharti KPIs, Bharti product trend, Peer view FY26, Sources. Peer view covers all 13 peers (persistency and conservation from each FY26 PD L-22; segment mix and growth from deliverable 01 Data tab). Yellow cells are reconstructed (FY23) or derived (FY25, FY26) segment NBP; the user approved both.
**For S1:** the Notes tab lists sources, rounding differences and caveats; please keep it when copying tabs into deliverable 01.

### 5 Nov 2026 · S3 · Bharti analysis step 2: trend data (FY21 to Q1 FY27)
**Status:** analysis/bharti/bharti_trend_data.csv (1,689 rows) and scripts/build_trend_data.py pushed on s3-bharti-analysis. Next: peer L-22 extraction, then the Excel.
**Done:** premium by segment (L-1-A-RA), L-4, L-22 ratios and persistency, channels (L-37, L-38), AUM (L-3), death claims (L-40), EoM against the limit (annual reports), KPI sheet, product performance and 90% lists. Segment NBP from annual-report Schedule 1 for FY21 to FY24; FY23 reconstructed from a misprinted comparative; FY25 and FY26 derived from L-22 growth and flagged.
**For S1:** your section 5 figures hold. Linked share of individual NBP FY24 is 17.9%. Par fell from 38.2% to 18.6% of gross premium; non-par individual life rose from 44.6% to 58.0%. EoM exceeded the limit every year FY21 to FY25 (not only FY25); FY26 is within the limit. Doubts are in for-your-attention/please_check.md under "Bharti analysis (S3)".

### 5 Nov 2026 · S3 · Bharti analysis step 1: inventory
**Status:** branch s3-bharti-analysis, file analysis/bharti/document_inventory.csv (52 rows). Next: trend data.
**Done:** Bharti PDs FY22 to FY26 and Q1 FY27 (FY24 PD now in hand), annual reports FY21 to FY26, KPI files, and FY26 PDs for all 13 peers. The file "fy2025 - L1-to-L45-consolidated-q4.pdf" is the FY26 PD. The "H2 FY27" KPI files cover Apr to Sep 2026 (H1).
**Asks / blockers:** annual reports FY23, FY25 and FY26 are scanned and need OCR; the user is installing tesseract. Peer PDs live on the user's laptop only (Desktop/LI-PDs), so S1 cannot see them.
### 4 Nov 2026 · S2 · ULIP deep: quote cleanup pass
**Status:** 51 more short-value fields now carry a quote with the number (109 in total). One wrong value found and fixed: SBI Smart Invest Builder (111L153V01) form number is 841, not 859. All 84 files pass validation.

**Left:** 38 short-value fields, mostly Tata and SBI discontinuance and premium paying term rows. Listed in `results/deep_ulip_wave1_report.md`. Tool: `scripts/s2_tools/fq.py`.

**Asks / blockers:** none.


### 4 Nov 2026 · S2 · i Systematic V11 documents in
**Status:** Tata AIA i Systematic (110L164V11) is rebuilt from your 3 uploads. All 84 JSON files pass validation and the cross-check is clean.

**Done:** Policy document and brochure print V11. The CIS prints V10, noted in the index. The old V04 brochure stays stored but is not used for values. The mortality table is on Tata's website, logged as not public.

**Asks / blockers:** none.


### 4 Nov 2026 · S2 · ULIP deep: wave 1 report
**Status:** Wave 1 is complete: 84 of 84 ULIPs, all files validate, 0 consistency problems. The report is `results/deep_ulip_wave1_report.md`.

**Done:**
- **Cross-check.** `scripts/s2_tools/crosscheck.py` (documents, sha256, UIN, text) and `valuecheck.py` (do the numbers in a value appear in its quotes) now run over all 84 files.
- **Redo list.** 61 fields in 28 files now carry a value-bearing quote. Bharti Grow Wealth Ultra's administration charge is a table. Bajaj Smart Wealth Goal VII Child Wealth and Joint Life Wealth are captured as 6 quoted entries.
- **Left.** 89 short-value fields still have quotes without the number (Tata AIA 21, SBI 17, Axis Max 14, HDFC 10, Canara 8, Bajaj 7, ABSLI 6, Bharti 6). About 300 more are long composite values.

**Asks / blockers:** @USER please upload the Tata AIA i Systematic V11 policy document, CIS and brochure (110L164V11). Only a V04 brochure is public.


### 4 Nov 2026 · S2 · ULIP deep: Ageas Federal done, wave 1 collected
**Status:** All 84 wave 1 ULIPs now have a feature JSON. Next: the cross-check of every file and the wave report.

**Done:**
- **Ageas Federal (6).** 6 sample policy documents, 6 CIS, 6 brochures. No BIs. All 84 JSON files pass `validate_ulip_json.py`, and `check_consistency.py` reports 0 problems.
- **Gaps.** ProGrow prints no mortality table. Wealth Gain's table has no row for age 61. The one-page "Flyer" or "KFD" files on three product pages were not stored.
- **Open from the redo list.** Tata i Systematic V11 (waiting for your upload), the Bajaj Smart Wealth Goal VII Child Wealth and Joint Life Wealth retry, Bharti Grow Wealth Ultra's admin charge as a table, and the older label-only quotes in the first 35 files.

**Asks / blockers:** none.


### 4 Nov 2026 · S2 · ULIP deep: Canara HSBC done
**Status:** Bharti, SBI, HDFC, Tata AIA, Bajaj, Axis Max, LIC, ABSLI and Canara HSBC are complete (78 of 84). Next: Ageas Federal (6).

**Done:**
- **Canara HSBC (8).** 8 policy documents, 8 CIS, 8 brochures. No BIs. All 78 JSON files pass `validate_ulip_json.py`, and `check_consistency.py` reports 0 problems.
- **Gaps.** Promise4Growth has no product page, so its PDFs came from the file-name pattern of Promise4Growth Plus (UINs checked, notes in the index). The policy documents are samples with no mortality table, so mortality rates are the brochure's sample ages.

**Asks / blockers:** none.

### 4 Nov 2026 · S1 · @S3 your Bharti NBP finding: confirmed and fixed
**Status:** you were right. Bharti's monthly report (p2) says the 8-product list is based on "NBP of all products for FY 2026-27 as on Sep 30, 2026". I checked your PD figures: L-38 p58 individual total 93,721 lakh, L-37 p57 group 13,138 lakh, L-4 p8 first year 90,487 and single 16,373 lakh, L-22 p29 linked share 33.0%. All match.
**Fixed in deliverable 01, Bharti portfolio tab:** removed the 90% assumption and the Rs 3.3 cr even split; added an FY26 reconciliation (individual NBP Rs 937.2 cr; ULIP Rs 309.3 cr; 4 other ULIPs Rs 97.2 cr derived; 13 other non-linked products Rs 335.3 cr derived, not split by category because the PDs do not split non-linked NBP); shares now use individual NBP as the base; undisclosed products show "not disclosed". I did not use your derived par and non-par segment NBP, because the FY26 PD alone does not give it; if your FY25 PD lets you derive it with sources, post the method.
**Ask:** record this in your QA workbook as a FAIL found ad hoc, with your reconciliation, and keep going.

### 4 Nov 2026 · S2 · ULIP deep: ABSLI done
**Status:** Bharti, SBI, HDFC, Tata AIA, Bajaj, Axis Max, LIC and ABSLI are complete (70 of 84). Next: Canara HSBC (8), Ageas Federal (6).

**Done:**
- **ABSLI (10).** 10 policy documents, 8 CIS, 10 brochures. No BIs. All 70 JSON files pass `validate_ulip_json.py`, and `check_consistency.py` reports 0 problems.
- **Gaps.** Fortune Wealth and Salaried Suraksha link no CIS. Wealth Aspire's policy document prints no product code, so it is stored with a note and not quoted. Charges and benefits are quoted from the brochures.

**Asks / blockers:** none.


### 4 Nov 2026 · S2 · ULIP deep: LIC done
**Status:** Bharti, SBI, HDFC, Tata AIA, Bajaj, Axis Max and LIC are complete (60 of 84). Next: ABSLI, Canara HSBC, Ageas Federal.

**Done:**
- **LIC (5).** 5 policy documents, 5 CIS, 9 brochures (four products link an old and a new brochure; the JSON uses the one from 22/09/2025). No BIs. All 60 JSON files pass `validate_ulip_json.py`, and `check_consistency.py` reports 0 problems.
- **Gap.** The LIC policy documents print no charge or mortality tables, so charges come from the brochures and mortality rates are sample ages only.

**Asks / blockers:** none.


### 4 Nov 2026 · S2 · ULIP deep: Axis Max Life done
**Status:** Bharti, SBI, HDFC, Tata AIA, Bajaj and Axis Max are complete (55 of 84). Next: LIC, ABSLI, Canara HSBC, Ageas Federal.

**Done:**
- **Axis Max (9).** 8 policy documents, 8 CIS, 9 prospectuses. No BIs. All 55 JSON files pass `validate_ulip_json.py`, and `check_consistency.py` reports 0 problems.
- **Documents found off the visible links.** Forever Young's policy document and CIS are in its page source. The Online Savings Plan Plus page links Online Savings Plan documents (UIN 104L098V06), which I stored under that product.
- **Gap.** Online Savings Plan Plus has no policy document of its own, so no mortality table.

**Asks / blockers:** none.


### 4 Nov 2026 · S2 · ULIP deep: Bajaj Life done
**Status:** Bharti, SBI, HDFC, Tata AIA and Bajaj are complete (46 of 84). Next: Axis Max, LIC, ABSLI, Canara HSBC, Ageas Federal.

**Done:**
- **Bajaj (11).** 11 policy documents, 13 CIS and 13 brochures. No BIs. Supreme and Smart Pension policy documents are not linked on their pages; I found them by the site's file-name pattern. All 46 JSON files pass `validate_ulip_json.py`, and `check_consistency.py` reports 0 problems.
- **Smart Wealth Goal VII (116L218V01).** It has three variants. The JSON records the Wealth variant field by field. Child Wealth and Joint Life Wealth are on the retry list.
- **Label change.** Bajaj labels every document "Download". `scripts/ulip_json.py` now tags later stored files with the same label as "Download (file name)". The first one keeps "Download".

**Asks / blockers:**
- Smart Pension: the site's policy document is V03, not V08. Every value from it is flagged.
- Fortune Gain II: the mortality annexure and the admin charge are not in its policy document.

### 4 Nov 2026 · S2 · Calculator products redone
@S1 the charge, eligibility and addition fields of your six calculator products are redone: 130L100V03, 130L123V01, 130L121V01, 111L147V01, 101L133V03 and 101L180V01. Every quote now contains its value, and charge tables are nested numbers. Mortality notes give the rate-table pages and a few sample rates.
- **New fields.** A table too long for one 300-character quote now uses `quote_2` to `quote_4`, each with `page_2` to `page_4`. `validate_ulip_json.py` checks them the same way as `quote`.
- **Changed value shapes.** Some values that were text are now objects. For example, Sampoorn Nivesh Plus allocation charges are lists by premium band, and entry ages are dicts by option or term. Please re-read these if your calculator parsed the old strings.

### 4 Nov 2026 · S2 · S2 project memory added
@S1 my working context is now in `S2_PROJECT_MEMORY.md`, and my reading tools are in `scripts/s2_tools/`. The format answer is received. Per the user: the new quote rule applies from Bajaj onwards, old quotes get redone at the end of wave 1, and first I redo the charge, eligibility and addition fields for your six calculator products (130L100V03, 130L123V01, 130L121V01, 111L147V01, 101L133V03, 101L180V01).

### 4 Nov 2026 · S2 · ULIP deep: Tata AIA done
**Status:** Bharti, SBI, HDFC and Tata AIA are complete (35 of 78). Next: Bajaj, Axis Max, LIC, ABSLI, Canara HSBC.

**Done:**
- **Tata AIA (14).** 13 policy documents and 13 CIS. The "Quote/Benefit Illustration" link opens a quote web page, so there are no BIs. All 35 JSON files pass `scripts/validate_ulip_json.py`.
- **Gaps.** i Systematic Insurance Plan's page links only the V04 sales literature (the deep set lists V11), so its JSON is brochure-only with every value flagged. Smart Sampoorna Raksha Pro's brochure is image-only with no readable UIN, so its eligibility is "not stated".
- **Mortality rates.** Several Tata policies do not print them: two say they are on the website, and five name no place at all. These are listed under `data_not_public`.

**Asks / blockers:**
- @S1 the format question on `features/ulip/130L100V03.json` is still open. I am keeping the same format.

**Answers to earlier asks:** none.
### 4 Nov 2026 · S1 · New session S3 for the Bharti analysis
**Status:** the user is starting S3 on their laptop for the Bharti trend and portfolio analysis. Brief: briefs/bharti_analysis_brief.md. S3 works on branch s3-bharti-analysis in analysis/bharti/ only. S2 is not affected.

### 4 Nov 2026 · S1 · Ageas Federal added to wave 1
**Ask @S2:** the user picked Ageas Federal as the third ULIP challenger. Its 6 ULIPs are now in briefs/ulip_deep_set.csv as wave 1. Please do them after Canara HSBC. Wave 1 is now 84 products. Light-pass notes for the Ageas site are in results/site_quirks.md (files on Azure blob storage; two pages link a UAT storage account).

### 4 Nov 2026 · S1 · Format approved, merged, 4 small changes
**Status:** your Bharti, SBI and HDFC work (21 JSON files) is merged into main. All files pass validate_ulip_json.py. ULIP feature list v2 is built from them (analysis/feature_list_ulip_v2.xlsx). The format works well. Keep it for the remaining insurers.

**Asks @S2, for the remaining insurers:**
1. Each quote must contain the value itself. A label such as "Minimum Entry Age:" alone is not evidence. If the value sits in a table, quote the table row.
2. Give charge tables as numbers in nested objects, the way you did for allocation charges. Bharti Grow Wealth Ultra's admin charge is prose ("table hard to read in text form"); please redo it on your second pass from the layout text. For mortality charges, add the policy-document page range of the rate table in the note.
3. Finish the SBI fields on your second-pass list (revival and surrender for Smart Privilege Plus and Smart Scholar Plus, switching for Smart Scholar Plus).
4. Keep messages short. Write one brief CHAT entry per insurer. Reply to the user in 2 or 3 lines and keep the detail in deep_ulip_summary.md.

Order after Tata: Bajaj, Axis Max, LIC, ABSLI, Canara HSBC.

### 4 Nov 2026 · S2 · ULIP deep: SBI and HDFC done
**Status:** Bharti, SBI and HDFC are complete (21 of 78). Next: Tata AIA, Bajaj, Axis Max, LIC, ABSLI, Canara HSBC.

**Done:**
- **SBI (7).** 7 "Policy Document", 7 CIS, 0 BI. Charges are in clause 17 of each policy document.
- **HDFC (7).** 8 policy documents (Smart Pension Plan has offline and online versions with the same terms). Product pages link no CIS, BI or fund documents. Smart Woman's policy document sits in the site's withdrawn folder but prints the deep-set UIN 101L082V03.
- All 21 JSON files pass `scripts/validate_ulip_json.py`. Odd findings and new features are in `results/deep_ulip_summary.md`.

**Asks / blockers:**
- @S1 the format question on `features/ulip/130L100V03.json` is still open. I am keeping the same format for the remaining insurers unless you say otherwise.

**Answers to earlier asks:** none.

### 4 Nov 2026 · S2 · ULIP deep: Bharti done, please review the format
**Status:** Bharti is complete (7 of 7). Next: SBI, HDFC, Tata AIA, Bajaj, Axis Max, LIC, ABSLI, Canara HSBC.

**Done:**
- **Documents.** 7 "Policy Bond" (one labelled "Policy Bond Part B"), 7 "Customer Information Sheet", 7 "Download Brochure", 0 BI. Fund information is on company-wide web pages ("Fund Factsheet", "Fund Performance"), so I stored no fund documents. Every document link per product page, with its label, is in `results/deep_ulip_docs.csv`. `index.csv` has a new `website_label` column.
- **Features.** `features/ulip/<UIN>.json` for all 7. `scripts/validate_ulip_json.py` checks that every quote appears verbatim on its cited page. Blank fields are "not stated in public documents" with a null value.
- **Summary so far.** `results/deep_ulip_summary.md` covers counts, odd findings and new features. Bharti has several charge-refund designs: 118% of all charges in Wealth Maximizer, 2x allocation charges in Growth Shield Plus, and rising multiples of mortality charges in Dream Shield Plus and Growth Shield Plus.

**Asks / blockers:**
- @S1 please look at one Bharti JSON, for example `features/ulip/130L100V03.json`, before I do the other 71. Value formats (tables as nested objects, notes on doubtful points) are easy to change now.

**Answers to earlier asks:** none.

### 4 Nov 2026 · S2 · ULIP deep discovery wave 1: started
**Status:** started. I pulled `main` and rebuilt my branch `ccr-d0d84e00-joo2mp` on it. My branch also carries one commit `main` doesn't have yet: the unslop writing rules added to `CLAUDE.md`, which the user asked for after the merge. Order: Bharti, SBI, HDFC, Tata AIA, Bajaj, Axis Max, LIC, ABSLI, Canara HSBC.

**Done:** nothing yet.

**Plan:**
- For each product, the collector opens the product page and stores the policy document, CIS, BI and any product-specific fund document. Each file gets the site's own label in a new `website_label` column in `index.csv`, and passes the same checks as the light pass (`%PDF`, `pdfinfo`, UIN in the text).
- `features/ulip/<UIN>.json` per product follows the schema. Values come from the policy document first, each with page and verbatim quote. "Not stated in public documents" means I couldn't find it.
- I'll push after each insurer and post here after Bharti so you can review the format.

**Asks / blockers:** none yet.

### 4 Nov 2026 · S1 · ULIP deep discovery: please start wave 1
**Status:** your light-discovery branch is merged into `main` (516 brochures, results, site quirks). Thank you, the site notes are excellent.

**Ask @S2:** run `briefs/deep_discovery_ulip_brief.md`.
- Wave 1 = 78 ULIPs (SBI, HDFC, LIC, Tata AIA, Bajaj, Axis Max, ABSLI, Canara HSBC, Bharti). Start with Bharti.
- Schema: `briefs/ulip_feature_schema.json`.
- Product list: `briefs/ulip_deep_set.csv`.
- Wave 2 (ICICI, Kotak) waits for the user's manual uploads.

**FYI from S1:**
- Feature list v1 is in `analysis/` and is built from your brochures.
- The scope questions you raised (health and micro rows, Individual/Group annuity lines, HDFC "withdrawn-only" products, Bajaj combination bundles, Tata i Systematic V11 vs V04) are now in `for-your-attention/` for the user and seniors.
- If a document disagrees with the master list, record it; don't change `master_list.csv`.
