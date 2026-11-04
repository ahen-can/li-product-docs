#!/usr/bin/env python3
"""addoc.py UIN DOC_TYPE URL FOUND_ON_PAGE LABEL NOTE [DOC_UIN]
Download one PDF by exact URL (1 request), check %PDF, pdfinfo, size and the UIN printed inside (DOC_UIN, default UIN),
store it as docs/<slug>/<UIN>/<doc_type>[-n].pdf, write -layout text, and append rows to index.csv and results/deep_ulip_docs.csv.
Use for links that the collector cannot see (script data on the page) or for a document that carries another product's UIN.
Never pass a URL that was not found on the insurer's site or returned a real PDF by file-name pattern."""
import sys, csv, os, re, hashlib, subprocess, datetime, urllib.request
uin, dtype, url, found, label, note = sys.argv[1:7]
doc_uin = sys.argv[7] if len(sys.argv) > 7 else uin
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
rows = list(csv.reader(open('index.csv'))); H = rows[0]
tpl = next(dict(zip(H, r)) for r in rows[1:] if r[H.index('uin')] == uin)
slug = tpl['file_path'].split('/')[1]
data = urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': UA}), timeout=60).read()
assert data[:4] == b'%PDF', 'not a PDF'
assert len(data) < 95 * 1024 * 1024
sha = hashlib.sha256(data).hexdigest()
for r in rows[1:]:
    if r[H.index('sha256')] == sha and r[H.index('uin')] == uin: sys.exit(f'already stored for {uin}: {r[H.index("file_path")]}')
d = f'docs/{slug}/{uin}'; os.makedirs(d, exist_ok=True)
n = 1; name = dtype
while os.path.exists(f'{d}/{name}.pdf'): n += 1; name = f'{dtype}-{n}'
fp = f'{d}/{name}.pdf'; open(fp, 'wb').write(data)
info = subprocess.run(['pdfinfo', fp], capture_output=True, text=True).stdout
pages = int(re.search(r'Pages:\s+(\d+)', info).group(1))
txt = subprocess.run(['pdftotext', '-layout', fp, '-'], capture_output=True, text=True).stdout
assert len(txt) > 200 * pages, 'scanned; OCR needed'
if doc_uin != '-': assert doc_uin in txt.replace(' ', ''), f'{doc_uin} not found in document'   # '-' = the document prints no product code; say so in the note
tp = f'text/{slug}/{uin}/{name}.txt'; os.makedirs(os.path.dirname(tp), exist_ok=True); open(tp, 'w').write(txt)
now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
d1 = dict(tpl); d1.update({'doc_id': f'{uin}-{name}', 'doc_type': dtype, 'source_url': url, 'found_on_page_url': found, 'download_date_utc': now, 'http_status': '200', 'sha256': sha,
          'bytes': str(len(data)), 'pages': str(pages), 'is_scanned': 'N', 'file_path': fp, 'text_path': tp, 'status': 'ok', 'notes': note, 'website_label': label})
with open('index.csv', 'a', newline='') as o: csv.writer(o).writerow([d1.get(k, '') for k in H])
H2 = next(csv.reader(open('results/deep_ulip_docs.csv')))
d2 = {'insurer': tpl['insurer'], 'product_name': tpl['product_name'], 'uin': uin, 'website_label': label, 'doc_type': dtype, 'status': 'ok', 'url': url, 'found_on_page_url': found,
      'stored_path': fp, 'pages': str(pages), 'uin_in_document': '' if doc_uin == '-' else doc_uin, 'is_scanned': 'N', 'notes': note, 'checked_utc': now}
with open('results/deep_ulip_docs.csv', 'a', newline='') as o: csv.writer(o).writerow([d2.get(k, '') for k in H2])
print('stored', fp, pages, 'pages')
