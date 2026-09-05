#!/usr/bin/env python3
"""
AMBRA — Fotos in Theme-Bilder verwandeln.

Nimmt die Aufnahmen, wie sie aus der Kamera oder aus einem Bildgenerator
kommen, und legt sie im richtigen Zuschnitt, in der richtigen Groesse und als
WebP im Theme ab. Dieselbe Aufgabe stellt sich bei jedem Kunden wieder, darum
ein Skript und keine Handarbeit.

    python3 build/art/ambra_fotos.py <hero> <siegel> <papier> <kachel> [<kachel> ...]

Ein Bindestrich statt eines Pfades laesst die Stelle unveraendert. Der Hero
etwa kommt aus dem Film und darf hier nicht ueberschrieben werden:

    python3 build/art/ambra_fotos.py - siegel.png papier.png g1.png g2.png

Das Siegel wird freigestellt: der weisse Grund wird von den Ecken her
weggenommen, damit es auf dem dunklen Umschlag liegen kann. Nur zusammen-
haengendes Weiss vom Rand her faellt weg, die hellen Glanzstellen im Wachs
bleiben stehen.

Wasserzeichen: manche Generatoren stempeln unten rechts ihren Namen hinein.
Beim Papier wird ohnehin nur die Mitte des Bogens gebraucht, damit ist der
Stempel weg und die Buettenkante gleich mit. Beim Siegel ginge das nicht,
ohne die Unterkante abzuschneiden — dort bleibt darum nur der groesste
zusammenhaengende Fleck stehen, und der Stempel faellt als kleinerer Rest
heraus.
"""
from __future__ import annotations

import pathlib
import sys
from collections import deque

from PIL import Image, ImageFilter

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
IMG = ROOT / "themes" / "ambra" / "assets" / "img"

# Zielgroessen. Grosszuegig gewaehlt fuer Bildschirme mit hoher Punktdichte,
# aber nicht groesser als noetig: eine Einladung wird unterwegs geoeffnet,
# oft mit schlechtem Empfang.
ZIELE = {
    "hero":   (1080, 1920, 80),  # bildschirmfuellend, 9:16
    "kachel": (900, 1200, 78),   # Galerie, 3:4
    "papier": (700, 700, 82),    # Faserung des Umschlags, quadratisch
    "siegel": (512, 0, 82),      # nur die Breite; die Hoehe folgt dem Zuschnitt
}

# Das Siegel wird mit rund 135 CSS-Pixeln angezeigt, waehrend der Oeffnung
# kurz 1,12-fach vergroessert. Auf einem Dreifach-Bildschirm sind das etwa
# 450 echte Pixel — 512 reichen, 640 kosten nur Platz.


def passend(im: Image.Image, breite: int, hoehe: int) -> Image.Image:
    """Auf das Zielverhaeltnis beschneiden, dann auf die Zielgroesse bringen.
    Hochskaliert wird nicht — ein weichgerechnetes Bild sieht schlechter aus
    als ein kleines, das der Browser selbst skaliert."""
    ziel = breite / hoehe
    b, h = im.size
    if b / h > ziel:                      # zu breit: links und rechts weg
        neu = int(h * ziel)
        im = im.crop(((b - neu) // 2, 0, (b - neu) // 2 + neu, h))
    elif b / h < ziel:                    # zu hoch: oben und unten weg
        neu = int(b / ziel)
        im = im.crop((0, (h - neu) // 2, b, (h - neu) // 2 + neu))
    if im.width > breite:
        im = im.resize((breite, hoehe), Image.LANCZOS)
    return im


def groesster_fleck(alpha: Image.Image) -> Image.Image:
    """Nur den groessten zusammenhaengenden undurchsichtigen Bereich behalten.
    Alles andere — Wasserzeichen, Staub, abgesprengte Ecken — faellt weg."""
    b, h = alpha.size
    px = alpha.load()
    marke = bytearray(b * h)          # 0 = ungeprueft, sonst Nummer des Flecks
    groessen = [0]
    nummer = 0

    for y0 in range(h):
        for x0 in range(b):
            if marke[y0 * b + x0] or px[x0, y0] < 128:
                continue
            nummer += 1
            zahl = 0
            stapel = [(x0, y0)]
            marke[y0 * b + x0] = nummer
            while stapel:
                x, y = stapel.pop()
                zahl += 1
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if (0 <= nx < b and 0 <= ny < h
                            and not marke[ny * b + nx] and px[nx, ny] >= 128):
                        marke[ny * b + nx] = nummer
                        stapel.append((nx, ny))
            groessen.append(zahl)

    if nummer <= 1:
        return alpha
    behalten = groessen.index(max(groessen))
    return Image.frombytes(
        "L", (b, h),
        bytes(px[i % b, i // b] if marke[i] == behalten else 0 for i in range(b * h)))


def freistellen(im: Image.Image, schwelle: int = 232, weich: float = 0.9) -> Image.Image:
    """Weissen Hintergrund entfernen. Es wird von den Bildecken her geflutet,
    nicht global nach Helligkeit gefiltert — sonst verschwinden auch die
    Lichter auf dem Wachs."""
    im = im.convert("RGB")
    b, h = im.size
    px = im.load()
    weiss = bytearray(b * h)              # 1 = gehoert zum Hintergrund
    q = deque()

    def hell(x: int, y: int) -> bool:
        r, g, bl = px[x, y]
        return r >= schwelle and g >= schwelle and bl >= schwelle

    for x in range(b):
        for y in (0, h - 1):
            if hell(x, y) and not weiss[y * b + x]:
                weiss[y * b + x] = 1
                q.append((x, y))
    for y in range(h):
        for x in (0, b - 1):
            if hell(x, y) and not weiss[y * b + x]:
                weiss[y * b + x] = 1
                q.append((x, y))

    while q:
        x, y = q.popleft()
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < b and 0 <= ny < h and not weiss[ny * b + nx] and hell(nx, ny):
                weiss[ny * b + nx] = 1
                q.append((nx, ny))

    alpha = Image.frombytes("L", (b, h), bytes(255 - v * 255 for v in weiss))
    alpha = groesster_fleck(alpha)                          # Wasserzeichen raus
    alpha = alpha.filter(ImageFilter.GaussianBlur(weich))   # Kante entschaerfen
    aus = im.convert("RGBA")
    aus.putalpha(alpha)

    # Eng beschneiden. Bliebe der durchsichtige Rand stehen, saesse das Siegel
    # als kleiner Knopf in einem grossen leeren Kasten.
    kasten = alpha.point(lambda v: 255 if v > 16 else 0).getbbox()
    if kasten:
        rand = int(max(kasten[2] - kasten[0], kasten[3] - kasten[1]) * 0.02)
        aus = aus.crop((max(0, kasten[0] - rand), max(0, kasten[1] - rand),
                        min(b, kasten[2] + rand), min(h, kasten[3] + rand)))
    return aus


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print(__doc__.strip())
        return 2
    hero, siegel, papier, *kacheln = argv
    namen = []

    if hero != "-":
        b, h, q = ZIELE["hero"]
        passend(Image.open(hero).convert("RGB"), b, h).save(
            IMG / "hero.webp", "WEBP", quality=q, method=6)
        namen.append("hero.webp")

    if papier != "-":
        b, h, q = ZIELE["papier"]
        im = Image.open(papier).convert("RGB")
        # Nur die Mitte des Bogens. Der Rand traegt die Buettenkante, die als
        # heller Streifen ueber jede Flaeche des Umschlags liefe, und die Ecke
        # unten rechts das Wasserzeichen. In der Mitte ist die Faser
        # gleichmaessig, und nur die wird gebraucht.
        w0, h0 = im.size
        im = im.crop((int(w0 * 0.19), int(h0 * 0.19),
                      int(w0 * 0.81), int(h0 * 0.81)))
        passend(im, b, h).save(IMG / "papier.webp", "WEBP", quality=q, method=6)
        namen.append("papier.webp")

    if siegel != "-":
        im = Image.open(siegel)
        if im.width > 1024:                       # sonst dauert der Fleck ewig
            im = im.resize((1024, round(1024 * im.height / im.width)), Image.LANCZOS)
        s = freistellen(im)
        breite, _, q = ZIELE["siegel"]
        if s.width > breite:
            s = s.resize((breite, round(breite * s.height / s.width)), Image.LANCZOS)
        s.save(IMG / "siegel.webp", "WEBP", quality=q, method=6, exact=True)
        namen.append("siegel.webp")

    b, h, q = ZIELE["kachel"]
    for i, k in enumerate(kacheln, start=1):
        if k == "-":
            continue
        passend(Image.open(k).convert("RGB"), b, h).save(
            IMG / f"g-{i}.webp", "WEBP", quality=q, method=6)
        namen.append(f"g-{i}.webp")

    for name in namen:
        pfad = IMG / name
        with Image.open(pfad) as im:
            print(f"  {name:14} {im.size[0]:>5}x{im.size[1]:<5} "
                  f"{pfad.stat().st_size // 1024:>4} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
