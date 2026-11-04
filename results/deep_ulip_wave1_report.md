# Deep ULIP discovery, wave 1 report

Written 4 Nov 2026 by S2. Branch `ccr-d0d84e00-joo2mp`. Per-insurer detail is in `results/deep_ulip_summary.md`.

## Result

- All 84 wave 1 ULIPs have a feature file in `features/ulip/`. The set is 10 insurers: Bharti 7, SBI 7, HDFC 7, Tata AIA 14, Bajaj 11, Axis Max 9, LIC 5, ABSLI 10, Canara HSBC 8, Ageas Federal 6.
- 251 documents are stored for these products (84 policy documents, 76 CIS, 91 brochures), 217 MB in total. Every file starts with `%PDF`, matches its sha256 in `index.csv`, and has text (scanned files are OCR'd).
- The 5,460 field entries hold 3,762 with a verbatim quote, 1,445 marked "not stated in public documents", and 253 "not offered" or "n/a" entries that carry a note in place of a quote.
- 197 features outside the schema are logged for feature list v2. 44 items are logged as "data not public".

## Checks run

| Check | Result |
|---|---|
| `validate_ulip_json.py`, every quote found verbatim on its cited page | 84 of 84 files pass |
| `check_consistency.py`, index rows against stored files | 0 problems |
| `scripts/s2_tools/crosscheck.py`, each JSON against the deep set, `index.csv`, sha256, PDF header, text density and printed UIN | 84 clean |
| `scripts/s2_tools/valuecheck.py`, do the numbers in a value appear in its quotes | see "Quote quality" below |
| Spot checks by hand, two products per insurer, tables compared with the PDF in layout mode | listed in the summary file |

## Documents by insurer

| Insurer | Products | Policy documents | CIS | Brochures |
|---|---|---|---|---|
| ABSLI | 10 | 10 | 8 | 10 |
| Axis Max Life | 9 | 8 | 8 | 9 |
| Bajaj Life | 11 | 11 | 13 | 13 |
| Bharti Life | 7 | 7 | 7 | 7 |
| Canara HSBC Life | 8 | 8 | 8 | 8 |
| HDFC Life | 7 | 8 | 0 | 8 |
| LIC | 5 | 5 | 5 | 9 |
| SBI Life | 7 | 7 | 7 | 7 |
| Tata AIA Life | 14 | 14 | 14 | 15 (i Systematic has the old V04 literature and the V11 upload) |
| Ageas Federal Life | 6 | 6 | 6 | 6 |

No insurer publishes a benefit illustration (BI) as a PDF, and none links a product-specific fund factsheet on the product page. Counts above are what the insurer's own product pages link.

## Not public, or missing

- **HDFC.** No CIS is linked for any of the 7 products.
- **ABSLI.** Fortune Wealth and Salaried Suraksha link no CIS. The Wealth Aspire policy document prints no product code, so it is stored with a note and nothing is quoted from it.
- **Axis Max.** Online Savings Plan Plus (104L131V03) has no policy document and no CIS on its page.
- **Tata AIA.** Smart Sampoorna Raksha Pro (110L172V03) has only an image-only brochure without a UIN, so eligibility is "not stated". i Systematic (110L164V11) links only V04 sales literature on its page. You supplied the V11 policy document, CIS and brochure, and the file is rebuilt from them. The CIS prints V10, noted in the index. The mortality rate table is on Tata's website, not in these documents.
- **Canara HSBC.** Promise4Growth has no product page. Its three PDFs came from the file-name pattern of the Promise4Growth Plus page, each carries the right UIN, and the index notes say so.
- **Ageas Federal.** Three product pages also link a one-page "Flyer" or "KFD" that was not stored. The Enhanced Value Fund has no description in the Smart Growth brochure.
- **Mortality rates.** Canara, ProGrow (Ageas), most LIC policy documents and some Tata products print only sample ages or no table. These are in the "data not public" list per file.

## Needs your upload

Nothing. The Tata AIA i Systematic V11 documents arrived and are stored and used.

## Quote quality

The brief asks that every quote contains the value itself. `valuecheck.py` compares the numbers in each value with the numbers in its quotes.

- 2,482 fields hold numbers. In 403 of them no number from the value appears in any quote. Most of these are long composite values (a whole charge table summarised in words) whose quote supports the claim but not every digit.
- 89 of the 403 have a short value ("65 years", "Rs 5,000"). These are the ones to fix first. Per insurer: Tata AIA 21, SBI 17, HDFC 10, Axis Max 14, Bajaj 7, ABSLI 6, Bharti 6, Canara 8.
- At the end of wave 1, 61 fields in 28 files were redone with value-bearing quotes: 57 got an extra row-level quote (the Tata eligibility rows, SBI and HDFC redirection and switching fields, Bharti switching, Axis, ABSLI, Bajaj, Canara and LIC fields), 3 SBI fields that had no quote now have one, and Bharti Grow Wealth Ultra's administration charge is now a nested table checked against the page image. The original quotes stay in place, so a redone field now has an old quote plus a new one. About 360 older fields were not touched.
- Ageas Federal and LIC have no short-value field flagged. The 5 and 6 fields that lack a number in their quotes are composite values.

The Bajaj Smart Wealth Goal VII Child Wealth and Joint Life Wealth variants are now captured as six quoted entries in `new_features_not_in_schema` (eligibility, premium and sum assured, administration charge, fund charges). They are not field by field, because a field cites one document and each variant has its own brochure. Their mortality and discontinuance tables are not captured.

## Findings to note

- **Return of charges.** Common in this set: Canara SecureInvest (2x allocation and mortality), Ageas ProGrow (4x allocation, 1x to 3x administration, 1x to 2x mortality), Tata, ABSLI and Bharti. Details are in the "new features" section of the summary file.
- **Zero or low administration charges.** Ageas Platinum Wealth Builder and Canara Promise4Growth Plus and Promise4Wealth (year 1) charge none or very little.
- **Premium funding after death.** Canara Promise4Care and Shield, Ageas Platinum and Golden Years, and Wealth Edge Premium Plus pay future premiums after the life assured dies.
- **Spouse cover.** Ageas Platinum Wealth Builder adds a second life with its own sum assured.
- **Source quirks.** Ageas product pages hold their documents in page data, not link tags. Canara policy documents are samples. ABSLI pension fund codes wrap across table cells. All are noted in the summary file.

## Next steps

1. Fix the 89 short-value fields, starting with Tata AIA and SBI.
2. Merge this branch so feature list v2 can use the 197 new-feature entries.
