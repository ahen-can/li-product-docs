# Tata AIA fund codes (SFIN) and FMC as printed in the "Fund Management Charges (FMC)" table of the policy documents.
FUNDS = {
 'Whole Life Mid Cap Equity Fund': ('ULIF 009 04/01/07 WLE 110', 1.20), 'Large Cap Equity Fund': ('ULIF 017 07/01/08 TLC 110', 1.20),
 'Multi Cap Fund': ('ULIF 060 15/07/14 MCF 110', 1.20), 'India Consumption Fund': ('ULIF 061 15/07/14 ICF 110', 1.20),
 'Super Select Equity Fund': ('ULIF 035 16/10/09 TSS 110', 1.20), 'Top 50 Fund': ('ULIF 026 12/01/09 ITF 110', 1.20),
 'Top 200 Fund': ('ULIF 027 12/01/09 ITT 110', 1.20), 'Emerging Opportunities Fund': ('ULIF 064 12/09/22 EOF 110', 1.20),
 'Sustainable Equity Fund': ('ULIF 065 12/09/22 ESG 110', 1.20), 'Dynamic Advantage Fund': ('ULIF 066 12/09/22 DAF 110', 1.20),
 'Flexi Growth Fund': ('ULIF 068 25/04/23 FGF 110', 1.20), 'Small Cap Discovery Fund': ('ULIF 071 22/05/23 SCF 110', 1.20),
 'Rising India Fund': ('ULIF 073 17/01/24 RIF 110', 1.20), 'Flexi Growth Fund II': ('ULIF 074 02/05/24 FG2 110', 1.35),
 'Whole Life Income Fund II': ('ULIF 076 06/06/24 WI2 110', 1.35), 'Nifty Alpha 50 Index Fund': ('ULIF 077 30/09/24 NAF 110', 1.35),
 'Multicap Momentum Quality Index Fund': ('ULIF 078 31/12/24 MQI 110', 1.35), 'Tax Bonanza Consumption Fund': ('ULIF 088 31/03/25 TBC 110', 1.35),
 'Top 200 Alpha 30 Index Fund': ('ULIF 090 30/06/25 TAF 110', 1.35), 'Momentum 50 Index Fund': ('ULIF 092 25/08/25 MFI 110', 1.35),
 'Sector Leaders Index Fund': ('ULIF 093 15/09/25 SLI 110', 1.35), 'Multicap Opportunities Fund': ('ULIF 095 31/12/25 MUF 110', 1.35),
 'Enhanced Value Index Fund': ('ULIF 098 16/02/26 EVI 110', 1.35),
 'Whole Life Aggressive Growth Fund': ('ULIF 010 04/01/07 WLA 110', 1.10), 'Whole Life Stable Growth Fund': ('ULIF 011 04/01/07 WLS 110', 1.00),
 'Whole Life Income Fund': ('ULIF 012 04/01/07 WLI 110', 0.80), 'Whole Life Short Term Fixed Income Fund': ('ULIF 013 04/01/07 WLF 110', 0.65),
 'Target Maturity Fund': ('ULIF 070 17/05/23 TMF 110', 0.80),
}
FUNDS.update({'Constant Maturity Fund': ('ULIF 069 17/05/23 CMF 110', 0.80), 'Business Cycle Fund': ('ULIF 072 15/01/24 BCF 110', 1.20), 'Midcap Momentum Index Fund': ('ULIF 075 09/05/24 MIF 110', 1.20)})
FUNDS.update({'Large Mid Cap Innovation Fund': ('ULIF09931/03/26LARMIDINNL110', 1.35), 'Multifactor Index Fund': ('ULIF10230/06/26MFACTINDXL110', 1.35),
              'Momentum Value 50 Index Fund': ('ULIF10330/09/26MOMV50INDX110', 1.35), 'Liquid Fund': ('ULIF 003 04/02/04 TLL 110', 0.90)})   # from Tata AIA Shubh SIP 2026 table
NO_SFIN = {}   # codes read from the Smart Sampoorna Raksha FMC table, where they are not split
def funds(names=None, override=None):
    names = names or list(FUNDS)
    override = override or {}
    return [{'name': n, 'SFIN': FUNDS[n][0].replace(' ', '') if n in FUNDS else None, 'FMC_pct': override.get(n, FUNDS[n][1] if n in FUNDS else NO_SFIN.get(n)),
             'asset_allocation': 'see policy document Schedule of Funds', 'risk_label': None} for n in names]
