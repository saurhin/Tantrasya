with open("templates/crystal_category.html", "r", encoding="utf-8") as f:
    content = f.read()

# Remove &larr; from prev button (CSS btn-ghost adds → but not ←, so prev needs different class)
# Simplest fix: use btn-outline for both nav buttons with explicit arrows in text only
content = content.replace(
    '<a class="btn btn-ghost" href="/crystals/{{ prev_crystal.slug }}/">&larr; {{ prev_crystal.name }}</a>',
    '<a class="btn btn-outline" href="/crystals/{{ prev_crystal.slug }}/">\u2190 {{ prev_crystal.name }}</a>'
)
content = content.replace(
    '<a class="btn btn-ghost" href="/crystals/{{ next_crystal.slug }}/">{{ next_crystal.name }} &rarr;</a>',
    '<a class="btn btn-outline" href="/crystals/{{ next_crystal.slug }}/">{{ next_crystal.name }} \u2192</a>'
)

with open("templates/crystal_category.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Done")
