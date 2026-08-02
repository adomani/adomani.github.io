#!/usr/bin/env python3
"""Self-check for scripts/conferences.py against _data/conferences.yml.

    python3 tests/test_conferences.py
"""
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
os.chdir(ROOT)
import conferences as C  # noqa: E402


def main():
    entries = yaml.safe_load(open(C.DATA, encoding='utf-8'))
    tex = C.to_tex(entries)

    assert tex.startswith('% GENERATED')
    assert C.HEADING in tex
    assert tex.count('\\item') == len(entries), 'one \\item per conference'
    assert tex.rstrip().endswith('\\end{itemize}')

    for e in entries:
        assert e.get('text'), f'conference entry missing text: {e}'

    # Content spot-checks: the \href session and a plain \emph title survive.
    assert '\\href{https://icms-conference.org/2026/session5.html}' in tex
    assert '{\\emph{Frontiers of rationality}}' in tex

    print(f'PASS: conferences.py renders {len(entries)} conferences')


if __name__ == '__main__':
    main()
