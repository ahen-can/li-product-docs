# Brief: ULIP deep discovery (S2), wave 1

**From:** S1 (main session) · **For:** S2 · **Date:** 4 Nov 2026 · Read `coordination/CHAT.md` first and post there when you start and finish.

## Why
Great work on the light pass: 516 of 527 reachable products, with very useful site notes. We're now doing one category end to end (ULIP) to show Neha:
1. deep discovery (you);
2. feature list v2 and a filled comparison matrix (S1);
3. a ULIP calculator and product comparer (S1);
4. an observation deck on Bharti's ULIPs vs the market (S1).

## What to cover
`briefs/ulip_deep_set.csv` has **99 ULIPs from 11 insurers**. For each product it gives the product page and the brochure you already stored.
- **Wave 1 (start now, 78 products):** SBI, HDFC, LIC, Tata AIA, Bajaj, Axis Max, ABSLI, Canara HSBC, Bharti.
- **Wave 2 (21 products, later):** ICICI and Kotak, once the user uploads their documents. Skip them for now.

Suggested order: **Bharti first** (7, the client, so we can review the format early), then SBI, HDFC, Tata AIA, Bajaj, Axis Max, LIC, ABSLI, Canara HSBC.

## Documents to collect per product (insurer's own site only, same rules as `CLAUDE.md`)
1. **Policy document / contract.** This is the key one: charges, benefits and annexures are here.
2. **Customer information sheet (CIS)**, if published.
3. **Benefit illustration (BI) sample**, if the site publishes one.
4. **Fund list or fund factsheet page** for the product, if it is a separate document.
5. The brochure is already stored. Re-download only if a newer version is on the site, and note it.

Store as `docs/<slug>/<UIN>/<doc_type>.pdf` (`policy.pdf`, `cis.pdf`, `bi.pdf`, `fund_factsheet.pdf`), with text in `text/…`, and add one row per file to `index.csv` as before.

**Please record each document under the website's own label** (e.g. "Policy Bond", "Policy Prospectus", "Product Brochure/Prospectus", "Policy Contract", "Leaflet", "Customer Information Sheet", "Benefit Illustration") in a new `website_label` column of `index.csv`, and in each product's `documents_inventory`.

## What to extract
Use `briefs/ulip_feature_schema.json` and write one file per product: `features/ulip/<UIN>.json`. For every field:
- **value:** in the product's own terms (keep tables as tables, e.g. allocation charge % by year).
- **status:** built-in / optional (at inception) / optional (during term) / rider / not offered / **not stated in public documents** / n/a.
  - Keep "not offered" (the document says it isn't there, or the full feature section clearly omits it) separate from "not stated" (you couldn't find it).
- **doc + page + quote:** a verbatim quote, ≤300 characters, from the document you used. Prefer the policy document over the brochure when they differ, and note the difference in `note`.
- **new_features_not_in_schema:** anything distinctive the schema doesn't cover (e.g. a new fund strategy or an unusual addition). This is how the feature list grows.
- **data_not_public:** anything the documents defer to "as per policy schedule / available on request" (e.g. mortality rates not published).

## Reuse your navigation
- `index.csv` `found_on_page_url` and `results/site_quirks.md` already say where each insurer keeps policy documents. For example:
  - **Bharti:** "Policy Bond" on each product page.
  - **SBI:** `/documents/d/sbil/…policy-document…`.
  - **HDFC:** `/policy-documents` page.
  - **Tata AIA:** some policy documents sit behind a customer login, so note it and use the brochure.
  - **Axis Max:** "Policy Contract" on product pages.
  - **Canara HSBC:** `policy-document.pdf` next to the brochure.
- This pass should be much quicker than the light one.

## Pace and getting stuck
Please don't let one stubborn document or site hold up the run. If something resists after a reasonable effort (an odd page structure, a file that won't open, a site that keeps timing out), add it to a **"retry at the end"** list in your summary and move on. Once everything else is done, take a second pass at the parked items with fresh eyes. Anything still unresolved goes on the manual list for the user.

## Commit and push
Push after each insurer, on your branch as before (S1 merges your branch into main):
`git add docs/<slug> text/<slug> index.csv features/ulip results/ && git commit -m "Deep ULIP: <insurer> (<n> products, <m> policy docs, <k> BIs)"`

## Hand back
**`results/deep_ulip_summary.md`**
- **Counts per insurer:** products done; documents found by type, **using the website's own labels** (e.g. "Bharti: 7 Policy Bond, 7 Brochure, 7 CIS, 0 BI").
- **Gaps:** documents not published or behind a login, plus the retry list and its outcome.
- **data_not_public**, aggregated.
- **New features found**, aggregated across products. This seeds feature list v2.
- **Anything odd:** UIN version differences, a brochure that disagrees with the policy document, or products that look withdrawn.

Spot-check 2 products per insurer by hand against the PDF and say which ones you checked.

**Also post a short status in `coordination/CHAT.md`** (on your branch) when you start, after each insurer if anything is notable, and at the end.

## Don'ts
- Don't classify or score products; S1 does that.
- Don't use aggregators.
- Don't get around bot protection.
- Don't download withdrawn products' documents.
