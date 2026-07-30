# Publications pipeline

One canonical, hand-editable source of truth for publications; everything else
is generated. The website page and the CV's `.bib` both derive from it.

## Pipeline

```
_bibliography/publications.json      <- CANONICAL (edit this). Rich data +
        │                               per-paper `description` (markdown).
        │  scripts/publications.py
        ├── --yaml ─▶ _data/publications.yml     (render-ready, for the website)
        │                 │  _includes/pub_entry.html  (Liquid template)
        │                 ▼
        │            papers/index.md  ─▶ /papers/
        │
        └── --bib  ─▶ _bibliography/papers.bib   (reconstructed, for the CV)
```

- Papers with a `description` render as a `<details>/<summary>` pair (citation
  shown, description hidden until clicked); papers without render as a plain
  citation. All authors are listed in order.
- An optional per-entry `citation_note` (markdown) is shown after the citation —
  used for dedications and the thesis/supervisor credit.
- Co-author homepages live in `_data/collaborators.yml` (a hand-edited
  `name: url` map — the single point of entry). The template links any author
  whose rendered name matches a key there; unlisted names render as plain text.
- Inline math is written `\\(..\\)` in the JSON/descriptions; it survives
  kramdown to `\(..\)`, which the site's MathJax typesets.

## Regenerate after editing the JSON

```sh
python3 scripts/publications.py --yaml _data/publications.yml
python3 scripts/publications.py --bib  _bibliography/papers.bib
```

## Testing

The pipeline checks itself, so CI can prove it does the right thing:

```sh
# Golden-file checks: are the generated files in sync with the JSON?
python3 scripts/publications.py --yaml _data/publications.yml --check
python3 scripts/publications.py --bib  _bibliography/papers.bib  --check

# Fixture test: pin JSON -> yaml and JSON -> bib output
python3 tests/test_publications.py            # --update to regenerate after an intended change
```

`.github/workflows/publications.yml` runs these on every PR, builds the site,
and asserts the rendered page (known entry, UTF-8 accents, a <details> block, a
migrated description, inline math, no proxied URLs). It is **validate-only** —
it never publishes.

## CV round-trip

`--bib` reconstructs `papers.bib` from the JSON. This was verified to rebuild
the CV with a byte-identical bibliography, so the CV can eventually consume the
generated `.bib` (Phase B: CI pushes it to the private CV repo). `bib2yaml.py`
remains only as a helper library (display formatting) and for the one-time
bib→json migration.

## Not yet modelled

- Extending the same JSON-canonical pattern to teaching, talks, etc.
