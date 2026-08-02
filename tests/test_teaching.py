#!/usr/bin/env python3
"""Self-check for scripts/teaching.py against the real _data/teaching.yml.

    python3 tests/test_teaching.py
"""
import _helpers


def main():
    T, data = _helpers.load('teaching')
    tex = T.to_tex(data)

    _helpers.assert_itemize(tex, len(data))          # one \item per institution

    # Every institution has a name and a non-empty ordered course list, and each
    # course has both columns (period + course), emitted verbatim into a tabular.
    for inst in data:
        assert inst.get('institution'), f'institution missing name: {inst}'
        assert inst.get('courses'), f'{inst["institution"]} has no courses'
        for c in inst['courses']:
            assert 'period' in c and 'course' in c, f'bad course row: {c}'

    # One tabular per institution, correct column spec.
    assert tex.count('\\begin{tabular}') == len(data)
    assert tex.count(T.COLSPEC) == len(data)

    # Content spot-checks: the earliest and latest institutions survive, and the
    # \emph{...} in the Tour of Mathematics outreach row is emitted verbatim.
    assert '{\\textbf{Warwick}}' in tex
    assert '{\\textbf{MIT}}' in tex
    assert '\\emph{Using computers to do maths for us!}' in tex

    n_courses = sum(len(i['courses']) for i in data)
    print(f'PASS: teaching.py renders {len(data)} institutions, {n_courses} courses')


if __name__ == '__main__':
    main()
