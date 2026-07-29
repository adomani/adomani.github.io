---
title: Papers (generated)
layout: single
permalink: /papers-generated/
math: true
---

*Prototype — this page is generated automatically from
[`papers.bib`](https://github.com/adomani/CV/blob/master/papers.bib), the same
file the CV is built from. Do not edit by hand.*

{% assign pubs = site.data.publications %}

## Publications

{% for r in pubs.publications %}{% include pub_entry.html pub=r %}
{% endfor %}

## Preprints

{% for r in pubs.preprints %}{% include pub_entry.html pub=r %}
{% endfor %}

## Books (in preparation)

{% for r in pubs.books %}{% include pub_entry.html pub=r %}
{% endfor %}
