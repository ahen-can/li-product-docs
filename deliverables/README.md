# Deliverables

Each link downloads the file.

| # | File | What it is |
|---|---|---|
| 01 | [01_life_insurance_category_analysis_Q4FY26.xlsx](https://github.com/ahen-can/li-product-docs/raw/main/deliverables/01_life_insurance_category_analysis_Q4FY26.xlsx) | FY26 premium by category for 25 insurers, from the Q4 public disclosures (Form L-1-A-RA), with a group overlay and observations. Same file as the first version. |
| 02 | [02_universal_product_list.xlsx](https://github.com/ahen-can/li-product-docs/raw/main/deliverables/02_universal_product_list.xlsx) | 633 in-scope individual products (Council list Sep-2026, plus the official ICICI and Bharti lists, plus SBI and Bajaj from their websites). The Discrepancies tab lists every mismatch between sources. |
| 03 | [03_light_discovery.xlsx](https://github.com/ahen-can/li-product-docs/raw/main/deliverables/03_light_discovery.xlsx) | The brochure pass. Status, document, source URL and description line per product, counts per insurer, the manual list, flags and site notes. |
| 04 | [04_feature_list_v1.xlsx](https://github.com/ahen-can/li-product-docs/raw/main/deliverables/04_feature_list_v1.xlsx) | Feature list v1 (v1.1 with the negation guard) from 516 brochures, for all 5 categories. |
| 05 | [05_feature_list_ulip_v2.xlsx](https://github.com/ahen-can/li-product-docs/raw/main/deliverables/05_feature_list_ulip_v2.xlsx) | ULIP feature list v2 for 140 ULIPs. 21 use deep data (Bharti, SBI, HDFC) and 119 use brochure data. It adds 36 schema rows and 21 new features found in policy documents, plus a v1 corrections tab. v3 follows when all 78 deep products are in. |

`scripts/build_deliverables.py` rebuilds 02 and 03 from the repo data.
