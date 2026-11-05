"""QA workbook for ULIP feature list v4 (S3). Reads analysis/product_features_ulip_v4.csv, analysis/v4/v4_changes.csv,
analysis/v4/additions_basis.csv, results/ulip_rider_benefits.csv and the v4 workbook's Features tab.
Output: qa/s3_v4/v4_qa_workbook.xlsx
Usage: python3 -I qa/s3_v4/build_v4_qa_workbook.py <repo_dir>"""
import csv, glob, os, random, re, sys, collections as C
import openpyxl
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

R = sys.argv[1]
random.seed(20261105)
PF = {}
for r in csv.DictReader(open(os.path.join(R, 'analysis/product_features_ulip_v4.csv'), encoding='utf-8')):
    PF[(r['uin'], r['feature'])] = r
CH = list(csv.DictReader(open(os.path.join(R, 'analysis/v4/v4_changes.csv'), encoding='utf-8')))
AB = list(csv.DictReader(open(os.path.join(R, 'analysis/v4/additions_basis.csv'), encoding='utf-8')))
RB = {r['ulip_uin']: r for r in csv.DictReader(open(os.path.join(R, 'results/ulip_rider_benefits.csv'), encoding='utf-8'))}
v4 = openpyxl.load_workbook(os.path.join(R, 'analysis/feature_list_ulip_v4.xlsx'), read_only=True)
feat_rows = [r for r in v4['Features'].iter_rows(values_only=True)][1:]
DEF = {r[1]: r[2] for r in feat_rows if r[1]}
rider_ws = [r for r in v4['Rider recoding'].iter_rows(values_only=True)][3:]
deep = sorted({u for (u, f), r in PF.items() if r['source'] == 'deep'})
name = {u: PF[(u, 'fund_switch')]['product'] if (u, 'fund_switch') in PF else u for u in deep}
ins = {u: PF[(u, 'fund_switch')]['insurer'] for u in deep}


def docs(u):
    return ' ; '.join(sorted(os.path.relpath(p, R) for p in glob.glob(os.path.join(R, 'docs', '*', u, '*.pdf'))))


def cell(u, f):
    r = PF.get((u, f), {})
    return [r.get('code', ''), (r.get('value') or '')[:500], r.get('doc', ''), r.get('page', ''), (r.get('quote') or '')[:500]]


wb = Workbook(); wb.remove(wb.active)
HEAD = PatternFill('solid', fgColor='1F3864'); HF = Font(bold=True, color='FFFFFF'); YEL = PatternFill('solid', fgColor='FFF2CC')
WR = Alignment(wrap_text=True, vertical='top')
CHECK = ['Correct value / status', 'PASS / FAIL / UNSURE', 'Comment (document, page, quote)']
COUNTS = []


def sheet(title, intro, header, data, widths):
    ws = wb.create_sheet(title)
    ws.cell(1, 1, intro).alignment = WR
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=min(len(header) + 3, 10)); ws.row_dimensions[1].height = 110
    H = ['#'] + header + CHECK
    for j, h in enumerate(H, 1):
        c = ws.cell(3, j, h); c.fill = HEAD; c.font = HF; c.alignment = WR
    for i, row in enumerate(data, 4):
        for j, v in enumerate([i - 3] + row, 1):
            ws.cell(i, j, v).alignment = WR
        for j in range(len(H) - 2, len(H) + 1):
            ws.cell(i, j).fill = YEL
    for j in range(1, len(H) + 1):
        ws.column_dimensions[get_column_letter(j)].width = 6 if j == 1 else widths.get(j - 1, 16)
    for j in range(len(H) - 2, len(H) + 1):
        ws.column_dimensions[get_column_letter(j)].width = 22 if j < len(H) else 60
    ws.freeze_panes = 'C4'; ws.auto_filter.ref = f'A3:{get_column_letter(len(H))}{3 + len(data)}'
    COUNTS.append((title, len(data)))


STD = ['Insurer', 'Product', 'UIN', 'Feature', 'Definition', 'v4 code', 'v4 value', 'Document', 'Page', 'Quote / evidence', 'PDFs']
W = {1: 16, 2: 30, 3: 12, 4: 24, 5: 40, 6: 8, 7: 40, 8: 18, 9: 6, 10: 50, 11: 40}

# A. Bharti claims (all feature rows)
A = []
for r in feat_rows:
    if not r[1]: continue
    A.append([r[0], r[1], r[2], r[5], r[6], r[10], r[11]])
sheet('A_Bharti_claims', 'A. Every feature row in v4, with the "Bharti" claim (column Bharti) and the counts. Is the Bharti claim right across the 7 Bharti ULIPs, and are the counts plausible? Many rows changed since your v3 QA: riders, coding rules, additions by basis, fund rows. Start with rows whose group ends in "(v4)" and the four rider rows (waiver_of_premium, critical_illness_inbuilt_or_option, accidental_death_extra, disability_benefit).',
      ['Group', 'Feature', 'Definition', 'Deep: has it (of 84)', 'Deep: type split', 'All ULIPs', 'Bharti claim'], A, {1: 18, 2: 28, 3: 50, 4: 12, 5: 18, 6: 12, 7: 60})

# B. Rider recoding, peers (every changed cell) plus a sample of unchanged R cells
B = []
seen = set()
for r in rider_ws:
    if not r or r[2] is None: continue
    u, f = r[2], r[3]
    if ins.get(u) == 'Bharti Life': continue
    seen.add((u, f))
    rb = RB.get(u, {})
    B.append([ins[u], name[u], u, f, DEF.get(f, ''), f'{r[4]} -> {r[5]}'] + cell(u, f)[1:] + [rb.get('riders_stored', ''), 'features/riders/<rider UIN>.json; docs/<insurer>/riders/<rider UIN>/'])
pool = [(u, f) for u in deep for f in ('waiver_of_premium', 'critical_illness_inbuilt_or_option', 'accidental_death_extra', 'disability_benefit')
        if PF.get((u, f), {}).get('code') == 'R' and (u, f) not in seen and ins[u] != 'Bharti Life']
for u, f in random.sample(pool, min(25, len(pool))):
    B.append([ins[u], name[u], u, f, DEF.get(f, ''), 'R (unchanged, sample)'] + cell(u, f)[1:] + [RB.get(u, {}).get('riders_stored', ''), 'features/riders/<rider UIN>.json; docs/<insurer>/riders/<rider UIN>/'])
sheet('B_rider_cells', 'B. Peer rider cells. Every cell the rider step changed, plus 25 random R cells it left alone. Check against the rider documents: does a rider this ULIP names (ULIP brochure or policy) give the benefit? Waiver must waive the ULIP premium, not only the rider\'s own. Accidental death must be an accident benefit, not only a term rider. Where a rider only waives on CI (SBI), critical illness is not "covered by rider".',
      ['Insurer', 'Product', 'UIN', 'Feature', 'Definition', 'Change', 'v4 value', 'Document', 'Page', 'Evidence', 'Riders stored', 'Where the rider documents are'], B, {1: 16, 2: 30, 3: 12, 4: 24, 5: 34, 6: 14, 7: 40, 8: 20, 9: 6, 10: 40, 11: 22, 12: 30})

# C. Additions by basis, all 84
Cc = []
for a in AB:
    u = a['uin']
    for key, lab in (('pct_of_premium', '% of premium'), ('pct_of_fund', '% of fund value')):
        Cc.append([ins[u], name[u], u, lab, a[key], a[key + '_conditions'], a[key + '_detail'][:500], a[key + '_doc'], a[key + '_page'], a[key + '_quote'][:400], a[key + '_method'], docs(u)])
sheet('C_additions_basis', 'C. Rule 2 (option b, user 5 Nov): additions are split by what they are a % of. "% of premium" = annualised, single, instalment or first-year premium, or a multiple of AP (amount known at the start). "% of fund value" = fund value or an average of it. Not counted: refunds of charges (own rows) and fund-floor top-ups (Tata, Axis "Cover Continuance Booster"). Check every product, both lines. Blank = no such addition in the deep data: search the policy document before agreeing. Also check the "Only for" conditions (women, online, staff, premium band, single pay).',
      ['Insurer', 'Product', 'UIN', 'Basis', 'v4 code', 'Only for', 'Detail', 'Document', 'Page', 'Quote', 'How S1 read it', 'PDFs'], Cc, {1: 16, 2: 30, 3: 12, 4: 14, 5: 8, 6: 18, 7: 50, 8: 16, 9: 6, 10: 40, 11: 18, 12: 40})

# D. Funds, all 84
D = []
for u in deep:
    for f in ('index_fund_offered', 'lowest_fmc_any_fund', 'lowest_fmc_equity_fund'):
        D.append([ins[u], name[u], u, f, DEF.get(f, '')] + cell(u, f) + [docs(u)])
sheet('D_funds', 'D. Rule 5: index fund offered, lowest FMC on any fund, lowest FMC on an equity fund. S1 took per-fund FMCs from the deep fund list (FMC_pct), which S2 sometimes filled with a default. Check against the fund table in the policy document or brochure. Equity fund = equity minimum of 60% or more; where the document gives no range, S1 used the fund name (method shown in the value): say if the fund is not an equity fund. Discontinued policy fund is excluded.',
      ['Insurer', 'Product', 'UIN', 'Feature', 'Definition', 'v4 code', 'v4 value', 'Document', 'Page', 'Quote', 'PDFs'], D, W)

# E. Other v4 changes (rules 1, 3, 4, scans, loose rows), every one
E = []
for c in CH:
    if c['rule_or_scan'].startswith(('rule 2', 'rule 5')): continue
    u, f = c['uin'], c['feature']
    E.append([c['insurer'], c['product'], u, f, DEF.get(f, ''), f"{c['code_before'] or 'blank'} -> {c['code_after'] or 'blank'}", c['rule_or_scan']] + cell(u, f)[1:] + [docs(u)])
sheet('E_rules_and_scans', 'E. Every other cell v4 changed: rule 1 (payor waiver needs the payer\'s own event as trigger), rule 3 (same loyalty design, same code), rule 4 (online or direct terms go to lower_charges_online; staff, women, family, auto-pay stay in customer_type_boosters), the scans (policy loan "not applicable", termination when the fund falls below a level, mortality as a % of IALM) and the loose v1 row "pension ULIP with guaranteed vesting", now read from the IRDAI description line. Scan hits say "to confirm".',
      ['Insurer', 'Product', 'UIN', 'Feature', 'Definition', 'Change', 'Rule or scan', 'v4 value', 'Document', 'Page', 'Quote', 'PDFs'], E, {1: 16, 2: 30, 3: 12, 4: 24, 5: 34, 6: 12, 7: 26, 8: 36, 9: 16, 10: 6, 11: 40, 12: 36})

# F. Peer sample for S3's v3 patterns that v4 did not scan
F = []
def pick(fs, cond, n, pat):
    pool = [(u, f) for u in deep if ins[u] != 'Bharti Life' for f in fs if cond(u, f)]
    for u, f in random.sample(pool, min(n, len(pool))):
        F.append([pat, ins[u], name[u], u, f, DEF.get(f, '')] + cell(u, f) + [docs(u)])
pick(['ppt_regular_pay'], lambda u, f: PF.get((u, f), {}).get('code') in ('N', '?'), 15, '4. Grid: regular pay = PPT equal to PT')
pick(['ppt_single_pay', 'ppt_limited_pay'], lambda u, f: PF.get((u, f), {}).get('code') in ('N', '?'), 10, '4. Grid: single or limited pay')
pick(['entry_age_max', 'maturity_age_max', 'entry_age_min'], lambda u, f: len(PF.get((u, f), {}).get('value', '')) > 60, 15, '5. Table columns read right')
pick(['admin_charge_waived_some_years'], lambda u, f: PF.get((u, f), {}).get('code') not in ('B',) and re.search(r'nil|0%', PF.get((u, 'policy_administration_charge'), {}).get('value', ''), re.I), 10, '3. In the policy bond, not the brochure')
pick(['restricted_withdrawals', 'min_fund_termination', 'mortality_as_ialm_share'], lambda u, f: PF.get((u, f), {}).get('code') == '', 15, '3. In the policy bond, not the brochure')
pick(['nri_available', 'riders_available', 'online_discount', 'tax_benefit_mention', 'child_payor_benefit'], lambda u, f: PF.get((u, f), {}).get('code') in ('Y', '-', ''), 15, '2. v1 keyword rows')
pick(['policy_loan'], lambda u, f: PF.get((u, f), {}).get('code') in ('?', ''), 10, '6. Policy loan still not stated')
pick(['top_up_premium', 'partial_withdrawal', 'free_switches_unlimited', 'premium_offset_or_holiday'], lambda u, f: PF.get((u, f), {}).get('code') in ('N',), 15, '7. "Not offered": does the document say so, or is it silence?')
sheet('F_peer_patterns', 'F. Random peer sample for your v3 error patterns that v4 did not scan. Pattern 4: regular pay means a PPT equal to the policy term; read the grid. Pattern 5: column labels in age tables (PPT vs DBM vs plan option). Pattern 3: features stated only in the policy bond. Pattern 2: v1 keyword rows. Pattern 6: policy loan on the CIS. Pattern 7 (new): "N" must mean the document says not available; silence is "?".',
      ['Pattern', 'Insurer', 'Product', 'UIN', 'Feature', 'Definition', 'v4 code', 'v4 value', 'Document', 'Page', 'Quote', 'PDFs'], F, {1: 24, 2: 16, 3: 30, 4: 12, 5: 24, 6: 34, 7: 8, 8: 40, 9: 16, 10: 6, 11: 40, 12: 36})

# Summary first
ws = wb.create_sheet('Summary', 0)
ws.column_dimensions['A'].width = 26; ws.column_dimensions['B'].width = 10
for c in 'CDE': ws.column_dimensions[c].width = 10
ws.column_dimensions['F'].width = 70
ws.cell(1, 1, 'Feature list v4 QA (S3). Brief: qa/s3_v4/s3_v4_qa_brief.md').font = Font(bold=True, size=13)
for j, h in enumerate(['Tab', 'Rows', 'PASS', 'FAIL', 'UNSURE', 'Notes'], 1):
    c = ws.cell(3, j, h); c.fill = HEAD; c.font = HF
for i, (t, n) in enumerate(COUNTS, 4):
    ws.cell(i, 1, t); ws.cell(i, 2, n)
    col = get_column_letter(len(wb[t][3]) - 1)
    for j, lab in zip((3, 4, 5), ('PASS', 'FAIL', 'UNSURE')):
        ws.cell(i, j, f'=COUNTIF({t}!{col}4:{col}{3 + n},"{lab}")')
    ws.cell(i, 6).fill = YEL
ws.cell(4 + len(COUNTS) + 1, 1, f'Total rows: {sum(n for _, n in COUNTS)}').font = Font(bold=True)
wb.save(os.path.join(R, 'qa/s3_v4/v4_qa_workbook.xlsx'))
print(COUNTS, sum(n for _, n in COUNTS))
