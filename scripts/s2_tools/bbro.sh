#!/bin/bash
# bbro.sh UIN [maxlines]: brochure pages with eligibility or charge tables (layout text), for Bajaj-style brochures
u=$1; n=${2:-70}; B=$(ls docs/*/$u/brochure*.pdf | head -1)
np=$(pdfinfo "$B" | awk '/Pages/{print $2}')
for p in $(seq 1 $np); do t=$(pdftotext -f $p -l $p -layout "$B" - 2>/dev/null)
  echo "$t" | grep -qiE 'Eligibility|Entry Age|Charges under|Premium Allocation|Administration Charge|Mortality Charge|Discontinuance Charge' && { echo "=== $B p$p"; echo "$t" | grep -v '^\s*$' | cut -c1-165 | head -$n; }; done
