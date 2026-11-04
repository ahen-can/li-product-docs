#!/usr/bin/env python3
"""licdig.py UIN [brochure|brochure-2] : compact LIC brochure text from 'Eligibility conditions' to the fund notes, then the charges paragraph."""
import re, subprocess, sys
uin = sys.argv[1]; doc = sys.argv[2] if len(sys.argv) > 2 else 'brochure'
f = f'docs/lic/{uin}/{doc}.pdf'
pages = subprocess.run(['pdftotext', '-layout', f, '-'], capture_output=True, text=True).stdout.split('\f')
txt = ''
for i, p in enumerate(pages, 1):
    for l in p.split('\n'):
        if l.strip(): txt += re.sub(r' {3,}', '   ', l.rstrip()) + '\n'
    txt += f'@@ p{i}\n'
def sect(a, b, maxc=14000):
    m = re.search(a, txt)
    if not m: return f'[no {a}]'
    n = re.search(b, txt[m.end():])
    return txt[m.start(): m.end() + (n.start() if n else maxc)][:maxc]
print('########## ELIGIBILITY TO FUNDS'); print(sect(r'Eligibility conditions', r'Method of calculation of Unit Value|Method of calculation'))
print('########## CHARGES'); print(sect(r'Charges under the Plan|Charges under the Policy', r'Tax Charge|Tax charge'))
