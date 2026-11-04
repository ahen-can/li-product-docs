#!/usr/bin/env python3
"""Print the passages of a ULIP's stored documents that matter for each schema area, with page numbers.

    python3 -I scripts/ulip_digest.py 130L100V03 [--area charges] [--docs policy,brochure,cis] [--width 900]

Reads text/<slug>/<UIN>/<doc>.txt (pages split on form feeds) and prints, per area, each matching paragraph once
as "[doc p.N] text". Boilerplate pages (ombudsman addresses, assignment/nomination sections, Section 45) are skipped.
This is a reading aid for filling features/ulip/<UIN>.json; it decides nothing.
"""
import argparse, csv, glob, os, re, subprocess

AREAS = {
    'product': r'unique identification|\bUIN\b|non[\s-]*participating|unit[\s-]*linked|variant|plan option|option\s*[1-4]\b|advt|online|target',
    'eligibility': r'entry age|maturity age|age at entry|age at maturity|policy term|premium payment term|\bPPT\b|minimum premium|maximum premium|'
                   r'sum assured|premium payment mode|frequency|single pay|limited pay|regular pay|annuali[sz]ed premium',
    'charges': r'allocation charge|administration charge|fund management charge|\bFMC\b|mortality charge|discontinuance charge|switching charge|'
               r'partial withdrawal charge|redirection charge|miscellaneous charge|guarantee charge|rider charge|charges? (will be|shall be) (deducted|levied)',
    'benefits': r'death benefit|maturity benefit|loyalty addition|wealth booster|guaranteed addition|return of mortality|return of (premium )?allocation|'
                r'return of (policy )?administration|addition|settlement option|terminal illness|accidental',
    'flexibility': r'switch|redirection|partial withdrawal|systematic withdrawal|top[\s-]*up|premium holiday|increase|decrease|policy loan|\bloan\b|'
                   r'strategy|systematic transfer|\bSTP\b|life[\s-]*cycle|auto[\s-]*rebalanc|trigger|alteration|change in (premium payment|policy) term',
    'funds': r'\bSFIN\b|fund name|equity|debt|money market|discontinued policy fund|fund options|index fund|new fund|risk (profile|level)|asset allocation',
    'protection': r'waiver of premium|critical illness|accidental death|terminal illness|spouse|rider',
    'surrender': r'lock[\s-]*in|discontinu|revival|revive|surrender|grace period|lapse',
    'not_public': r'as per (the )?policy schedule|available on request|on request|annexure|refer (to )?(the )?(company|website)|not disclosed|subject to (change|irdai)',
}
BOILER = re.compile(r'ombudsman|section 38|section 39|section 45|assignment|nomination|grievance redressal', re.I)

def pages(path):
    """Pages in reading order: plain pdftotext of the stored PDF (the -layout text in text/ interleaves columns)."""
    pdf = path.replace('text/', 'docs/', 1)[:-4] + '.pdf'
    if os.path.exists(pdf):
        t = subprocess.run(['pdftotext', pdf, '-'], capture_output=True, text=True).stdout
        if len(t.strip()) > 500: return t.split('\f')
    return open(path).read().split('\f')                          # OCR text for scanned PDFs

def paras(page):
    out, cur = [], []
    for line in page.splitlines():
        if line.strip(): cur.append(line.strip())
        elif cur: out.append(' '.join(cur)); cur = []
    if cur: out.append(' '.join(cur))
    return [re.sub(r'\s{2,}', '  ', p) for p in out]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('uin'); ap.add_argument('--area', default='')
    ap.add_argument('--docs', default='policy,brochure,cis,bi'); ap.add_argument('--width', type=int, default=900)
    ap.add_argument('--pages', default='', help='only these pages, e.g. 8-15')
    a = ap.parse_args()
    files = sorted(glob.glob(f'text/*/{a.uin}/*.txt'))
    want = a.docs.split(',')
    files = [f for f in files if os.path.basename(f).split('.')[0].split('-')[0] in want]
    lo, hi = (int(x) for x in a.pages.split('-')) if a.pages else (1, 10**6)
    for area, rx in AREAS.items():
        if a.area and area not in a.area.split(','): continue
        print(f'\n######## {area}')
        seen = set()
        for f in files:
            doc = os.path.basename(f)[:-4]
            for i, pg in enumerate(pages(f), 1):
                if not (lo <= i <= hi): continue
                if len(BOILER.findall(pg)) >= 3: continue
                for p in paras(pg):
                    if re.search(rx, p, re.I) and p[:120] not in seen:
                        seen.add(p[:120]); print(f'[{doc} p.{i}] {p[:a.width]}')

if __name__ == '__main__':
    main()
