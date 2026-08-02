#!/usr/bin/env python3
"""Materialise every generated artifact from the canonical data — the one place
that lists all targets. Used by the deploy (write) and CI (check).

    python3 scripts/build.py            # write every output (deploy)
    python3 scripts/build.py --check    # verify the committed outputs are in sync

Targets marked committed are checked into git (the website's publications.yml and
the CV's papers.bib) and verified by --check; the rest are build outputs
(gitignored) that are only ever written. Adding a section = one line here.
"""
import argparse
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(os.path.dirname(HERE))          # repo root, so relative data paths resolve

import _common            # noqa: E402
import cv_sections         # noqa: E402
import minicourses_page    # noqa: E402
import publications        # noqa: E402
import slides              # noqa: E402


def _pub_yaml():
    return publications.to_yaml(publications.load())


def _pub_bib():
    return publications.to_bib(publications.load())


def _section(name):
    return lambda: cv_sections.render(name)


# (output path, render -> content-or-(content,count), committed to git?)
TARGETS = [
    ('_data/publications.yml',                _pub_yaml,                    True),
    ('_bibliography/papers.bib',              _pub_bib,                     True),
    ('cv/sections/minicourses_generated.tex', _section('minicourses'),     False),
    ('cv/sections/talks_generated.tex',       _section('talks'),           False),
    ('cv/sections/teaching_generated.tex',    _section('teaching'),        False),
    ('cv/sections/conferences_generated.tex', _section('conferences'),     False),
    ('slides/index.md',                       slides.render,               False),
    ('minicourses/index.md',                  minicourses_page.render,     False),
]


def _content(render):
    r = render()
    return r[0] if isinstance(r, tuple) else r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true',
                    help='verify the committed outputs are in sync (no writes)')
    a = ap.parse_args()

    if a.check:
        rc = 0
        for path, render, committed in TARGETS:
            if committed:
                rc |= _common.emit(path, _content(render), check=True)
        return rc

    for path, render, _committed in TARGETS:
        _common.emit(path, _content(render))
    # The CV build reads cv/papers.bib (gitignored); keep it in sync.
    shutil.copyfile('_bibliography/papers.bib', 'cv/papers.bib')
    print('Wrote cv/papers.bib (copy of _bibliography/papers.bib)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
