# Brief for S2: QA of the Bharti section, and what to add (product focus)

## Why
The Bharti section of Neha's page (deliverable 08, section 2 "Bharti: product mix and trend") and the Bharti slide in the decks (07 and 09, slide "bharti") come from two sources:
- S1's Bharti portfolio tab in deliverable 01, built from Bharti's Product Performance disclosure and reconciled to the public disclosures;
- S3's trend analysis (`analysis/bharti/`).

S3 worked on the user's laptop, without the ULIP pilot's later findings, and S1 copied its headlines into the page. The page goes to Neha now, so every number must be right, and the section should be about Bharti's products, not its company finances.

## Part 1: QA, number by number
Check each claim below against its source. Record the result in `qa/s2/bharti_section_qa.csv` with these columns: id, claim, where it appears, source used (document and page), PASS / FAIL / UNSURE, correct value, comment with quote.

| id | Claim (page 08 section 2, and the deck's Bharti slide) |
|---|---|
| B1 | 25 Bharti products placed in a category (the master list has 26 Bharti rows: explain the difference) |
| B2 | The category table: ULIP 7 products, Rs 212 cr, 23%; Non-Par Savings 8, Rs 211 cr, 22%; Par 5, Rs 44 cr, 5%; Annuity 2, Rs 38 cr, 4%; Protection 3, Rs 0, 0%; not disclosed by product Rs 433 cr, 46%; total individual NBP Rs 937 cr |
| B3 | Largest disclosed product per category: Wealth Pro, Guaranteed Wealth Pro, Unnati, Swabhimaan Retirement Plan; Protection "none disclosed" |
| B4 | 8 products are 54% of FY26 individual new business |
| B5 | Four of the 8 launched in FY25 or FY26 |
| B6 | Guaranteed Wealth Pro fell from Rs 165 cr to Rs 113 cr in two years |
| B7 | ULIP is a third of new business, up from 13% in FY23 (S3's own note says the FY24 linked share is 17.9%; check FY23) |
| B8 | Wealth Pro Rs 82 cr; Growth Shield Plus Rs 80 cr, up 48% in its second year |
| B9 | No protection product is in the disclosed list |
| B10 | Hypotheses: ULIP grew from about 10% to 17% of the book; par fell from 38% to 19% of premium. The user has reworded this line in their own copy: check the numbers only, do not edit the wording |
| B11 | New policies fell 41% since FY21 while ticket size doubled |
| B12 | Agency fell from 45% to 14% of new business, and Direct rose to 45% |
| B13 | 13th-month persistency 64.5%, second lowest of the 14 insurers compared |
| B14 | Expense limit breached every year FY21 to FY25; IRDAI show-cause notice for FY25; expenses 34% of premium, mostly operating costs, against a proposed 15% limit |
| B15 | Deck Bharti slide: 33% of FY26 individual NBP is ULIP (about Rs 309 cr of Rs 937 cr); Wealth Pro 81.6 / 79.1; Growth Shield Plus 79.6 / 53.8; Dream Shield Plus 50.9 (launched); 4 others Rs 97.2 cr; linked premium grew 48% to Rs 563 cr; linked new business grew 90% |
| B16 | Consistency with the rest of the pilot: product names, UINs and counts match `master_list.csv`, feature list v5 and the comparison (for example "5 of 7 ULIPs return mortality charges") |

**Sources.**
- Bharti's KPI files are in `sources/bharti-kpi/` (Product Performance, monthly report, Returns and Premium).
- S3's numbers and page references are in `analysis/bharti/bharti_trend_data.csv` and `bharti_analysis.xlsx`; the method is in `analysis/bharti/document_inventory.csv`.
- The public disclosures (PD forms L-1, L-4, L-22, L-37, L-38 and others) and annual reports are on S3's laptop, not in the repo. Bharti publishes them on bhartiaxa.com (public disclosures). Download the ones you need under the usual rules (insurer site only, 1 request a second) into `sources/bharti-pd/` with a `sources.csv` row each, and cite the page.
- Where a claim depends on a document you cannot get, mark it UNSURE and say what is missing.

## Part 2: what to add, product focus
Propose up to 5 additions that tell Neha more about Bharti's **products**: what it sells, what sells, and how each product line is doing. Company finances (expenses, solvency, channels) stay as a short footnote at most. For each proposal give the source, the number, and a one-sentence reason it helps. Ideas to test, all from official sources:
- Product-level trend FY24 to H1 FY27 from the Product Performance file: new business, renewal proportion and exits per product. Which products grow, which fade, which lose customers.
- Launch and withdrawal history: what Bharti added or withdrew in the last 3 years (its withdrawn-products page, master list).
- Bharti's products against the market's sub-segments: where it has nothing (pension or child ULIP, immediate annuity beyond Saral, term with return of premium), using `analysis/taxonomy.md` and feature list v1.
- ULIP fund performance from the Returns and Premium file: one line on how Bharti's main funds performed, labelled as Bharti's own disclosure.
- Persistency or exits by product, if the Product Performance file supports it, to back up or replace the company-level persistency line.

## Rules
- Do not edit the page, the decks or deliverable 01. Record findings; S1 fixes and republishes.
- Insurer and regulator sites only. Never categorise a product from its name; use the IRDAI description line or the master list.
- Push on your branch and post a short CHAT entry for `@S1`: pass rate, the FAILs with correct values, and your proposed additions ranked by usefulness.
