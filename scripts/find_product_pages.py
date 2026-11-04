#!/usr/bin/env python3
"""Propose product-page URLs for master_list rows that have none, from the insurer's own sitemap(s).

    python3 -I scripts/find_product_pages.py --insurer bharti-life --sitemap https://www.bhartiaxa.com/sitemap.xml
    python3 -I scripts/find_product_pages.py --insurer bharti-life --sitemap ... --apply   # write verified matches

Only URLs listed in the sitemap are considered, and each proposed URL is opened (HTTP 200 required) before
--apply writes it to master_list.csv. Nothing is guessed. Rows that already have a URL are left alone
unless --overwrite is given. Review the printed matches before applying.
"""
import argparse, csv, gzip, re, subprocess, sys, time, urllib.parse

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
STOP = set("lic lics life insurance plan the of and for with sbi hdfc icici bharti axa tata aia bajaj allianz absli aditya birla sun "
           "kotak pnb metlife canara hsbc indiafirst sud indusind nippon reliance shriram ageas federal generali central edelweiss "
           "tokio pramerica aviva bandhan axis max new smart".split())
SKIP = re.compile(r'knowledge|blog|article|calculator|faq|news|press|career|claim|/hi/|/hindi|/mr/|/ta/|/te/|/kn/|/gu/|/bn/|/ml/|'
                  r'\.pdf$|\.jpg$|\.png$|renewal|nav|fund-performance', re.I)

def get(url):
    time.sleep(1.0)
    r = subprocess.run(['curl', '-sSL', '--compressed', '-m', '60', '-A', UA, '-w', '\n%{http_code}', url], capture_output=True)
    body, _, code = r.stdout.rpartition(b'\n')
    if body[:2] == b'\x1f\x8b':
        body = gzip.decompress(body)
    return int(code or 0), body.decode('utf-8', 'ignore')

def sitemap_urls(url, depth=0):
    code, t = get(url)
    if code != 200: print('sitemap', url, code, file=sys.stderr); return []
    locs = [l.strip() for l in re.findall(r'<loc>\s*([^<]+?)\s*</loc>', t)]
    if '<sitemapindex' in t and depth < 2:
        out = []
        for l in locs:
            if not re.search(r'blog|article|image|video|news|knowledge', l, re.I): out += sitemap_urls(l, depth + 1)
        return out
    return locs

def toks(name):
    return [w for w in re.findall(r'[a-z0-9]+', name.lower().replace("'", '')) if w not in STOP and len(w) > 1]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--insurer', required=True); ap.add_argument('--sitemap', action='append', required=True)
    ap.add_argument('--apply', action='store_true'); ap.add_argument('--overwrite', action='store_true')
    ap.add_argument('--min', type=float, default=0.99, help='share of name tokens that must appear in the URL path')
    ap.add_argument('--rows', default='', help='comma list of row_ids to limit to')
    a = ap.parse_args()
    urls = []
    for s in a.sitemap: urls += sitemap_urls(s)
    urls = sorted({u for u in urls if not SKIP.search(u)})
    print(len(urls), 'candidate URLs from sitemap', file=sys.stderr)
    M = list(csv.DictReader(open('master_list.csv'))); cols = list(M[0].keys())
    rows = set(a.rows.split(',')) if a.rows else None
    changed = 0
    for r in M:
        if r['insurer_slug'] != a.insurer or (rows and r['row_id'] not in rows): continue
        if r['website_product_page_url'] and not a.overwrite: continue
        tk = toks(r['product_name'])
        if not tk: continue
        best = []
        for u in urls:
            path = urllib.parse.unquote(urllib.parse.urlparse(u).path).lower()
            last = re.findall(r'[a-z0-9]+', path.rstrip('/').rsplit('/', 1)[-1].replace('.html', ''))
            pw = set(re.findall(r'[a-z0-9]+', path))
            hit = sum(1 for t in tk if t in pw) / len(tk)
            extra = len([w for w in last if w not in tk and w not in STOP and w not in ('html', 'htm', 'aspx', 'php')])
            if hit >= a.min: best.append((hit, -extra, -len(path), u))
        best.sort(reverse=True)
        if not best: print(f"{r['row_id']:>4} {r['product_name'][:50]:50} -> (no match)"); continue
        u = best[0][3]
        alt = ' | also: ' + ', '.join(b[3] for b in best[1:3]) if len(best) > 1 else ''
        code = get(u)[0] if a.apply else ''
        print(f"{r['row_id']:>4} {r['product_name'][:50]:50} -> {u} {code}{alt}")
        if a.apply and code == 200:
            r['website_product_page_url'] = u; changed += 1
    if a.apply:
        with open('master_list.csv', 'w', newline='') as fh:
            w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(M)
        print('updated', changed, 'rows', file=sys.stderr)

if __name__ == '__main__':
    main()
