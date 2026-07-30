---
title: Papers
layout: single
permalink: /papers/
math: true
---

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
