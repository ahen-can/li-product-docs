# Deliverables

Each link downloads the file.

| # | File | What it is |
|---|---|---|
| 01 | [01_life_insurance_category_analysis_Q4FY26.xlsx](https://github.com/ahen-can/li-product-docs/raw/main/deliverables/01_life_insurance_category_analysis_Q4FY26.xlsx) | FY26 premium by category for 25 insurers, from the Q4 public disclosures (Form L-1-A-RA), with a group overlay and observations. Same file as the first version. |
| 02 | [02_universal_product_list.xlsx](https://github.com/ahen-can/li-product-docs/raw/main/deliverables/02_universal_product_list.xlsx) | 633 in-scope individual products (Council list Sep-2026, plus the official ICICI and Bharti lists, plus SBI and Bajaj from their websites). The Discrepancies tab lists every mismatch between sources. |
| 03 | [03_light_discovery.xlsx](https://github.com/ahen-can/li-product-docs/raw/main/deliverables/03_light_discovery.xlsx) | The brochure pass. Status, document, source URL and description line per product, counts per insurer, the manual list, flags and site notes. |
| 04 | [04_feature_list_v1.xlsx](https://github.com/ahen-can/li-product-docs/raw/main/deliverables/04_feature_list_v1.xlsx) | Feature list v1 (v1.1 with the negation guard) from 516 brochures, for all 5 categories. |
| 05 | [05_feature_list_ulip_v3.xlsx](https://github.com/ahen-can/li-product-docs/raw/main/deliverables/05_feature_list_ulip_v3.xlsx) | ULIP feature list v3: 141 ULIPs, all 84 deep-discovery products (9 leaders and challengers plus Bharti) with policy-document data, the rest from brochures. Includes new features found in policy documents, each checked by hand. |
| 06 | [06_ulip_comparison_pilot.xlsx](https://github.com/ahen-can/li-product-docs/raw/main/deliverables/06_ulip_comparison_pilot.xlsx) | ULIP pilot comparison: Bharti's 3 ULIPs against 11 peer and reference products, 78 rows (charges, returns from our calculator, refunds, flexibility, protection, new features), best in class highlighted, evidence for every cell. |
| 07 | ULIP pilot deck: https://claude.ai/artifact/3VgZFusjxhJRLpqkBeXNLU (private to the owner until shared; downloads as PPTX or PDF). Slide source in `07_ulip_deck_source/`. | 12 slides: market, Bharti's ULIP position, landscape, features, Wealth Pro vs 4 leaders' products, returns, where Bharti leads and trails, five moves for discussion, method and limits. |
| 08 | [08_ulip_pilot_walkthrough.html](https://github.com/ahen-can/li-product-docs/raw/main/deliverables/08_ulip_pilot_walkthrough.html) | The walkthrough page for Neha. It shows how the ULIP pilot was built, step by step, with sheet previews, QA results, limits and questions. Download it and open it in a browser. |
| 09 | [09_ulip_pilot_deck.html](https://github.com/ahen-can/li-product-docs/raw/main/deliverables/09_ulip_pilot_deck.html) | S1's ULIP pilot deck, restyled with the content unchanged, as 12 slides in one file. Slide 11 lists observations, not recommendations. Download it and open it in a browser. Source slides are in docs-internal/s2_neha_walkthrough/deck. |

| 08 | ULIP Field Guide (walkthrough for beginners): https://claude.ai/artifact/G4BK3Ed5aep7B8ccWEJHom (private until shared). Page source in `08_ulip_field_guide/ulip_field_guide.html`; open it in a browser. | Product types, how a ULIP works, charges, features, returns, companies, popular products, where Bharti stands, glossary. |

`scripts/build_deliverables.py` rebuilds 02 and 03 from the repo data.
