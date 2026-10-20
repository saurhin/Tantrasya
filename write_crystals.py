import os

base = r"d:\tantrasya-python\tantrasya-py-paranormal"

# Create crystals image folder
img_dir = os.path.join(base, "static", "images", "crystals")
os.makedirs(img_dir, exist_ok=True)
print("Created static/images/crystals/")

# crystals.html template
template = """\
{% extends "base.html" %}
{% block content %}

<section class="hero">
  <div class="wrap">
    <div class="hero-copy">
      <p class="hero-kicker">Tantrasya</p>
      <h1>Crystals</h1>
      <p class="hero-lede">A curated selection of crystals across eleven categories — from raw and natural pieces to polished forms, wands, spheres and more.</p>
    </div>
  </div>
</section>

<section class="section-alt">
  <div class="wrap">
    <div class="section-head center">
      <p class="eyebrow">Browse by category</p>
      <h2>Eleven ways to explore</h2>
    </div>
    <div class="grid grid-crystal">
      {% for crystal in crystals %}
      <div class="crystal-card">
        <div class="crystal-thumb">
          {% set exts = ['.jpg', '.jpeg', '.png', '.webp'] %}
          {% set found = false %}
          {% for ext in exts %}
            {% if not found %}
              {# Try to show image if it exists; fallback to gradient placeholder #}
            {% endif %}
          {% endfor %}
          <img
            src="/static/images/crystals/{{ crystal.slug }}.jpg"
            alt="{{ crystal.name }}"
            onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';"
            class="crystal-img"
          >
          <div class="crystal-placeholder" style="display:none;">
            <span>{{ crystal.name }}</span>
          </div>
        </div>
        <div class="crystal-info">
          <h3>{{ crystal.name }}</h3>
          <p>{{ crystal.description }}</p>
        </div>
      </div>
      {% endfor %}
    </div>
  </div>
</section>

<section class="tight">
  <div class="wrap">
    <div class="cta-band">
      <p class="eyebrow">Interested?</p>
      <h2>Have a crystal or category in mind?</h2>
      <p>Get in touch to discuss availability or make an enquiry.</p>
      <div class="cta-ctas">
        <a class="btn btn-primary" href="/contact/">Make an Enquiry</a>
      </div>
    </div>
  </div>
</section>

{% endblock %}
"""

with open(os.path.join(base, "templates", "crystals.html"), "w", encoding="utf-8") as f:
    f.write(template)
print("crystals.html template written")

# content/pages/crystals.md
content = """\
---
title: "Crystals"
slug: "crystals"
description: "Browse Tantrasya crystal categories — tumbles, raw, bracelets, spheres, wands, towers, palm stones and more."
---
"""
with open(os.path.join(base, "content", "pages", "crystals.md"), "w", encoding="utf-8") as f:
    f.write(content)
print("crystals.md written")

print("Done.")
