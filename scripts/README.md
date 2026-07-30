# Shared-dataset prototype (publications)

Goal: maintain publications **once** and render them in both the LaTeX CV and
this website, instead of hand-copying `papers.bib` into `papers/index.md`.

## Pipeline

```
_bibliography/papers.bib          <- single source of truth (same file the CV uses)
        │  scripts/bib2yaml.py
        ▼
_data/publications.yml            <- generated; consumed natively by Jekyll
        │  _includes/pub_entry.html  (Liquid template, one entry)
        ▼
papers-generated/index.md         <- page that loops over site.data.publications
        ▼  /papers-generated/      <- rendered by GitHub Pages (no custom plugins)
```

## Regenerate

```sh
python3 scripts/bib2yaml.py _bibliography/papers.bib _data/publications.yml
```

`papers.bib` currently lives in the [CV repo](https://github.com/adomani/CV).
For now, copy it here and re-run the script; the CI step (next milestone) will
do this automatically on each push so the two never drift.

## Testing

The pipeline checks itself, so CI can prove it does the right thing:

```sh
# 1. Golden-file check: is the committed data in sync with the .bib?
python3 scripts/bib2yaml.py _bibliography/papers.bib _data/publications.yml --check

# 2. Fixture test: pin the converter's behaviour against a golden output
python3 tests/test_bib2yaml.py            # --update to regenerate after an intended change
```

`.github/workflows/publications.yml` runs both on every PR, then builds the
site and asserts the rendered page looks right (known entry present, UTF-8
accents rendered, no proxied URLs leaked). It is **validate-only** — it never
publishes; GitHub Pages still deploys the live site from the default branch.

## Scope / not yet modelled

- Per-paper prose/abstracts and co-author profile links (present on the current
  hand-written `papers/index.md`) are **website-only enrichments** — they would
  become optional fields on each record, emitted by the template but ignored by
  the CV.
- Only publications are prototyped. Teaching, talks, etc. would follow the same
  pattern with their own `_data/*.yml` + include.
