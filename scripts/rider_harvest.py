#!/usr/bin/env python3
"""Rider harvest: crawl an insurer's rider pages, download every rider document linked there, and store the ones that
print a rider UIN of that insurer.

    python3 -I scripts/rider_harvest.py SLUG "Insurer name" SEED_URL [SEED_URL ...] [--follow REGEX] [--max-pages N]

Seed pages are fetched, plus same-site pages they link whose URL matches --follow (default: "rider"). Every PDF link on
those pages (and PDF paths in embedded page data) is a candidate unless its name is plainly not a rider document
(claim forms, grievance policy and similar). Each candidate is downloaded once (1 request a second), checked (%PDF,
size, pdfinfo, text), and kept only if a rider UIN of the insurer (code + A or B + 3 digits + V + 2 digits) is printed in
it; the most frequent such UIN names the rider. Document type comes from the link label or file name (brochure, policy,
cis, leaflet), else "other". Stored as docs/<slug>/riders/<UIN>/<type>.pdf (type-2 for a second file), with text,
an index.csv row (doc_type rider_<type>) and a row in results/riders_downloaded.csv. Every candidate and its outcome
goes to results/rider_harvest_log.csv. Rider names come from analysis/riders/rider_list_council.csv where the UIN is
listed there. Only URLs found on the insurer's own pages are fetched."""
import argparse, csv, datetime, hashlib, html, os, re, subprocess, sys, time, urllib.parse, urllib.request
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
LIST = 'results/riders_downloaded.csv'
LOG = 'results/rider_harvest_log.csv'
LH = ['insurer', 'rider_uin', 'rider_name', 'doc_type', 'website_label', 'source_url', 'found_on_page_url', 'stored_path', 'pages', 'uin_in_document', 'status', 'notes', 'downloaded_utc']
GH = ['insurer', 'url', 'label', 'found_on', 'outcome', 'rider_uin', 'doc_type', 'stored_path', 'checked_utc']
SKIP = re.compile(r'grievance|claim|proposal|kyc|nomination|charter|whistle|privacy|csr|annual|disclosure|list[-_ ]of|isnp|'
                  r'fact[-_ ]?sheet|fund|aml|tat\b|booklet|handbook|policy[-_ ]for|code[-_ ]of|anti[-_ ]|fraud|form\b|forms|'
                  r'press|media|news|certificate|underwriting|sitemap|hindi|marathi|tamil|telugu|kannada|gujarati|bengali|'
                  r'malayalam|odia|punjabi|ombudsman|mandate|statement|addendum|tablet|specimen[-_ ]signature', re.I)
last = {}
def get(url, binary=False):
    host = urllib.parse.urlsplit(url).netloc
    wait = 1.1 - (time.time() - last.get(host, 0))
    if wait > 0: time.sleep(wait)
    last[host] = time.time()
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read(96 * 1024 * 1024)
    return data if binary else data.decode('utf-8', 'ignore')
def kind_of(label, url, first_page):
    s = (label + ' ' + urllib.parse.unquote(url)).lower()
    if re.search(r'\bcis\b|customer[-_ ]information', s): return 'cis'
    if re.search(r'leaflet|flyer|one[-_ ]?pager|2[-_ ]pager|at[-_ ]a[-_ ]glance|kfd|key[-_ ]feature', s): return 'leaflet'
    if re.search(r'polic(y|ies)[-_ ]?(doc|bond|contract|wording)|rider[-_ ]?(doc|wording)|\bbond\b|contract|terms|tandc|t&c|'
                 r'part[-_ ]?b|[-_]pd[-_.]|\bpd\b|endorsement|wordings', s): return 'policy'
    if re.search(r'brochure|prospectus|sales|literature|[-_]sl[-_.]|\bsl\b', s): return 'brochure'
    fp = first_page.lower()
    if re.search(r'policy document|part b|rider document|policy bond|terms and conditions', fp): return 'policy'
    if re.search(r'customer information sheet', fp): return 'cis'
    return 'other'
def norm_url(base, u):
    u = html.unescape(u.strip()).replace('\\/', '/')
    return urllib.parse.urljoin(base, u).split('#')[0]
def main():
    ap = argparse.ArgumentParser(); ap.add_argument('slug'); ap.add_argument('insurer'); ap.add_argument('seeds', nargs='+')
    ap.add_argument('--follow', default='rider'); ap.add_argument('--max-pages', type=int, default=40); ap.add_argument('--code')
    ap.add_argument('--skip', default='', help='regex: candidate URLs to leave out (for example withdrawn)')
    ap.add_argument('--extra-doc', default='', help='regex: also take document links (not ending .pdf) that match')
    a = ap.parse_args()
    council = {r['uin']: r for r in csv.DictReader(open('analysis/riders/rider_list_council.csv'))}
    code = a.code or next((u[:3] for u, r in council.items() if r['insurer'] == a.insurer), None)
    assert code, 'no insurer code'
    upat = re.compile(code + r'[AB]\d{3}V\d{2}')
    idx = list(csv.reader(open('index.csv'))); H = idx[0]
    shas = {(r[H.index('sha256')], r[H.index('uin')]) for r in idx[1:]}
    stored_urls = {r[H.index('source_url')] for r in idx[1:]}
    logged = {r['url'] for r in csv.DictReader(open(LOG))} if os.path.exists(LOG) else set()
    host = urllib.parse.urlsplit(a.seeds[0]).netloc.replace('www.', '')
    pages, queue, seen = [], list(a.seeds), set()
    cands = {}
    while queue and len(pages) < a.max_pages:
        p = queue.pop(0)
        if p in seen: continue
        seen.add(p)
        try: s = get(p)
        except Exception as e: print('page fail', p, e); continue
        pages.append(p)
        for m in re.finditer(r'<a\b[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', s, flags=re.S | re.I):
            u = norm_url(p, m.group(1)); lab = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', m.group(2)))).strip()
            if re.search(r'\.pdf($|[?/])', u, re.I) or (a.extra_doc and re.search(a.extra_doc, u)):
                cands.setdefault(u, (lab, p))
            elif host in u and re.search(a.follow, u, re.I) and u not in seen and not re.search(r'\.(jpg|png|css|js)$', u): queue.append(u)
        for m in re.finditer(r'(https?:\\?/\\?/[^"\'\s<>]+?\.pdf|/[^"\'\s<>]+?\.pdf)', s, flags=re.I):
            u = norm_url(p, m.group(1)); cands.setdefault(u, ('', p))
    print(len(pages), 'pages,', len(cands), 'document links')
    new = not os.path.exists(LOG)
    logf = open(LOG, 'a', newline=''); lw = csv.writer(logf)
    if new: lw.writerow(GH)
    kept = 0
    for u, (lab, fo) in cands.items():
        name = urllib.parse.unquote(u.split('?')[0].split('/')[-1])
        now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        if u in stored_urls or u in logged: continue
        rider_hint = re.search(r'rider', lab + name, re.I) or re.search(r'rider', fo, re.I) or upat.search(name)
        if (a.skip and re.search(a.skip, u, re.I)) or SKIP.search(name + ' ' + lab) or not rider_hint:
            lw.writerow([a.insurer, u, lab, fo, 'skipped (not a rider document by name)', '', '', '', now]); continue
        try: data = get(u, binary=True)
        except Exception as e: lw.writerow([a.insurer, u, lab, fo, f'download failed: {e}'[:120], '', '', '', now]); continue
        if data[:4] != b'%PDF': lw.writerow([a.insurer, u, lab, fo, 'not a PDF', '', '', '', now]); continue
        tmp = f'/tmp/rh_{hashlib.sha1(u.encode()).hexdigest()}.pdf'; open(tmp, 'wb').write(data)
        info = subprocess.run(['pdfinfo', tmp], capture_output=True, text=True).stdout
        mp = re.search(r'Pages:\s+(\d+)', info)
        if not mp: lw.writerow([a.insurer, u, lab, fo, 'pdfinfo failed', '', '', '', now]); continue
        pages_n = int(mp.group(1))
        txt = subprocess.run(['pdftotext', '-layout', tmp, '-'], capture_output=True, text=True).stdout
        if len(txt) < 200 * pages_n: lw.writerow([a.insurer, u, lab, fo, 'scanned (OCR needed), not stored', '', '', '', now]); continue
        found = upat.findall(txt.replace(' ', ''))
        if not found: lw.writerow([a.insurer, u, lab, fo, 'no rider UIN of this insurer printed', '', '', '', now]); continue
        uin = max(set(found), key=found.count)
        allu = re.findall(code + r'[A-Z]\d{3}V\d{2}', txt.replace(' ', ''))
        top = max(set(allu), key=allu.count)
        if top[3] not in 'AB' and allu.count(top) >= found.count(uin):
            lw.writerow([a.insurer, u, lab, fo, f'product document ({top}), names rider {uin}', uin, '', '', now]); continue
        sha = hashlib.sha256(data).hexdigest()
        if (sha, uin) in shas: lw.writerow([a.insurer, u, lab, fo, 'duplicate of a stored file', uin, '', '', now]); continue
        first = txt.split('\f')[0]
        if not (re.search(r'rider', lab + ' ' + name, re.I) or re.search(r'rider', re.sub(r'\s+', ' ', first)[:800], re.I)):
            lw.writerow([a.insurer, u, lab, fo, f'not a rider document (no "rider" in its name or first page), prints {uin}', uin, '', '', now]); continue
        kind = kind_of(lab, u, first)
        d = f'docs/{a.slug}/riders/{uin}'; os.makedirs(d, exist_ok=True)
        n, nm = 1, kind
        while os.path.exists(f'{d}/{nm}.pdf'): n += 1; nm = f'{kind}-{n}'
        fp = f'{d}/{nm}.pdf'; open(fp, 'wb').write(data)
        tp = f'text/{a.slug}/riders/{uin}/{nm}.txt'; os.makedirs(os.path.dirname(tp), exist_ok=True); open(tp, 'w').write(txt)
        c = council.get(uin)
        rname = c['rider_name'] if c else (lab or name)
        note = ('' if c else 'UIN not in the Council Sep-2026 rider list (other version or withdrawn). ') + \
               ('' if len(set(found)) == 1 else f'Other rider UINs also printed: {", ".join(sorted(set(found) - {uin}))}. ') + \
               ('Label and file name do not say the document type.' if kind == 'other' else '')
        row = {k: '' for k in H}
        row.update({'doc_id': f'{uin}-rider_{nm}', 'insurer': a.insurer, 'product_name': rname, 'uin': uin, 'linked_flag': 'R',
                    'doc_type': 'rider_' + kind, 'source_url': u, 'found_on_page_url': fo, 'download_date_utc': now, 'http_status': '200',
                    'sha256': sha, 'bytes': str(len(data)), 'pages': str(pages_n), 'is_scanned': 'N', 'file_path': fp, 'text_path': tp,
                    'status': 'ok', 'notes': note.strip(), 'website_label': lab or name})
        with open('index.csv', 'a', newline='') as o: csv.writer(o).writerow([row.get(k, '') for k in H])
        newl = not os.path.exists(LIST)
        with open(LIST, 'a', newline='') as o:
            w = csv.writer(o)
            if newl: w.writerow(LH)
            w.writerow([a.insurer, uin, rname, 'rider_' + kind, lab or name, u, fo, fp, pages_n, uin, 'ok', note.strip(), now])
        lw.writerow([a.insurer, u, lab, fo, 'stored', uin, kind, fp, now]); shas.add((sha, uin)); kept += 1
        print('stored', fp, kind, '|', rname[:60])
    logf.close()
    print(a.insurer, 'kept', kept)
if __name__ == '__main__': main()
