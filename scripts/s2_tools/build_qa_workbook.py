"""Builds qa/s2/s2_qa_workbook.xlsx: S2's own QA of the walkthrough page (deliverable 08)
and the restyled deck (deliverable 09). Each row is one claim, with what it was checked
against and the result. Edit ROWS, then run: python3 -I scripts/s2_tools/build_qa_workbook.py <repo>"""
import sys, collections
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

P, D = "Page (08)", "Deck (09)"
F01 = "deliverables/01 Data tab (linked life + linked pension), recalculated"
F01L = "deliverables/01 Linked and Summary tabs, recalculated"
F01B = "deliverables/01 Bharti portfolio tab"
F02 = "deliverables/02 Products tab"
F05 = "deliverables/05 v3 (Features, Matrix tabs)"
F06 = "deliverables/06 (Returns, Comparison tabs)"
S3 = "analysis/bharti/bharti_findings_FY21_to_FY27.md (branch s3-bharti-analysis)"
S3Q = "qa/s3/s3_qa_workbook.xlsx (branch s3-bharti-analysis)"
USER = "Told to S2 by the user in chat; not in the repo"

# (doc, where, claim, checked against, result, status, action)
ROWS = [
# Market
(D,"Slide 3","Seven insurers' ULIP premium and shares (SBI 54,243 / 27.9% ... Axis Max 11,198 / 5.8%)",F01,"All seven match to the rupee crore; shares match to 0.1 point",  "PASS",""),
(D,"Slide 3","ULIP market is Rs 1.94 lakh cr",F01,"Linked life + linked pension = 194,147 cr","PASS",""),
(D,"Slide 3","Seven insurers write 84%",F01,"Top 7 = 84.1%. Top 6 = 78.3%, so 7 is the fewest that pass 80%","PASS",""),
(D,"Slide 3","Challengers ABSLI, Canara HSBC, Ageas = 13,932 cr, 7.2%",F01,"8,774 + 3,921 + 1,237 = 13,932; 7.2%","PASS",""),
(D,"Slide 3","Bharti 563 cr, 0.3%, rank 16",F01,"563 cr, 0.29%, rank 16 by this measure","PASS",""),
(D,"Slide 3","ULIP is 19.6% of the life industry; SBI's own book 54%; industry average about 20%",F01,"19.6%, 53.6%, 19.6%","PASS",""),
(P,"Section 1","Par 3.50 / Non-par 2.91 / Linked 1.77 / Pension and annuity 1.74 lakh cr; 35 / 29 / 18 / 18%",F01L,"349,897 / 290,505 / 177,229 / 174,455 cr; 35.3 / 29.3 / 17.9 / 17.6%","PASS",""),
(P,"Section 1","Bharti book mix 19 / 62 / 17 / 2%",F01L,"18.6 / 62.1 / 17.3 / 2.0%","PASS",""),
(P,"Section 1","Every insurer reconciles to its total premium",F01,"Sum of segments equals L-1 grand total for all 25 insurers (0 differences above Rs 1 cr)","PASS",""),
(P,"Section 1","Preview rows (SBI, ICICI, HDFC, LIC, Bharti) values, and row numbers 4, 5 to 8, 20",F01L,"All values and row numbers match","PASS",""),
(P,"Section 1","Note that Linked here is linked life; with linked pension the market is Rs 1.94 lakh cr",F01,"1.77 lakh cr + 16,917 cr linked pension = 1.94 lakh cr","PASS",""),
# Bharti
(D,"Slide 4","ULIP is 33% of FY26 individual new business, about Rs 309 cr of Rs 937 cr",F01B,"309.28 / 937.21 = 33.0% (L-22 p29 says 33.0%)","PASS",""),
(D,"Slide 4","Product table: Wealth Pro 81.6 / 79.1, Growth Shield Plus 79.6 / 53.8, Dream Shield Plus 50.9, others 97.2",F01B,"81.55 / 79.13; 79.58 / 53.84; 50.91; 97.24","PASS",""),
(D,"Slide 4","Shares of ULIP 26 / 26 / 16 / 31%",F01B,"26.4 / 25.7 / 16.5 / 31.4%. The rounded figures add to 99","PASS","Cosmetic: could show 26 / 26 / 16 / 31 with a rounding note"),
(D,"Slide 4","Linked NBP grew 90%; linked premium grew 48% to Rs 563 cr",S3+"; "+F01L,"89.6% (L-22); 48.4% on 562 cr linked life, 563 cr with pension","PASS",""),
(D,"Slide 9","Growth Shield Plus new business up 48%, Rs 53.8 cr to Rs 79.6 cr",F01B,"+47.8%","PASS",""),
(P,"Section 2","Portfolio table: 7 / 8 / 5 / 2 / 3 products; 212 / 211 / 44 / 38 / 0 cr; 23 / 22 / 5 / 4 / 0%; 433 not disclosed; 937 total",F01B,"All values match (22.6, 22.5, 4.7, 4.1; 432.5; 937.21)","PASS",""),
(P,"Section 2","Row numbers shown on the preview (104 to 111)",F01B,"Actual rows are 106 to 113","FAIL","Fixed on the page"),
(P,"Section 2","8 disclosed products are 54% of FY26 individual new business",F01B,"504.71 / 937.21 = 53.9%","PASS",""),
(P,"Section 2","Four of the 8 launched in FY25 or FY26",F01B,"Growth Shield Plus has FY25 sales; Dream Shield Plus, InstaGain and Guaranteed Bachat have none before FY26. Launch dates are inferred from blank earlier years, not read from a document","WARN","Confirm launch dates from the policy documents"),
(P,"Section 2","Guaranteed Wealth Pro fell from Rs 165 cr to Rs 113 cr in two years",F01B,"164.89 (FY24) to 113.23 (FY26)","PASS",""),
(P,"Section 2","ULIP is a third of new business, up from 13% in FY23",S3,"12.5% in FY23 is right, but it was 22.6% in FY21. Starting at the FY23 low makes the rise look larger","WARN","Add FY21 (23%) or say 'from 13% in FY23, after 23% in FY21'"),
(P,"Section 2","ULIP grew from about 10% to 17% of the book; par halved from 38% to 19%",S3,"Linked 11.3% (FY21), 9.7% (FY23), 17.3% (FY26). Par 38.2% to 18.6%","PASS",""),
(P,"Section 2","Policies fell 41% since FY21, ticket size doubled",S3,"116,831 to 69,123 (-41%); Rs 51,350 to Rs 1,20,865","PASS",""),
(P,"Section 2","Agency 45% to 14% of new business; Direct 45%",S3,"44.8% to 13.8%; Direct 17.1% to 44.5%","PASS",""),
(P,"Section 2","13th-month persistency 64.5%, second lowest of 14 insurers",S3,"64.5% FY26; only Shriram (60.9%) is lower","PASS",""),
(P,"Section 2","Expenses over the IRDAI limit FY21 to FY25; show-cause notice for FY25; 34% of premium vs proposed 15%; mostly operating cost",S3,"Breach every year FY21 to FY25; notice 15 Jan 2026; 34.2% on the closest basis, 26% non-commission; 15% within two years","PASS","Note S3's branch is not merged, so the link points to a branch"),
(P,"Section 2","Bharti has 25 products placed in a category",F01B,"7 + 8 + 5 + 2 + 3 = 25","PASS",""),
# Product list and brochures
(P,"Section 3","633 products; sources 511 Council, 64 official lists, 58 websites",F02,"633; 511; 38 ICICI + 26 Bharti = 64; 27 SBI + 31 Bajaj = 58","PASS",""),
(P,"Section 3","Preview rows 181, 259, 522",F02,"Rows match (Wealth Pro, Click 2 Retire Plus II, Smart Fortune Builder)","PASS",""),
(P,"Section 3","Shobhit checked 100 products: 4 UIN differences, 1 withdrawn",USER,"Cannot be checked until Shobhit's workbook is pushed","USER","Re-check when the QA workbook lands"),
(P,"Section 4","Funnel 633 to 527 to 516; four insurers block downloads",F02,"516 ok + 11 not found = 527; 106 manual (ICICI 38, Star Union 33, Kotak 30, Go Digit 5)","PASS",""),
(P,"Section 4","Shobhit opened 100 brochures: 4 UIN versions, 5 policy documents or leaflets, none for the wrong product",USER,"Cannot be checked until pushed","USER","Re-check when the QA workbook lands"),
(P,"Section 4","v1 table values 53 / 82 / 56 / 102 of 140; 38 / 59 / 40 / 73%; Bharti N / N / Y / Y",  "deliverables/04 ULIP tab","All match","PASS",""),
(P,"Section 4","v1 table row numbers 13, 25, 26, 29","deliverables/04 ULIP tab","Actual rows are 13, 27, 28, 31","FAIL","Fixed on the page"),
# Who to compare
(P,"Section 5","168 ULIPs on the list",F02,"168 rows with linked flag L","PASS",""),
(P,"Section 5 and Q2","Leaders SBI 27.9, ICICI 12.7, HDFC 12.5, LIC 11.8, Tata 7.2, Bajaj 6.2, Axis 5.8 = 84%",F01,"Match; sum 84.1%","PASS",""),
(P,"Q2","Challenger scores ABSLI 0.88, Canara HSBC 0.77, Ageas 0.66; weights 40 / 30 / 20 / 10","analysis/selection_framework.md","Scores and weights match. The 10% expert nomination is not applied for anyone, so the scores use only the first three factors","FAIL","Fixed on the page (added 'not applied yet')"),
(P,"Section 5","ICICI's 13 ULIPs are not in yet",F02,"13 ICICI ULIPs on the list, all 'manual' (blocked)","PASS",""),
# v3
(P,"Section 6","84 ULIPs; 65 fields each; document, page and quote",  "features/ulip/*.json","84 files; every file has the same 65 value fields, each with doc, page and quote keys","PASS",""),
(P,"Section 6","31 features not in v1; 353 corrections to v1",F05,"31 rows on New features tab; 353 data rows on v1 corrections","PASS",""),
(P,"Section 6 / Deck 5, 9","Only 4 of 84 ULIPs refund fund management charges; 2 are Bharti's",F05,"4 of 84: Grow Wealth Ultra, Wealth Maximizer + 2 others","PASS",""),
(P,"Section 6 / Deck 5","3 Bharti products return charges at a multiple",F05,"Dream Shield Plus, Growth Shield Plus, Wealth Maximizer (17 of 84 overall)","PASS",""),
(P,"Section 6 / Deck 5, 9","All 7 Bharti ULIPs allow unlimited free switches",F05+"; features/ulip/130L049V05.json","Future Invest allows 12 free switches a year, then Rs 100 each (policy bond p5). So 6 of 7","FAIL","Fixed on the page. Deck slides 5 and 9 still say 'All 7' (S1's wording): decision needed"),
(D,"Slide 5","Loyalty additions or wealth boosters: 58 of 84; Bharti '5 products'",F05,"58 matches both features. Bharti has loyalty additions in 6 of 7 (all but Future Invest) and boosters in 3","FAIL","Change Bharti to '6 products' or say which feature the row means"),
(D,"Slide 2","Waiver of premium: 43 of 84 have it, 'mostly as a rider'",F05,"11 built-in, 17 optional, 15 rider. Options are the largest group, not riders","FAIL","Fixed in the deck copy (09): now says built in, as an option or as a rider"),
(D,"Slide 5","Waiver 43; top-up 38; index funds 56; return of mortality 45; customer-type terms 27; guaranteed additions 20; multiples 17; continues after death 16; online terms 14; refund all charges 4",F05,"All counts match the Features tab","PASS",""),
(P,"Section 6","Bharti lacks top-ups (38 of 84 have them)",F05,"Six Bharti ULIPs are 'not stated' for top-ups and only Grow Wealth Ultra is 'not offered'. 'Lacks' is stronger than the evidence","WARN","Say 'none state top-ups' on page and deck slides 5, 6, 10"),
(P,"Section 6","Return of mortality charges: 5 of 7 Bharti; waiver none; guaranteed additions none",F05,"5 of 7; all 7 'N'; none","PASS",""),
(P,"Section 6","Bharti has 8 funds against 14 to 31 at the leaders",F05,"Bharti 6, 8, 8, 8, 8, 8, 10; leaders SBI 14, HDFC 17, Tata 31, Bajaj 31. '8 in most' is right (5 of 7)","PASS",""),
(P,"Section 6","Preview row numbers 9, 14, 71",F05,"Actual rows 26, 11, 77","FAIL","Fixed on the page (rows now in sheet order)"),
(P,"Section 5","141 ULIPs on sale in the landscape slide; 63 / 50 / 18 / 9 by type","deliverables/02 and 05","Types match (63, 50, 18, 9 = 140, plus 1 unclassified). The 141 is the v3 list: 139 brochures found, 1 not found, plus 1 Bajaj product with no UIN. 'Brochures found' is not exact","WARN","Reword the footnote: '141 ULIPs in the v3 list'"),
# Calculator and returns
(D,"Slide 8","Net yield for 13 products, shown as reductions in yield (1.04% ... 2.00%)",F06,"All 13 match the Returns tab","PASS",""),
(D,"Slide 8","Bharti Grow Wealth Ultra (Rs 2.5 lakh) 1.31%",F06,"Not in the Returns tab or anywhere in deliverable 06. The deck cites deliverable 06","FAIL","Add it to 06 with its inputs, or remove the bar"),
(D,"Slide 9","Growth Shield Plus and Wealth Maximizer cost about 1.0 to 1.1%, the lowest of the 13 calculated",F06,"1.04% and 1.08%; both lowest of the 13","PASS",""),
(D,"Slide 8 footer","Checked against insurer figures: Bharti x3, SBI eWealth, HDFC Click 2 (within 0.3%)",F06,"06 marks 4 as checked: Wealth Pro (0.3%), Wealth Maximizer (0.2%), SBI eWealth (0.15%), HDFC Click 2 (0.15%). Growth Shield Plus says 'not yet checked'. The third Bharti check is not in 06","FAIL","Reconcile with S1: which Bharti product is the third?"),
(P,"Sections 7 and 11","5 products hand-checked within 0.3%; 8 of 13 still to check",F06,"Same issue: 4 checked in 06, so 9 of 13 remain","WARN","Update once the third Bharti check is traced"),
(D,"Slide 11","Growth Shield Plus costs about 0.7% a year less than Wealth Pro",F06,"1.79% - 1.04% = 0.75%, so 'about 0.8%' on normal rounding. The term differs too (30 vs 20 years)","WARN","Say 'about 0.75%'"),
(D,"Slide 7","Head to head: allocation charge yr 1 9 / 9 / 6 / 12 / nil",F06+"; features/ulip/130L100V03.json","Wealth Pro 9% (other channels); SBI 9%; HDFC 6% (premium band 1 to 5 lakh); Tata 12%; Bajaj nil","PASS",""),
(D,"Slide 7","Admin charges",F06,"All five match, including Wealth Pro 0.15% yrs 1-5 then 0.45% yrs 6-10, nil from yr 11","PASS",""),
(D,"Slide 7","Returns of charges, waiver, top-ups, funds, net yield rows",F06,"All match. Net yield 6.21 / 6.00 / 6.21 / not published / 6.72","PASS",""),
(D,"Slide 7","Additions: SBI '5% of AP at maturity'",F06,"SBI pays 0% below Rs 1 lakh, 5% for Rs 1-2 lakh, 10% above. 5% is right for the standard customer (Rs 1 lakh a year) but is not stated as band-dependent","WARN","Add 'for Rs 1-2 lakh premium'"),
(D,"Slide 7","Additions: HDFC 'Loyalty 1.2% every 2nd yr from yr 11'","features/ulip/101L180V01.json","Policy document p11: 1.2% (annual mode), every alternate year from the end of year 11","PASS",""),
(D,"Slide 7","Wealth Pro boosters 0.25% yr 5, 1.25% at maturity",F06,"Match","PASS",""),
(D,"Slide 9","SBI Smart Fortune Builder allows 2 free switches a year, HDFC Sampoorn Nivesh Plus 4",F06,"Match","PASS",""),
(D,"Slide 2","Wealth Pro 6.21% at 8%, level with HDFC and ABSLI, behind Bajaj 6.72% and Canara 6.78%; newer designs 6.9%",F06,"6.21 / 6.21 / 6.20 / 6.72 / 6.78; 6.96 and 6.92","PASS",""),
(D,"Slide 10","Wealth Pro 1.79% against 1.22 to 1.28% at Canara and Bajaj",F06,"Match","PASS",""),
(D,"Slide 10","18 pension and 9 child ULIPs on the market; pension and annuity 2% of Bharti's book vs 18%",F01L+"; "+F02,"18 and 9; 1.96% vs 17.6%","PASS",""),
(D,"Slide 10 note","Five Bharti ULIPs end the policy if the fund falls below a floor; only 9 of 84 carry the clause",F05,"min_fund_termination: 9 of 84; Bharti: Dream Shield Plus, Grow Wealth, Growth Shield Plus, Wealth Maximizer, Wealth Pro = 5","PASS",""),
(D,"Slide 9 note","Bharti's linked conservation ratio fell to 74.4% in FY26 from 75.4%",S3,"S3 gives 84.4% (FY21) to 74.4% (FY26); the FY25 figure of 75.4% is not in S3's note","UNVERIFIED","Read L-22 in the FY25 PD"),
(D,"Slide 11 note","Wealth Pro has the most policies in force of Bharti's disclosed ULIPs",F01B,"The portfolio tab has new policies (Wealth Pro 3,459; Growth Shield Plus 4,034), not policies in force. Growth Shield Plus sold more new policies","FAIL","Remove, or say 'largest new business'"),
(D,"Slide 11","Item 2: pension ULIP with an assured vesting option; reference designs HDFC Click 2 Retire Plus II and SBI Retire Smart Plus",F05,"Only 2 of 84 products have a capital guarantee or assured vesting, and HDFC Click 2 Retire Plus II is one (Secure option, at least 101% of premiums plus 1% a year). SBI Retire Smart Plus has a 1.5% terminal addition at vesting, not an assured benefit","FAIL","Drop SBI Retire Smart Plus as a reference for assured vesting"),
(D,"Slide 11","Item 3: SBI Smart Scholar Plus has waiver of premium built in",F05,"Matrix: waiver B, built-in accident or payor waiver B","PASS",""),
(D,"Slide 12","ICICI is 12.7% of ULIP premium",F01,"12.73%","PASS",""),
# Method and QA
(P,"Section 9","Head-to-head table on the page equals the deck's",F06,"Same values","PASS",""),
(P,"Section 8","84 to 14 to 5; Bharti anchors; four largest private sellers with documents","analysis/ulip_selection.md","Matches the selection note","PASS",""),
(P,"Section 7","Calculator steps (premium in, monthly charges, fund growth, year-end additions, result)","calc/ and docs-internal/METHODS.md","Not re-read against the calculator code","UNVERIFIED","Read calc/ before sending"),
(P,"Section 10","S3 QA: 255 checks, 237 pass, 8 fail, 10 unsure",S3Q,"255 rows in total. The workbook now shows 233 pass, 7 fail, 9 unsure and 6 rows with no verdict. The counts have moved since the numbers were written","FAIL","Update the counts once S3 finalises; fix on the page"),
(P,"Section 10","QA caught that the disclosed products are 54%, not 90%, of FY26 new business",F01B,"53.9% (row 14); 90% was FY27 so far","PASS",""),
(P,"Section 10","Shobhit checked 200 items by hand",USER,"Not in the repo","USER","Re-check when the workbook lands"),
(P,"Section 10","Checker's name is Shobhit",  "qa/checker_guide.md (branch s3-bharti-analysis)","The guide says Rahul. The user said Shobhit and the page follows the user","WARN","Confirm the name with the user; update the guide if it is wrong"),
(P,"Section 12","Fix the 8 QA fails",S3Q,"7 fails in the current workbook (see section 10)","WARN","Update with the section 10 fix"),
(P,"Links","GitHub links in the page","git tree of origin/main and origin/s3-bharti-analysis","Deliverables 01, 02, 04, 05, 06, analysis/selection_framework.md exist on main. The Bharti trend workbook link points to the S3 branch","PASS","Links to 08 and 09 work only after this branch merges"),
(P,"Header","Nine steps; 2 minute overview; about 6 minute full read","The page","Nine step cards; overview is short; reading time not timed","UNVERIFIED","Time a read-through"),
]

BHARTI = [
(D,"Slides 2, 6, 7, 10, 11","Bharti has no waiver of premium in any form; 'Waiver: None / No'","Bharti brochures (text/bharti-life/130L*/brochure.txt); "+"Bharti rider literature (bhartiaxa.com/riders-in-insurance/linked-complete-shield-rider; sales literature and part B PDFs, 2024-09)","Six of the 7 Bharti brochures (all but Future Invest) list the Linked Complete Shield Rider (UIN 130A012V02). Its literature says 'The Waiver of Premium benefit is also available for event arising due ATPD, SCI and CCI-major conditions' and Part B has 'Additional Option: Waiver of Premium Benefit'. v3 codes Bharti 'N' for all 7 and counts peers' riders in the 43 (15 are riders), so the comparison is not like for like. The waiver is for disability and critical illness events, not for the death of a payor","FAIL","Fixed in the page and in deck slides 2, 6, 7, 10, 11 (now 'rider only'). v3 and v1 still say N: S1 to recode"),
(D,"Slide 6","Better terms for online purchase: Bharti None","features/ulip/130L100V03.json (policy bond p13); text/bharti-life/130L088V04/brochure.txt line 750","Wealth Pro allocation charge year 1 is 6.0% online against 9.0% other channels. Grow Wealth admin charge is 0.10% online against 0.15%. So 2 of 7 Bharti ULIPs have online terms. v3 'lower_charges_online' misses both","FAIL","Fixed in the page and deck. S1 to recode lower_charges_online for 130L100V03 and 130L088V04"),
(P,"Section 6","Bharti has no top-ups (38 of 84 have them)",F05+"; text/bharti-life/130L*/policy.txt","Only Grow Wealth Ultra says 'Top-up Premiums are not allowed' (policy p, item 15). The other six documents do not mention top-ups at all","WARN","Say 'not stated in six, not allowed in one'. Page now says this; deck slides 2, 6, 10 still say 'no top-ups'"),
(D,"Slide 6","Scheduled guaranteed additions: Bharti None (20 of 84)",F05+"; features/ulip/130L100V03.json","Wealth Pro adds 0.25% of fund value at end of year 5 and 1.25% at maturity. That is a fixed schedule, like Bajaj's Fund Booster (2% every 5 years) which S1 counted. S1 coded Wealth Pro's as a wealth booster, a separate feature","WARN","Ask S1 for the rule that separates 'wealth booster' from 'scheduled guaranteed addition'"),
(D,"Slide 6","Plan continues after death (16 of 84): Bharti None","text/bharti-life/130L*/{brochure,policy}.txt","Keyword search for premium funding by the company, family income and income benefit finds nothing in the 7 Bharti ULIPs","PASS",""),
(D,"Slides 6, 10","No pension or child ULIP (18 and 9 on the market)",F02,"Bharti's 7 ULIPs are all 'wealth' or 'return of mortality' types","PASS",""),
(D,"Slides 6, 10","Bharti has 8 funds against 14 to 31",F05,"Bharti 6, 8, 8, 8, 8, 8, 10 (plus the discontinued fund). Five of 7 have 8","PASS",""),
(D,"Slide 6 (v3)","Rider benefits coded per Bharti product: accidental death, critical illness, disability",F05+"; "+"Bharti brochures","The same rider is listed in 6 brochures but coded accidental death R in 4 of 7, critical illness R in 1 of 7 (Wealth Pro) and disability '-' in all 7. The rider covers accidental death, total and partial disability, standard and comprehensive critical illness and cancer for all six. Any 'Bharti lacks' on these rows is unreliable","FAIL","S1 to recode the rider-driven features for Bharti. Not used in the deck, but used in the 'lacks' logic"),
(D,"Slide 6 footnote","Shaded rows are features Bharti lacks that 14 or more peers have",F05,"After the fixes, waiver and online terms are no longer shaded. Still shaded: top-ups, guaranteed additions (borderline), continues after death, customer-type terms is Grow Wealth Ultra only","WARN","Re-run the shading after S1 recodes"),
]
ROWS = BHARTI + ROWS

def build(repo):
    wb = Workbook()
    ws = wb.active; ws.title = "Summary"
    cnt = collections.Counter(r[5] for r in ROWS)
    by = collections.defaultdict(collections.Counter)
    for r in ROWS: by[r[0]][r[5]] += 1
    ws.append(["S2 QA of the walkthrough page (deliverable 08) and deck (deliverable 09), 5 Nov 2026"])
    ws.append(["Each claim was traced back to a deliverable, a policy-document JSON or S3's notes. Status: PASS, FAIL (wrong or does not trace), WARN (true but misleading or imprecise), UNVERIFIED (not yet checked), USER (supplied verbally, not in the repo)."])
    ws.append([])
    ws.append(["Document","PASS","FAIL","WARN","UNVERIFIED","USER","Total"])
    for d in (P, D):
        c = by[d]; ws.append([d,c["PASS"],c["FAIL"],c["WARN"],c["UNVERIFIED"],c["USER"],sum(c.values())])
    ws.append(["All",cnt["PASS"],cnt["FAIL"],cnt["WARN"],cnt["UNVERIFIED"],cnt["USER"],len(ROWS)])
    ws.append([])
    ws.append(["Fails and warnings to settle before the page goes to Neha (see the Checks tab, Action column)"])
    for r in ROWS:
        if r[5] in ("FAIL","WARN"): ws.append([f"{r[5]}: {r[0]}, {r[1]}: {r[2][:110]}  ->  {r[6]}"])
    ws["A1"].font = Font(bold=True, size=13)
    for c in ws[4]: c.font = Font(bold=True)
    ws.column_dimensions["A"].width = 120
    ws2 = wb.create_sheet("Checks")
    hdr = ["ID","Document","Where","Claim as written","Checked against","What the source shows","Status","Action"]
    ws2.append(hdr)
    fills = {"PASS":"D8EAD3","FAIL":"F4C7C3","WARN":"FCE8B2","UNVERIFIED":"E0E0E0","USER":"CFE2F3"}
    for i, r in enumerate(ROWS, 1):
        ws2.append([f"Q{i:03d}", r[0], r[1], r[2], r[3], r[4], r[5], r[6]])
        ws2.cell(i+1, 7).fill = PatternFill("solid", fgColor=fills[r[5]])
    for c in ws2[1]: c.font = Font(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor="1F3864")
    for col, w in zip("ABCDEFGH", (7,11,16,55,38,62,12,40)): ws2.column_dimensions[col].width = w
    for row in ws2.iter_rows(min_row=2):
        for c in row: c.alignment = Alignment(wrap_text=True, vertical="top")
    ws2.freeze_panes = "A2"; ws2.auto_filter.ref = f"A1:H{len(ROWS)+1}"
    ws3 = wb.create_sheet("Bharti lacks audit")
    ws3.append(["Feature the deck says Bharti lacks","Peers with it (of 84)","What the deck says","What the Bharti documents show","Verdict"])
    for r in [
      ("Waiver of premium","43","None / No","Optional rider on 6 of 7 ULIPs (Complete Shield Rider 130A012V02)","Wrong: rider only"),
      ("Better terms for online purchase","14","None","Wealth Pro (online allocation charge) and Grow Wealth (online admin charge)","Wrong: 2 of 7 have it"),
      ("Top-up premiums","38","None / No","Not mentioned in 6 documents; Grow Wealth Ultra says not allowed","Overstated: not stated"),
      ("Scheduled guaranteed additions","20","None","Wealth Pro boosters at year 5 and maturity look like a fixed schedule","Borderline: rule needed"),
      ("Plan continues after death","16","None","Nothing found in the 7 documents","Holds"),
      ("Pension ULIP","18","None","No pension ULIP in the 7","Holds"),
      ("Child ULIP","9","None","No child ULIP in the 7","Holds"),
      ("Funds (8 vs 14 to 31)","n/a","8","6, 8, 8, 8, 8, 8, 10","Holds"),
      ("Unlimited free switches (Bharti has)","60","All 7","Future Invest: 12 a year, then Rs 100","Wrong: 6 of 7"),
      ("Loyalty additions or boosters (Bharti has)","58","5 products","Loyalty additions in 6 of 7; boosters in 3","Wrong: 6 products"),
    ]: ws3.append(list(r))
    for c in ws3[1]: c.font = Font(bold=True)
    for col, w in zip("ABCDE", (38,18,22,70,26)): ws3.column_dimensions[col].width = w
    out = f"{repo}/qa/s2/s2_qa_workbook.xlsx"
    wb.save(out); print(out, dict(cnt), len(ROWS))

if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else ".")
