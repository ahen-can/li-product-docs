# Canara HSBC Life unit linked funds: name -> fund identification number as printed in the policy documents.
SFIN = {'Emerging Leaders Equity Fund': 'ULIF02020/12/17EMLEDEQFND136', 'India Multi-Cap Equity Fund': 'ULIF01816/08/16IMCAPEQFND136', 'Equity II Fund': 'ULIF00607/01/10EQUTYIIFND136',
        'Growth Plus Fund': 'ULIF00913/09/10GROWTPLFND136', 'Balanced Plus Fund': 'ULIF01013/09/10BLNCDPLFND136', 'Large Cap Advantage Fund': 'ULIF02109/06/20LARCPADFND136',
        'Multicap Momentum Quality Index Fund': 'ULIF02410/03/25MLMMQEQFND136', 'Debt Fund': 'ULIF00409/07/08INDEBTFUND136', 'Liquid Fund': 'ULIF00514/07/08LIQUIDFUND136',
        'Discontinued Policy Fund': 'ULIF01319/09/11POLDISCFND136'}
def funds(fmc_by_name, risk=None, alloc=None):
    return [{'name': n, 'SFIN': SFIN.get(n), 'FMC_pct': v, 'asset_allocation': (alloc or {}).get(n, 'see brochure fund table'), 'risk_label': (risk or {}).get(n)} for n, v in fmc_by_name.items()]
