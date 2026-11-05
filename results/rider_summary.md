# Rider discovery: summary

Brief: `briefs/rider_discovery_brief.md`. Riders downloaded are listed in `results/riders_downloaded.csv`. Links from each ULIP to its riders are in `results/ulip_rider_map.csv`. Rider features are in `features/riders/<rider UIN>.json`, built by `scripts/rider_json.py` from `scripts/rider_specs/`.

## Counts per insurer

| Insurer | ULIPs | ULIPs naming a rider | Riders named | Riders downloaded | Retry list |
|---|---|---|---|---|---|
| Bharti Life | 7 | 6 | 2 | 2 (4 documents) | none |

Peers follow in the wave 1 order.

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
