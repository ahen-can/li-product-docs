# ULIP deep discovery, wave 1: summary

Status: in progress. This file grows insurer by insurer. One JSON per product is in `features/ulip/<UIN>.json`, and `scripts/validate_ulip_json.py` checks that every quote in it appears verbatim on its cited page. `results/deep_ulip_docs.csv` lists every document link found on each product page, with the site's own label and what happened to it.

## How the files were made

- `scripts/deep_collect.py` reads each product's own page from `briefs/ulip_deep_set.csv`. It classifies document links by the site's label, then stores the policy document, CIS, BI and any product-specific fund document. Files pass the same checks as the light pass: `%PDF`, `pdfinfo`, under 95 MB, and the product code in the text (by OCR if needed).
- `scripts/ulip_digest.py` and the reading notes in `scripts/ulip_specs/<UIN>.py` record which passages fill each field. `scripts/ulip_json.py` builds the JSON from them. Fields not filled stay `not stated in public documents` with a null value.
- Values come from the policy document first and the brochure second (eligibility tables and rider lists are usually only in the brochure). Quotes are copied from the PDF's reading-order text. Some Bharti brochures lose the "ti" ligature in extraction ("par cipa ng"), so their quotes read that way.

## Counts per insurer (website labels)

| Insurer | Products | Policy document | CIS | BI | Brochure | Fund documents |
|---|---|---|---|---|---|---|
| Bharti Life | 7 of 7 | 7 ("Policy Bond" x6, "Policy Bond Part B" x1) | 7 "Customer Information Sheet" | 0 (none published) | 7 "Download Brochure" | none stored: "Fund Factsheet" and "Fund Performance" are company-wide web pages |

## Spot checks by hand

- **Bharti:** Wealth Pro (130L100V03) and Grow Wealth Ultra (130L128V01). I compared the premium allocation, admin and discontinuance tables and the death benefit against the PDFs in layout mode.

## Anything odd

- **Bharti Grow Wealth Ultra (130L128V01).** The brochure on its product page prints Dream Shield Plus's UIN (130L125V01). I stored it with a note, but only for eligibility, which the policy bond does not state.
- **Bharti Dream Shield Plus (130L125V01).** The brochure's rider section says the rider is available "along with Bharti AXA Life Growth Shield Plus".
- **Bharti Future Invest (130L049V05).** The policy bond defines "Policy" as "Bharti AXA Life Grow Wealth".
- **Bharti Wealth Maximizer (130L121V01).** The policy bond still carries a template placeholder, "UIN:130XXXXXXX", next to the real UIN.

## New features found (seed for feature list v2)

- **Charge refunds.** Wealth Maximizer refunds 118% of every charge, fund management included, over the 5 years after the premium term. Grow Wealth Ultra refunds all allocation, admin and mortality charges at maturity. Growth Shield Plus refunds 2x the year 1-4 allocation charges in years 10-13. Dream Shield Plus and Growth Shield Plus return 1x, 2x and then 3x the previous decade's mortality charges from year 11.
- **Customer-specific boosters (Grow Wealth Ultra).** An "EmpowHer" booster for women, an ECS-payment booster, and an existing-customer booster.
- **Joint life.** Grow Wealth offers a single-pay joint-life ULIP that tops up the fund on the first death.
- **Mortality terms.** Several Bharti policy bonds guarantee their mortality rates for the term. Future Invest publishes separate male and female mortality tables.
- **No allocation charge.** Future Invest and Grow Wealth charge no premium allocation at all.

## data_not_public

- **Bharti.** Nothing deferred. All seven policy bonds publish full mortality tables and charge tables.

## Gaps and retry list

- **Bharti.** No BIs or product-specific fund factsheets are published.
