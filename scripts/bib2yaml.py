#!/usr/bin/env python3
"""Convert a BibTeX file into _data/publications.yml for the Jekyll site.

This is the shared-dataset prototype: `papers.bib` is the single source of
truth (biblatex renders the CV from it; this script renders the website's
publication data from the same file).

Usage:
    python3 scripts/bib2yaml.py _bibliography/papers.bib _data/publications.yml
"""
import re
import sys
import unicodedata
import yaml

# --- tiny BibTeX parser -----------------------------------------------------
# Handles `@type{key, Field = {value} or "value" or bareword, ...}` with
# balanced braces in values. Good enough for this hand-maintained file.

def parse_bib(text):
    entries = []
    i, n = 0, len(text)
    while i < n:
        at = text.find('@', i)
        if at == -1:
            break
        brace = text.find('{', at)
        etype = text[at + 1:brace].strip().lower()
        # read balanced body
        depth, j = 0, brace
        while j < n:
            if text[j] == '{':
                depth += 1
            elif text[j] == '}':
                depth -= 1
                if depth == 0:
                    break
            j += 1
        body = text[brace + 1:j]
        i = j + 1
        # key is up to first comma
        comma = body.find(',')
        key = body[:comma].strip()
        fields = parse_fields(body[comma + 1:])
        fields['__type__'] = etype
        fields['__key__'] = key
        entries.append(fields)
    return entries


def parse_fields(s):
    fields, i, n = {}, 0, len(s)
    while i < n:
        eq = s.find('=', i)
        if eq == -1:
            break
        name = s[i:eq].strip().lower()
        i = eq + 1
        while i < n and s[i] in ' \t\r\n':
            i += 1
        if i >= n:
            break
        if s[i] == '{':
            depth, j = 0, i
            while j < n:
                if s[j] == '{':
                    depth += 1
                elif s[j] == '}':
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            val = s[i + 1:j]
            i = j + 1
        elif s[i] == '"':
            j = i + 1
            while j < n and s[j] != '"':
                j += 1
            val = s[i + 1:j]
            i = j + 1
        else:  # bareword / number
            j = i
            while j < n and s[j] != ',':
                j += 1
            val = s[i:j].strip()
            i = j
        # advance past trailing comma
        nxt = s.find(',', i)
        i = nxt + 1 if nxt != -1 else n
        if name:
            fields[name] = ' '.join(val.split())
    return fields


# --- LaTeX -> display text (approximate; math left for MathJax) --------------
# accent macro -> combining diacritical mark (applied via NFC normalization)
COMBINING = {
    "'": '\u0301', '"': '\u0308', '`': '\u0300', '^': '\u0302',
    '~': '\u0303', '=': '\u0304', '.': '\u0307', 'u': '\u0306',
    'v': '\u030C', 'c': '\u0327', 'H': '\u030B', 'r': '\u030A',
}
# standalone special-character macros
SPECIALS = {
    r'\ss': 'ß', r'\o': 'ø', r'\O': 'Ø', r'\l': 'ł', r'\L': 'Ł',
    r'\aa': 'å', r'\AA': 'Å', r'\ae': 'æ', r'\AE': 'Æ',
    r'\oe': 'œ', r'\OE': 'Œ',
}
# Two forms: braced `\'{e}` (inner spaces allowed) or bare `\'e` / `\`a`.
# The bare form must NOT swallow trailing spaces (e.g. `Variet\`a quiver`).
_ACCENT_RE = re.compile(
    r"\\([\"'`^~=.uvcHr])(?:\{\s*(\\[ij]|[A-Za-z])\s*\}|(\\[ij]|[A-Za-z]))")


def _apply_accents(s):
    def repl(m):
        acc = m.group(1)
        base = m.group(2) or m.group(3)
        base = {r'\i': 'i', r'\j': 'j'}.get(base, base)
        return unicodedata.normalize('NFC', base + COMBINING[acc])
    prev = None
    while prev != s:            # nested/repeated accents
        prev, s = s, _ACCENT_RE.sub(repl, s)
    return s


def delatex(s):
    if not s:
        return s
    # protect inline math for MathJax
    math = []
    def stash(m):
        math.append(m.group(0))
        return f'\x00{len(math)-1}\x00'
    s = re.sub(r'\$[^$]*\$', stash, s)
    s = _apply_accents(s)
    for k, v in SPECIALS.items():
        s = re.sub(re.escape(k) + r'(?![A-Za-z])', v, s)
    s = s.replace(r'\i', 'ı').replace(r'\j', 'ȷ')
    s = s.replace('{', '').replace('}', '')
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


def link_for(f):
    if f.get('doi'):
        return 'https://doi.org/' + f['doi']
    if f.get('url'):
        return f['url']
    ep = f.get('eprint', '')
    m = re.search(r'(\d{4}\.\d{4,5})', ep)
    if m:
        return 'https://arxiv.org/abs/' + m.group(1)
    return None


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
    kw = (f.get('keywords') or '').strip().lower()
    rec['category'] = CATEGORY.get(kw, 'publications')
    rec['status'] = kw
    return rec


def main():
    src, dst = sys.argv[1], sys.argv[2]
    with open(src, encoding='utf-8') as fh:
        entries = parse_bib(fh.read())
    records = [to_record(e) for e in entries]

    def sort_key(r):
        y = re.sub(r'[^0-9]', '', r['year']) or '0'
        return -int(y)
    buckets = {'publications': [], 'preprints': [], 'books': []}
    for r in sorted(records, key=sort_key):
        buckets[r['category']].append(r)

    with open(dst, 'w', encoding='utf-8') as fh:
        fh.write('# GENERATED by scripts/bib2yaml.py from _bibliography/papers.bib\n')
        fh.write('# Do not edit by hand; edit the .bib and re-run the script.\n')
        yaml.safe_dump(buckets, fh, allow_unicode=True, sort_keys=False,
                       default_flow_style=False, width=100)
    n = sum(len(v) for v in buckets.values())
    print(f'Wrote {n} records to {dst} '
          f"(publications={len(buckets['publications'])}, "
          f"preprints={len(buckets['preprints'])}, books={len(buckets['books'])})")


if __name__ == '__main__':
    main()
