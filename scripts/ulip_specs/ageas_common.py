# Ageas Federal Life unit linked funds: name -> fund identification number as printed in the policy documents
# (some are printed without slashes, for example ULIF080061223MULTICAP135; they are kept as printed).
SFIN = {'Equity Growth Fund': 'ULIF04111/01/08EQOPP135', 'Midcap Fund': 'ULIF06824/11/09MIDCAP135', 'Multicap Fund': 'ULIF080061223MULTICAP135',
        'Momentum Growth Fund': 'ULIF081240125MOMENTUM135', 'India Sector Leaders Fund': 'ULIF082070725ISLF135', 'Enhanced Value Fund': 'ULIF083071125ENVF135',
        'Pure Fund': 'ULIF07205/08/10PURE135', 'Bond Fund II': 'ULIF07731/10/17BOND2135', 'Aggressive Asset Allocator Fund': 'ULIF04811/01/08AGGRESSIVE135',
        'Moderate Asset Allocator Fund': 'ULIF04911/01/08MODERATE135', 'Large Cap Quality Fund': 'ULIF088010326LARGEQLTY135', 'IndiGenius Fund': 'ULIF08901/07/26INDIGENIUS135',
        'Discontinued Policy Fund': 'ULIF07301/07/10DISCON135',
        'Bond Fund': 'ULIF04011/01/08BOND135', 'Income Fund': 'ULIF04211/01/08INCOME135', 'Cautious Asset Allocator Fund': 'ULIF05011/01/08CAUTIOUS135'}
def funds(fmc_by_name, risk=None, alloc=None):
    return [{'name': n, 'SFIN': SFIN.get(n), 'FMC_pct': v, 'asset_allocation': (alloc or {}).get(n, 'see brochure fund table'), 'risk_label': (risk or {}).get(n)} for n, v in fmc_by_name.items()]

def mortality(path, start_marker, n_max=160, stop_after=12):
    """Read the age / male / female rate blocks that follow start_marker in a layout text file.
    Returns {'male': {age: rate}, 'female': {age: rate}}. Page breaks inside the table are skipped."""
    import re
    lines = open(path, errors='ignore').read().split('\n')
    i = next(k for k, l in enumerate(lines) if start_marker in l)
    male, female = {}, {}
    rows = miss = 0
    for l in lines[i + 1:i + 1 + n_max]:
        toks = re.findall(r'\d+(?:\.\d+)?', l)
        words = re.sub(r'[\d.\s]+', '', l)
        if len(toks) >= 3 and len(toks) % 3 == 0 and not words and all(int(float(toks[j])) == float(toks[j]) and float(toks[j]) < 110 for j in range(0, len(toks), 3)):
            rows += 1; miss = 0
            for j in range(0, len(toks), 3):
                a = int(toks[j]); male.setdefault(a, float(toks[j + 1])); female.setdefault(a, float(toks[j + 2]))
        elif rows:
            miss += 1
            if miss > stop_after: break
    return {'male': dict(sorted(male.items())), 'female': dict(sorted(female.items()))}
