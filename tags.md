---
layout: page
title: 태그
permalink: /tags/
---

<div class="tag-cloud">
{%- assign tags = site.tags | sort -%}
{%- for t in tags -%}<a class="tag-chip" href="#{{ t[0] | slugify: 'raw' }}">#{{ t[0] }} <small>{{ t[1].size }}</small></a>{%- endfor -%}
</div>

{% for t in tags %}
<h2 id="{{ t[0] | slugify: 'raw' }}">#{{ t[0] }}</h2>
<ul class="tag-post-list">
{%- for p in t[1] -%}
<li><span>{{ p.date | date: "%Y.%m.%d" }}</span> <a href="{{ p.url | relative_url }}">{{ p.title | escape }}</a></li>
{%- endfor -%}
</ul>
{% endfor %}
