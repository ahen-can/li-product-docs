# Start here: read PROJECT_MEMORY.md (project state, decisions, next steps) and coordination/CHAT.md before doing anything.

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

## Writing style (unslop)
Apply these rules to everything you write in this repo or report to the user: docs, notes in CSVs, commit messages, summaries and chat replies. Scan for the patterns, then rewrite. Keep the meaning and match the intended tone. Rule numbers are stable ids; a removed rule leaves a gap.

Content
- 3. No superficial -ing phrases ("highlighting...", "ensuring...", "reflecting...", "showcasing...", "fostering..."). Delete them or expand with real sources.
- 5. No vague attributions ("Experts believe", "Industry reports suggest"). Name the source or delete.

Language
- 7. No AI vocabulary: additionally, crucial, delve, enduring, enhance, fostering, garner, interplay, intricate, landscape (abstract), pivotal, showcase, tapestry (abstract), testament, underscore, vibrant. Use plain words.
- 8. Say "is" or "has", not "serves as", "stands as", "boasts" or "features".
- 9. No "not just X, but Y". State the point directly.
- 10. Don't force ideas into groups of three. Use the natural number.
- 11. No synonym cycling. Pick one term and repeat it.
- 12. No false ranges ("from X to Y" where X and Y are not on a real scale). List the items.

Style
- 13. No em dashes. Use periods or commas only: no parentheses, en dashes or hyphens standing in for dashes. To separate a thought, end the sentence or use a comma.
- 14. Colons only before a list or example, not as mid-sentence connectors.
- 15. Don't bold every proper noun or acronym.
- 16. No inline-header lists where a bold label and colon restate the line ("**Performance:** Performance improved..."). Write prose. A bold lead-in that ends in a period, names the item and is followed by new detail ("**Schema in TypeScript.** Tables live in one file.") is fine.
- 17. Sentence case for headings.
- 18. No decorative emojis.
- 19. Straight quotes, not curly quotes.

Communication
- 20. No chatbot phrases ("I hope this helps!", "Let me know if...", "Certainly!").
- 22. No sycophancy ("Great question!", "You're absolutely right!"). Respond directly.

Filler
- 23. Cut filler: "in order to" becomes "to", "due to the fact that" becomes "because". Delete "it is important to note that".
- 24. No stacked hedges: "could potentially possibly be argued that it might" becomes "may".
- 25. No generic conclusions ("The future looks bright."). State specific plans or facts.

Jargon
- 26. Use the concrete word, not an abstract metaphor noun: substrate (base), wedge, vector (way, method), locus, vantage, nexus, primitive as a noun, harness as a metaphor, surface as in "API surface", bedrock, scaffolding as a metaphor, modality, paradigm, gold-plating, ratchet as a metaphor, evacuate for moving code, endgame, north star, flywheel.

Plain speech
- 27. Say what it does, not how it feels. Name the mechanism or a number. If a sentence can't be restated as a concrete instruction, fact or number, cut it. If it could appear unchanged in another project's docs, cut it.
- 28. Shorten or split dense sentences. One idea per sentence.
- 29. Prefer active voice. Catch "is/are/was/were + past participle" and name the actor. Passive is fine only when the actor is unknown or doesn't matter.
- 30. Cut adverbs or use a stronger verb. "Runs quickly" becomes "is fast" or the number.
- 31. Prefer the plain word: "utilize" and "leverage" become "use", "facilitate" becomes "help", "numerous" becomes "many", "in the event that" becomes "if".
- 32. No mannered prose: aphorisms, rhetorical fragments, personified code, figurative verbs ("rides along", "stands on"), stock framing phrases. Say what you mean.
- 33. No over-compression: dropped articles, verbless fragments, arrows, symbol-speak or unexplained abbreviations. "Parser rejects bad date -> exit 2, no write" becomes "The parser rejects a bad date, exits with code 2, and writes nothing."
