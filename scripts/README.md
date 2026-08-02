# Publications pipeline

One canonical, hand-editable source of truth for publications; everything else
is generated. The website page and the CV's `.bib` both derive from it.

## Pipeline

```
_bibliography/publications.json      <- CANONICAL (edit this). Rich data +
        │                               per-paper `description` (markdown).
        │  scripts/publications.py
        ├── to_yaml ─▶ _data/publications.yml    (render-ready, for the website)
        │                 │  _includes/pub_entry.html  (Liquid template)
        │                 ▼
        │            papers/index.md  ─▶ /papers/
        │
        └── to_bib  ─▶ _bibliography/papers.bib   (for the CV)
                          │  copied to cv/papers.bib, then latexmk
                          ▼
                      cv/main.tex  ─▶ CV PDF   (.github/workflows/cv.yml)
```

The CV (`cv/`) and the website `/papers/` page are both generated from the same
`publications.json` — one source, two outputs.

Minicourses follow the same idea from `_data/minicourses.yml`:

```
_data/minicourses.yml     <- CANONICAL (edit this)
        ├── scripts/minicourses_page.py ─▶ minicourses/index.md  (/minicourses/ page)
        └── scripts/cv_sections.py minicourses ─▶ cv/sections/minicourses_generated.tex (CV)
```

Both the website page and the CV are generated from the one file (the page used
to be a Jekyll Liquid loop; now it comes from the shared builder like `/slides/`).
`url`, `links` and `collaborators` render on the website (the latter linked via
`_data/collaborators.yml`); the CV lists minicourses as plain text. Set
`cv_only: true` on an entry to keep it on the CV but hide it from the website
(e.g. an on-hold course). Both generated files are built at deploy time and
gitignored, like `cv/papers.bib`.

Talks work the same way from `_data/talks.yml`:

```
_data/talks.yml     <- CANONICAL (edit this)
        └── scripts/cv_sections.py talks ─▶ cv/sections/talks_generated.tex (CV)
```

Most entries are structured (`year, date, title, venue`); a few heterogeneous
ones (workshops, multi-talk series) keep the CV line verbatim in `text`.
`title`/`venue` are **Markdown inline text** (see *Inline text* below), so the
same field feeds both the CV and `/slides/`. An optional `slides:` URL renders on
the CV line as a trailing `\href{url}{slides}.`

The website `/slides/` page is generated from the same data:

```
_data/talks.yml  ── scripts/slides.py ─▶ slides/index.md  (/slides/ page)
```

It lists every talk with a `slides` URL (newest first), converting the CV's
LaTeX to the kramdown/MathJax the site expects (`\href{u}{t}` → `[t](u)`,
`$...$` → `\\(...\\)`, accents → Unicode). Two further fields the CV ignores are
used here: `video:` (a URL) and `note:` (a short sentence, may contain `\href`).
An entry with `web_only: true` shows on `/slides/` but is skipped by the CV —
used for the Tour of Mathematics (which is in the CV's Teaching section) and the
Tsinghua minicourse slides. `slides/index.md` is generated at build time and
gitignored, like the CV fragments.

The CV's Teaching institution tables work the same way from `_data/teaching.yml`:

```
_data/teaching.yml     <- CANONICAL (edit this)
        └── scripts/cv_sections.py teaching ─▶ cv/sections/teaching_generated.tex (CV)
```

One institution per entry, `courses` newest-first with `period` and `course`
columns (emitted verbatim into a two-column tabular, so they may hold LaTeX like
`\emph{...}`). Bootstrapped by parsing the old `teaching.tex` and **verified to
render byte-for-byte identically** (the one intended addition is the covid-era
"Tour of Mathematics" outreach lecture, which lived only on the website
`/slides/` page before). The website's per-course `/teaching/` pages stay as the
curated view — they carry problem sheets, drafts and course subpages the CV
doesn't, and only cover Warwick, so they're not regenerated from this data.

The CV's **Organized conferences** list works the same way from
`_data/conferences.yml`:

```
_data/conferences.yml  ── scripts/cv_sections.py conferences ─▶ cv/sections/conferences_generated.tex (CV)
```

The four entries are too heterogeneous to structure, so each is one **Markdown**
`text` line (`[*title*](url), with … venue … dates`) that `_common.md_to_tex`
renders to LaTeX. `teaching.tex` `\input`s both this and the teaching tables; the
whole Teaching section is data-driven.

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

## Inline text (one source, two dialects)

Sections that render to **both** the CV and the website (talks → `/slides/`,
conferences) store their inline formatting as neutral **Markdown**, not LaTeX:

```
[label](url)   *emphasis*   $math$   é ü “ ”      (in the YAML)
      │                                    │
      │ _common.md_to_tex                  │ _common.md_to_web
      ▼                                    ▼
\href{url}{label}, \emph{..}, $..$,   [label](url), *emphasis*, \(math\)
é ü `` '' (LaTeX, for the CV)          (kramdown/MathJax, for the site)
```

So the format is defined once; each target applies a tiny converter. `$math$`
and the verbatim `text` escape-hatch pass through. Sections whose CV text is
**plain** (minicourses — its links live in separate `url`/`collaborators`
fields) keep `tex_escape` instead; `publications` (biblatex) and `teaching`
(tables) are their own formats.

## How the generators fit together

Every generator exposes one function, `render() -> str`, and `scripts/build.py`
is the **single entry point**: it holds the one list of named *(data → output)*
targets and materialises them all. There is no per-script CLI — adding a section
is one line in `build.py`. The whole pipeline is three commands:

```sh
python3 scripts/build.py          # regenerate every output (fragments, papers.bib, /slides/)
python3 scripts/build.py --check  # verify the committed outputs are in sync (no writes)
python3 scripts/build.py talks    # preview one target on stdout (by name)
```

## Testing

The pipeline checks itself, so CI can prove it does the right thing:

```sh
python3 scripts/build.py --check              # committed files in sync with their source
for t in tests/test_*.py; do python3 "$t"; done   # one self-check per section
python3 tests/test_publications.py --update   # regenerate fixtures after an intended change
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

`publications.to_bib` reconstructs `papers.bib` from the JSON. The CV sources live in `cv/`;
the build copies the generated bib to `cv/papers.bib` (gitignored) and runs
`latexmk`. The CV's biblatex uses `url=false`, so preprint URLs are emitted as
`howpublished = {\url{...}}` (which is not suppressed) to keep the link visible.
`bib2yaml.py` remains only as a helper library (display formatting) and for the
one-time bib→json migration.

## Not yet modelled

- The remaining CV sections are still hand-written LaTeX in `cv/sections/`
  (education, positions, awards, service, students, personal). They have no
  website counterpart, so there's little to share yet.
- The website `/slides/` page is now generated from `_data/talks.yml` (see
  above), so talks and slides share one source.
