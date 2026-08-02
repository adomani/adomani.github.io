#!/usr/bin/env python3
"""Generate the CV's "Talks and conferences" LaTeX list from the shared data.

    _data/talks.yml   (canonical)
        └── scripts/talks.py --tex ─▶ a LaTeX itemize for the CV

Most entries are structured (year, date, title, venue); a few heterogeneous
ones keep the CV line verbatim in `text`. Fields may contain LaTeX (math in
titles, \\href in venues), so they are emitted verbatim — not escaped.

An optional `slides` URL renders as a trailing ", \\href{url}{slides}." on the
CV line. The website /slides/ page (scripts/slides.py) uses further optional
fields the CV ignores (`video`, `note`), and `web_only: true` entries are shown
on /slides/ but skipped here.

    python3 scripts/talks.py --out cv/sections/talks_generated.tex
    add --check to compare against an existing file instead of writing.
"""
import _common

DATA = '_data/talks.yml'
HEADER = _common.header('talks.py', DATA)


def reconstruct(e):
    if 'title' not in e:
        return e['text']
    venue = e['venue']
    if e.get('slides'):
        # Drop a trailing '.' so a venue like "..., online." doesn't render as
        # "online., \href{}{slides}." — the slides clause supplies the period.
        return (f"{e['year']}, {e['date']}, {{\\emph{{{e['title']}}}}}, "
                f"{venue.rstrip('.')}, \\href{{{e['slides']}}}{{slides}}.")
    return f"{e['year']}, {e['date']}, {{\\emph{{{e['title']}}}}}, {venue}"


def to_tex(entries):
    # `web_only` entries appear on the website /slides/ page but not in the CV.
    cv = [e for e in entries if not e.get('web_only')]
    items = '\n'.join('\\item\n' + reconstruct(e) for e in cv)
    return HEADER + '\\begin{itemize}\n' + items + '\n\\end{itemize}\n'


def render():
    entries = _common.load(DATA)
    return to_tex(entries), len(entries)


if __name__ == '__main__':
    raise SystemExit(_common.cli(render, noun='talks'))
