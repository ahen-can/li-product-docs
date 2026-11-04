#!/bin/bash
# bajaj_one.sh UIN : brochure key pages (eligibility, charges, benefits) + policy facts (strategies, withdrawals, mortality page), Bajaj style
u=$1; B=$(ls docs/bajaj-life/$u/brochure*.pdf | head -1); P=docs/bajaj-life/$u/policy.pdf
np=$(pdfinfo "$B" | awk '/Pages/{print $2}')
for p in $(seq 1 $np); do t=$(pdftotext -f $p -l $p -layout "$B" - 2>/dev/null)
  echo "$t" | grep -qE 'Eligibility (Table|Parameters|Criteria)|Product at a Glance|Charges under the Plan|Charges Under the Plan|Loyalty Addition|Booster|Return of Mortality|Death Benefit|Key (Advantages|Features)' || continue
  echo "=== brochure p$p"; echo "$t" | grep -v '^\s*$' | sed -n '3,78p' | grep -viE 'illustrat|assumed return|^ *(Of|At) [48]%|Scenario|years old' | cut -c1-165; done
if [ -f $P ]; then echo "=== policy"; X=$(pdftotext $P - | tr '\n' ' ' | tr -s ' ')
  echo "$X" | grep -oE '(minimum amount of Partial Withdrawal.{0,60}|maximum amount of Partial Withdrawal.{0,110}|should not fall below.{0,100}|must have a minimum balance.{0,100}|[a-d]\) [A-Z][A-Za-z ]+ Portfolio Strategy Or|Revival Period” means.{0,90}|unlimited free switch[^.]*|hike-up is called the [A-Za-z ]+|Systematic Partial Withdrawal \(SPW\) i\).{0,250})' | sort -u | cut -c1-300
  for p in $(seq 15 60); do t=$(pdftotext -f $p -l $p $P - 2>/dev/null); [ -z "$t" ] && break; echo "$t" | grep -q 'Mortality Charge[s]* *$\|Standard Mortality\|Per .000 Sum at Risk' && echo "mortality table p$p"; done; fi
