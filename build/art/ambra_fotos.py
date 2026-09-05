#!/usr/bin/env python3
"""
AMBRA — Fotos in Theme-Bilder verwandeln.

Nimmt die Aufnahmen, wie sie aus der Kamera oder aus einem Bildgenerator
kommen, und legt sie im richtigen Zuschnitt, in der richtigen Groesse und als
WebP im Theme ab. Dieselbe Aufgabe stellt sich bei jedem Kunden wieder, darum
ein Skript und keine Handarbeit.

    python3 build/art/ambra_fotos.py <hero> <siegel> <papier> <kachel> [<kachel> ...]

Das Siegel wird freigestellt: der weisse Grund wird von den Ecken her
weggenommen, damit es auf dem dunklen Umschlag liegen kann. Nur zusammen-
haengendes Weiss vom Rand her faellt weg, die hellen Glanzstellen im Wachs
bleiben stehen.
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
}


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
    if len(argv) < 4:
        print(__doc__.strip())
        return 2
    hero, siegel, papier, *kacheln = (pathlib.Path(a) for a in argv)

    b, h, q = ZIELE["hero"]
    passend(Image.open(hero).convert("RGB"), b, h).save(
        IMG / "hero.webp", "WEBP", quality=q, method=6)

    b, h, q = ZIELE["papier"]
    passend(Image.open(papier).convert("RGB"), b, h).save(
        IMG / "papier.webp", "WEBP", quality=q, method=6)

    s = freistellen(Image.open(siegel))
    if s.width > 640:
        s = s.resize((640, round(640 * s.height / s.width)), Image.LANCZOS)
    s.save(IMG / "siegel.webp", "WEBP", quality=88, method=6, exact=True)

    b, h, q = ZIELE["kachel"]
    namen = ["hero.webp", "siegel.webp", "papier.webp"]
    for i, k in enumerate(kacheln, start=1):
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
