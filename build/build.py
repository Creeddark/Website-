#!/usr/bin/env python3
"""
VELORA — statischer Seitengenerator.

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
sys.path.insert(0, str(ROOT / "build" / "art"))
from karte import legende as karten_legende  # noqa: E402
PAGES = ROOT / "build" / "pages"
LAYOUT = ROOT / "build" / "layout.html"
LAYOUT_BARE = ROOT / "build" / "layout-bare.html"
OUT = ROOT / "site"

BRAND = "VELORA"

# Absolute Adresse der Seite. og:url und og:image muessen absolut sein, ein
# relativer Pfad wird von keinem Vorschaudienst aufgeloest. Beim Umzug auf
# die echte Domain ist das hier die einzige Stelle, die sich aendert.
SITE = "https://velora.example/"  # Markenrecherche (DPMA/EUIPO) steht aus, siehe docs/11

NAV_KEYS = ["segmente", "produkt", "preise", "demo", "faq"]


def slugify(text: str) -> str:
    """Dateiname aus einem Namen — muss zu build/art/wifi.py passen."""
    t = text.lower()
    for a, b in [("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")]:
        t = t.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


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

    # Fakten der Seite als JSON — Eli liest sie von dort, statt eine Kopie
    # im Skript zu tragen. Eine Kopie läuft irgendwann auseinander, und dann
    # nennt der Assistent ein WLAN-Passwort, das nicht mehr gilt.
    facts = meta.get("facts")
    if facts:
        wlan = facts.get("wlan")
        if wlan and wlan.get("ssid"):
            facts = dict(facts)
            facts["wlanqr"] = base + "assets/img/wifi-" + slugify(wlan["ssid"]) + ".svg"
        facts_block = ('\n<script type="application/json" id="velora-facts">'
                       + json.dumps(facts, ensure_ascii=False) + "</script>")
    else:
        facts_block = ""

    # Die Orientierungskarte. Die Nummern im Bild und die Namen daneben
    # kommen aus derselben Funktion wie die SVG selbst — sonst zeigt die
    # Karte irgendwann auf die 4 und die Liste nennt dazu den falschen Ort.
    orte = (meta.get("facts") or {}).get("umgebung") or []
    if orte and "{{karte}}" in out:
        objekt = meta["facts"].get("objekt", "")
        zeilen = "".join(
            '<li><span class="karte__nr" aria-hidden="true">{nr}</span>'
            '<span class="karte__name">{nr}. {name}</span>'
            '<span class="karte__weit">{weit}</span>'
            '<p class="karte__hin">{richtung}</p></li>'.format(**e)
            for e in karten_legende(orte)
        )
        out = out.replace("{{karte}}", (
            '<figure class="karte">'
            '<img class="karte__bild" src="' + base + 'assets/img/karte-'
            + slugify(objekt) + '.svg" width="360" height="360" loading="lazy" decoding="async"'
            ' alt="Orientierungskarte: ' + objekt + ' in der Mitte, die nummerierten Orte'
            ' ringsum in der Richtung, in der sie liegen. Alle Namen stehen in der Liste darunter.">'
            '<ol class="karte__liste">' + zeilen + '</ol>'
            '<figcaption class="karte__fuss">Luftlinie ab ' + objekt
            + ', gerundet. Norden ist oben.</figcaption>'
            '</figure>'))
    else:
        out = out.replace("{{karte}}", "")

    # Eli richtet seine Vorschläge nach der Seite, auf der er steht.
    rel_str = str(rel).replace("\\", "/")
    if rel_str.startswith("demo/"):
        elictx = "demo"
    elif rel_str.startswith("segmente/"):
        elictx = "segment"
    elif rel_str in ("preise.html", "produkt.html"):
        elictx = rel_str[:-5]
    else:
        elictx = "start"

    replacements = {
        "{{elictx}}": elictx,
        "{{facts}}": facts_block,
        "{{title}}": meta["title"],
        "{{description}}": meta["description"],
        "{{path}}": str(rel).replace("\\", "/"),
        "{{base}}": base,
        "{{site}}": SITE,
        "{{seg}}": seg,
        "{{segattr}}": seg_attr,
        "{{head}}": meta.get("head", ""),
        "{{demonote}}": meta.get("demonote", ""),
        "{{democta}}": meta.get("democta", "index.html"),
        "{{democtalabel}}": meta.get("democtalabel", "Zur Website"),
    }
    for needle, value in replacements.items():
        out = out.replace(needle, value)

    out = out.replace("VELORA", BRAND)
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
