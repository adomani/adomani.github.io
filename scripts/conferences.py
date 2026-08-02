#!/usr/bin/env python3
"""Generate the CV's "Organized conferences" list from _data/conferences.yml.

    python3 scripts/conferences.py --out cv/sections/conferences_generated.tex
    python3 scripts/conferences.py --out <path> --check   # verify it is in sync

The four entries are heterogeneous (an \\href session title, plain \\emph
titles, differing "with ... venue ... dates" phrasing), so each is stored as one
verbatim `text` line and emitted as-is -- the same approach as the irregular
talks entries. One source, rendered into the CV; see scripts/README.md.
"""
import _common

DATA = '_data/conferences.yml'
HEADER = _common.header('conferences.py', DATA)
HEADING = '{\\textbf{Organized conferences}}'


def to_tex(entries):
    items = '\n'.join('\\item\n' + e['text'] for e in entries)
    return (HEADER + HEADING + '\n\\begin{itemize}\n' + items
            + '\n\\end{itemize}\n')


def render():
    entries = _common.load(DATA)
    return to_tex(entries), len(entries)


if __name__ == '__main__':
    raise SystemExit(_common.cli(render, noun='conferences'))
