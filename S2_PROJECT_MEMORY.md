# S2 project memory: read this first if you are S2

Last updated: 4 Nov 2026 by S2. S1's project memory is in `PROJECT_MEMORY.md`. Live coordination is in `coordination/CHAT.md`. This file holds what S2 needs to resume the ULIP deep discovery after a restart or a compacted chat.

## Role and branch
- S2 is the user's second Claude session. It works on branch `ccr-d0d84e00-joo2mp` and never pushes to `main`. S1 merges the branch into `main`.
- Before work, run `git fetch origin main` and merge it into the branch. Then read the top of `coordination/CHAT.md`. If CHAT.md conflicts, keep every entry from both sides, newest first.
- Force push is blocked. Merge instead of rewriting pushed history.
- End commits with:
  ```
  Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
  Claude-Session: https://claude.ai/code/session_01CUAfyogotnTRvsfH5LoNgf
  ```
- Push once per insurer. Write one short CHAT entry per insurer. Keep replies to the user to 2 or 3 lines, and put the detail in `results/deep_ulip_summary.md` (S1 ask, 4 Nov).
- Follow the unslop writing rules in `CLAUDE.md` for everything written.

## Task
- The brief is `briefs/deep_discovery_ulip_brief.md`. The product list is `briefs/ulip_deep_set.csv` and the schema is `briefs/ulip_feature_schema.json`.
- Wave 1 is 84 products, after the user added Ageas Federal on 4 Nov.
- **Done: 35.** Bharti 7, SBI 7, HDFC 7, Tata AIA 14. All pass validation.
- **Next, in this order:** Bajaj (11), Axis Max (9), LIC (5), ABSLI (10), Canara HSBC (8), Ageas Federal (6).
- Wave 2 (ICICI, Kotak) waits for the user's manual uploads.

## User decisions (4 Nov)
- **Quote rule.** S1 asked that every quote contain the value itself; a label such as "Minimum Entry Age:" alone is not evidence. If the value is in a table, quote the table row.
  - Apply the rule from Bajaj onwards.
  - Redo the older quotes at the end of wave 1.
- **Extra quotes.** A table too long for one 300-character quote uses `quote_2` to `quote_4` (with `page_2` to `page_4`) in `F(...)`. The validator checks all of them.
- **Exception, before Bajaj (done 4 Nov).** Redo now only the charge, eligibility and addition fields for the six products S1's calculator uses:
  - 130L100V03, 130L123V01, 130L121V01, 111L147V01, 101L133V03, 101L180V01.
  - Charge tables become nested numbers read from the layout text.
  - The mortality charge note gives the page range of the rate table in the policy document.
- **Other S1 asks.**
  - Redo Bharti Grow Wealth Ultra's (130L128V01) admin charge as a table on the second pass.
  - The SBI second-pass fields are done.
- **Tata i Systematic (110L164V11).** The user will supply the V11 documents. Until then, its JSON uses the V04 brochure, with every value flagged.

## How a product gets done
1. **Collect.** Run `python3 -I scripts/deep_collect.py --insurer <slug> --dry-run` to see the links per product page, then run it without `--dry-run`.
   - Use `--extra-page URL` for central document pages; HDFC needs its `/policy-documents` and `/brochures` pages.
   - The collector checks `%PDF`, `pdfinfo`, the 95 MB limit and the UIN, and OCRs image PDFs.
   - It writes `results/deep_ulip_docs.csv`, `index.csv` (with a `website_label` column), `docs/` and `text/`.
   - It skips page assets (css, js, images).
   - It skips fund factsheets that don't name the product.
2. **Read.**
   - Tools are in `scripts/s2_tools/`:
     - `kw.py UIN` prints key passages and the brochure eligibility page.
     - `tdig.py UIN [areas]` is a Tata-style digest by clause.
     - `rd.sh PDF a b` prints compact pages.
     - `tata.sh` prints the text between two headings.
     - `rowq.py PDF PAGE REGEX N` joins N layout lines into one quote string for a table row.
   - Dashes and hyphens at line ends vanish in the validator's matching, so leave them out of quotes ("Year 2 5.0%", not "Year 2 - 5.0%").
   - `scripts/ulip_digest.py` is a general reading aid.
   - Read charge tables with `pdftotext -layout`. Take quotes from the plain reading-order text.
3. **Spec.** Write `scripts/ulip_specs/<UIN>.py` with `F(value, status, doc_label, page, quote, note)` and `NS()` from `scripts/ulip_json.py`.
   - Shared helpers: `bharti_common.py`, `sbi_common.py`, `hdfc_common.py` and `tata_common.py`, which holds the Tata fund codes and FMCs.
   - `doc` is the website label. Unlabelled links are cited by file name.
   - The page is found automatically from the quote.
   - Twin products can be copied from a sibling spec with string replacements; check every replacement hit.
4. **Check.**
   - `python3 -I scripts/validate_ulip_json.py <UIN>` checks that every quote is verbatim on its page.
   - `python3 -I scripts/check_consistency.py` must report 0 problems.
   - Delete `scripts/__pycache__` before committing.
5. **Summary.** Add the insurer's row, two spot checks, odd findings, new features, `data_not_public` and gaps to `results/deep_ulip_summary.md`.
6. **Commit.** Use `git add docs/<slug> text/<slug> index.csv features/ulip results/deep_ulip_docs.csv results/deep_ulip_summary.md scripts`. The message is "Deep ULIP: <insurer> (<n> products, <m> policy docs, <k> BIs)". Push with `scripts/s2_tools/pushit.sh`, which retries and confirms against the remote.

## Lessons
- **Two-column PDFs (Tata).** Quotes often survive only in short pieces. When a quote fails, grep the plain text for the exact wording; Tata twins differ in small words ("Saving" or "Savings", "Rs." or "INR").
- **Ligatures and hyphens.** Some PDFs drop the "ti" and "fi" ligatures or hyphenate at line ends. The validator allows for both.
- **Image-only brochures.** OCR them. If no UIN is found, don't store the file; record it as failed with a note.
- **Process kills.** Never use `pkill -f` with a pattern that also appears in the shell command.
- **OCR stalls.** Run tesseract with a 120-second timeout and `OMP_THREAD_LIMIT=1`.
- **Field edits.** When editing many fields with a script, replace exact strings. A bracket-counting edit broke a spec once.
- **Session restarts.** The worker can restart mid-task. Commit locally often, but push only finished insurers.

## Open items and retry list
- **Tata i Systematic V11.** Waiting for the user's upload.
- **Tata SSR Pro (110L172V03).** Eligibility is not stated, because its only brochure is image-only without a UIN.
- **Tata Smart Pension Secure (110L182V09).** Fund names are not mapped to their codes.
- **Old quotes.** Redo the label-only quotes in the 35 files at the end of wave 1. A rough scan flags about 360 fields with numbers in the value but none in the quote, and some of those are fine ("three years").
- **No BIs.** None of the four insurers done so far publishes BIs or product-specific fund factsheets.
