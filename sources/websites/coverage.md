# Website coverage (individual products), fetched 3 Nov 2026

Source of truth = each insurer's own website. Cross-check = Life Insurance Council in-force list (Sep-2026). IRDAI's Dec-2025 list is **not used** (stale: e.g. Bharti's IRDAI-only products were all withdrawn).

## Method
- Fetched each insurer's plan listing pages (menus / "all plans" / category pages) and withdrawn-products page; snapshots in `listing_snapshots/` with URL and fetch time.
- Fetched candidate product pages (from listing links + sitemap), 1 request/second per site. A product page's own UIN = the insurer-prefixed UIN most frequent in its **visible text**, ignoring UINs that appear on >30% of that site's pages (promo banners).
- **current** = product page linked from a current plan listing, or listed as active on an official list. **withdrawn** = on the withdrawn-products page at the same or newer version than Council. A withdrawn **older** version is reported separately and is not treated as withdrawal.
- "page live, not in current plan listings" = a product page exists but is not linked from current listings (often legacy pages kept for existing policyholders) - not counted as current.
- No product category is inferred from names. Category columns are only: Council category (verbatim), IRDAI description line if the website quotes it, and Linked/Non-linked from the UIN.

## Per insurer

| Insurer | Master rows | In Council | Current on site | Older version withdrawn | Page live only | Not found | Site readable? |
|---|---|---|---|---|---|---|---|
| HDFC Life | 54 | 48 | 54 | 0 | 0 | 0 | OK, with caution: site keeps live pages for legacy products and shows a promo UIN on every page (ignored). No withdrawn-products page found. |
| Axis Max Life | 26 | 26 | 26 | 0 | 0 | 0 | OK |
| ICICI Life (formerly ICICI Prudential) | 38 | 38 | 0 | 0 | 0 | 0 | NOT READABLE: site returns 403 to automated access. User to supply product list (in progress). |
| Kotak Mahindra Life | 30 | 30 | 0 | 0 | 0 | 0 | NOT READABLE: site serves a bot-check (challenge) page; not bypassed by policy. User to supply. |
| Aditya Birla Sun Life | 35 | 35 | 33 | 0 | 0 | 0 | OK: brochures page mixes current and withdrawn without a status column; current status taken from linked product pages. |
| Tata AIA Life | 56 | 47 | 55 | 0 | 0 | 1 | OK: official "Active & Withdrawn Product Status" list (IRDAI format) read with status per UIN. |
| SBI Life | 32 | 0 | 32 | 0 | 0 | 0 | OK (website only; Council list has no SBI individual products). No withdrawn-products page found. |
| Bajaj Life | 46 | 0 | 46 | 0 | 0 | 0 | OK (website only; Council list has no Bajaj individual products). |
| PNB MetLife | 29 | 28 | 29 | 0 | 0 | 0 | OK |
| IndusInd Nippon Life | 30 | 30 | 26 | 0 | 0 | 4 | OK |
| Aviva Life | 20 | 18 | 19 | 0 | 0 | 1 | OK |
| Shriram Life | 26 | 26 | 21 | 5 | 0 | 0 | OK |
| Bharti Life | 30 | 26 | 30 | 0 | 0 | 0 | OK |
| Generali Central Life | 17 | 17 | 14 | 3 | 0 | 0 | OK |
| Ageas Federal Life | 24 | 24 | 3 | 12 | 7 | 2 | PARTIAL: current-plans listing is JavaScript-rendered, so product pages could not be tied to a current listing ("page live"). Withdrawn list read OK. |
| Canara HSBC Life | 24 | 24 | 24 | 0 | 0 | 0 | OK |
| Bandhan Life | 24 | 22 | 23 | 0 | 0 | 1 | OK |
| Pramerica Life | 24 | 23 | 21 | 2 | 0 | 1 | OK |
| Star Union Dai-ichi Life | 35 | 35 | 0 | 0 | 0 | 0 | NOT READABLE: site returns 403 to automated access. User to supply. |
| IndiaFirst Life | 37 | 31 | 33 | 0 | 0 | 4 | PARTIAL: product pages mostly do not print UINs; withdrawn page lists names without UINs. Flagged. |
| Edelweiss Life | 28 | 20 | 27 | 0 | 1 | 0 | OK |
| Acko Life | 2 | 2 | 0 | 0 | 0 | 2 | PARTIAL: individual product pages not discoverable from sitemap. Flagged (2 products). |
| Go Digit Life | 4 | 4 | 0 | 0 | 0 | 0 | NOT READABLE: site returns 403 to automated access. User to supply. |
| LIC | 39 | 38 | 35 | 2 | 0 | 2 | OK |

## Sites that could not be read (need user input)
- ICICI Life, Kotak Mahindra Life, Star Union Dai-ichi Life, Go Digit Life: blocked to automated access. Their rows carry Council data only, flagged `website not readable`.
- Partial: IndiaFirst Life, Acko Life, Ageas Federal Life (see table).

## Pages read per insurer

- **absli** (269 product pages fetched): [current+withdrawn] https://lifeinsurance.adityabirlacapital.com/forms-and-downloads/brochures-and-specimen-contracts/ (HTTP 200)
- **acko-life** (1 product pages fetched): [current] https://www.acko.com/life-insurance/ (HTTP 200)
- **ageas-federal** (42 product pages fetched): [withdrawn] https://www.ageasfederal.com/withdrawn-products (HTTP 200); [current] https://www.ageasfederal.com/brochures-list (HTTP 200); [current] https://www.ageasfederal.com/term-insurance-plans (HTTP 200)
- **aviva-life** (36 product pages fetched): [current] https://www.avivaindia.com/ulip-plans (HTTP 200); [current] https://www.avivaindia.com/term-insurance-plans (HTTP 200); [current] https://www.avivaindia.com/guaranteed-savings-plans (HTTP 200); [current] https://www.avivaindia.com/life-insurance-plans (HTTP 200); [current] https://www.avivaindia.com/retirement-pension-plans (HTTP 200); [current] https://www.avivaindia.com/form-and-resource-help-desk (HTTP 200)
- **axis-max-life** (146 product pages fetched): [withdrawn] https://www.axismaxlife.com/customer-servicing/withdrawn-plans (HTTP 200); [current] https://www.axismaxlife.com/all-insurance-plans (HTTP 200)
- **bajaj-life** (80 product pages fetched): [current] https://www.bajajlifeinsurance.com/ulip-plans.html (HTTP 200); [current] https://www.bajajlifeinsurance.com/term-insurance-plans.html (HTTP 200); [current] https://www.bajajlifeinsurance.com/savings-plans.html (HTTP 200); [current] https://www.bajajlifeinsurance.com/child-insurance-plans.html (HTTP 200); [current] https://www.bajajlifeinsurance.com/endowment-plans.html (HTTP 200); [current] https://www.bajajlifeinsurance.com/investment-insurance-plans.html (HTTP 200); [current] https://www.bajajlifeinsurance.com/retirement-pension-plans.html (HTTP 200); [withdrawn] https://www.bajajlifeinsurance.com/withdrawn-plans.html (HTTP 200)
- **bandhan-life** (59 product pages fetched): [withdrawn] https://www.bandhanlife.com/withdrawn-products (HTTP 200); [current] https://www.bandhanlife.com/term-insurance-plans (HTTP 200); [current] https://www.bandhanlife.com/savings-plans (HTTP 200); [current] https://www.bandhanlife.com/find-your-plan (HTTP 200); [current] https://www.bandhanlife.com/investment-plans (HTTP 200)
- **bharti-life** (48 product pages fetched): [current] https://www.bhartiaxa.com/retirement-plans (HTTP 200); [current] https://www.bhartiaxa.com/online-insurance-plans (HTTP 200); [current] https://www.bhartiaxa.com/protection-plans (HTTP 200); [current] https://www.bhartiaxa.com/child-education-plans (HTTP 200); [current] https://www.bhartiaxa.com/savings-plans (HTTP 200); [current] https://www.bhartiaxa.com/investment-plans (HTTP 200); [withdrawn] https://www.bhartiaxa.com/withdrawn-products (HTTP 200)
- **canara-hsbc** (55 product pages fetched): [withdrawn] https://www.canarahsbclife.com/download-centre/product-closed-for-sale (HTTP 200); [current] https://www.canarahsbclife.com/product-list (HTTP 200)
- **creditaccess-life** (0 product pages fetched): [withdrawn] https://www.creditaccesslife.in/pdf/Our_Products/withdrawn_product_list/CreditAccess_Life_Withdrawn_Products_V1.6.pdf (HTTP 200); [current] https://www.creditaccesslife.in/savings_product.php (HTTP 200); [current] https://www.creditaccesslife.in/ (HTTP 200)
- **edelweiss-life** (99 product pages fetched): [withdrawn] https://www.edelweisslife.in/discontinued-products (HTTP 200); [current] https://www.edelweisslife.in/product-listing (HTTP 200)
- **generali-central** (29 product pages fetched): [withdrawn] https://www.generalicentrallife.com/documents/withdrawn-products (HTTP 200); [current] https://www.generalicentrallife.com/insurance-plans (HTTP 200)
- **go-digit-life** (0 product pages fetched): [current] https://www.godigit.com/life-insurance (HTTP 403)
- **hdfc-life** (416 product pages fetched): [current] https://www.hdfclife.com/life-insurance-plans (HTTP 200); [current] https://www.hdfclife.com/term-insurance-plans (HTTP 200); [current] https://www.hdfclife.com/children-insurance-plans (HTTP 200); [current] https://www.hdfclife.com/savings-plans (HTTP 200); [current] https://www.hdfclife.com/ulip-plans (HTTP 200); [current] https://www.hdfclife.com/retirement-and-pension-plans (HTTP 200)
- **icici-life** (0 product pages fetched): [current] https://www.icicilife.com/insurance-plans/view-all-insurance-plans.html (HTTP 403)
- **indiafirst** (162 product pages fetched): [withdrawn] https://www.indiafirstlife.com/download-forms/withdrawn-products (HTTP 200); [current] https://www.indiafirstlife.com/life-insurance-plans (HTTP 200)
- **indusind-nippon** (33 product pages fetched): [current] https://www.indusindnipponlife.com/all-plans (HTTP 200)
- **kotak-life** (0 product pages fetched): [current] https://www.kotaklife.com/insurance-plans (HTTP 202); [current] https://www.kotaklife.com/ (HTTP 202)
- **lic** (31 product pages fetched): [current] https://licindia.in/products (HTTP 200); [current] https://licindia.in/protect-my-family-term-plan (HTTP 200); [current] https://licindia.in/plan-for-my-retirement-pension-plans (HTTP 200); [withdrawn] https://licindia.in/withdrawn-plans (HTTP 200); [current] https://licindia.in/plans-for-children-s-future (HTTP 200); [current] https://licindia.in/create-wealth-ulip-plans-endowment-money-back (HTTP 200)
- **pnb-metlife** (67 product pages fetched): [current] https://www.pnbmetlife.com/insurance-plans/ulip-plans.html (HTTP 200); [current] https://www.pnbmetlife.com/insurance-plans/retirement-plans.html (HTTP 200); [withdrawn] https://www.pnbmetlife.com/withdrawn-insurance-plans.html (HTTP 200); [current] https://www.pnbmetlife.com/life-insurance-plans.html (HTTP 200); [current] https://www.pnbmetlife.com/insurance-plans/term-insurance-plans.html (HTTP 200); [current] https://www.pnbmetlife.com/investment-plans.html (HTTP 200)
- **pramerica-life** (22 product pages fetched): [current] https://pramericalife.in/ (HTTP 200); [current] https://pramericalife.in/saving-plans (HTTP 200); [withdrawn] https://pramericalife.in/customer-services/withdrawn-plans (HTTP 200); [current] https://pramericalife.in/term-plans (HTTP 200)
- **sbi-life** (46 product pages fetched): [current] https://www.sbilife.co.in/life-insurance-plans/term-insurance (HTTP 200); [current] https://www.sbilife.co.in/savings-plans (HTTP 200); [current] https://www.sbilife.co.in/money-back-plan (HTTP 200); [current] https://www.sbilife.co.in/life-insurance-plans (HTTP 200); [current] https://www.sbilife.co.in/child-insurance-plan (HTTP 200); [current] https://www.sbilife.co.in/retirement-plans (HTTP 200); [current] https://www.sbilife.co.in/ulip-plans (HTTP 200)
- **shriram-life** (115 product pages fetched): [current] https://www.shriramlife.com/child-plans (HTTP 200); [current] https://www.shriramlife.com/life-insurance (HTTP 200); [withdrawn] https://www.shriramlife.com/legal/withdrawn-plan (HTTP 200)
- **sud-life** (0 product pages fetched): [current] https://www.sudlife.in/ (HTTP 403)
- **tata-aia** (180 product pages fetched): [current+withdrawn] https://www.tataaia.com/active-and-withdrawn-product-status.html (HTTP 200)
