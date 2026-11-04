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
| Tata AIA Life | 14 of 14 (13 with a policy document) | 13 ("Policy Document" x7, "Policy bond" x5, "Download Policy Document" x1) | 13 "Customer Information Sheet" | 0 ("Quote/Benefit Illustration" opens a quote web page) | 13 stored in the light pass; SSR Pro's brochure is image-only with no readable UIN, so it is not stored | none: the "View Fund Fact Sheet" link is one fund's factsheet shown on every page |
| HDFC Life | 7 of 7 | 8: "<product> - <UIN> - Policy Document" or "Policy Bond" (Smart Pension Plan has separate "Policy Bond offline" and "Policy Bond Online" files) | 0 (none linked) | 0 (none linked) | 7 "Download Brochure" (Smart Woman also links a retail brochure, stored as brochure-2) | none |
| Bharti Life | 7 of 7 | 7 ("Policy Bond" x6, "Policy Bond Part B" x1) | 7 "Customer Information Sheet" | 0 (none published) | 7 "Download Brochure" | none stored: "Fund Factsheet" and "Fund Performance" are company-wide web pages |
| Bajaj Life | 11 of 11 | 11: "Download" x9 on the product page, plus 2 not linked (Supreme and Smart Pension, found by the site's file-name pattern) | 13 "Download" or file-name labels (Smart Wealth Goal VII has 3) | 0 (none published; "E-Policy Bond" opens a login page) | 13: unlabelled links cited by file name (Smart Wealth Goal VII has 3 variant brochures, one found by file-name pattern) | none stored: "Investment Insight" is a company-wide factsheet |
| Axis Max Life | 9 of 9 (8 with a policy document) | 8 "Policy Contract" (Forever Young and Online Savings Plan documents were not linked on their own pages, see odd findings) | 8 "Customer Information Sheet" | 0 (none published) | 9 "Policy Prospectus" or "Prospectus" | none stored: the "Sustainable Yield Index Factsheet" is company-wide and "Monthly Factsheets" is a web page |

## Spot checks by hand

- **SBI:** eWealth Plus (111L147V01) and Smart Invest Builder (111L153V01). I compared the clause-17 charges, the partial withdrawal limits and the guaranteed-addition table against the PDFs.
- **Tata AIA:** Fortune Maxima (110L113V09) and Smart SIP (110L174V02). I compared the allocation-charge table, the admin charge, the loyalty additions and the maturity-booster table against the PDFs in layout mode.
- **HDFC:** Click 2 Wealth (101L133V03) and Smart Protect Plus (101L187V04). I compared the fund management, discontinuance and special-addition clauses, and the allocation-charge, mortality-refund and maturity-booster tables, against the PDFs in layout mode.
- **Bharti:** Wealth Pro (130L100V03) and Grow Wealth Ultra (130L128V01). I compared the premium allocation, admin and discontinuance tables and the death benefit against the PDFs in layout mode.
- **Bajaj:** Invest Protect Goal Plus (116L215V01) and LongLife Goal III (116L203V01). I compared the premium allocation, admin and discontinuance tables, the loyalty and return-of-mortality tables and the eligibility rows against the PDFs in layout mode.
- **Axis Max:** Flexi Wealth Advantage (104L121V05) and Platinum Wealth Plan (104L133V01). I compared the premium allocation band tables, administration, discontinuance and loyalty tables and the eligibility rows against the PDFs in layout mode.

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

- **Tata i Systematic Insurance Plan (110L164V11).** The deep set lists V11. Its product page is a separate microsite that links only the V04 sales literature. The JSON uses that brochure, with every value flagged, and the policy document is on the retry list.
- **Tata fund counts.** Part C of Fortune Maxima, Fortune Pro, Wealth Maxima and Smart Sampoorna Raksha says "24 Fund options" (Wealth Pro says 23). Their FMC tables list 31 funds.
- **Tata Shubh SIP (110L190V01).** The schedule of charges says there is no premium allocation charge, yet clause 3.4 refunds allocation charges from year 11.
- **Tata Fortune Pro (110L112V07).** Part C promises "return of charges", but the policy has no clause that returns a charge.
- **Tata fund codes.** Fortune Maxima prints the Tax Bonanza Consumption Fund code as "...TBC 100" in its FMC table and "...TBC 110" elsewhere. Shubh SIP prints the Enhanced Value Index Fund code as ULIF09816/02/26ENVALINDXL110; other Tata policies print "ULIF 098 16/02/26 EVI 110".
- **Tata Smart Fortune Plus (110L177V01).** The allocation-charge table charges the middle premium band more than the lowest band in years 4-5 (4.5%, 5.0%, 4.5%).
- **Bajaj Smart Pension (116L209V08).** The policy document on the site prints UIN 116L209V03 and the old Bajaj Allianz name. Its brochure and CIS print V08. Policy-document values carry a note.
- **Bajaj Fortune Gain II (116L196V05).** The specimen schedule inside the policy prints 116L196V04.
- **Bajaj GAIN (116L213V02).** The premium payment table prints 75 under "Maximum PPT", which reads as an age.
- **Bajaj Goal Assure IV (116L204V01).** The maximum sum assured table has 5 age columns but 4 values per row.
- **Bajaj Smart Wealth Goal VII (116L218V01).** The product page has no link for the Wealth variant brochure. The file-name pattern next to the other two returned a real PDF (`swg-wealth-brochure.pdf`). All documents on this page share the label "Download", so the JSON tags the later ones with their file name.
- **Bajaj Supreme (116L211V02).** The quarterly minimum is Rs 4,000, where the other Bajaj plans use Rs 3,000.
- **Axis Max Forever Young Pension (104L075V11).** The visible product page links no documents, but its page source contains the prospectus, policy document, CIS and leaflet links (script data). I stored the policy document and CIS from those exact URLs.
- **Axis Max Online Savings Plan Plus (104L131V03).** The page links "Policy Contract" and "Customer Information Sheet" files that print 104L098V06, the Online Savings Plan. I stored them under 104L098V06, whose own page links nothing. The Plus plan has only its prospectus.
- **Axis Max "Terms and Conditions" link.** Most Axis product pages link one company-wide leaflet under this label. It carries no product code, so it is recorded as failed.
- **Axis Max fund counts.** Fast Track Super says 30 funds and lists 32 including Secure Plus and the Discontinuance Policy Fund. Online Savings Plan Plus says 27 and lists 29.
- **Axis Max Flexi Wealth Advantage (104L121V05).** Its administration charge section is titled "All Years" but charges years 6 to 10 only.
- **Axis Max prospectuses.** Most tables print each premium band in six columns; the policy contracts are specimens with blank schedules, so charge values come from the prospectus.

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

- **Tata withdrawal plans.** Smart SIP, Shubh SIP and Smart Fortune Plus offer a chosen-rate withdrawal plan (pays fund growth above a chosen return) and an index-based plan (above benchmark CAGR, 10-year G-Sec, SBI savings or FD rates, or CPI).
- **Tata Cover Continuance Booster.** The Smart Sampoorna Raksha family and Shubh Wealth top up the fund when it falls below 10% of the premium (years 1-15) or below a fund value implied by a target net yield (from year 16), so cover does not lapse.
- **Tata refunds.** The Smart Sampoorna Raksha family, Shubh Wealth and Smart Raksha refund mortality charges monthly from year 11 (2x in some options) and allocation charges in years 10-13. SSR Supreme adds a "Twin Loyalty Booster" when bought with a protection plan.
- **Tata other.** Extra allocation for women ("Smart Lady"); a high premium booster (Smart Fortune Plus); online-only fund boosters up to 10% of fund value at maturity; mortality priced as a share of IALM by age band, with smokers and women at par (Fortune and Wealth series); Shubh SIP's Prime and Ultima fund 2x or 3x future premiums after death; Smart Raksha's sum assured steps up by 12.5% to 25% at set years; Smart Pension Secure adds 0.5% if the whole vesting benefit buys a Tata AIA annuity.

- **Bajaj family and booster features.** Magnum Fortune Plus III and Goal Based Saving III add a Family Benefit (0.5% or 1% of fund for relatives of customers). Magnum Fortune Plus III adds a Maturity Booster (0.25% to 1%) for existing customers or auto-pay payers, and three premium bands with allocation charges of 4%, 3% and 2%.
- **Bajaj charge refunds.** Goal Based Saving III returns up to 125% of mortality charges at maturity by premium band. Invest Protect Goal Plus returns mortality charges in steps (25% at year 7 to 100% at year 20) and, in the Elite variant, allocation charges at 7% a year compounded. Supreme returns 100% of mortality charges at year 15, every 5th year and at maturity, and adds back all allocation charges with 7% a year at year 15 (all nine variants are "effectively zero allocation charge"). LongLife Goal III returns mortality and waiver charges every 10 years from age 60.
- **Bajaj income options.** LongLife Goal III has Retired Life Income (0% to 12% of fund a year from age 45, each payment raised 0.5%). Invest Protect Goal Plus Elite has Smart Retire Income (1% to 6% a year). Settlement over 5 years carries a 0.5% Return Enhancer.
- **Bajaj Fund Maintenance Booster (Invest Protect Goal Plus).** From year 4 the company tops the fund up to one annualized premium if it falls below.
- **Bajaj strategies.** Trigger Based (moves gains to the Liquid Fund after a 15% equity rise), Target Asset Allocation (two funds, rebalanced quarterly) and Capital Preservation Oriented (steps toward debt as maturity nears).
- **Bajaj Smart Pension.** The Assure variant pays 105% of premiums on death, then the company pays the remaining premiums while the fund keeps growing. Vesting Booster of 2% and a return of allocation charges at year 15. Vesting can be postponed up to age 75.
- **Bajaj Smart Wealth Goal VII.** The Child Wealth variant waives premiums on death or accidental total permanent disability and pays one annualized premium each year until the end of the term. Fund Booster of 2% every 5 years from year 15.
- **Axis Max return of charges.** Flexi Wealth Advantage returns 0% to 100% of allocation and administration charges by premium band. Smart Term with Additional Returns returns 200% of allocation charges, 200% to 300% of mortality and morbidity charges and 300% of administration charges. Online Savings Plan Plus returns 125% or 150% of administration charges.
- **Axis Max death-benefit designs.** Online Savings Plan variant 2, Online Savings Plan Plus Gold, Platinum and Titanium, Shiksha Plus Super and Smart Term 3D Life Secure pay a lump sum, a monthly or yearly family income and then fund 1, 2 or 3 times the future premiums while the fund keeps growing.
- **Axis Max Cover Continuance Booster.** Smart Term with Additional Returns tops the fund up to 10% of annualized premium, or to a target-net-yield fund value, so cover does not lapse.
- **Axis Max Auto Debit Booster.** Flexi Wealth Advantage adds 0.75% of each of the first five years' premiums paid by auto debit.
- **Axis Max strategies.** Systematic Transfer Plan (Secure Plus Fund into growth funds over 12 months), Dynamic Fund Allocation, Lifecycle, Trigger Based and Self-Managed.
- **Axis Max pension.** Forever Young Pension accepts UK pension transfers (QROPS) and has a Save More Tomorrow top-up that rises 5% a year.
- **Axis Max Smart Withdrawals.** Flexi Wealth Advantage (whole life variant) allows up to 8% of fund value a year, and Online Savings Plan Plus up to 12%, without cutting the sum assured.

## data_not_public

- **SBI.** Nothing deferred. Mortality tables are published in every policy document.
- **Tata AIA.** Smart SIP and Smart Fortune Plus say the mortality table and the waiver factors are "given on Our website" and do not print them. The Smart Sampoorna Raksha family, Shubh Wealth and Smart Raksha print no mortality rates and name no place where they are published. The Fortune and Wealth series print full tables. Loyalty Program Reward amounts are only on the website.
- **HDFC.** Nothing deferred. Every policy document publishes its charge tables and mortality rates.
- **Bharti.** Nothing deferred. All seven policy bonds publish full mortality tables and charge tables.
- **Bajaj.** Fortune Gain II refers to Annexure 3 for mortality rates but does not attach it, and its specimen schedule does not print the administration charge. Magnum Fortune Plus III, Goal Based Saving III, Invest Protect Goal Plus, LongLife Goal III, Supreme and Smart Wealth Goal VII publish mortality rates in their policy documents. Smart Pension publishes them in the V03 document.
- **Axis Max.** Online Savings Plan Plus has no policy document, so its mortality rates are not public. The other eight policy documents print mortality tables (Fast Track Super p.23, Flexi Wealth Plus p.23, Flexi Wealth Advantage p.38, Forever Young p.22, Online Savings Plan p.18, Platinum Wealth p.32, Shiksha Plus Super p.21, Smart Term p.38); the JSON gives the prospectus sample ages where one exists.

## Gaps and retry list

- **Bharti, SBI and HDFC.** None publishes BIs or product-specific fund factsheets on the product page. HDFC product pages link no CIS either.
- **Tata AIA retry list.** i Systematic V11 policy document and CIS (only V04 sales literature found). Smart Sampoorna Raksha Pro eligibility (its only brochure is image-only without a UIN). Smart Pension Secure fund names (the two-column text splits names from codes).
- **HDFC, fields left "not stated".** Riders are not listed in any HDFC policy document. Launch dates are taken from the F&U date printed in each policy bond, except Smart Woman, which prints none.
- **SBI second pass (done).** Revival period and surrender value for Smart Privilege Plus and Smart Scholar Plus, and switching for Smart Scholar Plus, are now quoted from their policy documents.
- **Bajaj.** No BIs or product-specific fund factsheets. Smart Wealth Goal VII has three variants; the JSON records the Wealth variant field by field. Child Wealth (brochure.pdf, eligibility p.10, charges p.30) and Joint Life Wealth (brochure-2.pdf, eligibility p.9, charges p.26) are on the retry list. Smart Pension needs the V08 policy document if Bajaj publishes it.
- **Axis Max.** No BIs or product-specific fund factsheets. Online Savings Plan Plus needs its own policy document. Flexi Wealth Advantage online/ISNP allocation tables, Forever Young single-pay discontinuance table, Smart Term loyalty table for entry ages above 35, and the strategy mechanics for Online Savings Plan Plus and Platinum Wealth are not recorded field by field.
