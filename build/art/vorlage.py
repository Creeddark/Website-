# -*- coding: utf-8 -*-
"""VELORA — QR-Codes für die Druckvorlage.

Der Code auf der gedruckten Karte zeigt auf die Gästemappe des jeweiligen
Objekts. Adresse und Hausname stehen bereits in der Front-Matter der
Gästeseite; hier wird nichts ein zweites Mal getippt, sonst laufen die
beiden Stellen irgendwann auseinander.

Die Domain kommt aus build.py. Solange dort velora.example steht, zeigt
der Code ins Leere — er wird in dem Moment richtig, in dem die echte
Domain eingetragen ist, ohne dass hier etwas zu ändern wäre.
"""
import json, pathlib, re, sys
import segno

ROOT = pathlib.Path(__file__).resolve().parents[2]
PAGES = ROOT / "build" / "pages"
OUT = ROOT / "site" / "assets" / "img"

DARK = "#1A1A1A"
LIGHT = "#FFFFFF"   # Auf Papier ist der Grund weiss, nicht creme: eine
                    # vollflaechig eingefaerbte Karte kostet Tinte und
                    # kommt aus einem Heimdrucker streifig heraus.


def slug(text: str) -> str:
    t = text.lower()
    for a, b in [("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")]:
        t = t.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def site() -> str:
    """Die Domain steht an genau einer Stelle: in build.py."""
    quelle = (ROOT / "build" / "build.py").read_text(encoding="utf-8")
    m = re.search(r'^SITE\s*=\s*"([^"]+)"', quelle, re.M)
    if not m:
        raise SystemExit("SITE nicht in build.py gefunden")
    return m.group(1)


def main() -> int:
    basis = site()
    gemacht = []
    for page in sorted(PAGES.rglob("*.html")):
        m = re.match(r"\s*<!--\s*(\{.*?\})\s*-->", page.read_text(encoding="utf-8"), re.S)
        if not m:
            continue
        objekt = json.loads(m.group(1)).get("facts", {}).get("objekt")
        if not objekt:
            continue
        pfad = page.relative_to(PAGES).as_posix()
        ziel = basis + pfad
        name = "vorlage-qr-" + slug(objekt) + ".svg"
        # Fehlerkorrektur H, wie auf der Produktseite zugesagt: der Code
        # bleibt lesbar, auch wenn die Karte Fingerabdruecke abbekommt
        # oder eine Ecke fehlt.
        # Ruhezone von vier Modulen, wie die Norm sie verlangt. Ohne sie
        # scheitern Scanner, sobald der Code neben etwas Dunklem sitzt —
        # und eine Druckvorlage wird nun einmal weiterverwendet.
        qr = segno.make(ziel, error="h")
        qr.save(OUT / name, kind="svg", scale=1, border=4,
                dark=DARK, light=LIGHT, svgclass=None, lineclass=None,
                omitsize=True, xmldecl=False, svgns=True)
        svg = (OUT / name).read_text(encoding="utf-8")
        svg = svg.replace("<svg ", '<svg preserveAspectRatio="xMidYMid meet" ', 1)
        (OUT / name).write_text(svg, encoding="utf-8")
        gemacht.append((name, objekt, ziel, (OUT / name).stat().st_size))

    for name, objekt, ziel, size in gemacht:
        print(f"  {name:34} {objekt:26} {size/1024:5.1f} KB")
        print(f"  {'':34} -> {ziel}")
    print(f"\n{len(gemacht)} Vorlagen-Codes erzeugt.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
