# S2 project memory: read this first if you are S2

Last updated: 5 Nov 2026 (wave 1 done; walkthrough page and restyled deck for Neha drafted) by S2.

## Role and branch
- S2 is the user's second Claude session. It works on branch `ccr-d0d84e00-joo2mp` and never pushes to `main`. S1 merges the branch into `main`.
- Before work, run `git fetch origin main` and merge it into the branch. Then read the top of `coordination/CHAT.md`. If CHAT.md conflicts, keep every entry from both sides, newest first.
- Force push is blocked. Merge instead of rewriting pushed history.
- End commits with:
  ```
  Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
  Claude-Session: https://claude.ai/code/session_01CUAfyogotnTRvsfH5LoNgf
  ```
- Push once per insurer. Write one short CHAT entry per insurer. Keep replies to the user to 2 or 3 lines, and put the detail in `results/deep_ulip_summary.md` (S1 ask, 4 Nov).
- Follow the unslop writing rules in `CLAUDE.md` for everything written.

## Task
- The brief is `briefs/deep_discovery_ulip_brief.md`. The product list is `briefs/ulip_deep_set.csv` and the schema is `briefs/ulip_feature_schema.json`.
- Wave 1 is 84 products, after the user added Ageas Federal on 4 Nov.
- **Done: 60.** Bharti 7, SBI 7, HDFC 7, Tata AIA 14, Bajaj 11, Axis Max 9, LIC 5. All pass validation.
  - LIC is committed locally; if the last session ended before the push, push it with `scripts/s2_tools/pushit.sh` (check `git log origin/ccr-d0d84e00-joo2mp`).
  - Smart Wealth Goal VII (116L218V01, Bajaj) has three variants; only the Wealth variant is field by field.
- **ABSLI in progress (1 of 10 specs done; documents all collected).** Spec done: 109L073V05 Wealth Max. Left: 109L143V01 Fortune Wealth Plan, 109L149V01 Param Suraksha, 109L142V01 Platinum Gain Plan, 109L145V01 Salaried Suraksha, 109L157V01 Smart Wealth Pension Plan, 109L100V06 Wealth Aspire Plan, 109L129V03 Wealth Infinia, 109L074V05 Wealth Secure Plan, 109L147V02 Wealth Smart Plus.
  - Documents: brochure ("Prospectus"), "Policy Contract" and "CIS" per product. Fortune Wealth Plan and Salaried Suraksha link no CIS (record as not published). The Wealth Aspire policy document prints no product code and starts at Part E; it was stored with `addoc.py ... "-"` and a note.
  - The brochures are short (11 to 28 pages) and hold the charges, funds and Schedule A. `scripts/ulip_specs/absli_common.py` has the segregated-fund identification numbers and a `funds()` helper. The mortality tables are in each policy's Part E (policy page numbers vary; the brochures give sample ages).
  - When done: summary row, spot checks, oddities, new features, data_not_public; commit "Deep ULIP: ABSLI (10 products, ... policy docs, 0 BIs)"; push; CHAT entry.
- **Then, in this order:** Canara HSBC (8), Ageas Federal (6).
- Wave 2 (ICICI, Kotak) waits for the user's manual uploads.

## User decisions (4 Nov)
- **Quote rule.** S1 asked that every quote contain the value itself; a label such as "Minimum Entry Age:" alone is not evidence. If the value is in a table, quote the table row.
  - Apply the rule from Bajaj onwards.
  - Redo the older quotes at the end of wave 1.
- **Extra quotes.** A table too long for one 300-character quote uses `quote_2` to `quote_4` (with `page_2` to `page_4`) in `F(...)`. The validator checks all of them.
- **Exception, before Bajaj (done 4 Nov).** Redo now only the charge, eligibility and addition fields for the six products S1's calculator uses:
  - 130L100V03, 130L123V01, 130L121V01, 111L147V01, 101L133V03, 101L180V01.
  - Charge tables become nested numbers read from the layout text.
  - The mortality charge note gives the page range of the rate table in the policy document.
- **Other S1 asks.**
  - Redo Bharti Grow Wealth Ultra's (130L128V01) admin charge as a table on the second pass.
  - The SBI second-pass fields are done.
- **Tata i Systematic (110L164V11).** The user will supply the V11 documents. Until then, its JSON uses the V04 brochure, with every value flagged.

## How a product gets done
1. **Collect.** Run `python3 -I scripts/deep_collect.py --insurer <slug> --dry-run` to see the links per product page, then run it without `--dry-run`.
   - Use `--extra-page URL` for central document pages; HDFC needs its `/policy-documents` and `/brochures` pages.
   - The collector checks `%PDF`, `pdfinfo`, the 95 MB limit and the UIN, and OCRs image PDFs.
   - It writes `results/deep_ulip_docs.csv`, `index.csv` (with a `website_label` column), `docs/` and `text/`.
   - It skips page assets (css, js, images).
   - It skips fund factsheets that don't name the product.
2. **Read.**
   - Tools are in `scripts/s2_tools/`:
     - `kw.py UIN` prints key passages and the brochure eligibility page.
     - `tdig.py UIN [areas]` is a Tata-style digest by clause.
     - `rd.sh PDF a b` prints compact pages.
     - `tata.sh` prints the text between two headings.
     - `rowq.py PDF PAGE REGEX N` joins N layout lines into one quote string for a table row.
     - `bajaj_one.sh UIN` prints a Bajaj brochure's key pages plus policy facts (strategies, withdrawal limits, mortality-table page); `bpages.sh`, `bbro.sh` and `bdig.py` are older Bajaj helpers.
   - Dashes and hyphens at line ends vanish in the validator's matching, so leave them out of quotes ("Year 2 5.0%", not "Year 2 - 5.0%").
   - `scripts/ulip_digest.py` is a general reading aid.
   - Read charge tables with `pdftotext -layout`. Take quotes from the plain reading-order text.
3. **Spec.** Write `scripts/ulip_specs/<UIN>.py` with `F(value, status, doc_label, page, quote, note)` and `NS()` from `scripts/ulip_json.py`.
   - Shared helpers: `bharti_common.py`, `sbi_common.py`, `hdfc_common.py`, `tata_common.py` (Tata fund codes and FMCs) and `bajaj_common.py` (Bajaj fund FMCs; SFINs left out because they are split across lines).
   - `doc` is the website label. Unlabelled links are cited by file name.
   - The page is found automatically from the quote.
   - Twin products can be copied from a sibling spec with string replacements; check every replacement hit.
4. **Check.**
   - `python3 -I scripts/validate_ulip_json.py <UIN>` checks that every quote is verbatim on its page.
   - `python3 -I scripts/check_consistency.py` must report 0 problems.
   - Delete `scripts/__pycache__` before committing.
5. **Summary.** Add the insurer's row, two spot checks, odd findings, new features, `data_not_public` and gaps to `results/deep_ulip_summary.md`.
6. **Commit.** Use `git add docs/<slug> text/<slug> index.csv features/ulip results/deep_ulip_docs.csv results/deep_ulip_summary.md scripts`. The message is "Deep ULIP: <insurer> (<n> products, <m> policy docs, <k> BIs)". Push with `scripts/s2_tools/pushit.sh`, which retries and confirms against the remote.

## Bajaj notes
- **Labels.** Product pages label both the policy document and the CIS "Download". `doc='Download'` resolves to the policy document (first in the inventory), so cite the CIS only if unavoidable. Brochures are unlabelled and are cited by file name (for example `gain-brochure.pdf`).
- **Where values sit.** Eligibility, charges, FMC and discontinuance tables are in the brochure ("Eligibility Table" / "Product at a Glance" and "Charges under the Plan"). Strategies, withdrawal limits, revival and the mortality table (an Annexure near the end) are in the policy document.
- **Data not public.** Fortune Gain II's policy refers to Annexure 3 for mortality rates, but it is not attached; the brochure gives only sample rates. Its admin charge is "mentioned in the Schedule", but the specimen schedule doesn't print it.
- **Extra documents.** Supreme (116L211V02) and Smart Pension (116L209V08) policy documents were not linked on the product page. They were found at `.../ulip/supreme-policy-doc.pdf` and `.../retirement-plans/smart-pension-policy-doc.pdf` (real PDFs, noted in index.csv). Smart Pension's document prints 116L209V03 and the old Bajaj Allianz name, not V08: flag every value.
- **Removed.** The sitewide "individual-factsheet.pdf" was wrongly stored for GAIN, because "gain" is a common word. It was deleted, and its inventory row is now "skipped".
- **Oddities so far.** Fortune Gain II's specimen schedule prints 116L196V04. GAIN's PPT table prints 75 under "Maximum PPT", which reads as an age. Goal Assure IV's maximum-SA table has 5 age columns but 4 values per row.
- **Features seen.** Family Benefit (0.5% or 1% of fund for relatives of customers), Return Enhancer (settlement instalments +0.5%), Trigger Based strategy (moves gains to Liquid Fund after a 15% equity rise), ROMC up to 125% by premium band, first-year additional allocation of 3%.

## Working notes (4 Nov, after Bajaj)
- The user switched S2 to Sonnet to stretch the usage limit. Commit trailer: "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>" plus the Claude-Session line.
- `scripts/ulip_json.py` tags later stored files that share a website label with "(file name)" (Bajaj labels every document "Download"). The first keeps the bare label.
- Read only the pages that hold eligibility, charges, benefits and flexibility. Page maps first (grep for headings per page), then targeted pages.
- Quotes: take layout rows for tables; plain text when columns scramble. Drop a hyphen at the end of a line, such as "/-" or "sub-". Extra quotes use the same document as the field, so put values from a second document in another field.

## Axis Max notes
- Tools: `scripts/s2_tools/axdig.py UIN` (compact glance, charges and flexibility sections), `scripts/s2_tools/addoc.py` (stores one PDF by exact URL, checks it and writes the index rows; used for links in page source and for a document that carries another product's UIN), `scripts/ulip_specs/axis_funds.py` (parses the fund and FMC table; falls back to a joined-text parse and a SFIN-to-name map).
- Labels: policy "Policy Contract", brochure "Policy Prospectus" or "Prospectus", CIS "Customer Information Sheet". The "Terms and Conditions" link is a company-wide leaflet and fails the UIN check.
- Policy documents are specimens with blank schedules; the charge tables are in the prospectus. Most policy documents print the attained-age mortality table (see the summary for pages).
- In a quote, drop the hyphen of "/-" only when it ends a line; keep it when more text follows on the same line.

## LIC notes
- Tool: `scripts/s2_tools/licdig.py UIN` prints the eligibility-to-funds and charges sections (its section ends are rough; read the page directly if a section is cut).
- Each product links two dated brochures; the latest (from 22/09/2025) is `brochure.pdf`, the older is `brochure-2.pdf`. Labels are the website labels, which differ in capitals ("Sales brochure" and "Sales Brochures").
- Quotes from two-column tables: take the rowq line, keep hyphens that sit inside the row, drop the one at the end of a line.

## Walkthrough for Neha (5 Nov, latest work)
- **Goal (user's words).** Show Neha HOW we are working and ask whether the approach makes sense. Not a fleshed-out analysis. Bharti's product suite is the focus. Observations only, no recommendations.
- **Page.** https://claude.ai/artifact/VeBN1cragc4K9rPSVGNPrN (owner's private artifact; the user shares it). Source: `docs-internal/s2_neha_walkthrough/ulip_pilot_walkthrough.html`. Republish from this session with the same file path, or from another session with `url`.
  - Structure: 2-minute flow of 9 steps (each says what we did), then 13 sections: market landscape (4 PD categories), Bharti product mix and trend (Bharti portfolio tab of deliverable 01 + S3 findings, EoM breach), product list (sources: Council 511, official lists 64, websites 58), brochures and v1, who to compare (framework), policy documents and v3 (Bharti has / lacks boxes), calculator, shortlist 84 to 14 to 5, deck head-to-head, quality checks, limits, things to do, 6 questions with A-D options and a "Copy my answers" button.
  - Excel samples are spreadsheet-style HTML previews with links to the files on GitHub, not screenshots.
  - QA figures come from the user verbally (not pushed yet): Shobhit checked 100 products (4 UIN version differences, 1 withdrawn) and 100 brochures (4 UIN version differences, 5 policy documents or leaflets instead of brochures, none for the wrong product). S3: 255 checks, 237 pass, 8 fail, 10 unsure.
  - User's edits applied: no "for Neha", no bullet dots, par (not non-par) as the hypothesis, no "299 discrepancies", no "checked by hand across all 84", ICICI = "I'll analyse its ULIPs myself against the feature list", Q2 explains the framework with the ULIP numbers.
- **Deck.** https://claude.ai/artifact/K47aHoxEmo3J5AUtJ8hMWp, a restyled copy of S1's deck (https://claude.ai/artifact/3VgZFusjxhJRLpqkBeXNLU, which this session cannot edit). Same 12 slides and content; Public Sans, ink and blue palette, orange for gaps, source line and page number on each slide. Slide 11 retitled "Observations: five areas the comparison points to". Source: `docs-internal/s2_neha_walkthrough/deck/project/`. Update with the Artifact tool, `url` the deck, `root` a folder holding `project/`.
- **Facts checked in the repo** (the user's memory differed): 633 products; 516 documents found (499 brochures, 17 policy documents or leaflets); 106 products on blocked sites (ICICI, Kotak, Star Union Dai-ichi, Go Digit); 168 ULIPs on the list, 141 with brochures; all ULIPs of the 10 chosen insurers = 84. The Linked tab of deliverable 01 is linked life only (Rs 1.77 lakh cr); the deck's Rs 1.94 lakh cr includes linked pension.
- **Open with the user.** Possibly save the page into deliverables; S3's Bharti workbook still on branch `s3-bharti-analysis` (links point there).

## Session state (4 Nov, latest)
- All 84 wave 1 ULIP JSON files are built, validate, and are pushed per insurer with summary rows and CHAT entries (Canara HSBC and Ageas Federal done). `check_consistency.py` reports 0 problems.
- Ageas Federal quirk: product pages keep their documents in a `planWiseDoc` list in the page data. `scripts/deep_collect.py` has an `ageas_docs()` reader for it. Shared helpers: `scripts/ulip_specs/ageas_common.py` (SFINs as printed, `mortality()` table parser, fund dicts).
- Cross-check tool: `python3 -I scripts/s2_tools/valuecheck.py [UIN]` flags fields whose value numbers are not in the quote text. About 760 flags remain; most in Tata, HDFC, SBI and Bharti are the old label-only quotes. Some flags are fine (derived values, word numerals).
- Wave 1 is done and the report is `results/deep_ulip_wave1_report.md`. What is left: (1) the 89 short-value fields whose quotes lack the number (list them with `python3 -I scripts/s2_tools/fixquotes.py suggest <UIN prefixes>`, accept good suggestions, apply with `fixquotes.py apply`), (2) Tata i Systematic V11 is done (user uploads stored under uploads/tata-aia/), (3) wait for the user's next brief.
- Sonnet trailer: "Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>" plus the Claude-Session line.

## Lessons
- **Two-column PDFs (Tata).** Quotes often survive only in short pieces. When a quote fails, grep the plain text for the exact wording; Tata twins differ in small words ("Saving" or "Savings", "Rs." or "INR").
- **Ligatures and hyphens.** Some PDFs drop the "ti" and "fi" ligatures or hyphenate at line ends. The validator allows for both.
- **Image-only brochures.** OCR them. If no UIN is found, don't store the file; record it as failed with a note.
- **Process kills.** Never use `pkill -f` with a pattern that also appears in the shell command.
- **OCR stalls.** Run tesseract with a 120-second timeout and `OMP_THREAD_LIMIT=1`.
- **Field edits.** When editing many fields with a script, replace exact strings. A bracket-counting edit broke a spec once.
- **Session restarts.** The worker can restart mid-task. Commit locally often, but push only finished insurers.

## Open items and retry list
- **Tata i Systematic V11.** Waiting for the user's upload.
- **Tata SSR Pro (110L172V03).** Eligibility is not stated, because its only brochure is image-only without a UIN.
- **Tata Smart Pension Secure (110L182V09).** Fund names are not mapped to their codes.
- **Old quotes.** Redo the label-only quotes in the 35 files at the end of wave 1. A rough scan flags about 360 fields with numbers in the value but none in the quote, and some of those are fine ("three years").
- **No BIs.** None of the four insurers done so far publishes BIs or product-specific fund factsheets.

## S2 self-QA of the walkthrough page and deck (5 Nov)

Workbook: `qa/s2/s2_qa_workbook.xlsx`, built by `scripts/s2_tools/build_qa_workbook.py` (edit ROWS, rerun). 84 claims traced to the deliverables, policy-document JSONs and S3's notes: 57 pass, 12 fail, 9 warn, 3 unverified, 3 supplied verbally by the user.
- Fixed on the page (08): preview row numbers (Bharti portfolio, v1, v3), "All 7 free switches" is 6 of 7 (Future Invest has 12 a year), expert nomination not yet applied to the challenger scores.
- Open on the deck (S1's content, not changed): "mostly as a rider" (waiver is mostly an option), Bharti "5 products" for loyalty or boosters (6), Grow Wealth Ultra 1.31% not in deliverable 06, "Bharti x3 checked" (06 shows 2 Bharti checks), SBI Retire Smart Plus has no assured vesting, "most policies in force" claim on slide 11 note, S3 QA counts (237/8/10 vs 233/7/9 now).
- Still unverified: calculator steps on the page, FY25 conservation 75.4%, page reading time.
