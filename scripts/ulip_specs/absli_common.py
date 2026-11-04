# Aditya Birla Sun Life segregated funds as printed in the brochures' Schedule A (name -> identification no.).
SFIN = {'Liquid Plus': 'ULIF02807/10/11BSLLIQPLUS109', 'Income Advantage': 'ULIF01507/08/08BSLIINCADV109', 'Assure': 'ULIF01008/07/05BSLIASSURE109', 'Protector': 'ULIF00313/03/01BSLPROTECT109',
        'Builder': 'ULIF00113/03/01BSLBUILDER109', 'Enhancer': 'ULIF00213/03/01BSLENHANCE109', 'Creator': 'ULIF00704/02/04BSLCREATOR109', 'Magnifier': 'ULIF00826/06/04BSLIIMAGNI109',
        'Maximiser': 'ULIF01101/06/07BSLIINMAXI109', 'Multiplier': 'ULIF01217/10/07BSLIINMULTI109', 'Super 20': 'ULIF01723/06/09BSLSUPER20109', 'Pure Equity': 'ULIF02707/10/11BSLIPUREEQ109',
        'Value & Momentum': 'ULIF02907/10/11BSLIVALUEM109', 'Capped Nifty Index': 'ULIF03530/10/14BSLICNFIDX109', 'Asset Allocation': 'ULIF03430/10/14BSLIASTALC109', 'MNC': 'ULIF03722/06/18ABSLIMUMNC109', 'Linked Discontinued Policy Fund': 'ULIF03205/07/13BSLILDIS109'}
def funds(fmc_by_name, risk=None):
    return [{'name': n, 'SFIN': SFIN.get(n), 'FMC_pct': v, 'asset_allocation': 'see brochure Schedule A', 'risk_label': (risk or {}).get(n)} for n, v in fmc_by_name.items()]
