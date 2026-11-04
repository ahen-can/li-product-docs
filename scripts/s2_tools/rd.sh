#!/bin/bash
# rd.sh PDF FIRST LAST [maxchars] : compact reading-order text per page, skipping boilerplate pages
f=$1; a=$2; b=$3; n=${4:-6000}
for p in $(seq $a $b); do t=$(pdftotext -f $p -l $p "$f" - 2>/dev/null | tr -s ' \n' ' '); c=$(echo "$t" | grep -oiE 'ombudsman|section 45|section 39|section 38|assignment' | wc -l); [ $c -ge 3 ] && { echo "=== p$p (boilerplate, skipped)"; continue; }; echo "=== p$p"; echo "$t" | cut -c1-$n; done
