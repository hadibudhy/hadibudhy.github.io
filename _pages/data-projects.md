---
layout: archive
permalink: /data-projects/
title: "Data Projects"
author_profile: true
header:
  overlay_color: "#1a1a2e"
  overlay_image: "/images/waterfront.jpg"
  overlay_filter: 0.7
---

Explore my data science and engineering projects, from ETL pipelines to machine learning models.

<div class="grid__wrapper">
  
  {% for post in site.posts %}
  <div class="grid__item">
    <article class="archive__item">
      <div class="archive__item-teaser">
        {% if post.header.teaser %}
          <img src="{{ post.header.teaser }}" alt="{{ post.title }}">
        {% else %}
          <img src="/images/waterfront.jpg" alt="{{ post.title }}">
        {% endif %}
      </div>
      <h2 class="archive__item-title">
        <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
      </h2>
      <div class="archive__item-excerpt">
        <p>{{ post.excerpt | strip_html | truncate: 160 }}</p>
      </div>
      <div class="archive__item-tags">
        {% for tag in post.tags limit:4 %}
          <span class="tag">{{ tag }}</span>
        {% endfor %}
      </div>
    </article>
  </div>
  {% endfor %}

</div>
