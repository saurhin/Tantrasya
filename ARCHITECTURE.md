# Tantrasya.in — Architecture & Build Write-Up

*A technical record of how the Phase 1 redesign was planned and built.*

---

## 1. Where this started

You brought a detailed Phase 1 scope document — 29 sections covering
objective, visual direction, sitemap, page-by-page content requirements,
consultation pricing, blog structure, technical architecture, SEO,
responsiveness, and explicit Phase 2 exclusions. That document was the
brief; everything below is how it was actually built.

Three requirements from that brief shaped every technical decision:

1. **Static site, GitHub Pages, custom domain via Hostinger** — no backend,
   no database, no paid CMS.
2. **Markdown-based blog**, publishable by adding a file — no complicated
   CMS.
3. **"Existing Python/Markdown approach... reused and adapted"** — you'd
   already started down a Python path locally (`D:\tantrasya-python\
   tantrasya-py`), not Ruby/Jekyll, so the generator had to be Python.

Everything in this document follows from those three constraints.

---

## 2. The core architectural decision: static generation, not a live app

The site is **pre-built once, on your machine, into plain HTML/CSS/JS**,
then that output is what gets hosted. Nothing runs Python on the server.

```
Markdown content (content/)
         +
Jinja2 templates (templates/)
         │
         ▼
      build.py            ← runs on YOUR computer only
         │
         ▼
  docs/  (plain .html, .css, .js, images)
         │
         ▼
     git push
         │
         ▼
   GitHub Pages serves docs/ as-is
         │
         ▼
     tantrasya.in  (via Hostinger DNS → GitHub Pages)
```

**Why this matters:** GitHub Pages can only serve static files — it has no
Python runtime. So Python's job ends the moment `docs/` is generated.
Everything after that (hosting, the custom domain, HTTPS) works exactly
the way your current site already does, because from GitHub's point of
view, nothing has changed about *what kind* of site this is — only what's
inside it.

This directly satisfies scope section 20 ("Preferred architecture... Static
HTML/CSS/JS → GitHub Repository → GitHub Pages") and section 21
("Separation of Responsibilities" — Python handles generation only, never
serving).

---

## 3. Why a hand-built generator instead of Jekyll, Hugo, or Eleventy

The scope document mentioned reusing "the existing Python/Markdown
approach." Rather than introducing Ruby (Jekyll) or a JS toolchain (Hugo,
Eleventy, 11ty), the generator is a single dependency-light Python script
using three libraries:

| Library | Job |
|---|---|
| **Jinja2** | Template engine — same templating language used by Flask/Django, well documented, easy to extend |
| **Markdown** | Converts article/page bodies to HTML |
| *(front matter)* | Parsed by a small hand-written parser in `build.py` — not PyYAML, deliberately, after a dependency conflict surfaced on your machine. One less thing that can fail to `pip install` |

This keeps the whole toolchain to two `pip install` commands
(`jinja2 markdown`) and one script. No Node.js, no Ruby, no build
framework to learn — which matters since you're the one maintaining this
long-term, not a dev team.

---

## 4. Content model: everything is a file

Per section 16 of the scope ("allow Saurhin to create an article by adding
a Markdown file"), the entire site's content lives as plain `.md` files
with YAML-style front matter — no database, no admin panel.

```
content/
├── pages/          → Home, About, Consultations, Experiences, Contact
├── services/        → one file per service (8 files = 8 services)
└── blog/             → one file per article
```

Each file looks like this:

```markdown
---
title: "Crystal Healing"
slug: "crystal-healing"
order: 1
icon: "gem"
summary: "Crystal-based energy work and guidance for focus, balance and support."
---

Body content in Markdown goes here.
```

`build.py` reads every file in a folder, turns the Markdown body to HTML,
and hands the front-matter fields to a template as variables. **Publishing
a new blog post or adding a new service is: drop in a new `.md` file, run
`python build.py`.** No template editing required for routine content
work — this satisfies the "clean, maintainable Git/Markdown publishing
workflow" required in section 1.13 and the blog requirements in section 16.

---

## 5. Templates: one shared shell, page-specific bodies

```
templates/
├── base.html              ← shared header, nav, footer, <head>/SEO block
├── home.html
├── about.html
├── services_index.html
├── service.html            ← one template renders all 8 service pages
├── consultations.html
├── experiences.html
├── contact.html
├── blog_index.html
├── blog_post.html
└── 404.html
```

Jinja2's template inheritance (`{% extends "base.html" %}`) means the
header/nav/footer are defined exactly once. Change the phone number, the
nav links, or the footer copy in `base.html`, and it updates across all 18
generated pages in one edit — no risk of the About page's footer drifting
out of sync with the Contact page's.

`service.html` is a single template, not eight — `build.py` loops over
every file in `content/services/` and renders each one through it. Adding
a ninth service later means adding one `.md` file; the template, routing,
and navigation all handle it automatically, matching the scope's
requirement that "the service architecture should allow new services to
be added later without restructuring the entire website" (section 10).

---

## 6. `build.py`: what it actually does, step by step

1. **Load** every Markdown file in `content/services/` and `content/blog/`,
   parsing front matter and converting the body to HTML.
2. **Sort** services by their `order` field, blog posts by `date`
   (newest first).
3. **Render** each service through `service.html`, each post through
   `blog_post.html`, writing output to `docs/services/<slug>/index.html`,
   `docs/blog/<slug>/index.html`, etc. — pretty URLs, no `.html` extension
   visible.
4. **Render** the fixed pages (home, about, consultations, experiences,
   contact) with their own dedicated templates.
5. **Generate `sitemap.xml`** from every URL just rendered, and
   **`robots.txt`** pointing to it.
6. **Copy** the whole `static/` folder (CSS, JS, images) into
   `docs/static/`.
7. **Write `CNAME`** (`tantrasya.in`) and `.nojekyll` into `docs/`, so
   GitHub Pages keeps serving your custom domain and doesn't try to run
   its own Jekyll processing over the output.

Every run wipes and fully regenerates `docs/` — nothing in that folder is
ever hand-edited, which is what makes it safe to treat `docs/` as pure
build output rather than a second copy of your content.

### `--serve`

`python build.py --serve` runs the same build, then starts a local web
server (`http://localhost:8080/`) and opens it in your browser — the
same static server logic GitHub Pages uses in production, run locally, so
what you preview is what actually goes live.

### Cache-busting

Every CSS/JS `<link>`/`<script>` tag is suffixed with `?v=<timestamp>`,
regenerated on every build. This forces browsers to fetch the latest
version instead of serving a stale cached copy after a design change —
a real issue we hit and fixed during development.

---

## 7. Design system

### Color

Scope section 3 asked for warm, non-black, non-grey, non-generic-pastel
colors; a later request asked explicitly for something more colorful and
saturated than a muted palette. The resolution: a palette pulled from
**materials used in Indian ritual practice** rather than a generic
wellness-brand palette —

| Token | Color | Drawn from |
|---|---|---|
| `--cream` | warm papaya | base surface |
| `--marigold` | marigold gold | ritual flowers |
| `--terracotta` | sindoor red | vermillion |
| `--plum` | twilight plum | dusk sky, mystical |
| `--moss` | tulsi green | grounding |
| `--indigo` | deep dusk indigo | replaces black entirely for dark sections |
| `--ink` | ember brown | replaces black/grey for all text |

All defined as CSS custom properties at the top of `static/css/style.css`
— changing a brand color site-wide is a one-line edit.

### Type

**Fraunces** (display serif — warm, characterful curves, avoids the
generic "wellness Playfair" look) paired with **Work Sans** (body). Loaded
from Google Fonts in `base.html`.

### The arch motif

A recurring curved "threshold" shape — in the logo mark, the homepage
hero image frame, and conceptually through the site — chosen to echo the
brand line "an intimate practice exploring the seen and unseen" (section
5) without borrowing any specific religious iconography.

### Layout

Section 25 asked for calm, subtle interaction — gentle hover states,
smooth transitions, no heavy parallax or flashing effects. Only CSS
transitions are used (button hover lifts, card hover shadows); no
animation libraries.

---

## 8. Page-by-page mapping back to your scope

| Scope section | What was built |
|---|---|
| §6–7 Navigation & Sitemap | `base.html` nav list drives header + mobile menu + footer from one config array in `build.py` |
| §8 Homepage | Hero, trust strip, about teaser, 8-service grid, testimonials, consultations teaser, 3 featured posts, closing CTA |
| §9 About | Placeholder structure ready for Saurhin's real bio — marked, not fabricated (per your explicit "do not invent credentials" instruction) |
| §10 Services | 8 individual pages, one shared template, auto-listed on `/services/` |
| §11 Consultations & Fees | Full pricing table transcribed exactly: ₹1,500 / ₹501 / ₹5,100 / ₹7,100+travel / material+₹1,000 |
| §12 Experiences | Placeholder testimonial cards, clearly marked for replacement — never fabricated |
| §13–15 Contact form | Name / Email / Enquiry type / Message fields, Formspree endpoint, honeypot spam field, JS-driven success/error states, no backend |
| §16–19 Blog | Markdown + front matter, categories, clean URLs, related-posts, image support |
| §20–21 Technical architecture | Covered in §2–3 above |
| §22 SEO | Every page: unique `<title>`, meta description, canonical URL, Open Graph tags — generated automatically from front matter |
| §23 Responsive design | Mobile nav collapses to a hamburger menu; grid layouts collapse from 4→2→1 columns; hero reflows to single column |
| §24 Performance | No JS frameworks, no animation libraries, system-loaded fonts with `display=swap`, minimal custom JS (~60 lines total) |
| §26 Content integrity | No invented credentials, testimonials, or claims anywhere — every placeholder is explicitly labeled as such in the file |
| §27 Deliverables | All checked off except the three items still pending real content (see below) |
| §28 Phase 2 | Untouched — no marketing, ads, or campaign infrastructure included |

---

## 9. What's real vs. what's still placeholder

Being direct about this, since section 26 was explicit about not
fabricating content:

**Fully real and functional:**
- Consultation pricing (transcribed exactly from your scope doc)
- Service descriptions (written to reflect what you described, but see
  note below)
- Site structure, navigation, SEO, responsive behavior, contact form
  mechanics, blog engine

**Still placeholder — clearly marked in the files, not hidden:**
- **Testimonials** (homepage + Experiences page) — marked
  `[Placeholder — replace with a genuine testimonial]`
- **About page biography** — marked with `[...]` where your real
  background goes
- **Service page body copy** — written to be accurate in *shape* (what
  each service is, how a session runs) but not sourced from your existing
  site's actual wording, since that wasn't provided as text. Worth a pass
  to align with your original phrasing where it matters.
- **Formspree endpoint** — needs your real form ID before the contact
  form actually delivers mail

---

## 10. What's deliberately *not* built (by design, not oversight)

Per section 28 of your scope, explicitly excluded from this phase:

- No marketing/advertising infrastructure
- No analytics beyond what you might add later
- No CMS admin panel — content management is Git + a text editor, by design
- No database — pricing, services, and posts all live as files in the
  repo, which is also your backup
- No server-rendered logic of any kind — the contact form is the only
  "dynamic" piece, and it's handled entirely by a third-party static form
  service (Formspree), keeping the hosting itself 100% static

---

## 11. The day-to-day workflow, going forward

```
1. Edit or add a .md file in content/
2. python build.py --serve      ← preview locally at localhost:8080
3. Happy with it?
4. git add .
5. git commit -m "..."
6. git push                      ← live on tantrasya.in within a few minutes
```

That's the entire publishing loop — no build servers, no deploy keys
beyond what GitHub Pages already had configured, no new infrastructure
to maintain beyond what existed before this rebuild.
