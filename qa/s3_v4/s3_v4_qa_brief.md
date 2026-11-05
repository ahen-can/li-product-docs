# Brief for S3: QA of ULIP feature list v4

## Why
v4 changes many cells at once, and the next steps depend on it: the peer comparison, the Bharti has/lacks claims, the deck. Treat v4 as a draft until this QA is in. What changed since your v3 QA:
- **Your 63 Bharti corrections** are applied (`analysis/v3/s3_overrides.csv`).
- **Riders.** S2 read the 30 riders our 84 ULIPs name. Waiver of premium, critical illness, accidental death and disability are coded R where only a named rider gives them. An earlier R that came only from a rider's name is now "?" where the rider documents show no such benefit.
- **Coding rules** decided by the user on 5 Nov (`analysis/v3/coding_rules.md`):
  1. Payor waiver counts only when the payer's own event triggers it. Who may opt in does not count.
  2. Option b: additions are split by basis, "% of premium" (amount known at the start) or "% of fund value" (moves with the market). The "scheduled guaranteed additions" row is retired, because every addition written into a ULIP contract is payable.
  3. The same loyalty design gets the same code.
  4. Online or direct purchase terms go only to `lower_charges_online`. Staff, women, existing customers or family, and auto-pay stay in `customer_type_boosters`. A clause for "staff or online" goes in both.
  5. "Index or low-cost funds" is replaced by three rows: index fund offered, lowest FMC on any fund, lowest FMC on an equity fund.
- **Scans of all 84** for your patterns: policy loan "not applicable", termination when the fund falls below a level, mortality as a % of IALM. Hits say "to confirm".
- **Loose v1 row.** "Pension ULIP with guaranteed vesting" is now read from the IRDAI description line.

## What to check
Workbook: `qa/s3_v4/v4_qa_workbook.xlsx`, built by `qa/s3_v4/build_v4_qa_workbook.py`. Fill the yellow columns: the correct value or status, PASS / FAIL / UNSURE, and a comment with document, page and quote. 887 rows.

| Tab | Rows | What |
|---|---|---|
| A_Bharti_claims | 106 | Every feature row: is the Bharti claim right, and are the counts plausible? |
| B_rider_cells | 123 | Every peer cell the rider step changed, plus 25 random unchanged R cells |
| C_additions_basis | 168 | All 84 products, both bases, with the "only for" conditions |
| D_funds | 252 | All 84 products: index fund, lowest FMC any fund, lowest FMC equity fund |
| E_rules_and_scans | 141 | Every other v4 change: rules 1, 3, 4, the scans, the pension row |
| F_peer_patterns | 97 | Random peer sample for your v3 patterns that v4 did not scan |

**Order.**
1. **Tab B first.** Riders change the most visible counts (waiver of premium went from 43 to 60 of 84).
2. **Then C and D.** These are new rows. Nobody has checked them yet.
3. **Then E, F, and A last.** A row-level error in A usually traces back to cells in B to F.

Read the PDFs, not the text extracts. Rider documents are in `docs/<insurer>/riders/<rider UIN>/`; S2's reading of them is in `features/riders/<UIN>.json` and `results/ulip_rider_benefits.csv`.

## Things to watch
- **Waiver of premium.** A rider that waives only its own premium (HDFC Protect Plus and Health Plus, Bajaj Care Plus) does not give waiver of the ULIP premium. A rider that waives premium on critical illness (SBI) does not pay a critical illness benefit.
- **Accidental death.** A term rider pays on any death. It is not accident cover by itself.
- **Additions.** Charge refunds are not additions. Fund-floor top-ups (Tata and Axis "Cover Continuance Booster") pay only when the fund falls low and are not counted. Check the "only for" conditions, especially Bharti Grow Wealth Ultra (women, auto-pay).
- **Fund charges.** S2 sometimes filled per-fund FMC with a default (HDFC and LIC show 1.35% on bond funds). Check against the fund table. Say if a fund S1 called equity by its name is not an equity fund.
- **Silence vs "not offered".** "N" needs the document to say not available. Silence is "?".

## Rules
- Do not edit v4, the deep JSONs or the rider JSONs. Record what you find; S1 fixes the data and rebuilds.
- If a FAIL is a pattern, say so once in your CHAT entry. Do not repeat it on every row.
- Work on your branch `s3-bharti-analysis` (merge main first), commit the filled workbook as `qa/s3_v4/v4_qa_workbook.xlsx`, and push.
- Post a short CHAT entry for `@S1`: pass rate per tab, the FAILs grouped by pattern, and any rule that still needs a decision.
