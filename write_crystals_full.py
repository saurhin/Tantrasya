import os, re

base = r"d:\tantrasya-python\tantrasya-py-paranormal"

# ── 1. Extract crystal CSS from style.css → crystals.css ──────────────────
style_path = os.path.join(base, "static", "css", "style.css")
with open(style_path, "r", encoding="utf-8") as f:
    style_css = f.read()

marker = "/* ==========================================================================\n   Crystals page"
if marker in style_css:
    idx = style_css.index(marker)
    crystals_css_content = style_css[idx:]
    style_css_clean = style_css[:idx].rstrip() + "\n"
    with open(style_path, "w", encoding="utf-8") as f:
        f.write(style_css_clean)
    crystals_css_path = os.path.join(base, "static", "css", "crystals.css")
    with open(crystals_css_path, "w", encoding="utf-8") as f:
        f.write(crystals_css_content)
    print("Crystal CSS extracted to crystals.css")
else:
    print("Crystal CSS marker not found - writing crystals.css fresh")

# Write full crystals.css (fresh, includes gallery + lightbox styles)
crystals_css = """\
/* ==========================================================================
   Crystals — loaded only on crystal pages
   ========================================================================== */

/* Category grid */
.grid-crystal {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 28px;
  margin-top: 40px;
}

.crystal-card {
  background: var(--card);
  border-radius: var(--radius);
  box-shadow: var(--shadow-soft);
  overflow: hidden;
  text-decoration: none;
  color: inherit;
  display: block;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.crystal-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow);
}

.crystal-thumb {
  width: 100%;
  aspect-ratio: 1 / 1;
  overflow: hidden;
  position: relative;
}

.crystal-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.crystal-placeholder {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--plum) 0%, var(--indigo) 60%, var(--terracotta-deep) 100%);
  color: rgba(255,255,255,0.75);
  font-family: var(--font-display);
  font-size: 1.3rem;
  font-style: italic;
  letter-spacing: 0.03em;
}

.crystal-info {
  padding: 18px 20px 22px;
}
.crystal-info h3 {
  font-size: 1.1rem;
  margin: 0 0 8px;
  color: var(--ink);
}
.crystal-info p {
  font-size: 0.9rem;
  color: var(--ink-soft);
  margin: 0;
  line-height: 1.55;
}

/* ── Category sub-page gallery ── */
.crystal-gallery {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
  margin-top: 32px;
}

.gallery-item {
  border-radius: 14px;
  overflow: hidden;
  aspect-ratio: 1 / 1;
  cursor: pointer;
  position: relative;
  background: linear-gradient(135deg, var(--plum), var(--indigo));
}
.gallery-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.3s ease;
}
.gallery-item:hover img { transform: scale(1.05); }

/* Lightbox */
.lightbox {
  display: none;
  position: fixed;
  inset: 0;
  background: rgba(20, 10, 30, 0.92);
  z-index: 1000;
  align-items: center;
  justify-content: center;
  padding: 24px;
}
.lightbox.open { display: flex; }
.lightbox img {
  max-width: 90vw;
  max-height: 88vh;
  object-fit: contain;
  border-radius: 12px;
  box-shadow: 0 24px 80px rgba(0,0,0,0.6);
}
.lightbox-close {
  position: fixed;
  top: 20px; right: 28px;
  font-size: 2rem;
  color: #fff;
  cursor: pointer;
  line-height: 1;
  opacity: 0.8;
  background: none; border: none;
}
.lightbox-close:hover { opacity: 1; }

/* No images placeholder */
.gallery-empty {
  text-align: center;
  padding: 60px 20px;
  color: var(--ink-soft);
  font-style: italic;
}
"""
with open(os.path.join(base, "static", "css", "crystals.css"), "w", encoding="utf-8") as f:
    f.write(crystals_css)
print("crystals.css written")

# ── 2. Create image subdirs for each category ─────────────────────────────
slugs = ["tumbles","raw","bracelets","shapes","free-forms","pyramids","spheres","wands","cabachons","towers","palm-stones"]
for slug in slugs:
    d = os.path.join(base, "static", "images", "crystals", slug)
    os.makedirs(d, exist_ok=True)
print("Category image folders created")

# ── 3. Updated crystals.html — cards link to sub-pages ────────────────────
crystals_tmpl = """\
{% extends "base.html" %}
{% block extra_css %}
<link rel="stylesheet" href="/static/css/crystals.css?v={{ asset_version }}">
{% endblock %}
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
    <div class="grid-crystal">
      {% for crystal in crystals %}
      <a class="crystal-card" href="/crystals/{{ crystal.slug }}/">
        <div class="crystal-thumb">
          <img
            class="crystal-img"
            src="/static/images/crystals/{{ crystal.slug }}.jpg"
            alt="{{ crystal.name }}"
            onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';"
          >
          <div class="crystal-placeholder" style="display:none;">{{ crystal.name }}</div>
        </div>
        <div class="crystal-info">
          <h3>{{ crystal.name }}</h3>
          <p>{{ crystal.description }}</p>
        </div>
      </a>
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
    f.write(crystals_tmpl)
print("crystals.html updated (cards now link to sub-pages)")

# ── 4. Crystal category sub-page template ─────────────────────────────────
category_tmpl = """\
{% extends "base.html" %}
{% block extra_css %}
<link rel="stylesheet" href="/static/css/crystals.css?v={{ asset_version }}">
{% endblock %}
{% block content %}

<section class="tight">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow"><a href="/crystals/" style="color:var(--plum); text-decoration:none;">Crystals</a> &rsaquo; {{ crystal.name }}</p>
      <h1>{{ crystal.name }}</h1>
      <p class="hero-lede">{{ crystal.description }}</p>
    </div>
  </div>
</section>

<section class="tight">
  <div class="wrap">
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
  </div>
</section>

<section class="tight">
  <div class="wrap" style="display:flex; gap:16px; flex-wrap:wrap; align-items:center; justify-content:space-between;">
    <a class="btn btn-ghost" href="/crystals/">&larr; Back to all categories</a>
    <a class="btn btn-primary" href="/contact/">Enquire about {{ crystal.name }}</a>
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
    f.write(category_tmpl)
print("crystal_category.html template written")

print("\nAll done. Now update build.py manually for sub-page generation.")
