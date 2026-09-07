"""
Schneidet die Beispielfotos auf die Bildfenster der Vorlagen zu.

Zwei Regeln stecken hier drin:

1. Ein zentrierter Zuschnitt schneidet beim Querformat die Koepfe ab. Darum
   liegt jeder Ausschnitt um einen benannten Bezugspunkt — den Kuss, den
   Bauch — und dieser sitzt je Format an einer anderen Stelle im Bild.

2. Jeder Anlass bekommt sein eigenes Foto. Ein Hochzeitskuss in einer
   Geburtsanzeige waere schlimmer als ein grauer Platzhalter: der Platzhalter
   ist erkennbar ein Platzhalter, das falsche Foto sieht nach Schlamperei aus.

Ergebnis: assets/demo-<anlass>-<fenster>.png
"""

import pathlib

from PIL import Image

ASSETS = pathlib.Path(__file__).resolve().parent.parent / "assets"

# fenster -> (Verhaeltnis Breite/Hoehe, Hoehe des Bezugspunkts im Ausschnitt)
# Die vier Fenster kommen aus den Vorlagen: t08 nutzt landscape, portrait und
# square, t10 zusaetzlich tall als randabfallendes Titelbild.
SHAPE = {
    "landscape": (622 / 366, 0.42),
    "portrait":  (1.0, 0.50),
    "square":    (1.0, 0.36),
    "tall":      (750 / 1050, 0.30),
}

# anlass -> Quelldatei und je Fenster (Bezugspunkt, Ausschnittvergroesserung).
# Der Bezugspunkt ist ein Anteil von Breite und Hoehe des Originals.
PHOTOS = {
    "wedding": ("photo-example-wedding.png", {
        # Das Paar kuesst sich im oberen Drittel, der Strauss liegt unten
        # rechts — daraus werden zwei Bilder, die nebeneinander stehen koennen.
        "landscape": ((0.508, 0.216), 1.0),
        "portrait":  ((0.330, 0.740), 1.0),
        "square":    ((0.508, 0.216), 1.0),
        "tall":      ((0.508, 0.216), 1.0),
    }),
    "birthday": ("photo-example-birthday.jpg", {
        # Gesicht und Sektglas im oberen Drittel, die Torte ganz unten. Beides
        # in einen Querschnitt zu bekommen geht nicht — sie liegen zu weit
        # auseinander. Also traegt das breite Fenster die Person, und das
        # Detailfenster daneben die Torte mit den Kerzen.
        "landscape": ((0.420, 0.240), 1.0),
        "portrait":  ((0.620, 0.860), 1.9),
        "square":    ((0.420, 0.260), 1.0),
        "tall":      ((0.420, 0.240), 1.0),
    }),
    "baby": ("photo-example-baby.jpg", {
        "landscape": ((0.470, 0.500), 1.0),
        # Teddy, Schuhe und Geschenke als Detail: enger Ausschnitt rechts
        "portrait":  ((0.780, 0.640), 2.1),
        "square":    ((0.450, 0.470), 1.0),
        "tall":      ((0.460, 0.430), 1.0),
    }),
}


def crop(im, ratio, focus, focus_y, zoom=1.0):
    w, h = im.size
    fx, fy = focus[0] * w, focus[1] * h
    cw, ch = w / zoom, w / zoom / ratio
    if ch > h:                       # passt nicht in die Hoehe: ueber Breite
        ch, cw = h / zoom, h / zoom * ratio
    left = min(max(fx - cw / 2, 0), w - cw)
    top = min(max(fy - ch * focus_y, 0), h - ch)
    return im.crop((round(left), round(top), round(left + cw), round(top + ch)))


def main():
    for theme, (src, windows) in PHOTOS.items():
        im = Image.open(ASSETS / src).convert("RGB")
        for shape, (focus, zoom) in windows.items():
            ratio, focus_y = SHAPE[shape]
            out = ASSETS / f"demo-{theme}-{shape}.png"
            c = crop(im, ratio, focus, focus_y, zoom)
            c.save(out)
            print(f"{out.name:30} {c.size[0]} x {c.size[1]}")


if __name__ == "__main__":
    main()
