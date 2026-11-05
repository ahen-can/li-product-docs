# Methods log: how this project works

This file explains how each output is produced, which script does it, and why we made the choices we made. The project state and next steps are in `PROJECT_MEMORY.md`. The full decision trail is in `docs-internal/plan_history.md`. The conversation between sessions is in `coordination/CHAT.md`.

## Working model
- **The user decides.** S1 (main session) plans, builds analysis and merges. S2 (second session) collects documents and reads them field by field. S3 (a session on the user's laptop) does the Bharti analysis from local files and then QA. Rahul checks samples by hand.
- **One task at a time, checked in with the user.** Accuracy before speed. Ambiguous or garbled items go to `for-your-attention/` and to the user, never silently resolved.
- **Official sources only.** Insurer websites, IRDAI, the Life Insurance Council, public disclosures, annual reports, investor presentations, press releases. The one agreed exception is fund ratings (Value Research or Morningstar), entered by hand with the source named.
- **Every number carries its source.** Document, page and a verbatim quote for deep data; form and page for PD numbers; URL for every stored file (`index.csv`).
- **Categories come from the IRDAI description line**, never from product names.
- **Rebuildable outputs.** Every Excel is built by a script from data files in the repo. Re-running the script after new data arrives gives the next version.

## Pipeline and scripts

| Step | Output | Script | Notes |
|---|---|---|---|
| 1. Category market sizing (phase 1) | deliverables/01 (boom repo: `li-category-analysis/`) | boom `scripts/build_data.py`, `make_xlsx.py`, `add_bharti_tabs.py` | FY26 PD Form L-1-A-RA by segment; group overlay from L-25(ii). Bharti portfolio tab uses Bharti's official Product Performance disclosure. |
| 2. Universal product list | `master_list.csv`, deliverables/02 | `scripts/build_master_v3.py`, `scripts/build_deliverables.py` | Council Sep-2026 list as the base, patched with the official ICICI and Bharti lists, and SBI and Bajaj from their sites. Website scraping (v2) was kept only as an audit trail because the Council list proved accurate. |
| 3. Light discovery (brochures) | `docs/`, `text/`, `index.csv`, `results/`, deliverables/03 | `scripts/light_discovery.py` (S2), `scripts/build_summary.py`, `build_coverage.py` | 1 request per second per site; `%PDF` and UIN checks; blocked sites not contacted. |
| 4. Feature list v1 (all categories) | `analysis/feature_list_v1.xlsx`, deliverables/04 | `analysis/scripts/extract_v1.py`, `build_feature_list_v1.py` | Keyword and context rules on brochure text, with a negation guard. Shows whether a feature is mentioned, not its type. |
| 5. ULIP deep discovery | `features/ulip/<UIN>.json`, `results/deep_ulip_summary.md` | `scripts/deep_collect.py`, `ulip_digest.py`, `ulip_json.py`, `ulip_specs/`, `s2_tools/` (S2); `scripts/validate_ulip_json.py`, `check_consistency.py` | Policy document first, brochure second. Each field has a value, a status (built-in, optional, rider, not offered, not stated), the site's document label, a page and a verbatim quote. The validator checks every quote is on its page. |
| 6. ULIP feature list v2 / v3 | `analysis/feature_list_ulip_v3.xlsx`, deliverables/05 | `analysis/scripts/build_ulip_features.py` | Deep data where it exists, v1 brochure flags otherwise. Flags weak quotes (label only). Lists every v1 vs deep disagreement. |
| 7. New-feature search | `analysis/v3/new_feature_candidates.csv`, `new_feature_verdicts.csv` | `analysis/scripts/scan_new_features.py`, `new_feature_verdicts.py` | A search pattern per new feature runs over every deep product's documents. S1 reads each match and records Y or N with a reason. Rejection reasons: the feature belongs to a rider; standard clause every ULIP has; staff-only; the words match but the feature is different. |
| 8. ULIP calculator | `calc/ulip.py`, `calc/params/ulip/`, `calc/results_ulip*.csv` | `calc/tools/make_ulip_params.py`, `extract_mortality.py` | Monthly fund projection from the policy document's charges and mortality table, at 4% and 8%. Checked against SBI, HDFC and Bharti quote tools and illustrations: within 0.3% (excluding GST, as insurers illustrate). |
| 9. Non-par IRR | `calc/engine.py`, `calc/params/130N122V04.json` | | Exact from published factor tables (Bharti Income Laabh). |
| 10. QA | `qa/checker_workbook.xlsx` (Rahul), `qa/s3/s3_qa_workbook.xlsx` (S3) | `qa/s3/build_s3_workbook.py` | Random samples with a fixed seed, ground truth named per check, target 95% PASS. |

## Key choices and why
- **Council list as the base for products:** the user's official ICICI and Bharti lists matched it almost exactly; website scraping produced more noise than signal.
- **Breadth then depth:** a brochure for every product (to see the whole market and spot innovators), then policy documents for the chosen insurers' products only (to compare exactly).
- **Selection of insurers per category:** the smallest set reaching 80% of category premium (leaders), plus 3 challengers scored on features, specialisation and growth, plus Bharti; LIC as a reference column (`analysis/selection_framework.md`). For ULIP the third challenger is Ageas (user's choice); Kotak dropped.
- **Output size:** the deck shows 5 products per category; the supporting Excel 10 to 15.
- **Deep data beats brochure data** wherever both exist. The v1 brochure scan is fine for "does the market offer X", not for product-by-product comparison.
- **Calculator results are shown on two bases:** excluding GST (what insurers illustrate, for checking) and including GST (what the customer pays).
- **"Net yield" definitions differ by insurer** (Bharti's excludes mortality charges), so comparisons use our calculator's IRR on one definition.
- **Versions:** feature list v2 is the rolling ULIP list; v3 is the final one once S2's last 14 and ICICI's 13 are in.

## Rules for adding new data
- Manual uploads go to `manual-uploads/<insurer>/` with `sources.csv` (see `manual-uploads/README.md`). S2 moves them into `docs/` with an `index.csv` row.
- After new deep files arrive: run `scripts/validate_ulip_json.py`, then `analysis/scripts/scan_new_features.py`, review new candidate rows and add verdicts in `new_feature_verdicts.py`, then rebuild with `build_ulip_features.py` and copy to `deliverables/05`.
- Do not commit personal documents (benefit illustrations with a name) to the repo.

## QA overrides and rider recoding (5 Nov 2026)
- `analysis/scripts/make_s3_overrides.py` turns S3's tab B FAILs into `analysis/v3/s3_overrides.csv` (63 rows, Bharti). UNSURE rows are not applied; they wait for rules in `analysis/v3/coding_rules.md`.
- `build_ulip_features.py` applies, in this order: the deep data, then the rider map (`results/ulip_rider_map.csv`: a feature the ULIP does not give itself but a rider it names covers becomes R), then every `analysis/v3/*_overrides.csv`. Tabs "QA overrides" and "Rider recoding" list each change.
- `build_ulip_comparison.py` reads corrected cells from `product_features_ulip_v3.csv`, so run it after `build_ulip_features.py`.
- Universal rider list from the Council sheet: `analysis/scripts/build_rider_list_council.py` writes `analysis/riders/rider_list_council.csv` and `.xlsx` (225 riders). Tally against S2's list by UIN when it lands.

## Feature list v4 (5 Nov 2026)
- Order of steps in `build_ulip_features.py`: deep data; riders (`results/ulip_rider_benefits.csv`); QA overrides (`analysis/v3/*_overrides.csv`, `analysis/v4/*_overrides.csv`); v4 rules and scans. Outputs `analysis/feature_list_ulip_v4.xlsx`, `product_features_ulip_v4.csv` and `analysis/v4/v4_changes.csv` (one row per cell the rules or scans changed). v3 files are kept as they were.
- Run `analysis/scripts/additions_basis.py` first: it writes `analysis/v4/additions_basis.csv` (rule 2, option b) from the deep additions fields, with reviewed exclusions in the script.
- Rules: `analysis/v3/coding_rules.md`. Judgement calls for seniors: `for-your-attention/questions_for_seniors.md`, section E.
- QA: `qa/s3_v4/` (brief, builder, workbook; 887 rows).
- Calculator: SBI Smart Fortune Builder now includes its periodic Guaranteed Additions (policy p27); net yield at 8% excl. GST moved from 6.00% to 6.16%.
