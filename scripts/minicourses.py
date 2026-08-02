#!/usr/bin/env python3
"""Generate the CV's Minicourses LaTeX block from the shared data file.

    _data/minicourses.yml   (canonical; also read directly by the website)
        └── scripts/minicourses.py --tex ─▶ a LaTeX itemize for the CV

The website renders the same YAML itself (Jekyll), so both the CV and the
website page come from one source. `url` and `links` are website-only (the CV
lists minicourses as plain text, matching its existing style).

    python3 scripts/minicourses.py --out cv/sections/minicourses_generated.tex
    add --check to compare against an existing file instead of writing.
"""
import _common

DATA = '_data/minicourses.yml'
HEADER = _common.header('minicourses.py', DATA)


def tex_escape(s):
    for a, b in (('\\', r'\textbackslash '), ('&', r'\&'), ('%', r'\%'),
                 ('#', r'\#'), ('_', r'\_'), ('~', r'\textasciitilde ')):
        s = s.replace(a, b)
    return s


def join_people(names):
    names = [tex_escape(n) for n in names]
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return f'{names[0]} and {names[1]}'
    return ', '.join(names[:-1]) + ', and ' + names[-1]


def render_item(e):
    parts = [f"{e['year']}, {tex_escape(str(e['date']))}",
             r'{\emph{' + tex_escape(e['title']) + '}}']
    if e.get('context'):
        parts.append(tex_escape(e['context']))
    if e.get('collaborators'):
        parts.append('with ' + join_people(e['collaborators']))
    parts.append(tex_escape(e['venue']))
    return '\\item\n' + ', '.join(parts) + '.'


def to_tex(entries):
    items = '\n'.join(render_item(e) for e in entries)
    return (HEADER + '{\\textbf{Minicourses}}\n\\begin{itemize}\n'
            + items + '\n\\end{itemize}\n')


def render():
    entries = _common.load(DATA)
    return to_tex(entries), len(entries)


if __name__ == '__main__':
    raise SystemExit(_common.cli(render, noun='minicourses'))
