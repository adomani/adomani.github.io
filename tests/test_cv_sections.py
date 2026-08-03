#!/usr/bin/env python3
"""Self-checks for scripts/cv_sections.py (minicourses, talks, teaching,
organized conferences) against the real _data/*.yml.

    python3 tests/test_cv_sections.py
"""
import _helpers

import cv_sections as CV


def check_minicourses():
    entries = _helpers.read(CV.MINICOURSES)
    tex = CV.minicourses_tex(entries)
    _helpers.assert_itemize(tex, len(entries))
    assert '\\section{Minicourses}' in tex

    for e in entries:                       # url/links are website-only
        assert '\\emph{' in tex
        assert CV.tex_escape(e['venue']) in tex
    assert 'http' not in tex, 'url leaked into the CV (should be website-only)'
    assert 'programme' not in tex, 'extra link leaked into the CV'
    assert 'with Martin Bright and Ronald van Luijk' in tex
    if any(e.get('cv_only') for e in entries):
        assert 'CIMPA' in tex, 'cv_only entry must still appear on the CV'
    assert CV.tex_escape('a & b_c %d') == r'a \& b\_c \%d'
    return f'{len(entries)} minicourses'


def check_talks():
    entries = _helpers.read(CV.TALKS)
    tex = CV.talks_tex(entries)

    # web_only entries appear on /slides/ but not in the CV talks list.
    n_cv = sum(1 for e in entries if not e.get('web_only'))
    _helpers.assert_itemize(tex, n_cv)
    for e in entries:
        if 'title' in e:
            assert 'venue' in e, f'structured entry missing venue: {e}'
            if not e.get('web_only'):
                assert 'date' in e, f'CV entry missing date: {e}'
        else:
            assert 'text' in e, f'entry has neither title nor text: {e}'
        if e.get('web_only'):
            assert e['title'] not in tex, f'web_only leaked into CV: {e["title"]}'

    assert '{\\emph{Metaprogramming in Lean}}' in tex
    assert '$\\overline{M}_{0,134}$' in tex          # math preserved for LaTeX
    slides = [e for e in entries if e.get('slides') and not e.get('web_only')]
    assert slides, 'expected at least one CV talk with a slides field'
    for e in slides:
        assert f"\\href{{{e['slides']}}}{{slides}}." in tex
        assert '{slides}' not in e['venue'], f'inline slides href in venue: {e}'
    return f'{len(entries)} talks'


def check_teaching():
    data = _helpers.read(CV.TEACHING)
    tex = CV.teaching_tex(data)
    _helpers.assert_itemize(tex, len(data))          # one \item per institution
    for inst in data:
        assert inst.get('institution'), f'institution missing name: {inst}'
        assert inst.get('courses'), f'{inst["institution"]} has no courses'
        for c in inst['courses']:
            assert 'period' in c and 'course' in c, f'bad course row: {c}'
    assert tex.count('\\begin{tabular}') == len(data)
    assert tex.count(CV.COLSPEC) == len(data)
    assert '{\\textbf{Warwick}}' in tex and '{\\textbf{MIT}}' in tex
    assert '\\emph{Using computers to do maths for us!}' in tex
    n_courses = sum(len(i['courses']) for i in data)
    return f'{len(data)} institutions, {n_courses} courses'


def check_conferences():
    entries = _helpers.read(CV.CONFERENCES)
    tex = CV.conferences_tex(entries)
    _helpers.assert_itemize(tex, len(entries))       # one \item per conference
    assert CV.CONF_HEADING in tex
    for e in entries:
        assert e.get('text'), f'conference entry missing text: {e}'
    assert '\\href{https://icms-conference.org/2026/session5.html}' in tex
    assert '{\\emph{Frontiers of rationality}}' in tex
    return f'{len(entries)} conferences'


def main():
    for check in (check_minicourses, check_talks, check_teaching, check_conferences):
        print(f'PASS: cv_sections {check.__name__[6:]} — {check()}')


if __name__ == '__main__':
    main()
