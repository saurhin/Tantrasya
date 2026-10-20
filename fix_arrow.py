with open("static/css/style.css", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "btn-ghost::after" in line and "content:" in line:
        lines[i] = '.btn-ghost::after { content: "\\2192"; transition: transform 0.18s ease; }\n'
        print(f"Fixed line {i+1}: {lines[i].strip()}")

with open("static/css/style.css", "w", encoding="utf-8") as f:
    f.writelines(lines)
print("Done")
