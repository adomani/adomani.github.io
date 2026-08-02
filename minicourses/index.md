---
title: Minicourses
layout: single
last_modified_at: 2026-03-19T07:12:52
---

{% comment %}
Generated from _data/minicourses.yml — the same source the CV uses
(scripts/minicourses.py). Edit the data file, not this list.
{% endcomment %}
{% for m in site.data.minicourses %}{% unless m.cv_only %}{% capture people %}{% for a in m.collaborators %}{% assign u = site.data.collaborators[a] %}{% if u %}[{{ a }}]({{ u }}){% else %}{{ a }}{% endif %}{% unless forloop.last %}, {% endunless %}{% endfor %}{% endcapture -%}
{{ m.year }}, {{ m.date }},{% if m.url %} [**{{ m.title }}**]({{ m.url }}){% else %} **{{ m.title }}**{% endif %}{% if m.context %}, {{ m.context }}{% endif %}{% if m.collaborators %}, with {{ people }}{% endif %}, {{ m.venue }}{% if m.links %}{% for l in m.links %} ([{{ l.label }}]({{ l.url }})){% endfor %}{% endif %}.

{% endunless %}{% endfor %}
