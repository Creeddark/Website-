# -*- coding: utf-8 -*-
"""VELORA — Orientierungskarten aus den Fakten der Gästeseiten.

Bewusst KEINE Straßenkarte. Eine Straßenkarte müsste von einem Kachelserver
kommen: jede Anzeige wäre eine Anfrage an einen Dritten, mit der IP des
Gastes, und sie kostet je nach Anbieter pro Aufruf. Diese Seite verspricht
das Gegenteil.

Gezeichnet wird stattdessen, was ein Gastgeber tatsächlich weiß und in ein
Formular tippen kann: Richtung und Entfernung. „Fischbude, 500 m, Nordwest."
Daraus wird eine Karte, die die eine Frage beantwortet, die ein Gast wirklich
hat — was ist wo, und wie weit ist es.

In der Karte stehen nur Zahlen, die Namen stehen als echter HTML-Text
daneben. Das hat drei handfeste Gründe: eine SVG im <img> lädt die
Schriften der Seite nicht (Montserrat käme nie an), auf einem Telefon
schrumpft die Karte auf ein Drittel und mit ihr jede Beschriftung, und
lange Namen wie „Fischbude Käpt'n Selmer" ragen aus jedem Kreis heraus.
Text daneben ist lesbar, markierbar, übersetzbar und vorlesbar.

Nichts daran ist erfunden: steht keine Richtung in den Fakten, taucht der Ort
auf der Karte nicht auf.
"""
import json, math, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
PAGES = ROOT / "build" / "pages"
OUT = ROOT / "site" / "assets" / "img"

CREAM = "#FFF7EE"
LINE = "#E4DAC7"
INK = "#4A4238"      # 9,3:1 auf Creme — die Ziffern
SOFT = "#6C6559"     # 5,4:1 auf Creme — Ringe und Norden
GOLD = "#D4AF37"
GOLD_INK = "#7B641A"

# Die viewBox-Einheiten sind so gewählt, dass eine Einheit ungefähr einem
# Pixel auf dem Telefon entspricht. Damit ist die kleinste Schrift dort
# wirklich so gross, wie sie hier aussieht.
W = H = 360
CX = CY = 180

AUSSEN = 132.0
INNEN = 0.34          # nichts sitzt näher an der Mitte
PIN = 12.0
MIND = 29.0           # Mindestabstand zweier Nadelmitten

BEARING = {"n": 0, "no": 45, "o": 90, "so": 135,
           "s": 180, "sw": 225, "w": 270, "nw": 315}
HIMMEL = {"n": "Norden", "no": "Nordosten", "o": "Osten", "so": "Südosten",
          "s": "Süden", "sw": "Südwesten", "w": "Westen", "nw": "Nordwesten"}


def slugify(text: str) -> str:
    t = text.lower()
    for a, b in [("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")]:
        t = t.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def esc(t: str) -> str:
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def radius(meter: float, maxmeter: float) -> float:
    """Wurzelskala zwischen INNEN und AUSSEN. Linear gerechnet würden 20 m
    neben 2 km auf denselben Punkt fallen."""
    t = math.sqrt(min(meter, maxmeter) / maxmeter)
    return AUSSEN * (INNEN + (1 - INNEN) * t)


def ring_werte(maxmeter: float) -> list:
    """Ein runder äußerer Wert knapp über der größten Entfernung, darunter
    zwei Zwischenringe. Eine feste Leiter verschenkt sonst die halbe Fläche:
    2,4 km auf einem 5-km-Ring drängt alles in die Mitte."""
    exp = math.floor(math.log10(max(maxmeter, 1)))
    basis = 10 ** exp
    for f in (1, 1.5, 2, 2.5, 3, 4, 5, 7.5, 10):
        aussen = f * basis
        if aussen >= maxmeter:
            break
    return [round(aussen * 0.4), round(aussen * 0.7), round(aussen)]


def beschriftung(meter: float) -> str:
    if meter >= 1000:
        v = meter / 1000
        return (f"{v:.1f}".rstrip("0").rstrip(".") + " km").replace(".", ",")
    return f"{round(meter)} m"


def platziere(orte: list, maxm: float) -> list:
    """Nadeln auf ihren Peilstrahl setzen und sich überlappende auseinander-
    drehen. Gedreht wird, nicht verschoben: eine um wenige Grad verrückte
    Richtung ist ehrlicher als eine falsche Entfernung. Mehr als 14° gibt
    es nicht — dann berühren sich die Nadeln eben, und die Liste daneben
    sagt ohnehin, welche welche ist."""
    pins = [{"o": o, "grad": float(BEARING[o["richtung"].lower()]),
             "ab": 0.0, "r": radius(o["meter"], maxm)} for o in orte]

    def xy(p):
        w = math.radians(p["grad"] + p["ab"])
        return CX + p["r"] * math.sin(w), CY - p["r"] * math.cos(w)

    for _ in range(200):
        eng = False
        for i, a in enumerate(pins):
            for b in pins[i + 1:]:
                ax, ay = xy(a)
                bx, by = xy(b)
                if math.hypot(ax - bx, ay - by) >= MIND:
                    continue
                eng = True
                delta = ((b["grad"] + b["ab"]) - (a["grad"] + a["ab"])) % 360
                s = 1.0 if delta < 180 else -1.0
                a["ab"] = max(-14.0, min(14.0, a["ab"] - s * 1.2))
                b["ab"] = max(-14.0, min(14.0, b["ab"] + s * 1.2))
        if not eng:
            break

    for p in pins:
        p["x"], p["y"] = xy(p)
    return pins


def karte(objekt: str, orte: list) -> str:
    """orte: [{name, meter, richtung}] — Richtung als Kompasskürzel."""
    orte = [o for o in orte if o.get("richtung", "").lower() in BEARING]
    orte = sorted(orte, key=lambda o: o["meter"])
    maxm = max([o["meter"] for o in orte] + [100])
    ringe = ring_werte(maxm)
    maxm = max(maxm, ringe[-1])

    s = [f'<rect width="{W}" height="{H}" fill="{CREAM}"/>']

    # --- Entfernungsringe -------------------------------------------------
    # Die Ringbeschriftung liegt auf einer Diagonale zwischen zwei
    # Kompassrichtungen — dort steht nach Konstruktion keine Nadel.
    diag = math.radians(22.5)
    for m in ringe:
        r = radius(m, maxm)
        s.append(f'<circle cx="{CX}" cy="{CY}" r="{r:.1f}" fill="none" '
                 f'stroke="{LINE}" stroke-width="1.2"/>')
        lx = CX + r * math.sin(diag)
        ly = CY - r * math.cos(diag)
        s.append(f'<text x="{lx:.1f}" y="{ly + 4:.1f}" text-anchor="middle" '
                 f'font-family="sans-serif" font-size="11" fill="{SOFT}" '
                 f'stroke="{CREAM}" stroke-width="3.5" paint-order="stroke">'
                 f'{beschriftung(m)}</text>')

    # --- Kompass: nur Norden, mehr braucht es nicht -----------------------
    s.append(f'<path d="M{CX} 24 l6 14 l-6 -4.5 l-6 4.5 Z" fill="{GOLD_INK}"/>')
    s.append(f'<text x="{CX}" y="16" text-anchor="middle" font-family="sans-serif" '
             f'font-size="12" font-weight="700" letter-spacing="1.2" fill="{SOFT}">N</text>')

    # --- Die Orte: Peilstrahl, Nadel, Nummer ------------------------------
    pins = platziere(orte, maxm)
    for i, p in enumerate(pins, 1):
        s.append(f'<line x1="{CX}" y1="{CY}" x2="{p["x"]:.1f}" y2="{p["y"]:.1f}" '
                 f'stroke="{LINE}" stroke-width="1"/>')
    for i, p in enumerate(pins, 1):
        s.append(f'<circle cx="{p["x"]:.1f}" cy="{p["y"]:.1f}" r="{PIN}" '
                 f'fill="{CREAM}" stroke="{INK}" stroke-width="1.6"/>')
        s.append(f'<text x="{p["x"]:.1f}" y="{p["y"] + 4.6:.1f}" text-anchor="middle" '
                 f'font-family="sans-serif" font-size="13" font-weight="600" '
                 f'fill="{INK}">{i}</text>')

    # --- Die Mitte: das Objekt selbst -------------------------------------
    s.append(f'<circle cx="{CX}" cy="{CY}" r="13" fill="{GOLD}" '
             f'stroke="{CREAM}" stroke-width="3"/>')
    s.append(f'<circle cx="{CX}" cy="{CY}" r="4.5" fill="{CREAM}"/>')

    titel = (f"Orientierungskarte: {objekt} in der Mitte, "
             f"{len(pins)} nummerierte Orte ringsum. "
             + "; ".join(f'{i} {p["o"]["name"]}, {beschriftung(p["o"]["meter"])} '
                         f'{HIMMEL[p["o"]["richtung"].lower()]}'
                         for i, p in enumerate(pins, 1)) + ".")
    return ('<svg xmlns="http://www.w3.org/2000/svg" '
            f'viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
            f'preserveAspectRatio="xMidYMid meet" role="img" '
            f'aria-label="{esc(titel)}">' + "".join(s) + "</svg>")


def legende(orte: list) -> list:
    """Dieselbe Reihenfolge wie die Nummern in der Karte."""
    orte = [o for o in orte if o.get("richtung", "").lower() in BEARING]
    return [{"nr": i, "name": o["name"], "weit": beschriftung(o["meter"]),
             "richtung": HIMMEL[o["richtung"].lower()]}
            for i, o in enumerate(sorted(orte, key=lambda o: o["meter"]), 1)]


def main() -> int:
    gemacht = []
    for page in sorted(PAGES.rglob("*.html")):
        m = re.match(r"\s*<!--\s*(\{.*?\})\s*-->", page.read_text(encoding="utf-8"), re.S)
        if not m:
            continue
        facts = json.loads(m.group(1)).get("facts", {})
        orte = facts.get("umgebung") or []
        if not orte:
            continue
        name = "karte-" + slugify(facts.get("objekt", page.stem)) + ".svg"
        (OUT / name).write_text(karte(facts.get("objekt", ""), orte), encoding="utf-8")
        gemacht.append((name, len(orte), (OUT / name).stat().st_size))

    for name, n, size in gemacht:
        print(f"  {name:34} {n} Orte   {size/1024:5.1f} KB")
    print(f"\n{len(gemacht)} Orientierungskarten erzeugt.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
