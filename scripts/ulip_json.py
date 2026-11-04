#!/usr/bin/env python3
"""Helpers to write features/ulip/<UIN>.json from a compact per-product spec (used by the extraction notes).

    from ulip_json import F, build
    build('130L100V03', {'charges': {'fund_management_charge': F(value, 'built-in', 'Policy Bond', 13, quote, note)}},
          new_features=[...], not_public=[...])

Fields left out of the spec are written as {value: null, status: 'not stated in public documents'}, so nothing is
guessed. documents_inventory is filled from results/deep_ulip_docs.csv and index.csv (website labels, URLs, paths).
The file is then checked with validate_ulip_json.py (quotes must be verbatim on the cited page).
"""
import csv, json, os, subprocess, sys, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

SCHEMA = json.load(open('briefs/ulip_feature_schema.json'))
GROUPS = [k for k, v in SCHEMA.items() if isinstance(v, dict) and k != '_about']

def F(value, status, doc=None, page=None, quote=None, note=None, quote_2=None, page_2=None, quote_3=None, page_3=None, quote_4=None, page_4=None):
    o = {'value': value, 'status': status, 'doc': doc, 'page': page, 'quote': quote, 'note': note}
    for n, q, pg in ((2, quote_2, page_2), (3, quote_3, page_3), (4, quote_4, page_4)):   # extra verbatim quotes when a table does not fit in 300 characters
        if q: o[f'quote_{n}'] = q; o[f'page_{n}'] = pg
    return o

def NS(note=None):
    return F(None, 'not stated in public documents', note=note)

def inventory(uin):
    inv = [r for r in csv.DictReader(open('results/deep_ulip_docs.csv')) if r['uin'] == uin]
    idx = {r['file_path']: r for r in csv.DictReader(open('index.csv')) if r['uin'] == uin}
    out, seen = [], set()
    for r in inv:
        key = (r['url'], r['website_label'])
        if key in seen: continue
        seen.add(key)
        dt = {'policy': 'policy_document', 'cis': 'CIS', 'bi': 'BI'}.get(r['doc_type'], r['doc_type'])
        out.append({'website_label': r['website_label'], 'doc_type': dt, 'url': r['url'], 'found_on_page_url': r['found_on_page_url'],
                    'pages': int(r['pages']) if str(r['pages']).isdigit() else None,
                    'stored_path': r['stored_path'] if r['status'] in ('ok', 'already stored', 'already stored (not linked from product page)') else None,
                    'status': r['status'], 'note': r['notes'] or None})
    for fp, r in idx.items():                                      # stored files the page no longer links
        if not any(o['stored_path'] == fp for o in out):
            lab = r.get('website_label') or urllib.parse.unquote(r['source_url']).rsplit('/', 1)[-1] or None   # unlabelled link: file name
            out.append({'website_label': lab, 'doc_type': r['doc_type'], 'url': r['source_url'],
                        'found_on_page_url': r['found_on_page_url'], 'pages': int(r['pages']) if r['pages'].isdigit() else None,
                        'stored_path': fp, 'status': 'already stored', 'note': r['notes'] or None})
    return out

def locate_pages(j):
    """Fill a missing page number by finding the quote in the cited document (same matching as the validator)."""
    import validate_ulip_json as V
    paths = {}
    for d in j['documents_inventory']:
        if d.get('stored_path'): paths.setdefault(d['website_label'], d['stored_path'])
    cache = {}
    def pages_of(sp):
        if sp not in cache:
            tp = sp.replace('docs/', 'text/', 1)[:-4] + '.txt'
            lay = open(tp).read().split('\f') if os.path.exists(tp) else []
            raw = subprocess.run(['pdftotext', sp, '-'], capture_output=True, text=True).stdout.split('\f')
            cache[sp] = [(lay[i] if i < len(lay) else '') + '\n' + (raw[i] if i < len(raw) else '') for i in range(max(len(lay), len(raw)))]
        return cache[sp]
    objs = [o for g in GROUPS for o in j[g].values()] + list(j['new_features_not_in_schema'])
    for o in objs:
        if o.get('quote') and o.get('doc') and not o.get('page') and o['doc'] in paths:
            for i, t in enumerate(pages_of(paths[o['doc']]), 1):
                if V.found(o['quote'], t): o['page'] = i; break
        for n in (2, 3, 4):
            if o.get(f'quote_{n}') and o.get('doc') and not o.get(f'page_{n}') and o['doc'] in paths:
                for i, t in enumerate(pages_of(paths[o['doc']]), 1):
                    if V.found(o[f'quote_{n}'], t): o[f'page_{n}'] = i; break

def build(uin, spec, new_features=(), not_public=(), extra_notes=None):
    j = {}
    for g in GROUPS:
        j[g] = {}
        for f in SCHEMA[g]:
            j[g][f] = spec.get(g, {}).get(f) or NS()
        unknown = set(spec.get(g, {})) - set(SCHEMA[g])
        if unknown: raise KeyError(f'{g}: fields not in schema: {unknown}')
    j['documents_inventory'] = inventory(uin)
    j['new_features_not_in_schema'] = list(new_features)
    j['data_not_public'] = list(not_public)
    locate_pages(j)
    if extra_notes: j['extraction_notes'] = extra_notes
    os.makedirs('features/ulip', exist_ok=True)
    json.dump(j, open(f'features/ulip/{uin}.json', 'w'), indent=1, ensure_ascii=False)
    return j
