# Coordination channel: S1 (main session) · S2 (second session) · USER

**How to use this file**
- **Newest entries at the top.** Never edit or delete old entries.
- **Before starting any work:** pull or fetch and read the top entries.
- **After each step:** add an entry.
- **Entry format:**
  `### <date time IST> · <S1|S2|USER> · <topic>` then **Status**, **Done**, **Asks / blockers**, **Answers to earlier asks**.
- **Where it lives:** S1 writes on `main`. S2 writes on its own branch (S1 merges S2's branch into main regularly, so both see one history). If an entry needs action from the other session, start it with `@S1` or `@S2`.
- **Decisions belong to the USER.** If a session needs one, write `@USER` and also tell the user in chat.

---

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
