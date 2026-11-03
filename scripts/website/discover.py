"""Find product-list / UIN-list / withdrawn-product pages on insurer websites.
Usage: python3 -I discover.py <outdir> [slug ...]
Writes <outdir>/<slug>/home.html, sitemap snapshots and candidates.tsv (url, anchor text, why)."""
import sys, os, re, subprocess, time, html, urllib.parse, json

SITES = {
    'lic': 'https://licindia.in/', 'sbi-life': 'https://www.sbilife.co.in/', 'hdfc-life': 'https://www.hdfclife.com/',
    'icici-life': 'https://www.icicilife.com/', 'axis-max-life': 'https://www.axismaxlife.com/', 'tata-aia': 'https://www.tataaia.com/',
    'bajaj-life': 'https://www.bajajlifeinsurance.com/', 'absli': 'https://lifeinsurance.adityabirlacapital.com/',
    'kotak-life': 'https://www.kotaklife.com/', 'pnb-metlife': 'https://www.pnbmetlife.com/', 'canara-hsbc': 'https://www.canarahsbclife.com/',
    'indiafirst': 'https://www.indiafirstlife.com/', 'sud-life': 'https://www.sudlife.in/', 'indusind-nippon': 'https://www.indusindnipponlife.com/',
    'shriram-life': 'https://www.shriramlife.com/', 'ageas-federal': 'https://www.ageasfederal.com/', 'generali-central': 'https://www.generalicentrallife.com/',
    'bharti-life': 'https://www.bhartiaxa.com/', 'edelweiss-life': 'https://www.edelweisslife.in/', 'pramerica-life': 'https://pramericalife.in/',
    'aviva-life': 'https://www.avivaindia.com/', 'bandhan-life': 'https://www.bandhanlife.com/', 'go-digit-life': 'https://www.godigit.com/life-insurance',
    'acko-life': 'https://www.acko.com/life-insurance/', 'creditaccess-life': 'https://www.creditaccesslife.in/',
}
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
KEY = re.compile(r'uin|withdraw|discontinu|list[-_ ]?of[-_ ]?product|all[-_ ]?plans|all[-_ ]?products|view[-_ ]?all|product[-_ ]?list|'
                 r'products?[-_ ]?(and|&)[-_ ]?riders|closed[-_ ]?product|our[-_ ]?products|insurance[-_ ]?plans|existing[-_ ]?product', re.I)

def get(url, path):
    r = subprocess.run(['curl', '-sSL', '--compressed', '--max-time', '40', '-A', UA, '-o', path, '-w', '%{http_code} %{url_effective}', url],
                       capture_output=True, text=True)
    time.sleep(1.0)
    return r.stdout.strip()

def links(path, base):
    try: t = open(path, encoding='utf-8', errors='ignore').read()
    except FileNotFoundError: return []
    out = []
    for m in re.finditer(r'<a\b[^>]*href=["\']([^"\'#]+)["\'][^>]*>(.*?)</a>', t, re.S | re.I):
        u = urllib.parse.urljoin(base, html.unescape(m.group(1)).strip())
        txt = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', m.group(2)))).strip()
        out.append((u, txt))
    for m in re.finditer(r'<loc>([^<]+)</loc>', t):
        out.append((m.group(1).strip(), '(sitemap)'))
    return out

outdir = sys.argv[1]; slugs = sys.argv[2:] or list(SITES)
summary = {}
for slug in slugs:
    base = SITES[slug]; d = os.path.join(outdir, slug); os.makedirs(d, exist_ok=True)
    st = get(base, os.path.join(d, 'home.html'))
    root = '{0.scheme}://{0.netloc}/'.format(urllib.parse.urlparse(st.split(' ', 1)[-1] if ' ' in st else base))
    sm = get(root + 'sitemap.xml', os.path.join(d, 'sitemap.xml'))
    L = links(os.path.join(d, 'home.html'), base) + links(os.path.join(d, 'sitemap.xml'), root)
    # follow sitemap indexes one level
    for u, t in list(L):
        if t == '(sitemap)' and u.endswith('.xml') and len([x for x in os.listdir(d) if x.startswith('sm_')]) < 8:
            p = os.path.join(d, 'sm_%d.xml' % len([x for x in os.listdir(d) if x.startswith('sm_')]))
            get(u, p); L += links(p, root)
    cands = {}
    for u, t in L:
        if KEY.search(u) or KEY.search(t):
            cands.setdefault(u, t)
    with open(os.path.join(d, 'candidates.tsv'), 'w') as f:
        for u, t in cands.items(): f.write(f'{u}\t{t[:80]}\n')
    summary[slug] = {'home': st, 'sitemap': sm.split(' ')[0], 'links': len(L), 'candidates': len(cands)}
    print(slug, summary[slug], flush=True)
json.dump(summary, open(os.path.join(outdir, 'summary_%d.json' % int(time.time())), 'w'), indent=1)
