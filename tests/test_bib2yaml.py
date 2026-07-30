#!/usr/bin/env python3
"""Golden test for the bib -> yaml converter.

Renders tests/fixture.bib and compares against tests/expected.yml, so a change
to bib2yaml.py that alters output fails loudly. Regenerate the expected file
after an intentional change with:  python3 tests/test_bib2yaml.py --update
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'scripts'))
import bib2yaml  # noqa: E402

FIXTURE = os.path.join(HERE, 'fixture.bib')
EXPECTED = os.path.join(HERE, 'expected.yml')


def main():
    out, _ = bib2yaml.render_yaml(open(FIXTURE, encoding='utf-8').read())

    if '--update' in sys.argv:
        open(EXPECTED, 'w', encoding='utf-8').write(out)
        print('Updated', EXPECTED)
        return 0

    expected = open(EXPECTED, encoding='utf-8').read()
    if out == expected:
        print('PASS: converter output matches tests/expected.yml')
        return 0

    sys.stderr.write('FAIL: converter output differs from tests/expected.yml\n')
    import difflib
    diff = difflib.unified_diff(expected.splitlines(True), out.splitlines(True),
                                'expected.yml', 'actual')
    sys.stderr.writelines(diff)
    return 1


if __name__ == '__main__':
    sys.exit(main())
