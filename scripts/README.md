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
        └── --bib  ─▶ _bibliography/papers.bib   (for the CV)
                          │  copied to cv/papers.bib, then latexmk
                          ▼
                      cv/main.tex  ─▶ CV PDF   (.github/workflows/cv.yml)
```

The CV (`cv/`) and the website `/papers/` page are both generated from the same
`publications.json` — one source, two outputs.

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
migrated description, inline math, no proxied URLs).
`.github/workflows/deploy.yml` builds the Jekyll site **and** the CV PDF together
and deploys them as one GitHub Pages artifact (Pages source = "GitHub Actions").
The CV PDF is generated from the same `publications.json`, placed at
`pdfs/CV.pdf`, and served from the built site — so the published CV is always in
sync, with no committed binary and no manual step. On pull requests it builds and
asserts (preprint present, repo link shown, accents render) but does not deploy.

## CV build

`--bib` reconstructs `papers.bib` from the JSON. The CV sources live in `cv/`;
the build copies the generated bib to `cv/papers.bib` (gitignored) and runs
`latexmk`. The CV's biblatex uses `url=false`, so preprint URLs are emitted as
`howpublished = {\url{...}}` (which is not suppressed) to keep the link visible.
`bib2yaml.py` remains only as a helper library (display formatting) and for the
one-time bib→json migration.

## Not yet modelled

- Extending the same JSON-canonical pattern to the other CV sections (teaching,
  talks, etc.) so the website pages and the CV share that data too.
