# Tantrasya.in — Static Site (Python build)

This is the Phase 1 redesign of tantrasya.in: a Python-built static site
(Jinja2 + Markdown), styled with a warm, colorful, "seen and unseen" identity
— no black, no grey, no washed-out pastel. Content lives in Markdown; the
build script turns it into the `docs/` folder that GitHub Pages serves.

## 1. Set up (one-time)

You already have Python installed. From the project folder, install the
three dependencies:

```
pip install jinja2 markdown
```

## 2. Build the site

Every time you change content or templates, rebuild:

```
python build.py
```

This regenerates the entire `docs/` folder from scratch (nothing needs to
be edited by hand in `docs/` — it's fully generated output).

## 3. Preview locally before pushing

Build and serve in one step — this also opens your browser automatically:

```
python build.py --serve
```

Then open `http://localhost:8080/` if it doesn't open on its own. Press
`Ctrl+C` to stop the server. Useful flags:

- `python build.py --serve --port 3000` — use a different port
- `python build.py --serve --no-browser` — don't auto-open a browser tab

(You can still just run `python build.py` on its own — it builds `docs/`
without serving it, if that's all you need.)

## 4. Publish

Commit and push `docs/` to GitHub as usual. Since GitHub Pages is already
set to serve from `/docs` on your repo, and `CNAME` inside `docs/` keeps
tantrasya.in pointed correctly, publishing is just:

```
git add .
git commit -m "Update site"
git push
```

## Before you go live — three things to finish

1. **Contact form** — open `build.py` and replace
   `formspree_endpoint` with your real Formspree form URL (create a free
   form at formspree.io using your inbox email). Until you do this, the
   contact form will not deliver messages anywhere.
2. **Testimonials** — `templates/home.html` and `templates/experiences.html`
   each contain clearly marked placeholder testimonials. Swap in the real
   ones from the current site.
3. **About page bio** — `content/pages/about.md` has placeholder biographical
   copy marked with `[...]`. Replace with Saurhin's real background.

Also double-check the `email` field near the top of `build.py` — it's set
to a placeholder inbox.

## Editing content

- **Pages** (About, Consultations, Experiences, Contact, Home copy):
  `content/pages/*.md`
- **Services**: `content/services/*.md` — one file per service. Add a new
  file here to add a new service; it will automatically appear on the
  Services page and in navigation-adjacent lists.
- **Blog**: `content/blog/*.md` — add a new Markdown file with front matter
  (title, date, category, description, slug) to publish a new article. No
  other step is needed — the build script picks it up automatically.

Every content file uses this front-matter format:

```markdown
---
title: "Article Title"
description: "Short SEO description"
date: "2026-08-15"
category: "Crystals"
slug: "article-slug"
image: "article-slug.jpg"
---

Article content in Markdown starts here.
```

## Adding real photos to blog articles

Right now, blog cards and article pages show a soft color gradient where a
photo would go — that's just a placeholder until you add real images.

1. Drop your image file into `static/images/blog/` — e.g.
   `static/images/blog/crystal-myths.jpg`. Landscape photos around
   1600×1100px work best; keep file size reasonable (under ~400KB) so
   pages load fast.
2. In that article's `.md` file, add an `image:` line to the front matter
   with just the filename:
   ```yaml
   image: "crystal-myths.jpg"
   ```
3. Run `python build.py --serve` again.

That's it — the image will automatically appear on the blog listing card,
the homepage "Recent notes" card, related-article cards, and as a large
cover image at the top of the article itself. Articles without an `image:`
line keep showing the gradient placeholder, so you can add photos
gradually, article by article — no need to do them all at once.

You can add photos inside an article's body too, using normal Markdown:

```markdown
![A description of the photo](/static/images/blog/some-photo.jpg)
```

## Adding a photo to the homepage hero (the big arch shape)

That purple/indigo arch shape at the top of the homepage is also just a
gradient placeholder, same idea as the blog cards.

1. Drop a photo into `static/images/` — e.g. `static/images/hero.jpg`
   (portrait orientation works best, since the arch is taller than wide —
   roughly 1000×1250px)
2. Open `content/pages/home.md`, and add a line to the front matter:
   ```yaml
   hero_image: "hero.jpg"
   ```
3. Run `python build.py --serve` again

The photo will fill the arch shape, with the "8 practice areas" badge
sitting on top of it. No `hero_image` line yet? It keeps the gradient.



Same idea — put the file in `static/images/`, then reference it in the
relevant template (e.g. `templates/about.html`) with a normal `<img>` tag,
or inside the Markdown content itself as shown above. Ask if you'd like
help wiring up a specific spot (e.g. a portrait photo on the About page,
or a photo per service).

## Project structure

```
tantrasya-py/
├── build.py                  ← the generator — run this to build the site
├── content/
│   ├── pages/                ← home, about, consultations, experiences, contact
│   ├── services/             ← one .md file per service (8 total)
│   └── blog/                 ← blog articles
├── templates/                ← Jinja2 HTML templates (design lives here)
├── static/
│   ├── css/style.css         ← all design tokens & styling
│   ├── js/main.js            ← mobile nav + contact form handling
│   └── images/               ← favicon etc.
└── docs/                     ← GENERATED OUTPUT — what GitHub Pages serves
```

## Design notes

- **Colors**: warm papaya cream background, marigold gold, sindoor
  terracotta, twilight plum, tulsi green, deep indigo — drawn from ritual
  materials rather than a generic wellness palette. All tokens are CSS
  variables at the top of `static/css/style.css` if you want to adjust any
  of them.
- **Type**: Fraunces (display) + Work Sans (body), loaded from Google Fonts.
- **The arch motif**: the recurring curved shape in the logo mark, hero
  image and section dividers is a deliberate "threshold" signature —
  nodding to Tantrasya's "seen and unseen" positioning.
- **SEO**: every page gets a unique title, meta description, canonical URL,
  and Open Graph tags automatically from front matter. `sitemap.xml` and
  `robots.txt` are regenerated on every build.
