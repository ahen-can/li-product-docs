"""ULIP projection engine. Monthly fund roll-forward from the charges in each product's policy document.

Inputs: calc/params/ulip/<UIN>.json (every number cites the policy document page).
Method, per policy month m (policy year y = m // 12 + 1):
  1. Start of a policy year within the premium term: premium in, allocation charge out, any "special addition"
     credited, units bought.
  2. Policy admin charge and mortality charge deducted (mortality = sum at risk x annual rate per 1000 / 12,
     sum at risk = max(sum assured - fund value, 0), rate by age last birthday at the start of the policy year).
  3. Fund grows at the gross rate for one month; fund management charge (FMC) is taken from the grown fund.
  4. End of a policy year: additions (loyalty, boosters, charge refunds) as the parameter file defines.
GST at 18% is added to every charge (allocation, admin, mortality, FMC), as in insurer benefit illustrations.
Refunds of charges exclude GST, as the policy documents state.
Outputs: fund value at maturity, IRR (= net yield) of premiums against that value, reduction in yield.
Survival scenario only. Results are unchecked until compared with an official benefit illustration.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import irr

HERE = os.path.dirname(os.path.abspath(__file__))
GST = 0.18


def load(uin):
    return json.load(open(os.path.join(HERE, 'params', 'ulip', f'{uin}.json'), encoding='utf-8'))


def yr_lookup(schedule, y, default=0.0):
    """schedule: list of [from_year, to_year, value]; to_year None = open-ended."""
    for a, b, v in schedule:
        if a <= y and (b is None or y <= b):
            return v
    return default


def project(uin, age=30, ap=100000, ppt=10, pt=20, gross=0.08, gst=True, trace=False):
    p = load(uin)
    g = GST if gst else 0.0
    q = {int(k): v for k, v in p['mortality_per_1000'].items()}
    sa = p['sum_assured_multiple'] * ap
    fmc = p['fmc_pct'] / 100
    fmc_m = 1 - (1 - fmc * (1 + g)) ** (1 / 12)
    grow_m = (1 + gross) ** (1 / 12) - 1
    fv = 0.0
    paid = {k: 0.0 for k in ('pac', 'admin', 'mort', 'fmc')}           # charges excl. GST, whole term
    paid_ppt = {k: 0.0 for k in paid}                                     # charges during the premium term
    month_fv = []                                                         # end-of-month fund values
    rows = []
    adds_log = []
    for m in range(pt * 12):
        y = m // 12 + 1
        a = age + y - 1
        yc = {'pac': 0.0, 'admin': 0.0, 'mort': 0.0, 'fmc': 0.0}
        if m % 12 == 0 and y <= ppt:
            pac = yr_lookup(p['allocation_charge_pct'], y) / 100 * ap
            yc['pac'] += pac
            fv += ap - pac * (1 + g)
            for s in p.get('additions', []):
                if s['type'] == 'pct_ap_at_allocation' and y in s['years']:
                    fv += ap * s['pct'] / 100; adds_log.append((y, s['name'], ap * s['pct'] / 100))
        adm = p['admin']
        if adm['basis'] == 'pct_ap':
            av = yr_lookup(adm['schedule'], y) / 100 * ap
            if adm.get('escalation_pa'):
                ys = adm['escalation_from_year']
                if y >= ys: av *= (1 + adm['escalation_pa']) ** (y - ys)
        else:
            av = yr_lookup(adm['schedule'], y)
        av = min(av, adm.get('cap_per_month', 1e18))
        if adm.get('only_while_premiums_due') and y > ppt:
            av = 0.0
        sar = max(sa - fv, 0.0)
        mort = sar * q[a] / 1000 / 12
        yc['admin'] += av; yc['mort'] += mort
        fv -= (av + mort) * (1 + g)
        fv *= 1 + grow_m
        f = fv * fmc_m
        yc['fmc'] += f / (1 + g)
        fv -= f
        for k in paid:
            paid[k] += yc[k]
            if y <= ppt: paid_ppt[k] += yc[k]
        month_fv.append(fv)
        if m % 12 == 11:                       # end of policy year y
            last = y == pt
            add_total = 0.0
            for s in p.get('additions', []):
                amt = 0.0; t = s['type']
                if t == 'pct_fv_end_of_year' and y in s['years']:
                    amt = fv * s['pct'] / 100
                elif t == 'pct_avg_fv' and y in s['years']:
                    n = s['avg_months']; amt = sum(month_fv[-n:]) / min(n, len(month_fv)) * s['pct'] / 100
                elif t == 'pct_fv_at_maturity_before_refunds' and last:
                    amt = fv * s['pct'] / 100
                elif t == 'refund_at_maturity' and last:
                    base = paid if s.get('scope', 'term') == 'term' else paid_ppt
                    amt = sum(base[c] for c in s['charges']) * s.get('multiple', 1.0)
                elif t == 'refund_spread' and y in s['years']:
                    base = paid_ppt if s.get('scope') == 'ppt' else paid
                    amt = sum(base[c] for c in s['charges']) * s.get('multiple', 1.0) / len(s['years'])
                elif t == 'pct_ap_once' and y == s['year']:
                    amt = ap * s['pct'] / 100
                if amt:
                    add_total += amt; adds_log.append((y, s['name'], amt))
            fv += add_total
            rows.append({'year': y, 'age': a, 'fund_value': round(fv), 'additions': round(add_total)})
    cfs = [(k, -ap) for k in range(ppt)] + [(pt, fv)]
    net = irr(cfs)
    out = {'uin': uin, 'product': p['product'], 'variant': p['variant_used'], 'age': age, 'annual_premium': ap,
           'ppt': ppt, 'pt': pt, 'gross_return': gross, 'maturity_value': round(fv), 'total_premium': ap * ppt,
           'net_yield': net, 'reduction_in_yield': gross - net,
           'charges_excl_gst': {k: round(v) for k, v in paid.items()},
           'additions_total': round(sum(x[2] for x in adds_log))}
    if trace:
        out['years'] = rows; out['additions'] = [(y, n, round(v)) for y, n, v in adds_log]
    return out


def zero_charge_check():
    """With every charge and addition removed, the net yield must equal the gross rate."""
    import tempfile, shutil
    p = {'product': 'test', 'variant_used': 'test', 'sum_assured_multiple': 0, 'fmc_pct': 0, 'allocation_charge_pct': [],
         'admin': {'basis': 'flat', 'schedule': []}, 'mortality_per_1000': {str(a): 0 for a in range(0, 120)}, 'additions': []}
    path = os.path.join(HERE, 'params', 'ulip', 'ZERO.json')
    json.dump(p, open(path, 'w'))
    try:
        r = project('ZERO', gross=0.08)
        assert abs(r['net_yield'] - 0.08) < 1e-6, r['net_yield']
    finally:
        os.remove(path)
    return True


if __name__ == '__main__':
    print('zero-charge check passes:', zero_charge_check())
    uins = sys.argv[1:] or sorted(f[:-5] for f in os.listdir(os.path.join(HERE, 'params', 'ulip')) if f.endswith('.json'))
    for u in uins:
        p = load(u); prof = p.get('standard_profile', {})
        for gr in (0.04, 0.08):
            r = project(u, gross=gr, **prof)
            print(f"{u} {p['product'][:34]:34} AP {r['annual_premium']:>7} {int(gr*100)}%: maturity {r['maturity_value']:>10,}  net yield {r['net_yield']:.2%}  RIY {r['reduction_in_yield']:.2%}")
