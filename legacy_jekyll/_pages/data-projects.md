---
layout: default
permalink: /data-projects/
title: "Data Projects"
---

<div class="page__hero--overlay" style="padding: 3rem 1.5rem; text-align: center; border-radius: 16px; margin: 2rem 0;">
  <h1 class="page__title">{{ page.title }}</h1>
  <p class="page__lead">Explore my data science and engineering projects, from ETL pipelines to machine learning models.</p>
</div>

<div class="filter-controls">
  <button class="filter-btn active" data-filter="all">All</button>
  <button class="filter-btn" data-filter="data-engineering">Data Engineering</button>
  <button class="filter-btn" data-filter="machine-learning">Machine Learning</button>
  <button class="filter-btn" data-filter="analytics">Analytics</button>
</div>

<div class="grid__wrapper">
  
  {% for post in site.posts %}
  <div class="grid__item project-item" data-tags="{% for cat in post.categories %}{{ cat | downcase | replace: ' ', '-' }} {% endfor %}{% for tag in post.tags %}{{ tag | downcase | replace: ' ', '-' }} {% endfor %}">
    <article class="archive__item">
      <div class="archive__item-teaser">
        {% if post.header.teaser %}
          <img src="{{ post.header.teaser }}" alt="{{ post.title }}">
        {% else %}
          <div class="fallback-pattern">
            <i class="fas fa-chart-network"></i>
          </div>
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

<script>
document.addEventListener("DOMContentLoaded", function() {
  const filterBtns = document.querySelectorAll('.filter-btn');
  const items = document.querySelectorAll('.project-item');

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      // Remove active class
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const filterValue = btn.getAttribute('data-filter');

      items.forEach(item => {
        if (filterValue === 'all') {
          item.style.display = 'block';
        } else {
          const tags = item.getAttribute('data-tags') || '';
          if (tags.includes(filterValue)) {
            item.style.display = 'block';
          } else {
            item.style.display = 'none';
          }
        }
      });
    });
  });
});
</script>
