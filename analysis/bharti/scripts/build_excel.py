"""Build analysis/bharti/bharti_analysis.xlsx from bharti_trend_data.csv and document_inventory.csv.

Every number in the workbook is read from bharti_trend_data.csv (lakh and '000 converted to Rs crore here).
Run after build_trend_data.py:  python3 analysis/bharti/scripts/build_excel.py
"""
import csv
import os

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

HERE = os.path.dirname(__file__)
BASE = os.path.normpath(os.path.join(HERE, '..'))
R = list(csv.DictReader(open(os.path.join(BASE, 'bharti_trend_data.csv'))))
INV = list(csv.reader(open(os.path.join(BASE, 'document_inventory.csv'))))

YEARS = ['FY21', 'FY22', 'FY23', 'FY24', 'FY25', 'FY26']
YQ = YEARS + ['Q1 FY26', 'Q1 FY27']
BOLD = Font(bold=True)
TITLE = Font(bold=True, size=13)
HFILL = PatternFill('solid', fgColor='DDE4EE')
FLAG = PatternFill('solid', fgColor='FFF2CC')
WRAP = Alignment(wrap_text=True, vertical='top')


def get(metric, seg, per, unit=None):
    for r in R:
        if r['metric'] == metric and r['segment_or_product'] == seg and r['period'] == per and (unit is None or r['unit'] == unit):
            v = r['value']
            try:
                return float(v)
            except ValueError:
                return v
    return None


def cr(v, unit):
    if v is None:
        return None
    return round(v / 100.0, 2) if unit == 'Rs lakh' else round(v / 10000.0, 2) if unit == "Rs '000" else v


class Sheet:
    def __init__(self, ws):
        self.ws = ws
        self.row = 1

    def title(self, text, note=None):
        self.ws.cell(self.row, 1, text).font = TITLE
        self.row += 1
        if note:
            c = self.ws.cell(self.row, 1, note)
            c.alignment = Alignment(wrap_text=False)
            self.row += 1

    def table(self, name, header, rows, fmt=None, source=None, flags=()):
        self.ws.cell(self.row, 1, name).font = BOLD
        self.row += 1
        for j, h in enumerate(header, 1):
            c = self.ws.cell(self.row, j, h)
            c.font = BOLD
            c.fill = HFILL
            c.alignment = WRAP
        self.row += 1
        for r in rows:
            for j, v in enumerate(r, 1):
                c = self.ws.cell(self.row, j, v)
                if fmt and j > 1 and isinstance(v, (int, float)):
                    c.number_format = fmt
                if (r[0], header[j - 1]) in flags or (r[0], '*') in flags:
                    c.fill = FLAG
            self.row += 1
        if source:
            self.ws.cell(self.row, 1, 'Source: ' + source).font = Font(italic=True, size=9)
            self.row += 1
        self.row += 1

    def widths(self, first=46, rest=13, n=16):
        self.ws.column_dimensions['A'].width = first
        for j in range(2, n + 1):
            self.ws.column_dimensions[get_column_letter(j)].width = rest


def series(metric, seg, periods, unit=None, conv=None):
    out = []
    for p in periods:
        v = get(metric, seg, p, unit)
        if conv and v is not None:
            v = cr(v, conv)
        out.append(v)
    return out


wb = Workbook()

# ------------------------------------------------------------------ Notes
ws = wb.active
ws.title = 'Notes'
notes = [
    ('Bharti Life analysis for deliverable 01 (S3)', TITLE),
    ('Built by analysis/bharti/scripts/build_excel.py from bharti_trend_data.csv. Every number has a source file, form and page in that CSV.', None),
    ('', None),
    ('Units', BOLD),
    ('Amounts are Rs crore unless a header says otherwise. PDs report Rs lakh; annual-report schedules report Rs \'000. The CSV keeps the original value and unit.', None),
    ('Years are financial years ending 31 March. Q1 is April-June. H1 FY27 is April-September 2026.', None),
    ('', None),
    ('Which source for what', BOLD),
    ('Segment premium: PD Form L-1-A-RA line (a) Premium. First year, renewal and single totals: PD L-4.', None),
    ('Ratios, persistency, conservation, solvency, ticket size: PD L-22. Channels: PD L-37 (group) and L-38 (individual). AUM: PD L-3 (L-12 + L-13 + L-14). Claims: PD L-40.', None),
    ('NBP by segment: annual-report Schedule 1 (FY21 report p94, FY22 report p60, FY24 report p117). PDs do not publish NBP by segment.', None),
    ('EoM against the regulatory limit: annual-report notes to accounts. PDs give only EoM as a share of gross premium (L-22 row 6), which is a different measure.', None),
    ('Product figures: Bharti KPI disclosures (Product Performance, Monthly Product Performance and Improvement Report).', None),
    ('', None),
    ('Cells shaded yellow need care', BOLD),
    ('FY23 NBP by segment is reconstructed. The FY23 comparative on FY24 annual report p124 prints some cells one column off. The cells were moved back so that each segment total matches FY23 PD L-1-A-RA; the result also matches L-37 group NBP (21,462 lakh) and L-22 linked share (12.5%) and single share (5.0%). User confirmed 5 Nov 2026.', None),
    ('FY25 and FY26 NBP by segment are derived, not disclosed: FY24 segment NBP x (1 + L-22 segment NBP growth). The derived segments add to within 5 lakh (FY25) and 18 lakh (FY26) of the disclosed L-4 total.', None),
    ('', None),
    ('Rounding and small differences (accepted)', BOLD),
    ('Segment premiums in L-1-A-RA add to the printed total within 1 lakh (FY21, FY22, FY23, FY24).', None),
    ('FY24 non-par group premium: 14,151 lakh in the FY24 PD, 14,152 lakh in the FY25 PD comparative.', None),
    ('L-37 + L-38 NBP differs from L-4 first year + single by up to 63 lakh a year (FY23).', None),
    ('EoM charged to shareholders: FY22 23,14,373 (auditors) vs 2,314,375 (note); FY23 20,97,385 (FY23 report) vs 20,97,387 (FY24 report), Rs \'000.', None),
    ('Q1 FY27 EoM to gross premium: 47.7% in PD L-22, 48.1% in the KPI spreadsheet.', None),
    ('', None),
    ('Other points', BOLD),
    ('Files labelled "H2 FY27" by Bharti cover April-September 2026; this workbook calls the period H1 FY27.', None),
    ('Product Performance FY24-FY26 tables list only the 8 products on the current 90% list. They covered 46.5% (FY24), 56.5% (FY25) and 53.9% (FY26) of individual NBP, so they do not show the full product mix in those years.', None),
    ('The 90% list is measured against individual NBP: the 8 products were 96.4% of individual NBP in Q1 FY27.', None),
    ('Persistency values that look odd (FY24 policy-basis 49th month 24.4%, FY21 policy-basis 13th month 39.0%) were checked by the user against the PD and are as printed.', None),
    ('FY23 PD also prints persistency under the 2014 circular (13th month 71.2%). The trend uses the main L-22 table (2021 circular, 69.4%).', None),
    ('VNB, VNB margin and embedded value are not disclosed. The FY26 PD index lists L-44 Embedded Value as "Not applicable"; none of the annual reports FY21-FY26 mentions VNB or EV.', None),
    ('Peer segment premium comes from deliverable 01 (Data tab), which uses the same L-1-A-RA line for every insurer. Group business sits inside each segment there, so "Non-Par Life" includes non-par group.', None),
]
for i, (t, f) in enumerate(notes, 1):
    c = ws.cell(i, 1, t)
    if f:
        c.font = f
ws.column_dimensions['A'].width = 160

# ------------------------------------------------------------------ Bharti trend
s = Sheet(wb.create_sheet('Bharti trend'))
s.title('Bharti Life: premium trend FY21 to FY26, with Q1 FY26 and Q1 FY27',
        'Rs crore unless stated. Source columns are in bharti_trend_data.csv.')
SEGS = ['Par life', 'Par pension', 'Non-par individual life', 'Non-par individual pension', 'Non-par individual health',
        'Non-par group', 'Linked life', 'Linked pension', 'Linked group', 'Total']
s.table('A. Gross premium by PD segment (Rs crore)', ['Segment'] + YQ,
        [[x] + series('Gross premium', x, YQ, 'Rs lakh', 'Rs lakh') for x in SEGS], '#,##0.00',
        'PD L-1-A-RA (a) Premium. FY21 from the FY22 PD prior-year column.')
ROLL = ['Par', 'Non-par individual life', 'Non-par individual pension and annuity', 'Health', 'Non-par group',
        'Linked (life, pension, group)']
s.table('B. Gross premium by category (Rs crore)', ['Category'] + YQ,
        [[x] + series('Gross premium (roll-up)', x, YQ, 'Rs lakh', 'Rs lakh') for x in ROLL] +
        [['Total'] + series('Gross premium', 'Total', YQ, 'Rs lakh', 'Rs lakh')], '#,##0.00',
        'Sums of the PD segments in table A. Par = par life + par pension. Linked = linked life + pension + group. PDs do not separate annuity from pension.')
s.table('C. Gross premium mix (% of total)', ['Category'] + YQ,
        [[x] + series('Share of gross premium', x, YQ, '%') for x in ROLL], '0.0',
        'Table B / total.')
s.table('D. Gross premium growth, year on year (%)', ['Category'] + YEARS[1:],
        [[x] + series('Gross premium growth (roll-up)', x, YEARS[1:], '%') for x in ROLL] +
        [['Total'] + series('Gross premium growth', 'Total', YEARS[1:], '%')], '0.0', 'From table B.')
s.table('E. Individual vs group gross premium (Rs crore)', ['Line'] + YQ,
        [['Individual'] + series('Gross premium, individual', 'Individual', YQ, 'Rs lakh', 'Rs lakh'),
         ['Group (non-par group + linked group)'] + series('Gross premium, group (non-par group + linked group)', 'Group', YQ, 'Rs lakh', 'Rs lakh')],
        '#,##0.00', 'PD L-1-A-RA.')
s.table('F. First year, renewal and single premium (Rs crore)', ['Line'] + YQ,
        [[m] + series(m, 'Total', YQ, 'Rs lakh', 'Rs lakh') for m in ('First year premium', 'Renewal premium', 'Single premium', 'Gross premium')],
        '#,##0.00', 'PD L-4 premium schedule.')
nbp_rows = []
for x in SEGS:
    nbp_rows.append([x] + [cr(get('New business premium (first year + single)', x, p), 'Rs lakh') for p in YEARS])
s.table('G. New business premium by PD segment, first year + single (Rs crore)', ['Segment'] + YEARS, nbp_rows, '#,##0.00',
        'FY21, FY22, FY24: annual-report Schedule 1. FY23: reconstructed (yellow). FY25, FY26: derived from L-22 growth (yellow). Total: PD L-4.',
        flags={(x, 'FY23') for x in SEGS[:-1]} | {(x, 'FY25') for x in SEGS[:-1]} | {(x, 'FY26') for x in SEGS[:-1]})
s.table('H. NBP mix by category (% of total NBP)', ['Category'] + YEARS,
        [[x] + series('NBP share (roll-up)', x, YEARS, '%') for x in ROLL], '0.0', 'From table G.',
        flags={(x, p) for x in ROLL for p in ('FY23', 'FY25', 'FY26')})
s.table('I. NBP growth by segment, as disclosed (%)', ['Segment'] + YQ,
        [[x] + series('NBP growth', x, YQ, '%') for x in ['Par life', 'Non-par individual life', 'Non-par individual pension',
                                                         'Non-par group', 'Linked life', 'Linked group']], '0.0',
        'PD L-22 row 1. Blank = NA in the PD.')
ind = series('Individual new business premium by channel', 'Total', YEARS + ['Q1 FY27'], 'Rs lakh', 'Rs lakh')
grp = series('Group new business premium by channel', 'Total', YEARS + ['Q1 FY27'], 'Rs lakh', 'Rs lakh')
s.table('J. Individual vs group NBP', ['Line'] + YEARS + ['Q1 FY27'],
        [['Individual NBP (Rs crore)'] + ind, ['Group NBP (Rs crore)'] + grp,
         ['Individual share of NBP (%)'] + series('Individual share of NBP', 'Individual', YEARS + ['Q1 FY27'], '%')],
        '#,##0.00', 'PD L-38 and L-37 totals.')
s.table('K. Single vs regular premium, individual NBP (%)', ['Line'] + YQ,
        [['Single premium share'] + series('Single premium share of individual NBP', 'Individual', YQ, '%'),
         ['Regular premium share'] + series('Regular premium share of individual NBP', 'Individual', YQ, '%'),
         ['Linked share of individual NBP'] + series('Linked share of individual NBP', 'Individual', YQ, '%')],
        '0.0', 'PD L-22 rows 2 and 3.')
s.widths(52, 12, 10)
s.ws.freeze_panes = 'B3'

# ------------------------------------------------------------------ Bharti KPIs
k = Sheet(wb.create_sheet('Bharti KPIs'))
k.title('Bharti Life: KPIs FY21 to FY26, with Q1 FY27', 'Source columns are in bharti_trend_data.csv.')
P7 = YEARS + ['Q1 FY27']
MON = ['13th month', '25th month', '37th month', '49th month', '61st month']
for lab in ('Persistency, premium basis, regular/limited pay', 'Persistency, policy basis, regular/limited pay',
            'Persistency, premium basis, single/fully paid-up'):
    k.table(lab + ' (%)', ['Month'] + P7, [[m] + series(lab, m, P7, '%') for m in MON], '0.0',
            'PD L-22 row 19, year-to-date column. Q1 FY27 is a rolling 12-month cohort. FY21 single-premium: NA in the PD.')
CS = ['Par life', 'Par pension', 'Non-par individual life', 'Non-par individual pension', 'Non-par individual health',
      'Linked life', 'Linked pension']
k.table('Conservation ratio by segment (%)', ['Segment'] + P7, [[x] + series('Conservation ratio', x, P7, '%') for x in CS], '0.0',
        'PD L-22 row 5. Blank = NA in the PD.')
k.table('Expense and commission ratios (%)', ['Ratio'] + P7,
        [['Expenses of management to gross direct premium'] + series('Expenses of management to gross direct premium', 'Total', P7, '%'),
         ['Commission ratio (gross commission / gross premium)'] + series('Commission ratio', 'Total', P7, '%')],
        '0.0', 'PD L-22 rows 6 and 7.')
EY = ['FY21', 'FY22', 'FY23', 'FY24', 'FY25']


def eom(metric):
    out = []
    for p in EY:
        v = get(metric, 'Total', p)
        u = [r['unit'] for r in R if r['metric'] == metric and r['period'] == p][0]
        out.append(cr(v, u))
    return out


k.table('Expenses of management against the regulatory limit (Rs crore)', ['Line'] + EY + ['FY26'],
        [['Allowable (limit)'] + eom('EoM allowable (regulatory limit)') + [None],
         ['Actual'] + eom('EoM actual') + [None],
         ['Excess charged to shareholders'] + eom('EoM excess charged to shareholders') + [0],
         ['Actual as % of allowable'] + series('EoM actual as % of allowable', 'Total', EY, '%') + [None],
         ['Forbearance'] + ['Applied; granted', 'Applied; granted 7 Dec 2022', 'Applied 31 Mar 2023; granted',
                            'Applied 22 Mar 2024; granted', 'Applied 27 Mar 2025; pending. Show-cause notice 15 Jan 2026',
                            'Within limit']],
        '#,##0.00',
        'Annual-report notes to accounts: FY21 report p130, FY22 p79, FY23 p120, FY24 p106, FY25 p86-87, FY26 p100-101. FY23, FY25, FY26 pages are scanned (OCR-read, user-checked). FY25 report p87: EoM ratio 101% at company level, 99% for individual participating.')
dc = 'Death claim settlement ratio (paid / (outstanding at start + intimated))'
k.table('Claims (%)', ['Line'] + P7,
        [['Individual death claim settlement ratio, by count'] + series(dc, 'Individual', P7, '%'),
         ['Group death claim settlement ratio, by count'] + series(dc, 'Group', P7, '%'),
         ['Claim settlement ratio stated in the annual report'] + series('Claim settlement ratio as stated by the company', 'Individual death', P7, '%')],
        '0.00', 'PD L-40 death-claim counts (FY22 onwards). The company\'s stated ratio uses the same basis (annual reports). FY21 from the FY21 annual report p10.')
k.table('Solvency, AUM and ticket size', ['Line'] + P7,
        [['Solvency ratio (%)'] + series('Solvency ratio', 'Total', P7, '%'),
         ['AUM, investments L-12 + L-13 + L-14 (Rs crore)'] + series('AUM (investments L-12 + L-13 + L-14)', 'Total', P7, 'Rs lakh', 'Rs lakh'),
         ['AUM growth (%)'] + [None] + series('AUM growth', 'Total', YEARS[1:], '%') + [None],
         ['Average ticket size, individual non-single (Rs)'] + series('Average ticket size, individual non-single premium', 'Individual', P7, 'Rs')],
        '#,##0.0', 'PD L-22 rows 21 and 25; PD L-3-A-BS.')
CH = ['Individual agents', 'Corporate agents, banks', 'Corporate agents, others', 'Brokers', 'Direct', 'IMF',
      'Web aggregators', 'Point of sales']
k.table('Channel mix, individual NBP (% of individual NBP)', ['Channel'] + P7,
        [[c] + series('Channel share of individual NBP', c, P7, '%') for c in CH], '0.0',
        'PD L-38. Bancassurance = corporate agents, banks. Online sales sit inside Direct (shown below). Negative values are cancellations printed by Bharti.')
k.table('Channel NBP, individual (Rs crore)', ['Channel'] + P7,
        [[c] + series('Individual new business premium by channel', c, P7, 'Rs lakh', 'Rs lakh') for c in CH + ['Direct, online', 'Total']],
        '#,##0.00', 'PD L-38.')
k.table('Number of new policies, individual', ['Channel'] + P7,
        [[c] + series('Individual new policies by channel', c, P7, 'count') for c in CH + ['Total']], '#,##0',
        'PD L-38.')
GCH = ['Corporate agents, banks', 'Corporate agents, others', 'Brokers', 'Direct', 'IMF', 'Total']
k.table('Group NBP by channel (Rs crore)', ['Channel'] + P7,
        [[c] + series('Group new business premium by channel', c, P7, 'Rs lakh', 'Rs lakh') for c in GCH] +
        [['Group lives covered (count)'] + series('Group lives covered', 'Total', P7, 'count')],
        '#,##0.00', 'PD L-37.')
KP = ['FY24', 'FY25', 'FY26', 'Q1 FY27', 'H1 FY27']
k.table('KPI disclosures spreadsheet (%)', ['Ratio'] + KP,
        [[m] + series(m, 'Total', KP, '%') for m in ('AUM to total premium ratio', 'Renewal premium to new business premium ratio',
                                                     'Policies issued to policies exited ratio',
                                                     'Expenses of management to gross premium (KPI sheet)')],
        '0.0', 'kpi-disclosures, sheet financial-soundness. Published only for FY24 onwards.')
k.table('VNB, VNB margin, embedded value', ['Line', 'Status'],
        [['VNB / VNB margin / EV', 'Not disclosed. FY26 PD index: "L-44 Embedded Value: Not applicable". Not mentioned in annual reports FY21-FY26.']])
k.widths(52, 12, 10)
k.ws.freeze_panes = 'B3'

# ------------------------------------------------------------------ Bharti product trend
pt = Sheet(wb.create_sheet('Bharti product trend'))
pt.title('Bharti Life: products making up 90% of individual NBP',
         'Source: Bharti KPI disclosures, Product Performance files (FY24 to H1 FY27) and monthly 90% lists (Jun to Sep 2026).')
PRODS = ['Guaranteed Wealth Pro', 'Growth Shield Plus', 'Unnati', 'Wealth Pro', 'Swabhimaan Retirement Plan',
         'Insta Gain Plan', 'Guaranteed Bachat Plan', 'Dream Shield Plus']
CAT = {'Guaranteed Wealth Pro': ('130N107', 'Non-Par Savings'), 'Growth Shield Plus': ('130L123V01', 'ULIP'),
       'Unnati': ('130N106V02', 'Par'), 'Wealth Pro': ('130L100V03', 'ULIP'),
       'Swabhimaan Retirement Plan': ('130N109', 'Annuity'), 'Insta Gain Plan': ('130N145', 'Non-Par Savings'),
       'Guaranteed Bachat Plan': ('130N144V01', 'Non-Par Savings'), 'Dream Shield Plus': ('130L125V01', 'ULIP')}
PP = ['FY24', 'FY25', 'FY26', 'Q1 FY27', 'YTD Jul FY27', 'YTD Aug FY27', 'H1 FY27']
FIELDS = [('New business premium', 'NBP (Rs crore)', '#,##0.00'), ('New policies', 'New policies', '#,##0'),
          ('Renewal premium', 'Renewal premium (Rs crore)', '#,##0.00'), ('Renewal proportion', 'Renewal proportion (%)', '0'),
          ('Exit proportion', 'Exit proportion (%)', '0')]
for f, lab, fmt in FIELDS:
    rows = []
    for p in PRODS:
        rows.append([p, CAT[p][1]] + series(f, 'Bharti AXA Life ' + p, PP))
    pt.table(lab, ['Product', 'Category'] + PP, rows, fmt,
             'Product Performance tables. 0 or blank = "-" in the file (no business that year).')
rows = []
for p in PRODS:
    rows.append([p, CAT[p][1]] + series('Share of FY27 year-to-date NBP (90% list)', 'Bharti AXA Life ' + p,
                                        ['Jun 2026', 'Jul 2026', 'Aug 2026', 'Sep 2026']))
rows.append(['Total of listed products', ''] + series('Share of FY27 year-to-date NBP (90% list)', 'Total of listed products',
                                                       ['Jun 2026', 'Jul 2026', 'Aug 2026', 'Sep 2026']))
pt.table('Share of FY27 NBP on the monthly 90% list (%)', ['Product', 'Category', 'Jun 2026', 'Jul 2026', 'Aug 2026', 'Sep 2026'], rows, '0',
         'Monthly Product Performance and Improvement Reports, page 2.')
cov = [['Listed products NBP (Rs crore)'] + series('NBP of products on the current 90% list', 'Total of listed products', ['FY24', 'FY25', 'FY26', 'Q1 FY27']),
       ['Share of individual NBP (L-38) (%)'] + series('Listed products as share of individual NBP', 'Total of listed products', ['FY24', 'FY25', 'FY26', 'Q1 FY27'])]
pt.table('How much of individual NBP the listed products cover', ['Line', 'FY24', 'FY25', 'FY26', 'Q1 FY27'], cov, '#,##0.0',
         'Product Performance and PD L-38. The FY24-FY26 tables show only today\'s 8 products, so earlier products that have since left the list are missing.')
pt.table('Launches, list changes and UIN versions', ['Product', 'First year with sales in the file', 'Notes'],
         [['Guaranteed Wealth Pro', 'FY24 or earlier', 'UIN 130N107V12 to Aug 2026, V13 in Sep 2026'],
          ['Wealth Pro', 'FY24 or earlier', ''],
          ['Unnati', 'FY24 or earlier', ''],
          ['Swabhimaan Retirement Plan', 'FY24 or earlier', 'UIN 130N109V03 to Aug 2026, V04 in Sep 2026'],
          ['Growth Shield Plus', 'FY25', 'No opening policies in FY25'],
          ['Dream Shield Plus', 'FY26', 'No opening policies in FY26'],
          ['Guaranteed Bachat Plan', 'FY26', 'No opening policies in FY26'],
          ['Insta Gain Plan', 'FY26', 'UIN 130N145V02 to Aug 2026, V03 in Sep 2026'],
          ['List changes Jun-Sep 2026', '', 'The same 8 products are on the list in all four months. Earlier lists are not in the files.']])
pt.widths(30, 13, 10)
pt.ws.column_dimensions['B'].width = 16
pt.ws.column_dimensions['C'].width = 16

# ------------------------------------------------------------------ Peer view
pv = Sheet(wb.create_sheet('Peer view FY26'))
pv.title('Peer view FY26: Bharti against 13 peers',
         'Same PD forms for every insurer: L-1-A-RA (segment premium, via deliverable 01), L-22 (persistency, conservation). Year-to-date FY26 columns.')
PEERS = ['SBI Life', 'HDFC Life', 'ICICI Prudential Life', 'Axis Max Life', 'Tata AIA Life', 'Bajaj Life', 'Aditya Birla Sun Life',
         'Canara HSBC Life', 'Ageas Federal Life', 'Shriram Life', 'Generali Central Life', 'Pramerica Life', 'IndusInd Nippon Life',
         'Bharti Life']


rows = []
for n in PEERS:
    t26 = get('Peer: gross premium by segment', f'{n} | FY26 Grand Total (L-1)', 'FY26')
    sh = [get('Peer: share of gross premium', f'{n} | {c}', 'FY26') for c in
          ('Par', 'Non-par life', 'Non-par pension and annuity', 'Linked', 'Health and variable')]
    gr = [get('Peer: gross premium growth', f'{n} | {c}', 'FY26') for c in ('Total', 'Par', 'Non-par life', 'Linked')]
    rows.append([n, t26, gr[0]] + sh + gr[1:])
pv.table('Segment mix and growth', ['Insurer', 'Gross premium FY26 (Rs crore)', 'Total growth FY26 (%)', 'Par (% of total)',
                                    'Non-par life (% of total)', 'Non-par pension and annuity (% of total)', 'Linked (% of total)',
                                    'Health and variable (% of total)', 'Par growth (%)', 'Non-par life growth (%)', 'Linked growth (%)'],
         rows, '#,##0.0', 'L-1-A-RA (a) Premium, FY26 and FY25 columns of each FY26 PD, via deliverable 01 Data tab. Non-par life includes group.',
         flags={('Bharti Life', '*')})
rows = []
for n in PEERS:
    rows.append([n] + [get('Peer: persistency, premium basis, regular/limited pay', f'{n} | {m}', 'FY26') for m in MON])
pv.table('Persistency, premium basis, regular/limited pay (%)', ['Insurer'] + MON, rows, '0.0',
         'L-22 row 19, year-to-date FY26. Axis Max prints whole percentages.', flags={('Bharti Life', '*')})
rows = []
for n in PEERS:
    rows.append([n] + [get('Peer: conservation ratio', f'{n} | {x}', 'FY26') for x in ('Linked life', 'Par life', 'Non-par life')])
pv.table('Conservation ratio (%)', ['Insurer', 'Linked life', 'Par life', 'Non-par life'], rows, '0.0',
         'L-22 row 5, year-to-date FY26. Generali Central and IndusInd Nippon print whole percentages for some segments.',
         flags={('Bharti Life', '*')})
pv.ws.cell(pv.row, 1, 'Missing peers: none. All 13 peer FY26 PDs are in Desktop/LI-PDs (see Sources).')
pv.widths(26, 14, 12)

# ------------------------------------------------------------------ Sources
so = wb.create_sheet('Sources')
for i, r in enumerate(INV, 1):
    for j, v in enumerate(r, 1):
        c = so.cell(i, j, int(v) if (j == 5 and v.isdigit()) else v)
        if i == 1:
            c.font = BOLD
            c.fill = HFILL
for j, w in enumerate([48, 26, 16, 40, 9, 6, 40, 120], 1):
    so.column_dimensions[get_column_letter(j)].width = w
so.freeze_panes = 'A2'

out = os.path.join(BASE, 'bharti_analysis.xlsx')
wb.save(out)
print('saved', out)
