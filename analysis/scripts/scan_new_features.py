"""Search every deep-discovery product's policy document and brochure for each new-feature group.
Writes analysis/v3/new_feature_candidates.csv (one row per product x group: first match, doc, page, snippet).
A person (S1) then reviews each row and records Y/N in analysis/v3/new_feature_verdicts.csv.
Usage: python3 -I analysis/scripts/scan_new_features.py <repo>"""
import re, os, sys, glob, csv, json
R = sys.argv[1]
PAT = {
 'refund_fmc_or_all_charges': r'(return|refund)\w*\s+of\s+(the\s+)?(total\s+)?(fund management charges?|FMC)\b|(return|refund)\w*\s+of\s+all\s+(the\s+)?charges',
 'multiplied_charge_refunds': r'\b(2|3|two|three|double|twice)\s*(x|times)\b[^.]{0,60}(allocation|mortality|administration|guarantee) charges|\b(1[1-9]\d|[2-6]\d\d)\s*%\s+of\s+(the\s+)?(total\s+)?(premium allocation|mortality|policy administration|all) charges',
 'capital_or_vesting_guarantee': r'assured vesting benefit|capital guarantee|guaranteed (maturity|vesting) benefit|capital (protection|preservation) (option|guarantee)',
 'scheduled_guaranteed_additions': r'guaranteed additions?|guaranteed (wealth|fund) booster|special additions?',
 'customer_type_boosters': r'female (life|lives|customers?)[^.]{0,100}(additional|extra|booster)|existing (customer|policyholder)s?[^.]{0,60}(benefit|additional|booster|discount)|\bstaff\b[^.]{0,60}(charge|discount|allocation)|auto[- ]?debit booster|\bECS\b[^.]{0,60}(benefit|booster|additional)',
 'women_life_event_cover': r'pregnancy complication|congenital|female cancer|childbirth',
 'joint_life': r'\bjoint life\b',
 'decreasing_cover_option': r'decreasing (cover|sum assured|life cover)',
 'death_benefit_waiver_plus_income': r'(future|all) (due |remaining )?premiums?[^.]{0,80}(will be|shall be|are) (paid|funded|credited|invested) by (the company|us|the insurer)|family income benefit|waiver plus|premium funding benefit',
 'builtin_accident_or_payor_waiver': r'(in-?built|built-?in)[^.]{0,40}(accident|waiver|payor)|premium payor waiver|\bfamily benefit\b',
 'restricted_withdrawals': r'withdraw\w*.{0,250}(higher education|marriage of)|(higher education|marriage of).{0,250}partial withdraw',
 'premium_cap': r'maximum (annuali[sz]ed |annual |instalment )?premium\s*[:\-]?\s*(rs\.?|₹|inr)\s?[\d,]{5,}',
 'min_fund_termination': r'fund value.{0,80}(falls|less than|below).{0,80}terminat',
 'delayed_risk_start_minor': r'deferred risk|delayed risk|risk (cover )?(shall|will) (commence|start) (on|from) .{0,60}(birthday|attain)',
 'uk_pension_transfer': r'QROPS|QOPS',
 'mortality_rates_guaranteed': r'mortality charges?\s+(are|is|will be|shall be)\s+guaranteed|rates of mortality charges are guaranteed',
 'allocation_above_100': r'allocation rate.{0,60}10[1-9](\.\d+)?\s*%|additional allocation|extra allocation',
 'lower_charges_online': r'online[^.]{0,80}(lower|reduced|discount|booster|additional allocation)|digital[^.]{0,60}(booster|benefit)',
 'index_or_low_cost_funds': r'index fund|nifty\s*(\d+\s*)?(\w+\s*)?index\b',
 'settlement_enhancer': r'settlement[^.]{0,100}(enhancer|increase[ds]? by \d|additional \d)',
 'value_added_services': r'health management|wellness (program|benefit|service)|loyalty program',
 'mortality_as_ialm_share': r'\d+(\.\d+)?\s*%\s+of\s+(the\s+)?IALM|IALM\s*\(?2012',
 'cover_continuance_booster': r'cover continuance',
 'annuity_purchase_booster': r'annuity (purchase )?booster|booster[^.]{0,60}(purchase|buy)[^.]{0,20}annuity',
 'increasing_cover': r'(sum assured|cover)[^.]{0,40}(increase|step[- ]?up)s?\s+(by \d|every|each year)',
 'high_cover_multiple': r'\b([3-9]\d|1[0-2]\d)\s*(x|times)\s+(the\s+)?(of\s+)?annuali[sz]ed premium',
 'premium_step_up': r'save more tomorrow|premium[^.]{0,40}(increase|step[- ]?up)s?\s+(by \d|every year|each year)',
 'vesting_postponement': r'(postpone|defer|extend)\w*\s[^.]{0,40}vesting',
 'no_mortality_charge': r'no mortality charges?\b|mortality charges?\s*[:\-]\s*(nil|not applicable)',
}
deep = sorted(os.path.basename(f)[:-5] for f in glob.glob(os.path.join(R, 'features/ulip/*.json')))
rows = []
for u in deep:
    docs = []
    for t in sorted(glob.glob(os.path.join(R, 'text', '*', u, '*.txt'))):
        dt = os.path.basename(t)[:-4]
        if dt.startswith('cis'): continue
        pages = open(t, encoding='utf-8', errors='replace').read().split('\f')
        docs.append((0 if dt.startswith('policy') else 1, dt, [re.sub(r'\s+', ' ', p) for p in pages]))
    docs.sort()
    for g, rx in PAT.items():
        hit = None; n = 0
        for _, dt, pages in docs:
            for i, pg in enumerate(pages, 1):
                for m in re.finditer(rx, pg, re.I):
                    n += 1
                    if not hit:
                        s = max(0, m.start() - 120); hit = (dt, i, pg[s:m.end() + 160])
        if hit:
            rows.append({'uin': u, 'group': g, 'matches': n, 'doc': hit[0], 'page': hit[1], 'snippet': hit[2]})
os.makedirs(os.path.join(R, 'analysis/v3'), exist_ok=True)
with open(os.path.join(R, 'analysis/v3/new_feature_candidates.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, ['uin', 'group', 'matches', 'doc', 'page', 'snippet']); w.writeheader(); w.writerows(rows)
import collections as C
print(len(deep), 'products;', len(rows), 'candidate rows'); print(C.Counter(r['group'] for r in rows).most_common())
