# PROJECT MEMORY: read this first (any session, any account)

Last updated: 4 Nov 2026 by S1 (main session). Full decision trail: `docs-internal/plan_history.md`. Live coordination: `coordination/CHAT.md`.


## 0. Latest state (5 Nov 2026, before compaction)
- **Deliverables** (deliverables/README.md):
  - 01 category workbook with the Bharti portfolio tab, fixed after S3 found the "90%" error;
  - 02 product list; 03 light discovery; 04 feature list v1;
  - 05 ULIP feature list v3;
  - 06 ULIP comparison (14 products);
  - 07 deck (artifact https://claude.ai/artifact/3VgZFusjxhJRLpqkBeXNLU, now shared by link);
  - 08 S2's walkthrough page for Neha; 09 S2's HTML deck;
  - 10 ULIP Field Guide (artifact https://claude.ai/artifact/G4BK3Ed5aep7B8ccWEJHom).
- **Merged:** S3's Bharti trend analysis (analysis/bharti/, findings in bharti_findings_FY21_to_FY27.md) and S3's QA rounds (qa/s3, qa/s3_v3).
- **Rule from S2's and S3's audits.** "Bharti lacks" claims must check riders and channel terms, and must not read "not stated" as "not offered". Decks 07 and 09 are corrected for: switches 6 of 7, loyalty 6 products, top-ups not stated, online terms in Wealth Pro and Grow Wealth.
- **Waiver of premium is CONFIRMED** via the Linked Complete Shield Rider 130A012V02 (option on ATPD, standard CI or major CCI; not on death; separate rider premium) on 6 of 7 Bharti ULIPs, all except Future Invest. Decks 07 and 09 still say "to confirm" or "rider only": update them to "via rider on 6 of 7". Open point: whether it waives the ULIP premium or only the rider premium.
- **Done 5 Nov (after compaction):** S3's 63 Bharti cell FAILs applied via analysis/v3/s3_overrides.csv; rider-map recoding in build_ulip_features.py (Bharti now, peers automatically as S2 adds rows to results/ulip_rider_map.csv); deliverables 05 and 06 rebuilt. Comparison now reads corrected cells from product_features_ulip_v3.csv. Universal rider list from the Council sheet: analysis/riders/rider_list_council.xlsx (225 riders, 157 individual, 61 linked "A").
- **S2 riders done and coded (5 Nov):** all 10 insurers, 30 riders, merged. v3 rider recoding now reads results/ulip_rider_benefits.csv (112 cells to R incl. 19 Bharti, 5 name-only R to ?). Counts over 84: waiver 60 (B 11, O 17, R 32), CI 55, accidental death 67, disability 53. Council vs S2 tally: all linked Council riders for the 10 insurers are in S2's list (HDFC Health Plus version aside). NEXT item 3 below is done except the peer QA sample.
- **User decision (5 Nov):** do not update Neha's pages or decks (07-10) for now. Fix our side first, then refresh them together.
- **Feature list v4 built (5 Nov), draft until S3's QA:** user chose option (b) for additions (split by % of premium vs % of fund, "guaranteed" row retired) and accepted rules 1, 3, 4, 5 as proposed. Scans of all 84 for policy loan, min-fund termination, IALM. 476 cell changes in analysis/v4/v4_changes.csv. Deliverable 05 is now 05_feature_list_ulip_v4.xlsx; 06 reads v4. Judgement calls are in for-your-attention/questions_for_seniors.md section E (questions 20-30). User rule: every such judgement call goes into that file.
- **Calculator:** SBI Smart Fortune Builder periodic Guaranteed Additions added (6.00% -> 6.16% at 8% excl. GST). The decks still say 6.00%.
- **S3's v4 QA (5 Nov):** 887 checks, 89% pass; every Bharti claim right; riders 100%. Systemic errors found and fixed in v5: payor riders (rule 1 matched only "payor"), additions basis misses, index funds by name, online terms, admin waived years, silence coded N. Not yet fixed: pay-term grids (S2 re-reading, briefs/ppt_grid_rescan_brief.md). v5 = deliverable 05. Provisional decisions 31-36 in for-your-attention/questions_for_seniors.md.
- **ULIP pilot finalised for Neha (5 Nov):** selection (14 products) unchanged under v5; calculator unchanged except SBI SFB (6.16%); decks 07 (artifact v9) and 09 and page 08 refreshed to v5 numbers (waiver 60 of 84, Bharti via rider not on death; additions by basis; index funds 63; online 28; FMC refund 3 of 84; min-fund termination 13 of 84, all 7 Bharti). Hypothesis line in 08 still the old one; the user has their own wording. User: no other categories until the ULIP pilot is shown.
- **NEXT for S1:**
  1. When S2's results/ppt_grid.csv arrives: apply it (overrides), rebuild v5 (or v6), comparison 06.
  2. Refresh decks 07, 09 and Neha page 08 in one pass (waiver 60 of 84, Bharti "via rider on 6 of 7"; additions by basis; SBI 6.16%; hypothesis line from the user).
  4. SBI and Bajaj BIs when the user sends them.
- **People:** the manual checker is Shobhit (named on the page; earlier notes said Rahul).
- **Sessions:** S2 is on branch ccr-d0d84e00-joo2mp and is doing the peer riders per briefs/rider_discovery_brief.md, with its format approved. S3 is on branch s3-bharti-analysis. Merge both regularly; CHAT.md conflicts resolve as "theirs first, then ours".
- **Git:** local main tracks origin/main (upstream set on 5 Nov).

## 1. Goal and people
- **Goal:** a product-suite analysis of **Bharti Life** (formerly Bharti AXA Life, UIN prefix 130), in two steps:
  1. a market landscape of individual life products by category;
  2. Bharti's gaps and strengths: categories it is missing, features peers have that it lacks, best ideas (including from LIC) and pricing/IRR position.
- **Deliverables:**
  - a feature-list Excel per category;
  - a filled comparison matrix;
  - a PolicyBazaar-style IRR calculator / product comparer;
  - a short PPT observation deck per category.
- **Pilot:** **ULIP end-to-end first**, to show **Neha** (the user's lead) and align.
- **People**
  - The user: ahen-can.
  - **Neha:** the user's lead; receives status updates.
  - **Seniors:** answer the expert questions in `for-your-attention/questions_for_seniors.md`.
  - **Rahul:** manual QA checker (`qa/`).
  - **Industry friends:** will supply data that isn't public.

## 2. Working rules (user preferences, all binding)
- **Official sources only:** insurer websites, IRDAI, the Life Insurance Council, public disclosures (PDs), investor presentations and press releases. No aggregators or news for facts.
- **The insurer's website is the absolute truth.** The Life Council in-force list (Sep-2026) is accurate and is the backbone (user verified it on Bharti and ICICI). **The IRDAI list is dropped** because it is stale.
- **Never assign a category from a product name.** Use only the IRDAI description line printed on the brochure/policy document, the UIN linked flag (4th character L/N), or the Council category label as a flagged fallback.
- **One task at a time; check in; accuracy and thoroughness over speed.** Ask doubts.
- **Raise garbled, OCR or ambiguous items explicitly** with the user and put them in `for-your-attention/`.
- Keep a **log of documents used** per iteration.
- **Don't get around bot protection.** ICICI, Kotak, Star Union Dai-ichi (SUD) and Go Digit block automation, so the user uploads their documents manually.
- **Pushback is welcome.** The user agreed with: calculator/comparer after the ULIP matrix; parameter files from deep data; missing values to be listed for industry friends.
- **Commits** end with:
  ```
  Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
  Claude-Session: https://claude.ai/code/session_01KJxjeqZKs9djTSauiMPhDu
  ```
  No model names in repo content. Don't create PRs unless asked.


## 2a. Output size and fund data (user, 4 Nov)
- **Deck: 5 products per category. Supporting Excel: 10 to 15 products per category.** For ULIP, choose them from the 84 deep products: Bharti's top 2 by NBP (Wealth Pro, Growth Shield Plus), each leader's and challenger's flagship, and LIC as a reference. The user's "My view" tab (deliverable 01) feeds the choice.
- **Fund factsheets are a future integration.** For now use fund ratings. Ratings come from third parties (Value Research, Morningstar), an agreed exception to the official-sources rule, entered manually with the source named.
- **Bharti product-level NBP is official, but partial:** sources/bharti-kpi/ (Product Performance FY24 to H2 FY27, from bhartiaxa.com/kpi-disclosures). It lists 8 products chosen because they make up 90% of NBP in FY 2026-27 to 30 Sep 2026 (Monthly Product Performance report, p2). For FY26 the 8 are only 53.9% of individual NBP (Rs 504.7 of Rs 937.2 cr, PD L-38 p58). Correction made 4 Nov after S3's QA; deliverable 01's Bharti portfolio tab now reconciles to the PDs.

## 3. Repos, branches and environment
- **`ahen-can/boom`** (public): branch `ccr-b8ad4f03-rfkxka`, folder `li-category-analysis/`, holds the phase-1 workbook `life_insurance_category_analysis_Q4FY26.xlsx` and its scripts (`rows.py`, `build_data.py`, `make_xlsx.py`, `data.json`, `notes.json`).
- **`ahen-can/li-product-docs`** (public; the user should make it private): everything else, on `main`.
  - S2 (the user's second Claude account/session) works on branch **`ccr-d0d84e00-joo2mp`**.
  - S1 merges that branch into main after each S2 step (user approved).
  - S3 (a Claude Code session on the user's laptop, with Bharti PDs, annual reports and KPI files) works on branch **`s3-bharti-analysis`**, folder `analysis/bharti/`, per `briefs/bharti_analysis_brief.md`. S1 merges it and copies its tabs into deliverable 01.
- **Network:** the allowlist needs **`www.` / wildcard** entries (`*.hdfclife.com`, etc.). ICICI, Kotak, SUD and Go Digit return 403 or a bot check. S2's environment needs the same allowlist.
- **Local paths (S1 container; may not survive):**
  - `/home/user/li-product-docs` (main);
  - `/home/user/ld-branch` (worktree of S2's branch);
  - `/home/user/boom`;
  - scratchpad `/tmp/claude-0/-home-user/42c9e8ea-081f-5f5b-9023-52021c0c1d32/scratchpad`;
  - the older scratchpad `/tmp/claude-0/-home-user-boom/…/scratchpad` holds `data.json` (phase-1 data; a copy is in boom).
- **User uploads** are in `/root/.claude/uploads/42c9e8ea-081f-5f5b-9023-52021c0c1d32/`:
  - PD zips lipd-1/2/3i/3ii;
  - SBI and PNB MetLife PDs;
  - LIC L-1A;
  - Bharti FY22/FY23 PDs;
  - Bharti FY25 audited results (scanned);
  - the Council PDF and xls;
  - the ICICI/Bharti official lists xlsx;
  - the reference slide photos.

## 4. Done so far (with key numbers)
1. **Phase 1, category workbook** (boom): 25 insurers (LIC + 24 private), FY26 gross premium by segment from PD Form L-1-A-RA.
   - Categories: Par Life, Non-Par Life, Linked, Pension & Annuity, plus a Group overlay from L-25(ii) (group is embedded in segments, so the overlay is not additive). Health and variable insurance are excluded.
   - Every insurer reconciles to its L-1 grand total.
   - Summary, category tabs with observations, selection data.
   - "INLIC" was renamed to IndusInd Nippon Life.
   - LIC's group premium of ₹1,96,609 cr comes from its press release.
2. **Master list v3** (`master_list.csv/.xlsx`): **633 in-scope individual products**.
   - Built from the Council Sep-2026 list, plus the ICICI and Bharti official lists, SBI (27, from its own product pages) and Bajaj (29 + 2 no-UIN bundles, from its official on-sale page).
   - Excluded: Health, Accident and Micro by the Council label, riders (B/A) and govt/combi (G/Y). Saral/POS products are tagged.
   - Audit trails: v1 (Council + IRDAI) and v2 (website-vs-Council scrape) are in `sources/`. The scraping showed the Council list is accurate.
3. **Light discovery** (run by S2, merged): **516 of 633 brochures** (97.9% of reachable products), plus description lines, `index.csv` with source URLs, `results/light_discovery_summary.md` and `results/site_quirks.md` (where each site keeps policy documents and BIs).
   - 106 products are on blocked sites (manual); 11 were not found.
4. **Taxonomy + feature list v1.1** (`analysis/`):
   - 5 market categories (Protection, Non-Par Savings, Par, ULIP, Annuity), each mapped to a PD category, with about 25 sub-segments (`taxonomy.md`).
   - About 70 features with counts n/N, value bands, Bharti has/lacks, a coverage grid, and evidence (snippet + page) for every "yes".
   - v1.1 adds a negation guard (229 negated mentions skipped, logged).
   - Numeric fields only where label-adjacent (about 25–30% coverage).
   - `brochures_used_log.csv`.
5. **IRR calculator start** (`calc/`): `engine.py` plus `params/130N122V04.json` (Bharti Income Laabh, exact from published factors).
6. **ULIP deep-discovery brief issued to S2:**
   - `briefs/deep_discovery_ulip_brief.md`, `ulip_feature_schema.json` and `ulip_deep_set.csv` (99 ULIPs).
   - Wave 1: 78 products (SBI, HDFC, LIC, Tata, Bajaj, Axis Max, ABSLI, Canara, Bharti first).
   - Wave 2: ICICI 13 + Kotak 8, after uploads.
   - Website labels for documents; status built-in/optional/rider/not offered/not stated; timebox with a retry list.
7. **`for-your-attention/`** (00_ACTIONS, manual_uploads 119 rows, please_check, questions_for_seniors, reminders), **`analysis/selection_framework.md`**, the **QA pack** for Rahul (`qa/checker_guide.md` + `checker_workbook.xlsx`, 265 checks), and **`coordination/CHAT.md`**.

8. **Deliverables folder** (`deliverables/`, links in its README): 01 category analysis, 02 universal product list (with a Discrepancies tab), 03 light discovery workbook, 04 feature list v1, 05 ULIP feature list v2. Rebuild 02 and 03 with `scripts/build_deliverables.py`.
9. **ULIP deep wave 1, partly merged:** Bharti, SBI and HDFC (21 of 78) are in `features/ulip/`. Tata was in progress when S2 hit its usage limit. **ULIP feature list v2** (`analysis/feature_list_ulip_v2.xlsx`, built by `analysis/scripts/build_ulip_features.py`) uses deep data for 21 products and v1 brochure flags for 119. Re-run it when more deep files land; the run with all 78 is v3.

10. **ULIP pilot complete (4 Nov):** S2's wave 1 (84 ULIPs) merged; feature list v3 (deliverable 05; new features searched in all 84 policy documents, 357 matches reviewed); selection of 14 products (`analysis/ulip_selection.md`); calculator for 14 products (5 checked against insurer figures within 0.3%); comparison workbook (deliverable 06, `analysis/scripts/build_ulip_comparison.py`); 12-slide deck (deliverable 07, https://claude.ai/artifact/3VgZFusjxhJRLpqkBeXNLU). Next: show Neha, then ICICI if documents arrive, then the next category.

## 5. Key findings so far
- **ULIP market (FY26 linked life + linked pension, total premium ₹1.94 lakh cr; 19.6% of the industry book):**
  - Leaders (84.1% together): SBI 27.9%, ICICI 12.7%, HDFC 12.5%, LIC 11.8% (reference column), Tata 7.2%, Bajaj 6.2%, Axis Max 5.8%.
  - Challenger scores: ABSLI 0.88, Canara 0.77, Ageas 0.66, SUD 0.63*, IndiaFirst 0.59, PNB 0.56, Kotak 0.53* (*no documents yet). Third challenger: Ageas or Kotak is the user's call.
  - Bharti: ₹563 cr, 0.3% share, #16, +48% YoY; ULIP is 17.3% of its book.
- **Bharti white space (v1 rules):** no par whole life, ULIP pension, whole-life guaranteed income, non-Saral immediate annuity, or par pension.
  - Strongest areas: non-par savings (8 products) and return-of-mortality ULIPs (4).
  - Flexi Term Pro sits under "term with ROP option" but also offers pure term. Gaps must be read against product options.
- **Bharti trend** (PDs; FY24 PD still missing):
  - Linked share of individual NBP: 22.6% → 16.3% → 12.5% → 25.0% → **33.0%** (FY21–FY26 without FY24).
  - Par share of total premium fell from 38% to 19%. Non-par did **not** halve; it is 58% of total.
  - FY25 audited results note: **the expense-of-management (EoM) limit was exceeded and forbearance was sought.**
- **IRR**
  - Bharti Income Laabh: **about 4.2–4.3%**, pre-tax, survival, excluding GST.
  - The brochure case study (lump sum ₹3.75L) **contradicts** the policy document (Appendix V gives 410%, i.e. ₹4.10L).
  - SBI Smart Platina Supreme, HDFC Sanchay Plus (V30) and Tata Fortune Guarantee Supreme **don't publish income factors** (Tata's policy document is behind a login), so they need BIs or quotes.
  - ULIP charges and mortality tables should be public in policy documents, so ULIP is the most scalable product for the calculator.

## 6. In progress
- **S2: ULIP deep discovery, wave 1** (78 products), writing `features/ulip/<UIN>.json` and `results/deep_ulip_summary.md`.
- **The user:** manual uploads (P1 = ICICI and Kotak ULIPs, plus 2 garbled documents: ABSLI Assured Income Plus 109N127V19, Shriram Pension Plus 128L065V03), please-check items (Bajaj Guaranteed Pension Goal II 116N187V11 has no description line and was provisionally put in Annuity; 12 OCR-read description lines; 13 HDFC products possibly withdrawn), seniors' questions, Rahul's QA.

## 7. Left to do (in order)
1. Merge S2's branch after each insurer; review the Bharti output first (format check); answer S2 in `coordination/CHAT.md`.
2. Decide the 3rd ULIP challenger (Ageas vs Kotak); run wave 2 when the ICICI and Kotak documents arrive.
3. **ULIP feature list v2**, from the deep data plus new features found, and the **filled comparison matrix** (products × features, built-in/optional/rider, best-in-class highlighting, citations).
4. **ULIP calculator** (charges + mortality → fund value at 4%/8% → net yield/IRR), checked against official BIs. Then a **product comparer** front end (Excel first, a web page optional) using the comparison data. List missing parameters for industry friends.
5. **ULIP observation deck** (PPT): market context from the PDs, landscape/coverage, top and distinctive features with counts, Bharti's ULIPs vs peers, IRR/charges position, recommendations.
6. Show Neha; adjust; then repeat for Protection, Non-Par Savings, Par and Annuity.
7. **Bharti trend tab:** needs the FY24 PD and FY24–FY26 annual reports from the user.
8. QA round 2 (a ULIP tab for Rahul); fix FAILs.
9. Housekeeping: make the repos private; decide the version-mismatch updates in the master list.

## 8. Known data limits
- Market share is based on **total premium** (FY+renewal+single); NBP by segment isn't disclosed per insurer.
- Feature "Y" in v1 = **described** in the brochure, not split into built-in/rider (the deep pass fixes this). Numeric eligibility values are only partial.
- 30 documents carry a different UIN version from the master list (kept as found). 2 documents are garbled. 12 description lines were read by OCR.
- Blocked insurers (ICICI, Kotak, SUD, Go Digit) are not yet in the feature data.

## 9. How to resume (new session or after compaction)
1. Attach/clone `ahen-can/li-product-docs` (main) and, if needed, `ahen-can/boom`.
2. Read this file, then `coordination/CHAT.md` (top entries), then `for-your-attention/00_ACTIONS.md`.
3. Fetch S2's branch: `git fetch origin ccr-d0d84e00-joo2mp`, then merge it into main if there are new commits.
4. Continue at section 7, first open item.
