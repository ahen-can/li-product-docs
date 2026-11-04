# Product taxonomy v1 (individual life products)

**Source of classification:** the IRDAI product description line printed on each brochure or policy document (e.g. *"A Non-Linked, Participating, Individual, Life Insurance Savings Plan"*), plus the UIN's linked flag (4th character L/N). When the description line names no plan type (5 products), the Life Insurance Council's category label is used, and that's marked in `sub_basis`. **No category is ever taken from a product name.**

## Level 1: market category (5) and PD category (4)

| Rule (description line / UIN) | Market category | PD category (public disclosure segment) |
|---|---|---|
| UIN = L (unit-linked) | **ULIP** | Linked (Pension & Annuity if "pension") |
| Non-linked + Participating | **Par** | Par Life (Pension & Annuity if pension/annuity) |
| Non-linked + Non-par + pure risk / term / protection | **Protection** | Non-Par Life |
| Non-linked + Non-par + annuity / pension / immediate / deferred | **Annuity** (retirement) | Pension & Annuity |
| Non-linked + Non-par + savings / endowment / whole life / money back | **Non-Par Savings** | Non-Par Life |
| "Micro" or "Health" in the description line | Out of scope | n/a |

## Level 2: sub-segments, from the description line and brochure feature evidence

**Protection**

| Sub-segment | Rule |
|---|---|
| Saral Jeevan Bima (standard term) | IRDAI standard product |
| Credit / loan / decreasing cover | Description line mentions loan or credit, or decreasing cover without a whole-life option |
| Term with savings element (ROP-type) | Description line says "pure risk premium / savings" |
| Term with ROP option | Brochure describes return of premium |
| Pure term with whole-life option | Cover to age 99/100 |
| Pure term | Everything else |

**Non-par savings**

| Sub-segment | Rule |
|---|---|
| Standard / POS savings | Standard or POS product |
| Whole-life guaranteed income | Guaranteed income + to age 99/100 |
| Guaranteed income + lump-sum (multi-option) | Both described |
| Guaranteed income | Guaranteed income only |
| Guaranteed maturity (endowment) | Everything else |

**Par**

| Sub-segment | Rule |
|---|---|
| Par pension | Pension or annuity par product |
| Par money-back | Periodic survival benefits / money back |
| Par whole life | To age 99/100 |
| Par income | Cash bonus or guaranteed income |
| Par endowment | Everything else |

**ULIP**

| Sub-segment | Rule |
|---|---|
| ULIP pension | Pension product |
| ULIP with return of mortality (TULIP-type) | Return of mortality charges |
| ULIP with payor / child benefit | Payor or parent waiver |
| ULIP wealth | Everything else |

**Annuity**

| Sub-segment | Rule |
|---|---|
| Saral Pension (standard immediate annuity) | IRDAI standard product |
| Immediate annuity | Description line says immediate |
| Deferred annuity / pension | Deferred / deferment |
| Annuity / pension (other) | Everything else |

The rules are applied in the order listed: the first match wins. A product with several plan options goes into the multi-option bucket where one exists, otherwise into its first matching sub-segment. v2 will review the edge cases by hand.

## v1 counts (516 products, 21 insurers)

Full grid by insurer: `feature_list_v1.xlsx` → *Coverage by sub-segment*.

| Category | Sub-segments (products) |
|---|---|
| Protection (98) | Pure term 34 · Term with ROP option 22 · Saral Jeevan Bima 21 · Term with savings element 16 · Pure term with whole-life option 5 |
| Non-Par Savings (127) | Guaranteed maturity 58 · Income + lump-sum 36 · Guaranteed income 17 · Whole-life income 10 · Standard/POS 6 |
| Par (86) | Endowment 29 · Whole life 22 · Money-back 15 · Income 14 · Pension 6 |
| ULIP (140) | Wealth 63 · Return of mortality (TULIP) 50 · Pension 18 · Payor/child 9 |
| Annuity (59) | Deferred 30 · Saral Pension 19 · Immediate 7 · Other 3 |
| Out of scope | Micro 5 · Health 1 |
