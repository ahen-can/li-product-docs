# Deliverables

Each link downloads the file.

| # | File | What it is |
|---|---|---|
| 01 | [01_life_insurance_category_analysis_Q4FY26.xlsx](https://github.com/ahen-can/li-product-docs/raw/main/deliverables/01_life_insurance_category_analysis_Q4FY26.xlsx) | FY26 premium by category for 25 insurers, from the Q4 public disclosures (Form L-1-A-RA), with a group overlay and observations. Same file as the first version. |
| 02 | [02_universal_product_list.xlsx](https://github.com/ahen-can/li-product-docs/raw/main/deliverables/02_universal_product_list.xlsx) | 633 in-scope individual products (Council list Sep-2026, plus the official ICICI and Bharti lists, plus SBI and Bajaj from their websites). The Discrepancies tab lists every mismatch between sources. |
| 03 | [03_light_discovery.xlsx](https://github.com/ahen-can/li-product-docs/raw/main/deliverables/03_light_discovery.xlsx) | The brochure pass. Status, document, source URL and description line per product, counts per insurer, the manual list, flags and site notes. |
| 04 | [04_feature_list_v1.xlsx](https://github.com/ahen-can/li-product-docs/raw/main/deliverables/04_feature_list_v1.xlsx) | Feature list v1 (v1.1 with the negation guard) from 516 brochures, for all 5 categories. |
| 05 | [05_feature_list_ulip_v5.xlsx](https://github.com/ahen-can/li-product-docs/raw/main/deliverables/05_feature_list_ulip_v5.xlsx) | ULIP feature list v5: v4 plus S3's QA corrections (887 checks, 89% pass on v4). 141 ULIPs, 84 with policy-document data. Rider-delivered features from 30 rider documents, the user's coding rules (additions by % of premium or % of fund, index funds and lowest fund charges), payor riders, scans for S3's error patterns. The three pay-term rows are still being re-read for peers (S2). Earlier versions are in git history. |
| 06 | [06_ulip_comparison_pilot.xlsx](https://github.com/ahen-can/li-product-docs/raw/main/deliverables/06_ulip_comparison_pilot.xlsx) | ULIP pilot comparison: Bharti's 3 ULIPs against 11 peer and reference products, 81 rows (charges, returns from our calculator, additions by basis, refunds, flexibility, protection incl. riders, funds, new features), best in class highlighted, evidence for every cell. Reads feature list v5. |
| 07 | ULIP pilot deck: https://claude.ai/artifact/3VgZFusjxhJRLpqkBeXNLU (private to the owner until shared; downloads as PPTX or PDF). Slide source in `07_ulip_deck_source/`. | 12 slides: market, Bharti's ULIP position, landscape, features, Wealth Pro vs 4 leaders' products, returns, where Bharti leads and trails, five moves for discussion, method and limits. |
| 08 | [08_ulip_pilot_walkthrough.html](https://github.com/ahen-can/li-product-docs/raw/main/deliverables/08_ulip_pilot_walkthrough.html) | The walkthrough page for Neha. It shows how the ULIP pilot was built, step by step, with sheet previews, QA results, limits and questions. Download it and open it in a browser. |
| 09 | [09_ulip_pilot_deck.html](https://github.com/ahen-can/li-product-docs/raw/main/deliverables/09_ulip_pilot_deck.html) | S1's ULIP pilot deck, restyled with the content unchanged, as 12 slides in one file. Slide 11 lists observations, not recommendations. Download it and open it in a browser. Source slides are in docs-internal/s2_neha_walkthrough/deck. |

| 10 | ULIP Field Guide (walkthrough for beginners): https://claude.ai/artifact/G4BK3Ed5aep7B8ccWEJHom (private until shared). Page source in `10_ulip_field_guide/ulip_field_guide.html`; open it in a browser. | Product types, how a ULIP works, charges, features, returns, companies, popular products, where Bharti stands, glossary. |

`scripts/build_deliverables.py` rebuilds 02 and 03 from the repo data.
