"""Parse the Fund Management Charge table of an Axis Max Life prospectus (layout text) into fund dicts.
Each fund prints as: name line(s), an (SFIN: ...) fragment and a percentage, in either order."""
import re, subprocess

def parse(uin, doc='brochure'):
    out = _parse_sfin_table(uin, doc)
    return out if len(out) >= 5 else _parse_name_pct(uin, doc)

def _parse_sfin_table(uin, doc):
    pdf = f'docs/axis-max-life/{uin}/{doc}.pdf'
    pages = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout.split('\f')
    start = next((i for i, p in enumerate(pages) if re.search(r'annual rate of Fund Management Charge|Charge \(per annum\)', p, re.I)), None)
    if start is None: return []
    lines = []
    for p in pages[start:start + 4]:
        lines += [re.sub(r'\s{2,}', '  ', l.strip()) for l in p.split('\n') if l.strip()]
    out, name, sfin, pct = [], [], None, None
    def flush():
        nonlocal name, sfin, pct
        if name and pct is not None:
            out.append({'name': ' '.join(name).replace('( ', '(').strip(' ()'), 'SFIN': sfin, 'FMC_pct': float(pct)})
        name, sfin, pct = [], None, None
    hdr = next((i for i, l in enumerate(lines) if 'Name of Fund' in l), 0)
    lines = lines[hdr + 1:]
    for l in lines:
        if re.match(r'(Policy Administration|3\.\s*Policy Administration)', l): break
        m1 = re.search(r'\(*\s*SFIN:\s*(ULIF[0-9A-Z/ ]+?)\s*\)', l); m2 = re.search(r'\b(\d\.\d+)%', l)
        rest = re.sub(r'\(*\s*SFIN:.*?\)', '', l); rest = re.sub(r'\d\.\d+%', '', rest).strip(' ()')
        if rest and not re.search(r'Name of Fund|Charge \(per annum\)|Fund Value|only available|available only|-available|^Page \d+|^\d\.$|surrender or discontinuance|policy in first|annual rate|This is a charge|Fund Management Charge$', rest):
            if sfin is not None and pct is not None: flush()
            name.append(rest)
        if m1: sfin = m1.group(1).replace(' ', '')
        if m2: pct = m2.group(1)
        if sfin is not None and pct is not None and name: flush()
    return out


def _parse_name_pct(uin, doc='brochure'):
    """Tables that print 'Fund name   1.25%' on one line; SFINs come from the fund descriptions elsewhere in the prospectus."""
    pdf = f'docs/axis-max-life/{uin}/{doc}.pdf'
    full = subprocess.run(['pdftotext', pdf, '-'], capture_output=True, text=True).stdout
    flat = re.sub(r'\s+', ' ', full)
    sf = {}
    for m in re.finditer(r'(?:[a-z]{1,2}\)\s*)?([A-Z][A-Za-z0-9 &\.\-]+?(?:Fund|FUND)(?: II)?)\s*\(+\s*SFIN:\s*(ULIF[0-9A-Z/ ]+?)\s*\)', flat):
        sf.setdefault(m.group(1).strip().lower(), m.group(2).replace(' ', ''))
    pages = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout.split('\f')
    start = next(i for i, p in enumerate(pages) if re.search(r'Fund Management Charge \(p\.a\.\)|Fund Management Charge \(per annum\)', p))
    out = []
    for p in pages[start:start + 3]:
        for l in p.split('\n'):
            m = re.match(r'\s*(?:\d+\s+)?([A-Z][A-Za-z0-9 &\.\-]+?(?:Fund|FUND)(?: II)?)\s+(\d\.\d+)%\s*$', l)
            if m and m.group(1).strip() not in [o['name'] for o in out]:
                out.append({'name': m.group(1).strip(), 'SFIN': sf.get(m.group(1).strip().lower()), 'FMC_pct': float(m.group(2))})
        if any('Discontinuance Policy Fund' in o['name'] for o in out): break
    return out

if __name__ == '__main__':
    import sys
    for f in parse(sys.argv[1]): print(f)
