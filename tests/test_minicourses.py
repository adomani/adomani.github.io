#!/usr/bin/env python3
"""Self-check for scripts/minicourses.py against the real _data/minicourses.yml.

    python3 tests/test_minicourses.py
"""
import _helpers


def main():
    M, entries = _helpers.load('minicourses')
    tex = M.to_tex(entries)

    # Structure
    _helpers.assert_itemize(tex, len(entries))
    assert '{\\textbf{Minicourses}}' in tex

    # Every required field surfaces; url/links are website-only and must NOT leak
    for e in entries:
        assert '\\emph{' in tex
        assert M.tex_escape(e['venue']) in tex
    assert 'http' not in tex, 'url leaked into the CV (should be website-only)'
    assert 'programme' not in tex, 'extra link leaked into the CV'

    # Collaborators rendered as "with A and B"
    assert 'with Martin Bright and Ronald van Luijk' in tex

    # cv_only hides from the website only — the CV still lists the entry
    if any(e.get('cv_only') for e in entries):
        assert 'CIMPA' in tex, 'cv_only entry must still appear on the CV'

    # LaTeX escaping of specials
    assert M.tex_escape('a & b_c %d') == r'a \& b\_c \%d'

    print(f'PASS: minicourses.py renders {len(entries)} entries correctly')


if __name__ == '__main__':
    main()
