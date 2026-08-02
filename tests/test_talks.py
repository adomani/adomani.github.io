#!/usr/bin/env python3
"""Self-check for scripts/talks.py against the real _data/talks.yml.

    python3 tests/test_talks.py
"""
import _helpers


def main():
    T, entries = _helpers.load('talks')
    tex = T.to_tex(entries)

    # `web_only` entries appear on the website /slides/ page but not in the CV.
    n_cv = sum(1 for e in entries if not e.get('web_only'))
    _helpers.assert_itemize(tex, n_cv)

    # Every entry is either structured (title+venue, date unless web_only) or text.
    for e in entries:
        if 'title' in e:
            assert 'venue' in e, f'structured entry missing venue: {e}'
            if not e.get('web_only'):
                assert 'date' in e, f'CV entry missing date: {e}'
        else:
            assert 'text' in e, f'entry has neither title nor text: {e}'

    # web_only entries must not leak into the CV output.
    for e in entries:
        if e.get('web_only'):
            assert e['title'] not in tex, f'web_only entry leaked into CV: {e["title"]}'

    # Content spot-checks: a plain talk, a math title and an \href survive verbatim.
    assert '{\\emph{Metaprogramming in Lean}}' in tex
    assert '$\\overline{M}_{0,134}$' in tex          # math preserved for LaTeX
    assert '\\href{' in tex                           # slide link preserved

    # A `slides` URL renders as a trailing ", \href{url}{slides}." on the line,
    # and structured entries never keep an inline {slides} href in the venue.
    slides = [e for e in entries if e.get('slides') and not e.get('web_only')]
    assert slides, 'expected at least one CV talk with a slides field'
    for e in slides:
        assert f"\\href{{{e['slides']}}}{{slides}}." in tex
        assert '{slides}' not in e['venue'], f'inline slides href left in venue: {e}'

    print(f'PASS: talks.py renders {len(entries)} talks correctly')


if __name__ == '__main__':
    main()
