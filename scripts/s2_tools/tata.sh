#!/bin/bash
# tata.sh UIN [from-regex] [to-regex] : reading-order text of a Tata policy between two headings, one paragraph stream
u=$1; f=docs/tata-aia/$u/policy.pdf; a=${2:-'PART C'}; b=${3:-'PART E'}
pdftotext $f - | awk -v a="$a" -v b="$b" '$0 ~ a {on=1} on && $0 ~ b && NR>1 && seen {exit} on {print; seen=1}' | grep -v '^\s*$' | grep -v "(UIN: $u)\|IRDA of India Regn" | tr '\n' ' ' | fold -w 230
