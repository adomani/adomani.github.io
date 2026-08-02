#!/usr/bin/env python3
"""Generate the CV's Teaching institution tables from _data/teaching.yml.

    python3 scripts/teaching.py --tex cv/sections/teaching_generated.tex
    python3 scripts/teaching.py --check      # verify the .tex is in sync

The data is a list of institutions, each with an ordered list of courses:

    - institution: Warwick
      courses:
        - {period: "2026-27, Term 1", course: "MA4N1 Theorem Proving with Lean"}
        - ...

`period` and `course` are emitted verbatim into a two-column tabular, so they
may contain LaTeX. One source, rendered into the CV; see scripts/README.md.
"""
import _common

DATA = '_data/teaching.yml'
HEADER = _common.header('teaching.py', DATA)
COLSPEC = '{@{\\textendash \\hspace{3pt}}l@{ -- }l}'


def render_institution(inst):
    rows = []
    courses = inst['courses']
    for i, c in enumerate(courses):
        last = i == len(courses) - 1
        suffix = '' if last else ' \\\\'
        rows.append(f"{c['period']} &\n{c['course']}{suffix}")
    body = '\n'.join(rows)
    return (
        '\\item\n'
        f"{{\\textbf{{{inst['institution']}}}}}\\\\[3pt]\n"
        f"\\begin{{tabular}}{COLSPEC}\n"
        f"{body}\n"
        '\\end{tabular}'
    )


def to_tex(data):
    items = '\n'.join(render_institution(inst) for inst in data)
    return HEADER + '\\begin{itemize}\n' + items + '\n\\end{itemize}\n'


def render():
    data = _common.load(DATA)
    return to_tex(data), len(data)


if __name__ == '__main__':
    raise SystemExit(_common.cli(render, noun='institutions'))
