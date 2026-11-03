"""Parse the Life Insurance Council in-force products PDF text (pdftotext -layout) into rows.
Usage: python3 -I parse_council.py council.txt out.csv"""
import re, sys, csv, collections

UIN = re.compile(r'(\d{3}[A-Z]\d{3}V\d{2})\s*$')
LOB = re.compile(r'\s(Individual|Group)\s')
HDR = re.compile(r'Name of the (Products|Riders)')
lines = open(sys.argv[1], encoding='utf-8').read().split('\n')

# Insurer section titles: a line that is only an insurer name (no UIN, no LoB token)
INS = re.compile(r'^\s*([A-Z][A-Za-z&.\-() ]+?(Limited\.?|Limited \(Formerly.*|Corporation Of India|Ltd\.?))\s*$')

rows = []; insurer = None; section = None; cur = None; lob_col = None
in_summary = True
for i, ln in enumerate(lines):
    if 'PRODUCTS' == ln.strip():
        in_summary = False
    if in_summary:
        continue
    if not ln.strip():
        continue
    m = HDR.search(ln)
    if m:
        section = m.group(1)
        lob_col = ln.find('Line of Business')
        cur = None
        continue
    if '(Individual / Group)' in ln:
        continue
    um = UIN.search(ln); lm = LOB.search(ln)
    if not um and not lm:
        im = INS.match(ln)
        # an insurer title has no large internal gaps (row continuations do)
        if im and not re.search(r'\S\s{3,}\S', ln.strip()) and len(ln.strip()) > 15:
            # could also be a wrapped name ending in "Limited"; insurer titles are followed by a header or rows
            insurer = im.group(1).strip(); cur = None
            continue
    if um and lm:
        name = ln[:lm.start()].strip()
        cat = ln[lm.end():um.start()].strip()
        cur = {'insurer': insurer, 'section': section, 'name': name, 'lob': lm.group(1), 'category': cat,
               'uin': um.group(1), 'line': i + 1, 'lob_pos': lm.start(), 'cat_pos': lm.end()}
        rows.append(cur)
        continue
    if 'NIL' in ln:
        cur = None; continue
    # continuation line: split into chunks by 3+ spaces and attach by column position
    if cur is not None:
        for mm in re.finditer(r'\S(?:.*?\S)?(?=\s{3,}|\s*$)', ln):
            pos = mm.start(); txt = mm.group(0).strip()
            if pos < cur['lob_pos'] - 2:
                cur['name'] += ' ' + txt
            else:
                cur['category'] += ' ' + txt

for r in rows:
    r['name'] = re.sub(r'\s+', ' ', r['name']); r['category'] = re.sub(r'\s+', ' ', r['category'])
with open(sys.argv[2], 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['insurer', 'section', 'name', 'lob', 'category', 'uin', 'line'], extrasaction='ignore')
    w.writeheader(); w.writerows(rows)
c = collections.Counter((r['insurer'], r['section'], r['lob']) for r in rows)
for k in sorted(c, key=lambda k: (str(k[0]), str(k[1]), k[2])):
    print(f'{str(k[0])[:55]:55} {str(k[1]):8} {k[2]:10} {c[k]}')
print('rows', len(rows), 'no-insurer', sum(1 for r in rows if not r['insurer']))
