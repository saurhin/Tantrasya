# Tantrasya.in — Architecture

Last updated: 10 Oct 2026, after the crystal-gallery caption redesign (name moved
below the photo, bigger gap between tiles).
This file replaced the older Antigravity/Sonnet 4.6 `ARCHITECTURE.md` on 9 Oct 2026 —
that one described an earlier plan (blog, consultations, services) that is no longer
how the live site works. This version describes what is actually built, and is kept
current as changes ship.

**Keep this file current**: any time a change is made to templates, build.py, content
structure, or the live page list, update the relevant section below in the same pass.

---

## 1. What this is

A static site generator written in plain Python (Jinja2 + markdown), no Ruby/Jekyll,
no Node. `python build.py` reads `content/` and `templates/`, and writes a finished
static site into `docs/`, which GitHub Pages serves directly. `CNAME` in `docs/` points
the custom domain (tantrasya.in, on Hostinger) at GitHub Pages.

```
python build.py            # one-off build into docs/
python build.py --serve    # build + local preview server with auto-rebuild
```

## 2. Live pages (what build.py actually generates)

18 pages, all wired into the nav/footer:

| URL | Template | Source |
|---|---|---|
| `/` | `home.html` | `content/pages/home.md` |
| `/paranormal-investigation/` | `paranormal.html` | `content/pages/paranormal-investigation.md` |
| `/occult-practice/` | `occult.html` | `content/pages/occult-practice.md` |
| `/about/` | `about.html` | `content/pages/about.md` |
| `/contact/` | `contact.html` | `content/pages/contact.md` |
| `/titles-note/` | `titles_note.html` | `content/pages/titles-note.md` |
| `/crystals/` | `crystals.html` | `content/pages/crystals.md` + `CRYSTALS` list in `build.py` |
| `/crystals/{slug}/` × 11 | `crystal_category.html` | `CRYSTALS` list in `build.py` (no per-category .md files) |
| `/404.html` | `404.html` | — |

Plus `robots.txt`, `sitemap.xml`, `CNAME` written straight into `docs/`.

Nav bar: Home · Paranormal Investigation · Occult Practice · Crystals · About · Contact,
plus a persistent "Discuss a case" button. Footer repeats these and adds the titles-note link.

### Crystals section
`CRYSTALS` (top of `build.py`) is the single source of truth for the 11 categories —
slug, display name, one-line description. Each category gets:
- A cover photo at `static/images/crystals/{slug}.jpg` — shown on the `/crystals/`
  grid (uses its own `.crystal-card` styling, separate from the gallery below). Falls
  back to a text placeholder tile if the file is missing (`onerror` in
  `templates/crystals.html`).
- A folder `static/images/crystals/{slug}/` — every image file in it (any of
  `.jpg .jpeg .png .webp .gif`) is auto-detected by `build.py`, no registration needed.
  **The filename is the caption**: `rose-quartz.jpg` → "Rose Quartz" label. Hyphens/
  underscores become spaces, title-cased (`caption_from_filename()` in `build.py`).
  Empty folder → "Photos coming soon" message.
- **Caption placement (changed 10 Oct 2026)**: the name sits in the cream space
  *below* each photo, not overlaid on top of it — a small marigold rule under the
  name is the only decoration. This was a deliberate fix: the old style (white text
  over a dark gradient, on top of the photo) washed out and became unreadable on
  light/cream-toned photos. Each photo+caption is one `.gallery-card`; only the photo
  (`.gallery-item`) is clickable. Grid gap increased (16px → 28–36px) so tiles don't
  feel cramped. The lightbox (enlarged view) also shows the caption below the big
  photo, white text on the dark backdrop — this looked fine when first built but
  turned out to have its own separate bug (caption could overlap the photo on
  common screen sizes), fixed 16 Oct — see §5.
- Click-to-enlarge lightbox (full-size image + caption, dark backdrop, Esc/backdrop/×
  to close) — built into `crystal_category.html` + `static/css/crystals.css`.
- Prev/All/Next footer nav between categories, wraps to two lines on mobile
  (fixed 8 Oct — see §5).

As of this writing: all 11 cover photos are done. Only `bracelets/` has photos inside
its detail folder (3 test files, not yet renamed to real stone names — see §4). The
other 10 category folders are empty and show "Photos coming soon".

## 3. Templates & content

```
templates/
  base.html              nav, footer, <head>, asset version query string
  home.html, paranormal.html, occult.html, about.html,
  contact.html, titles_note.html, crystals.html,
  crystal_category.html  — all live, all used
  404.html                — live

content/pages/*.md        front-matter + markdown body per standalone page
                           (home/paranormal/occult pages: most real copy actually
                           lives in the .html templates, not the .md — .md is
                           mostly front-matter for those three)
```

### Dead weight still sitting in the project (not built, not linked, safe to ignore or delete)
- `templates/blog_index.html`, `blog_post.html`, `consultations.html`,
  `experiences.html`, `service.html`, `services_index.html` — left over from an
  earlier version of the brief (blog + paid consultations + service catalogue).
  `build.py` never renders these; nothing links to them. They cost nothing live but
  clutter the templates folder.
- `content/blog/`, `content/services/` — empty, same story.
- `static/images/blog/`, `chakras.png`, `hecate.png`, `hero_image.jpg` — **deleted
  10 Oct 2026** (confirmed unreferenced outside the dead blog templates; removing
  them also got the project zip under the 30 MB upload limit). If needed again,
  they're still in earlier zips.
- Root-level one-off scripts from the Antigravity session: `write_cat_tmpl.py`,
  `write_crystals.py`, `write_crystals_full.py`, `fix_arrow.py`, `fix_nav.py` — these
  were used once to scaffold the crystal templates/content and are not part of the
  build pipeline (`build.py` doesn't call them). Hardcoded Windows paths from that
  machine. Safe to delete whenever; not deleted yet because it hasn't been asked for.
- `README.md` — also inherited from Antigravity, describes the old blog/consultations
  plan. Not corrected yet.

None of the above affects the live site — `docs/` only contains what's actually linked.

## 4. Known content gaps (not bugs — waiting on real content)

- 10 of 11 crystal categories have no detail photos yet (cover photo only).
- `bracelets/` detail folder has 3 placeholder photos: `bracelets1.jpg`,
  `bracelets2.jpg`, `bracelets..jpg` (typo'd double-dot filename, renders fine as a
  caption but should be renamed/removed when real photos go in).
- To add real photos to any category: drop files named after the stone
  (`clear-quartz.jpg`) into `static/images/crystals/{slug}/`, rebuild, push. No code
  changes needed — the filename becomes the caption automatically.

## 5. Fix log

Chronological, most recent first. Add a line here every time a change ships.

- **16 Oct 2026** — Fixed: the enlarged (lightbox) photo caption could land on
  top of the photo instead of below it, on common screen sizes (confirmed on
  1366×768, a typical laptop resolution, and any short/wide window). Cause:
  the caption was pinned a fixed 28px from the *browser window's* bottom edge
  (`position: fixed`), not tied to the photo's actual bottom edge — so on a
  short window, or a landscape-shaped photo that renders tall, the two
  overlapped. Fix: the photo and its caption are now one column
  (`.lightbox-frame`) that centers as a unit, so the caption always sits a
  fixed 16px below wherever the photo's bottom edge actually lands, on any
  screen size or photo shape. Verified at 1200×650, 1366×768, 1200×1000 and
  on mobile (390×844) — no overlap at any of them. The gallery-grid caption
  (Option A, name below the photo on cream) was not affected by this bug and
  needed no change.
- **10 Oct 2026** — Deleted unused dead-weight images (`static/images/blog/`,
  `chakras.png`, `hecate.png`, `hero_image.jpg`, ~16 MB) — confirmed referenced only
  by the never-rendered blog templates, so unreachable on the live site either way.
  Also got the project zip back under the 30 MB delivery limit.
- **10 Oct 2026** — Crystal gallery caption redesign: name moved from an overlay on
  the photo (white text + dark gradient, which washed out on light/cream photos) to
  the cream space below the photo, with a small marigold rule. Grid gap widened for
  breathing room. Markup is now `.gallery-card` (photo + caption as siblings) instead
  of the caption being absolutely positioned inside `.gallery-item`. Lightbox caption
  left unchanged at the time — incorrectly assumed to already be fine; it had its own
  overlap bug, found and fixed 16 Oct (see that entry above).
- **9 Oct 2026** — Rewrote this ARCHITECTURE.md from scratch to match the real,
  current codebase (previous version was the stale Antigravity doc describing an
  unbuilt blog/consultations plan). Established going forward: update §5 here with
  every change.
- **8 Oct 2026** — Crystal photo captions (first version): filename → display caption,
  shown on gallery thumbnails and in the lightbox (`caption_from_filename()` in
  `build.py`).
- **8 Oct 2026** — Fixed: prev/All/Next nav row (`.crystal-nav`) overflowed off the
  right edge on phones (~390px) on every one of the 11 category pages — two
  `min-width: 140px` columns didn't fit next to the middle button. Added a
  `@media (max-width: 640px)` rule so it wraps and centers instead.
- **7 Oct 2026** — Added "Crystals" to the contact form's subject dropdown (was
  missing after the Crystals section was added).
- **7 Oct 2026** — Re-applied three fixes that had regressed in a zip built from an
  earlier branch: mobile hero layout (Paranormal/Occult/About stacked to one column
  again instead of squeezing into a 67px image), missing `og-cover.jpg` social
  preview image, contact form submit button reverting to the literal string
  "Send message" instead of its original label after sending.
- **19 Sep 2026** — First pass on the Antigravity/Sonnet 4.6 build: mobile hero fix,
  `og-cover.jpg` generated, form button label fix, removed then-unused
  blog/consultations/services templates (these were later reintroduced in a
  subsequent zip — see 7 Oct entry — and are currently still present as dead code,
  §3).

## 6. Design tokens (static/css/style.css)

```
--cream        #FBEEDA   page background
--cream-deep   #F5DFB8   alternating section background
--ink          #3A2013   primary text
--ink-soft     #6E4B34   secondary text
--marigold     #E89327   primary accent
--terracotta   #C1442C   secondary accent
--plum         #6E2D63   mystical accent
--moss         #4C6B37   grounding accent
--indigo       #2B2350   dark section background
--font-display "Fraunces", Georgia, serif
--font-body    "Work Sans", sans-serif
```
No black, no grey/pastel — warm palette by design (stated requirement).

## 7. Site identity / config (top of build.py)

```
name:        Tantrasya
tagline:     Paranormal Investigation & Occult Practice
url:         https://tantrasya.in
practitioner: Saurhin
email:       Tantrasya@gmail.com
city:        Mumbai
formspree:   https://formspree.io/f/xjykkejp   (contact form backend)
```

## 8. Not e-commerce

The Crystals section is a catalogue, not a store — no prices, no cart, no checkout.
Every category and every "Enquire" button routes to `/contact/`, where the subject
dropdown includes a "Crystals" option. The intended flow is: browse photos → call or
fill the form → human conversation. This was a deliberate choice, not a missing
feature.
