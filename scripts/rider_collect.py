#!/usr/bin/env python3
"""Rider discovery: store one rider document and record it.

    python3 -I scripts/rider_collect.py SLUG "Insurer name" RIDER_UIN "Rider name" brochure|policy URL FOUND_ON "site label" ["note"]

Downloads the exact URL (1 request), checks %PDF, size, pdfinfo and that the rider UIN is printed in the text, stores
docs/<slug>/riders/<UIN>/<brochure|policy>.pdf and text/<slug>/riders/<UIN>/<...>.txt, appends an index.csv row (doc_type
rider_brochure / rider_policy) and a row in results/riders_downloaded.csv (the running list of riders downloaded).
Pass the real URL found on the insurer's site; never a guessed one."""
import sys, csv, os, re, hashlib, subprocess, datetime, urllib.request
slug, insurer, uin, rname, kind, url, found, label = sys.argv[1:9]
note = sys.argv[9] if len(sys.argv) > 9 else ''
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
LIST = 'results/riders_downloaded.csv'
LH = ['insurer', 'rider_uin', 'rider_name', 'doc_type', 'website_label', 'source_url', 'found_on_page_url', 'stored_path', 'pages', 'uin_in_document', 'status', 'notes', 'downloaded_utc']
rows = list(csv.reader(open('index.csv'))); H = rows[0]
data = open(url[7:], 'rb').read() if url.startswith('upload:') else urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=60).read()   # upload:PATH for a file the user supplied
assert data[:4] == b'%PDF', 'not a PDF'
assert len(data) < 95 * 1024 * 1024
sha = hashlib.sha256(data).hexdigest()
for r in rows[1:]:
    if r[H.index('sha256')] == sha and r[H.index('uin')] == uin: sys.exit('already stored: ' + r[H.index('file_path')])
d = f'docs/{slug}/riders/{uin}'; os.makedirs(d, exist_ok=True)
fp = f'{d}/{kind}.pdf'
assert not os.path.exists(fp), fp + ' exists'
open(fp, 'wb').write(data)
pages = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', fp], capture_output=True, text=True).stdout).group(1))
txt = subprocess.run(['pdftotext', '-layout', fp, '-'], capture_output=True, text=True).stdout
assert len(txt) > 200 * pages, 'scanned; OCR needed'
uin_ok = uin in txt.replace(' ', '')
tp = f'text/{slug}/riders/{uin}/{kind}.txt'; os.makedirs(os.path.dirname(tp), exist_ok=True); open(tp, 'w').write(txt)
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
n2 = note + ('' if uin_ok else ' UIN not printed in the document.')
d1 = {k: '' for k in H}
d1.update({'doc_id': f'{uin}-rider_{kind}', 'insurer': insurer, 'product_name': rname, 'uin': uin, 'linked_flag': 'R', 'doc_type': 'rider_' + kind,
           'source_url': url, 'found_on_page_url': found, 'download_date_utc': now, 'http_status': '200', 'sha256': sha, 'bytes': str(len(data)),
           'pages': str(pages), 'is_scanned': 'N', 'file_path': fp, 'text_path': tp, 'status': 'ok', 'notes': n2.strip(), 'website_label': label})
with open('index.csv', 'a', newline='') as o: csv.writer(o).writerow([d1.get(k, '') for k in H])
new = not os.path.exists(LIST)
with open(LIST, 'a', newline='') as o:
    w = csv.writer(o)
    if new: w.writerow(LH)
    w.writerow([insurer, uin, rname, 'rider_' + kind, label, url, found, fp, pages, uin if uin_ok else '', 'ok', n2.strip(), now])
print('stored', fp, pages, 'pages', 'uin ok' if uin_ok else 'UIN NOT IN TEXT')
