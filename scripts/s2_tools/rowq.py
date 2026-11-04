#!/usr/bin/env python3
"""rowq.py PDF PAGE REGEX [N]: print N layout lines from the first line matching REGEX on PAGE, joined into one quote
(spaces collapsed). The validator ignores whitespace, so a quote built this way matches the stored -layout text."""
import re, subprocess, sys
pdf, page, rx = sys.argv[1], sys.argv[2], sys.argv[3]; n = int(sys.argv[4]) if len(sys.argv) > 4 else 1
lines = subprocess.run(['pdftotext', '-layout', '-f', page, '-l', page, pdf, '-'], capture_output=True, text=True).stdout.splitlines()
lines = [l for l in lines if l.strip()]
for i, l in enumerate(lines):
    if re.search(rx, l):
        q = ' '.join(re.sub(r'\s+', ' ', x).strip() for x in lines[i:i + n])
        print(len(q), q); break
else: print('NO MATCH')
