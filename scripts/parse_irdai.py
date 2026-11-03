"""Parse IRDAI 'List of Life Products' per-insurer xlsx files (products section only).
Usage: python3 -I parse_irdai.py <xlsx_dir> out.csv"""
import openpyxl, glob, re, sys, csv, datetime, os, collections

UINRE = re.compile(r'^\s*(\d{3}[A-Z]\d{3}V\d{2})\s*$')
out = []
for f in sorted(glob.glob(os.path.join(sys.argv[1], '*.xlsx'))):
    ws = openpyxl.load_workbook(f, read_only=True).worksheets[0]
    section = None
    for r in ws.iter_rows(values_only=True):
        cells = [c for c in r if c is not None]
        if not cells:
            continue
        s = ' '.join(str(c) for c in cells)
        if len(cells) <= 2 and re.search(r'Riders', s):
            section = 'Riders'
        elif len(cells) <= 2 and re.search(r'Products', s):
            section = 'Products'
        uin_i = next((i for i, c in enumerate(r) if c is not None and UINRE.match(str(c))), None)
        if uin_i is None:
            continue
        uin = UINRE.match(str(r[uin_i])).group(1)
        # English name is the cell just before the UIN; dates follow it
        name_en = str(r[uin_i - 1]).strip() if uin_i >= 1 and r[uin_i - 1] else ''
        after = r[uin_i + 1:]
        dates = [c for c in after if isinstance(c, (datetime.datetime, datetime.date))]
        txt_after = ' '.join(str(c) for c in after if isinstance(c, str))
        opened = dates[0].date().isoformat() if dates else ''
        closed = dates[1].date().isoformat() if len(dates) > 1 else ''
        withdrawn = 'Withdrawn' in txt_after or bool(closed)
        out.append({'file': os.path.basename(f), 'section': section, 'fy': str(r[0] or '').strip(), 'name_en': name_en,
                    'uin': uin, 'opened': opened, 'closed': closed,
                    'status': 'withdrawn' if withdrawn else 'in operation', 'remarks': txt_after.strip()[:120]})
with open(sys.argv[2], 'w', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=list(out[0].keys())); w.writeheader(); w.writerows(out)
c = collections.Counter((o['section'], o['status'], o['uin'][3]) for o in out)
for k, v in sorted(c.items(), key=lambda kv: str(kv[0])): print(k, v)
print('rows', len(out), 'no-name', sum(1 for o in out if not o['name_en']))
