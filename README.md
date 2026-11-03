# Life insurance product documents (India) — individual products

A repository of the official documents for currently active **individual** life insurance products from all Indian life insurers. It covers each product's policy document, sales brochure, and benefit illustration or customer information sheet where one is published. It exists so that feature comparison, product mapping and IRR work can cite the source text exactly.

**In scope:** active individual products in five market categories: **Protection, Non-Par Savings, Par, ULIP, Annuity** (including pension).
**Out of scope:** group products, health, riders, micro-insurance and withdrawn products.

## Layout

```
master_list.csv        every in-scope product: insurer, name, UIN, classification, product-page URL
index.csv              one row per downloaded document, including the exact source URL (see schema below)
coverage.md            per-insurer coverage, plus a manual-download list for anything the script could not fetch
docs/<insurer>/<UIN>/<doc_type>.pdf          original file, byte-for-byte as downloaded
text/<insurer>/<UIN>/<doc_type>.txt          text extract (pdftotext -layout; OCR if the PDF is scanned)
features/<category>.csv                      deep-extraction output (features with document and page citations)
scripts/                                     downloader and text extraction
CLAUDE.md                                    operating rules for any agent working in this repo
```

`<insurer>` is a short slug (e.g. `hdfc-life`, `sbi-life`, `bharti-life`). `<doc_type>` is one of `policy`, `brochure`, `bi`, `cis`, `leaflet`. If a product has two files of the same type (e.g. separate regular-pay and single-pay brochures), the second one gets a suffix: `brochure-2.pdf`.

## index.csv schema

| Column | Meaning |
|---|---|
| doc_id | `<UIN>-<doc_type>[-n]` |
| insurer, product_name, uin | as on the document / insurer site |
| linked_flag | `L` / `N`: the 4th character of the UIN |
| par_flag | `Par` / `Non-Par` / `NA`, taken from the IRDAI description line |
| irdai_description_line | verbatim, e.g. "A Non-Linked, Participating, Individual, Life Insurance Savings Plan" |
| market_category | Protection / Non-Par Savings / Par / ULIP / Annuity |
| pd_category | Par Life / Non-Par Life / Linked / Pension & Annuity (the public-disclosure segment) |
| doc_type | policy / brochure / bi / cis / leaflet |
| **source_url** | **the exact URL the file was downloaded from**, so anyone can check it by hand |
| found_on_page_url | the insurer page where the link was found |
| download_date_utc, http_status, sha256, bytes, pages, is_scanned | provenance and integrity |
| file_path, text_path | paths in this repo |
| status | `ok` / `failed` / `manual` / `not_published` |
| notes | anything unusual (version mismatch, redirect, etc.) |

## Document types

- **Policy document** (policy wordings / policy contract): the legal contract filed with IRDAI. It has every definition, benefit formula, surrender value factor, exclusion and annexure. It is the authoritative source for features and calculations.
- **Sales brochure** (prospectus): regulated sales literature. It summarises benefits, eligibility, options and riders, and carries the IRDAI product description line.
- **Benefit illustration (BI):** a projection of benefits for a sample customer. Par and ULIP projections are shown at the IRDAI 4% and 8% rates; non-par shows guaranteed values. Insurers publish these only sometimes.
- **Customer information sheet (CIS) / key features document:** the standard 1–2 page summary given at purchase.
- **Leaflet / one-pager:** short marketing material, kept only when nothing better exists.

## Searching

```bash
grep -ril "return of premium" text/            # which products mention a feature
grep -l "Participating" text/*/*/brochure.txt  # classification check
python3 -c "import csv;[print(r['uin'],r['source_url']) for r in csv.DictReader(open('index.csv')) if r['insurer']=='HDFC Life']"
```

All documents are public regulatory disclosures published by the insurers. Each file's original location is in `index.csv` → `source_url`.
