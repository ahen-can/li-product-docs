import re, subprocess, sys, glob, os
u = sys.argv[1]; want = sys.argv[2].split(',') if len(sys.argv) > 2 else None
f = f'docs/tata-aia/{u}/policy.pdf'
raw = subprocess.run(['pdftotext', f, '-'], capture_output=True, text=True).stdout
lay = subprocess.run(['pdftotext', '-layout', f, '-'], capture_output=True, text=True).stdout
t = re.sub(r'\s+', ' ', '\n'.join(l for l in raw.splitlines() if f'(UIN: {u})' not in l and 'IRDA of India Regn' not in l))
def grab(rx, n=700, k=1):
    out = []
    for m in re.finditer(rx, t):
        out.append(t[m.start():m.start() + n])
        if len(out) >= k: break
    return out
S = {
 'intro': (r'PART C', 900, 1), 'heads': None,
 'death': (r'DEATH BENEFIT [A-Z(a-z]', 1500, 1), 'maturity': (r'MATURITY BENEFIT [A-Z(a-z]', 400, 1),
 'loyal': (r'(LOYALTY ADDITION|WEALTH BOOSTER|FUND BOOSTER|MATURITY BOOSTER|RETURN OF MORTALITY|SMART LADY|GUARANTEED ADDITION|ONLINE/ ?DIGITAL)', 900, 4),
 'topup': (r'TOP-?UP PREMIUM [a-z(]', 500, 1), 'change': (r'CHANGE IN (SUM ASSURED|PREMIUM)', 500, 1),
 'pw': (r'PARTIAL WITHDRAWAL OF FUND VALUE', 1300, 1), 'swp': (r'SYSTEMATIC WITHDRAWAL PLAN', 500, 1),
 'switch': (r'\d\.\d+\. FUND SWITCHING', 500, 1), 'loan': (r'\d\.\d+\. LOAN', 120, 1), 'settle': (r'SETTLEMENT OPTION [a-z(]', 400, 1),
 'strat': (r'PORTFOLIO STRATEG|ENHANCED SMART|LIFE-?STAGE|AUTO ?REBALANC', 500, 3),
 'alloc': (r'Premium Allocation Charge', 700, 3), 'admin': (r'Policy Administration Charge:', 900, 1),
 'mort': (r'Mortality Charge Table|Mortality Charges \(per|% of IALM', 400, 2), 'swc': (r'Fund Switching Charge', 400, 1),
 'other_ch': (r'(Premium Re-?direction [Cc]harge|Miscellaneous Charge|Guarantee Charge|Rider Charge)', 250, 4),
 'disc': (r'Discontinuance Charge:', 300, 1), 'riders': (r'[Rr]ider', 200, 3),
 'web': (r'(on Our website|given on Our website|available on (our|the Company\'s) website)', 200, 4),
}
for k, v in S.items():
    if want and k not in want: continue
    if k == 'heads':
        print('## heads:', ' | '.join(re.findall(r'(?m)^\d\.\d+\.? [A-Z][A-Z /&()\-]{3,60}$', raw))[:1500]); continue
    for g in grab(*v): print(f'## {k}: {g}\n')
m = re.search(r'Fund Management Charges?(?: \(FMC\))?\n', lay)
if not want or 'fmc' in want:
    i = lay.find('Fund Management Charge')
    idx = [m.start() for m in re.finditer(r'Fund Management Charges', lay)]
    for j in idx[-1:]:
        blk = lay[j:j + 6000].split('Discontinued Policy Fund')[0]
        print('## fmc:', '\n'.join(l.rstrip()[:130] for l in blk.splitlines() if '%' in l or 'ULIF' in l))
if not want or 'bro' in want:
    for b in sorted(glob.glob(f'docs/tata-aia/{u}/brochure*.pdf'))[:1]:
        bt = subprocess.run(['pdftotext', '-f', '1', '-l', '4', b, '-'], capture_output=True, text=True).stdout
        bt = re.sub(r'\n+', '|', bt)
        for rx in [r'(Entry Age|Issue Age|Age at [Ee]ntry).{0,260}', r'(Maturity Age|Age at [Mm]aturity).{0,200}', r'Policy Term.{0,200}', r'Premium Pay(ing|ment) Term.{0,200}',
                   r'Minimum Premium.{0,220}', r'Maximum Premium.{0,120}', r'(Basic )?Sum Assured.{0,300}', r'(Premium Payment Mode|Pay Mode).{0,100}']:
            m = re.search(rx, bt)
            if m: print('## bro:', m.group(0))
