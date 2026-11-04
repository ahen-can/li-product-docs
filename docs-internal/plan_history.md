# Plan: Phase 2 — Bharti trend analysis, product master list, feature lists, product scoring and IRR

## Context
Phase 1 is done: the category workbook covers 25 insurers' FY26 premium. The user's colleagues now want a **"feature list"** Excel. To support it, we need:
- a master list of every individual product across all insurers, mapped to the market categories;
- a feature list per category, built from the actual policy documents and brochures;
- a comparison of products against those features;
- a consulting-style framework to pick the top products;
- an IRR comparison of those products for a standard customer profile.

There is also a side analysis of Bharti's history (FY21–FY26).

**Decisions so far**
- **Market categories:** "Investor-deck 5", namely **Protection, Non-Par Savings, Par, ULIP and Annuity**. Pension products are mapped by their construction: ULIP pension goes to ULIP, non-par deferred pension to Annuity (retirement), and par pension to Par. Each product also keeps its PD category (Par Life / Non-Par Life / Linked / Pension & Annuity).
- **Peer sets:** the leaders, plus Bharti's size peers, plus innovators. The user is right that innovators can only be spotted by scanning **all** products, so we do a light scan of everything and a deep feature extraction on a selected set.
- **Document access:** the user will allowlist domains (instructions below). The fallback is uploads.

## Fixes to phase 1 (do first)
- "INLIC" is **IndusInd Nippon Life** (per the Life Insurance Council list), not "Nippon India Life". Rename it in the workbook and push.

## Workstream 1: Bharti trend analysis (FY21–FY26)
**Data in hand**
- L-1 segment premium for FY21, FY22, FY23 (from the FY22 and FY23 PDs) and FY25, FY26 (from the FY26 PD).
- L-22 ratios: linked share of individual new business premium (NBP), and segment-wise NBP growth.

**Pending from the user:** the FY24 Q4 PD and the FY24–FY26 annual reports.

**Early findings** (check these with the user's hypothesis):

| Measure | FY21 | FY22 | FY23 | FY25 | FY26 |
|---|---|---|---|---|---|
| Linked % of individual NBP (L-22) | 22.6% | 16.3% | 12.5% | 25.0% | **33.0%** |
| Linked % of total premium | 11% | 10% | 9.5% | 12.7% | 17.3% |
| Par % of total premium | 38% | 33% | 27% | 23% | **19%** |
| Non-par individual life % of total premium | 45% | 50% | 55% | 60% | 58% |

- The ULIP rise is real: linked went from about 10% to 17% of total premium, and from about 12.5% to 33% of new business.
- **Non-par did not halve. Par is the shrinking book:** par NBP fell 24.7% in FY26.
- Non-par NBP fell 15.8% in FY25, then grew 37.2% in FY26. Non-par pension is growing from a tiny base.
- Group premium went 129 → 172 → 211 → 90 → 131 (₹ cr), so the group book shrank sharply in FY25.

**Analyses**
- Segment mix trend, both total premium and NB mix.
- Conservation (persistency proxy) by segment. Linked conservation fell to 74% in FY26 from 75% in FY25. Non-par fell to 77% from 82%.
- Single premium share, commission ratio and channel mix (L-5 / L-38).
- Peer comparison of the same metrics for the FY26 peer set, which we already have.

**Output:** a new "Bharti Trend" tab with charts, and observations citing PD and annual report pages.

## Workstream 2: Master product list (individual products only)
**Scope:** exclude group, health, riders and micro-insurance.

**Backbone:** the Life Insurance Council "In-Force Products, Sep-2026" PDF. It has about 1,040 rows with insurer, product, individual/group, a self-reported category and the UIN.

**Gaps in the Council list**
- It shows **0 individual products** for SBI Life, Bajaj Life, Edelweiss Life and Canara HSBC.
- Its category field is free text (e.g. "Endowment", "Savings", "Traditional") and mostly does **not** say par or non-par.
- It still lists Exide Life, which has merged into HDFC Life.

**How each product gets classified, and how we confirm the insurer's own definition**
1. **UIN code:** the 4th character is **L = linked**, **N = non-linked**. For example, 109**L**149V01 is a ULIP. This is mechanical and authoritative.
2. **IRDAI product description line:** every brochure and policy document must open with it, e.g. "A Non-Linked, **Participating**, Individual, Life Insurance **Savings** Plan". This is the insurer's own classification. It gives par vs non-par and protection vs savings vs annuity/pension, and it's the confirmation the user asked about.
3. The Council category is used only as a cross-check.
4. Fill the gaps (SBI, Bajaj, Edelweiss, Canara HSBC) from each insurer's website **"List of products"** page. IRDAI requires insurers to publish all current and withdrawn products with UINs. Cross-check against IRDAI's product list where available.

The PDs do **not** list products, so they can't confirm the categories. They only report segment totals.

**Master list columns:** Insurer, Product, UIN, Linked/Non-linked (from UIN), Par/Non-par, IRDAI description line, Council category, Market category (5), PD category (4), Sub-type (term with return of premium, whole life, child, guaranteed income…), Launch/version, Online/offline, Brochure URL, Policy document URL, Document status.

## Workstream 3: Document collection
**Scale:** about 450 individual products, each with a brochure and a policy document, so about 900 PDFs. Typical size is 0.3–3 MB, about 1–2 GB in total. Session disk is limited, so we store text extracts plus a selected set of PDFs, not everything.

**Feasibility**
- With the domains allowlisted, a script can scrape each insurer's product page and download the PDFs.
- About 60–70% of insurers have predictable links. The rest use JavaScript-rendered sites or bot protection, which the headless Chromium already in the session can partly handle.
- Expect about 70–85% automated coverage. For the rest I'll give the user a precise manual-download checklist.

**Two-pass approach**
1. **Light scan of all products:** brochure only. Extract the description line, key features, riders and options with a keyword and section parser. This classifies every product and flags innovators.
2. **Deep extraction for the selected set** (about 15–25 products per category): the policy document and brochure, plus the benefit illustration where available.

## Workstream 4: Feature list Excel (one tab per market category)
- Features come from the policy documents of leaders plus innovators, and are grouped into:
  - eligibility and terms (age, policy term, premium payment term, minimum sum assured / premium);
  - benefit structure;
  - flexibility (premium holiday, partial withdrawal, switch, top-up);
  - payout options;
  - riders;
  - special features (return of premium, zero-cost exit, life-stage increase, spouse cover, critical illness / terminal illness acceleration, waiver of premium, loyalty additions, guaranteed additions);
  - charges (ULIP);
  - surrender (GSV/SSV);
  - claim and service.
- Comparison matrix: products × features (Y/N, value), with citations to the document and page.

**Peer selection rationale per category, documented in the sheet**
- the 9 common leaders, plus the category's #10;
- 2–3 Bharti size peers (Shriram, Pramerica, Generali Central, Ageas Federal, Canara HSBC, PNB MetLife, IndiaFirst…);
- 2–3 innovators flagged by the light scan, e.g. a feature that appears in fewer than 10% of products, or a recent launch.

## Workstream 5: Product scoring and IRR
**Weighted scorecard**, consulting style:
- Feature richness: 25%
- Customer value (IRR or premium competitiveness): 30%
- Market traction: 20%
- Flexibility: 15%
- Innovation: 10%

These are the default weights; the user tunes them.

**Traction data and its limits**
- Product-level sales are not in the PDs.
- Bharti publishes a product-level **"Product Performance"** disclosure on bhartiaxa.com (KPI disclosures section; the file is titled "Product Performance FY24 – YTD Jul FY27").
- Check whether peers publish the same disclosure.
- Otherwise use these proxies: flagship products named in investor decks or annual reports, online-aggregator bestseller tags, and the product's version count and age.

**IRR approach**

| Category | Approach | Feasibility |
|---|---|---|
| Protection | No IRR. Compare annual premium for 1 cr cover and the cost per lakh of cover. Return-of-premium variants do get an IRR. | Premiums come from insurer online calculators or PolicyBazaar. Premium rates aren't in the policy documents. |
| Non-Par Savings | Exact IRR from guaranteed cash flows. | The benefit formulas are in the policy document. Some guaranteed rates come from premium tables that aren't published, so the BI or calculator is needed. |
| Par | IRR at the IRDAI 4% and 8% illustration rates. | Uses the BI. Bonuses are non-guaranteed. |
| ULIP | Own calculator: premium allocation, policy admin, mortality and fund management charges from the policy document, at 4% and 8% gross. Validated against one official BI per product. | This is where our own calculator works fully. |
| Annuity | Annuity rate per ₹10 lakh purchase price → IRR, for joint life with return of purchase price etc. | Rates come from the insurer's online quote. |

**Standard profiles (proposed, to confirm)**
- **Protection:** 30-year-old male, non-smoker, salaried ₹10 L, ₹1 cr cover to age 70 (40-year term), regular pay, annual premiums.
- **Savings, Par and ULIP:** same person, ₹1 L annual premium, 10-year premium payment term, 20-year policy term.
- **Annuity:** 60-year-old, ₹10 L single premium, life annuity with return of purchase price.

**Calculator:** a Python model, mirrored as an Excel calculator tab with formulas.

## Document types (for the user)
- **Policy document (policy wordings / contract):** the legal contract filed with IRDAI. It contains all definitions, benefit formulas, surrender value factors, exclusions and annexures, and it is needed for the calculator.
- **Sales brochure / prospectus:** IRDAI-regulated sales literature. It summarises features, eligibility, options, riders and sample illustrations, and it carries the product description line.
- **Leaflet / one-pager / flyer:** short marketing material. It's the least detailed and is not used for analysis.
- **Benefit illustration (BI):** a personalised projection at 4% and 8% for par and ULIP products, or the guaranteed values for non-par. It is mandatory at sale and is the key input for the IRR.
- **Customer information sheet / key features document:** a standard 1–2 page summary given at purchase.

## Instructions for the user: allowlisting on Android
1. Open the session at **claude.ai/code** in Chrome on the phone (switch to "Desktop site" if the menu doesn't appear). Go to the environment selector on the session's top bar, then **Edit environment**, then **Network access**. Environment settings may not be editable in the Android app itself.
2. **Simplest option:** set access to **Full** temporarily. Insurer PDFs often sit on CDN subdomains, so a precise list will still miss some.
3. **Otherwise:** choose **Limited / Custom**, keep "Allow package managers" ticked, and add these under Allowed domains (`*.` wildcards where supported):
   - **Insurers:** licindia.in, sbilife.co.in, hdfclife.com, iciciprulife.com, axismaxlife.com, maxlifeinsurance.com, tataaia.com, bajajlifeinsurance.com, bajajallianzlife.com, adityabirlacapital.com, kotaklife.com, insurance.kotak.com, pnbmetlife.com, canarahsbclife.com, indiafirstlife.com, sudlife.in, indusindnipponlife.com, reliancenipponlife.com, shriramlife.com, ageasfederal.com, generalicentrallife.com, futuregenerali.in, bhartiaxa.com, bhartilife.com, edelweisslife.in, pramericalife.in, avivaindia.com, bandhanlife.com, godigit.com, acko.com, creditaccesslife.in.
   - **Regulators, exchanges and aggregators:** irdai.gov.in, lifeinscouncil.org, nseindia.com, nsearchives.nseindia.com, bseindia.com, maxfinancialservices.com, policybazaar.com.
4. Start a **new session** after saving if this one still can't reach the sites. Steps: https://code.claude.com/docs/en/cloud-environments#network-access

## Working mode (user instructions, 3 Nov)
- **Go one task at a time and check in after each.** Accuracy and thoroughness come before speed. Ask doubts as they come up.
- **Split of work**
  - **This session:** the light scan of all products, the master list, and classification. It also writes a **deep-extraction brief** (`li-category-analysis/deep_extraction_brief.md`) with the exact product list, documents, feature schema, the citation rule and the output format. The user's second Claude account runs it, possibly overnight.
  - **The deep extraction results come back to this session** for the feature Excel, the scorecard and the IRR work.
- **Network status (tested 3 Nov)**
  - The bare domains now work: licindia.in, irdai.gov.in, hdfclife.com, sbilife.co.in, bhartiaxa.com, lifeinscouncil.org.
  - **`www.` subdomains are still refused**. Almost every insurer redirects to www, so the user must add wildcard entries (`*.hdfclife.com`) or `www.` entries, or set access to Full. bseindia.com is still refused.
  - The allowlist change took effect in this session without a restart, so no new session is needed.
- **New input:** Bharti AXA FY25 audited financial results (Reg. 52, 12 scanned pages, read as images).
  - It has FY24 comparatives, which partly fill the FY24 gap.
  - Note 5: the **EoM limit was exceeded in FY25** and Bharti applied for forbearance.
  - The FY24 PD and annual reports will be uploaded later by the user.

## Policy document repository (user request)
**Goal:** a git repo holding every obtainable brochure, policy document, benefit illustration (BI) and customer information sheet (CIS) for individual products (excluding group, health, riders and micro), with an index and a guide. Any session can then read the full documents on demand.

**Repo**
- A new **private** GitHub repo, e.g. `ahen-can/li-policy-docs`, created by the user. This session can't create repositories. It gets attached here with `add_repo`, and the second account gets push access as a collaborator.
- Layout:
```
README.md                  guide: what's here, how to search, document types, coverage gaps
index.csv                  one row per document: insurer, product, UIN, linked/par flags, market category (5),
                           PD category, doc_type (brochure|policy|BI|CIS|leaflet), source URL, download date,
                           sha256, pages, file path, text path, status (ok|failed|manual)
coverage.md                per insurer: products in master list vs documents found; manual-download list
docs/<insurer>/<UIN>/<doc_type>.pdf
text/<insurer>/<UIN>/<doc_type>.txt     pdftotext -layout output (OCR if scanned) — searchable with grep
scripts/download.py        reads master_list.csv → finds/downloads documents → writes index rows
scripts/extract_text.py
```

**Size and limits**
- About 450 products × 2–4 documents ≈ 1,200–1,800 PDFs, around 1–2.5 GB.
- GitHub limits: each file under 100 MB (fine), and each push must stay **under 2 GB**, so the agent commits and pushes **per insurer**.
- No Git LFS (the free quota is 1 GB).
- Sessions read the `text/` folder plus `index.csv` via sparse checkout, which is a small download, and pull individual PDFs only when needed (e.g. annexure tables).

**Who does what**
1. **This session** builds `master_list.csv`, with product, UIN and the official product-page URL where known, plus `download.py` and the brief, and commits all of them to the docs repo.
2. **The second account** runs the download per insurer. It fixes site-specific scrapers (headless Chromium for JS/bot-protected sites), OCRs scanned PDFs, pushes in batches and records failures in `coverage.md`.
3. **The user** hand-downloads the leftover failures listed in `coverage.md`.
4. **The second account** then runs the deep extraction from the repo (brief: `deep_extraction_brief.md`) and commits `features/<category>.csv` with document and page citations.

**Network:** the second account's cloud environment needs the **same allowlist, including `www.`/wildcard entries**, because each account has its own environment settings.

**Legality / visibility:** these are public regulatory documents, but redistributing them publicly is unnecessary, so the repo stays private.

**Decisions (3 Nov)**
- The user creates a private repo (e.g. `ahen-can/li-policy-docs`) and adds the second account as a collaborator. This session attaches it with `add_repo`.
- **Target:** policy document + brochure for **every currently active individual product in scope**, with BI/CIS wherever the insurer publishes them. Withdrawn products are left out, which keeps the volume at ~1,000–1,500 files.
- Success claim: "100% of in-scope active products have a policy document and brochure, or are listed in `coverage.md` as manual/unavailable."
- The second account does the downloading and deep extraction.

**Update (3 Nov, later)**
- Repo created: **https://github.com/ahen-can/li-product-docs** (currently public). Recommend switching it to private before PDFs are pushed. Not a blocker.
- `index.csv` must record the **exact source URL** of every file (plus the product-page URL it was found on), so the user can cross-check by hand.
- **The Bharti trend analysis is deferred** until the user uploads the FY24 PD and annual reports.
- **Scraper instructions:** no special skill is needed. The brief will give the second agent:
  - a ready `download.py` (requests + headless Chromium/Playwright fallback, which is pre-installed in cloud sessions);
  - per-insurer notes from my light scan (product-page URL patterns and quirks);
  - rules: polite rate limit, verify PDF magic bytes, sha256 dedupe, record failures, never invent URLs.

## Master list v2: website-first (user direction, 3 Nov)
**Rules from the user**
- The **insurer's website is the absolute truth**. The Council list (Sep-2026) is the cross-check.
- **Drop the IRDAI list** as a source. The user checked Bharti's 11 "IRDAI-only" products and all of them were withdrawn; many appear on Bharti's withdrawn-products page. Keep the IRDAI files in `sources/` for the record, but don't use them in the master list.
- **No category from product names.** A category is filled only when officially stated: the website's product classification, the Council category, or the brochure's IRDAI description line. Otherwise leave it blank for the light-discovery pass.
  - Remove the name-based rules from `build_master.py`. The fields become `category_council` (verbatim), `category_website` (verbatim, if the site states one) and `linked_flag` from the UIN (official: the regulator's code).
- **ICICI caveat:** after Prudential's exit the products were renamed (ICICI Life), and some still say "Pru". The website name wins.
- Report every **discrepancy** between the website and the Council list, and which websites couldn't be read.

**Inputs**
- Council list: use the user's `.xls` export (`/root/.claude/uploads/42c9e8ea-081f-5f5b-9023-52021c0c1d32/f94d6678-ProductsandRiders.xls`). It is really an HTML table, so it parses with no line-wrap problems. Re-parse it and verify the result matches the PDF parse (594 individual products).
- **Per insurer, from its website:**
  1. the "all plans" / products page (current products, names and UINs where shown);
  2. the IRDAI-mandated **product list / UIN list** page, often a PDF or table of current and withdrawn products and riders;
  3. the **withdrawn products** page.
  - Record every page URL used.

**Method (one insurer at a time, 1 request/sec)**
- Find the pages by crawling the site's nav and footer links and its sitemap.xml for keywords: "all plans", "products", "UIN", "withdrawn", "discontinued", "list of products".
- Use curl first, then headless Chromium for JS-rendered pages.
- Extract name and UIN. Tables and PDFs get parsed; plain product cards (name without UIN) are matched to Council rows by name, with any uncertain match flagged.
- Save the raw page HTML/PDF snapshots to `sources/websites/<insurer>/` with fetch date and URL, for audit.

**Known blocked sites (tested 3 Nov):** ICICI Life (icicilife.com and iciciprulife.com), Star Union Dai-ichi (sudlife.in) and Go Digit (godigit.com). They return 403 "Access Denied" to both curl and headless Chromium, because their firewalls block cloud-server traffic.
- Options:
  - (a) the user saves those pages (or the UIN-list PDFs) from their browser and uploads them;
  - (b) connect Claude in Chrome / Remote Control so the pages load from the user's own network.
- For now, mark them as "website not readable" and keep the Council data, flagged as such.

**Outputs, all in `li-product-docs`**
- `sources/websites/website_products.csv`: one row per product found on a website.
  - Columns: insurer, product name (site), UIN, status (current/withdrawn), category stated by the site (verbatim), page URL, page type (all-plans / UIN list / withdrawn list), fetch date.
  - Also published as `website_products.xlsx` with one tab per insurer plus a summary tab.
- `master_list.csv` v2. Membership: website-current products, plus Council products missing from the website (flagged).
  - Columns: in_website, in_council, website_status, category_council, category_website, linked_flag (UIN), discrepancy note, source URLs.
  - Category columns are filled only from official statements.
- `sources/websites/discrepancies.csv`, with these types:
  - on the Council list but not on the website;
  - on the Council list but on the website's **withdrawn** list;
  - on the website but not on the Council list;
  - UIN version differs;
  - name differs (e.g. the ICICI renames).
- `sources/websites/coverage.md`: per insurer, which pages were read, counts, and **which sites could not be read**.

**Check-in point:** after all websites have been attempted, report counts per insurer, the discrepancies, the unreadable sites and what's needed from the user. Brochure downloading and the decisions still open from the last message (who downloads brochures; standard/POS products) wait for that report.

## CHECKPOINT (4 Nov): where we are
**Done**
1. Phase 1 category workbook: 25 insurers, FY26, in `boom/li-category-analysis/`.
2. `li-product-docs` repo: scaffold, rules, sources.
3. Master list v1 (Council + IRDAI), now superseded.
4. Master list v2: website check of all sites (`sources/websites/`).

**Finding from the user's official ICICI and Bharti lists:** the Council list is accurate.
- Bharti: 26 of 26 exact.
- ICICI: 37 of 38 exact, plus 1 newer version (105N205V08) and 1 new product (105N226V02, Guaranteed Indexed Pension).
- The only systematic difference is ICICI's rename from "ICICI Pru" to "ICICI Life".
- Most website-scrape discrepancies are scraper noise: stale or legacy pages, missed menu items.

**Decision proposed:** the backbone is the Council list (Sep-2026), with these patches:
- (a) the insurer's official list where provided (ICICI and Bharti now; others if found);
- (b) SBI and Bajaj from their websites, since the Council list has no individual products for them;
- (c) names as on the insurer's site (ICICI renames).
- No more scraping effort on the website-vs-Council comparison. Keep the v2 files as an audit trail only.

## Next steps (to confirm with the user)
1. **Master list v3:** Council individual products, plus the patches above.
   - Scope filter uses only the **Council's own category labels**: exclude Health, Accident and Micro, riders (UIN B/A), and G/Y codes.
   - Keep Saral/POS products, tagged.
   - Output `master_list.csv` and xlsx in `li-product-docs`.
2. **Light discovery = brochure pass.**
   - For each in-scope product, find its brochure on the insurer site (the product page's documents link), download it into `docs/<insurer>/<UIN>/brochure.pdf` with its source URL, and extract text.
   - Capture the IRDAI description line, giving **par/non-par and the plan type the insurer itself states**. Map it to the 5 market categories and the 4 PD categories.
   - Also note headline features with a keyword scan, to flag innovators.
   - Blocked sites (ICICI, Kotak, SUD, Go Digit): the user or second account downloads by hand from a checklist.
3. **Peer and innovator shortlist per category.** Uses size (phase-1 shares), the specialist index (category share of an insurer's book vs the industry; user's idea), Bharti's size peers, and innovators from the brochure scan. Each choice gets a written rationale.
4. **Deep-extraction brief** for the second account: policy documents and BI/CIS, a feature schema per category, page citations.
5. Feature list Excel, then comparison, scorecard, IRR.
6. **Deferred:** Bharti trend analysis, waiting on the FY24 PD and annual reports.

## Decisions (4 Nov checkpoint)
- **Backbone:** Council + patches. That means the official ICICI and Bharti lists (the user's xlsx, tabs `icici` and `bharti`; individual products only, current section), SBI and Bajaj from the websites (`sources/websites/website_products.csv`, status current), and names as on the insurer's site. No more website-vs-Council scraping.
- **Scope:** exclude Health, Accident and Micro (Council labels only), riders (B/A) and govt/combi (G/Y). Keep Saral/POS, tagged with `standard_or_pos` from the official name text ("Saral", "POS"). That tag is a label, not a category.
- **Light discovery runs in the user's second session.** This session writes the brief and script; the second session executes and pushes. Deep extraction comes later.
- **Blocked sites:** ICICI, Kotak, SUD and Go Digit go on a manual checklist for the user. If the brochures can't be obtained, skip them and keep only the Council label.

## Immediate work (this session)
1. **Build master list v3.**
   - Read `sources/life-council/council_rows_parsed.csv`, which is the xls parse.
   - Apply the ICICI and Bharti official lists: add 105N226V02, set 105N205 to V08, use ICICI Life names. Bharti matches exactly.
   - Add SBI and Bajaj products from the website rows with status current, excluding anything not N/L.
   - Apply the scope filter.
   - Columns: insurer, slug, product_name, uin, product_code, linked_flag, council_category (verbatim), source (council / official list / website), standard_or_pos tag, website_product_page_url (from the v2 evidence where available), plus empty columns for the brochure pass: brochure_url, irdai_description_line, par_flag, market_category, pd_category, notes.
   - Write `master_list.csv` and `master_list.xlsx`, and save the user's xlsx in `sources/official-lists/`.
2. **Write `briefs/light_discovery_brief.md` and `scripts/light_discovery.py`** for the second session.
   - **Input:** `master_list.csv`, plus the v2 product-page URLs as the starting point.
   - **Per product:**
     - open the product page (or search the insurer's site and sitemap) and find the **brochure / sales literature PDF**;
     - download it to `docs/<slug>/<UIN>/brochure.pdf`;
     - check it: `%PDF` header, `pdfinfo`, UIN present;
     - extract text to `text/…/brochure.txt`, OCR if scanned;
     - parse the **IRDAI description line** and a 1st-page summary;
     - run a keyword feature scan: return of premium, whole life, limited pay, single pay, income options, loyalty additions, rider list, ULIP fund count, etc.;
     - append a row to `index.csv` with `source_url` and `found_on_page_url`, and fill the master list's brochure columns.
   - **Rules:** follow `li-product-docs/CLAUDE.md` (1 req/s per domain, never invent URLs, push per insurer).
   - **Stop conditions and reporting:** `coverage.md`, plus `manual_checklist.csv` for anything not found.
   - **Output for this session:** `light_discovery_results.csv`, which I then use to set `market_category` and `pd_category` from the description line, and to shortlist peers and innovators.
3. **Write `manual_checklist_blocked_sites.csv`** for the user: ICICI, Kotak, SUD and Go Digit products, each with UIN, name and the insurer's products page URL to visit.
4. Commit and push to `li-product-docs`, then report to the user with the exact message to paste into the second session.

## RETHINK (4 Nov, after light-discovery hand-off): how to proceed to the end goal
**End goal:** a market landscape of individual life products, then a nuanced analysis of Bharti's product suite (gaps, missing categories, features peers have that Bharti lacks, "best ideas" even from LIC). Two deliverables: a **feature-list Excel per category** and a **short PPT deck**.

The user's reference slides compare a client's product with 5 peers' flagship products per category:
- **ULIP:** AUM, fund switching, policy admin charges, fund management charges, partial withdrawal charges, premium allocation charges, payment modes.
- **TULIP (ULIP with protection):** fund ratings, premium allocation charges, policy admin charges, fund management charges, return of mortality charges, return of premium allocation charges, loyalty bonus.
- **Protection:** yearly premium for a standard profile, maximum maturity age, minimum and maximum term, payment modes, minimum sum assured.
- Green cells mark the best in class.

**Recommended route: breadth first, then depth, anchored on Bharti**
1. **Landscape (breadth), right after light discovery, using all ~630 products.**
   - Map each product to the 5 market categories plus sub-segments from its official description line. Examples:
     - **Protection:** pure term, return of premium term, whole-life term, women-specific, credit/loan, Saral.
     - **Non-par savings:** guaranteed income, guaranteed maturity, whole-life income.
     - **Par:** endowment, money back, whole life, child.
     - **ULIP:** wealth, ULIP with protection (TULIP), pension, child.
     - **Annuity:** immediate, deferred, Saral Pension.
   - **Output: Landscape tab plus 2–3 slides.**
     - Insurer × sub-segment product grid, showing **where Bharti has no product** (e.g. annuity, ROP or whole-life term).
     - Feature-prevalence matrix from the keyword scan: "% of products in the category offering X", against "Bharti has / doesn't".
     - The category shares from phase 1 as market context.
2. **Feature list v1 (schema), also after light discovery.**
   - Draft each category's feature list from the brochures of about 5–8 leaders, one innovator and Bharti. Brochures cover most rows (terms, ages, payment options, payout options, riders, loyalty and guaranteed additions, and for ULIPs usually the charges).
   - Rows are grouped: eligibility and terms, premium payment, benefit design, flexibility, riders/add-ons, charges (ULIP), customer value (premium/IRR), plus market data (AUM, ratings, claims).
   - The schema grows as new features are found, so the deep pass is only needed for exact values.
3. **Comparison set: compare products, not companies.**
   - Per category or sub-segment: **Bharti's product, plus about 7–9 peer products.**
   - Peers: the flagship product of each top player by phase-1 category premium; 2–3 of Bharti's size peers; 1–2 innovators picked from the landscape scan using the specialist index.
   - **LIC appears as a separate "reference / best ideas" column**, not a peer.
   - Like-for-like: Bharti's ROP term is compared with peers' ROP term, not their pure term.
   - "Flagship" = the product the insurer itself features (investor deck, "top selling" tag, homepage), else its latest version. The reason for each pick is written down.
4. **Deep extraction for the comparison set only** (second session).
   - Policy documents and brochures (BI where needed), for about 8–10 products × 6–8 sub-segments, so roughly 60–80 products.
   - Fill the feature matrix with exact values and page citations.
   - Flag the best in class (green, as in the user's slides) and **Bharti's gaps**.
5. **Pricing and returns.**
   - **Protection:** premium for the standard profile, from insurer online quotes (manual) or the user's contacts.
   - **ULIP:** our charges calculator → net yield at 4% and 8%.
   - **Non-par savings:** IRR from the BI or guaranteed tables.
   - **Par:** BI at 4% and 8%.
6. **Deck** (about 10–14 slides).
   - Market context (phase 1).
   - Landscape and white space.
   - One comparison table per category (the user's slide format).
   - Bharti summary: gaps, strengths, "borrow from LIC/innovators" ideas, and pricing position.

**Data not available from PDs or brochures** (the user sources these via contacts, or we mark them n/a):
- **Product-level sales or AUM:** PDs give insurer-level linked AUM only (L-14 / L-27 fund-level). Bharti's product-performance file is the exception.
- **Fund ratings:** Value Research / Morningstar.
- **Premium quotes:** insurer calculators or aggregators.
- **Product-level persistency and claims:** PDs give only insurer-level claim settlement (L-39) and persistency.
- **Channel mix by product.**

**Alternative routes (not recommended)**
- *Bharti-anchored only:* start from Bharti's 26 products and find each one's nearest peers. Faster, but it gives no true landscape and misses categories where Bharti has nothing.
- *Exhaustive deep extraction (all ~630 products):* the most complete, but slow and costly, and the deck only needs the comparison set.

**Decisions (4 Nov)**
- **Route:** breadth, then depth.
- **Feature list:** v1 right after light discovery; final values after the deep pass.
- **Comparison set size:** decided later. 7–9 peers is fine where they make sense; otherwise use the slide format (Bharti + 5).
- **Deck:** PPT, built later.
- **Blocked sites:** the user adds docs manually tomorrow; leave blank for now.
- **Bharti's 26 brochures:** pushed by the second session on a separate branch, which is fine.

**IRR calculator: a PolicyBazaar-style tool, a key value-add (user request, 4 Nov)**

Feasibility by category:

| Category | Result | Why |
|---|---|---|
| Non-par savings | **Exact** | Benefits = premium × factor tables in the policy document. |
| ULIP / TULIP | **Exact at stated gross returns** | Charges and mortality tables are in the policy document. |
| Par | Indicative | Published bonus rates or the 4%/8% illustration basis. |
| Annuity | Partial | Sample rates are sometimes published. |
| Pure term | Premium comparison only | Needs quotes. |

**Design**
- **Engine:** `calc/engine.py`, cash flows → IRR, with mechanics modules for guaranteed income, guaranteed maturity, ULIP fund projection and par bonus scenarios.
- **Parameter files:** `calc/params/<UIN>.json`, holding eligibility limits, factor tables and charges. Each value cites the document and page.
- **Excel front end:** inputs are age, gender, premium, premium payment term, policy term and the products chosen. Outputs are a benefits schedule, cash flows and IRR, side by side.
- **Check:** each product's result is reconciled against its official BI before it's used.

**While the second session runs (this session):** build the engine and a pilot.
- Pilot: 2 Bharti non-par savings products plus 2–3 peers in the same sub-segment. Bharti's brochures are on the second session's branch; their policy documents are fetched as needed.
- Then add the ULIP calculator.
- In parallel: draft the sub-segment taxonomy and feature-list v1 schema, and pull the PD market-data columns (insurer ULIP AUM from L-14, claim settlement from L-39).

**Go-ahead (4 Nov):** start the IRR calculator pilot and the taxonomy + feature-list v1. Profiles are sensible defaults per product type and stay editable in the calculator:
- **Savings:** 35-year-old, ₹1L a year, 10-year premium payment, 20-year policy term (or the nearest allowed combination).
- **ULIP:** 30-year-old, ₹1L a year, 10-year premium payment, 20-year policy term.
- **Annuity:** 60-year-old, ₹10L.
- **Term:** 30-year-old male non-smoker, ₹1 cr cover, 30-year term.

**Steps**
1. Fetch the second session's branch (Bharti brochures), pick 2 Bharti non-par guaranteed products, download their policy documents and any published BIs, and pick 2–3 peers in the same sub-segment (e.g. HDFC Sanchay Plus, SBI Smart Platina Assure/Plus, Axis Max Smart Wealth Advantage Guarantee), confirmed from their description lines.
2. Write the engine, the parameter files and the Excel front end, checked against each product's BI.
3. Draft the taxonomy and feature-list v1 in `li-product-docs/analysis/`.
4. Check in with results.

**Pausing here.** The next action, when the user resumes, is to pull the light-discovery results (including the branch) and run step 1, the landscape.

## NEXT TASK (user asleep, resumes tomorrow): taxonomy + feature list v1 from the 194 brochures
**Context:** the second session's branch `ccr-d0d84e00-joo2mp` (worktree `/home/user/ld-branch`) holds 194 brochures with text and description lines: Bharti, LIC, SBI, HDFC, Generali Central and Tata AIA. The user wants:
- the taxonomy and feature list v1 drafted from these;
- a **log of the brochures used** in this iteration, so the next one skips them;
- for every feature: **how many products have it**, and a **range or bands of values**. Be thorough and record every detail found.

**Steps**
1. **Classify each product** from its official description line plus brochure text (never the product name) into the market category (5), the PD category (4) and a sub-segment.
   - **Protection:** pure term, ROP term, whole-life term, credit/loan, Saral.
   - **Non-par savings:** guaranteed income (immediate or deferred), guaranteed maturity, whole-life income, child.
   - **Par:** endowment, money back, whole life, income, child.
   - **ULIP:** wealth, protection-oriented (TULIP), pension, child.
   - **Annuity:** immediate, deferred, Saral Pension.
   - Each rule is written in `analysis/taxonomy.md` with the text cue it relies on. Ambiguous cases get flagged, not guessed.
2. **Define the feature schema per category.** Groups: eligibility (entry age, maturity age, policy term, premium term, minimum premium / sum assured); premium modes; benefit design; payout options; riders; flexibility; charges (ULIP); special features (ROP, spouse cover, life-stage increase, terminal illness / critical illness, waiver of premium, zero-cost exit, loyalty/guaranteed additions, bonus types, discounts); surrender.
3. **Extract per brochure.**
   - Section-aware regex and table parsing for the numeric fields: ages, terms, minimums, charge percentages, fund counts.
   - A keyword plus context check for the yes/no features.
   - Each value is stored with an evidence snippet and the page number.
   - I read in full every Bharti brochure (26) and about 2 per sub-segment for the leaders, to calibrate and correct the extractors.
   - Low-confidence values are flagged, never silently filled.
4. **Outputs** in `li-product-docs/analysis/`, committed to `main`:
   - `taxonomy.md`;
   - `product_features_v1.csv`: product × feature, value, evidence, page, confidence;
   - `feature_list_v1.xlsx`: one tab per category. Rows are features, with definition, count of products with the feature (n / N), value range and bands, example products, and **whether Bharti has it**, plus a summary tab of sub-segment coverage by insurer, showing Bharti's white space;
   - `brochures_used_log.csv`: UIN, insurer, sha256, source_url, iteration = v1, date.
5. **Verification:** re-read 10% of the extracted values against the PDF text; counts reconcile with the classified product set; every "Bharti has / lacks" claim is backed by evidence.

## PLAN (4 Nov, after feature list v1): ULIP end-to-end, get session 2 moving first
**Context:** the light discovery is done: 516 of 633 products, a 97.9% hit rate on readable sites. The second session's `results/light_discovery_summary.md` and `site_quirks.md` give per-site document locations, odd description lines, 30 version mismatches, 13 HDFC products that may be withdrawn, and a list of scope questions.

The user wants:
- a ULIP end-to-end pilot to show Neha;
- a deep-discovery brief for session 2 right away;
- a "for your attention" folder and a seniors' questions doc;
- a coordination ("chat") file between the sessions;
- a QA pack for Rahul;
- a selection framework;
- later, a product-comparer front end and a ULIP observation deck.

**Priority order (do in this order)**
1. **ULIP deep-discovery brief + product set** for session 2, so it can start now with the accessible leaders.
2. **Coordination file** (`coordination/CHAT.md` on main): an append-only log, newest at the top. Each entry has date, author (S1 = main session, S2 = second session, USER), status, asks and answers. Both sessions read it before starting work and append when they finish a step. S2 works on its branch, so it appends to the same file on its branch, and S1 merges S2's branch into main periodically (needs the user's OK).
3. **`for-your-attention/` folder:**
   - `00_ACTIONS.md`: a numbered checklist for the user.
   - `questions_for_seniors.md`: taxonomy and scope questions, point-wise.
   - `manual_uploads.csv`: 106 blocked-site products, 11 not found, 2 garbled (OCR), the Bajaj product with no description line, 2 Bajaj combination bundles.
   - `please_check.md`: 13 HDFC products listed as withdrawn, Edelweiss 404, Tata i Systematic V11 vs V04, Individual/Group annuity lines, health products in the master list.
   - `reminders.md`: Bharti FY24 PD and annual reports; make the repo private; Bharti analysis tab.
4. **Feature v1.1 fix:** add a negation guard, so "no / not / without / not available … critical illness" is not counted as a yes. Rebuild the counts. Deep discovery replaces these with built-in / optional / rider values anyway.
5. **Selection framework** (`analysis/selection_framework.md`), plus the ULIP application table.
6. **QA pack for Rahul** (`qa/checker_guide.md` + `qa/checker_workbook.xlsx`).
7. **After S2 returns the deep data:** feature list v2 for ULIP, the filled comparison matrix, the ULIP calculator plus a comparer front end (Excel first, then an optional web page), then the ULIP observation deck.

**ULIP selection (proposal; framework option A)**
- **Leaders:** the smallest set reaching ≥80% of ULIP premium (FY26 linked life + linked pension, from the PDs), up to 7. That gives SBI 27.9%, ICICI 12.7%, HDFC 12.5%, LIC 11.8% (as a reference column), Tata AIA 7.2%, Bajaj 6.2% and Axis Max 5.8%, together 84.1%.
- **Challengers:** 3 picked from insurers with ≥0.5% share, scored on 40% feature richness (from the v1 counts), 30% specialist index (ULIP share of the insurer's own book vs the industry's 19.6%), 20% growth (only if the ULIP book is ≥₹500 cr) and 10% expert nomination.
  - Likely: **ABSLI** (4.5%, +61%, specialist index 1.89), **Canara HSBC** (2.0%, +34%, 2.00), and **Kotak** (2.9%, +27%; blocked, so needs manual docs) or **PNB MetLife** (1.7%, many TULIP features).
- **Anchor: Bharti** (0.3%, 7 ULIPs).
- **Deep pass scope:** all current individual ULIPs (pension included) of these insurers, about 80 products.
  - **Start now:** SBI 7, HDFC 7, LIC 5, Tata 14, Bajaj 11, Axis Max 9, ABSLI 10, Canara 8, Bharti 7 (about 78).
  - **ICICI (13) and Kotak (8)** follow once the user uploads their documents.

**Deep-discovery brief for S2 (`briefs/deep_discovery_ulip_brief.md` + `briefs/ulip_feature_schema.json` + `briefs/ulip_deep_set.csv`)**
- **Documents per product:** policy document (contract), brochure (already in hand), CIS, sample BI if published, fund list or factsheet page.
- Record a **document inventory using each website's own labels** ("Policy Bond", "Policy Prospectus", "Product Brochure/Prospectus", "Policy Contract", "Leaflet", "Customer Information Sheet", "Benefit Illustration") and the counts per type in the summary.
- **Extract to `features/ulip/<UIN>.json`**, with a value, doc_type, page and verbatim quote for every field:
  - variants and options;
  - eligibility: entry and maturity ages, policy term and premium term options, min/max premium, sum-assured multiples;
  - premium modes;
  - charges: premium allocation by year, policy admin, FMC per fund, mortality basis and table reference, discontinuance, switching, partial withdrawal, miscellaneous;
  - benefits: death and maturity;
  - additions: loyalty additions / wealth boosters / return of mortality / return of allocation charges, with schedule and formula;
  - flexibility: free switches, premium redirection, partial withdrawals, top-ups, SWP, settlement option, premium holiday;
  - funds: name, SFIN, FMC, asset ranges, risk;
  - portfolio strategies;
  - riders;
  - **feature status for each feature: built-in / optional / rider / not offered;**
  - "not stated in public documents" kept distinct from "not offered".
- **Reuse the light-discovery navigation:** `index.csv` `found_on_page_url` and `site_quirks.md`. That makes this pass faster.
- **Timebox:** if a document or an insurer resists after a reasonable effort, park it in a "retry at the end" list and move on, then do a second pass on the parked items once everything else is done.
- **Output:** a `results/deep_ulip_summary.md` covering counts, gaps, data that isn't public (charges or mortality tables "as per policy schedule", etc.) and new features found that aren't in the schema.

**QA pack for Rahul (quantified)**
- **A. Master list vs ground truth:** 5 products per insurer × 21 insurers = 105 checks. Is the product current on the ground-truth source?
  - Sources: the Council Sep-2026 list; the official lists (Bharti, ICICI); Bajaj on-sale; Tata status page; the insurers' all-plans pages (links given; mark where S2 navigated menus because no list exists).
- **B. Brochure ↔ product match:** the same 105. Does the stored PDF open, show the right name and UIN (version noted), and does the description line match the sheet?
- **C. Classification:** 3 per category × 5 categories = 15. Category and sub-segment vs the description line.
- **D. Feature flags:** 20 random Y flags and 10 random N flags. Is the evidence right, and is the feature really offered or really absent?
- **E. Numeric fields:** 15 random values vs the brochure.
- **F. Phase-1 PD numbers:** 10 random cells (insurer × segment) vs the PD PDF page.
- **G. IRR:** Bharti Income Laabh, one case recomputed by hand.
- **Workbook:** one tab per check type, with prefilled rows, links and expected values, a pass/fail column and comments. Target ≥95% pass; anything failed is fixed and re-checked.

**Answers to the user's questions (for the reply)**
- **Negation ("no critical illness"):** v1 would count it as a yes. Fixed in v1.1 with a negation guard; the deep pass gives the real built-in / optional / rider status.
- **Garbled text / OCR / ambiguous items:** listed explicitly in `for-your-attention/`, and raised in the reply.

## CONTEXT HAND-OFF (4 Nov): project memory before /compact or a new session
**Context:** the context window is about 78% full. The user wants everything durable written to the repo before compacting or moving to a new chat, so nothing is lost.

**Plan (execute right after approval)**
1. Write **`li-product-docs/PROJECT_MEMORY.md`**, a single self-contained file covering:
   - goal and audience (Bharti product-suite analysis; Neha, seniors, Rahul);
   - all user decisions and preferences (official sources only, website = truth, no categories from names, one task at a time, accuracy first, raise ambiguous items explicitly, attention folder, LIC as a reference column, 5 market categories, scope exclusions, Saral/POS tagged);
   - repos, branches and paths (`boom`: phase-1 workbook; `li-product-docs`: everything else; S2's branch `ccr-d0d84e00-joo2mp`, merged into main);
   - the S1/S2 working model and the coordination file;
   - what's done, with key numbers and file paths;
   - what's in progress (S2 ULIP deep pass, wave 1);
   - what's left (ordered roadmap);
   - key findings so far (ULIP shares, Bharti white space, Bharti trend, the Income Laabh IRR and the brochure-vs-policy discrepancy, factor tables not published by SBI/HDFC/Tata);
   - known data issues and limits;
   - network and environment notes (allowlist with `www.` wildcards; blocked sites; the bot-check policy);
   - how to resume (the first commands to run).
2. Copy the approved plan file into the repo as `docs-internal/plan_history.md`, for the full decision trail. Also add the scratchpad scripts and data that matter (phase-1 `data.json`, `rows.py`, `build_data.py`, `make_xlsx.py` are already in `boom`; the IRR scratch is in `calc/`).
3. Add a pointer in `li-product-docs/CLAUDE.md`: "Read PROJECT_MEMORY.md first."
4. Commit and push to main.

**Recommendation on options:** both work once memory is in the repo.
- **/compact in this session is the better choice:** worktrees, scratchpad files and the attached repos stay in place, and the summary is backed by PROJECT_MEMORY.md.
- **A new session also works:** attach `li-product-docs` (and `boom`) and say "read PROJECT_MEMORY.md". It starts clean, but it needs re-cloning and loses the scratchpad.

**Also in the reply:** a short status update for Neha (done / doing / next).

## Execution order (one at a time, check in after each)
1. Rename INLIC, push.
2. ~~Bharti trend analysis~~ **deferred** until the docs are uploaded. Attach `ahen-can/li-product-docs` with `add_repo` and scaffold the README, `index.csv` schema and scripts.
3. **Master list v1:** Council PDF plus UIN parsing, then fill gaps and classify using the brochure description line (needs the www fix).
4. **Light scan** of all individual-product brochures, then the innovators and peers shortlist per category with rationale, then the deep-extraction brief for the second account.
5. Ingest the deep-extraction output, then build the feature list Excel.
6. Scorecard, then IRR calculators, then the top-product shortlist.

## Verification
- **Master list:** each insurer's count matches the Council's individual count (±withdrawn products). 100% of UINs parse. Every market category is backed by a quoted description line.
- **Features:** every cell cites the document and page. A spot-check of 10% of products is done by re-reading the source.
- **IRR:** the ULIP calculator matches the official BI fund values within 1%. Non-par IRRs reproduce the BI cash flows.
