# How we choose the ~10 insurers to compare in each category

## Recommended (option A): "leaders by coverage + scored challengers + Bharti"
1. **Leaders (up to 7):** the smallest set of insurers that together hold **≥80% of the category's premium**. Source: FY26 public disclosures, L-1-A-RA segment premium; total premium, since new business by segment isn't disclosed.
   - **LIC** is kept as a **reference column** ("best ideas"), not as a direct peer.
2. **Challengers (3):** from insurers with **≥0.5% category share** that aren't leaders. Score out of 1:

   | Factor | Weight | How it's measured |
   |---|---|---|
   | Feature richness | 40% | Features described across the insurer's products in the category (union), from feature list v1, scaled to the best candidate |
   | Specialisation | 30% | Specialist index = category share of the insurer's own book ÷ industry average (capped at 2.0 = full marks). Your "over-indexed, maybe doing something right" idea. |
   | Growth | 20% | FY26 vs FY25 category premium, **only if the book is ≥ ₹500 cr**, which guards against tiny bases; +60% = full marks |
   | Expert nomination | 10% | 1 point if seniors or industry friends name the insurer as innovative in the category |

   Missing data (e.g. no brochures for blocked sites) is left out and the weights re-normalised. Such rows are flagged.
3. **Bharti** is always included as the anchor.
4. **Then compare products:** within each chosen insurer, all current products in the category (ULIP pilot), or for the deck, the product matching Bharti's sub-segment (like-for-like).

## Alternatives
- **B. Top 10 by share:** simplest and easy to defend, but it picks only the big players and has no innovator view.
- **C. Expert-led:** seniors name 10. Quick, but subjective and hard to explain in a deck.
- **A is a blend of both,** reproducible from data, with one expert lever.

## ULIP application (FY26; industry ULIP premium ₹1.94 lakh cr; ULIP = 19.6% of the industry book)

**Leaders: 84.1% of ULIP premium**

| # | Insurer | ULIP premium (₹ cr) | Share | Cumulative |
|---|---|---|---|---|
| 1 | SBI Life | 54,243 | 27.9% | 27.9% |
| 2 | ICICI Life | 24,718 | 12.7% | 40.7% |
| 3 | HDFC Life | 24,209 | 12.5% | 53.1% |
| 4 | LIC (reference) | 22,939 | 11.8% | 65.0% |
| 5 | Tata AIA | 13,896 | 7.2% | 72.1% |
| 6 | Bajaj Life | 12,110 | 6.2% | 78.4% |
| 7 | Axis Max Life | 11,198 | 5.8% | 84.1% |

**Challenger scores** (feature richness = union of 36 ULIP v1 features)

| Insurer | Share | Specialist index | YoY | Features | Score |
|---|---|---|---|---|---|
| **Aditya Birla Sun Life** | 4.5% | 1.89 | +61% | 27/36 | **0.88** |
| **Canara HSBC Life** | 2.0% | 2.00 | +34% | 24/36 | **0.77** |
| Ageas Federal Life | 0.6% | 1.73 | +22% | 22/36 | 0.66 |
| Star Union Dai-ichi | 1.1% | 1.14 | +54% | n/a (blocked site) | 0.63* |
| IndiaFirst Life | 1.1% | 1.38 | +17% | 22/36 | 0.59 |
| PNB MetLife | 1.7% | 1.31 | +1% | 24/36 | 0.56 |
| Kotak Mahindra Life | 2.9% | 1.36 | +27% | n/a (blocked site) | 0.53* |
| IndusInd Nippon Life | 0.5% | 0.87 | −6% | 22/36 | 0.46 |

\* The feature part is missing, so the score is re-normalised. The expert-nomination 10% isn't applied yet for anyone.

**Result:** ABSLI and Canara HSBC are clear picks. **The third slot is a judgement call:**
- **Ageas Federal:** best by formula; a small ULIP specialist; documents available now.
- **Kotak:** bigger (#9 by share, would take coverage to 91.6%), but documents need your manual upload.
- **Star Union Dai-ichi:** fast-growing, but blocked.

**Decision (user, 4 Nov):** Ageas Federal is the third challenger. Its 6 ULIPs are in wave 1 of the deep set. Kotak stays in wave 2 as an optional extra once its documents are uploaded.

**Anchor: Bharti Life:** ₹563 cr, 0.3% share, #16; ULIP = 17.3% of its book (specialist index 0.88); +48% YoY.

Scores are reproducible: inputs are the phase-1 data and `analysis/product_features_v1.csv`.

## Output size (user, 4 Nov)
The deck shows **5 products per category**: Bharti's flagship plus 4 peers (top leaders plus at most one innovator, adjusted by the user's "My view" tab). The supporting Excel shows **10 to 15 products per category**, chosen from the leaders' and challengers' flagships, Bharti's top products by NBP, and LIC as a reference column.
