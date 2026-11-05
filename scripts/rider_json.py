#!/usr/bin/env python3
"""Builds features/riders/<rider UIN>.json from scripts/rider_specs/<UIN>.py and checks every quote.

    python3 -I scripts/rider_json.py 130A012V02 [more UINs]

A spec leaf is L(value, status, doc, quote, note=None). doc is 'brochure' or 'policy' (the rider's own stored files) or a
path under docs/. The builder finds the page where the quote appears (layout or raw text, ligatures and spacing
normalised), fails if the quote is on no page, and writes value, status, document label, page, quote and note."""
import sys, os, re, json, csv, subprocess, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def norm(s):
    s = s.replace('ﬁ', 'fi').replace('ﬂ', 'fl').replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    s = re.sub(r'­|-\n', '', s)
    return re.sub(r'\s+', ' ', s).strip().lower()

def pages(pdf, mode):
    out = subprocess.run(['pdftotext', '-' + mode, pdf, '-'], capture_output=True, text=True).stdout
    return [norm(p) for p in out.split('\f')]

def L(value, status, doc=None, quote=None, note=None):
    return {'value': value, 'status': status, 'doc': doc, 'quote': quote, 'note': note}

def build(uin):
    spec = importlib.util.spec_from_file_location('s', f'scripts/rider_specs/{uin}.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    slug = m.SLUG; base = f'docs/{slug}/riders/{uin}'
    idx = {r['file_path']: r for r in csv.DictReader(open('index.csv'))}
    cache = {}
    def pg(path):
        if path not in cache: cache[path] = (pages(path, 'layout'), pages(path, 'raw'))
        return cache[path]
    bad = 0
    def fill(o, path=''):
        nonlocal bad
        if isinstance(o, dict) and set(o) == {'value', 'status', 'doc', 'quote', 'note'}:
            if o['quote']:
                p = o['doc'] if o['doc'].startswith('docs/') else f'{base}/{o["doc"]}.pdf'
                q = norm(o['quote']); hit = None
                for pages_ in pg(p):
                    for i, t in enumerate(pages_):
                        if q in t: hit = i + 1; break
                    if hit: break
                if not hit: print('QUOTE NOT FOUND', path, '|', o['quote'][:90]); bad += 1
                o['page'] = hit; o['doc_path'] = p; o['doc'] = idx[p]['website_label'] if p in idx else p
            else: o['page'] = None; o['doc_path'] = None
            return o
        if isinstance(o, dict): return {k: fill(v, path + '/' + k) for k, v in o.items()}
        return o
    out = fill(m.SPEC)
    json.dump(out, open(f'features/riders/{uin}.json', 'w'), indent=1, ensure_ascii=False)
    print(uin, 'written;', 'quote problems:', bad)
    return bad

if __name__ == '__main__':
    sys.exit(1 if sum(build(u) for u in sys.argv[1:]) else 0)
