#!/usr/bin/env python3
"""axdig.py UIN [prospectus|policy] : compact sections of an Axis Max Life document, skipping fund descriptions and discontinuance narrative.
Prospectus: AT A GLANCE, Benefits, FLEXIBILITIES, CHARGES (fund rows collapsed), mortality sample."""
import re, subprocess, sys
uin = sys.argv[1]; doc = sys.argv[2] if len(sys.argv) > 2 else 'brochure'
f = f'docs/axis-max-life/{uin}/{"policy" if doc.startswith("pol") else "brochure"}.pdf'
pages = subprocess.run(['pdftotext', '-layout', f, '-'], capture_output=True, text=True).stdout.split('\f')
txt = ''
for i, p in enumerate(pages, 1):
    for l in p.split('\n'):
        if l.strip(): txt += f'{re.sub(r" {3,}", "   ", l.rstrip())}\n'
    txt += f'@@ p{i}\n'
def sect(a, b, maxc=9000):
    m = re.search(a, txt)
    if not m: return f'[no {a}]'
    n = re.search(b, txt[m.end():])
    s = txt[m.start(): m.end() + (n.start() if n else maxc)]
    return s[:maxc]
for title, a, b in [('GLANCE', r'AT A GLANCE', r'TAX BENEFITS|FLEXIBILITIES OFFERED'), ('BENEFITS', r'\n\s*Benefits\s*\n|Maturity Benefit:', r'AT A GLANCE|FLEXIBILITIES OFFERED'),
                    ('FLEX', r'FLEXIBILITIES OFFERED', r'SURRENDER/DISCONTINUANCE|SURRENDER / DISCONTINUANCE|What happens when you surrender'), ('CHARGES', r'CHARGES UNDER THE POLICY', r'A WORD ON THE RISKS')]:
    s = sect(a, b)
    if title == 'CHARGES':
        s = re.sub(r'\n\s*\(*SFIN:[^\n]*', '', s)
    print(f'########## {title}\n{s}')
