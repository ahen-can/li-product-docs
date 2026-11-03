"""Fetch pages for ONE insurer with curl (1 req/s) and save a JSON record like textdump.js:
{url,type,fetched_utc,status,final_url,title,h1,og_title,text,links,raw_file}.  PDFs: text via pdftotext.
Usage: python3 -I grab.py <outdir> <spec.json> <slug>"""
import sys, os, json, subprocess, time, hashlib, re, html, datetime, urllib.parse

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'

def html_to_rec(raw, base):
    t = raw.decode('utf-8', 'ignore')
    title = re.search(r'<title[^>]*>(.*?)</title>', t, re.S | re.I)
    og = re.search(r'<meta[^>]+property=["\']og:title["\'][^>]+content=["\']([^"\']*)', t, re.I)
    h1 = [re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', x))).strip() for x in re.findall(r'<h1[^>]*>(.*?)</h1>', t, re.S | re.I)]
    links = []
    for m in re.finditer(r'<a\b[^>]*href=["\']([^"\'#][^"\']*)["\'][^>]*>(.*?)</a>', t, re.S | re.I):
        u = urllib.parse.urljoin(base, html.unescape(m.group(1)).strip())
        links.append([u, re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', m.group(2)))).strip()[:200]])
    body = re.sub(r'<script.*?</script>|<style.*?</style>|<noscript.*?</noscript>', ' ', t, flags=re.S | re.I)
    body = re.sub(r'<(br|/p|/div|/li|/tr|/h\d|/td|/a)\b[^>]*>', '\n', body, flags=re.I)
    text = html.unescape(re.sub(r'<[^>]+>', ' ', body))
    text = '\n'.join(re.sub(r'[ \t\xa0]+', ' ', ln).strip() for ln in text.split('\n'))
    text = re.sub(r'\n{2,}', '\n', text)
    # JSON blobs embedded in scripts (Next.js etc.) often carry product names/UINs: keep their strings
    scripts = ' '.join(re.findall(r'<script[^>]*>(.*?)</script>', t, re.S | re.I))
    return {'title': html.unescape(title.group(1)).strip() if title else '', 'og_title': og.group(1) if og else '',
            'h1': [x for x in h1 if x][:3], 'text': text, 'links': links, 'script_text': scripts[:2_000_000]}

outdir, spec, slug = sys.argv[1], json.load(open(sys.argv[2])), sys.argv[3]
d = os.path.join(outdir, slug, 'text'); raw_d = os.path.join(outdir, slug, 'raw'); os.makedirs(d, exist_ok=True); os.makedirs(raw_d, exist_ok=True)
for it in spec[slug]:
    url = it['url']; fn = hashlib.md5(url.encode()).hexdigest()[:10]
    if os.path.exists(os.path.join(d, fn + '.json')) and not it.get('refresh'):
        continue
    rawp = os.path.join(raw_d, fn)
    r = subprocess.run(['curl', '-sSL', '--compressed', '--max-time', '60', '-A', UA, '-H', 'Accept-Language: en-IN,en;q=0.9',
                        '-o', rawp, '-w', '%{http_code}\t%{url_effective}', url], capture_output=True, text=True)
    st, final = (r.stdout.split('\t') + [''])[:2]
    raw = open(rawp, 'rb').read() if os.path.exists(rawp) else b''
    rec = {'url': url, 'type': it.get('type', ''), 'fetched_utc': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
           'status': int(st) if st.isdigit() else 0, 'final_url': final, 'raw_file': rawp, 'method': 'curl'}
    if raw[:4] == b'%PDF':
        rec.update({'title': '', 'og_title': '', 'h1': [], 'links': [], 'script_text': '',
                    'text': subprocess.run(['pdftotext', '-layout', rawp, '-'], capture_output=True, text=True).stdout})
    else:
        rec.update(html_to_rec(raw, final or url))
    json.dump(rec, open(os.path.join(d, fn + '.json'), 'w'))
    nu = len(set(re.findall(r'\b\d{3}[A-Z]\d{3}V\d{2}\b', rec['text'] + rec['script_text'])))
    print(f"{slug:18} {rec['status']:3} text={len(rec['text']):7} links={len(rec['links']):5} uins={nu:4} {it.get('type','')[:9]:9} {url[:100]}", flush=True)
    time.sleep(1.0)
