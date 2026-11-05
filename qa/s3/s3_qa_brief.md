# Brief for S3: QA round on ULIP and Bharti outputs

You are S3, now acting as an independent checker. S1 built most of what you check, and S2 built the deep-discovery data. Your job is to confirm the outputs against the source documents, not to redo them. Read `PROJECT_MEMORY.md` and `CLAUDE.md` first.

## What to check
Workbook: `qa/s3/s3_qa_workbook.xlsx` (255 rows, random samples with a fixed seed; the script that made them is `qa/s3/build_s3_workbook.py`). Fill the yellow columns: PASS, FAIL or UNSURE, and a comment with what you saw and the page.

| Tab | Rows | What | Ground truth |
|---|---|---|---|
| A_deep_fields | 90 | S2's deep-discovery values and statuses, 15 ULIPs x 6 fields | The policy document or brochure PDF in `docs/<insurer>/<UIN>/` at the cited page |
| B_new_feature_calls | 100 | S1's calls on new features: all 70 rejections and 30 random acceptances | The PDF; feature definitions in `analysis/feature_list_ulip_v2.xlsx`, tab Features |
| C_calculator_inputs | 30 | The ULIP calculator's inputs for 6 products | The policy document for the variant stated |
| D_Bharti_NBP | 8 | Product NBP in the Bharti portfolio tab | `sources/bharti-kpi/product_performance_FY24_to_H2FY27.pdf` |
| E_list_discrepancies | 12 | Rows from the universal product list's Discrepancies tab | Insurer website and the PDFs |
| F_v1_vs_deep | 15 | Where the brochure scan and the deep data disagree | The PDF |

## Rules
- Read the PDF itself, not the `text/` extracts. The extracts lose table layout.
- Do not fix anything in the data. Record what you find; S1 and S2 fix it.
- When a check needs judgement (is this a "rider" or "built-in"?), give your reason in the comment and mark UNSURE if you are not sure.
- Write any problem you see outside your sample at the bottom of the relevant tab with "found ad hoc".
- Target is 95% PASS per tab.

## When done
Commit the filled workbook on your branch `s3-bharti-analysis` (same branch as your Bharti work) as `qa/s3/s3_qa_workbook.xlsx`, push, and post a short entry in `coordination/CHAT.md` for `@S1` with the pass rate per tab and the 3 most important FAILs.
