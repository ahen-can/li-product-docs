"""Build candidate product-page URLs per insurer from sitemaps + listing-page links.
Usage: candidates.py <S> -> writes <S>/sites/<slug>/product_candidates.txt, prints counts"""
import sys,os,re,glob,json,urllib.parse
S=sys.argv[1]
INC=re.compile(r'plan|insurance|ulip|saving|pension|retire|child|term|invest|protect|annuity|money-?back|product|wealth|income|bima|shield|guarant|endow|smart|click|policy',re.I)
EXC=re.compile(r'knowledge|blog|article|calculator|faq|glossary|news|media|press|career|investor|claim|form|download|help|service|login|contact|about|branch|fund-?perf|nav|tax|nri-|/hi/|/hindi|/mr/|/ta/|/te/|/kn/|/gu/|/bn/|/ml/|/or/|/pa/|guide|learn|library|/what-is|/how-|/why-|/best-|/types-of|difference|-vs-|benefits-of|features-of|crore|lakh|year-|years|-in-your|for-women|for-parents|for-housewife|senior|self-employed|heart|compar|/tag/|/category/|/author/|amp$|\.pdf$|\.xml$|group|health|micro|rider|webstories|web-stories|podcast|video|event|award|csr|sitemap|grievance|disclos|ombuds|privacy|terms-and|disclaim|cookie|unclaimed|fraud|nominat|surrender|premium-pay|renew|status|tracker',re.I)
for d in sorted(glob.glob(f'{S}/sites/*/')):
    slug=d.rstrip('/').split('/')[-1]; urls=set(); host=None
    for f in glob.glob(d+'text/*.json'):
        r=json.load(open(f))
        if 'current' in r['type']:
            host=host or urllib.parse.urlparse(r['final_url'] or r['url']).netloc
            urls|={u for u,_ in r['links']}
    for f in glob.glob(d+'sitemap.xml')+glob.glob(d+'sm_*.xml'):
        urls|=set(re.findall(r'<loc>\s*([^<\s]+)\s*</loc>',open(f,errors='ignore').read()))
    out=set()
    for u in urls:
        p=urllib.parse.urlparse(u)
        if host and p.netloc and p.netloc.replace('www.','')!=host.replace('www.',''): continue
        path=p.path.rstrip('/')
        if path.count('/')<2 and not re.search(r'plan|ulip|bima|shield|smart|click',path.split('/')[-1] if path else '',re.I): continue
        if not INC.search(path) or EXC.search(path): continue
        out.add(p.scheme+'://'+p.netloc+path)
    open(d+'product_candidates.txt','w').write('\n'.join(sorted(out)))
    print(f'{slug:18} {len(out)}')
