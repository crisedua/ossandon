#!/usr/bin/env python3
"""Inline the page, engine, fonts and portraits into one self-contained HTML file.

Writes preview/cisent-preview.html and the repo-root index.html (what Vercel
serves at "/"). Run from anywhere: python3 scrollcraft/builds/cisent/bundle.py
"""
import base64
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def data_uri(path, mime):
    return f"data:{mime};base64," + base64.b64encode((HERE / path).read_bytes()).decode()


s = (HERE / "index.html").read_text()
s = s.replace('<link rel="stylesheet" href="scrollcraft.css">',
              "<style>\n" + (HERE / "scrollcraft.css").read_text() + "\n</style>")
s = s.replace('<script src="scrollcraft.js"></script>',
              "<script>\n" + (HERE / "scrollcraft.js").read_text() + "\n</script>")
s = re.sub(r'<link rel="preload"[^>]*>\n', "", s)
for f in ["archivo-latin-standard-normal", "archivo-latin-standard-italic",
          "ibm-plex-mono-latin-400-normal", "ibm-plex-mono-latin-500-normal"]:
    s = s.replace(f'url("assets/fonts/{f}.woff2")', f'url("{data_uri(f"assets/fonts/{f}.woff2", "font/woff2")}")')
for k in ["salaberry", "ossandon", "uauy", "hormero"]:
    s = s.replace(f'src="assets/team/{k}.webp"', f'src="{data_uri(f"assets/team/{k}.webp", "image/webp")}"')
assert 'src="assets/' not in s and 'url("assets/' not in s, "an asset was left unbundled"

for out in (HERE / "preview" / "cisent-preview.html", ROOT / "index.html"):
    out.write_text(s)
    print(f"wrote {out.relative_to(ROOT)} ({len(s) // 1024} KB)")
