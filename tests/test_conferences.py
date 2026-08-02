#!/usr/bin/env python3
"""Self-check for scripts/conferences.py against _data/conferences.yml.

    python3 tests/test_conferences.py
"""
import _helpers


def main():
    C, entries = _helpers.load('conferences')
    tex = C.to_tex(entries)

    _helpers.assert_itemize(tex, len(entries))       # one \item per conference
    assert C.HEADING in tex

    for e in entries:
        assert e.get('text'), f'conference entry missing text: {e}'

    # Content spot-checks: the \href session and a plain \emph title survive.
    assert '\\href{https://icms-conference.org/2026/session5.html}' in tex
    assert '{\\emph{Frontiers of rationality}}' in tex

    print(f'PASS: conferences.py renders {len(entries)} conferences')


if __name__ == '__main__':
    main()
