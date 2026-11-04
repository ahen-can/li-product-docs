#!/usr/bin/env python3
"""Check features/ulip/<UIN>.json files against the schema and the stored documents.

    python3 -I scripts/validate_ulip_json.py [UIN ...]     # default: every file in features/ulip/

For every field object {value, status, doc, page, quote, note}:
  - status must be one of the schema's status_values;
  - a quote must be <= 300 characters and appear verbatim (whitespace and hyphenation at line ends ignored) on the
    cited page of the cited document; 'doc' is the website label, resolved to a file via documents_inventory;
  - 'not stated in public documents' must have a null value.
Also checks that every schema group and field is present. Exit code 1 if anything fails.
"""
import glob, json, os, re, subprocess, sys

S = json.load(open('briefs/ulip_feature_schema.json'))
STATUS = set(S['status_values'])
GROUPS = {k: v for k, v in S.items() if isinstance(v, dict) and k not in ('_about',)}
norm = lambda s: re.sub(r'[\s­]+', '', s.replace('-\n', '')).lower().replace('’', "'").replace('‘', "'") \
    .replace('“', '"').replace('”', '"').replace('–', '-').replace('—', '-').replace('ﬁ', 'fi').replace('ﬂ', 'fl')

LIGS = re.compile(r'ffi|ffl|ff|fi|fl|ti|tt|ft')
lig = lambda s: LIGS.sub('', norm(s))   # PDFs whose fonts drop ligatures ('par ally' for 'partially'): compare without them

norm2 = lambda s: norm(s.replace('-\n', '-'))                    # keep a real hyphen that ends a line
def found(q, t):
    return any(f(q) in f(t) for f in (norm, norm2, lig)) or lig(q) in LIGS.sub('', norm2(t))

def check(path):
    j = json.load(open(path)); errs = []; uin = j.get('product', {}).get('uin', {}).get('value') or os.path.basename(path)[:-5]
    inv = j.get('documents_inventory', [])
    by_label = {}
    for d in inv:
        if d.get('stored_path'):
            by_label.setdefault(d['website_label'], d['stored_path'])
    texts = {}
    def page_text(label, page):
        sp = by_label.get(label)
        if not sp: return None
        tp = sp.replace('docs/', 'text/', 1)[:-4] + '.txt'
        if tp not in texts:                                        # stored -layout text plus plain reading-order text of the PDF
            lay = open(tp).read().split('\f') if os.path.exists(tp) else []
            raw = subprocess.run(['pdftotext', sp, '-'], capture_output=True, text=True).stdout.split('\f') if os.path.exists(sp) else []
            n = max(len(lay), len(raw))
            texts[tp] = [(lay[i] if i < len(lay) else '') + '\n' + (raw[i] if i < len(raw) else '') for i in range(n)]
        pg = texts[tp]
        try: pages = [int(x) for x in re.findall(r'\d+', str(page))]
        except ValueError: pages = []
        if not pages: return None
        return ' '.join(pg[p - 1] for p in range(min(pages), max(pages) + 1) if 0 < p <= len(pg))
    for g, fields in GROUPS.items():
        if g not in j: errs.append(f'missing group {g}'); continue
        for f in fields:
            o = j[g].get(f)
            if o is None: errs.append(f'missing field {g}.{f}'); continue
            if o.get('status') not in STATUS: errs.append(f'{g}.{f}: bad status {o.get("status")!r}')
            if o.get('status') == 'not stated in public documents' and o.get('value') not in (None, '', []):
                errs.append(f'{g}.{f}: not stated but has a value')
            q = o.get('quote')
            if q:
                if len(q) > 300: errs.append(f'{g}.{f}: quote longer than 300 characters')
                t = page_text(o.get('doc'), o.get('page'))
                if t is None: errs.append(f'{g}.{f}: cannot resolve doc {o.get("doc")!r} page {o.get("page")!r}')
                elif not found(q, t): errs.append(f'{g}.{f}: quote not found on {o.get("doc")} p.{o.get("page")}: {q[:70]!r}')
    for k in ('new_features_not_in_schema', 'data_not_public'):
        if not isinstance(j.get(k), list): errs.append(f'{k} must be a list')
    for nf in j.get('new_features_not_in_schema', []):
        if nf.get('quote'):
            t = page_text(nf.get('doc'), nf.get('page'))
            if t is None or not found(nf['quote'], t): errs.append(f'new feature {nf.get("feature")!r}: quote not found')
    return errs

if __name__ != '__main__':
    pass
else:
  files = [f'features/ulip/{u}.json' for u in sys.argv[1:]] or sorted(glob.glob('features/ulip/*.json'))
  bad = 0
  for f in files:
      e = check(f)
      print(f'{os.path.basename(f)}: {"ok" if not e else str(len(e)) + " problems"}')
      for x in e[:40]: print('   ', x)
      bad += bool(e)
  sys.exit(1 if bad else 0)
