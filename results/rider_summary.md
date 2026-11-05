# Rider discovery: summary

Brief: `briefs/rider_discovery_brief.md`. Riders downloaded are listed in `results/riders_downloaded.csv`. Links from each ULIP to its riders are in `results/ulip_rider_map.csv`. Rider features are in `features/riders/<rider UIN>.json`, built by `scripts/rider_json.py` from `scripts/rider_specs/`.

## Counts per insurer

| Insurer | ULIPs | ULIPs with a rider found | Riders downloaded | Documents | Notes |
|---|---|---|---|---|---|
| Bharti Life | 7 | 6 | 2 | 4 | Future Invest names none |
| SBI Life | 7 | 5 | 2 | 4 | Smart Scholar Plus has waiver built in; Retire Smart Plus links none |
| HDFC Life | 7 | 4 | 5 | 10 | The deep data said none of the 7 name riders; the product pages and ULIP brochures do |
| Tata AIA | 14 | 12 | 6 | 12 | Rider pages publish newer versions than the ULIP documents name; Linked Comprehensive Health and OPD Care on the retry list |

Bajaj, Axis Max, LIC, ABSLI, Canara HSBC and Ageas Federal follow.

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
