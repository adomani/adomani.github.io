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

Minicourses follow the same idea from `_data/minicourses.yml`:

```
_data/minicourses.yml     <- CANONICAL (edit this)
        ├── Jekyll reads it directly ─▶ /minicourses/ (website; links + collaborators)
        └── scripts/minicourses.py --tex ─▶ cv/sections/minicourses_generated.tex (CV)
```

`url`, `links` and `collaborators` render on the website (the latter linked via
`_data/collaborators.yml`); the CV lists minicourses as plain text. Set
`cv_only: true` on an entry to keep it on the CV but hide it from the website
(e.g. an on-hold course). The generated `.tex` is built at deploy time and
gitignored, like `cv/papers.bib`.

Talks work the same way from `_data/talks.yml`:

```
_data/talks.yml     <- CANONICAL (edit this)
        └── scripts/talks.py --tex ─▶ cv/sections/talks_generated.tex (CV)
```

Most entries are structured (`year, date, title, venue`); a few heterogeneous
ones (workshops, multi-talk series) keep the CV line verbatim in `text`. Fields
may hold LaTeX (math in titles, `\href` in venues) and are emitted verbatim.
The data was bootstrapped by parsing the old `talks.tex` and **verified to
render byte-for-byte identically** to the hand-written list. The website
`/slides/` page will render a subset of this data (follow-up).

The CV's Teaching institution tables work the same way from `_data/teaching.yml`:

```
_data/teaching.yml     <- CANONICAL (edit this)
        └── scripts/teaching.py --tex ─▶ cv/sections/teaching_generated.tex (CV)
```

One institution per entry, `courses` newest-first with `period` and `course`
columns (emitted verbatim into a two-column tabular, so they may hold LaTeX like
`\emph{...}`). Bootstrapped by parsing the old `teaching.tex` and **verified to
render byte-for-byte identically** (the one intended addition is the covid-era
"Tour of Mathematics" outreach lecture, which lived only on the website
`/slides/` page before). The website's per-course `/teaching/` pages stay as the
curated view — they carry problem sheets, drafts and course subpages the CV
doesn't, and only cover Warwick, so they're not regenerated from this data.

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
