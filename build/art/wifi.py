# -*- coding: utf-8 -*-
"""VELORA — WLAN-QR-Codes aus den Fakten der Gästeseiten.

Ein Gast scannt den Code und ist im Netz. Kein Abtippen eines Passworts,
das aus Zufallszeichen besteht. Das Format ist der WIFI:-Standard, den
iOS und Android seit Jahren aus der Kamera heraus verstehen.
"""
import json, pathlib, re, sys
import segno

ROOT = pathlib.Path(__file__).resolve().parents[2]
PAGES = ROOT / "build" / "pages"
OUT = ROOT / "site" / "assets" / "img"

DARK = "#1A1A1A"     # Charcoal — auf Creme 16,4:1, jede Kamera liest ihn
LIGHT = "#FFF7EE"


def escape(value: str) -> str:
    """Im WIFI:-Format sind \\ ; , : und " zu maskieren."""
    return re.sub(r'([\;,:"])', r"\\\1", value)


def payload(ssid: str, password: str) -> str:
    return f"WIFI:T:WPA;S:{escape(ssid)};P:{escape(password)};;"


def slug(text: str) -> str:
    t = text.lower()
    for a, b in [("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")]:
        t = t.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def main() -> int:
    made = []
    for page in sorted(PAGES.rglob("*.html")):
        m = re.match(r"\s*<!--\s*(\{.*?\})\s*-->", page.read_text(encoding="utf-8"), re.S)
        if not m:
            continue
        wlan = json.loads(m.group(1)).get("facts", {}).get("wlan")
        if not wlan:
            continue
        name = "wifi-" + slug(wlan["ssid"]) + ".svg"
        # Fehlerkorrektur H: der Code bleibt lesbar, auch wenn der Aufsteller
        # an der Kühlschranktür Fingerabdrücke abbekommt.
        qr = segno.make(payload(wlan["ssid"], wlan["pass"]), error="h")
        qr.save(OUT / name, kind="svg", scale=1, border=2,
                dark=DARK, light=LIGHT, svgclass=None, lineclass=None,
                omitsize=True, xmldecl=False, svgns=True)
        # Ohne feste Größe skaliert der Code sauber in jeden Container.
        svg = (OUT / name).read_text(encoding="utf-8")
        svg = svg.replace("<svg ", '<svg preserveAspectRatio="xMidYMid meet" ', 1)
        (OUT / name).write_text(svg, encoding="utf-8")
        made.append((name, wlan["ssid"], (OUT / name).stat().st_size))

    for name, ssid, size in made:
        print(f"  {name:28} {ssid:22} {size/1024:5.1f} KB")
    print(f"\n{len(made)} WLAN-Codes erzeugt.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
