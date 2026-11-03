#!/usr/bin/env python3
"""Fill website_product_page_url in master_list.csv from insurer listing pages that print each product's UIN
next to the link to its page (e.g. LIC's category tables). Matching is by exact UIN (or product code if
--code), never by name. Each page is opened (HTTP 200) before it is written. Rows that already have a URL are
kept unless --overwrite.

    python3 -I scripts/map_pages_by_uin.py --insurer lic URL [URL ...] [--apply]
"""
import argparse, csv, html, re, subprocess, sys, time, urllib.parse
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
def get(u):
    time.sleep(1.0)
    r = subprocess.run(['curl', '-sSL', '--compressed', '-m', '60', '-A', UA, '-w', '\n%{http_code}\t%{url_effective}', u], capture_output=True)
    body, _, tail = r.stdout.rpartition(b'\n'); code, _, eff = tail.decode().partition('\t')
    return int(code or 0), body.decode('utf-8', 'ignore'), eff or u
ap = argparse.ArgumentParser(); ap.add_argument('--insurer', required=True); ap.add_argument('pages', nargs='+')
ap.add_argument('--apply', action='store_true'); ap.add_argument('--overwrite', action='store_true')
ap.add_argument('--code', action='store_true', help='match on product code (UIN without version) instead of full UIN')
a = ap.parse_args()
M = list(csv.DictReader(open('master_list.csv'))); cols = list(M[0].keys())
want = {(r['product_code'] if a.code else r['uin']).upper(): r for r in M if r['insurer_slug'] == a.insurer}
found = {}
for pg in a.pages:
    code, t, eff = get(pg); print('listing', pg, code, file=sys.stderr)
    for row in re.findall(r'<tr[^>]*>(.*?)</tr>', t, re.S | re.I) or [t]:
        flat = re.sub(r'\s+', '', re.sub(r'<[^>]+>', ' ', row)).upper()
        links = [urllib.parse.urljoin(eff, html.unescape(h)) for h in re.findall(r'href=["\']([^"\'#]+)["\']', row, re.I)]
        links = [l for l in links if not l.lower().endswith('.pdf')]
        for k in want:
            if k in flat and links and k not in found: found[k] = (links[0], pg)
n = 0
for k, r in want.items():
    if k not in found: print(f"{r['row_id']:>4} {r['product_name'][:50]:50} -> (UIN not on listing pages)"); continue
    if r['website_product_page_url'] and not a.overwrite: print(f"{r['row_id']:>4} {r['product_name'][:50]:50} keeps {r['website_product_page_url']}"); continue
    u, pg = found[k]; c = get(u)[0] if a.apply else ''
    print(f"{r['row_id']:>4} {r['product_name'][:50]:50} -> {u} {c}")
    if a.apply and c == 200: r['website_product_page_url'] = u; n += 1
if a.apply:
    w = csv.DictWriter(open('master_list.csv', 'w', newline=''), fieldnames=cols); w.writeheader(); w.writerows(M)
    print('updated', n, file=sys.stderr)
