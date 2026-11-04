# Checker guide (for Rahul): sanity-checking the product data

**Goal:** independently confirm that what the two Claude sessions collected and computed is correct, before it goes into Excel files and decks. You fill the yellow columns in `qa/checker_workbook.xlsx` (PASS / FAIL / UNSURE, plus a comment). The Summary tab computes pass rates. **Target: ≥95% PASS per tab.** Every FAIL gets fixed and re-checked.

**Time needed:** about 6–8 hours in total, and the tabs can be split across days.

## What you need
- Access to the GitHub repo `ahen-can/li-product-docs`. Ask for a collaborator invite. Every stored PDF is under `docs/<insurer>/<UIN>/…`, and `index.csv` gives each file's original URL on the insurer's site.
- The public-disclosure (PD) zip files for FY26 Q4 (for tab F).
- A normal browser. Some insurer sites (ICICI, Kotak, Star Union Dai-ichi, Go Digit) block automated access but open fine for people.

## Ground truth: what counts as "correct"
| Question | Ground truth, in this order |
|---|---|
| Is a product current, and is its UIN right? | 1) The insurer's own official list where one exists: **Bajaj** on-sale-plans page, **Tata AIA** active & withdrawn status page, **Bharti** and **ICICI** lists supplied by the client (`sources/official-lists/`). 2) The insurer's product / all-plans page (link in tab A). 3) The Life Insurance Council in-force list, Sep 2026 (`sources/life-council/`). |
| Is the document right? | The PDF itself: product name, UIN printed (usually on page 1 or the last page), and the IRDAI description line on page 1. |
| Category and sub-segment | The description line plus the rules in `analysis/taxonomy.md`. |
| Feature present or absent | The brochure (or policy document) text. A feature that is only a **rider** should be noted in the comment. |
| Premium numbers (phase 1) | The PD PDF, Form L-1-A-RA, year-end revenue account, "(a) Premium" row. |

**Insurers with no single product-list page** (the sessions used site menus and sitemaps instead): SBI Life, PNB MetLife, Shriram Life, Pramerica Life. For these, use the site menus.

## The checks (quantified)
| Tab | What | How many | What PASS means |
|---|---|---|---|
| **A. List vs truth** | Random products, up to 5 per insurer, 21 insurers | 97 | Listed as current on the ground truth, with the same UIN (a version difference goes in the comment) |
| **B. Document match** | The same 97 products | 97 | The stored PDF opens, it is the right product, the UIN matches (note the version), the description line matches ours, and it is a brochure (not a leaflet, CIS or rider document) |
| **C. Classification** | 3 per category × 5 categories | 15 | The category and sub-segment fit the description line and brochure |
| **D. Feature flags** | 20 random "yes" and 10 random "no" | 30 | For "yes": the evidence is on that page and it really is a product feature. For "no": you can't find it in the brochure. |
| **E. Numeric values** | Random ages / minimum premium / FMC values | 15 | The value matches the brochure |
| **F. PD numbers** | Random insurer × segment premium values | 10 | The PD shows the same value. Individual and group columns may need adding together; LIC reports in ₹ crore, which we multiply by 100. |
| **G. IRR** | Bharti Income Laabh, one profile | 1 | Your own Excel IRR on the cash flows from the documents matches 4.20%. Also say whether the brochure case study (₹3.75L lump sum) or the policy document (₹4.10L) is right. |

## How to record
- **PASS / FAIL / UNSURE** in the yellow column.
- **Comment:** always add one for FAIL or UNSURE. Say what you saw and where (page, URL).
- If you find something wrong outside your sample, add it at the bottom of the relevant tab with "found ad hoc".

## Round 2 (after ULIP deep discovery)
We'll add a ULIP tab: 10 products × 10 fields (charges, loyalty additions, fund count, eligibility), each with a page reference to check against the policy document.
