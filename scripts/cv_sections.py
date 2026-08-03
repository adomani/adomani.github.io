#!/usr/bin/env python3
"""The CV's LaTeX \\begin{itemize} sections, each generated from a YAML list.

Four sections share one envelope (_common.itemize); only the per-entry rendering
differs. scripts/build.py lists the outputs and is the entry point; preview one
section with `python3 scripts/build.py talks`.

Fields may hold LaTeX and are emitted verbatim (minicourses escape their plain
text; the others were bootstrapped from the old hand-written .tex and proven to
render byte-for-byte identically). See scripts/README.md.
"""
import _common


# ---- Minicourses (_data/minicourses.yml) --------------------------------
MINICOURSES = '_data/minicourses.yml'


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


def _minicourse_item(e):
    parts = [f"{e['year']}, {tex_escape(str(e['date']))}",
             r'{\emph{' + tex_escape(e['title']) + '}}']
    if e.get('context'):
        parts.append(tex_escape(e['context']))
    if e.get('collaborators'):
        parts.append('with ' + join_people(e['collaborators']))
    parts.append(tex_escape(e['venue']))
    return '\\item\n' + ', '.join(parts) + '.'


def minicourses_tex(entries):
    # url/links/collaborators are website-only; the CV lists plain text.
    items = '\n'.join(_minicourse_item(e) for e in entries)
    return _common.itemize(_common.header('cv_sections.py', MINICOURSES),
                           items, lead='\\section{Minicourses}\n')


# ---- Talks (_data/talks.yml) --------------------------------------------
TALKS = '_data/talks.yml'


def talk_line(e):
    if 'title' not in e:                 # heterogeneous entry: verbatim CV line
        return e['text']
    title = _common.md_to_tex(e['title'])           # fields are Markdown
    venue = _common.md_to_tex(e['venue'])
    if e.get('slides'):
        # Drop a trailing '.' so "..., online." doesn't become "online., \href..".
        return (f"{e['year']}, {e['date']}, {{\\emph{{{title}}}}}, "
                f"{venue.rstrip('.')}, \\href{{{e['slides']}}}{{slides}}.")
    return f"{e['year']}, {e['date']}, {{\\emph{{{title}}}}}, {venue}"


def talks_tex(entries):
    cv = [e for e in entries if not e.get('web_only')]   # web_only -> /slides/ only
    items = '\n'.join('\\item\n' + talk_line(e) for e in cv)
    return _common.itemize(_common.header('cv_sections.py', TALKS), items)


# ---- Teaching tables (_data/teaching.yml) -------------------------------
TEACHING = '_data/teaching.yml'
COLSPEC = '{@{\\textendash \\hspace{3pt}}l@{ -- }l}'


def _institution(inst):
    courses = inst['courses']
    rows = []
    for i, c in enumerate(courses):
        suffix = '' if i == len(courses) - 1 else ' \\\\'
        rows.append(f"{c['period']} &\n{c['course']}{suffix}")
    body = '\n'.join(rows)
    return (
        '\\item\n'
        f"{{\\textbf{{{inst['institution']}}}}}\\\\[3pt]\n"
        f"\\begin{{tabular}}{COLSPEC}\n"
        f"{body}\n"
        '\\end{tabular}'
    )


def teaching_tex(data):
    items = '\n'.join(_institution(inst) for inst in data)
    return _common.itemize(_common.header('cv_sections.py', TEACHING), items)


# ---- Organized conferences (_data/conferences.yml) ----------------------
CONFERENCES = '_data/conferences.yml'
CONF_HEADING = '\\section{Organized conferences}'


def conferences_tex(entries):
    items = '\n'.join('\\item\n' + _common.md_to_tex(e['text']) for e in entries)
    return _common.itemize(_common.header('cv_sections.py', CONFERENCES),
                           items, lead=CONF_HEADING + '\n')


# ---- registry + CLI -----------------------------------------------------
SECTIONS = {
    'minicourses': (MINICOURSES, minicourses_tex),
    'talks':       (TALKS,       talks_tex),
    'teaching':    (TEACHING,    teaching_tex),
    'conferences': (CONFERENCES, conferences_tex),
}


def render(section):
    """The LaTeX for one section — used by scripts/build.py."""
    data_path, to_tex = SECTIONS[section]
    return to_tex(_common.load(data_path))
