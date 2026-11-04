"""fq.py SPEC.json -> finds a verbatim quote per entry. Entry: {uin, section, field, rx, [pages]}.
Searches the field's own document (layout text, then reading-order text), shortest 1 to 3 line window matching rx.
Prints the hits; writes accept-format JSON to argv[2]."""
import json, re, sys
sys.argv_ = sys.argv
exec(open('scripts/s2_tools/fixquotes.py').read().split("def flagged")[0].replace("import importlib.util", "").replace("spec_ = importlib.util.spec_from_file_location('validate_ulip_json', 'scripts/validate_ulip_json.py')", ""))
ents = json.load(open(sys.argv[1])); out = []
for e in ents:
    j = json.load(open(f"features/ulip/{e['uin']}.json")); fld = j[e['section']][e['field']]
    lay, raw = pages(j, fld['doc']); best = None
    rx = re.compile(e['rx'], re.I)
    for src in (lay, raw):
        for p, txt in enumerate(src, 1):
            if e.get('pages') and p not in e['pages']: continue
            L = [re.sub(r'\s+', ' ', l).strip() for l in txt.split('\n') if l.strip()]
            for i in range(len(L)):
                for n in (1, 2, 3):
                    w = ' '.join(L[i:i + n])
                    if len(w) <= 290 and rx.search(w):
                        if best is None or len(w) < len(best[0]): best = (w, p)
                        break
        if best: break
    if best: out.append({'uin': e['uin'], 'section': e['section'], 'field': e['field'], 'quote': best[0], 'page': best[1]}); print(f"OK  {e['uin']} {e['field']} | {str(fld['value'])[:40]} | p{best[1]} | {best[0][:200]}")
    else: print(f"--  {e['uin']} {e['field']} no match")
json.dump(out, open(sys.argv[2], 'w'), indent=1)
