SFIN = {'Equity Fund': 'ULIF001100105EQUITYFND111', 'Bond Fund': 'ULIF002100105BONDULPFND111', 'Growth Fund': 'ULIF003241105GROWTHFND111',
        'Balanced Fund': 'ULIF004051205BALANCDFND111', 'Money Market Fund': 'ULIF005010206MONYMKTFND111', 'Equity Optimiser Fund': 'ULIF010210108EQTYOPTFND111',
        'Top 300 Fund': 'ULIF016070110TOP300FND111', 'Discontinued Policy Fund': 'ULIF024110411DISCOPOFND111', 'Pure Fund': 'ULIF030290915PUREULPFND111',
        'Midcap Fund': 'ULIF031290915MIDCAPFUND111', 'Bond Optimiser Fund': 'ULIF032290618BONDOPTFND111', 'Corporate Bond Fund': 'ULIF033290618CORBONDFND111',
        'Bluechip Fund': 'ULIF034250824BLUECHPFND111', 'Flexicap Fund': 'ULIF035231026FLXICAPFND111', 'Large Cap Fund': 'ULIF036231026LARGCAPFND111'}
def funds(fmc):
    """fund_list entries from {fund name: FMC %}; asset ranges are in each policy document's fund table."""
    return [{'name': n, 'SFIN': SFIN.get(n), 'FMC_pct': v, 'asset_allocation': 'see policy document fund table', 'risk_label': None} for n, v in fmc.items()]
