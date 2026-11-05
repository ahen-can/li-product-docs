"""Build analysis/bharti/bharti_trend_data.csv.

Every value below was transcribed from the source document and page named next to it.
Source PDFs are in the user's folder ~/Desktop/for-liprodanal-agent (not committed).
Derived rows (mixes, growth, derived segment NBP) are computed here and say so in the note.

Run: python3 analysis/bharti/scripts/build_trend_data.py
"""
import csv
import os

OUT = os.path.join(os.path.dirname(__file__), '..', 'bharti_trend_data.csv')

P22 = 'fy22-pd.pdf'
P23 = 'fy23-pd.pdf'
P24 = 'FY24-pd.pdf'
P25 = 'fy25-pd.pdf'
P26 = 'fy2025 - L1-to-L45-consolidated-q4.pdf'
PQ1 = 'q1-fy27-pd.pdf'
AR = {y: f'fy{y}-annual-report.pdf' for y in (22, 23, 24, 25, 26)}
AR[21] = 'fy21-annual-report'
KPI = 'kpi-disclosures'
PP = {'Q1 FY27': 'Product Performance FY24 - Q1FY27.pdf',
      'YTD Jul FY27': 'Product Performance FY24 - YTD Jul FY 27.pdf',
      'YTD Aug FY27': 'Product Performance FY24 - YTD Aug FY 27.pdf',
      'H1 FY27': 'Product Performance FY24 - H2 FY 27.pdf'}
MR = {'Jun 2026': 'Features.pdf',
      'Jul 2026': 'Monthly Product Performance and Improvement Report - YTD July FY27.pdf',
      'Aug 2026': 'Monthly Product Performance and Improvement Report - YTD Aug FY27.pdf',
      'Sep 2026': 'Monthly Product Performance and Improvement Report - H2 FY27.pdf'}
OCR = 'OCR-read (scanned page); checked against the page image'

H = ['metric', 'segment_or_product', 'period', 'value', 'unit', 'source_file',
     'form_or_section', 'page', 'note']
rows = []


def add(metric, seg, period, value, unit, src, form, page, note=''):
    rows.append([metric, seg, period, value, unit, src, form, page, note])


YEARS = ['FY21', 'FY22', 'FY23', 'FY24', 'FY25', 'FY26']
SEGS = ['Par life', 'Par pension', 'Non-par individual life', 'Non-par individual pension',
        'Non-par individual health', 'Non-par group', 'Linked life', 'Linked pension',
        'Linked group', 'Total']

# ---------------------------------------------------------------- L-1-A-RA premium by segment
# (a) Premium, year to date, Rs lakh. Columns in SEGS order.
L1 = {
    'FY21': (P22, 4, [87128, 22, 101720, 0, 464, 12912, 24882, 222, 733, 228082],
             'FY22 PD prior-year column. No non-par individual pension column that year (shown as 0).'),
    'FY22': (P22, 2, [84847, 9, 130430, 0, 424, 17166, 26600, 171, 508, 260156],
             'No non-par individual pension column that year (shown as 0).'),
    'FY23': (P23, 3, [79944, 7, 160766, 1597, 400, 21108, 27623, 150, 464, 292058], ''),
    'FY24': (P24, 3, [73257, 7, 170925, 1784, 381, 14151, 30191, 128, 5, 290830],
             'FY25 PD restates FY24 non-par group as 14,152 (fy25-pd.pdf p4).'),
    'FY25': (P25, 2, [69528, 7, 177738, 3431, 367, 8959, 37849, 110, 6, 297995],
             'Same values in FY26 PD prior-year column (p4).'),
    'FY26': (P26, 2, [60611, 7, 188990, 6290, 354, 13132, 56170, 88, 6, 325648], ''),
    'Q1 FY27': (PQ1, 3, [10195, 2, 26717, 1267, 54, 7257, 9438, 17, 2, 54949], 'Quarter Apr-Jun 2026.'),
    'Q1 FY26': (PQ1, 4, [11965, 3, 28186, 289, 57, 3551, 8871, 22, 3, 52947], 'Quarter Apr-Jun 2025, comparative.'),
}
for per, (src, pg, vals, note) in L1.items():
    for s, v in zip(SEGS, vals):
        add('Gross premium', s, per, v, 'Rs lakh', src, 'L-1-A-RA (a) Premium', pg, note)
add('Gross premium', 'Non-par group', 'FY24', 14152, 'Rs lakh', P25, 'L-1-A-RA (a) Premium', 4,
    'Restated comparative; FY24 PD shows 14,151. Difference of 1 lakh, rounding.')

# ---------------------------------------------------------------- L-4 premium schedule
L4 = {'FY21': (P22, 8, 55951, 149798, 22333, 228082), 'FY22': (P22, 8, 70682, 166632, 22841, 260156),
      'FY23': (P23, 9, 76239, 190429, 25390, 292058), 'FY24': (P24, 9, 62305, 212757, 15768, 290830),
      'FY25': (P25, 8, 61185, 223829, 12981, 297995), 'FY26': (P26, 8, 90487, 218788, 16373, 325648),
      'Q1 FY27': (PQ1, 7, 15793, 35913, 3243, 54949), 'Q1 FY26': (PQ1, 7, 11233, 37131, 4583, 52947)}
for per, (src, pg, fy, ren, sp, tot) in L4.items():
    for m, v in (('First year premium', fy), ('Renewal premium', ren), ('Single premium', sp), ('Gross premium', tot)):
        add(m, 'Total', per, v, 'Rs lakh', src, 'L-4 Premium schedule', pg)

# ---------------------------------------------------------------- Annual report Schedule 1, by segment
# Rs '000. Columns in SEGS order without Total; then printed total.
S1 = {
    'FY21': (AR[21], 94, {'First year premium': [888660, -381, 4113895, 0, -23, 0, 593035, -72, 0, 5595114],
                          'Renewal premium': [7824182, 2626, 6054777, 0, 46379, 0, 1029851, 21951, 0, 14979766],
                          'Single premium': [0, 0, 3298, 0, 0, 1291167, 865298, 273, 73300, 2233336]},
             'Schedule 1 of the audited segmental revenue account. Same figures as FY22 annual report p65.'),
    'FY22': (AR[22], 60, {'First year premium': [1102051, 0, 5231048, 0, 0, 0, 735090, 12, 0, 7068201],
                          'Renewal premium': [7382669, 881, 7798436, 0, 42392, 0, 1421934, 16909, 0, 16663221],
                          'Single premium': [0, 0, 13547, 0, 0, 1716553, 503018, 200, 50823, 2284141]},
             'Schedule 1. Two printed pages per PDF page (printed page 116).'),
    'FY23': (AR[24], 124, {'First year premium': [938384, 0, 5868295, 143286, 0, 10547, 663437, -13, 0, 7623936],
                           'Renewal premium': [7056023, 696, 10160914, 0, 39992, 10992, 1759416, 14868, 0, 19042901],
                           'Single premium': [0, 0, 47346, 16385, 0, 2089216, 339459, 146, 46400, 2538952]},
             'RECONSTRUCTED. FY23 comparative in the FY24 annual report prints some cells one column off '
             '(e.g. linked life total shows 3,60,998). Cells reassigned so that every segment total matches '
             'FY23 PD L-1-A-RA and every row total matches L-4. The FY23 annual report has no segment-wise '
             'Schedule 1. See for-your-attention/please_check.md.'),
    'FY24': (AR[24], 117, {'First year premium': [639089, 0, 4550632, 54965, 0, 3005, 982792, 0, 0, 6230483],
                           'Renewal premium': [6686644, 695, 12544647, 114600, 38117, 2495, 1875740, 12773, 0, 21275711],
                           'Single premium': [0, 0, -2757, 8855, 0, 1409644, 160536, 5, 549, 1576832]},
             'Schedule 1. Text layer has OCR-style digit errors (dots for commas); values checked against the '
             'page image and the row and segment totals.'),
}
for per, (src, pg, d, note) in S1.items():
    for m, vals in d.items():
        for s, v in zip(SEGS, vals):
            add(m, s, per, v, "Rs '000", src, 'Annual report Schedule 1 Premium (segmental)', pg, note)

# ---------------------------------------------------------------- L-22 analytical ratios (year to date)
# page for rows 1-17 and page for rows 18-25
L22P = {'FY21': (P22, 29, 30, 'FY22 PD prior-year column'), 'FY22': (P22, 29, 30, ''),
        'FY23': (P23, 30, 31, ''), 'FY24': (P24, 30, 31, ''), 'FY25': (P25, 29, 30, ''),
        'FY26': (P26, 29, 30, ''), 'Q1 FY27': (PQ1, 28, 29, 'Quarter Apr-Jun 2026'),
        'Q1 FY26': (PQ1, 28, 29, 'Quarter Apr-Jun 2025, comparative')}
NBPG = {  # NBP growth, %; None = NA
    'Linked life': [49.9, -15.1, -19.0, 14.0, 42.6, 89.6, 2.7, 138.2],
    'Linked group': [193.2, -30.7, -8.7, -98.8, 9.0, 0.0, 0.0, 0.0],
    'Par life': [-22.9, 24.0, -14.9, -31.9, 34.6, -24.7, -13.4, 38.2],
    'Non-par individual life': [-2.4, 27.4, 12.8, -23.1, -15.81, 37.2, -22.3, -30.2],
    'Non-par individual pension': [None, None, None, -60.0, 215.6, 89.7, 352.7, 190.4],
    'Non-par individual health': [-114.5, None, None, None, None, None, None, None],
    'Non-par group': [-32.6, 32.9, 22.3, -32.7, -36.6, 46.6, 104.4, 212.9],
}
PERS = list(L22P.keys())
for seg, vals in NBPG.items():
    for per, v in zip(PERS, vals):
        if v is None:
            continue
        src, p1, p2, n = L22P[per]
        add('NBP growth', seg, per, v, '%', src, 'L-22 row 1 New business premium income growth', p1, n)
SINGLE = [13.4, 6.8, 5.0, 2.6, 6.2, 10.9, 7.5, 24.8]
LINKED = [22.6, 16.3, 12.5, 17.9, 25.0, 33.0, 41.7, 39.0]
EOM = [37.7, 40.0, 38.3, 33.7, 31.4, 34.2, 47.7, 38.4]
COMM = [6.9, 6.5, 6.4, 9.6, 9.0, 8.0, 9.0, 6.0]
SOLV = [178.0, 161.6, 163.0, 162.0, 167.0, 191.0, 192.0, 241.0]
TICKET = [51350, 60625, 72787, 70460, 87160, 120865, 104022, 89809]
for per, a, b, c, d, e, f in zip(PERS, SINGLE, LINKED, EOM, COMM, SOLV, TICKET):
    src, p1, p2, n = L22P[per]
    add('Single premium share of individual NBP', 'Individual', per, a, '%', src, 'L-22 row 2', p1, n)
    add('Linked share of individual NBP', 'Individual', per, b, '%', src, 'L-22 row 3', p1, n)
    add('Expenses of management to gross direct premium', 'Total', per, c, '%', src, 'L-22 row 6', p1,
        (n + '; ' if n else '') + 'Gross EoM before transfer to shareholders. Not the same measure as the regulatory limit test.')
    add('Commission ratio', 'Total', per, d, '%', src, 'L-22 row 7', p1, n)
    add('Solvency ratio', 'Total', per, e, '%', src, 'L-22 row 21', p2, n)
    add('Average ticket size, individual non-single premium', 'Individual', per, f, 'Rs', src, 'L-22 row 25', p2, n)
CONS = {
    'Linked life': [84.4, 87.6, 81.6, 77.4, 75.4, 74.4, 75.7, 77.8],
    'Linked pension': [55.1, 77.0, 87.9, 86.0, 85.9, 80.3, 78.9, 84.6],
    'Par life': [84.7, 84.7, 83.2, 83.6, 83.2, 77.9, 73.2, 81.4],
    'Par pension': [73.6, 33.5, 79.0, 99.9, 104.0, 92.4, 60.0, 88.9],
    'Non-par individual life': [67.9, 76.7, 78.0, 78.3, 81.6, 76.8, 79.6, 77.6],
    'Non-par individual pension': [None, None, None, 80.0, 83.6, 74.6, 88.9, 38.4],
    'Non-par individual health': [90.6, 91.4, 94.3, 95.3, 96.3, 96.7, 95.0, 98.3],
}
for seg, vals in CONS.items():
    for per, v in zip(PERS, vals):
        if v is None:
            continue
        src, p1, p2, n = L22P[per]
        nn = n
        if seg == 'Par pension' and per == 'FY25':
            nn = 'FY25 PD shows 104%; FY26 PD prior-year column shows 104.5%.'
        add('Conservation ratio', seg, per, v, '%', src, 'L-22 row 5', p1, nn)
# Persistency, regular/limited pay, individual. 13,25,37,49,61 months.
PR = {  # premium basis, policy basis, single-premium premium basis, single-premium policy basis
    'FY21': ([62.5, 52.6, 49.8, 46.1, 41.4], [39.0, 44.3, 42.9, 39.8, 37.5], None, None),
    'FY22': ([67.4, 50.7, 45.8, 46.7, 43.2], [59.6, 31.1, 37.9, 39.6, 36.7],
             [99.6, 100.0, 99.8, 100.0, 73.3], [99.9, 100.0, 100.0, 100.0, 86.8]),
    'FY23': ([69.4, 53.2, 44.3, 43.5, 43.0], [64.0, 46.8, 26.8, 35.4, 37.1],
             [100.0, 99.9, 100.0, 99.9, 87.5], [100.0, 99.9, 100.0, 100.0, 95.0]),
    'FY24': ([73.0, 54.6, 46.7, 40.9, 38.0], [66.0, 50.7, 40.7, 24.4, 32.5],
             [94.1, 99.9, 99.8, 99.3, 72.7], [98.7, 99.9, 99.9, 56.8, 89.7]),
    'FY25': ([71.0, 57.0, 49.6, 44.5, 35.5], [67.4, 52.0, 46.2, 38.5, 22.2],
             [98.9, 94.1, 99.9, 100.0, 85.9], [99.9, 98.5, 100.0, 100.0, 94.4]),
    'FY26': ([64.5, 49.0, 51.8, 45.2, 37.9], [60.9, 47.8, 47.5, 42.3, 34.1],
             [100.0, 90.0, 99.6, 99.9, 90.2], [100.0, 98.9, 99.9, 100.0, 92.8]),
    'Q1 FY27': ([67.4, 49.1, 51.6, 45.0, 38.6], [62.7, 47.7, 47.1, 41.9, 35.5],
                [100.0, 100.0, 93.3, 99.9, 88.9], [99.3, 100.0, 97.7, 100.0, 93.2]),
}
MON = ['13th month', '25th month', '37th month', '49th month', '61st month']
for per, sets in PR.items():
    src, p1, p2, n = L22P[per]
    labels = ['Persistency, premium basis, regular/limited pay', 'Persistency, policy basis, regular/limited pay',
              'Persistency, premium basis, single/fully paid-up', 'Persistency, policy basis, single/fully paid-up']
    for lab, vals in zip(labels, sets):
        if vals is None:
            continue
        for mth, v in zip(MON, vals):
            note = n
            if per == 'FY21' and 'single' in lab:
                note = 'FY22 PD shows NA for FY21.'
            if per == 'Q1 FY27':
                note = 'Rolling 12-month cohort (policies issued Jun 2024 to May 2025 for 13th month).'
            add(lab, mth, per, v, '%', src, 'L-22 row 19', p2, note)
for lab, vals in (('Persistency, premium basis, regular/limited pay (2014 circular basis)', [71.2, 52.0, 45.0, 41.7, 38.4]),
                  ('Persistency, policy basis, regular/limited pay (2014 circular basis)', [65.3, 45.9, 27.6, 34.1, 34.6])):
    for mth, v in zip(MON, vals):
        add(lab, mth, 'FY23', v, '%', P23, 'L-22, second table "Persistency reported in Annual Financials FY 23"', 31,
            'Calculated under IRDA/ACT/CIR/MISC/035/01/2014 (cohort Mar-Feb). The main L-22 table uses the 2021 circular. Recorded, not used in the trend.')

# ---------------------------------------------------------------- L-38 individual channels, year to date
CH = ['Individual agents', 'Corporate agents, banks', 'Corporate agents, others', 'Brokers',
      'Direct', 'Direct, online', 'Direct, others', 'IMF', 'Web aggregators', 'Point of sales', 'Total']
L38 = {  # (policies, premium lakh) per channel in CH order; None = not reported/blank
    'FY21': (P22, 58, [(53027, 28962), (8849, 3801), (17429, 10790), (12991, 9875), (23749, 11084),
                       (4375, 3333), (19374, 7751), (0, 0), (307, 106), (479, 68), (116831, 64686)]),
    'FY22': (P22, 58, [(50619, 32688), (10843, 5368), (16772, 15115), (17587, 12607), (25960, 9998),
                       (9927, 3359), (16033, 6639), (0, 0), (34, 14), (68, 8), (121883, 75797)]),
    'FY23': (P23, 59, [(47470, 36624), (11891, 6705), (11328, 14041), (16169, 13059), (17230, 9471),
                       (9591, 2645), (7639, 6827), (0, 0), (-3, 1), (1122, 329), (105207, 80230)]),
    'FY24': (P24, 59, [(33404, 21824), (11600, 6465), (10539, 7757), (17703, 14200), (15654, 13656),
                       (183, 267), (15471, 13390), (0, 0), (0, 0), (170, 61), (89070, 63963)]),
    'FY25': (P25, 58, [(19760, 14976), (10263, 7442), (5114, 6446), (12921, 10886), (20296, 22356),
                       (-223, -92), (20519, 22448), (3099, 3104), (0, 0), (60, 1), (71513, 65210)]),
    'FY26': (P26, 58, [(13356, 12949), (11313, 9463), (4828, 16722), (5717, 13041), (34018, 41747),
                       (-83, -46), (34101, 41793), (-108, -201), (0, 0), (-1, -1), (69123, 93721)]),
    'Q1 FY27': (PQ1, 54, [(2737, 1703), (360, 635), (1260, 1202), (1753, 1952), (6197, 6219),
                          (-13, -24), (6210, 6244), (44, 55), (0, 0), (0, 0), (12351, 11766)]),
}
for per, (src, pg, vals) in L38.items():
    for ch, (pol, prem) in zip(CH, vals):
        add('Individual new business premium by channel', ch, per, prem, 'Rs lakh', src, 'L-38 Business acquisition, individuals', pg)
        add('Individual new policies by channel', ch, per, pol, 'count', src, 'L-38 Business acquisition, individuals', pg)
GCH = ['Corporate agents, banks', 'Corporate agents, others', 'Brokers', 'Direct', 'IMF', 'Total']
L37 = {  # (policies, lives, premium lakh)
    'FY21': (P22, 57, [(4, 47881, 883), (0, 247, 91), (1, 390, 13), (17, 1875360, 12658), (0, 0, 0), (22, 1923878, 13645)]),
    'FY22': (P22, 57, [(8, 250475, 1990), (0, 517, 251), (5, 759, 67), (10, 243264, 15366), (0, 0, 0), (23, 495015, 17674)]),
    'FY23': (P23, 58, [(6, 444918, 4468), (0, 58, 20), (0, 64, 9), (4, 32736, 16964), (0, 0, 0), (10, 477776, 21462)]),
    'FY24': (P24, 58, [(0, 590239, 5984), (0, -266, -42), (0, -1, -1), (0, 14589, 8190), (0, 0, 0), (0, 604561, 14132)]),
    'FY25': (P25, 57, [(5, 301030, 3127), (0, 0, 0), (0, 0, 0), (1, 52372, 5835), (0, 0, 0), (6, 353402, 8961)]),
    'FY26': (P26, 57, [(0, 33950, 557), (2, 10960, 5020), (38, 147620, 3012), (25, 222053, 4517), (4, 1200, 31), (69, 415783, 13138)]),
    'Q1 FY27': (PQ1, 53, [(0, 225, 45), (0, 2836, 1401), (68, 454811, 3847), (0, 118309, 1965), (0, 34, 0.31), (68, 576215, 7259)]),
}
for per, (src, pg, vals) in L37.items():
    for ch, (pol, lives, prem) in zip(GCH, vals):
        add('Group new business premium by channel', ch, per, prem, 'Rs lakh', src, 'L-37 Business acquisition, group', pg)
        if ch == 'Total':
            add('Group new schemes', ch, per, pol, 'count', src, 'L-37 Business acquisition, group', pg)
            add('Group lives covered', ch, per, lives, 'count', src, 'L-37 Business acquisition, group', pg)

# ---------------------------------------------------------------- AUM (L-3 balance sheet investments)
L3 = {'FY21': (P22, 7, 52848, 744497, 140034, 'FY22 PD prior-year column'), 'FY22': (P22, 7, 55375, 875951, 171154, ''),
      'FY23': (P23, 8, 56891, 1059238, 176614, ''), 'FY24': (P24, 8, 75652, 1231533, 224565, ''),
      'FY25': (P25, 7, 51309, 1419858, 232331, ''), 'FY26': (P26, 7, 97123, 1487509, 244082, ''),
      'Q1 FY27': (PQ1, 6, 100328, 1534999, 273036, 'As at 30 Jun 2026')}
for per, (src, pg, sh, ph, ul, n) in L3.items():
    add('Investments, shareholders', 'Total', per, sh, 'Rs lakh', src, 'L-3-A-BS (L-12)', pg, n)
    add('Investments, policyholders', 'Total', per, ph, 'Rs lakh', src, 'L-3-A-BS (L-13)', pg, n)
    add('Assets held to cover linked liabilities', 'Total', per, ul, 'Rs lakh', src, 'L-3-A-BS (L-14)', pg, n)
    add('AUM (investments L-12 + L-13 + L-14)', 'Total', per, sh + ph + ul, 'Rs lakh', src, 'L-3-A-BS', pg,
        'Derived: sum of the three investment lines.')

# ---------------------------------------------------------------- Claims (L-40 death claims, year to date)
L40 = {'FY22': (P22, 62, (0, 3203, 3174, 27), (5, 1802, 1779, 28)),
       'FY23': (P23, 63, (2, 2114, 2097, 19), (0, 2579, 2550, 29)),
       'FY24': (P24, 63, (0, 2016, 1996, 20), (0, 4965, 4914, 51)),
       'FY25': (P25, 62, (0, 2085, 2068, 17), (0, 6257, 6250, 7)),
       'FY26': (P26, 62, (0, 2285, 2267, 18), (0, 4516, 4513, 3)),
       'Q1 FY27': (PQ1, 56, (0, 541, 535, 1), (0, 636, 636, 0))}
for per, (src, pg, ind, grp) in L40.items():
    for seg, (os_, intim, paid, rep) in (('Individual', ind), ('Group', grp)):
        add('Death claims outstanding at start', seg, per, os_, 'count', src, 'L-40 death claims', pg)
        add('Death claims intimated', seg, per, intim, 'count', src, 'L-40 death claims', pg)
        add('Death claims paid', seg, per, paid, 'count', src, 'L-40 death claims', pg)
        add('Death claims repudiated', seg, per, rep, 'count', src, 'L-40 death claims', pg)
        add('Death claim settlement ratio (paid / (outstanding at start + intimated))', seg, per,
            round(100 * paid / (os_ + intim), 2), '%', src, 'L-40 death claims', pg, 'Derived from the counts on this page.')
for per, v, src, pg in (('FY21', 99.05, AR[21], 10), ('FY22', 99.09, AR[23], 12), ('FY23', 99.10, AR[23], 12),
                        ('FY24', 99.01, AR[24], 11), ('FY25', 99.18, AR[25], 5), ('FY26', 99.21, AR[26], 4)):
    add('Claim settlement ratio as stated by the company', 'Individual death', per, v, '%', src,
        'Annual report, directors\' report / highlights', pg,
        ('OCR-read. ' if src in (AR[23], AR[25], AR[26]) else '') +
        'Matches the individual death-claim count ratio from L-40 where both exist.')

# ---------------------------------------------------------------- EoM against the regulatory limit
EOMLIM = [
    ('FY21', AR[21], 130, 6655385, 8590225, 2004007, "Rs '000", 'Notes to accounts, EoM table. Forbearance applied via Life Council letter 23 Mar 2021.'),
    ('FY22', AR[22], 79, 8108882, 10398656, 2314375, "Rs '000", 'Notes to accounts, EoM table. Auditors\' report (p43) says 23,14,373; note says 2,314,375. Applied for forbearance 14 Mar 2022; granted 7 Dec 2022 (FY23 annual report p120).'),
    ('FY23', AR[23], 120, 9099858, 11173281, 2097385, "Rs '000", OCR + '. FY24 annual report (p106) gives the FY23 amount as 20,97,387. Applied for forbearance 31 Mar 2023.'),
    ('FY24', AR[24], 106, 9092489, 9810650, 1003754, "Rs '000", 'Applied for forbearance 22 Mar 2024. FY25 annual report (p87) says forbearance received up to FY24.'),
    ('FY25', AR[25], 86, 92978, 93639, 879, 'Rs lakh', OCR + '. Note on p87: EoM ratio 101% at company level. Forbearance applied 27 Mar 2025, still pending; IRDAI show-cause notice 15 Jan 2026, response filed (FY26 annual report p101, auditors p41).'),
]
for per, src, pg, allow, act, charged, unit, note in EOMLIM:
    add('EoM allowable (regulatory limit)', 'Total', per, allow, unit, src, 'Notes to accounts, EoM limit table', pg, note)
    add('EoM actual', 'Total', per, act, unit, src, 'Notes to accounts, EoM limit table', pg, note)
    add('EoM excess charged to shareholders', 'Total', per, charged, unit, src, 'Notes to accounts, EoM limit table', pg, note)
    add('EoM actual as % of allowable', 'Total', per, round(100 * act / allow, 1), '%', src,
        'Notes to accounts, EoM limit table', pg, 'Derived: actual / allowable.')
add('EoM excess charged to shareholders', 'Total', 'FY26', 0, 'Rs lakh', AR[26], 'Notes to accounts, EoM', 100,
    OCR + '. "Actual expenses incurred for FY 2025-26 are within the allowable limit".')
add('EoM limit plan', 'Total', 'FY24', 'Board-approved 3-year plan submitted 7 Aug 2023 to bring EoM within limits by FY26', 'text',
    AR[25], 'Notes to accounts', 87, OCR)

# ---------------------------------------------------------------- KPI disclosures spreadsheet
KP = ['FY24', 'FY25', 'FY26', 'Q1 FY27', 'H1 FY27']
for m, vals in (('AUM to total premium ratio', [527, 572, 562, 3473, 1446]),
                ('Renewal premium to new business premium ratio', [272, 302, 205, 189, 206]),
                ('Policies issued to policies exited ratio', [107, 96, 86, 130, 148]),
                ('Expenses of management to gross premium (KPI sheet)', [33.7, 31.4, 34.2, 48.1, 41.0])):
    for per, v in zip(KP, vals):
        note = ''
        if m.startswith('Expenses') and per == 'Q1 FY27':
            note = 'Q1 FY27 PD L-22 row 6 gives 47.7%. The two disagree.'
        add(m, 'Total', per, v, '%', KPI, 'sheet financial-soundness', 'sheet', note)
CP = ['FY24', 'FY25', 'FY26', 'Q1 FY27', 'YTD Jul FY27', 'YTD Aug FY27', 'YTD Sep FY27']
for m, vals in (('Claims paid in full (by count)', [98.98, 99.71, 99.69, 99.49, 96.45, 95.87, 99.17]),
                ('Claims repudiated (by count)', [1.02, 0.29, 0.31, 0.08, 0.06, 0.20, 0.31]),
                ('Value proportion of claims settled', [96.80, 98.70, 98.96, 99.76, 99.83, 99.62, 99.57]),
                ('Claims settled within 15 days (by count)', [81.49, 91.98, 89.38, 87.26, 85.96, 85.55, 88.33])):
    for per, v in zip(CP, vals):
        add(m, 'All claims', per, v, '%', KPI, 'sheet claims-responsiveness', 'sheet')

# ---------------------------------------------------------------- Product Performance (90% of individual NBP)
PRODS = {'Unnati': ('130N106V02', 'Par'), 'Wealth Pro': ('130L100V03', 'ULIP'),
         'Growth Shield Plus': ('130L123V01', 'ULIP'), 'Dream Shield Plus': ('130L125V01', 'ULIP'),
         'Guaranteed Bachat Plan': ('130N144V01', 'Non-Par Savings'),
         'Guaranteed Wealth Pro': ('130N107V13', 'Non-Par Savings'),
         'Swabhimaan Retirement Plan': ('130N109V04', 'Annuity'), 'Insta Gain Plan': ('130N145V03', 'Non-Par Savings')}
# opening policies, new policies, NBP cr, renewal cr, total cr, renewal %, exits, exit %
PPD = {
    ('FY24', PP['H1 FY27'], 3): {
        'Unnati': (6833, 3043, 24.25, 53.15, 77.40, 69, 109, 1), 'Wealth Pro': (13864, 7683, 101.89, 80.10, 181.99, 44, 493, 2),
        'Guaranteed Wealth Pro': (41599, 25346, 164.89, 266.44, 431.33, 62, 786, 1),
        'Swabhimaan Retirement Plan': (535, 195, 6.38, 11.46, 17.84, 64, 21, 3)},
    ('FY25', PP['H1 FY27'], 2): {
        'Unnati': (9001, 5882, 57.26, 63.74, 121.00, 53, 561, 4), 'Wealth Pro': (19258, 5354, 79.13, 139.80, 218.93, 64, 252, 1),
        'Growth Shield Plus': (0, 3033, 53.84, 0, 53.84, 0, 69, 2),
        'Guaranteed Wealth Pro': (56454, 22613, 157.86, 348.79, 506.65, 69, 1259, 2),
        'Swabhimaan Retirement Plan': (678, 701, 20.14, 14.17, 34.31, 41, 41, 3)},
    ('FY26', PP['H1 FY27'], 2): {
        'Unnati': (14002, 5448, 43.85, 85.51, 129.36, 66, 1385, 7), 'Wealth Pro': (22700, 3459, 81.55, 160.72, 242.27, 66, 926, 4),
        'Growth Shield Plus': (3026, 4034, 79.58, 37.99, 117.57, 32, 71, 1), 'Dream Shield Plus': (0, 3074, 50.91, 0, 50.91, 0, 41, 1),
        'Guaranteed Bachat Plan': (0, 9689, 46.56, 0, 46.56, 0, 163, 2),
        'Guaranteed Wealth Pro': (71055, 16545, 113.23, 416.60, 529.83, 79, 3242, 4),
        'Swabhimaan Retirement Plan': (1334, 673, 38.21, 24.69, 62.90, 39, 74, 4), 'Insta Gain Plan': (0, 1375, 50.82, 0, 50.82, 0, 19, 1)},
    ('Q1 FY27', PP['Q1 FY27'], 1): {  # file gives Rs; converted to Rs cr (2 dp) here, see note
        'Unnati': (17357, 2018, 13.33, 12.25, 25.58, 48, 663, 3), 'Wealth Pro': (22983, 615, 14.00, 22.80, 36.80, 62, 176, 1),
        'Growth Shield Plus': (6483, 988, 16.57, 10.88, 27.45, 40, 49, 1), 'Dream Shield Plus': (2985, 328, 11.59, 0.42, 12.01, 4, 11, 0),
        'Guaranteed Bachat Plan': (9641, 3142, 15.66, 0, 15.66, 0, 126, 1),
        'Guaranteed Wealth Pro': (79692, 3205, 21.74, 68.50, 90.24, 76, 1538, 2),
        'Swabhimaan Retirement Plan': (1882, 212, 10.91, 1.76, 12.67, 14, 39, 2), 'Insta Gain Plan': (1600, 255, 9.62, 0, 9.62, 0, 18, 1)},
    ('YTD Jul FY27', PP['YTD Jul FY27'], 1): {
        'Guaranteed Wealth Pro': (79692, 4482, 31.67, 95.78, 127.46, 75, 1871, 2), 'Growth Shield Plus': (6483, 1461, 24.04, 17.57, 41.61, 42, 62, 1),
        'Unnati': (17357, 2915, 19.91, 17.15, 37.06, 46, 781, 4), 'Guaranteed Bachat Plan': (9641, 3868, 19.76, 3.08, 22.84, 13, 174, 1),
        'Wealth Pro': (22983, 824, 19.57, 31.13, 50.70, 61, 438, 2), 'Swabhimaan Retirement Plan': (1882, 388, 18.59, 3.72, 22.31, 17, 57, 3),
        'Insta Gain Plan': (1600, 568, 17.11, 0, 17.11, 0, 29, 1), 'Dream Shield Plus': (2985, 487, 16.03, 2.74, 18.77, 15, 13, 0)},
    ('YTD Aug FY27', PP['YTD Aug FY27'], 1): {
        'Guaranteed Wealth Pro': (79692, 5627, 39.54, 126.30, 165.85, 76, 2101, 2), 'Growth Shield Plus': (6483, 1929, 31.66, 22.78, 54.44, 42, 78, 1),
        'Unnati': (17357, 3896, 26.60, 22.71, 49.31, 46, 877, 4), 'Guaranteed Bachat Plan': (9641, 4529, 23.39, 6.30, 29.70, 21, 197, 1),
        'Wealth Pro': (22983, 1037, 24.63, 39.27, 63.90, 61, 1202, 5), 'Swabhimaan Retirement Plan': (1882, 479, 24.62, 7.29, 31.91, 23, 62, 3),
        'Insta Gain Plan': (1600, 911, 24.79, 0, 24.79, 0, 36, 1), 'Dream Shield Plus': (2985, 632, 20.77, 6.15, 26.92, 23, 14, 0)},
    ('H1 FY27', PP['H1 FY27'], 1): {
        'Unnati': (17357, 4572, 32.11, 31.44, 63.55, 49, 991, 5), 'Wealth Pro': (22983, 1223, 31.48, 70.80, 102.27, 69, 1658, 7),
        'Growth Shield Plus': (6483, 2681, 44.67, 30.09, 74.76, 40, 84, 1), 'Dream Shield Plus': (2985, 836, 26.51, 10.54, 37.05, 28, 16, 0),
        'Guaranteed Bachat Plan': (9641, 4931, 26.20, 8.53, 34.72, 25, 238, 2),
        'Guaranteed Wealth Pro': (79692, 6710, 49.06, 161.56, 210.62, 77, 2348, 3),
        'Swabhimaan Retirement Plan': (1882, 631, 34.03, 12.73, 46.77, 27, 68, 3), 'Insta Gain Plan': (1600, 1523, 41.44, 5.45, 46.89, 12, 45, 1)},
}
FIELDS = [('Opening policies', 'count'), ('New policies', 'count'), ('New business premium', 'Rs cr'),
          ('Renewal premium', 'Rs cr'), ('Total premium', 'Rs cr'), ('Renewal proportion', '%'),
          ('Exits (maturity, surrender, withdrawal, foreclosure, cancellation)', 'count'), ('Exit proportion', '%')]
for (per, src, pg), d in PPD.items():
    for prod, vals in d.items():
        uin, cat = PRODS[prod]
        note = f'UIN {uin}; category {cat} (Bharti label, matches analysis/product_features_v1.csv).'
        if per == 'Q1 FY27':
            note += ' File states amounts in Rs; converted to Rs cr here.'
        if per == 'H1 FY27':
            note += ' File and table are labelled H2 FY27; period is Apr-Sep 2026.'
        if per in ('FY24', 'FY25', 'FY26'):
            note += ' Same values in all four Product Performance files.'
        for (f, unit), v in zip(FIELDS, vals):
            add(f, 'Bharti AXA Life ' + prod, per, v, unit, src, 'Product Performance table', pg, note)
for (per, src, pg) in PPD:
    if per in ('FY24', 'FY25'):
        for prod in PRODS:
            if prod not in PPD[(per, src, pg)]:
                add('New business premium', 'Bharti AXA Life ' + prod, per, 0, 'Rs cr', src, 'Product Performance table', pg,
                    'Shown as "-" (no sales; product not yet launched or no business).')

# ---------------------------------------------------------------- Monthly 90% lists
ML = {
    'Jun 2026': {'Guaranteed Bachat Plan': (13, '130N144V01'), 'Guaranteed Wealth Pro': (18, '130N107V12'), 'Insta Gain Plan': (8, '130N145V02'),
                 'Unnati': (11, '130N106V02'), 'Wealth Pro': (12, '130L100V03'), 'Swabhimaan Retirement Plan': (9, '130N109V03'),
                 'Growth Shield Plus': (14, '130L123V01'), 'Dream Shield Plus': (10, '130L125V01')},
    'Jul 2026': {'Guaranteed Wealth Pro': (18, '130N107V12'), 'Growth Shield Plus': (14, '130L123V01'), 'Guaranteed Bachat Plan': (11, '130N144V01'),
                 'Unnati': (11, '130N106V02'), 'Wealth Pro': (11, '130L100V03'), 'Swabhimaan Retirement Plan': (11, '130N109V03'),
                 'Insta Gain Plan': (10, '130N145V02'), 'Dream Shield Plus': (9, '130L125V01')},
    'Aug 2026': {'Guaranteed Wealth Pro': (18, '130N107V12'), 'Growth Shield Plus': (14, '130L123V01'), 'Guaranteed Bachat Plan': (10, '130N144V01'),
                 'Unnati': (12, '130N106V02'), 'Wealth Pro': (11, '130L100V03'), 'Swabhimaan Retirement Plan': (11, '130N109V03'),
                 'Insta Gain Plan': (11, '130N145V02'), 'Dream Shield Plus': (9, '130L125V01')},
    'Sep 2026': {'Guaranteed Wealth Pro': (17, '130N107V13'), 'Growth Shield Plus': (15, '130L123V01'), 'Guaranteed Bachat Plan': (9, '130N144V01'),
                 'Unnati': (11, '130N106V02'), 'Wealth Pro': (11, '130L100V03'), 'Swabhimaan Retirement Plan': (12, '130N109V04'),
                 'Insta Gain Plan': (14, '130N145V03'), 'Dream Shield Plus': (9, '130L125V01')},
}
TOT = {'Jun 2026': 96, 'Jul 2026': 95, 'Aug 2026': 96, 'Sep 2026': 97}
for per, d in ML.items():
    for prod, (pct, uin) in d.items():
        add('Share of FY27 year-to-date NBP (90% list)', 'Bharti AXA Life ' + prod, per, pct, '%', MR[per],
            'A. Products contributing to 90% of NBP', 2, f'UIN as printed: {uin}.')
    add('Share of FY27 year-to-date NBP (90% list)', 'Total of listed products', per, TOT[per], '%', MR[per],
        'A. Products contributing to 90% of NBP', 2)

# ---------------------------------------------------------------- Derived rows
def val(metric, seg, per, unit=None):
    for r in rows:
        if r[0] == metric and r[1] == seg and r[2] == per and (unit is None or r[4] == unit):
            return r[3]
    raise KeyError((metric, seg, per))


# Segment roll-ups used in the Excel (brief segments)
ROLL = {'Par': ['Par life', 'Par pension'], 'Non-par individual life': ['Non-par individual life'],
        'Non-par individual pension and annuity': ['Non-par individual pension'],
        'Health': ['Non-par individual health'], 'Non-par group': ['Non-par group'],
        'Linked (life, pension, group)': ['Linked life', 'Linked pension', 'Linked group']}
for per in YEARS + ['Q1 FY27', 'Q1 FY26']:
    src, pg = L1[per][0], L1[per][1]
    tot = val('Gross premium', 'Total', per)
    for name, parts in ROLL.items():
        v = sum(val('Gross premium', p, per) for p in parts)
        add('Gross premium (roll-up)', name, per, v, 'Rs lakh', src, 'L-1-A-RA (a) Premium', pg, 'Derived: sum of ' + ', '.join(parts) + '.')
        add('Share of gross premium', name, per, round(100 * v / tot, 1), '%', src, 'L-1-A-RA (a) Premium', pg, 'Derived: roll-up / total.')
    grp = val('Gross premium', 'Non-par group', per) + val('Gross premium', 'Linked group', per)
    add('Gross premium, group (non-par group + linked group)', 'Group', per, grp, 'Rs lakh', src, 'L-1-A-RA', pg, 'Derived.')
    add('Gross premium, individual', 'Individual', per, tot - grp, 'Rs lakh', src, 'L-1-A-RA', pg, 'Derived: total minus group.')
for a, b in zip(YEARS[:-1], YEARS[1:]):
    for s in SEGS:
        x, y = val('Gross premium', s, a), val('Gross premium', s, b)
        if x and x > 50:
            add('Gross premium growth', s, b, round(100 * (y / x - 1), 1), '%', L1[b][0], 'L-1-A-RA', L1[b][1], f'Derived: {b} vs {a}.')
    for name, parts in ROLL.items():
        x = sum(val('Gross premium', p, a) for p in parts)
        y = sum(val('Gross premium', p, b) for p in parts)
        if x > 50:
            add('Gross premium growth (roll-up)', name, b, round(100 * (y / x - 1), 1), '%', L1[b][0], 'L-1-A-RA', L1[b][1], f'Derived: {b} vs {a}.')

# NBP by segment: annual report FYP + single (FY21-FY24), then L-22 growth (FY25, FY26)
NBPSEG = {}
for per in ('FY21', 'FY22', 'FY23', 'FY24'):
    src, pg = S1[per][0], S1[per][1]
    for s in SEGS:
        v = (val('First year premium', s, per, "Rs '000") + val('Single premium', s, per, "Rs '000")) / 100.0
        NBPSEG[(s, per)] = v
        add('New business premium (first year + single)', s, per, round(v, 1), 'Rs lakh', src,
            'Annual report Schedule 1 Premium (segmental)', pg, "Derived: (first year + single) Rs '000 / 100." +
            (' Uses the reconstructed FY23 table.' if per == 'FY23' else ''))
GROWTH_SEG = {'Par life': 'Par life', 'Non-par individual life': 'Non-par individual life',
              'Non-par individual pension': 'Non-par individual pension', 'Non-par group': 'Non-par group',
              'Linked life': 'Linked life', 'Linked group': 'Linked group'}
for per, prev in (('FY25', 'FY24'), ('FY26', 'FY25')):
    src, p1 = L22P[per][0], L22P[per][1]
    total = 0.0
    for s in SEGS[:-1]:
        if s in GROWTH_SEG:
            g = val('NBP growth', GROWTH_SEG[s], per)
            v = NBPSEG[(s, prev)] * (1 + g / 100.0)
            note = f'DERIVED, not disclosed: {prev} segment NBP x (1 + L-22 NBP growth {g}%). Annual reports for FY25 and FY26 have no segment-wise first-year/single split.'
        else:
            v = NBPSEG[(s, prev)]
            note = f'DERIVED, not disclosed: L-22 shows NA growth for this segment; {prev} value carried. Small segment.'
        NBPSEG[(s, per)] = v
        total += v
        add('New business premium (first year + single)', s, per, round(v, 1), 'Rs lakh', src, 'L-22 row 1 applied to prior-year NBP', p1, note)
    actual = val('First year premium', 'Total', per, 'Rs lakh') + val('Single premium', 'Total', per, 'Rs lakh')
    NBPSEG[('Total', per)] = actual
    add('New business premium (first year + single)', 'Total', per, actual, 'Rs lakh', L4[per][0], 'L-4 Premium schedule', L4[per][1],
        f'Disclosed. Sum of derived segments = {total:,.0f}; gap {actual - total:,.0f} lakh ({100 * (actual - total) / actual:.1f}%).')
for per in YEARS:
    tot = NBPSEG[('Total', per)]
    src = S1[per][0] if per in S1 else L22P[per][0]
    pg = S1[per][1] if per in S1 else L22P[per][1]
    for name, parts in ROLL.items():
        v = sum(NBPSEG[(p, per)] for p in parts)
        add('NBP share (roll-up)', name, per, round(100 * v / tot, 1), '%', src,
            'Annual report Schedule 1' if per in S1 else 'Derived from L-22 growth', pg,
            'Derived.' + (' FY25/FY26 segment NBP are themselves derived.' if per in ('FY25', 'FY26') else ''))
# Individual vs group NBP from L-37/L-38
for per in YEARS + ['Q1 FY27']:
    ind = val('Individual new business premium by channel', 'Total', per)
    grp = val('Group new business premium by channel', 'Total', per)
    l4 = val('First year premium', 'Total', per, 'Rs lakh') + val('Single premium', 'Total', per, 'Rs lakh')
    src, pg = L38[per][0], L38[per][1]
    add('Individual share of NBP', 'Individual', per, round(100 * ind / (ind + grp), 1), '%', src, 'L-38 and L-37 totals', pg,
        f'Derived: individual / (individual + group). L-4 first year + single = {l4:,}; L-37 + L-38 = {ind + grp:,}.')
    for ch in CH[:-1]:
        if ch in ('Direct, online', 'Direct, others'):
            continue
        v = val('Individual new business premium by channel', ch, per)
        add('Channel share of individual NBP', ch, per, round(100 * v / ind, 1), '%', src, 'L-38', pg, 'Derived.')

# Operating expenses other than commission (approximate), used in the Notes tab
for per in YEARS + ['Q1 FY27']:
    e, c = val('Expenses of management to gross direct premium', 'Total', per), val('Commission ratio', 'Total', per)
    src, p1 = L22P[per][0], L22P[per][1]
    add('Operating expenses other than commission to gross premium (approx.)', 'Total', per, round(e - c, 1), '%', src, 'L-22 rows 6 and 7', p1,
        'Derived: EoM ratio minus commission ratio. Approximate: commission ratio is printed rounded in some years, and EoM here is gross (before transfer to shareholders).')

# Single vs regular for individual NBP
for per in YEARS + ['Q1 FY27', 'Q1 FY26']:
    s = val('Single premium share of individual NBP', 'Individual', per)
    src, p1 = L22P[per][0], L22P[per][1]
    add('Regular premium share of individual NBP', 'Individual', per, round(100 - s, 1), '%', src, 'L-22 row 2', p1, 'Derived: 100 minus single share.')
# AUM growth
for a, b in zip(YEARS[:-1], YEARS[1:]):
    x, y = val('AUM (investments L-12 + L-13 + L-14)', 'Total', a), val('AUM (investments L-12 + L-13 + L-14)', 'Total', b)
    add('AUM growth', 'Total', b, round(100 * (y / x - 1), 1), '%', L3[b][0], 'L-3-A-BS', L3[b][1], f'Derived: {b} vs {a}.')
# Product share of individual NBP (90% list products)
for per, prev_files in (('FY24', None), ('FY25', None), ('FY26', None), ('Q1 FY27', None)):
    key = [k for k in PPD if k[0] == per][0]
    s = sum(v[2] for v in PPD[key].values())
    ind_cr = val('Individual new business premium by channel', 'Total', per) / 100.0
    add('NBP of products on the current 90% list', 'Total of listed products', per, round(s, 2), 'Rs cr', key[1],
        'Product Performance table', key[2], 'Derived: sum of listed products.')
    add('Listed products as share of individual NBP', 'Total of listed products', per, round(100 * s / ind_cr, 1), '%', key[1],
        'Product Performance table and L-38', key[2], f'Derived: listed-product NBP / L-38 individual NBP ({ind_cr:,.2f} cr).')


# ---------------------------------------------------------------- Peer view, FY26 (year to date)
# Persistency: L-22 row 19, premium basis, regular/limited pay, individual, "up to the quarter / year ended
# March 31, 2026" column. Conservation: L-22 row 5, same column. Files are in Desktop/LI-PDs.
# Segment premium: deliverables/01 Data tab, which S1 built from each insurer's L-1-A-RA (a) Premium.
PEERS = {
    # name: (file, L-1 pages, L-22 conservation page, L-22 persistency page,
    #        persistency 13/25/37/49/61, conservation {segment: value})
    'SBI Life': ('sbi-life-q4fy26.pdf', '3-6', 38, 39, [87.55, 77.66, 72.22, 68.64, 57.98],
                 {'Linked life': 87.57, 'Par life': 89.58, 'Non-par life': 86.71, 'Overall': 85.40}),
    'HDFC Life': ('hdfc-life-q4fy26.pdf', '2-6', 32, 33, [84.9, 77.1, 72.6, 70.9, 64.4],
                  {'Linked life': 83.6, 'Par life': 84.6, 'Non-par life': 87.6}),
    'ICICI Prudential Life': ('icici-pru-q4fy26.pdf', '3-6', 53, 54, [83.1, 76.5, 76.6, 71.1, 61.7],
                              {'Linked life': 79.5, 'Par life': 79.9, 'Non-par life': 88.5}),
    'Axis Max Life': ('axis-max-q4fy26.pdf', '2-6', 27, 28, [83, 73, 66, 58, 58],
                      {'Linked life': 77.2, 'Par life': 84.4, 'Non-par life': 87.7}),
    'Tata AIA Life': ('tata-aia-q4fy26.pdf', '2-6', 29, 30, [86.10, 78.39, 76.57, 72.29, 66.41],
                      {'Linked life': 85.78, 'Par life': 84.28, 'Non-par life': 90.25}),
    'Bajaj Life': ('bajaj-life-q4fy26.pdf', '2-6', 39, 40, [80.6, 70.9, 67.4, 61.8, 51.4],
                   {'Linked life': 83.3, 'Par life': 82.0, 'Non-par life': 85.5}),
    'Aditya Birla Sun Life': ('absli-q4fy26.pdf', '1-5', 33, 33, [82.40, 70.11, 68.59, 62.96, 58.45],
                              {'Linked life': 77.09, 'Par life': 88.08, 'Non-par life': 84.81}),
    'Canara HSBC Life': ('canara-hsbc-q4fy26.pdf', '2-6', 41, 42, [85.4, 72.1, 66.2, 60.8, 54.3],
                         {'Linked life': 85.2, 'Par life': 86.2, 'Non-par life': 87.4}),
    'Ageas Federal Life': ('ageas-federal-q4fy26.pdf', '1-4', 34, 35, [79.02, 71.16, 66.18, 58.98, 43.51],
                           {'Linked life': 79.30, 'Par life': 82.17, 'Non-par life': 87.00}),
    'Shriram Life': ('shriram-life-q4fy26.pdf', '2-6', 31, 32, [60.9, 45.4, 41.6, 33.0, 28.5],
                     {'Linked life': 77.9, 'Par life': 79.9, 'Non-par life': 76.8}),
    'Generali Central Life': ('generali-central-q4fy26.pdf', '4-7', 36, 37, [71.03, 56.41, 50.59, 40.89, 29.07],
                              {'Linked life': 61, 'Par life': 87, 'Non-par life': 54}),
    'Pramerica Life': ('pramerica-q4fy26.pdf', '2-6', 31, 32, [73.2, 64.6, 60.1, 58.0, 54.6],
                       {'Linked life': 74.85, 'Par life': 83.24, 'Non-par life': 81.63}),
    'IndusInd Nippon Life': ('indusind-nippon-q4fy26.pdf', '3-6', 31, 31, [80.2, 67.7, 63.7, 57.8, 38.7],
                             {'Linked life': 73.2, 'Par life': 87, 'Non-par life': 82}),
}
for name, (f, l1p, cp, pp, pers, cons) in PEERS.items():
    for mth, v in zip(MON, pers):
        add('Peer: persistency, premium basis, regular/limited pay', name + ' | ' + mth, 'FY26', v, '%', f, 'L-22 row 19', pp,
            'Year-to-date FY26 column. ' + ('Printed as whole percentages.' if name == 'Axis Max Life' else ''))
    for seg, v in cons.items():
        note = 'Year-to-date FY26 column.'
        if name == 'Aditya Birla Sun Life':
            note += ' ABSLI labels rows by segment name (e.g. "Non Participating Linked - Individual Life").'
        if name in ('Generali Central Life', 'IndusInd Nippon Life'):
            note += ' Printed as whole percentages.'
        add('Peer: conservation ratio', name + ' | ' + seg, 'FY26', v, '%', f, 'L-22 row 5', cp, note)
for mth, v in zip(MON, PR['FY26'][0]):
    add('Peer: persistency, premium basis, regular/limited pay', 'Bharti Life | ' + mth, 'FY26', v, '%', P26, 'L-22 row 19', 30, 'Same as the Bharti KPI rows.')
for seg, key in (('Linked life', 'Linked life'), ('Par life', 'Par life'), ('Non-par life', 'Non-par individual life')):
    add('Peer: conservation ratio', 'Bharti Life | ' + seg, 'FY26', val('Conservation ratio', key, 'FY26'), '%', P26, 'L-22 row 5', 29, 'Same as the Bharti KPI rows.')

D01 = 'deliverables/01_life_insurance_category_analysis_Q4FY26.xlsx'
try:
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(os.path.dirname(__file__), '..', '..', '..', D01), data_only=True)
    ws = wb['Data']
    hdr = [c.value for c in ws[4]]
    files = {n: v[0] for n, v in PEERS.items()}
    files['Bharti Life'] = 'bharti-life-q4fy26.pdf'
    l1pages = {n: v[1] for n, v in PEERS.items()}
    l1pages['Bharti Life'] = '2-5'
    for r in ws.iter_rows(min_row=5, values_only=True):
        if r[0] not in files:
            continue
        for h, v in zip(hdr[2:], r[2:]):
            if h is None or v is None:
                continue
            add('Peer: gross premium by segment', r[0] + ' | ' + h, h.split(' ')[0], v, 'Rs cr', files[r[0]],
                'L-1-A-RA (a) Premium, via deliverable 01 Data tab', l1pages[r[0]],
                'Copied from deliverable 01 (S1). Group business sits inside each segment. FY25 values are the prior-year column of the FY26 PD.')

    # Derived peer mix and growth (used by the Peer view tab)
    def pseg(n, col):
        for r in rows:
            if r[0] == 'Peer: gross premium by segment' and r[1] == f'{n} | {col}':
                return r[3] or 0
        return 0
    for n in list(PEERS) + ['Bharti Life']:
        t26, t25 = pseg(n, 'FY26 Grand Total (L-1)'), pseg(n, 'FY25 Grand Total (L-1)')
        cat26 = {'Par': sum(pseg(n, f'FY26 {c}') for c in ('Par Life', 'Par Pension', 'Par Annuity')),
                 'Non-par life': pseg(n, 'FY26 Non-Par Life'),
                 'Non-par pension and annuity': sum(pseg(n, f'FY26 {c}') for c in ('Non-Par Annuity', 'Non-Par Pension')),
                 'Linked': sum(pseg(n, f'FY26 {c}') for c in ('Linked Life', 'Linked Pension'))}
        cat25 = {'Par': sum(pseg(n, f'FY25 {c}') for c in ('Par Life', 'Par Pension', 'Par Annuity')),
                 'Non-par life': pseg(n, 'FY25 Non-Par Life'),
                 'Linked': sum(pseg(n, f'FY25 {c}') for c in ('Linked Life', 'Linked Pension'))}
        cat26['Health and variable'] = t26 - sum(cat26.values())
        f, pg = files[n], l1pages[n]
        for c, v in cat26.items():
            add('Peer: share of gross premium', f'{n} | {c}', 'FY26', round(100 * v / t26, 1), '%', f,
                'L-1-A-RA, via deliverable 01 Data tab', pg, 'Derived: category / grand total. Non-par life includes group.')
        add('Peer: gross premium growth', f'{n} | Total', 'FY26', round(100 * (t26 / t25 - 1), 1), '%', f,
            'L-1-A-RA, via deliverable 01 Data tab', pg, 'Derived: FY26 vs FY25 grand total.')
        for c, v25 in cat25.items():
            if v25:
                add('Peer: gross premium growth', f'{n} | {c}', 'FY26', round(100 * (cat26[c] / v25 - 1), 1), '%', f,
                    'L-1-A-RA, via deliverable 01 Data tab', pg, 'Derived: FY26 vs FY25.')
except ImportError:
    print('openpyxl not installed: peer segment premium rows skipped')

with open(OUT, 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(H)
    w.writerows(rows)
print(len(rows), 'rows ->', os.path.normpath(OUT))
