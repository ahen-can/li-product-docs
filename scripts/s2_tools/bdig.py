#!/usr/bin/env python3
"""bdig.py UIN [areas]: digest of a Bajaj Life ULIP policy document (sections numbered 1-40, charges in Section 17,
allocation and admin rates in the Schedule, mortality rates in an Annexure). Prints reading-order text per area."""
import re, subprocess, sys, glob
u = sys.argv[1]; want = sys.argv[2].split(',') if len(sys.argv) > 2 else None
f = f'docs/bajaj-life/{u}/policy.pdf'
raw = subprocess.run(['pdftotext', f, '-'], capture_output=True, text=True).stdout
name = re.search(r'\n(Bajaj (?:Allianz )?Life [^\n]+)\n', raw).group(1).strip()
keep = [l for l in raw.splitlines() if not re.search(r'Policy Document Ver|^UIN: ?116|^Bajaj Life Insurance Limited$|A Unit[- ]Linked', l) and l.strip() != name]
t = re.sub(r'\s+', ' ', ' '.join(keep))
def sec(rx, n):
    m = re.search(rx, t); return t[m.start():m.start() + n] if m else '(not found)'
A = {'desc': (r'Policy Description', 1500), 'benefit': (r'Policy Benefits', 2600), 'loyal': (r'Loyalty Addition', 900),
     'sched': (r'Charges: • Premium Allocation Rate', 1800), 'admin': (r'Policy Administration Charge', 500),
     'charges': (r'a\) Mortality Charge \(i\)', 4200), 'pw': (r'Partial Withdrawal', 1600), 'topup': (r'Top Up Premium (a|i)\)', 900),
     'switch': (r'Switch(es|ing) (a|i)\)', 700), 'settle': (r'Settlement Option', 900), 'strat': (r'Portfolio Strateg', 1500),
     'surr': (r'9\. Surrender Value', 900), 'revival': (r'Revival', 600), 'annex': (r'Annexure 3', 700)}
for k, (rx, n) in A.items():
    if want and k not in want: continue
    print(f'## {k}: {sec(rx, n)}\n')
if not want or 'pages' in want:
    for p in range(1, 60):
        pt = subprocess.run(['pdftotext', '-f', str(p), '-l', str(p), f, '-'], capture_output=True, text=True).stdout
        if not pt: break
        if re.search(r'Annexure ?[0-9]|ANNEXURE', pt) and re.search(r'(?m)^\d+\.\d{2,4}$', pt): print('## mortality-table page', p)
