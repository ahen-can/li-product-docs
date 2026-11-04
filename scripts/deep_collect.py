#!/usr/bin/env python3
"""ULIP deep discovery, step 1: collect each product's policy document, CIS, BI and fund documents.

    python3 -I scripts/deep_collect.py --insurer bharti-life            # one insurer from briefs/ulip_deep_set.csv
    python3 -I scripts/deep_collect.py --insurer bharti-life --dry-run  # list the labelled links only

For each product, the script reads only that product's own page (product_page_url in the deep set), so it never
picks up a neighbouring product's file. It classifies every document link by the site's own label (anchor text,
else file name), downloads it, and keeps it only if:
  - the body starts with %PDF, pdfinfo opens it and it is under 95 MB;
  - for policy/CIS/BI/brochure: the product code (UIN without version) is in the text, by OCR if the PDF is
    image-only; a different version is kept and noted (CLAUDE.md);
  - for fund documents: the product name is on the first pages (company-wide factsheets are skipped).
Each kept file is stored as docs/<slug>/<UIN>/<doc_type>.pdf (-2, -3 for more of a type), with text in text/, one
index.csv row including website_label, and one row in results/deep_ulip_docs.csv (the documents inventory).
A brochure is re-downloaded only if the product page links a different file that passes the checks (stored as
brochure-2 with a note); the stored brochure is kept.
"""
import argparse, csv, datetime, hashlib, os, re, subprocess, sys, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import light_discovery as L

SLUG = {'Bharti Life': 'bharti-life', 'SBI Life': 'sbi-life', 'HDFC Life': 'hdfc-life', 'Tata AIA Life': 'tata-aia',
        'Bajaj Life': 'bajaj-life', 'Axis Max Life': 'axis-max-life', 'LIC': 'lic', 'Aditya Birla Sun Life': 'absli',
        'Canara HSBC Life': 'canara-hsbc', 'ICICI Life': 'icici-life', 'Kotak Mahindra Life': 'kotak-life'}
KIND = [  # (doc_type, label pattern); first match wins, so order matters
    ('cis', r'customer information sheet|\bcis\b|key feature'),
    ('bi', r'benefit illustration|sales illustration|sample illustration|\bbi\b'),
    ('policy', r'policy[\s_-]*(bond|document|contract|wording|terms)|terms[\s_-]*(and|&)[\s_-]*conditions|specimen|sample[\s_-]*policy|'
               r'part[\s_-]*b\b|policy[\s_-]*doc|\bpd\b|_pd_|-pd\.|t\s*&\s*c\b|tnc'),
    ('fund_factsheet', r'fund[\s_-]*(fact[\s_-]*sheet|performance|details|options|brochure)|factsheet'),
    ('leaflet', r'leaflet|one[\s_-]*pager|flyer'),
    ('brochure', r'brochure|prospectus|sales[\s_-]*lit|\bsl\b|_sl_|-sl[-_.]'),
]
SKIP = re.compile(r'claim|proposal[\s_-]*form|hindi|marathi|tamil|telugu|kannada|gujarati|bengali|malayalam|odia|punjabi|'
                  r'rider|grievance|nomination|kyc|annual[\s_-]*report|disclosure|whistle|privacy|csr|policy[\s_-]*for|'
                  r'underwriting|code[\s_-]*of[\s_-]*conduct|service[\s_-]*manual|calculator|form[\s_-]*\d|policy[\s_-]*loans?', re.I)
IDX_EXTRA = 'website_label'

def kind_of(label, url):
    blob = (label + ' ' + urllib.parse.unquote(url).rsplit('/', 1)[-1]).lower()
    if SKIP.search(blob): return None
    for k, rx in KIND:
        if re.search(rx, blob, re.I): return k
    return None

def ensure_index_column():
    rows = list(csv.DictReader(open('index.csv'))); cols = list(rows[0].keys()) if rows else []
    if IDX_EXTRA not in cols:
        cols.append(IDX_EXTRA)
        for r in rows: r[IDX_EXTRA] = ''
        L.write_index(rows, cols)
    return cols

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--insurer', required=True); ap.add_argument('--dry-run', action='store_true')
    ap.add_argument('--only', default=''); ap.add_argument('--tmp', default='/tmp/deep_cache')
    ap.add_argument('--extra-page', action='append', default=[],
                    help='central document page (e.g. HDFC /policy-documents); only links naming the product are taken')
    a = ap.parse_args(); os.makedirs(a.tmp, exist_ok=True)
    D = [r for r in csv.DictReader(open('briefs/ulip_deep_set.csv')) if SLUG.get(r['insurer']) in a.insurer.split(',')
         and (not a.only or r['uin'] in a.only.split(','))]
    M = {m['uin']: m for m in csv.DictReader(open('master_list.csv'))}
    cols = ensure_index_column()
    invf = 'results/deep_ulip_docs.csv'
    inv_cols = ['insurer', 'product_name', 'uin', 'website_label', 'doc_type', 'status', 'url', 'found_on_page_url',
                'stored_path', 'pages', 'uin_in_document', 'is_scanned', 'notes', 'checked_utc']
    inv = list(csv.DictReader(open(invf))) if os.path.exists(invf) else []
    done_uins = {r['uin'] for r in inv}
    for d in D:
        uin, slug = d['uin'], SLUG[d['insurer']]
        prod = dict(M.get(uin, {}), product_code=uin[:7], uin=uin, product_name=d['product_name'])
        page = d['product_page_url']
        now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        links = L.page_links(page, a.tmp) if page else []
        norm = lambda x: re.sub(r'[^a-z0-9]+', ' ', x.lower()).strip()
        pname = norm(re.sub(r'^(hdfc life|sbi life|tata aia( life)?( insurance)?|bajaj life|axis max life|absli|canara hsbc life( insurance)?|lic.?s?|bharti axa life)\s+', '', d['product_name'].lower()))
        ver = int(uin[-2:]); xl = []
        for xp in a.extra_page:                                      # central pages: only links naming this product and version
            for u, t in L.page_links(xp, a.tmp):
                blob = norm(urllib.parse.unquote(u).rsplit('/', 1)[-1] + ' ' + t)
                if not pname or pname not in blob or 'appendix' in blob: continue
                vs = {int(x) for x in re.findall(r'(?:^|\s)(?:v|' + uin[:7].lower() + r'v)0?(\d{1,2})(?=\s|$)', blob)}
                if vs and ver not in vs: continue
                xl.append((u, t))
        if any('-live/' in u for u, t in xl): xl = [(u, t) for u, t in xl if '-withdrawn/' not in u]
        links += xl
        seen = {}
        for u, t in links:
            if urllib.parse.urlparse(u).scheme not in ('http', 'https'): continue
            low = u.lower().split('?')[0]
            doclike = low.endswith('.pdf') or '/documents/' in low or re.search(r'brochure|prospectus|policy|cis|illustration|fact', low + ' ' + t.lower())
            if not doclike: continue
            k = kind_of(t, u)
            if not k: continue
            if not t:                                                  # link from page data / footer: needs the product name in the URL
                toks = L.name_tokens(d['product_name']); fn = urllib.parse.unquote(u).lower()
                if not toks or sum(1 for tk in toks if tk in fn) < max(1, -(-2 * len(toks) // 3)): continue
            if u not in seen or (t and not seen[u][1]): seen[u] = (k, t)
        labelled = {k for k, t in seen.values() if t}               # unlabelled (footer/page-data) links only fill a gap
        seen = {u: v for u, v in seen.items() if v[1] or v[0] not in labelled}
        if a.dry_run:
            print(f"== {uin} {d['product_name']} | {page}")
            for u, (k, t) in seen.items(): print(f"   {k:15} {t[:45]!r:48} {u[-90:]}")
            continue
        if uin in done_uins: print('skip (already in inventory)', uin); continue
        idx = list(csv.DictReader(open('index.csv')))
        have = [r for r in idx if r['uin'] == uin]
        have_sha = {r['sha256']: r for r in idx}
        rows_out = []
        for u, (k, t) in seen.items():
            if k == 'brochure' and any(r['doc_type'] == 'brochure' for r in have) and not t:
                rows_out.append({'insurer': d['insurer'], 'product_name': d['product_name'], 'uin': uin, 'website_label': urllib.parse.unquote(u).rsplit('/', 1)[-1],
                                 'doc_type': k, 'status': 'not stored (unlabelled link; brochure already stored)', 'url': u, 'found_on_page_url': page, 'stored_path': '',
                                 'pages': '', 'uin_in_document': '', 'is_scanned': '', 'notes': '', 'checked_utc': now}); continue
            label = t or urllib.parse.unquote(u).rsplit('/', 1)[-1]
            rec = {'insurer': d['insurer'], 'product_name': d['product_name'], 'uin': uin, 'website_label': label, 'doc_type': k,
                   'status': '', 'url': u, 'found_on_page_url': page, 'stored_path': '', 'pages': '', 'uin_in_document': '',
                   'is_scanned': '', 'notes': '', 'checked_utc': now}
            if k == 'leaflet' and any(r['doc_type'] == 'brochure' for r in have):
                rec.update(status='not stored (leaflet; brochure already stored)'); rows_out.append(rec); continue
            prev = next((r for r in have if r['source_url'] == u), None)
            if prev:                                                   # already stored (light pass): label it
                prev[IDX_EXTRA] = prev[IDX_EXTRA] or label
                rec.update(status='already stored', stored_path=prev['file_path'], pages=prev['pages'], is_scanned=prev['is_scanned'])
                rows_out.append(rec); continue
            tmp = os.path.join(a.tmp, 'dl.pdf')
            code, eff = L.fetch(u, tmp)
            body = open(tmp, 'rb').read() if os.path.exists(tmp) else b''
            if code == 200 and body[:4] != b'%PDF':
                rec.update(status='web page (not stored)', notes='link opens a web page, not a document'); rows_out.append(rec); continue
            if code != 200 or body[:4] != b'%PDF':
                rec.update(status='failed', notes=f'HTTP {code}, not a PDF' if code == 200 else f'HTTP {code}'); rows_out.append(rec); continue
            if len(body) > 95 * 2**20:
                rec.update(status='manual', notes='file over 95 MB'); rows_out.append(rec); continue
            if subprocess.run(['pdfinfo', tmp], capture_output=True).returncode != 0:
                rec.update(status='failed', notes='pdfinfo cannot open it'); rows_out.append(rec); continue
            txt = L.pdf_text(tmp); npg = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', tmp], capture_output=True, text=True).stdout).group(1))
            ocr = ''
            if len(txt.strip()) / max(npg, 1) < 200 and npg <= 80:
                txt = L.ocr_text(tmp, '200'); ocr = 'scanned - text by OCR'
            flat = re.sub(r'\s+', '', txt)
            code_rx = uin[:4] + ('O?' if ocr else '') + ''.join('[0O]' if c == '0' else c for c in uin[4:7]) + r'V\d{2}'
            found = sorted({x[:4] + x[4:].replace('O', '0')[-6:] for x in re.findall(code_rx, flat)})
            if k == 'fund_factsheet':
                toks = L.name_tokens(d['product_name'])
                if not found and not (toks and all(tk in txt[:6000].lower() for tk in toks)):
                    rec.update(status='skipped', notes='fund document does not name this product (company-wide)'); rows_out.append(rec); continue
            elif not found:
                if not ocr and npg <= 60 and len(txt.strip()) / max(npg, 1) < 1500:
                    txt = L.ocr_text(tmp, '200'); ocr = 'UIN and text read by OCR (image-heavy PDF)'
                    flat = re.sub(r'\s+', '', txt)
                    code_rx = uin[:4] + 'O?' + ''.join('[0O]' if c == '0' else c for c in uin[4:7]) + r'V\d{2}'
                    found = sorted({x[:4] + x[4:].replace('O', '0')[-6:] for x in re.findall(code_rx, flat)})
                if not found:
                    rec.update(status='failed', notes='product code not in the document'); rows_out.append(rec); continue
            sha = hashlib.sha256(body).hexdigest()
            n = 1 + sum(1 for r in have + [x for x in rows_out if x['status'] == 'ok'] if r.get('doc_type') == k or
                        os.path.basename(r.get('file_path', r.get('stored_path', ''))).split('.')[0].split('-')[0] == k)
            name = k if n == 1 else f'{k}-{n}'
            d_doc = os.path.join('docs', slug, uin); d_txt = os.path.join('text', slug, uin)
            os.makedirs(d_doc, exist_ok=True); os.makedirs(d_txt, exist_ok=True)
            fp, tp = os.path.join(d_doc, name + '.pdf'), os.path.join(d_txt, name + '.txt')
            dup = have_sha.get(sha)
            notes = [x for x in [('' if uin in found or not found else 'document shows ' + ','.join(found)), ocr] if x]
            if dup and dup['uin'] == uin:                            # this product already has these exact bytes
                rec.update(status='already stored (same file)', stored_path=dup['file_path'], pages=npg, notes='identical to ' + dup['doc_id'])
                rows_out.append(rec); continue
            if dup:
                fp, tp = dup['file_path'], dup['text_path']; notes.append('same file as ' + dup['doc_id'])
            else:
                open(fp, 'wb').write(body); open(tp, 'w').write(txt)
            if k == 'brochure': notes.append('product page links a different brochure from the one stored in the light pass')
            row = {c: '' for c in cols}
            row.update({'doc_id': f"{uin}-{name}", 'insurer': d['insurer'], 'product_name': d['product_name'], 'uin': uin,
                        'linked_flag': uin[3], 'par_flag': '', 'irdai_description_line': '', 'doc_type': k, 'source_url': eff or u,
                        'found_on_page_url': page, 'download_date_utc': now, 'http_status': code, 'sha256': sha, 'bytes': len(body),
                        'pages': npg, 'is_scanned': 'Y' if ocr.startswith('scanned') else 'N', 'file_path': fp, 'text_path': tp,
                        'status': 'ok', 'notes': '; '.join(notes), IDX_EXTRA: label})
            idx.append(row); have.append(row); have_sha[sha] = row
            rec.update(status='ok', stored_path=fp, pages=npg, uin_in_document=','.join(found), is_scanned=row['is_scanned'], notes=row['notes'])
            rows_out.append(rec)
        # label the stored light-pass brochure if the page links it; otherwise list it as not linked from the page
        for r in have:
            if r['doc_type'] in ('brochure', 'policy', 'leaflet') and not any(x['url'] == r['source_url'] for x in rows_out) and r.get('download_date_utc', '') < now:
                rows_out.append({'insurer': d['insurer'], 'product_name': d['product_name'], 'uin': uin, 'website_label': r.get(IDX_EXTRA, ''),
                                 'doc_type': r['doc_type'], 'status': 'already stored (not linked from product page)', 'url': r['source_url'],
                                 'found_on_page_url': r['found_on_page_url'], 'stored_path': r['file_path'], 'pages': r['pages'],
                                 'uin_in_document': '', 'is_scanned': r['is_scanned'], 'notes': r['notes'], 'checked_utc': now})
        L.write_index(idx, cols)
        inv = [x for x in inv if x['uin'] != uin] + rows_out
        with open(invf + '.tmp', 'w', newline='') as fh:
            w = csv.DictWriter(fh, fieldnames=inv_cols); w.writeheader(); w.writerows(inv)
        os.replace(invf + '.tmp', invf)
        got = {}
        for x in rows_out:
            if x['status'] in ('ok', 'already stored'): got[x['doc_type']] = got.get(x['doc_type'], 0) + 1
        print(f"{uin} {d['product_name'][:40]:40} {got} {[x['status'] for x in rows_out if x['status'] not in ('ok', 'already stored')]}", flush=True)

if __name__ == '__main__':
    main()
