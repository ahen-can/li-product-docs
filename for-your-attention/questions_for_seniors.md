# Questions for insurance-product experts (taxonomy and scope)

Context: we classify about 630 individual life products from each brochure's IRDAI description line (e.g. "A Non-Linked, Participating, Individual, Life Insurance Savings Plan"). We then group them into 5 market categories and about 25 sub-segments, and compare features. Rules are in `analysis/taxonomy.md`. These are the judgement calls we'd like an expert view on.

## A. Categories
1. **Pension products:** we map non-par deferred pension plans (e.g. "Non-Linked, Non-Participating, Individual Savings Pension Plan") to **Annuity / retirement**; ULIP pension to **ULIP**; par pension to **Par**. Is that how the market and management reporting would group them?
2. **"Pure risk premium / savings" products** (e.g. return-of-premium term, SBI Saral Swadhan Supreme): we treat them as **Protection** (sub-segment "term with savings element"). Should they count as savings instead?
3. **Whole-life guaranteed income** (non-par, income to age 99/100): a separate sub-segment or just "guaranteed income"?
4. **Child plans:** we don't create a child category. Child products sit in their construction category (par / non-par / ULIP) with a "payor / parent waiver" flag. OK, or should "Child" be its own segment as many insurers market it?
5. **Saral Jeevan Bima / Saral Pension / POS products:** kept and tagged, and they will usually be **excluded from like-for-like comparisons** because they are IRDAI standard products. Agree?
6. **"Individual/Group" annuity products** (description line says both): treat as individual?
7. **Credit / loan protection sold to individuals:** keep it in Protection, or exclude it like group credit life?
8. **Combination offerings without their own UIN** (e.g. a ULIP + health bundle): exclude, or analyse as a proposition?

## B. Sub-segments used for comparison (like-for-like)
9. **Protection:** pure term / term with ROP option / term with savings element / whole-life term / credit / Saral. Is this the right split for comparing Bharti's term plans?
10. **Non-par savings:** guaranteed maturity (endowment) / guaranteed income / income + lump-sum (multi-option) / whole-life income / standard-POS. Is "multi-option" a fair bucket, given most modern plans offer both income and lump-sum variants?
11. **Par:** endowment / money-back / income (cash bonus) / whole life / pension. OK?
12. **ULIP:** wealth / ULIP with return of mortality charges ("TULIP-type") / pension / payor-child. Is "return of mortality charges" the right marker for protection-oriented ULIPs, or should we use the sum-assured multiple (e.g. ≥ 25x)?
13. **Annuity:** immediate / deferred / Saral Pension / other. Should NPS-annuity and joint-life variants be split out?

## C. Comparison approach
14. **Comparison set per category:** leaders covering ~80% of category premium (from public disclosures), plus 3 challengers (scored on feature richness, specialisation and growth), plus Bharti. **LIC is shown as a reference column**, not a peer. Agree?
15. **Market share basis:** we use **total premium** (first year + renewal + single) from the public-disclosure segment accounts. New-business premium by segment isn't disclosed per insurer. Is total premium acceptable, or do you have a better source for NBP/APE by category?
16. **Features most valued by customers and distributors** in each category: which 5–10 matter most? This will set the order of rows in the comparison and the deck.
17. **Data not in public documents** that you could source: fund ratings, product-level sales or AUM, premium quotes for standard profiles, persistency by product, mortality rates where they're "as per policy schedule".

## D. Calculator
18. **IRR basis:** we plan to show pre-tax, survival-scenario IRR excluding GST, at 4% and 8% gross for ULIP/par. Is that the industry convention for comparisons, or should GST and tax be included?
19. **Standard customer profiles:**
    - savings: 35-year-old, ₹1 L/yr, 10 years pay, 20-year term;
    - ULIP: 30-year-old, ₹1 L/yr, 10 years pay, 20-year term;
    - term: 30-year-old male non-smoker, ₹1 cr, 30-year term;
    - annuity: 60-year-old, ₹10 L.

    Are these representative?
