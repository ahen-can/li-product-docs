"""Extract (uin, context text) blocks from a fetched page. Usage: extract.py file [prefix]
HTML: blocks = <tr>, <li>, <a>, <div>/<p> leaf text; PDF: lines. Prints uin \t text."""
import sys,re,html,subprocess
f=sys.argv[1]; pre=sys.argv[2] if len(sys.argv)>2 else r'\d{3}'
UIN=re.compile(r'('+pre+r')\s*([A-Z])\s*(\d{3})\s*V\s*(\d{2})')
def norm(s): return re.sub(r'\s+',' ',html.unescape(s)).strip()
out=[]
raw=open(f,'rb').read()
if raw[:4]==b'%PDF':
    t=subprocess.run(['pdftotext','-layout',f,'-'],capture_output=True,text=True).stdout
    for ln in t.split('\n'):
        for m in UIN.finditer(ln): out.append(('%s%s%sV%s'%m.groups(),norm(ln)))
else:
    t=raw.decode('utf-8','ignore')
    t=re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S|re.I)
    for tag in ('tr','li','a','p','h2','h3','h4','div','span','td'):
        for m in re.finditer(r'<%s\b[^>]*>(.*?)</%s>'%(tag,tag),t,re.S|re.I):
            inner=m.group(1)
            if '<'+tag in inner.lower() and tag in('div','li'): continue
            txt=norm(re.sub(r'<[^>]+>',' | ',inner)); txt=re.sub(r'(\s*\|\s*)+',' | ',txt).strip(' |')
            href=re.findall(r'href=["\']([^"\']+)["\']',m.group(0))
            for u in UIN.finditer(txt+' '+' '.join(href)):
                out.append(('%s%s%sV%s'%u.groups(),tag+': '+txt[:220]+(' [href '+href[0][:100]+']' if href else '')))
    # bare text fallback
    plain=norm(re.sub(r'<[^>]+>',' ',t))
    for m in UIN.finditer(plain): out.append(('%s%s%sV%s'%m.groups(),'text: '+plain[max(0,m.start()-120):m.end()+20]))
best={}
order=['tr','li','td','a','p','h2','h3','h4','span','div','text']
for u,c in out:
    k=next((i for i,o in enumerate(order) if c.startswith(o)),99) if not c.startswith(('tr','li')) or True else 0
    if raw[:4]==b'%PDF': k=0
    if u not in best or k<best[u][0]: best[u]=(k,c)
for u,(k,c) in best.items(): print(u+'\t'+c)
