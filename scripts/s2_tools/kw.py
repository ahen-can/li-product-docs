# kw.py UIN [policy_label_file=policy] : first passage per key term in policy + brochure, then the brochure glance table
import re, subprocess, sys, glob, os
uin = sys.argv[1]; W = int(sys.argv[2]) if len(sys.argv) > 2 else 380
TERMS = ['Death Bene', 'Maturity Bene', 'Loyalty', 'Booster', 'Guaranteed Addition', 'Milestone', 'Return of Mortality', 'Return of Premium Allocation', 'Refund',
         'Premium Allocation Charge', 'Administration Charge', 'Fund Management Charge', 'Mortality Charge', 'Discontinuance Charge', 'Switch', 'Partial Withdrawal',
         'Systematic Withdrawal', 'Top-up', 'Top up', 'Redirection', 'Settlement', 'Loan', 'Strategy', 'Revival Period', 'Lock-in', 'investment funds currently',
         'Rider', 'Waiver', 'Sum Assured', 'Advt', 'variant', 'option']
for d in sorted(glob.glob(f'docs/*/{uin}/*.pdf')):
    doc = os.path.basename(d)[:-4]
    if doc.split('-')[0] not in ('policy', 'brochure'): continue
    pg = subprocess.run(['pdftotext', d, '-'], capture_output=True, text=True).stdout.split('\f')
    print(f'####### {doc} ({len(pg)} pages)')
    for kw in TERMS:
        for i, p in enumerate(pg, 1):
            f = re.sub(r'\s+', ' ', p)
            if re.search('ombudsman|section 45', f, re.I) and len(re.findall('ombudsman|section 4[15]|section 3[89]', f, re.I)) > 2: continue
            m = re.search(re.escape(kw), f, re.I)
            if m and not re.match(r'.{0,30}(means|is the|is a )', f[m.end():m.end() + 30]):
                print(f'[{doc} p{i}] {kw}: {f[max(0, m.start() - 60):m.start() + W]}'); break
for d in glob.glob(f'docs/*/{uin}/brochure.pdf'):
    pg = subprocess.run(['pdftotext', '-layout', d, '-'], capture_output=True, text=True).stdout.split('\f')
    for i, p in enumerate(pg, 1):
        if re.search(r'entry age|age at entry', p, re.I) and re.search(r'premium', p, re.I):
            print(f'####### brochure glance p{i}'); print(re.sub(r' {3,}', '   ', re.sub(r'\n\s*\n', '\n', p))[:4500]); break
