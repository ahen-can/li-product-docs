"""Write calc/results_ulip.csv and calc/results_ulip_by_year.csv for every product in calc/params/ulip.
Two bases: excluding GST (as insurers illustrate) and including GST (what the customer pays).
Usage: python3 -I calc/tools/write_results.py <repo>"""
import sys, os, csv
R = sys.argv[1]; sys.path.insert(0, os.path.join(R, 'calc')); import ulip
CHECK = {'111L147V01': 'checked vs SBI quote, within 0.15%', '101L133V03': 'checked vs HDFC quote, within 0.15%',
         '130L100V03': 'checked vs Bharti BI, within 0.3%', '130L121V01': 'checked vs Bharti BI, within 0.2%', '130L128V01': 'checked vs Bharti BI, within 0.3%'}
rows, tr = [], []
for f in sorted(os.listdir(os.path.join(R, 'calc/params/ulip'))):
    u = f[:-5]; p = ulip.load(u); prof = p['standard_profile']
    out = [u, p['product'], p['variant_used'], prof['age'], prof['ap'], prof['ppt'], prof['pt']]
    for gst in (False, True):
        for g in (0.04, 0.08):
            r = ulip.project(u, gross=g, gst=gst, trace=(gst and g == 0.08), **prof)
            out += [r['maturity_value'], round(r['net_yield'] * 100, 2), round(r['reduction_in_yield'] * 100, 2)]
            if gst and g == 0.08:
                ch = r['charges_excl_gst']; adds = r['additions_total']
                for y in r['years']: tr.append([u, p['product'], '8% incl. GST', y['year'], y['age'], y['fund_value'], y['additions']])
    rows.append(out + [ch['pac'], ch['admin'], ch['mort'], ch['fmc'], adds, p.get('note', ''), CHECK.get(u, 'not yet checked against an insurer illustration')])
hdr = ['uin', 'product', 'variant', 'age', 'annual_premium', 'ppt', 'pt',
       'maturity_4_exGST', 'net_yield_4_exGST', 'riy_4_exGST', 'maturity_8_exGST', 'net_yield_8_exGST', 'riy_8_exGST',
       'maturity_4_inclGST', 'net_yield_4_inclGST', 'riy_4_inclGST', 'maturity_8_inclGST', 'net_yield_8_inclGST', 'riy_8_inclGST',
       'alloc_charges', 'admin_charges', 'mortality_charges', 'fmc', 'additions_and_refunds', 'note', 'check_status']
with open(os.path.join(R, 'calc/results_ulip.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(hdr); w.writerows(rows)
with open(os.path.join(R, 'calc/results_ulip_by_year.csv'), 'w', newline='') as f:
    w = csv.writer(f); w.writerow(['uin', 'product', 'basis', 'year', 'age', 'fund_value_end_of_year', 'additions_in_year']); w.writerows(tr)
for r in rows: print(r[1][:34].ljust(34), 'exGST 8%:', r[11], 'RIY', r[12], '| inclGST 8%:', r[17], '|', r[-1][:20])
