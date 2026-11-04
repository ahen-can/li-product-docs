# Light discovery (brochure pass): summary

`scripts/build_summary.py` builds this file from `results/light_discovery_results.csv` (one row per product) and
`master_list.csv`. The last sections are hand-written notes from `results/site_quirks.md`.

## Counts per insurer

| Insurer | Products | ok | of which brochure | of which policy doc | not found | manual (site blocks automation) | not run |
|---|---|---|---|---|---|---|---|
| Acko Life | 2 | 2 | 2 | 0 | 0 | 0 | 0 |
| Aditya Birla Sun Life | 34 | 34 | 32 | 2 | 0 | 0 | 0 |
| Ageas Federal Life | 23 | 22 | 19 | 3 | 1 | 0 | 0 |
| Aviva Life | 17 | 17 | 16 | 1 | 0 | 0 | 0 |
| Axis Max Life | 26 | 26 | 26 | 0 | 0 | 0 | 0 |
| Bajaj Life | 31 | 30 | 28 | 1 | 1 | 0 | 0 |
| Bandhan Life | 22 | 22 | 22 | 0 | 0 | 0 | 0 |
| Bharti Life | 26 | 26 | 25 | 1 | 0 | 0 | 0 |
| Canara HSBC Life | 24 | 22 | 22 | 0 | 2 | 0 | 0 |
| Edelweiss Life | 20 | 18 | 18 | 0 | 2 | 0 | 0 |
| Generali Central Life | 17 | 17 | 17 | 0 | 0 | 0 | 0 |
| Go Digit Life | 5 | 0 | 0 | 0 | 0 | 5 | 0 |
| HDFC Life | 47 | 47 | 43 | 4 | 0 | 0 | 0 |
| ICICI Life | 38 | 0 | 0 | 0 | 0 | 38 | 0 |
| IndiaFirst Life | 31 | 31 | 31 | 0 | 0 | 0 | 0 |
| IndusInd Nippon Life | 28 | 27 | 27 | 0 | 1 | 0 | 0 |
| Kotak Mahindra Life | 30 | 0 | 0 | 0 | 0 | 30 | 0 |
| LIC | 39 | 39 | 37 | 2 | 0 | 0 | 0 |
| PNB MetLife | 27 | 27 | 27 | 0 | 0 | 0 | 0 |
| Pramerica Life | 22 | 21 | 21 | 0 | 1 | 0 | 0 |
| SBI Life | 27 | 27 | 27 | 0 | 0 | 0 | 0 |
| Shriram Life | 26 | 26 | 25 | 1 | 0 | 0 | 0 |
| Star Union Dai-ichi Life | 33 | 0 | 0 | 0 | 0 | 33 | 0 |
| Tata AIA Life | 38 | 35 | 34 | 1 | 3 | 0 | 0 |
| **Total** | **633** | **516** | 499 | 16 | **11** | **106** | 0 |

Hit rate on sites that allow automated access: 516 of 527 (97.9%).

## Description lines that look odd

Insurers print many ULIP lines without a par flag, for example "A Unit Linked Individual Savings Life Insurance Plan".
This table leaves those out.

| Insurer | Product | UIN | Description line (as extracted) | Why listed |
|---|---|---|---|---|
| Aviva Life | Aviva Bharat Bal Vikas Yojana | 122N180V01 | An Individual Non-Linked, Non-Participating Savings Life Insurance Plan | read by OCR from an image |
| Axis Max Life | Axis Max Life Smart Retirement Income with Sustained Earnings Plan | 104N160V01 | A Non-Linked Non-Participating Individual/ Group General Annuity Savings Plan | group product |
| Axis Max Life | Axis Max Life Smart Wealth Annuity Guaranteed Pension Plan | 104N137V16 | A Non-Linked Non-Participating Individual/ Group General Annuity Savings Plan | group product |
| Bajaj Life | Bajaj Life ACE | 116N186V04 | Non linked, Participating, Individual Life Insurance Savings Plan | read by OCR from an image |
| Bajaj Life | Bajaj Life ACE Advantage | 116N189V02 | a non-linked, participating, individual life insurance, savings plan | read by OCR from an image |
| Bajaj Life | Bajaj Life Assured Wealth Goal | 116N170V14 | A Non linked, Non Participating, Individual, Life Insurance Savings Plan | read by OCR from an image |
| Bajaj Life | Bajaj Life Guaranteed Pension Goal II | 116N187V11 |  | no description line found; read by OCR from an image |
| Bajaj Life | Bajaj Life Secure Plus | 116N216V01 | A Non-Participating, Non-Linked, Individual Health Plan | health product |
| Bajaj Life | Bajaj Life Smart Secure ROP |  | A Unit-Linked Non-Participating Individual Life Savings Insurance Plan | linked/non-linked differs from UIN letter ''; combination product |
| Bharti Life | Bharti AXA Life Grameen Jeevan Bima | 130N098V02 | A Non-Linked, Non-Participating Life Term Micro Insurance Plan | micro-insurance product |
| Bharti Life | Bharti AXA Life Growth Shield Plus | 130L123V01 | A unit Linked, non-par cipa ng individual life insurance plan | text extraction dropped ligatures ("ti") |
| Bharti Life | Bharti AXA Life Wealth Pro | 130L100V03 | A unit Linked, non-par cipa ng individual life insurance plan | text extraction dropped ligatures ("ti") |
| Canara HSBC Life | Canara HSBC Life Insurance Guaranteed Fortune Plan | 136N084V05 | Non-Linked Non-Participating Individual Savings Life Insurance Plan | read by OCR from an image |
| Canara HSBC Life | Canara HSBC Life Insurance Guaranteed Suraksha Kavach | 136N078V04 | A Non-Linked Non-Par Individual Life Insurance Savings cum Protection Plan | read by OCR from an image |
| Canara HSBC Life | Canara HSBC Life Insurance Saral Jeevan Bima | 136N075V02 | A Non Linked Non Par�cipa�ng Individual Pure Risk Premium Life Insurance Plan | text extraction dropped ligatures ("ti") |
| Canara HSBC Life | Canara HSBC Life Insurance Young Term Plan | 136N087V03 | A Non-Linked, Non-Par�cipa�ng, Individual, Pure Risk Premium, Life Insurance Plan | text extraction dropped ligatures ("ti") |
| Edelweiss Life | Edelweiss Life - Suraksha Kavach Bima Yojana (Micro Insurance Plan) | 147N083V01 | An Individual, Non-Linked, Non-Participating, Pure Risk, Life, Micro Insurance Product | micro-insurance product |
| HDFC Life | HDFC Life Smart Pension Plus | 101N173V13 | A Non-Linked, Non-Participating Individual/ PENSION Group Annuity Savings Plan | group product |
| IndiaFirst Life | IndiaFirst Life “INSURANCE KHATA” Plan (MicroInsuranceProduct) | 143N057V03 | A Non-Linked, Non Participating, Individual Life, Micro Insurance, Savings Plan | micro-insurance product |
| IndusInd Nippon Life | IndusInd Nippon Life Nishchit Pension | 121N158V03 | A Non-Linked, Non-Participating, Individual, Deferred Annuity Plan | read by OCR from an image |
| LIC | LIC's Jan Suraksha | 512N388V01 | A Non-Par, Non-Linked, Individual, Savings, Life Micro Insurance Plan | micro-insurance product |
| LIC | LIC's Micro Bachat | 512N329V03 | A Par, Non-Linked, Individual, Savings, Life Micro Insurance Plan | micro-insurance product |
| PNB MetLife | PNB MetLife 360 Health Savings Plan | 117L143V02 | an Individual, Unit–Linked, Non–Participating, Savings, Health Insurance Plan | health product |
| SBI Life | SBI Life - Retire Smart Plus | 111L135V02 | an Individual, Unit Linked, Non-Par cipa ng, Pension Savings Product | text extraction dropped ligatures ("ti") |
| SBI Life | SBI Life - Smart Annuity Plus | 111N134V10 | An Individual, Non-Linked, Non-Participating, General Annuity Product | read by OCR from an image |
| Shriram Life | Shriram Life Smart Choice Plan | 128N097V03 | A Non Linked Non Participating Individual Pure Risk Life Insurance Plan | read by OCR from an image |
| Tata AIA Life | Tata AIA Life Guaranteed Return Insurance Plan | 110N152V16 | Individual, Non-Linked, Non-Participating, Life Insurance Savings Plan | read by OCR from an image |
| Tata AIA Life | Tata AIA Life Insurance Fortune Guarantee | 110N120V12 | Non Linked Non Participating Individual Life Insurance Savings Plan | read by OCR from an image |

## Documents whose UIN version differs from the master list

The script keeps each document as found and never relabels it (CLAUDE.md). "Older" usually means the site has not
posted the latest version. "Newer" usually means the master list is behind the insurer.

| Insurer | Product | Master UIN | UIN in document | Document is | Doc type |
|---|---|---|---|---|---|
| Aditya Birla Sun Life | ABSLI Fixed Maturity Plan | 109N135V06 | 109N135V02 | older | brochure |
| Aditya Birla Sun Life | ABSLI Guaranteed Annuity Plus | 109N132V18 | 109N132V19 | newer | brochure |
| Ageas Federal Life | Ageas Federal Life Insuarnce MAGIC Savings Plan | 135N098V04 | 135N098V05 | newer | brochure |
| Aviva Life | Aviva Signature 3D Term Plan | 122N148V02 | 122N148V01 | older | brochure |
| Aviva Life | Aviva Signature Investment Plan-LP | 122L150V03 | 122L150V01 | older | brochure |
| Axis Max Life | Axis Max Life Smart Total Elite Protection Plan | 104N125V09 | 104N125V10 | newer | brochure |
| Bandhan Life | Bandhan Life iGuarantee ChildAssure | 138N122V01 | 138N122V02 | newer | brochure |
| Edelweiss Life | Edelweiss Life - Wealth Premier | 147L066V03 | 147L066V04 | newer | brochure |
| HDFC Life | HDFC Life ClassicAssure Plus | 101N089V06 | 101N089V05 | older | brochure |
| HDFC Life | HDFC Life Click 2 Protect Supreme Plus | 101N189V03 | 101N189V04 | newer | brochure |
| HDFC Life | HDFC Life Income Advantage Plan | 101N152V03 | 101N152V02 | older | policy |
| HDFC Life | HDFC Life Personal Pension Plus | 101N091V05 | 101N091V04 | older | brochure |
| HDFC Life | HDFC Life Pragati | 101N114V05 | 101N114V04 | older | brochure |
| HDFC Life | HDFC Life Sampoorn Samridhi Plus | 101N102V06 | 101N102V05 | older | brochure |
| HDFC Life | HDFC Life Saral Jeevan Bima | 101N140V02 | 101N140V01 | older | brochure |
| HDFC Life | HDFC Life Super Income Plan | 101N098V06 | 101N098V05 | older | brochure |
| HDFC Life | HDFC Life YoungStar Udaan | 101N099V05 | 101N099V04 | older | brochure |
| IndusInd Nippon Life | IndusInd Nippon Life Nishchit Ace | 121N180V01 | 121N180V02 | newer | brochure |
| IndusInd Nippon Life | IndusInd Nippon Life Nishchit Pension | 121N158V03 | 121N158V04 | newer | brochure |
| PNB MetLife | PNB MetLife Century Plan | 117N129V03 | 117N129V04 | newer | brochure |
| PNB MetLife | PNB MetLife Smart Goal Ensuring Multiplier | 117L139V04 | 117L139V05 | newer | brochure |
| PNB MetLife | PNB MetLife Smart Invest Pension Plan Pro | 117L138V05 | 117L138V06 | newer | brochure |
| PNB MetLife | PNB MetLife Smart Platinum Pro | 117L142V02 | 117L142V03 | newer | brochure |
| Shriram Life | Shriram Life Deferred Annuity Plan | 128N105V03 | 128N105V04 | newer | brochure |
| Tata AIA Life | TATA AIA Shubh Maha Life | 110N208V04 | 110N208V05 | newer | brochure |
| Tata AIA Life | Tata AIA Fortune Guarantee Secure | 110N206V03 | 110N206V04 | newer | brochure |
| Tata AIA Life | Tata AIA Fortune Guarantee Supreme | 110N163V14 | 110N163V15 | newer | brochure |
| Tata AIA Life | Tata AIA Life Insurance Fortune Guarantee | 110N120V12 | 110N120V13 | newer | brochure |
| Tata AIA Life | Tata AIA Shubh Employee Protect | 110N185V01 | 110N185V02 | newer | brochure |
| Tata AIA Life | Tata AIA i Systematic Insurance Plan | 110L164V11 | 110L164V04 | older | brochure |

## Other flags on found documents

| Insurer | Product | UIN | Note |
|---|---|---|---|
| Aditya Birla Sun Life | ABSLI Saral Pension | 109N130V01 | brochure not verified (UIN missing/different); policy document used |
| Aditya Birla Sun Life | ABSLI Super Term Plus Plan | 109N155V01 | brochure not verified (UIN missing/different); policy document used |
| Ageas Federal Life | Ageas Federal Life Insurance Easy Save Plan | 135N122V01 | brochure not verified (UIN missing/different); policy document used |
| Ageas Federal Life | Ageas Federal Life Insurance Wealthsurance Growth Insurance Plan SP II | 135L082V02 | brochure not verified (UIN missing/different); policy document used |
| Ageas Federal Life | Ageas Federal Life Insurance Young Star Plus Plan | 135N076V03 | brochure not verified (UIN missing/different); policy document used; file is linked from the ageasfederal.com product page but hosted on storage account sacicwputd01 (name suggests a test/UAT environment) - confirm it is the published version |
| Aviva Life | Aviva Smart Return of Premium Term Plan | 122N161V01 | brochure not verified (UIN missing/different); policy document used |
| Bajaj Life | Bajaj Life Capital Goal Suraksha | (none) | no UIN in master list (NA on Bajaj on-sale list); stored file is the Bajaj Life Goal Suraksha brochure (116N155V20), likely the base product of this offering - UIN check not possible |
| Bajaj Life | Bajaj Life Flexi Income Goal Plus | 116N242V02 | brochure not verified (UIN missing/different); policy document used |
| Bajaj Life | Bajaj Life Goal Suraksha | 116N155V20 | same file as NOUIN-bajaj-life-capital-goal-suraksha-brochure |
| Bajaj Life | Bajaj Life Smart Secure ROP | (none) | no verified brochure or policy document; leaflet used; no UIN in master list; stored file is a combination leaflet for Invest Protect Goal Plus Elite (ULIP, 116L215V01) + Secure Plus Shield with ROP (health, 116N216V01); description line is the ULIP component's |
| Bharti Life | Bharti AXA Life Grow Wealth Ultra | 130L128V01 | brochure not verified (UIN missing/different); policy document used |
| Bharti Life | Bharti AXA Life Monthly Advantage | 130N068V05 | UIN printed as 130NO68V05 (letter O for zero) |
| Canara HSBC Life | Canara HSBC Life Insurance Guaranteed Fortune Plan | 136N084V05 | UIN and text read by OCR (image-heavy PDF); UIN printed as 136NO084V05 (letter O for zero) |
| HDFC Life | HDFC Life ClassicAssure Plus | 101N089V06 | document shows 101N089V05; hdfclife.com/policy-documents lists this product only under withdrawn sections; master list says active - confirm sale status |
| HDFC Life | HDFC Life Income Advantage Plan | 101N152V03 | document shows 101N152V02; brochure not verified (UIN missing/different); policy document used; hdfclife.com/policy-documents lists this product only under withdrawn sections; master list says active - confirm sale status |
| HDFC Life | HDFC Life My Assured Income Plan | 101N155V02 | brochure not verified (UIN missing/different); policy document used; hdfclife.com/policy-documents lists this product only under withdrawn sections; master list says active - confirm sale status |
| HDFC Life | HDFC Life New Fulfilling Life | 101N149V02 | brochure not verified (UIN missing/different); policy document used; hdfclife.com/policy-documents lists this product only under withdrawn sections; master list says active - confirm sale status |
| HDFC Life | HDFC Life Personal Pension Plus | 101N091V05 | document shows 101N091V04; hdfclife.com/policy-documents lists this product only under withdrawn sections; master list says active - confirm sale status |
| HDFC Life | HDFC Life Pragati | 101N114V05 | document shows 101N114V04; hdfclife.com/policy-documents lists this product only under withdrawn sections; master list says active - confirm sale status |
| HDFC Life | HDFC Life Sampoorn Samridhi Plus | 101N102V06 | document shows 101N102V05; hdfclife.com/policy-documents lists this product only under withdrawn sections; master list says active - confirm sale status |
| HDFC Life | HDFC Life Saral Jeevan Bima | 101N140V02 | document shows 101N140V01; hdfclife.com/policy-documents lists this product only under withdrawn sections; master list says active - confirm sale status |
| HDFC Life | HDFC Life Saral Pension | 101N141V03 | hdfclife.com/policy-documents lists this product only under withdrawn sections; master list says active - confirm sale status |
| HDFC Life | HDFC Life Smart Woman | 101L082V03 | hdfclife.com/policy-documents lists this product only under withdrawn sections; master list says active - confirm sale status |
| HDFC Life | HDFC Life Star Saver | 101N167V02 | brochure not verified (UIN missing/different); policy document used; hdfclife.com/policy-documents lists this product only under withdrawn sections; master list says active - confirm sale status |
| HDFC Life | HDFC Life Super Income Plan | 101N098V06 | document shows 101N098V05; hdfclife.com/policy-documents lists this product only under withdrawn sections; master list says active - confirm sale status |
| HDFC Life | HDFC Life YoungStar Udaan | 101N099V05 | document shows 101N099V04; hdfclife.com/policy-documents lists this product only under withdrawn sections; master list says active - confirm sale status |
| LIC | LIC’s Yuva Credit Life | 512N357V01 | brochure not verified (UIN missing/different); policy document used |
| LIC | LIC’s Yuva Term | 512N355V02 | brochure not verified (UIN missing/different); policy document used |
| Shriram Life | Shriram Life Golden Jubilee Plan | 128L095V02 | brochure not verified (UIN missing/different); policy document used |
| Tata AIA Life | Tata AIA Smart Sampoorna Raksha Pro | 110L172V03 | brochure not verified (UIN missing/different); policy document used |

## Not found / manual

`results/manual_checklist.csv` lists every product below with the page to visit. `results/manual_checklist_blocked_sites.csv`
covers the four sites that block automated access.

| Insurer | Product | UIN | Status | Where looked / reason |
|---|---|---|---|---|
| Ageas Federal Life | Ageas Federal Life Insurance Guaranteed Lifetime Income Plan | 135N073V04 | not found | 47 PDF links seen on 1 pages; none verified (product code not in text or no match); no product page or document on ageasfederal.com (sitemap and savings-plans pages checked) |
| Bajaj Life | Bajaj Life Realizing Dreams Plus | 116N243V01 | not found | 20 PDF links seen on 2 pages; none verified (product code not in text or no match); not on bajajlifeinsurance.com on-sale-plans.html or sitemap.xml |
| Canara HSBC Life | Canara HSBC Life Insurance Pension4life Plan | 136N071V11 | not found | 16 PDF links seen on 1 pages; none verified (product code not in text or no match); not on canarahsbclife.com product-list or sitemap.xml |
| Canara HSBC Life | Canara HSBC Life Insurance Promise4Growth | 136L089V02 | not found | 19 PDF links seen on 2 pages; none verified (product code not in text or no match); not on canarahsbclife.com product-list or sitemap; /ulips/promise4growth-plus is a different product (136L093V01) |
| Edelweiss Life | Edelweiss Life - Flexi-Savings Plan | 147N075V04 | not found | 18 PDF links seen on 7 pages; none verified (product code not in text or no match); edelweisslife.in/flexi-savings-plan returns 404 although listed in sitemap.xml; no brochure found elsewhere on the site |
| Edelweiss Life | Edelweiss Life - Premier Guaranteed STAR Pro | 147N115V02 | not found | 7 PDF links seen on 2 pages; none verified (product code not in text or no match); not on edelweisslife.in product listing or sitemap; /premier-guaranteed-star is a different product (147N077V05) |
| IndusInd Nippon Life | IndusInd Nippon Life Secure Shield Plan | 121N154V01 | not found | 3 PDF links seen on 3 pages; none verified (product code not in text or no match); not on indusindnipponlife.com all-plans / term-insurance-plans pages or sitemap |
| Pramerica Life | Pramerica Life Poorna Rakhak | 140N113V01 | not found | 12 PDF links seen on 4 pages; none verified (product code not in text or no match); not on pramericalife.in sitemap or plan listing pages |
| Tata AIA Life | Tata AIA Life Insurance POS Saat Saath - Micro Insurance Product | 110N134V04 | not found | 18 PDF links seen on 1 pages; none verified (product code not in text or no match); POS variant: listed Active on tataaia.com/active-and-withdrawn-product-status.html but no product page or document link on tataaia.com (sitemap, status page, base-product page checked) |
| Tata AIA Life | Tata AIA Life Insurance POS Smart Income Plus | 110N148V07 | not found | 18 PDF links seen on 1 pages; none verified (product code not in text or no match); POS variant: listed Active on tataaia.com/active-and-withdrawn-product-status.html but no product page or document link on tataaia.com (sitemap, status page, base-product page checked) |
| Tata AIA Life | Tata AIA Life Insurance Sampoorna Raksha Supreme Plan | 110N160V06 | not found | 37 PDF links seen on 8 pages; none verified (product code not in text or no match); listed Active (V06) on tataaia.com status page; product pages tataaia.com/sampoorna-raksha-supreme.html and /sampoorna-raksha-supreme/non-linked-comprehensive-protection.html link no brochure or policy document |
| Go Digit Life (5), ICICI Life (38), Kotak Mahindra Life (30), Star Union Dai-ichi Life (33) | all products | | manual | the site blocks automated access, so the brief says not to try it |

## Site quirks for the deep pass (where policy documents and BIs live)

- **Bharti Life.** Each product page (`/savings-plans/<plan>`, `/ulip-plans/<plan>`, `/term-insurance/<plan>` and so on, all in `sitemap.xml`) has three links: *Download Brochure*, *Policy Bond* (the policy document, often named `…part_b.pdf`) and *Customer Information Sheet*. All three sit under `/sites/default/files/<yyyy-mm>/`. Every page also embeds a few old 2023 brochures (Wealth Pro, SIGP, Flexi Term Pro), so a `.pdf` on a product page is not necessarily that product's file. Grow Wealth Ultra's brochure prints Dream Shield Plus's UIN, so I stored its policy bond instead. Monthly Advantage's brochure prints its UIN as `130NO68V05`, with a letter O. The site publishes no BIs.
- **LIC.** The category pages (`/web/guest/endowment-plans`, `…/whole-life-plans`, `…/money-back-plans`, `…/term-assurance-plans`, `…/pension-plan`, `…/unit-linked-plans`, `…/micro-insurance-plans`) are tables with columns for the plan name (linked to the plan page), the plan number and the UIN. Each plan page links a *Sales brochure*, a *Policy Document* and a *CIS* under `/documents/20121/…`. Some plan pages list two brochures dated "From … To …" and "From … onwards". LIC prints the par flag before "Linked", as in "A Par, Non-Linked, …".
- **SBI Life.** Product pages link URLs like `/documents/d/sbil/product-brochure-prospectus-NN`, with no `.pdf` suffix. The same pages link the policy documents.
- **Generali Central.** The site is built with Next.js. Product pages (in `sitemap.xml`) embed four files in their page data: `/docs/<plan_slug>/product_brochure.pdf`, `policy_document.pdf`, `customer_information_sheet.pdf` and `policy_schedule.pdf`. ULIP brochures put the par flag, in brackets, before "Unit linked": "Non-Participating (without profits), Unit linked, …".
- **HDFC Life.** Product pages (in `universal-sitemap.xml`) link only rider brochures, not the product's own brochure. Current files are on `/brochures`, in folders named `…/brochure-documents-pdfs/<line>-live/`, and on `/policy-documents`, in folders ending `-live/` or `-withdrawn/`. `pdf-sitemap.xml` lists every PDF the site hosts, old versions included. 13 master-list products appear on `/policy-documents` only under the withdrawn sections, and each of those rows carries a note. Several brochures on the site are older versions than the master-list UIN (see the versions table).
- **Tata AIA.** Product pages are in `sitemap.xml`. Brochure and policy-document links sit under `/content/dam/tataaialifeinsurancecompanylimited/life-insurance-plans/<line>/<plan>/`. Some product pages link only a policy bond. `active-and-withdrawn-product-status.html` lists every UIN version with its launch and withdrawal dates, which helps with status checks. The POS variants have no pages.
- **Shriram Life.** Each product page links a *Downloads* page at `…/life-insurance/<plan>-download-documents`. That page's links sit in embedded Nuxt data, point to `cdn.shriramlife.com/slic-kalam/files/<yyyy-mm>/…`, and use `\u002F` for slashes and a `?VersionId=` suffix. The same page has the policy document and a product presentation. Smart Choice Plan prints its description line only inside an image, so I read it with OCR.
- **Aditya Birla Sun Life (ABSLI).** All documents sit under `lifeinsurance.adityabirlacapital.com/uploads/…`. The *brochures and specimen contracts* page (a seed page in the script) lists the brochure and policy contract for every product. Product pages are in `sitemap.xml`.
- **Acko Life.** `acko.com/life/download/` lists the brochure ("Product Brochure (Effective …)"), policy document, CIS and **benefit illustration** for both products. The files are on Acko's asset domain, `acko-cms.ackoassets.com`. The *Download* button on `/life-insurance/` opens that page with JavaScript.
- **Ageas Federal.** Product pages (`/savings-plans/…`, `/ulip-plans/…`, `/term-insurance-plans/…`, in `sitemap.xml`) link files on Azure blob storage at `sacicwpprd01.blob.core.windows.net/$web/sccicwppr01/assets/…`. Two pages (Super Protect Plus and Young Star Plus) link a second storage account, `sacicwputd01`, whose name suggests a test (UAT) environment. Both rows carry a note.
- **Aviva.** Product pages link files under `/sites/default/files/…`. The `form-and-resource-help-desk` page (a seed page) lists many brochures. The sales literature for Bharat Bal Vikas Yojana is a scanned image PDF, so I read it with OCR.
- **Axis Max Life.** Product pages (in `main-sitemap.xml`) link a *Policy Prospectus*, *Policy Contract* and *Policy Leaflet*. Files are named by the product's initials, for example `/static-page/assets/homepage/PWP_Prospectus_<hash>.pdf` for Platinum Wealth Plan.
- **Bajaj Life.** Brochures sit at `/content/dam/balic-web/pdf/<line>/<plan>-brochure.pdf`, next to `-cis.pdf` and `-leaflet.pdf` files. `on-sale-plans.html` (a seed page) links every product page. Two master-list rows have no UIN because they are combination offers (see the flags table).
- **Bandhan Life.** Product pages (in `sitemap.xml`) link files under `/sites/default/files/asset/<yyyy-mm>/…`.
- **Canara HSBC.** Product pages (in `sitemap.xml`) link `/content/dam/chli/pdf…/<plan>/…/product-brochure.pdf`, with `policy-document.pdf` and `customer-information-sheet.pdf` in the same folder. Several brochures print the UIN only inside images, so I read them with OCR.
- **Edelweiss Life.** The site runs on Liferay. Product pages link `/documents/d/guest/<slug>_productbrochure` (no `.pdf`) and `/documents/20121/<id>/…_ProductBrochure.pdf`, plus a sample policy, a sample rates table and a CIS.
- **IndiaFirst Life.** Brochures sit under `/content/dam/ifliwebsite/in/en/download-center/all-product-related-documents/brochures/individual/<plan>/…pdf.coredownload.inline.pdf`. `pdf-sitemap.xml` lists every PDF, including a `withdrawn-products/` folder.
- **IndusInd Nippon Life.** The site runs on Liferay. Pages at `all-plans/<line>/<plan>` link files under `/documents/34625/<id>/…`. Some product pages link only a mortality-rate table, or a copy on `onlinesales.indusindnipponlife.com`.
- **PNB MetLife.** Pages at `insurance-plans/<line>/<plan>.html` link brochures under `/content/dam/pnb-metlife/docs/product/Download_Brochure/…`. The `TermsCondition/` folder holds policy documents and `leaflet/` holds one-pagers.
- **Pramerica Life.** Product pages (in `sitemap-index.xml`) link uploads under `pramericalife.in/admin/assets/fileUpload/…` and `…/images/pages/…`. The file names contain raw spaces.
- **Leaflets next to brochures.** ABSLI, SBI, Bandhan, PNB MetLife, HDFC and others publish a one-page leaflet next to the full sales brochure, and often link the leaflet more prominently. The script tries the brochure first, then the policy document, then the leaflet, and labels leaflets `doc_type=leaflet`. Only one leaflet is stored: Bajaj Smart Secure ROP, a combination offer with no other document online.
- **Blocked sites.** I did not contact ICICI, Kotak, Star Union Dai-ichi or Go Digit, as the brief says. Their 106 products are `manual`, and `results/manual_checklist.csv` and `results/manual_checklist_blocked_sites.csv` give the page to visit for each.

## Scope questions for the main session

The brief says not to classify products from their names or set categories, so I changed nothing here. These rows are worth a look.

- **Health products in the master list.** Shriram Life Comprehensive Cancer Care (128N070V02, "Protection Plan"), Bajaj Life Secure Plus (116N216V01, "Individual Health Plan") and PNB MetLife 360 Health Savings Plan (117L143V02, "… Savings, Health Insurance Plan").
- **Micro-insurance products.** The description lines of Bharti Grameen Jeevan Bima, Edelweiss Suraksha Kavach Bima Yojana, IndiaFirst Insurance Khata, LIC Jan Suraksha and LIC Micro Bachat say "Micro Insurance".
- **Individual/Group lines.** Axis Smart Wealth Annuity Guaranteed Pension, Axis Smart Retirement Income with Sustained Earnings and HDFC Smart Pension Plus print "Individual/ Group … Annuity". Text extraction garbled the HDFC line into "Individual/ PENSION Group …", so read it in the PDF.
- **Possibly withdrawn but still on the master list.** HDFC lists 13 products only under withdrawn on hdfclife.com/policy-documents, and each row carries a note. The Edelweiss Flexi-Savings Plan page returns 404. Tata's status page lists POS Saat Saath and POS Smart Income Plus as Active, but the site has no page or document for either.
- **Bajaj rows without a UIN.** Capital Goal Suraksha and Smart Secure ROP bundle other products' UINs. Both rows carry a note.
- **Large version gap.** Tata AIA i Systematic Insurance Plan is 110L164V11 in the master list, but the only brochure online shows V04.

## Notes on this run

- I checked 2 products per insurer by hand: the UIN in the PDF, and the product name and description line on the first pages. An audit script also checked every stored file. It requires the product name on the first 4 pages and the UIN code in the text or OCR, and it rejects CIS, BI, rate-table, appendix and rider documents.
- The script reads the description line from the first 3 pages. It tries the layout text first, then plain text, then OCR at 400 and then 200 dpi, and collapses whitespace. Some PDFs lose the "ti" ligature, so "Participating" comes out as "Non-Par cipa ng". The odd-lines table lists those rows.
- `features_keyword_hits` records only whether a keyword appears. It does not verify the feature.
- A crashed re-extraction emptied `index.csv` once during the run. I rebuilt it from the results file and the stored files, recomputing hashes, sizes and page counts. The rebuilt rows matched the Bharti rows already in git, field for field. The script now writes `index.csv` through a temporary file. `scripts/check_consistency.py` confirms that every file in `docs/` has an index row and that every row's files exist.
- A second pass replaced 70 stored leaflets and one-pagers, and 10 fallback policy documents, with full brochures where the site has them.
- New helper scripts: `find_product_pages.py` (matches products to sitemap URLs and opens each URL before writing it), `map_pages_by_uin.py` (LIC's tables), `set_product_page.py`, `add_note.py`, `stage_insurers.py` (one-insurer commits), `check_consistency.py`, `build_coverage.py` and `build_summary.py`.
