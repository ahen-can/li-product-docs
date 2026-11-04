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

## ULIP calculator (pilot, 4 Nov 2026)

`calc/ulip.py` projects a ULIP fund month by month from the charges printed in the policy document. Each month it applies the allocation charge on each premium, the admin charge, the mortality charge on the sum at risk, fund growth and the fund management charge, adding 18% GST to every charge. At year ends it adds loyalty additions, boosters and charge refunds. Each product's parameters are in `calc/params/ulip/<UIN>.json`, with page references. `calc/tools/make_ulip_params.py` writes them, and `calc/tools/extract_mortality.py` reads the mortality table from the policy text.

Run `python3 -I calc/ulip.py` to print all products. Results are in `calc/results_ulip.csv`, with fund values by year in `calc/results_ulip_by_year.csv`.

Standard profile: male, age 30, Rs 1,00,000 a year, premiums for 10 years, policy term 20 years, cover 10x annual premium, equity fund (FMC 1.35%), survival to maturity. Grow Wealth Ultra needs at least Rs 2,50,000 a year, so it uses that.

| Product | Net yield at 4% | Net yield at 8% | Reduction in yield at 8% |
|---|---|---|---|
| Bharti Wealth Maximizer | 2.81% | 6.59% | 1.41% |
| Bharti Grow Wealth Ultra (Rs 2.5 lakh) | 2.53% | 6.39% | 1.61% |
| HDFC Click 2 Wealth | 2.36% | 6.29% | 1.71% |
| SBI eWealth Plus | 2.14% | 6.10% | 1.90% |
| Bharti Wealth Pro | 2.01% | 5.85% | 2.15% |
| HDFC Sampoorn Nivesh Plus | 1.74% | 5.80% | 2.20% |

Checks done: with every charge set to zero, the net yield equals the gross rate. Not done yet: comparison with official benefit illustrations, which none of these insurers publishes. Treat these numbers as unchecked until the user supplies BIs for the same profile.

Known simplifications:
- Mortality uses age last birthday at the start of each policy year.
- Customer-specific boosters are left out: Grow Wealth Ultra's EmpowHer, ECS and existing-customer boosters, and Sampoorn Nivesh Plus's direct-channel reward.
- Wealth Maximizer's 118% refund is paid at the end of years 11 to 15.
- Where the policy document doesn't say whether GST applies to a refund, refunds exclude GST.
