#!/usr/bin/env python3
"""labels.py UIN: print the stored documents and their website labels as the JSON builder sees them."""
import sys; sys.path.insert(0, 'scripts')
import ulip_json
for o in ulip_json.inventory(sys.argv[1]):
    if o['stored_path']: print(repr(o['website_label']), o['doc_type'], o['stored_path'])
