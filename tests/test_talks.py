#!/usr/bin/env python3
"""Self-check for scripts/talks.py against the real _data/talks.yml.

    python3 tests/test_talks.py
"""
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
os.chdir(ROOT)
import talks as T  # noqa: E402


def main():
    entries = yaml.safe_load(open(T.DATA, encoding='utf-8'))
    tex = T.to_tex(entries)

    assert tex.startswith('% GENERATED')
    assert tex.count('\\item') == len(entries), 'item count mismatch'
    assert tex.rstrip().endswith('\\end{itemize}')

    # Every entry is either structured (title+date+venue) or verbatim text.
    for e in entries:
        if 'title' in e:
            assert 'date' in e and 'venue' in e, f'structured entry missing fields: {e}'
        else:
            assert 'text' in e, f'entry has neither title nor text: {e}'

    # Content spot-checks: a plain talk, a math title and an \href survive verbatim.
    assert '{\\emph{Metaprogramming in Lean}}' in tex
    assert '$\\overline{M}_{0,134}$' in tex          # math preserved for LaTeX
    assert '\\href{' in tex                           # slide link preserved

    print(f'PASS: talks.py renders {len(entries)} talks correctly')


if __name__ == '__main__':
    main()
