# Brief for S2: re-read the premium payment grids for the 84 ULIPs

## Why
S3's QA of feature list v4 found 10 wrong cells in a sample of 25 for the three pay-term rows (single, limited and regular pay). The deep JSON field `eligibility.ppt_options` often lists the PPT choices without saying which policy terms they go with, so "regular pay" (PPT equal to the policy term) is missed. Examples: LIC SIIP "Same as Policy Term"; Bajaj Goal Assure IV, where PPT 10 is allowed with PT 10; single pay in Tata Smart Fortune Plus and Bajaj Smart Wealth Goal VII. Bharti's 7 are already checked by S3; do the other 77.

## What to do
For each ULIP, read the PT and PPT table or text in the brochure or policy document (the PDF, not the text extract). Write one row per product to `results/ppt_grid.csv`:

| Column | Meaning |
|---|---|
| uin | ULIP UIN |
| single_pay | Y / N / ? (N only if the document says single pay is not available, or the document lists every payment option and single is not among them) |
| limited_pay | Y / N / ?, with the limited PPTs allowed (e.g. "5, 7, 10, 12") |
| regular_pay | Y / N / ?. Y if any PPT can equal the policy term, whether the document calls it "regular" or not |
| variants | if the answer differs by variant or plan option, say which |
| doc, page, quote | where the grid is, and a quote that shows the answer |

## Rules
- Insurer documents already in `docs/` only. No new downloads are needed.
- Push on your branch and post a short CHAT entry for `@S1` with the count of products where single, limited or regular pay changed from the v5 values (`analysis/product_features_ulip_v5.csv`, features `ppt_single_pay`, `ppt_limited_pay`, `ppt_regular_pay`).
