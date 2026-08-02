## [Damiano Testa's webpage](https://adomani.github.io/)

- **CV (PDF):** <https://adomani.github.io/pdfs/CV.pdf>
- [Publications](https://adomani.github.io/papers/) ·
  [Talks / slides](https://adomani.github.io/slides/) ·
  [Minicourses](https://adomani.github.io/minicourses/) ·
  [Teaching](https://adomani.github.io/teaching/)

## About this repository

The website and CV are generated from:

| Canonical source | Feeds |
| --- | --- |
| [`_bibliography/publications.json`](_bibliography/publications.json) | `/papers/` and the CV bibliography |
| [`_data/talks.yml`](_data/talks.yml) | the CV talks list and `/slides/` |
| [`_data/minicourses.yml`](_data/minicourses.yml) | the CV and `/minicourses/` |
| [`_data/teaching.yml`](_data/teaching.yml), [`_data/conferences.yml`](_data/conferences.yml) | the CV Teaching section |
| [`_data/courses.yml`](_data/courses.yml), [`_data/collaborators.yml`](_data/collaborators.yml) | the teaching pages and co-author links |

The single command [`python3 scripts/build.py`](scripts/build.py) materialises everything, and CI
rebuilds and deploys the site and the CV together on every push to `master`.

See [`scripts/README.md`](scripts/README.md) for the full pipeline.
