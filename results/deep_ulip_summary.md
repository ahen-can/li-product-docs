# ULIP deep discovery, wave 1: summary

Status: in progress. This file grows insurer by insurer. One JSON per product is in `features/ulip/<UIN>.json`, and `scripts/validate_ulip_json.py` checks that every quote in it appears verbatim on its cited page. `results/deep_ulip_docs.csv` lists every document link found on each product page, with the site's own label and what happened to it.

## How the files were made

- `scripts/deep_collect.py` reads each product's own page from `briefs/ulip_deep_set.csv`. It classifies document links by the site's label, then stores the policy document, CIS, BI and any product-specific fund document. Files pass the same checks as the light pass: `%PDF`, `pdfinfo`, under 95 MB, and the product code in the text (by OCR if needed).
- `scripts/ulip_digest.py` and the reading notes in `scripts/ulip_specs/<UIN>.py` record which passages fill each field. `scripts/ulip_json.py` builds the JSON from them. Fields not filled stay `not stated in public documents` with a null value.
- Values come from the policy document first and the brochure second (eligibility tables and rider lists are usually only in the brochure). Quotes are copied from the PDF's reading-order text. Some Bharti brochures lose the "ti" ligature in extraction ("par cipa ng"), so their quotes read that way.

## Counts per insurer (website labels)

| Insurer | Products | Policy document | CIS | BI | Brochure | Fund documents |
|---|---|---|---|---|---|---|
| SBI Life | 7 of 7 | 7 "Policy Document" | 7 "Customer Information Sheet (CIS)" | 0 (none published) | 7 "Product Brochure/Prospectus" (5 products also link a "Product Guide" leaflet, not stored) | none |
| HDFC Life | 7 of 7 | 8: "<product> - <UIN> - Policy Document" or "Policy Bond" (Smart Pension Plan has separate "Policy Bond offline" and "Policy Bond Online" files) | 0 (none linked) | 0 (none linked) | 7 "Download Brochure" (Smart Woman also links a retail brochure, stored as brochure-2) | none |
| Bharti Life | 7 of 7 | 7 ("Policy Bond" x6, "Policy Bond Part B" x1) | 7 "Customer Information Sheet" | 0 (none published) | 7 "Download Brochure" | none stored: "Fund Factsheet" and "Fund Performance" are company-wide web pages |

## Spot checks by hand

- **SBI:** eWealth Plus (111L147V01) and Smart Invest Builder (111L153V01). I compared the clause-17 charges, the partial withdrawal limits and the guaranteed-addition table against the PDFs.
- **HDFC:** Click 2 Wealth (101L133V03) and Smart Protect Plus (101L187V04). I compared the fund management, discontinuance and special-addition clauses, and the allocation-charge, mortality-refund and maturity-booster tables, against the PDFs in layout mode.
- **Bharti:** Wealth Pro (130L100V03) and Grow Wealth Ultra (130L128V01). I compared the premium allocation, admin and discontinuance tables and the death benefit against the PDFs in layout mode.

## Anything odd

- **Bharti Grow Wealth Ultra (130L128V01).** The brochure on its product page prints Dream Shield Plus's UIN (130L125V01). I stored it with a note, but only for eligibility, which the policy bond does not state.
- **Bharti Dream Shield Plus (130L125V01).** The brochure's rider section says the rider is available "along with Bharti AXA Life Growth Shield Plus".
- **Bharti Future Invest (130L049V05).** The policy bond defines "Policy" as "Bharti AXA Life Grow Wealth".
- **SBI Smart Elite Plus (111L146V01).** The brochure's eligibility table prints the rider UIN as "111AXXXV01" (a template placeholder). The rider section of the same brochure gives the real UIN, 111A049V01.
- **SBI eWealth Plus (111L147V01).** The site labels the policy document and CIS "new fund addition" versions (Form No 861).
- **Bharti Wealth Maximizer (130L121V01).** The policy bond still carries a template placeholder, "UIN:130XXXXXXX", next to the real UIN.

- **HDFC Click 2 Invest Plus (101L191V02).** One page of the policy bond calls the product "Click 2 Invest".
- **HDFC Smart Woman (101L082V03).** The product page links a policy document stored in the site's "savings-and-investment-withdrawn" folder. It prints 101L082V03, the UIN in the deep set, so I kept it with a note.
- **HDFC Smart Protect Plus (101L187V04).** The guarantee-charge table prints one rate, 0.50% p.a., across both Capital Growth Fund and Capital Secure Fund. I recorded it as applying to Capital Growth Fund and noted the doubt.
- **HDFC central pages.** The "specimen policy documents" and "product brochures" links on every product page open company-wide pages. The collector reads them only for links that name the product and its UIN version.

## New features found (seed for feature list v2)

- **Charge refunds.** Wealth Maximizer refunds 118% of every charge, fund management included, over the 5 years after the premium term. Grow Wealth Ultra refunds all allocation, admin and mortality charges at maturity. Growth Shield Plus refunds 2x the year 1-4 allocation charges in years 10-13. Dream Shield Plus and Growth Shield Plus return 1x, 2x and then 3x the previous decade's mortality charges from year 11.
- **Customer-specific boosters (Grow Wealth Ultra).** An "EmpowHer" booster for women, an ECS-payment booster, and an existing-customer booster.
- **Joint life.** Grow Wealth offers a single-pay joint-life ULIP that tops up the fund on the first death.
- **Mortality terms.** Several Bharti policy bonds guarantee their mortality rates for the term. Future Invest publishes separate male and female mortality tables.
- **No allocation charge.** Future Invest and Grow Wealth (Bharti) and eWealth Plus (SBI) charge no premium allocation at all.
- **SBI guaranteed additions.** Smart Invest Builder adds guaranteed additions every 5 years from year 10 (up to 150% of annualised premium at a 30-year term) plus a maturity addition. Smart Fortune Builder adds 5% or 10% of premium at maturity by premium band.
- **SBI premium caps.** Smart Fortune Builder caps the premium at Rs 2,50,000, and Smart Invest Builder at Rs 20,000 a month (monthly only).
- **SBI built-in protection.** Smart Elite Plus has a built-in accident benefit, with total permanent disability paid in 10 yearly instalments. Smart Scholar Plus (child plan) has a built-in premium payor waiver and accident benefit, and its loyalty additions continue after the parent's death.
- **SBI withdrawal rules.** Retire Smart Plus allows withdrawals only for listed purposes (education, marriage, home, illness, re-skilling, starting a business), at most 3 times. Retire Smart Plus also gives SBI staff lower allocation charges. Several SBI products cap withdrawals at 15% of fund value and 10 per term.
- **SBI settlement on death.** Several SBI products let the nominee take the death benefit in instalments while it stays invested.

- **HDFC charge refunds.** Smart Protect Plus returns 2x then 3x mortality charges from year 11, all year 1-4 allocation charges in years 10-17, all fund management charges at age 85 or maturity (if cover is above 30x premium), and 2x guarantee charges at maturity. Click 2 Invest Plus and Click 2 Retire Plus II return admin and mortality charges under their "Loyalty" options. Click 2 Wealth returns all mortality charges at maturity.
- **HDFC capital guarantees.** Click 2 Retire Plus II (Secure) guarantees 101% of premiums plus 1% for each year the term exceeds the premium term. Smart Protect Plus options B and D guarantee premiums paid less withdrawals.
- **HDFC death benefit designs.** Click 2 Invest Plus and Sampoorn Nivesh Plus offer a "Classic Waiver Plus" option that pays the sum assured, funds future premiums and pays a monthly income of a chosen % of sum assured. Smart Protect Plus offers decreasing cover after a chosen level-cover period.
- **HDFC Smart Woman.** Premium waiver and periodic cash on pregnancy complications, a child born with congenital disorders, female cancers and (Elite) death of the spouse. Up to 12 free switches and withdrawals in the year after childbirth. Years 11-15 allocate 102.5% of premium.
- **HDFC pensions.** Click 2 Retire Plus II and Smart Pension Plan allow partial withdrawals only for listed purposes, at most 3 times. Both accept UK pension transfers (QROPS/QOPS). Smart Pension Plan has an automatic rebalancing strategy by years to vesting (90/10 down to 20/80).
- **HDFC other.** Cheaper service requests online (Rs 25 instead of Rs 250). Sampoorn Nivesh Plus pays a loyalty reward of 1.5% x term x annual premium on direct-channel policies, and lets a child's cover start up to 2 years late with no mortality charge until then. Click 2 Wealth adds 1% of premium as "special additions" for 5 years.

## data_not_public

- **SBI.** Nothing deferred. Mortality tables are published in every policy document.
- **HDFC.** Nothing deferred. Every policy document publishes its charge tables and mortality rates.
- **Bharti.** Nothing deferred. All seven policy bonds publish full mortality tables and charge tables.

## Gaps and retry list

- **Bharti, SBI and HDFC.** None publishes BIs or product-specific fund factsheets on the product page. HDFC product pages link no CIS either.
- **HDFC, fields left "not stated".** Riders are not listed in any HDFC policy document. Launch dates are taken from the F&U date printed in each policy bond, except Smart Woman, which prints none.
- **SBI, fields to finish on the second pass.** Some standard fields are "not stated" because I did not quote them, not because the documents lack them: revival period and surrender value for Smart Privilege Plus and Smart Scholar Plus, and switching for Smart Scholar Plus. Their policy documents use the same clauses as eWealth Plus.
