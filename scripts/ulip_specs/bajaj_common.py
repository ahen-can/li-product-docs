# Bajaj Life fund FMCs as printed in the "Fund Management Charge" tables of the 2026 brochures and policy documents.
# SFINs are printed in the policy fund tables but split across lines, so they are left out.
FMC = {'Accelerator Mid Cap Fund II': 1.35, 'Asset Allocation Fund II': 1.25, 'Bluechip Equity Fund': 1.25, 'Bond Fund': 0.95, 'Equity Growth Fund II': 1.35,
       'Liquid Fund': 0.95, 'Pure Stock Fund': 1.35, 'Debt Plus Fund': 0.70, 'Long Term Debt Solution Fund': 0.70, 'Nifty Alpha 50 Index Fund': 1.35,
       'Nifty 200 Alpha 30 Index Fund': 1.35, 'Focused 25 Fund': 1.35, 'Pure Stock Fund II': 1.30, 'Flexi Cap Fund': 1.35, 'Sustainable Equity Fund': 1.35,
       'Small Cap Fund': 1.35, 'Dynamic Asset Allocation Fund': 1.35, 'Individual Short Term Debt Fund': 0.95, 'Midcap Index Fund': 1.35,
       'Smallcap Quality Index Fund': 1.35, 'Nifty 200 Momentum 30 Index Fund': 1.35, 'Nifty 500 Multicap Momentum Quality 50 Index Fund': 1.35,
       'Nifty 500 Multifactor 50 Index Fund': 1.35, 'BSE 500 Enhanced Value 50 Index Fund': 1.35, 'BSE 500 Dividend Leaders 50 Index Fund': 1.35,
       'India Consumption Fund': 1.35, 'Pure Stock Innovation Fund': 1.35, 'BSE 500 Quality 50 Index Fund': 1.35, 'Opportunities Fund': 1.35,
       'Nifty 500 Low Volatility 50 Index Fund': 1.35, 'Nifty 200 Value 30 Index Fund': 1.35, 'BSE 500 Momentum Value 50 Index Fund': 1.35}
def funds(names=None, override=None):
    override = override or {}
    return [{'name': n, 'SFIN': None, 'FMC_pct': override.get(n, FMC.get(n)), 'asset_allocation': 'see policy document Part E', 'risk_label': None} for n in (names or list(FMC))]
