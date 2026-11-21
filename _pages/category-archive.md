---
title: "Categorie"
layout: single
permalink: /categorie/
author_profile: false
classes: wide
breadcrumbs: false
---

{%- comment -%}
GUIDA-SVILUPPO: pagina Categorie = una scheda per categoria, prese da _data/categorie.json (admin > Categorie), quindi si aggiornano da sole.
Il numero articoli conta solo gli articoli in italiano (esclude /en/). Link: /blog/<slug>/. Griglia 3 colonne, 2 sotto 900px, 1 sotto 560px.
{%- endcomment -%}

<style>
.cg-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1.4rem;margin:1.5rem 0 3rem}
@media (max-width:900px){.cg-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media (max-width:560px){.cg-grid{grid-template-columns:1fr}}
.cg-card{display:flex;flex-direction:column;min-height:190px;background:#fff;border:1px solid rgba(0,0,0,.12);border-radius:14px;padding:1.5rem 1.6rem;text-decoration:none !important;color:inherit;position:relative;overflow:hidden;transition:box-shadow .2s,transform .2s,border-color .2s}
.cg-card::before{content:"";position:absolute;left:0;top:0;height:3px;width:0;background:var(--t-accent,#8a6d3b);transition:width .25s}
.cg-card:hover,.cg-card:focus-visible{box-shadow:0 10px 26px rgba(0,0,0,.12);transform:translateY(-4px);border-color:rgba(0,0,0,.28)}
.cg-card:hover::before,.cg-card:focus-visible::before{width:100%}
.cg-card h2{margin:0 0 .5rem !important;padding:0 !important;border:0 !important;font-size:1.25rem;line-height:1.3;text-transform:capitalize;color:#1a1a2e}
.cg-card p{margin:0 0 1.1rem !important;font-size:.92rem;line-height:1.55;color:#666;flex:1}
.cg-meta{display:flex;justify-content:space-between;align-items:center;font-size:.88rem;font-weight:700;color:var(--t-accent,#8a6d3b)}
.cg-arrow{transition:transform .2s}
.cg-card:hover .cg-arrow,.cg-card:focus-visible .cg-arrow{transform:translateX(5px)}
</style>

<div class="cg-grid">
{% for cat in site.data.categorie %}
  {%- assign n = 0 -%}
  {%- for p in site.posts -%}
    {%- unless p.url contains "/en/" -%}
      {%- if p.categories contains cat.nome -%}{%- assign n = n | plus: 1 -%}{%- endif -%}
    {%- endunless -%}
  {%- endfor -%}
  <a class="cg-card" href="{{ '/blog/' | append: cat.nome | append: '/' | relative_url }}">
    <h2>{{ cat.nome | replace: "-", " " }}</h2>
    {% if cat.descrizione and cat.descrizione != "" %}<p>{{ cat.descrizione | strip_html | truncate: 120 }}</p>{% else %}<p></p>{% endif %}
    <div class="cg-meta"><span>{{ n }} {% if n == 1 %}articolo{% else %}articoli{% endif %}</span><span class="cg-arrow">&rarr;</span></div>
  </a>
{% endfor %}
</div>
