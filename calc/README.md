# IRR calculator (PolicyBazaar-style), driven by published documents

- `engine.py`: builds year-by-year cash flows from `params/<UIN>.json` and solves the IRR (survival case, pre-tax; GST optional).
- `params/<UIN>.json`: every factor and schedule taken from the insurer's brochure or policy document, with its source noted. Known discrepancies between documents are recorded in the file; the policy document (the contract) wins.

Usage: `python3 -I calc/engine.py <UIN> <age> <M|F> <annual_premium> <PPT>`

| Product | Data published? | Status |
|---|---|---|
| Bharti Income Laabh (130N122V04) | Yes: income % (brochure) + lump-sum factor table by age × band (policy doc App. V) | Exact |
| SBI Smart Platina Supreme (111N171V04) | No: "Guaranteed Income Factor varies by age/PPT/PT…", table not in brochure or policy document | Needs BI/quote |
| HDFC Sanchay Plus (101N134V30) | No: income "% of AP… refer to Policy Schedule" | Needs BI/quote |
| Tata AIA Fortune Guarantee Supreme (110N163V14) | Policy document is behind customer login | Needs BI/quote |
