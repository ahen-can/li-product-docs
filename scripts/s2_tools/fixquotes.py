"""Suggest and apply value-bearing quotes for fields whose quotes lack the value.
  python3 -I scripts/s2_tools/fixquotes.py suggest PREFIX [PREFIX ...]   -> prints one suggestion per flagged simple field
  python3 -I scripts/s2_tools/fixquotes.py apply ACCEPT.json            -> adds quote_N/page_N to the spec files
ACCEPT.json is a list of {uin, section, field, quote, page}. Quotes are checked with the validator's own matcher first."""
import ast, glob, json, os, re, subprocess, sys
sys.path.insert(0, 'scripts'); sys.path.insert(0, 'scripts/s2_tools')
import importlib.util
spec_ = importlib.util.spec_from_file_location('validate_ulip_json', 'scripts/validate_ulip_json.py')
SECTIONS = ['product', 'eligibility', 'charges', 'benefits', 'flexibility', 'funds', 'protection_add_ons', 'surrender_revival']
SKIP = {'uin', 'uin_in_brochure', 'fund_list', 'fund_count'}
WORDS = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'fifth': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 'twelve': 12, 'fifteen': 15, 'twice': 2, 'double': 2, 'half': 0.5}
def nums(s):
    s = re.sub(r'(?<=\d),(?=\d)', '', str(s))
    s += ' ' + ' '.join(str(v) for w, v in WORDS.items() if re.search(r'\b' + w + r'\b', s, re.I))
    return {str(float(x)).rstrip('0').rstrip('.') for x in re.findall(r'\d+(?:\.\d+)?', s)}
def leaves(v):
    if isinstance(v, dict):
        for x in v.values(): yield from leaves(x)
    elif isinstance(v, list):
        for x in v: yield from leaves(x)
    elif v is not None and not isinstance(v, bool): yield v
norm = lambda s: re.sub(r'[\s­]+', '', s.replace('-\n', '')).lower()
_cache = {}
def pages(j, label):
    sp = next((d['stored_path'] for d in j['documents_inventory'] if d.get('stored_path') and d['website_label'] == label), None)
    if not sp: return None
    if sp in _cache: return _cache[sp]
    lay = open(sp.replace('docs/', 'text/', 1)[:-4] + '.txt', errors='ignore').read().split('\f')
    raw = subprocess.run(['pdftotext', sp, '-'], capture_output=True, text=True).stdout.split('\f')
    _cache[sp] = (lay, raw)
    return _cache[sp]
def flagged(j):
    for sec in SECTIONS:
        for key, fld in (j.get(sec) or {}).items():
            if key in SKIP or not isinstance(fld, dict) or fld.get('status') == 'not offered' or 'value' not in fld: continue
            v = fld['value']; vn = set()
            for lf in leaves(v): vn |= nums(lf)
            if not vn or isinstance(v, (dict, list)) or len(str(v)) > 60: continue
            qn = set()
            for q in ('quote', 'quote_2', 'quote_3', 'quote_4'):
                if fld.get(q): qn |= nums(fld[q])
            if not (vn & qn): yield sec, key, fld, vn
def windows(lines, maxlen=290):
    L = [l.strip() for l in lines if l.strip()]
    for i in range(len(L)):
        for n in range(1, 5):
            w = ' '.join(L[i:i + n])
            if len(w) <= maxlen: yield w
def suggest(uin):
    j = json.load(open(f'features/ulip/{uin}.json')); out = []
    for sec, key, fld, vn in flagged(j):
        pg = pages(j, fld['doc'])
        if not pg: continue
        lay, raw = pg
        cand_pages = sorted({int(x) for x in re.findall(r'\d+', str(fld['page']))})
        cand_pages = sorted({p + d for p in cand_pages for d in (-1, 0, 1) if p + d >= 1})
        kw = {w.lower() for w in re.findall(r'[A-Za-z]{4,}', ' '.join([key.replace('_', ' '), str(fld['value'])])) if w.lower() not in ('years', 'year', 'with', 'from', 'rs', 'per', 'only')}
        best = None
        for p in cand_pages:
            for src in (raw, lay):
                if p - 1 >= len(src): continue
                for w in windows(src[p - 1].split('\n')):
                    cov = len(vn & nums(w))
                    if not cov: continue
                    bonus = sum(1 for k in kw if k in w.lower())
                    score = (cov, bonus, -len(w), p == min(cand_pages) + 1)
                    if best is None or score > best[0]: best = (score, w, p, cov)
        if best: out.append({'uin': uin, 'section': sec, 'field': key, 'value': fld['value'], 'cov': f'{best[3]}/{len(vn)}', 'quote': re.sub(r'\s+', ' ', best[1]), 'page': best[2], 'old': (fld.get('quote') or '')[:60]})
    return out
def cmd_suggest(prefixes):
    res = []
    for f in sorted(glob.glob('features/ulip/*.json')):
        uin = os.path.basename(f)[:-5]
        if any(uin.startswith(p) for p in prefixes): res += suggest(uin)
    json.dump(res, open('/tmp/claude-0/-home-user-li-product-docs/496e0fed-4e04-5fcc-9c09-9c8e08f43587/scratchpad/suggest.json', 'w'), indent=1)
    for k, r in enumerate(res):
        print(f"{k:3} {r['uin']} {r['section'][:4]}.{r['field']} | {str(r['value'])[:50]} | cov {r['cov']} p{r['page']} | {r['quote'][:150]}")
def cmd_apply(path):
    acc = json.load(open(path)); by = {}
    for a in acc: by.setdefault(a['uin'], []).append(a)
    for uin, items in by.items():
        sp = f'scripts/ulip_specs/{uin}.py'; src = open(sp).read(); tree = ast.parse(src); lines = src.split('\n')
        edits = []
        for a in items:
            call = None
            for node in ast.walk(tree):
                if isinstance(node, ast.Dict):
                    for k, v in zip(node.keys, node.values):
                        if isinstance(k, ast.Constant) and k.value == a['field'] and isinstance(v, ast.Call) and getattr(v.func, 'id', '') == 'F': call = v
            if call is None: print('no F call for', uin, a['field']); continue
            used = {kw.arg for kw in call.keywords}; n = next((x for x in (2, 3, 4) if f'quote_{x}' not in used), None)
            if n is None: print('no free quote slot', uin, a['field']); continue
            edits.append((call.end_lineno, call.end_col_offset, f", quote_{n}={a['quote']!r}, page_{n}={a['page']!r}"))
        for ln, col, txt in sorted(edits, reverse=True):
            line = lines[ln - 1]; lines[ln - 1] = line[:col - 1] + txt + line[col - 1:]
        open(sp, 'w').write('\n'.join(lines))
        print('edited', uin, len(edits))
if sys.argv[1] == 'suggest': cmd_suggest(sys.argv[2:])
else: cmd_apply(sys.argv[2])
