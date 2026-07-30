---
title: Papers
layout: single
permalink: /papers-generated/
math: true
---

<style>
.page__content .pub { margin: 0.55em 0; }
.page__content details.pub > summary { cursor: pointer; }
.page__content details.pub[open] > summary { margin-bottom: 0.4em; }
.page__content .pub-desc { margin: 0.3em 0 0.8em 1.4em; }
</style>

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
