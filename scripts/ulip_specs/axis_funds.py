"""Parse the Fund Management Charge table of an Axis Max Life prospectus (layout text) into fund dicts.
Each fund prints as: name line(s), an (SFIN: ...) fragment and a percentage, in either order."""
import re, subprocess

def parse(uin, doc='brochure'):
    pdf = f'docs/axis-max-life/{uin}/{doc}.pdf'
    pages = subprocess.run(['pdftotext', '-layout', pdf, '-'], capture_output=True, text=True).stdout.split('\f')
    start = next(i for i, p in enumerate(pages) if re.search(r'annual rate of Fund Management Charge|Charge \(per annum\)', p, re.I))
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

if __name__ == '__main__':
    import sys
    for f in parse(sys.argv[1]): print(f)
