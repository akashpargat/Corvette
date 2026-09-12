"""Assemble the static dashboard into ./site with the data inlined.

The dashboard works two ways: on GitHub Pages it fetches ./data/*.json,
and as a single self-contained file (Claude artifact, email attachment,
double-click on a laptop) it reads the inlined JSON blocks.
"""
from __future__ import annotations

import json
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, "site")


def build(out_dir: str = SITE, inline: bool = True) -> str:
    if os.path.isdir(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(os.path.join(out_dir, "data"))
    for n in os.listdir(os.path.join(HERE, "data")):
        if n.endswith(".json"):
            shutil.copy(os.path.join(HERE, "data", n), os.path.join(out_dir, "data", n))
    html = open(os.path.join(HERE, "dashboard", "index.html"), encoding="utf-8").read()
    css = open(os.path.join(HERE, "dashboard", "styles.css"), encoding="utf-8").read()
    js = open(os.path.join(HERE, "dashboard", "app.js"), encoding="utf-8").read()
    html = html.replace('<link rel="stylesheet" href="styles.css">', f"<style>\n{css}\n</style>")
    html = html.replace('<script src="app.js"></script>', f"<script>\n{js}\n</script>")
    if inline:
        blocks = []
        for name in ("listings", "runs", "market"):
            p = os.path.join(HERE, "data", f"{name}.json")
            if os.path.exists(p):
                raw = open(p, encoding="utf-8").read().replace("</script", "<\\/script")
                blocks.append(f'<script id="data-{name}" type="application/json">{raw}</script>')
        html = html.replace("<!-- INLINE_DATA -->", "\n".join(blocks))
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    open(os.path.join(out_dir, ".nojekyll"), "w").close()
    return os.path.join(out_dir, "index.html")


if __name__ == "__main__":
    print(build())
