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

# ---- EoM breach, forbearance, show-cause notice: quotes and references
EOM_Q = [
    # (year, point, exact quote, source file, page, who, check status)
    ('FY21', 'Excess charged to shareholders; industry forbearance application',
     "We draw attention to Note No. 23 (c) of Notes forming part of financial statements regarding expenses incurred in excess of limits specified by IRDAI Expenses of Management Rules 2016, aggregating to Rs. 20,04,007 ('000) pertaining to FY 2020-21 charged to Shareholders Account. An application has been made by Life Council to IRDAI seeking forbearance on behalf of several life insurance companies.",
     'fy21-annual-report', '60', 'Auditors (emphasis of matter)', 'Text layer'),
    ('FY17-FY20', 'Forbearance history',
     'The Company has received forbearance as per EOM Regulations, 2016 for the FY 2016-17, FY 2017-18 and FY 2018-19.The company has received forbearance for FY 2019-20 vide Letter No. 446/16/F&A-L/EoM/2019-20/ dated 23rd November 2020.',
     'fy21-annual-report', '130', 'Company (notes to accounts)', 'Text layer'),
    ('FY22', 'Excess charged; company applies for forbearance',
     "...aggregating to ` 23,14,373 ('000) pertaining to F.Y. 2021-22 charged to Shareholders Account. An application has been made by the Company to IRDAI seeking forbearance of expenses in excess of the limits incurred for the F.Y: 2021-22 u/s 64K(l) of the IRDA Act.",
     'fy22-annual-report.pdf', '43', 'Auditors (emphasis of matter)', 'Text layer'),
    ('FY17-FY21', 'Forbearance granted up to FY21',
     'The Company has received forbearance as per EOM Regulations, 2016 for the FY 2016-17, FY 2017-18, FY 201819, FY 2019-20 & FY 2020-21.',
     'fy22-annual-report.pdf', '79', 'Company (notes to accounts)', 'Text layer'),
    ('FY22', 'Forbearance application date',
     'The company has applied to IRDAI for forbearance for F.Y. 2021-22 vide letter dated 14th March 2022, which is awaited.',
     'fy22-annual-report.pdf', '80', 'Company (notes to accounts)', 'Text layer'),
    ('FY23', 'Excess charged; company applies for forbearance',
     "...aggregating to Rs. 20,97,385 ('000) pertaining to FY. 2022-23 charged to Shareholders Account. An application has been made by the Company to IRDAI seeking forbearance of expenses in excess of the limits incurred for the F.Y. 2022-23 u/s 64K(1) of the IRDA Act.",
     'fy23-annual-report.pdf', '53', 'Auditors (emphasis of matter)', 'OCR; user checked the scan'),
    ('FY22, FY23', 'FY22 forbearance granted; FY23 applied',
     'IRDAI vide letter dated 7th December, 2022 having Ref no. 446/20/F&I-L/EoM/2021-22/75 have granted Forbearance for Expense of Management for FY 2021-22. The company has applied to IRDAI for forbearance for F.Y. 2022-23 vide letter dated 31st March 2023, which is awaited.',
     'fy23-annual-report.pdf', '120', 'Company (notes to accounts)', 'OCR; wording as read by the user from the scan'),
    ('FY23, FY24', 'Auditors flag both years',
     'We draw attention to Note No. 23 (b) of Schedule 16 of Notes to Accounts forming part of financial statements on excess of Expense of Management for F.Y. 2022-2023 and F.Y. 2023-2024. Our opinion is not modified in respect of above matter.',
     'fy24-annual-report.pdf', '51', 'Auditors (emphasis of matter)', 'Text layer'),
    ('FY24', 'Excess charged; forbearance applied for FY23 and FY24',
     "...such excess has been charged to shareholder account which amounts to Rs. 10,03,754 ('000) [Previous Year 20,97,387 ('000)]. ... The company has applied to IRDAI for forbearance for F.Y. 2022-23 vide letter dated 31st March 2023 & for F.Y. 2023-24 vide letter dated 22nd March 2024, which is awaited.",
     'fy24-annual-report.pdf', '106', 'Company (notes to accounts)', 'Text layer'),
    ('FY25', 'EoM over the 2024 Regulations limit; forbearance applied through Life Council',
     "...with respect to the Company's 'Expense of Management' (EoM') ratio, which is in excess of the limits as per Insurance Regulatory and Development Authority of India (Expenses of Management, including Commission, of Insurers) Regulations, 2024. The Company has filed an application for forbearance for exceeding the EoM beyond the allowable limits for the financial year ended March 31, 2025, with IRDAI (through Life Council) vide email dated March 27, 2025. The grant of such forbearance is at IRDAI's discretion and so the impact of the same on the financial statements will depend on the final communication from IRDAI.",
     'fy25-annual-report.pdf', '36-37', 'Auditors (emphasis of matter)', 'OCR'),
    ('FY24, FY26', 'Forbearance up to FY24; 3-year plan to reach the limit by FY26',
     'The Company has received forbearance as per EOM Regulations till Financial Year 2023-24. The company has applied to IRDAI for forbearance for Financial Year 2024-2025 vide email dated March 27, 2025. ... The Company has submitted the 3 years Board approved business plan on August 07, 2023 to bring the EOM within the prescribed limits by Financial Year 2025-2026.',
     'fy25-annual-report.pdf', '87', 'Company (notes to accounts)', 'OCR; user checked the scan (OCR typos corrected)'),
    ('FY25', 'EoM ratio 101%; par within limits',
     'As at 31st March 2025, the EOM ratio at Company Level is 101%, Rs 879 lakhs and at Individual Participating segment it is within limits at 99%, The Company anticipates that EOM ratio for Financial Year 2025-2026 will be within the regulatory limit of 100%.',
     'fy25-annual-report.pdf', '87', 'Company (notes to accounts)', 'OCR; user checked the scan'),
    ('FY25', 'Show-cause notice received, response filed (auditors)',
     "During the year, the Company has received a show-cause notice from the IRDAI against which the Company has filed its response. The grant of such forbearance is at IRDAI's discretion and so the impact of the same on the financial statements will depend on the final communication from IRDAI. Our opinion is not modified in respect of this matter.",
     'fy26-annual-report.pdf', '40-41', 'Auditors (emphasis of matter)', 'OCR'),
    ('FY26', 'Within the limit',
     'Actual expenses incurred for FY 2025-26 are within the allowable limit so no amount have been charged to shareholder account towards the excess expense over the allowable limit as per IRDAI (Expenses of Management of Insurers transacting life insurance business) Regulations, 2024.',
     'fy26-annual-report.pdf', '100', 'Company (notes to accounts)', 'OCR; user checked the scan'),
    ('FY25', 'Show-cause notice date',
     'The Company have received show-cause notice for FY 24-25 on 15th January, 2026 and response for same has been filed. The Company believes that they shall get this approval in accordance with applicable Expense of Management Regulations.',
     'fy26-annual-report.pdf', '101', 'Company (notes to accounts)', 'OCR; user checked the scan'),
    ('Rule', 'Forbearance is normally only for insurers in their first 5 years',
     "16. Life Insurers: The Authority may exercise forbearance in case a Life insurer exceeds the limits of expenses of management on an overall basis in the Participating and Non-Participating (including Linked) business. Such forbearance may be exercised on a case to case basis in respect of insurers having 'duration of business' up to 5 years.",
     'IRDAI (Expenses of Management, including Commission, of Insurers) Regulations, 2024; Gazette 23 Jan 2024, F. No. IRDAI/Reg/2/196/2024', '18', 'Regulator (regulation 16)', 'Downloaded from irdai.gov.in, document-detail?documentId=4359902'),
    ('Rule', 'Transition route for insurers over the limit in FY24: back within limits by FY26',
     '17. In case of an insurer having actual expenses of management more than the allowable expenses of management for the financial year 2023-24, the Authority, having regard to the business model of the insurer, may grant forbearance subject to the confirmation by its board that it shall bring its actual expenses within the allowable limits, within a period of 2 years i.e. by the end of financial year 2025-26.',
     'IRDAI EoM Regulations 2024', '18', 'Regulator (regulation 17)', 'irdai.gov.in'),
    ('Rule', 'Variable pay for MD/CEO/KMPs',
     'In case the actual expenses of management of an insurer exceeds by 10 percent or more of the projected expenses of management levels as per the Business plan formulated in terms of Regulation 5, no variable pay shall be payable to Managing Director (MD) / Chief Executive Officer (CEO) / Whole-Time Directors (WTD) and Key Management Persons (KMPs) for the said financial year.',
     'IRDAI EoM Regulations 2024', '19', 'Regulator (regulation 21)', 'irdai.gov.in'),
    ('Rule', 'What IRDAI can do on a breach',
     '22. Additional compliance: (1) In case an Insurer exceeds the limits of expenses as specified in these regulations or is not in compliance with the directions issued by the Authority in this regard; it may be subject to one or more of the following: (a) Excess to be charged to Profit and Loss Account; (b) Restrictions on opening of new places of business; (c) Administer a warning to the insurer; (d) Cause a valuation of the insurer to evaluate its financial health and soundness; (e) Penal action under section 102 of the Act; (f) Restriction of performance incentive to ... (KMPs); (g) Removal of Managerial Personnel and / or appointment of Administrator; (h) Any other action as specified in the Act. (2) ... also direct the insurer not to underwrite new business in one or more segments in case of repeated breach of the limits of expenses...',
     'IRDAI EoM Regulations 2024', '19', 'Regulator (regulation 22)', 'irdai.gov.in'),
    ('FY25 industry', '8 of 25 life insurers exceeded the limit in FY25 (not named)',
     'During the year 2024-25, out of 25 life insurers in operation, 17 were compliant with the aforementioned regulations. Eight life insurers had exceeded the limits of expenses on an overall basis in Par/Non-Par (including Linked) business.',
     'IRDAI Annual Report 2024-25 (lifeinscouncil.org/component/IRDAI Annual Report 2024-25.pdf)', 'PDF 40, para I.2.2.10', 'Regulator', 'Text layer'),
    ('Aug 2026', 'What IRDAI did to two life insurers in the same position',
     'The Insurance Regulatory and Development Authority of India (IRDAI) passed Orders against Edelweiss Life Insurance Co. Limited and Pramerica Life Insurance Limited for exceeding the permissible Expenses of Management (EoM) limits ... The insurers were warned for their failure to remain within the prescribed EoM limits and directed not to open any new place of business for a period of six months from the date of the Order, under Regulation 22(1)(b) and (c) of the EoM Regulations, 2024.',
     'IRDAI press release, 21 Aug 2026 (irdai.gov.in document-detail?documentId=9753023)', '1', 'Regulator', 'irdai.gov.in'),
    ('Aug 2026', 'Same action against two non-life insurers',
     'The Insurance Regulatory and Development Authority of India (IRDAI) passed Orders against Acko General Insurance Limited and Niva Bupa Health Insurance Co. Limited for exceeding the permissible Expenses of Management (EoM) limits ...',
     'IRDAI press release, 20 Aug 2026 (irdai.gov.in document-detail?documentId=9748708)', '1', 'Regulator', 'irdai.gov.in'),
    ('Status 5 Nov 2026', 'No published IRDAI order against Bharti Life',
     'IRDAI Warnings and Penalties page, page 1 (entries 25-11-2025 to 15-10-2026), lists orders against Edelweiss Life, Pramerica Life, Canara HSBC Life, Acko General, Niva Bupa and others. None names Bharti, Bharti AXA or Bharti Life.',
     'irdai.gov.in/warnings-and-penalties', 'page 1 of 21', 'Our check', 'Checked 5 Nov 2026'),
]
OPEN_Q = [
    'Has IRDAI decided the FY25 show-cause notice? No order was published as of 5 Nov 2026. Edelweiss Life and Pramerica Life got a warning and a 6-month ban on new branches in Aug 2026 for the same breach; ask whether Bharti received a similar order that is not yet published.',
    'Why a show-cause notice at all? Regulation 17 gives insurers over the limit in FY24 until the end of FY26 to comply, subject to a board confirmation. Bharti\'s 7 Aug 2023 plan targets FY26. Did Bharti apply under regulation 17, and did IRDAI accept the plan?',
    'Were FY23 and FY24 forbearance formally granted? The FY25 report says forbearance was received "till Financial Year 2023-24" but quotes no IRDAI letter reference for those years (FY22 has one: 446/20/F&I-L/EoM/2021-22/75).',
    'Is Bharti one of the 8 life insurers that exceeded the limit in FY25 (IRDAI Annual Report 2024-25, para I.2.2.10)? Very likely at 101%, but the report does not name them.',
    'Regulation 21: was EoM 10% or more above Bharti\'s business-plan projection in any year since FY25? If so, no variable pay for MD/CEO/KMPs that year. Check remuneration disclosures.',
    'FY27 run-rate: Q1 FY27 EoM to gross premium was 47.7% (Q1 FY26: 38.4%). Q1 ratios are seasonally high, but worth tracking against the limit.',
    'Proposed lower EoM limits: news reports in Oct 2026 (e.g. Business Standard) describe an IRDAI consultation paper cutting life EoM limits. Not yet checked on irdai.gov.in.',
    'Other regulatory items in the FY26 annual report: an IND AS forbearance application (p14, p114); a Maharashtra GST order for FY2018-19 of Rs 3,452 lakh plus interest and penalty, dated 26 Apr 2024 (p90); transfer of a 15% stake by Bharti Life Ventures to 360 ONE funds during FY26 (p90).',
]
r0 = len(notes) + 3
ws.cell(r0, 1, 'EoM breach, forbearance and the FY25 show-cause notice: quotes and references').font = TITLE
ws.cell(r0 + 1, 1, 'Quotes are verbatim from the page cited (PDF page numbers). Annual reports are in Desktop/for-liprodanal-agent; IRDAI documents are on irdai.gov.in. "..." marks omitted text.')
hdr = ['Year', 'Point', 'Exact quote', 'Source', 'Page', 'Who says it', 'Text quality / check']
for j, h in enumerate(hdr, 1):
    c = ws.cell(r0 + 2, j, h)
    c.font = BOLD
    c.fill = HFILL
for i, row in enumerate(EOM_Q, r0 + 3):
    for j, v in enumerate(row, 1):
        c = ws.cell(i, j, v)
        c.alignment = WRAP
r1 = r0 + 3 + len(EOM_Q) + 1
ws.cell(r1, 1, 'Open questions to look into').font = BOLD
for i, q in enumerate(OPEN_Q, r1 + 1):
    ws.cell(i, 1, f'{i - r1}.')
    c = ws.cell(i, 2, q)
    c.alignment = WRAP
ws.column_dimensions['A'].width = 16
for col, w in zip('BCDEFG', (34, 90, 36, 10, 22, 22)):
    ws.column_dimensions[col].width = w
for i in range(1, len(notes) + 1):
    ws.cell(i, 1).alignment = Alignment(wrap_text=False)

# ---- IRDAI consultation paper on distribution reforms (Sep 2026)
CPQ = [
    # (proposal, exact quote, source page, what it means for Bharti)
    ('EoM is kept and tightened, not removed',
     'The current EoM computation is a single composite ceiling which in itself is sound and simple. Within this framework the following reforms are proposed: ... In the case of Life insurance, the EoM will be Total Expenses as a percentage of Total Premium.',
     'Part 1, p43, para 95(1)',
     'The ceiling stays; the measure becomes total expenses / total premium. Bharti\'s closest published measure is L-22 row 6 (EoM to gross direct premium): 34.2% in FY26, 31.4% in FY25.'),
    ('New life limit: 15% in 2 years, 12.5% in 5 years',
     'To achieve an EoM of 15% of the premium in 2 years and 12.5% in 5 years (FY2027-28 being Year 1) with a glide path requiring reduction every year.',
     'Part 1, p43, Box 2 A(i)',
     'Bharti would need to go from about 34% to 15% by FY2028-29 and 12.5% by FY2031-32, i.e. cut its expense ratio by more than half. The paper puts the private life average at 20.2% in FY26 (Box 1, p42). Our reading: Bharti is among the furthest from the target.'),
    ('Why IRDAI is acting',
     'In life insurance, expenses fell steadily from 21.3% of gross premium in FY15 to a low of 16.5% in FY21, before reversing course to reach 20.2% in FY26, nearly back to where the decade began.',
     'Part 1, p42, Box 1',
     'Context for Bharti\'s repeated breaches FY21-FY25.'),
    ('Operating expenses (not just commission) are a target',
     'For FY26 operational expenses other than commissions varied from 6.1% to 27.7% of the premium in case of Life insurers ... It is evident that insurers will also have to focus on controlling operational expenses other than commissions if they are to deliver the expected value to customers.',
     'Part 1, p44, para 95(5)',
     'Bharti\'s operating expenses other than commission were about 26.2% of gross premium in FY26 (L-22 EoM 34.2% minus commission 8%; approximate), near the top of IRDAI\'s 6.1%-27.7% range. Its commission ratio (8%) is below the private-life average of 9% (Part 1 p46). Bharti\'s gap is mainly operating cost and scale, not commission.'),
    ('2023 carve-outs folded back into EoM',
     'The 2023 EoM framework carved out additional allowances over and above the Expenses of Management limit, including technology and insurance awareness spend, and rural and government scheme expenses. ... To simplify the EoM structure, these would have to be included in the overall EoM.',
     'Part 1, p42, para 94',
     'Any technology or awareness spend Bharti currently keeps outside the limit would count against it. Not visible in the PDs; worth asking.'),
    ('Consequences of missing the glide path',
     'Insurers that have not converged on the EoM ceiling by the scheduled dates should face graduated supervisory consequences such as restrictions on new product launches, restrictions on dividend distribution, and in extreme cases restrictions on new business through the channel responsible for the over run.',
     'Part 1, p44, para 97',
     'Harsher than today\'s Regulation 22 practice (warning plus branch-opening ban, Aug 2026). Restrictions on new product launches would hit Bharti\'s product plans directly.'),
    ('Hard commission caps return',
     'The inability to exercise adequate cost discipline under the flexible EoM regime makes a compelling case for hard caps on commissions within revised EoM limits, stringent implementation, and enhanced regulatory oversight.',
     'Part 1, p45, para 101',
     'Caps by product, premium-paying term and channel (Box 4B, p51-52).'),
    ('Lower caps for open-architecture distributors (brokers, banks, corporate agents)',
     'Open distribution architecture should have lower commission limits to create disincentive against commission-led sales. ... IDEs will have lower commission caps compared to individual category (agents and associates) engaged directly by insurers.',
     'Part 1, p47, para 102(1)-(2)',
     'In FY26, 42% of Bharti\'s individual NBP came through corporate agents (banks 10.1%, others 17.8%) and brokers (13.9%) (PD L-38). A small insurer may find it harder to win shelf space with banks and brokers when it cannot outbid larger insurers on commission. Our inference, not in the paper.'),
    ('Very low caps on single premium savings and annuity',
     'Individual Savings: single premium 1% (distribution entities), 2% (agents). Pension/deferred annuity/ Immediate Annuity*: single premium 0.5% / 0.75%.',
     'Part 1, p51-52, Box 4B',
     'Single premium was 10.9% of Bharti\'s individual NBP in FY26 (L-22). Swabhimaan Retirement Plan (annuity) was 12% of FY27 NBP to Sep 2026 (90% list). Products sold on single premium through distributors would carry little commission room.'),
    ('Regular-premium caps rise with premium-paying term',
     'Individual Non-Linked (Par or Non-Par) and Linked: first year 5% (PPT below 5 years) up to 20% (PPT 10 years and above) for distribution entities; 6.25% to 25% for agents. Renewal 2%-3% (entities), 5% (agents).',
     'Part 1, p51, Box 4B',
     'Short-PPT savings products (e.g. 5-8 year pay) get low first-year caps. Check the PPT mix of Guaranteed Wealth Pro, Guaranteed Bachat and Unnati against these caps.'),
    ('Commission should reward persistency',
     'Commission structure for life insurance policies should incentivize distribution persons and entities to nudge policyholders to persist with the multi-year payment plans instead of incentivizing first year payment.',
     'Part 1, p48, para 102(9)',
     'Bharti\'s 13th-month persistency (64.5% FY26) is second-lowest of the 14 insurers in the Peer view. Renewal-weighted commissions would reward distributors who keep policies alive.'),
    ('All payouts count as commission',
     'Commissions should be all-inclusive covering direct commission, incentives, awards, reimbursement of selling expenses, brand value payments to related parties, non-cash incentives like gifts and visits.',
     'Part 1, p48, para 102(12)',
     'Payments now booked as operating expense (e.g. sales promotion) would move under the commission caps.'),
    ('Cost audit for every insurer',
     'All insurers irrespective of their business size, and IDEs with insurance commission income above ₹100 crores would be mandated to have an annual cost audit and submit the report to their respective Board and to the regulator.',
     'Part 1, p53, para 105',
     'Applies to Bharti.'),
    ('Industry evidence on distribution cost',
     'Private life insurers paid an average commission of 9% of the total premium mobilised during FY26. ... Across private life insurers, commission payments ranged from 3% to 39%. ... Multiple tie-up bank arrangements entailed much higher average total pay-out of 33% of the life new business premium generated.',
     'Part 2, p8 para 2.3.1; p13 para 9.1.4',
     'Bharti\'s FY26 commission ratio of 8% is close to the average. The paper does not name insurers.'),
    ('Timeline',
     'The last date for submission of comments and feedback is 25th October 2026. ... The EoM norms will be reviewed along with products reforms which are likely to follow during FY28.',
     'Part 1, p76 para 163; p44 para 96',
     'Comments closed 25 Oct 2026. Final regulations not yet issued (as of 5 Nov 2026). Proposed Year 1 of the glide path is FY2027-28.'),
]
r2 = ws.max_row + 2
ws.cell(r2, 1, 'IRDAI consultation paper: Recalibrating economics of insurance distribution (Sep 2026)').font = TITLE
ws.cell(r2 + 1, 1, 'Source: "Distribution Reforms Part 1.pdf" (80 pages) and "Part 2.pdf" (41 pages) on the user\'s desktop; PDF created 23 Sep 2026. Proposals only, not yet regulation. The paper keeps EoM and tightens it; it does not remove it.')
for j, h in enumerate(['Proposal', 'Exact quote', 'Page', 'What it means for Bharti (our reading; Bharti figures from the CSV)'], 1):
    c = ws.cell(r2 + 2, j + 1, h)
    c.font = BOLD
    c.fill = HFILL
for i, row in enumerate(CPQ, r2 + 3):
    ws.cell(i, 1, i - r2 - 2)
    for j, v in enumerate(row, 2):
        ws.cell(i, j, v).alignment = WRAP
r3 = r2 + 3 + len(CPQ) + 1
ws.cell(r3, 1, 'Open questions on the consultation paper').font = BOLD
for k, q in enumerate([
    'What is Bharti\'s EoM on the paper\'s proposed basis (total expenses / total premium)? L-22 row 6 is the closest public figure; the exact basis may differ (gross vs after transfer to shareholders).',
    'What did the Life Insurance Council and Bharti submit in the consultation (closed 25 Oct 2026)? Smaller insurers may seek a longer glide path.',
    'Under the proposal, would the 15% target apply from FY2028-29 (Year 2) to an insurer with Bharti\'s scale, or is there a size or vintage relief? The paper gives none.',
    'How much of Bharti\'s new business is short premium-paying-term or single premium, where the proposed caps are lowest?',
], 1):
    ws.cell(r3 + k, 1, f'{k}.')
    ws.cell(r3 + k, 2, q).alignment = WRAP
ws.column_dimensions['E'].width = 60

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
