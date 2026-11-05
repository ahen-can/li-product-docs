# Rider discovery: summary

Brief: `briefs/rider_discovery_brief.md`. Riders downloaded are listed in `results/riders_downloaded.csv`. Links from each ULIP to its riders are in `results/ulip_rider_map.csv`. Rider features are in `features/riders/<rider UIN>.json`, built by `scripts/rider_json.py` from `scripts/rider_specs/`.

## Counts per insurer

| Insurer | ULIPs | ULIPs with a rider found | Riders downloaded | Documents | Notes |
|---|---|---|---|---|---|
| Bharti Life | 7 | 6 | 2 | 4 | Future Invest names none |
| SBI Life | 7 | 5 | 2 | 4 | Smart Scholar Plus has waiver built in; Retire Smart Plus links none |
| HDFC Life | 7 | 4 | 5 | 10 | The deep data said none of the 7 name riders; the product pages and ULIP brochures do |
| Tata AIA | 14 | 12 | 7 | 13 | Rider pages publish newer versions than the ULIP documents name; OPD Care and 110A167V02 on the retry list. Linked Comprehensive Health is a brochure from a user upload |
| Bajaj Life | 11 | 11 | 3 | 6 | Goal Based Saving III and Supreme name riders in their documents, which the deep data had missed |
| Axis Max Life | 9 | 9 | 2 | 4 | All name both riders (Forever Young Pension only the second) |
| LIC | 5 | 4 | 1 | 2 | New Pension Plus names none |
| Aditya Birla Sun Life | 10 | 9 | 5 | 10 | Wealth Max Plus (109L073V05) names none |
| Canara HSBC | 8 | 3 | 2 | 4 | The Promise series ULIPs name none |
| Ageas Federal | 6 | 4 | 2 | 4 | Smart Growth and Golden Years name none |
| **Total** | **84** | **67** | **31** | **61** | |

Two lists are kept. `results/riders_downloaded.csv` has one row per document stored. `results/riders_universal.csv` lists the riders each insurer publishes on its riders page, with `download_status` (downloaded, not downloaded, or retry), so the rest can be fetched later.

## Bharti Life

Bharti's rider pages are at `bhartiaxa.com/riders-in-insurance/<rider>`. Each page links *Download Brochure* and *Policy Bond*.

| Rider | UIN | ULIPs that name it | Gives |
|---|---|---|---|
| Linked Complete Shield Rider | 130A012V02 | Grow Wealth, Wealth Pro, Wealth Maximizer, Growth Shield Plus, Dream Shield Plus, Grow Wealth Ultra | Accidental death, accidental total and partial disability, critical illness (standard 12 conditions, 15 for women; comprehensive 68; cancer care 5), and an optional waiver of premium |
| Cover Plus Linked Term Rider | 130A034V01 | Wealth Pro, Growth Shield Plus, Dream Shield Plus, Grow Wealth Ultra | Death cover from any cause. No waiver, critical illness or disability |

Future Invest names no rider.

**Waiver of premium.** It is inside the Linked Complete Shield Rider as an option, and applies on accidental total and permanent disability, a standard critical illness, or a major condition under comprehensive critical illness. It is not offered on death. The wording says the company waives "future premiums for the base cover along with other opted Rider options". The rider defines "Base Policy" as the ULIP, so the wording could mean the ULIP's premiums are waived, or only the rider's own. The documents do not settle it. This needs a Bharti answer.

**Critical illness and accident cover.** Wealth Pro, Growth Shield Plus, Dream Shield Plus, Grow Wealth, Wealth Maximizer and Grow Wealth Ultra reach critical illness, accidental death and disability only through the Linked Complete Shield Rider. None has them built in.

**How the rider is paid.** As a separate rider premium next to the ULIP premium, not as units cancelled from the fund. The ULIP brochures say "paying additional premium"; the rider documents do not mention the fund.

**Other Bharti rider pages, not named by any ULIP and not downloaded:** Premium Waiver Rider (130B005V05), Term Rider (130B009V03), Hospi Cash Benefit Rider, Group Accidental Death Benefit Rider, Non-Linked Complete Shield Rider and Non-Linked Group Complete Shield Rider. The brief covers only riders the 84 ULIPs name.

**Earlier work to fix.** Feature list v3 codes Bharti's waiver as "N" for all 7 and codes the rider's other benefits inconsistently across products (accident death, critical illness, disability). S1 recodes these from the rider JSONs.

## SBI Life

Riders: Accident Benefit Rider - Linked (111A042V01, accidental death and partial disability) and Waiver of Premium Rider - Linked (111A049V01). The waiver rider waives all future premiums under the base policy (the wording says "base policy"), on the death of the proposer (when proposer and life assured differ), accidental total permanent disability or 20 listed critical illnesses. Both riders are paid as a separate premium. Smart Fortune Builder, Smart Privilege Plus, eWealth Plus and Smart Invest Builder name both; Smart Elite Plus names only the waiver rider.

## HDFC Life

Five linked riders are linked from the product pages: Health Plus (101A034V01, 60 critical illnesses or cancer), Waiver of Premium (101A035V01, waives all outstanding premiums of the base policy on death, disability or 60 critical illnesses), LiveWell (101A036V02, death, accidental death, personal accident, daily hospital cash and wellness benefits), Protect Plus (101A037V01, personal accident, accidental death or cancer) and Income Benefit on Accidental Disability (101A038V01). Only the waiver rider waives the ULIP premium. The site's policy-documents page lists every live rider, which feeds the universal list. The LiveWell policy bond prints 101A036V01 while the product-page brochure prints V02.

## Tata AIA

Waiver of Premium (110A026V03, total and permanent disability only, waives the basic plan premiums), Waiver of Premium Plus (110A025V03, death or disability of a proposer who is not the life assured), ADDL (110A027V03), Linked Comprehensive Protection (110A032V05, term, accidental death, ATPD, 40 critical illnesses, waiver as a payout option), Vitality Health Plus (110A047V03) and Vitality Protect Plus (110A048V04, waiver of future premium as a payout option across the base plan and riders). The three linked riders with unit deduction take their charge from the base policy fund. ULIP documents name older versions (V02 and similar) that are not on the site.

## Bajaj Life, Axis Max, LIC, ABSLI, Canara HSBC, Ageas Federal

- **Bajaj Life.** Care Plus Rider (116A059V01: OPD benefits and an accidental total permanent disability lump sum; its waiver covers only the rider's own premium), Linked Accident Protection Rider II (116A057V03: accidental death and ATPD, each with or without return of premium) and Linked New Critical Illness Benefit Rider (116A060V01: 10, 25 or 60 conditions). Premium is separate. No Bajaj rider waives the ULIP premium.
- **Axis Max Life.** Smart Ultra Protect Rider (104A049V03) has a Payor Benefit: on the death or terminal illness of the policyholder (when different from the life insured) the company funds all future premiums under the base policy. Critical Illness and Disability Secure Rider (104A034V02): 22 or 64 critical illnesses, with or without total and permanent disability. Both are paid as level rider premium, not as a charge from units.
- **LIC.** Linked Accidental Death Benefit Rider (512A211V02). Accidental death only. The charge is Rs 0.40 per thousand a year, cancelled from units. LIC's riders page lists 7 riders; the other 6 are non-linked.
- **ABSLI.** Waiver of Premium Rider (109A039V01) waives all premiums on the proposer's disability, 4 critical illnesses or death. Also Accidental Death Benefit Rider Plus (109A024V01), Comprehensive Critical Illness Rider (109A041V01, Silver 10, Gold 25, Platinum 64 conditions), Suraksha Term Rider (109A042V01) and Suraksha Term Rider Plus (109A045V01).
- **Canara HSBC.** Accidental Benefit Rider (136A016V01: accidental death up to 3 times base cover, and ATPD; the brochure calls it non-linked) and Linked Critical Illness Benefit Rider (136A018V01: 40 illnesses). Neither waives premium.
- **Ageas Federal.** Linked Accident Care Rider (135A036V01: accidental death with 2X in air or train accidents, or a comprehensive option with ATPD) and Linked Critical Shield Rider (135A038V01: 30 or 50 illnesses). The waiver rider on the site (135B039V01) is non-linked. Its policy document file is hosted on a different storage account (sacicwputd01).

## Which ULIPs reach waiver, critical illness or accident cover only through riders

`results/ulip_rider_benefits.csv` has one row per ULIP. Of the 84 ULIPs, 44 name a rider that waives the ULIP's own premium (Bharti's counts as unclear, Axis Max's is a payor benefit on death or terminal illness only), 54 a rider with critical illness cover and 64 a rider with accidental death or disability. Insurers with no waiver of the ULIP premium in any named rider: Bajaj (the Care Plus waiver is the rider's own premium), Canara HSBC, Ageas Federal, LIC. Where a built-in benefit exists (SBI Smart Scholar Plus has waiver built in), the ULIP JSON records it.

## Open points

- **Bharti waiver wording.** "Future premiums for the base cover" may mean the ULIP's premium or only the rider's. Ask Bharti.
- **Version mismatches.** Tata AIA ULIP documents name older rider versions (V02) than the site publishes (V03 to V05). The LiveWell policy bond prints V01 and its brochure V02.
- **Retry list.** OPD Care (110A166V01) and 110A167V02. The "OPD Care" file the user uploaded is a Tata AIG General Insurance rider, not Tata AIA Life. The Linked Comprehensive Health Rider (110A031V02) came from a user upload (brochure only; its policy document is still missing). Fields marked "not stated" in the rider JSONs because the text read did not show them (premium deduction for several riders) need a second read.
- **Name quirks.** Canara's "Accidental Benefit Rider (Linked)" and Bharti's "Linked" riders are named for linked base policies, while their documents call them non-linked.

## Full rider harvest (5 Nov, all insurers)

`scripts/rider_harvest.py` crawls each insurer's rider pages (or sitemaps, or product pages), downloads every rider PDF and keeps a file only if it prints a rider UIN of that insurer. It skips product brochures that only mention a rider. `scripts/s2_tools/rider_prune.py` re-checks the stored files, and `results/rider_harvest_log.csv` records every link tried and its outcome.

- **Council list (225 riders, 23 insurers):** 149 stored, 110 of them with both brochure and policy. Another 29 riders are on the sites but not in the Council list (other versions or not listed), giving 254 rows in `results/riders_universal.csv`.
- **Documents stored:** 372 rider documents (148 brochures, 142 policy documents, 37 CIS, 22 leaflets, 23 untyped).
- **Complete:** Ageas, Bajaj, Canara HSBC, Edelweiss, IndiaFirst and PNB MetLife have every Council rider.
- **Blocked sites:** ICICI (9), Kotak (17) and Star Union Dai-ichi (6) were not contacted. Their 32 riders need manual download.
- **Not found (44):** Generali 11, IndusInd Nippon 8, Pramerica 5, SBI 5, Acko 3, ABSLI 3, Aviva 2, Bandhan 2, Shriram 2, Axis Max 1, LIC 1, Tata AIA 1. IndusInd and Acko have no rider pages that link documents; the others' remaining riders are not linked from the pages read.
- Rider JSONs (features) exist only for the 31 riders the 84 ULIPs name. The rest are stored documents only.
