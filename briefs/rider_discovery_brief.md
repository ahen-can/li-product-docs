# Brief for S2: rider documents for the 84 wave 1 ULIPs

## Why
Features such as waiver of premium, critical illness, accidental death and disability often reach the customer only through a rider. Without the rider's own document we can't say what a ULIP really offers. Example: is waiver of premium inside Bharti's Linked Complete Shield Rider? Wealth Pro's brochure only says "additional sum assured… in case of happening of a covered event". This pass collects the riders our 84 ULIPs name. It does not collect every rider in the market.

## Scope
`briefs/ulip_riders_named.csv` lists, for each of the 84 ULIPs, the riders the deep data found. 48 products name rider UINs (27 distinct UINs). The other 36 name riders without UINs, say "riders as offered from time to time", or name none (all 7 HDFC products). For those, look on the product page and brochure for the riders offered with that ULIP. HDFC product pages link rider brochures (`results/site_quirks.md`).

**Order:**
1. **Bharti first.** Linked Complete Shield Rider 130A012V02, Cover Plus Linked Term Rider 130A034V01, and any other rider a Bharti ULIP names. Push and post in CHAT as soon as Bharti is done: S3 needs these for its QA (`qa/s3_v3/s3_v3_qa_brief.md`, tab C) and can then skip its own download.
2. **Then the peers,** in the wave 1 order.

## Per rider
1. **Documents.** Store the rider's brochure and its policy document (or rider terms) in `docs/<insurer>/riders/<rider UIN>/brochure.pdf` and `policy.pdf`. Add `index.csv` rows (doc_type `rider_brochure` / `rider_policy`), with the site's own label and the usual checks: `%PDF`, `pdfinfo`, UIN in the text. Extract text to `text/<insurer>/riders/<rider UIN>/`.
2. **`features/riders/<rider UIN>.json`.** For each field give value, status, document, page and a value-bearing quote, as in the ULIP files:
   - name, UIN, linked or non-linked;
   - benefits covered, each as covered / not covered / not stated:
     - waiver of premium (on death, disability or critical illness of the life assured or the proposer);
     - critical illness (number of illnesses, lump sum or staged);
     - accidental death;
     - accidental disability;
     - term cover;
     - hospital cash;
     - other;
   - rider term and premium-paying rules;
   - entry ages;
   - sum assured limits;
   - how the rider premium or charge is deducted (from the fund as units, or paid as a separate premium).
3. **`results/ulip_rider_map.csv`.** One row per ULIP and rider, with columns: ulip_uin, rider_uin, rider_name, where the link is stated (document and page), and benefits covered (a short list).

## Rules
The same as the deep pass: insurer sites only, 1 request a second, no getting around bot protection, never invent a URL. If a rider page or document can't be found after a reasonable search, park it on a retry list and move on.

## When done
- Write `results/rider_summary.md`: counts per insurer and which ULIPs reach waiver of premium, critical illness or accident cover only through riders.
- Post a short CHAT entry for `@S1`.

S1 will then recode the rider-delivered features in feature list v3.
