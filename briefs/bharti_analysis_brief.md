# Brief for S3: Bharti Life trend and portfolio analysis

You are S3, a Claude Code session on the user's laptop. S1 (main session) and S2 (deep discovery) work in this same repo. Read this file in full, then `PROJECT_MEMORY.md` (project state and rules) and the top of `coordination/CHAT.md`. Follow `CLAUDE.md` for writing style and honesty.

## Goal
Build the Bharti Life analysis for the category workbook (deliverable 01): how Bharti's business has changed over the last 5 years (FY21 to FY26, plus FY27 year to date where published), by category and by product, and how it compares with peers. The user's lead (Neha) will read it, so every number needs a source document and page.

## Your inputs
1. **The user's folder** `~/Desktop/for-liprodanal-agent` (the user will confirm the path). It holds documents the user downloaded from Bharti's website: public disclosures (PDs, quarterly and annual), annual reports for the last 5 years, KPI disclosures and others. Decide which to use. Do not assume a file is what its name says; open it and check the period and the form number.
2. **This repo:**
   - `sources/bharti-kpi/` holds the Product Performance file (FY24 to H2 FY27) and the Returns & Premium file, which S1 already downloaded from bhartiaxa.com/kpi-disclosures.
   - `deliverables/01_life_insurance_category_analysis_Q4FY26.xlsx` has the FY26 category data for all 25 insurers. Its "Bharti portfolio" tab has product-level NBP. Use it for peer comparison; do not rebuild it.
   - Phase-1 data for all insurers (FY26 and FY25, Rs lakh) is in the `ahen-can/boom` repo at `li-category-analysis/scripts/data.json`, branch `ccr-b8ad4f03-rfkxka`. Read it only if you need peer numbers beyond the workbook.
   - `analysis/product_features_v1.csv` maps each Bharti product (UIN) to its market category.

## What to produce
Work on a new branch `s3-bharti-analysis` in this repo, in a folder `analysis/bharti/`:

1. **`document_inventory.csv`**: one row per document you looked at, with these columns: file name, document type (PD form, annual report, KPI disclosure, other), period, pages, used (Y/N), why not used, notes (e.g. scanned, OCR used). Do not commit the PDFs themselves. They are in the user's folder, and annual reports are large.
2. **`bharti_trend_data.csv`**: one row per number, with these columns: metric, segment or product, period, value, unit, source file, form or section, page, note. This is the evidence base, so every number in the Excel and the findings must appear here.
3. **`bharti_analysis.xlsx`**: tabs that S1 will copy into deliverable 01. Use plain tables with clear headers, and give units in each header.
   - **Bharti trend**, FY21 to FY26:
     - total premium by segment (par, non-par, linked, pension, annuity, health, group) and its mix;
     - new business premium by segment and its mix;
     - individual vs group;
     - single vs regular premium;
     - growth rates.
   - **Bharti KPIs**, FY21 to FY26, whatever the PDs and annual reports give:
     - persistency (13th, 25th, 37th, 49th, 61st month);
     - conservation ratio;
     - commission ratio;
     - expense of management against the regulatory limit (Bharti exceeded it in FY25 and sought forbearance);
     - claims settlement ratio;
     - solvency ratio;
     - AUM;
     - channel mix (agency, bancassurance, brokers, direct, online);
     - number of policies;
     - average ticket size;
     - VNB and VNB margin, and embedded value, if disclosed.
   - **Bharti product trend.** Every product in the Product Performance files across all periods: NBP, new policies, renewal premium, renewal proportion and exit proportion, with its market category. Note launches and withdrawals, and which products enter or leave the 90% list.
   - **Peer view FY26.** Bharti against the peer set on the measures available for all insurers in the FY26 PDs: segment mix, growth, persistency and conservation. Peer set: SBI, HDFC, ICICI, Axis Max, Tata AIA, Bajaj, ABSLI, Canara HSBC, Ageas Federal, plus Bharti's size peers Shriram, Generali Central, Pramerica and IndusInd Nippon. Use the same PD forms for every insurer. If you do not have a peer's PD, leave it blank and say so.
   - **Sources.** The inventory, as a tab.
4. **`findings.md`**: 10 to 15 observations, each one or two sentences with the numbers and the source page. Then a short "questions this raises" list. Use the user's earlier hypotheses as a starting point and test them:
   - ULIP grew from about 10% to 17-19% of the book;
   - non-par halved.
   S1's reading of the PDs so far is in `PROJECT_MEMORY.md` section 5: linked share of individual NBP went 22.6%, 16.3%, 12.5%, 25.0%, 33.0% (FY21 to FY26 without FY24); par fell from 38% to 19% of total premium; non-par did not halve. Confirm or correct this, and fill FY24.

## Which numbers to trust
- **For segment premium, use the PD forms:** L-1-A-RA, the revenue account, "(a) Premium" by segment. For NBP mix, use L-22 analytical ratios or the new business forms. Quote the form number in the `form or section` column.
- **For KPIs, use the PD form that reports each one.** Persistency and conservation are usually in L-22, claims in L-39 or the annual report, solvency in L-32, and channels in the business-acquisition form. Check the form titles in the files you have; numbering changed in some years.
- **The annual reports are for what the PDs do not have:** VNB, embedded value, management commentary on strategy and products, and regulatory issues (EoM limit, forbearance). Quote them with page numbers.
- **Where two documents disagree, record both and flag the difference.** Do not choose silently.
- **Units.** PDs report in Rs '000 or Rs lakh; check each form's header. Convert to Rs crore in the Excel and keep the original value and unit in the CSV.

## Rules
- Use only the user's documents and the official Bharti, IRDAI and Life Insurance Council websites. No news sites or aggregators.
- Raise doubts with the user, and record them as below:
  - **Scanned, garbled or unclear pages.** OCR them if needed, mark the number as OCR-read, and add the item to `for-your-attention/please_check.md` under a heading "Bharti analysis (S3)".
  - **A missing year or form.** Say so in the inventory and in `findings.md`. Do not estimate it.
- Work in this order, and commit and push after each step:
  1. inventory;
  2. trend data;
  3. Excel;
  4. findings.
  After each push, add a short entry to the top of `coordination/CHAT.md` (author S3, 3 to 5 lines).
- If one document or year takes too long, park it on a retry list in `findings.md`, move on, and come back at the end.
- Keep messages to the user short: what you finished, and any question. The detail goes in the files.
- Commit messages end with the attribution lines your session gives you. Do not open a pull request. S1 merges your branch.

## When you are done
Post a CHAT entry for `@S1` with the branch name and the file list. S1 will:
- copy the tabs into deliverable 01 next to the "Bharti portfolio" tab;
- replace the estimated NBP values there with real ones where your data has them;
- update `PROJECT_MEMORY.md`.
