#!/usr/bin/env python3
"""
ATRIA — statischer Seitengenerator.

Setzt die Seiten aus build/pages/*.html in das gemeinsame Gerüst und schreibt
fertiges, abhängigkeitsfreies HTML nach site/. Das Ergebnis ist eingecheckt —
die Website funktioniert also auch ohne diesen Schritt. Der Generator existiert
nur, damit Header, Navigation und Footer nicht in jeder Seite dupliziert werden.

    python3 build/build.py

Markennamen austauschen: BRAND unten ändern und neu bauen.
"""

from __future__ import annotations

import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGES = ROOT / "build" / "pages"
LAYOUT = ROOT / "build" / "layout.html"
LAYOUT_BARE = ROOT / "build" / "layout-bare.html"
OUT = ROOT / "site"

BRAND = "ATRIA"  # Arbeitstitel — Markenrecherche steht aus, siehe docs/11

NAV_KEYS = ["segmente", "produkt", "preise", "demo", "faq"]


def parse_front_matter(text: str) -> tuple[dict, str]:
    """Front matter steht als JSON im ersten HTML-Kommentar der Datei."""
    m = re.match(r"\s*<!--\s*(\{.*?\})\s*-->\s*", text, re.S)
    if not m:
        raise ValueError("Front matter fehlt")
    return json.loads(m.group(1)), text[m.end():]


def render(page_path: pathlib.Path, layout: str, layout_bare: str) -> tuple[pathlib.Path, str]:
    meta, content = parse_front_matter(page_path.read_text(encoding="utf-8"))
    rel = page_path.relative_to(PAGES)
    depth = len(rel.parts) - 1
    base = "../" * depth

    seg = meta.get("seg", "")
    seg_attr = f' data-seg="{seg}"' if seg else ""

    out = layout_bare if meta.get("bare") else layout
    for key in NAV_KEYS:
        out = out.replace(
            "{{cur_%s}}" % key,
            ' aria-current="page"' if meta.get("nav") == key else "",
        )

    out = out.replace("{{content}}", content.strip())

    replacements = {
        "{{title}}": meta["title"],
        "{{description}}": meta["description"],
        "{{path}}": str(rel).replace("\\", "/"),
        "{{base}}": base,
        "{{seg}}": seg,
        "{{segattr}}": seg_attr,
        "{{head}}": meta.get("head", ""),
        "{{demonote}}": meta.get("demonote", ""),
        "{{democta}}": meta.get("democta", "index.html"),
        "{{democtalabel}}": meta.get("democtalabel", "Zur Website"),
    }
    for needle, value in replacements.items():
        out = out.replace(needle, value)

    out = out.replace("ATRIA", BRAND)
    return OUT / rel, out


def main() -> int:
    layout = LAYOUT.read_text(encoding="utf-8")
    layout_bare = LAYOUT_BARE.read_text(encoding="utf-8")
    pages = sorted(PAGES.rglob("*.html"))
    if not pages:
        print("Keine Seiten in build/pages/ gefunden.", file=sys.stderr)
        return 1

    written = []
    for page in pages:
        target, html = render(page, layout, layout_bare)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(html, encoding="utf-8")
        written.append((target.relative_to(ROOT), len(html)))

    leftovers = set()
    for target, _ in written:
        text = (ROOT / target).read_text(encoding="utf-8")
        for token in re.findall(r"\{\{[a-z_]+\}\}", text):
            leftovers.add((str(target), token))
    if leftovers:
        for t, token in sorted(leftovers):
            print(f"WARNUNG nicht ersetzt: {token} in {t}", file=sys.stderr)
        return 1

    total = sum(size for _, size in written)
    for target, size in written:
        print(f"  {str(target):46} {size / 1024:6.1f} KB")
    print(f"\n{len(written)} Seiten, {total / 1024:.0f} KB HTML gesamt.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
