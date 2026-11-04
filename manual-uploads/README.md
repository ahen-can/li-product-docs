# Manual uploads

Documents from sites that block automated access go here. The user downloads them in a browser and uploads them on GitHub. S2 then moves each file into `docs/<insurer>/<UIN>/`, adds an `index.csv` row and extracts the text.

## How to upload on GitHub (web)
1. Open https://github.com/ahen-can/li-product-docs/tree/main/manual-uploads/icici-life
2. Click "Add file", then "Upload files".
3. Drag in the PDFs. Name each one `<UIN>_<type>.pdf`, where type is `policy`, `brochure` or `cis`. Example: `105L177V13_policy.pdf`.
4. Under "Commit changes", choose "Commit directly to the main branch" and click "Commit changes".
5. Fill in `sources.csv` in the same folder (click it, then the pencil icon): one row per file with the page you downloaded it from. Our provenance rule needs the source page; the exact file URL is a bonus if you can copy it.

GitHub's web upload takes files up to 25 MB each and 100 files per upload.
