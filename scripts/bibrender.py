#!/usr/bin/env python3
"""Display helpers that turn a publication's BibTeX-style fields into the record
the website shows. Used by scripts/publications.py.

Flow (canonical source is the JSON, never the .bib):

    _bibliography/publications.json  ──scripts/publications.py──▶ render record
        │                                      │  to_record() + the helpers here
        │                                      ▼
        │                            _data/publications.yml  ──▶ /papers/ (website)
        └──────────────────────────▶ cv/papers.bib ──▶ CV PDF

These are pure functions on a field dict (`to_record` and the `delatex` /
`format_authors` / `link_for` it calls); there is no BibTeX parsing here — the
data is authored in JSON. `bib2yaml` and the one-time bib→json migration that
seeded the JSON were retired; see the git history if you need them.
"""
import re


# --- LaTeX -> display text ---------------------------------------------------
# The JSON stores accents as UTF-8, so all that remains is stripping
# capitalization-protection braces ({F}ermat) and a couple of escapes.
# Inline math `$...$` is re-emitted as `\\(...\\)`: the site's MathJax uses the
# \(...\) delimiter, and the doubled backslash survives kramdown (which would
# otherwise eat a single `\(` as an escaped paren) to yield `\(...\)` in the HTML.
def delatex(s):
    if not s:
        return s
    math = []
    def stash(m):
        math.append('\\\\(' + m.group(0)[1:-1] + '\\\\)')  # $x$ -> \\(x\\)
        return f'\x00{len(math)-1}\x00'
    s = re.sub(r'\$[^$]*\$', stash, s)          # protect + convert math
    s = s.replace('{', '').replace('}', '')      # drop {F}ermat-style braces
    s = s.replace('\\&', '&').replace('~', ' ')
    s = re.sub(r'\s+', ' ', s).strip()
    s = re.sub('\x00(\\d+)\x00', lambda m: math[int(m.group(1))], s)
    return s


def format_authors(raw):
    out = []
    for name in re.split(r'\s+and\s+', raw.strip()):
        name = name.strip()
        if ',' in name:
            fam, giv = [p.strip() for p in name.split(',', 1)]
            name = f'{giv} {fam}'.strip()
        out.append(delatex(name))
    return out


CATEGORY = {  # keyword -> section bucket
    'published': 'publications', 'accepted': 'publications',
    'preprint': 'preprints', 'book': 'books',
}


def arxiv_url(f):
    """The arXiv abstract URL from an `eprint` field like 'arXiv:2607.29111'."""
    m = re.search(r'(\d{4}\.\d{4,5})', f.get('eprint', ''))
    return 'https://arxiv.org/abs/' + m.group(1) if m else None


def link_for(f):
    # The title's primary link: a DOI, then the arXiv abstract, then a bare URL.
    # arXiv outranks `url` so a preprint that also lists a code repo (in `url`)
    # links its title to the paper, and the repo becomes a separate `code` link.
    if f.get('doi'):
        return 'https://doi.org/' + f['doi']
    return arxiv_url(f) or f.get('url') or None


def to_record(f):
    venue = delatex(f.get('fjournal') or f.get('journal') or f.get('booktitle') or '')
    rec = {
        'key': f['__key__'],
        'title': delatex(f.get('title', '')),
        'authors': format_authors(f.get('author', '')),
        'year': f.get('year', ''),
    }
    if venue:
        rec['venue'] = venue
    for k in ('volume', 'number', 'pages'):
        if f.get(k):
            rec[k] = delatex(f[k])
    link = link_for(f)
    if link:
        rec['url'] = link
    # A code repository (`url`) shown alongside the paper: only when the primary
    # link is the paper itself (arXiv/DOI), so the repo doesn't duplicate it.
    repo = f.get('url')
    if repo and repo != link:
        rec['code'] = repo
    kw = (f.get('keywords') or '').strip().lower()
    rec['category'] = CATEGORY.get(kw, 'publications')
    rec['status'] = kw
    return rec
