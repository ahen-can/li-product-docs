#!/bin/bash
# cmp.sh FILE: compact text with page markers
python3 -I - "$1" <<'P'
import sys,re
t=open(sys.argv[1],errors='ignore').read().split('\f')
for i,p in enumerate(t,1):
    s=re.sub(r'[ \t]+',' ',p); s=re.sub(r'\n\s*\n+','\n',s)
    print(f'@@ p{i}'); print(s)
P
