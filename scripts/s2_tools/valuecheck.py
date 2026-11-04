"""Cross-check: does each field's quote text contain the field's values?
Usage: python3 -I scripts/s2_tools/valuecheck.py [UIN ...] [--min-cover 0.5]
For every field with numbers in its value, the numbers are compared with the numbers in quote .. quote_4.
A field is flagged when fewer than min-cover of the distinct value numbers appear in the quotes."""
import json, os, re, sys, glob
SECTIONS = ['product', 'eligibility', 'charges', 'benefits', 'flexibility', 'funds', 'protection_add_ons', 'surrender_revival']
SKIP = {'uin', 'uin_in_brochure', 'fund_list', 'fund_count'}
WORDS = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'fifth': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 'twelve': 12, 'fifteen': 15, 'twice': 2, 'thrice': 3, 'double': 2, 'triple': 3, 'half': 0.5}
def nums(s):
    s = re.sub(r'(?<=\d),(?=\d)', '', str(s))
    s += ' ' + ' '.join(str(v) for w, v in WORDS.items() if re.search(r'\b' + w + r'\b', s, re.I))
    return {str(float(x)).rstrip('0').rstrip('.') for x in re.findall(r'\d+(?:\.\d+)?', s)}
def leaves(v):
    if isinstance(v, dict):
        for k, x in v.items():
            yield from leaves(x)
    elif isinstance(v, list):
        for x in v: yield from leaves(x)
    elif v is not None and not isinstance(v, bool):
        yield v
def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    cover = 0.5
    if '--min-cover' in sys.argv: cover = float(sys.argv[sys.argv.index('--min-cover') + 1]); args = [a for a in args if a != str(cover)]
    files = sorted(glob.glob('features/ulip/*.json')) if not args else [f'features/ulip/{a}.json' for a in args]
    tot = flagged = 0
    for f in files:
        j = json.load(open(f)); uin = os.path.basename(f)[:-5]; out = []
        for sec in SECTIONS:
            for key, fld in (j.get(sec) or {}).items():
                if key in SKIP or not isinstance(fld, dict) or 'value' not in fld: continue
                vn = set()
                for lf in leaves(fld['value']): vn |= nums(lf)
                if not vn: continue
                qn = set()
                for q in ('quote', 'quote_2', 'quote_3', 'quote_4'):
                    if fld.get(q): qn |= nums(fld[q])
                tot += 1
                got = len(vn & qn) / len(vn)
                if not qn:
                    out.append((sec, key, 'no quote', sorted(vn)[:6]))
                elif got < cover:
                    out.append((sec, key, f'cover {got:.0%}', sorted(vn - qn)[:6]))
        if out:
            flagged += len(out)
            print(uin, j['product'].get('product_name', {}).get('value', ''))
            for sec, key, why, miss in out: print(f'   {sec}.{key}: {why}; value numbers not in quotes: {miss}')
    print(f'fields with numbers: {tot}; flagged: {flagged}')
main()
