# Rules for agents working in this repo

Read README.md for the layout and the index.csv schema. These rules are not optional.

## Provenance
- Every file in `docs/` must have exactly one row in `index.csv`. The row records the **exact `source_url`** the bytes came from and the `found_on_page_url` where the link appeared.
- Download only from the insurer's own website (or irdai.gov.in / lifeinscouncil.org). Never use aggregators, document-sharing sites or caches.
- **Never invent or guess a URL and record it as a source.** You may try a URL pattern, but log it only if it returned a real PDF.
- Keep the original bytes. Never edit, compress or re-save a PDF.

## Validity checks before committing a file
- The response body starts with `%PDF` (an HTML error page saved as .pdf is a failure), and `pdfinfo` opens it.
- The UIN printed in the document matches the product's UIN. If the document shows a different version (e.g. V02 vs V03), keep it and record that in `notes`. Never silently relabel.
- sha256 dedupe: the same file linked for two products gets two index rows pointing to one stored file (record this in `notes`).

## Text
- `pdftotext -layout` into `text/…/<doc_type>.txt`. If a document yields under 200 characters per page, it is scanned: OCR it (`ocrmypdf` or `tesseract`), set `is_scanned=Y`, and keep the original PDF.

## Etiquette and limits
- At most 1 request per second per insurer domain, with a normal desktop browser User-Agent and no parallel hammering.
- Commit and push **one insurer at a time**: `git add docs/<slug> text/<slug> index.csv coverage.md`. Keep each push well under 2 GB, and never add a file over 95 MB (record it as `manual` instead).
- If a site blocks automation (captcha, 403 after a JS check), stop on that site. Record its products as `manual` in `coverage.md`, with the page URL the user should visit.

## Honesty
- `coverage.md` must state counts truthfully: found, failed, manual, not published. "Not published" is only for products whose page has no such document link.
- When unsure whether a file is the right product or version, mark it `status=ok` with a note, or `failed`. Never drop the uncertainty.
