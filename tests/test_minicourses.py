#!/usr/bin/env python3
"""Self-check for scripts/minicourses.py against the real _data/minicourses.yml.

    python3 tests/test_minicourses.py
"""
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
os.chdir(ROOT)
import minicourses as M  # noqa: E402


def main():
    entries = yaml.safe_load(open(M.DATA, encoding='utf-8'))
    tex = M.to_tex(entries)

    # Structure
    assert tex.startswith('% GENERATED'), 'missing provenance header'
    assert '{\\textbf{Minicourses}}' in tex
    assert tex.count('\\item') == len(entries), 'item count mismatch'
    assert tex.rstrip().endswith('\\end{itemize}')

    # Every required field surfaces; url/links are website-only and must NOT leak
    for e in entries:
        assert '\\emph{' in tex
        assert M.tex_escape(e['venue']) in tex
    assert 'http' not in tex, 'url leaked into the CV (should be website-only)'
    assert 'programme' not in tex, 'extra link leaked into the CV'

    # Collaborators rendered as "with A and B"
    assert 'with Martin Bright and Ronald van Luijk' in tex

    # LaTeX escaping of specials
    assert M.tex_escape('a & b_c %d') == r'a \& b\_c \%d'

    print(f'PASS: minicourses.py renders {len(entries)} entries correctly')


if __name__ == '__main__':
    main()
