"""Find a per-1000 mortality rate table (age -> rate) in a policy document's layout text.
Usage: python3 -I calc/tools/extract_mortality.py <policy.txt> [start_line]
Prints page, line range and the table as JSON. Tables are read as 'age rate' pairs on each line;
the block with the longest run of consecutive ages wins. Check the output against the PDF page."""
import re, sys, json

def extract(path, start=0, pick=None):
    lines = open(path, encoding='utf-8', errors='replace').read().split('\n')
    page_of, pg = [], 1
    for l in lines:
        page_of.append(pg); pg += l.count('\f')
    pair = re.compile(r'(?<![\d.])(\d{1,3})\s{1,40}(\d{1,2}\.\d{2,6})(?![\d.%])')
    blocks, cur, last = [], {}, None
    for i in range(start, len(lines)):
        hits = [(int(a), float(r)) for a, r in pair.findall(lines[i]) if int(a) <= 120]
        # a row that wraps: the age sits alone on this line and its rate starts the next line
        lone = re.match(r'^(?:.*\s)?(\d{1,3})\s*$', pair.sub('', lines[i]))
        if lone and i + 1 < len(lines):
            nxt = re.match(r'^\s*(\d{1,2}\.\d{2,6})\s*$', lines[i + 1])
            if nxt and int(lone.group(1)) <= 120:
                hits.append((int(lone.group(1)), float(nxt.group(1))))
        if hits:
            for a, r in hits: cur.setdefault(a, (r, i))
            last = i
        elif last is not None and i - last > 12:
            if cur: blocks.append(cur)
            cur, last = {}, None
    if cur: blocks.append(cur)
    def run(b):
        ages = sorted(b); best = n = 1
        for x, y in zip(ages, ages[1:]):
            n = n + 1 if y == x + 1 else 1; best = max(best, n)
        return best
    blocks.sort(key=run, reverse=True)
    out = []
    for b in blocks[:3]:
        ln = [v[1] for v in b.values()]
        out.append({'run': run(b), 'ages': f'{min(b)}-{max(b)}', 'lines': f'{min(ln)+1}-{max(ln)+1}', 'pages': sorted({page_of[x] for x in ln}),
                    'table': {a: b[a][0] for a in sorted(b)}})
    return out

if __name__ == '__main__':
    for b in extract(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 0):
        t = b.pop('table'); print(b, {k: t[k] for k in (0, 18, 30, 40, 50, 60, 70) if k in t})
