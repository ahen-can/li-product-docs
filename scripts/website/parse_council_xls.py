"""Parse Life Council xls (HTML table export). Usage: parse_council_xls.py in.xls out.csv"""
import sys,re,html,csv,collections
t=open(sys.argv[1],encoding='utf-8',errors='ignore').read()
def cells(r): return [re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',c))).strip() for c in re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>',r,re.S)]
UIN=re.compile(r'^\d{3}[A-Z]\d{3}V\d{2}$')
ins=None; sec=None; out=[]; started=False
for r in re.findall(r'<tr[^>]*>(.*?)</tr>',t,re.S):
    c=cells(r)
    if not c: continue
    j=' '.join(c)
    if 'Name of the Products' in j: sec='Products'; started=True; continue
    if 'Name of the Riders' in j: sec='Riders'; started=True; continue
    if len(c)>=4 and UIN.match(c[3].replace(' ','')):
        out.append({'insurer':ins,'section':sec,'name':c[0],'lob':c[1],'category':c[2],'uin':c[3].replace(' ','')}); continue
    nonempty=[x for x in c if x]
    if len(nonempty)==1 and re.search(r'Limited|Corporation Of India|Ltd',nonempty[0]) and not UIN.match(nonempty[0]):
        ins=nonempty[0]
with open(sys.argv[2],'w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['insurer','section','name','lob','category','uin']); w.writeheader(); w.writerows(out)
P=[o for o in out if o['section']=='Products' and o['lob']=='Individual']
print('rows',len(out),'individual products',len(P),'no-insurer',sum(1 for o in out if not o['insurer']))
