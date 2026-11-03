"""IRR engine for life-insurance savings products, driven by per-product parameter files (params/<UIN>.json).

Every number in a parameter file comes from the insurer's published documents (policy document / brochure)
and carries a source reference.  The engine only does arithmetic: build year-by-year cash flows, then solve IRR.

Conventions
- t = 0 is the policy start. Annual premiums are paid at t = 0 .. PPT-1 (beginning of each policy year).
- A benefit "at end of policy year k" is at t = k; "beginning of year k" is at t = k-1.
- Premiums exclude GST unless include_gst=True (non-par savings: 4.5% in year 1, 2.25% thereafter).
- Survival scenario (life assured survives to the end): this is the maturity/income IRR shown by aggregators.
"""
import json, os, math

HERE = os.path.dirname(os.path.abspath(__file__))

def load(uin):
    return json.load(open(os.path.join(HERE, 'params', f'{uin}.json')))

def irr(cfs, lo=-0.99, hi=1.0, tol=1e-10):
    """cfs: list of (t, amount). Bisection on NPV; returns annual rate."""
    def npv(r): return sum(a / (1 + r) ** t for t, a in cfs)
    f_lo, f_hi = npv(lo), npv(hi)
    if f_lo * f_hi > 0:
        return float('nan')
    for _ in range(300):
        mid = (lo + hi) / 2; f = npv(mid)
        if abs(f) < tol: break
        if f_lo * f > 0: lo, f_lo = mid, f
        else: hi = mid
    return (lo + hi) / 2

def band_of(p, ap):
    for b in p['premium_bands']:
        if b['min'] <= ap <= b.get('max', 1e18):
            return b['band']
    raise ValueError('premium outside bands')

def table_lookup(p, table, age, band, gender):
    """Age-banded factor table with the product's female age rule."""
    t = p['tables'][table]
    rule = p.get('female_rule')
    a = age
    if gender == 'F' and rule:
        a = age - rule['age_setback']
        ages = sorted(int(k) for k, v in t.items() if v[band - 1] is not None)
        if a < ages[0]:
            a = ages[0]          # e.g. "female rate for first entry ages = male rate at minimum entry age"
    row = t.get(str(a))
    if row is None or row[band - 1] is None:
        raise ValueError(f'factor not available for age {a}, band {band} in {table}')
    return row[band - 1] / 100.0

def check_eligibility(p, v, age, ap):
    e = v['eligibility']
    if not (e['min_entry_age'] <= age <= e['max_entry_age']):
        raise ValueError(f"entry age {age} outside {e['min_entry_age']}-{e['max_entry_age']} for PPT {v['ppt']}/PT {v['pt']}")
    if ap < e['min_annual_premium']:
        raise ValueError(f"annual premium below minimum {e['min_annual_premium']}")

def cashflows(uin, age, gender, annual_premium, ppt, pt=None, include_gst=False):
    p = load(uin)
    v = next(x for x in p['variants'] if x['ppt'] == ppt and (pt is None or x['pt'] == pt))
    check_eligibility(p, v, age, annual_premium)
    band = band_of(p, annual_premium) if p.get('premium_bands') else 1
    cfs = []
    for k in range(v['ppt']):
        gst = (0.045 if k == 0 else 0.0225) if include_gst else 0.0
        cfs.append((k, -annual_premium * (1 + gst)))
    for seg in v.get('income', []):
        for yr in range(seg['from_end_of_year'], seg['to_end_of_year'] + 1):
            cfs.append((yr, annual_premium * seg['pct_of_ap'] / 100.0))
    for ls in v.get('lumpsums', []):
        f = table_lookup(p, ls['table'], age, band, gender) if 'table' in ls else ls['pct_of_ap'] / 100.0
        cfs.append((ls['t'], annual_premium * f))
    return cfs, {'band': band, 'variant': f"PPT {v['ppt']} / PT {v['pt']}"}

def quote(uin, age, gender, annual_premium, ppt, pt=None, include_gst=False):
    cfs, meta = cashflows(uin, age, gender, annual_premium, ppt, pt, include_gst)
    paid = -sum(a for _, a in cfs if a < 0); got = sum(a for _, a in cfs if a > 0)
    return {'uin': uin, **meta, 'total_premium': round(paid), 'total_benefits': round(got),
            'multiple': round(got / paid, 3), 'irr': irr(cfs), 'cashflows': sorted(cfs)}

if __name__ == '__main__':
    import sys
    q = quote(sys.argv[1], int(sys.argv[2]), sys.argv[3], float(sys.argv[4]), int(sys.argv[5]))
    print({k: v for k, v in q.items() if k != 'cashflows'}, f"IRR={q['irr']:.2%}")
