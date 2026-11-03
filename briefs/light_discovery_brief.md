# Brief: light discovery (brochure pass) for the second session

## Goal
For every in-scope product in `master_list.csv` (633 individual products, 25 insurers):
1. Download its **sales brochure** from the insurer's own website.
2. Read the **IRDAI product description line** printed on it, e.g. *"A Non-Linked, Participating, Individual, Life Insurance Savings Plan"*. This line is how the insurer officially classifies its own product (par/non-par, linked, plan type). It is the whole point of this pass.
3. Run a light keyword scan for headline features.

**Out of scope for this pass:** policy documents, benefit illustrations and deep feature extraction. Download a policy document **only** when no brochure exists, because it carries the same description line.

## Before you start
- **Network:** this account's cloud environment needs the insurer domains allowed **including `www.` subdomains**. Wildcards like `*.hdfclife.com` work, or set access to Full.
  - Quick test: `curl -sI https://www.hdfclife.com/ | head -1` should return 200.
  - The domain list is in the README of the analysis repo (`ahen-can/boom` → `li-category-analysis`), or just allow the 25 insurer domains used in `master_list.csv`'s URLs.
- Read `CLAUDE.md` and `README.md` in this repo. The rules there are mandatory:
  - 1 request/second per domain;
  - the insurer's own site only;
  - **never invent or guess a URL and record it**;
  - keep the original bytes;
  - push one insurer at a time.
- **Do not try to get around bot protection** (captcha or challenge pages). ICICI, Kotak, Star Union Dai-ichi and Go Digit block automated access; they're on the user's manual checklist (`results/manual_checklist_blocked_sites.csv`). Skip them.

## How to run
```bash
git clone https://github.com/ahen-can/li-product-docs && cd li-product-docs
python3 -I scripts/light_discovery.py --insurer bharti-life            # start with one insurer and check the output
python3 -I scripts/light_discovery.py --insurer hdfc-life --dry-run     # shows candidate links without downloading
python3 -I scripts/light_discovery.py --insurer all --skip-blocked      # then everything
```
It's safe to re-run: products already `ok` in `results/light_discovery_results.csv` are skipped.

**What the script does for each product:**
1. Opens the product page (`website_product_page_url` in the master list) and the insurer's seed pages (`SEEDS` in the script).
2. Collects document links: `.pdf` links, or links whose URL or text says brochure, prospectus or policy document. For example, SBI links `/documents/d/sbil/product-brochure-prospectus-12`.
3. Scores the links (product code in the URL or text, product-name words, the word "brochure", links on the product's own page) and downloads the best ones.
4. **Accepts a file only if** it starts with `%PDF` and its text contains the product's **UIN code** (e.g. `101N207`). A different version (V02 vs V03) is kept and noted, never relabelled.
5. Saves `docs/<slug>/<UIN>/brochure.pdf` and `text/<slug>/<UIN>/brochure.txt`, appends a row to `index.csv` (with the exact `source_url` and the `found_on_page_url`), and records the description line, the par flag, linked/non-linked, the plan type as stated, and keyword hits.

**Test run in the main session (18 products from 6 insurers):** 13 found.
- **Working:** Bharti, SBI, ABSLI and Tata's ULIPs found their brochures, with correct description lines.
- **Still to fix:** LIC and older HDFC products weren't found, because no product-page URL is known yet. That is your job below.

## Your job: raise the hit rate insurer by insurer
After the first run, open `results/light_discovery_results.csv` and work through each insurer's `not found` rows:
1. **Find where that insurer keeps product pages or brochures.** Look in its menu, a "download centre / brochures / product documents" page, `sitemap.xml`, or the site search. Patterns seen so far:
   - **SBI:** `/documents/d/sbil/product-brochure-prospectus-NN` links on product pages.
   - **HDFC:** `/content/dam/hdfclifeinsurancecompany/products-page/brochure-pdf/<name>.pdf`.
   - **Bharti:** `/sites/default/files/...` PDFs on product pages.
   - **ABSLI:** the brochures and specimen contracts page lists everything.
   - **LIC:** each plan has its own page under `licindia.in` with a "Sales Brochure" link; find the plan pages from the products menu.
2. Add the page(s) to `SEEDS[slug]`, or fill `website_product_page_url` in `master_list.csv` for those rows (only with real URLs you opened), then re-run that insurer.
3. When a product genuinely has no brochure online, try the **policy document** (the script stores it as `policy.pdf`; its description line is just as valid). If neither exists, leave it `not found` with a short note on where you looked.
4. **Scanned PDFs** (`is_scanned=Y`): OCR them (`ocrmypdf` or `tesseract`), re-extract the text and the description line, and note it.
5. **Spot-check 2 products per insurer by hand:** open the PDF and confirm the description line and UIN are right.

## Commit and push (one insurer at a time)
```bash
git add docs/<slug> text/<slug> index.csv results/ master_list.csv scripts/light_discovery.py
git commit -m "Light discovery: <insurer> brochures (<n> ok, <m> not found)"
git push origin main
```
Keep each push well under 2 GB, and never add a single file over 95 MB.

## What to hand back (the main session uses these)
1. **`results/light_discovery_results.csv`**, one row per product: status, doc_type, source_url, found_on_page_url, uin_in_document, **irdai_description_line**, par_flag_stated, linked_stated, plan_type_stated, pages, features_keyword_hits, notes.
2. **`results/manual_checklist.csv`**: the products you couldn't get, each with where you looked.
3. **A short summary in `results/light_discovery_summary.md`:**
   - counts per insurer (ok / not found / manual);
   - any description lines that look odd;
   - any document whose UIN version differs from the master list;
   - site quirks worth knowing for the deep pass (where policy documents and BIs live).

## Don'ts
- Don't set `market_category` or `pd_category`; the main session maps those from the description line.
- Don't classify anything from the product name.
- Don't download from aggregators (PolicyBazaar etc.) or document-sharing sites.
- Don't download withdrawn products' documents.
