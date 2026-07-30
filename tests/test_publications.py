#!/usr/bin/env python3
"""Golden test for the JSON -> {yaml, bib} generator.

Renders tests/fixture.json through publications.py and compares against
tests/expected.yml and tests/expected.bib. Regenerate the expected files
after an intentional change with:  python3 tests/test_publications.py --update
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'scripts'))
import publications as P  # noqa: E402

FIXTURE = os.path.join(HERE, 'fixture.json')
EXP_YAML = os.path.join(HERE, 'expected.yml')
EXP_BIB = os.path.join(HERE, 'expected.bib')


def main():
    entries = json.load(open(FIXTURE, encoding='utf-8'))
    got = {EXP_YAML: P.to_yaml(entries), EXP_BIB: P.to_bib(entries)}

    if '--update' in sys.argv:
        for path, text in got.items():
            open(path, 'w', encoding='utf-8').write(text)
        print('Updated', ', '.join(os.path.basename(p) for p in got))
        return 0

    import difflib
    ok = True
    for path, text in got.items():
        expected = open(path, encoding='utf-8').read()
        if text == expected:
            continue
        ok = False
        sys.stderr.write(f'FAIL: {os.path.basename(path)} differs\n')
        sys.stderr.writelines(difflib.unified_diff(
            expected.splitlines(True), text.splitlines(True),
            os.path.basename(path) + '.expected', 'actual'))
    if ok:
        print('PASS: JSON -> yaml and JSON -> bib match the golden files')
        return 0
    return 1


if __name__ == '__main__':
    sys.exit(main())
