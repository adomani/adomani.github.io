# adomani.github.io

Source for Damiano Testa's academic website **and** CV.

### 🌐 Live site — <https://adomani.github.io/>

- **CV (PDF):** <https://adomani.github.io/pdfs/CV.pdf>
- [Publications](https://adomani.github.io/papers/) ·
  [Talks / slides](https://adomani.github.io/slides/) ·
  [Minicourses](https://adomani.github.io/minicourses/) ·
  [Teaching](https://adomani.github.io/teaching/)

## About this repository

The website (Jekyll → GitHub Pages) and the CV (LaTeX → PDF) are generated from
**one set of canonical data files**, so the two never drift apart:

| Canonical source | Feeds |
| --- | --- |
| `_bibliography/publications.json` | `/papers/` and the CV bibliography |
| `_data/talks.yml` | the CV talks list and `/slides/` |
| `_data/minicourses.yml` | the CV and `/minicourses/` |
| `_data/teaching.yml`, `_data/conferences.yml` | the CV Teaching section |
| `_data/courses.yml`, `_data/collaborators.yml` | the teaching pages and co-author links |

A single command materialises everything (`python3 scripts/build.py`), and CI
rebuilds and deploys the site and the CV together on every push to `master`.

See [`scripts/README.md`](scripts/README.md) for the full pipeline.
