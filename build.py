#!/usr/bin/env python3
"""
Tantrasya.in static site generator.

Usage:
    python build.py
    python build.py --serve

Reads:
    content/pages/*.md   -> standalone pages (home, about, contact,
                            paranormal-investigation, occult-practice,
                            titles-note)

Writes:
    docs/                -> final static site (GitHub Pages serves from here)
"""

import os
import sys
import shutil
import datetime
import argparse
import http.server
import socketserver
import webbrowser
import markdown
from jinja2 import Environment, FileSystemLoader, select_autoescape

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SITE = {
    "name": "Tantrasya",
    "tagline": "Paranormal Investigation & Occult Practice",
    "url": "https://tantrasya.in",
    "practitioner": "Saurhin",
    "email": "Tantrasya@gmail.com",
    "phone": "",
    "city": "Mumbai",
    "formspree_endpoint": "https://formspree.io/f/xjykkejp",
    "instagram": "",
    "nav": [
        {"label": "Home",                     "href": "/"},
        {"label": "Paranormal Investigation", "href": "/paranormal-investigation/"},
        {"label": "Occult Practice",          "href": "/occult-practice/"},
        {"label": "About",                    "href": "/about/"},
        {"label": "Contact",                  "href": "/contact/"},
    ],
}

ROOT          = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR   = os.path.join(ROOT, "content")
TEMPLATES_DIR = os.path.join(ROOT, "templates")
STATIC_DIR    = os.path.join(ROOT, "static")
OUTPUT_DIR    = os.path.join(ROOT, "docs")

# Appended to CSS/JS links as ?v=... so browsers always fetch the latest version.
ASSET_VERSION = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

md = markdown.Markdown(extensions=["extra", "meta", "toc", "smarty"])

MONTH_NAMES = [
    "", "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_front_matter(raw_text):
    """Parse simple `key: value` YAML-style front matter without PyYAML.
    Handles strings (quoted or bare), integers, and YYYY-MM-DD dates."""
    front = {}
    for line in raw_text.strip().splitlines():
        line = line.rstrip()
        if not line or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, _, value = line.partition(":")
        key   = key.strip()
        value = value.strip()

        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]

        if len(value) == 10 and value[4] == "-" and value[7] == "-" and value[:4].isdigit():
            try:
                y, m, d = value.split("-")
                value = datetime.date(int(y), int(m), int(d))
            except ValueError:
                pass
        elif value.isdigit():
            value = int(value)

        front[key] = value
    return front


def read_markdown(path):
    """Split a markdown file into (front_matter_dict, html_body)."""
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()

    if raw.startswith("---"):
        parts = raw.split("---", 2)
        front = parse_front_matter(parts[1])
        body  = parts[2]
    else:
        front = {}
        body  = raw

    md.reset()
    html = md.convert(body.strip())
    return front, html


def load_dir(path):
    """Load every .md file in a directory into a list of dicts with 'content' html."""
    items = []
    if not os.path.isdir(path):
        return items
    for fname in sorted(os.listdir(path)):
        if not fname.endswith(".md"):
            continue
        front, html = read_markdown(os.path.join(path, fname))
        front["content"] = html
        front.setdefault("slug", os.path.splitext(fname)[0])
        items.append(front)
    return items


def write_page(rel_path, html):
    """Write rendered html to docs/rel_path/index.html (pretty URLs)."""
    if rel_path in ("", "/", "index"):
        out_dir = OUTPUT_DIR
    else:
        out_dir = os.path.join(OUTPUT_DIR, rel_path.strip("/"))
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)


def canonical(rel_path):
    rel_path = rel_path.strip("/")
    if not rel_path:
        return SITE["url"] + "/"
    return f"{SITE['url']}/{rel_path}/"


env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=select_autoescape(["html"]),
    trim_blocks=True,
    lstrip_blocks=True,
)


# ---------------------------------------------------------------------------
# Build steps
# ---------------------------------------------------------------------------

def clean():
    """Remove generated files from docs/ without deleting the folder itself.
    This means a running --serve server keeps its lock and doesn't need
    to be stopped before a rebuild."""
    if not os.path.isdir(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        return
    for item in os.listdir(OUTPUT_DIR):
        full = os.path.join(OUTPUT_DIR, item)
        # keep the static/ copy — copy_static() will overwrite it anyway
        if item == "static":
            shutil.rmtree(full, ignore_errors=True)
        elif os.path.isdir(full):
            shutil.rmtree(full, ignore_errors=True)
        else:
            try:
                os.remove(full)
            except PermissionError:
                pass  # skip locked files (e.g. the serve cwd itself)


def copy_static():
    dest = os.path.join(OUTPUT_DIR, "static")
    shutil.copytree(STATIC_DIR, dest)
    with open(os.path.join(OUTPUT_DIR, "CNAME"), "w", encoding="utf-8") as f:
        f.write("tantrasya.in\n")
    open(os.path.join(OUTPUT_DIR, ".nojekyll"), "w").close()


def render(template_name, out_path, **context):
    tmpl = env.get_template(template_name)
    context.setdefault("site", SITE)
    context.setdefault("canonical_url", canonical(out_path))
    context.setdefault("year", datetime.date.today().year)
    context.setdefault("asset_version", ASSET_VERSION)
    html = tmpl.render(**context)
    write_page(out_path, html)
    return canonical(out_path)


def build():
    clean()
    copy_static()

    urls = []  # for sitemap.xml

    # -- Standalone pages ---------------------------------------------------
    pages         = load_dir(os.path.join(CONTENT_DIR, "pages"))
    pages_by_slug = {p["slug"]: p for p in pages}

    # Home
    home = pages_by_slug.get("home", {})
    urls.append(render(
        "home.html",
        "",
        page=home,
        title=f"{SITE['name']} | {SITE['tagline']}",
        meta_description=home.get("description", SITE["tagline"]),
    ))

    # Paranormal Investigation
    paranormal = pages_by_slug.get("paranormal-investigation", {})
    urls.append(render(
        "paranormal.html",
        "paranormal-investigation",
        page=paranormal,
        title=f"Paranormal Investigation | {SITE['name']}",
        meta_description=paranormal.get(
            "description",
            "Tantrasya investigates reported paranormal and unexplained experiences — "
            "unusual activity, disturbances, apparitions and more.",
        ),
    ))

    # Occult Practice
    occult = pages_by_slug.get("occult-practice", {})
    urls.append(render(
        "occult.html",
        "occult-practice",
        page=occult,
        title=f"Occult Practice | {SITE['name']}",
        meta_description=occult.get(
            "description",
            "Traditional tantra, mantra and ritual practices "
            "undertaken where such an approach is appropriate.",
        ),
    ))

    # About
    about = pages_by_slug.get("about", {"title": "About", "content": ""})
    urls.append(render(
        "about.html",
        "about",
        page=about,
        title=f"About | {SITE['name']}",
        meta_description=about.get("description", SITE["tagline"]),
    ))

    # Contact
    contact = pages_by_slug.get("contact", {"title": "Contact", "content": ""})
    urls.append(render(
        "contact.html",
        "contact",
        page=contact,
        title=f"Contact | {SITE['name']}",
        meta_description=contact.get("description", SITE["tagline"]),
    ))

    # A Note on Titles, Masters & Everything Else
    titles_note = pages_by_slug.get("titles-note", {"title": "A Note on Titles", "content": ""})
    urls.append(render(
        "titles_note.html",
        "titles-note",
        page=titles_note,
        title=f"A Note on Titles, Masters & Everything Else | {SITE['name']}",
        meta_description=titles_note.get(
            "description",
            "On the quiet path Tantrasya chooses instead of grand titles, "
            "endless modalities and louder claims of spiritual mastery.",
        ),
    ))

    # -- 404 ---------------------------------------------------------------
    tmpl = env.get_template("404.html")
    with open(os.path.join(OUTPUT_DIR, "404.html"), "w", encoding="utf-8") as f:
        f.write(tmpl.render(
            site=SITE,
            title=f"Page not found | {SITE['name']}",
            asset_version=ASSET_VERSION,
        ))

    # -- sitemap.xml & robots.txt ------------------------------------------
    sitemap_entries = "\n".join(
        f"  <url><loc>{u}</loc></url>" for u in urls
    )
    sitemap_xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{sitemap_entries}\n"
        "</urlset>\n"
    )
    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_xml)

    robots_txt = (
        "User-agent: *\n"
        "Allow: /\n\n"
        f"Sitemap: {SITE['url']}/sitemap.xml\n"
    )
    with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots_txt)

    print(f"Built {len(urls)} pages into {OUTPUT_DIR}/")


def serve(port=8080, open_browser=True):
    """Serve the built docs/ folder locally — preview before push."""
    if not os.path.isdir(OUTPUT_DIR):
        print("No docs/ folder found — building first...")
        build()

    os.chdir(OUTPUT_DIR)
    handler = http.server.SimpleHTTPRequestHandler
    url = f"http://localhost:{port}/"

    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Serving {OUTPUT_DIR} at {url}")
        print("Press Ctrl+C to stop.")
        if open_browser:
            webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Build (and optionally serve) the Tantrasya static site."
    )
    parser.add_argument(
        "--serve", action="store_true",
        help="Build the site, then serve docs/ locally and open it in your browser.",
    )
    parser.add_argument("--port", type=int, default=8080, help="Port to serve on (default: 8080).")
    parser.add_argument("--no-browser", action="store_true", help="Don't auto-open a browser tab.")
    args = parser.parse_args()

    build()

    if args.serve:
        serve(port=args.port, open_browser=not args.no_browser)
