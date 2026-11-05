# Brief for S3: QA of ULIP feature list v3, Bharti first

## Why
S2's audit of the deck found that several "Bharti has / lacks" claims were wrong. The causes:
- **Rider features.** Waiver of premium may come through Bharti's Complete Shield rider.
- **Channel-specific terms.** Wealth Pro and Grow Wealth have online terms.
- **Counts off by one.** 6 of 7 Bharti ULIPs allow unlimited free switches, not 7.
- **"Not stated" read as "not offered".** Top-ups are not mentioned, which does not mean they are not allowed.

These errors live in feature list v3 (`analysis/feature_list_ulip_v3.xlsx`, deliverable 05), and the deck and comparison inherit them. Bharti is the anchor, so every Bharti cell must be right before we check peers.

## What to check
Workbook: `qa/s3_v3/v3_qa_workbook.xlsx`. The script that made it is `qa/s3_v3/build_v3_qa_workbook.py`. Fill the yellow columns: the correct value or status, PASS / FAIL / UNSURE, and a comment with document, page and quote.

| Tab | Rows | What |
|---|---|---|
| A_Bharti_claims | 103 | One row per feature in v3. Is the "Bharti" claim right across all 7 Bharti ULIPs? |
| B_Bharti_cells | 721 | Every v3 cell for the 7 Bharti ULIPs (103 features x 7), with the evidence we hold |
| C_Bharti_riders | 2+ | What each Bharti rider covers |

**Order.**
1. **Tab C first.** Download the rider brochures and policy documents for the Linked Complete Shield Rider (130A012V02), the Cover Plus Linked Term Rider (130A034V01) and any other rider a Bharti ULIP names. Get them from bhartiaxa.com, put them in `manual-uploads/bharti-life/`, and add a `sources.csv` row for each, as for ICICI.
2. **Then tab A.** A row-level error tells you which cells in B to look at.
3. **Then tab B.** Start with blank and "?" cells, then "N", then the rest.

Read the PDFs themselves (`docs/bharti-life/<UIN>/`), not the text extracts: tables lose their layout in text.

## Error patterns to look for
1. **Riders.** A feature delivered only through a rider (waiver of premium, critical illness, accidental death, disability) must be coded R, not N or blank.
2. **Not stated vs not offered.** Mark N only if the document says the feature is not available. Silence is "?".
3. **Counts.** "All 7" claims and "has it" lists must match product by product. Future Invest's 12 free switches a year is not "unlimited".
4. **Channel and customer terms.** Online, staff, women, existing customers and ECS can each change charges or add boosters.
5. **v1 keyword rows.** Some rows (group "v1 feature" with source "brochure only") only show that a word appears in the brochure. Say whether the product really has the feature.
6. **Overlapping definitions.** Example: Wealth Pro's year-5 and maturity boosters. Are they "scheduled guaranteed additions" or "wealth boosters"? Note the rule you used.

## Rules
- Do not edit feature list v3 or the deep JSON files. Record what you find; S1 fixes the data and rebuilds.
- If you find a pattern that probably affects peers too, write it in your CHAT entry. After Bharti, S1 will build a peer sample for those patterns.
- Work on your branch `s3-bharti-analysis`, commit the filled workbook as `qa/s3_v3/v3_qa_workbook.xlsx`, and push.
- Post a short CHAT entry for `@S1`: pass rate per tab, the list of FAILs (feature, product, correct value), and the error patterns you saw.
