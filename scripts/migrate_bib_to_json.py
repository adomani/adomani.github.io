#!/usr/bin/env python3
"""One-time migration that produced _bibliography/publications.json from the
old canonical papers.bib. Kept for provenance; the JSON is canonical now.
Descriptions were added afterwards from the hand-written papers page.

    python3 scripts/migrate_bib_to_json.py papers.bib publications.json
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bib2yaml as B  # noqa: E402


def main():
    src, dst = sys.argv[1], sys.argv[2]
    records = []
    for e in B.parse_bib(open(src, encoding='utf-8').read()):
        fields = {k: v for k, v in e.items() if not k.startswith('__')}
        author = fields.pop('author', '')
        records.append({
            'key': e['__key__'],
            'type': e['__type__'],
            'author': B.re.split(r'\s+and\s+', author.strip()) if author else [],
            'keywords': fields.pop('keywords', ''),
            'fields': fields,
        })
    json.dump(records, open(dst, 'w', encoding='utf-8'),
              ensure_ascii=False, indent=2)
    print(f'Wrote {len(records)} entries to {dst}')


if __name__ == '__main__':
    main()
