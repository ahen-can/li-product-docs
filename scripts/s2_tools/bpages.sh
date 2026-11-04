#!/bin/bash
# bpages.sh UIN : brochure eligibility and charges pages (layout), Bajaj style
u=$1; B=$(ls docs/*/$u/brochure*.pdf | head -1); np=$(pdfinfo "$B" | awk '/Pages/{print $2}')
for p in $(seq 1 $np); do t=$(pdftotext -f $p -l $p -layout "$B" - 2>/dev/null)
  echo "$t" | grep -qE 'Eligibility (Table|Parameters|Criteria)|Charges under|Premium Allocation  |Charges *$' && { echo "=== p$p"; echo "$t" | grep -v '^\s*$' | sed -n '3,80p' | cut -c1-165; }; done
