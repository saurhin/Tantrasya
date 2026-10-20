import os
base = r"d:\tantrasya-python\tantrasya-py-paranormal"

tmpl = """\
{% extends "base.html" %}
{% block extra_css %}
<link rel="stylesheet" href="/static/css/crystals.css?v={{ asset_version }}">
{% endblock %}
{% block content %}

<section class="tight">
  <div class="wrap">

    <!-- Breadcrumb + back link -->
    <div class="crystal-breadcrumb">
      <a href="/crystals/">&larr; All Crystals</a>
      <span class="crumb-sep">&rsaquo;</span>
      <span>{{ crystal.name }}</span>
    </div>

    <!-- Title + description -->
    <h1 style="margin: 12px 0 8px;">{{ crystal.name }}</h1>
    <p class="hero-lede" style="margin: 0 0 32px;">{{ crystal.description }}</p>

    <!-- Gallery -->
    {% if images %}
    <div class="crystal-gallery">
      {% for img in images %}
      <div class="gallery-item" onclick="openLightbox('/static/images/crystals/{{ crystal.slug }}/{{ img }}')">
        <img src="/static/images/crystals/{{ crystal.slug }}/{{ img }}" alt="{{ crystal.name }}">
      </div>
      {% endfor %}
    </div>
    {% else %}
    <div class="gallery-empty">
      <p>Photos coming soon — check back shortly.</p>
    </div>
    {% endif %}

    <!-- Prev / Back / Next navigation -->
    <div class="crystal-nav">
      <div class="crystal-nav-prev">
        {% if prev_crystal %}
        <a class="btn btn-ghost" href="/crystals/{{ prev_crystal.slug }}/">&larr; {{ prev_crystal.name }}</a>
        {% endif %}
      </div>
      <a class="btn btn-outline" href="/crystals/">All Crystals</a>
      <div class="crystal-nav-next">
        {% if next_crystal %}
        <a class="btn btn-ghost" href="/crystals/{{ next_crystal.slug }}/">{{ next_crystal.name }} &rarr;</a>
        {% endif %}
      </div>
    </div>

    <!-- Enquiry -->
    <div style="text-align:center; margin-top: 24px;">
      <a class="btn btn-primary" href="/contact/">Enquire about {{ crystal.name }}</a>
    </div>

  </div>
</section>

<!-- Lightbox -->
<div class="lightbox" id="lightbox" onclick="closeLightbox()">
  <button class="lightbox-close" onclick="closeLightbox()">&times;</button>
  <img id="lightbox-img" src="" alt="">
</div>

<script>
function openLightbox(src) {
  document.getElementById('lightbox-img').src = src;
  document.getElementById('lightbox').classList.add('open');
  document.body.style.overflow = 'hidden';
}
function closeLightbox() {
  document.getElementById('lightbox').classList.remove('open');
  document.body.style.overflow = '';
}
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') closeLightbox();
});
</script>

{% endblock %}
"""

with open(os.path.join(base, "templates", "crystal_category.html"), "w", encoding="utf-8") as f:
    f.write(tmpl)
print("crystal_category.html updated")
