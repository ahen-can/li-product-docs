#!/usr/bin/env python3
"""Set website_product_page_url for master_list rows by hand, after opening each URL (HTTP 200 required).
    python3 -I scripts/set_product_page.py 262=https://... 268=https://...
"""
import csv, subprocess, sys, time
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
M = list(csv.DictReader(open('master_list.csv'))); cols = list(M[0].keys())
want = dict(a.split('=', 1) for a in sys.argv[1:])
for r in M:
    if r['row_id'] in want:
        time.sleep(1)
        code = subprocess.run(['curl', '-sL', '-o', '/dev/null', '-w', '%{http_code}', '-m', '60', '-A', UA, want[r['row_id']]], capture_output=True, text=True).stdout
        print(r['row_id'], r['product_name'], code, want[r['row_id']])
        if code == '200': r['website_product_page_url'] = want[r['row_id']]
w = csv.DictWriter(open('master_list.csv', 'w', newline=''), fieldnames=cols); w.writeheader(); w.writerows(M)
