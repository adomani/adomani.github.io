#!/usr/bin/env python3
"""The single entry point: materialise every generated artifact from the
canonical data. This is the one place that lists all targets.

    python3 scripts/build.py            # write every output (deploy)
    python3 scripts/build.py --check    # verify the committed outputs are in sync
    python3 scripts/build.py talks      # preview one target on stdout (by name)

Each target is `name -> (output path, render() -> str, committed?)`. Targets
marked committed are checked into git (the website's publications.yml and the
CV's papers.bib) and verified by --check; the rest are build outputs (gitignored)
that are only ever written. Adding a section = one line here.
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


# name -> (output path, render() -> str, committed to git?)
TARGETS = {
    'publications-yaml': ('_data/publications.yml',                _pub_yaml,                True),
    'publications-bib':  ('_bibliography/papers.bib',              _pub_bib,                 True),
    'minicourses':       ('cv/sections/minicourses_generated.tex', _section('minicourses'), False),
    'talks':             ('cv/sections/talks_generated.tex',       _section('talks'),       False),
    'teaching':          ('cv/sections/teaching_generated.tex',    _section('teaching'),    False),
    'conferences':       ('cv/sections/conferences_generated.tex', _section('conferences'), False),
    'slides':            ('slides/index.md',                       slides.render,           False),
    'minicourses-page':  ('minicourses/index.md',                  minicourses_page.render, False),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('target', nargs='?', choices=sorted(TARGETS),
                    help='render just this target to stdout (default: write all)')
    ap.add_argument('--check', action='store_true',
                    help='verify the committed outputs are in sync (no writes)')
    a = ap.parse_args()

    if a.target:
        return _common.emit('-', TARGETS[a.target][1]())

    if a.check:
        rc = 0
        for path, render, committed in TARGETS.values():
            if committed:
                rc |= _common.emit(path, render(), check=True)
        return rc

    for path, render, _committed in TARGETS.values():
        _common.emit(path, render())
    # The CV build reads cv/papers.bib (gitignored); keep it in sync.
    shutil.copyfile('_bibliography/papers.bib', 'cv/papers.bib')
    print('Wrote cv/papers.bib (copy of _bibliography/papers.bib)')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
