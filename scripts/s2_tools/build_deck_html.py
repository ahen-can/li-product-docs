"""Builds deliverables/09_ulip_pilot_deck.html from the slide sources in
docs-internal/s2_neha_walkthrough/deck/project. Run from the repo root."""
import json, re
P = 'docs-internal/s2_neha_walkthrough/deck/project'
d = json.load(open(f'{P}/deck.json'))
secs = [re.sub(r'<aside>.*?</aside>', '', open(f'{P}/slides/{s}.html').read(), flags=re.S) for s in d['order']]
html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{d["title"]}</title>
<link href="https://fonts.googleapis.com/css2?family=Public+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#2B2F36;padding:24px 0}}
.wrap{{width:min(1920px,calc(100vw - 32px));aspect-ratio:16/9;margin:0 auto 24px;position:relative;overflow:hidden;box-shadow:0 2px 12px rgba(0,0,0,.4)}}
.wrap>section{{width:1920px;height:1080px;position:absolute;top:0;left:0;transform-origin:0 0}}
ul{{padding-left:1.2em}}
@media print{{body{{background:none;padding:0}}.wrap{{width:100vw;margin:0;box-shadow:none;page-break-after:always}}}}
</style></head><body>
{"".join(f'<div class="wrap">{s}</div>' for s in secs)}
<script>
function fit(){{document.querySelectorAll('.wrap').forEach(w=>{{w.firstElementChild.style.transform='scale('+(w.clientWidth/1920)+')'}})}}
addEventListener('resize',fit);fit();
</script></body></html>'''
open('deliverables/09_ulip_pilot_deck.html', 'w').write(html)
