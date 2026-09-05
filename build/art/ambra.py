#!/usr/bin/env python3
"""
AMBRA — Illustrationsgenerator fuer das Hochzeits-Theme.

Erzeugt die Bilder des Themes als SVG. Bewusst als Zeichnung und nicht als
Fotomontage: wir haben keine lizenzierten Fotos, und eine ehrliche Zeichnung
ist besser als ein erfundenes Bild. Sobald das Paar eigene Fotos liefert,
ersetzen die Fotos diese Blaetter, siehe themes/README.md.

Bildsprache: dieselbe wie auf der VELORA-Website. Architektonische
Aufrisszeichnung, eine Grundlinie, flache Frontalansicht, feine Linien,
sparsam getoente Flaechen. Gezeichnet wird in Elfenbein auf Nachtgrund,
weil die Galerie im dunklen Teil der Einladung liegt.

    python3 build/art/ambra.py
"""
from __future__ import annotations

import math
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent.parent / "themes" / "ambra" / "assets" / "img"
OUT.mkdir(parents=True, exist_ok=True)

# Palette — identisch zu den CSS-Tokens in einladung.css
# Die Galerie steht auf dem hellen Teil der Einladung, also wird in Tinte
# auf Papier gezeichnet. Das Siegel bringt seine eigenen Farben mit.
NIGHT = "#F3EADB"     # Blattgrund: Papier, eine Spur tiefer als die Seite
LINE = "#3B3327"      # Tinte
SOFT = "#A2947C"      # zurueckgenommene Linien, zweite Ebene
TINT = "#B58F4F"      # Messing, die einzige getoente Flaeche je Motiv


def svg(w: int, h: int, body: str, title: str, bg: str = NIGHT, defs: str = "") -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'width="100%" height="100%" preserveAspectRatio="xMidYMid slice" '
        f'role="img" aria-label="{title}">'
        f'{defs}<rect width="{w}" height="{h}" fill="{bg}"/>{body}</svg>'
    )


def g(stroke: str = LINE, sw: float = 2.4, fill: str = "none", extra: str = "") -> str:
    return (
        f'<g fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
        f'stroke-linecap="round" stroke-linejoin="round" {extra}>'
    )


def ground(y: int, x0: int = 0, x1: int = 900) -> str:
    return f'<path d="M{x0} {y}H{x1}"/>'


def glow(cx: int, cy: int, r: int, op: float = 0.17):
    """Die eine getoente Flaeche je Motiv: ein weicher Lichtkreis."""
    ident = f"glow{cx}_{cy}"
    return (
        f'<radialGradient id="{ident}" cx="50%" cy="50%" r="50%">'
        f'<stop offset="0%" stop-color="{TINT}" stop-opacity="{op}"/>'
        f'<stop offset="100%" stop-color="{TINT}" stop-opacity="0"/>'
        "</radialGradient>"
    ), f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{ident})" stroke="none"/>'


def kerze(x: int, base: int, hoehe: int, breite: int = 40) -> str:
    """Kerze mit Flamme. Der Koerper ist Linie, nur die Flamme ist gefuellt."""
    top = base - hoehe
    f = breite * 0.62
    return (
        f'<path d="M{x - breite // 2} {base}v{-hoehe}h{breite}v{hoehe}"/>'
        f'<path d="M{x} {top - 6}v-14"/>'
        f'<path d="M{x} {top - 20 - f * 2:.0f}c{f:.0f} {f * 1.3:.0f} {f * .78:.0f} {f * 2:.0f} 0 {f * 2:.0f}'
        f'c{-f * .78:.0f} 0 {-f:.0f} {-f * .7:.0f} 0 {-f * 2:.0f}z" fill="{TINT}" stroke="none"/>'
    )


def glas(x: int, base: int, h: int = 150, w: int = 78) -> str:
    """Weinglas im Aufriss: Kelch, Stiel, Fuss."""
    k = h * 0.52
    return (
        f'<path d="M{x - w // 2} {base - h}c0 {k * .72:.0f} {w // 2 - 4} {k:.0f} {w // 2} {k:.0f}'
        f'c4 0 {w // 2} {-k * .28:.0f} {w // 2} {-k:.0f}z"/>'
        f'<path d="M{x} {base - h + k:.0f}v{h - k - 8:.0f}"/>'
        f'<path d="M{x - 28} {base}h56"/>'
    )


def stuhl(x: int, base: int, h: int = 300, w: int = 130) -> str:
    """Stuhl im Aufriss, Lehne links, mit zwei Sprossen."""
    sitz = base - h * 0.46
    return (
        f'<path d="M{x} {base}v{-h}"/>'
        f'<path d="M{x} {sitz:.0f}h{w}"/>'
        f'<path d="M{x + w} {sitz:.0f}v{base - sitz:.0f}"/>'
        f'<path d="M{x + 6} {base}v{sitz - base:.0f}" stroke="{SOFT}"/>'
        f'<path d="M{x + 16} {base - h + 34}h{w - 34}" stroke="{SOFT}"/>'
        f'<path d="M{x + 16} {base - h + 84}h{w - 34}" stroke="{SOFT}"/>'
    )


def blatt(x: float, y: float, r: float, winkel: float) -> str:
    """Ein Blatt als zwei Bogen, um den Winkel gedreht."""
    return (
        f'<path transform="rotate({winkel:.1f} {x:.1f} {y:.1f})" '
        f'd="M{x:.1f} {y:.1f}c{r * .55:.1f} {-r * .5:.1f} {r:.1f} {-r * .2:.1f} {r:.1f} 0'
        f'c0 {r * .2:.1f} {-r * .45:.1f} {r * .5:.1f} {-r:.1f} 0z"/>'
    )


def baum(x: int, base: int, s: float = 1.0) -> str:
    """Linde: Stamm, zwei Aeste, Krone aus drei ueberlagerten Bogen."""
    return (
        f'<g transform="translate({x} {base}) scale({s})">'
        '<path d="M0 0v-300"/>'
        f'<path d="M0 -210l-64 -54M0 -250l58 -48" stroke="{SOFT}"/>'
        '<circle cx="0" cy="-410" r="150"/>'
        f'<path d="M-96 -486a118 118 0 0 1 192 0" stroke="{SOFT}"/>'
        f'<path d="M-104 -352a124 124 0 0 0 208 0" stroke="{SOFT}"/>'
        "</g>"
    )


# --------------------------------------------------------------- Galerie ----
# Hochformat 900x1200. Die Galerie steht auf dem Telefon, also ist das Blatt
# hochkant, und das Motiv fuellt den Rahmen — eine Zeichnung, die in der Mitte
# schwebt, wirkt in einer 380 Pixel breiten Karte wie ein Fehler.

def ringe() -> str:
    gdef, gbody = glow(660, 700, 330, 0.20)
    body = (
        f"<defs>{gdef}</defs>{gbody}"
        + g(sw=5.5)
        + ground(1050, 0, 900)
        + f'<path d="M0 1094H900" stroke="{SOFT}" stroke-width="3"/>'
        + '<circle cx="330" cy="836" r="206"/><circle cx="330" cy="836" r="168"/>'
        + '<g transform="rotate(-16 596 880)"><circle cx="596" cy="880" r="172"/>'
          '<circle cx="596" cy="880" r="138"/></g>'
        + kerze(716, 1050, 470, 46)
        + f'<g stroke="{SOFT}" stroke-width="4">'
        + blatt(118, 1032, 62, -22) + blatt(196, 1040, 48, 12) + "</g>"
        + "</g>"
    )
    return svg(900, 1200, body, "Zwei Trauringe auf der Tafel, daneben eine Kerze")


def tafel() -> str:
    gdef, gbody = glow(450, 560, 400, 0.20)
    kerzen = "".join(kerze(x, 700, 300, 36) for x in (250, 450, 650))
    glaeser = glas(120, 700) + glas(780, 700)
    body = (
        f"<defs>{gdef}</defs>{gbody}"
        + g(sw=5.5)
        + ground(1120, 0, 900)
        + stuhl(40, 1120, 300, 150) + stuhl(700, 1120, 300, 150)
        + '<path d="M0 700H900"/>'
        + f'<path d="M0 726H900" stroke="{SOFT}" stroke-width="3"/>'
        + '<path d="M108 726v394"/><path d="M760 726v394"/>'
        + glaeser + kerzen
        + "</g>"
    )
    return svg(900, 1200, body, "Gedeckte Tafel mit Kerzen und Glaesern")


def bogen() -> str:
    gdef, gbody = glow(450, 900, 380, 0.16)
    laub = ""
    for i in range(19):          # entlang des Bogens
        t = i / 18 * math.pi
        laub += blatt(450 - 268 * math.cos(t), 640 - 268 * math.sin(t), 46,
                      math.degrees(t) + 90)
    for i in range(4):           # an den Pfosten hinunter
        y = 700 + i * 84
        laub += blatt(182, y, 40, 200) + blatt(718, y, 40, -20)
    body = (
        f"<defs>{gdef}</defs>{gbody}"
        + g(sw=5.5)
        + ground(1050, 0, 900)
        + '<path d="M182 1050V640"/><path d="M718 1050V640"/>'
        + '<path d="M182 640a268 268 0 0 1 536 0"/>'
        + f'<g stroke="{SOFT}" stroke-width="3.4">{laub}</g>'
        + f'<path d="M300 1050l40 -64h220l40 64" stroke="{SOFT}"/>'
        + "</g>"
    )
    return svg(900, 1200, body, "Traubogen mit Laub ueber dem Mittelgang")


def kronleuchter() -> str:
    gdef, gbody = glow(450, 520, 430, 0.22)
    arme = ""
    for dx, y in ((-250, 610), (-150, 560), (150, 560), (250, 610)):
        arme += (f'<path d="M450 470c{dx * .5:.0f} 0 {dx:.0f} {y - 462} {dx:.0f} {y - 458}"/>'
                 + kerze(450 + dx, y, 132, 30))
    for dx, y in ((-92, 430), (92, 430)):
        arme += (f'<path d="M450 380c{dx * .5:.0f} 0 {dx:.0f} {y - 372} {dx:.0f} {y - 368}"/>'
                 + kerze(450 + dx, y, 110, 26))
    tropfen = "".join(
        f'<path d="M{450 + dx} 700v{28 + (i % 3) * 22}"/>'
        f'<circle cx="{450 + dx}" cy="{738 + (i % 3) * 22}" r="13"/>'
        for i, dx in enumerate((-206, -124, -42, 42, 124, 206))
    )
    body = (
        f"<defs>{gdef}</defs>{gbody}"
        + g(sw=5.5)
        + '<path d="M450 0v230"/>'
        + '<path d="M450 230l-70 74h140z"/>'
        + '<path d="M244 470h412"/><path d="M330 380h240"/>'
        + arme
        + '<path d="M450 470v230"/><ellipse cx="450" cy="470" rx="30" ry="22"/>'
        + f'<g stroke="{SOFT}" stroke-width="3.4">{tropfen}</g>'
        + f'<path d="M120 1090H780" stroke="{SOFT}"/>'
        + "</g>"
    )
    return svg(900, 1200, body, "Kronleuchter ueber der Tanzflaeche")


def gut() -> str:
    gdef, gbody = glow(450, 760, 380, 0.15)
    fenster = ""
    for r, y in enumerate((640, 800)):
        for c, x in enumerate((300, 396, 492, 588)):
            fill = TINT if (r + c) % 3 else "none"
            fenster += (f'<rect x="{x}" y="{y}" width="58" height="86" rx="3" '
                        f'fill="{fill}" fill-opacity="0.48"/>')
    body = (
        f"<defs>{gdef}</defs>{gbody}"
        + g(sw=5.5)
        + ground(1050, 0, 900)
        + baum(96, 1050, 0.92) + baum(824, 1050, 0.78)
        + '<path d="M268 1050V590h364v460"/>'
        + '<path d="M238 590L450 440L662 590"/>'
        + '<path d="M632 1050V720h192v330"/><path d="M608 720l108 -74 108 74"/>'
        + '<path d="M76 1050V760h192v290"/><path d="M52 760l120 -78 120 78"/>'
        + fenster
        + '<path d="M420 1050V938h60v112"/>'
        + f'<path d="M414 938a36 36 0 0 1 72 0" stroke="{SOFT}"/>'
        + "</g>"
    )
    return svg(900, 1200, body, "Gut Morgentau am Abend, Aufriss mit Linden")


# ---------------------------------------------------------------- Siegel ----

def _monogramm() -> str:
    """M und A, dazwischen ein feines Und-Zeichen."""
    return (
        '<path d="M52 118V74l17 27 17-27v44"/>'
        '<path d="M114 118l17-44 17 44"/><path d="M120 104h22"/>'
        '<path d="M92 136c-7-6-1-13 5-9c5 4 2 12-6 15c-4 1-6-1-4-3l14-11" '
        'stroke-width="3.4"/>'
    )


def siegel() -> str:
    """Das Wachssiegel. Kein Aufriss, sondern ein Objekt: unregelmaessiger
    Rand, plastischer Verlauf, eingepraegtes Monogramm."""
    cx = cy = 100
    pts = []
    for i in range(48):
        a = i / 48 * math.tau
        r = 78 + 4.2 * math.sin(a * 7 + 0.6) + 2.6 * math.sin(a * 3 - 1.2)
        pts.append(f"{cx + r * math.cos(a):.1f} {cy + r * math.sin(a):.1f}")
    rand = "M" + "L".join(pts) + "Z"

    defs = (
        "<defs>"
        '<radialGradient id="wachs" cx="38%" cy="32%" r="72%">'
        '<stop offset="0%" stop-color="#E8C078"/>'
        '<stop offset="46%" stop-color="#BE8F42"/>'
        '<stop offset="100%" stop-color="#6E4E1C"/>'
        "</radialGradient>"
        '<radialGradient id="wachsInnen" cx="50%" cy="46%" r="54%">'
        '<stop offset="0%" stop-color="#000" stop-opacity="0.20"/>'
        '<stop offset="70%" stop-color="#000" stop-opacity="0"/>'
        "</radialGradient>"
        "</defs>"
    )
    body = (
        f'<path d="{rand}" fill="url(#wachs)"/>'
        f'<path d="{rand}" fill="url(#wachsInnen)"/>'
        f'<circle cx="{cx}" cy="{cy}" r="62" fill="none" stroke="#7A5522" '
        'stroke-opacity="0.55" stroke-width="1.6"/>'
        f'<circle cx="{cx}" cy="{cy}" r="56" fill="none" stroke="#F0D49A" '
        'stroke-opacity="0.30" stroke-width="1"/>'
        '<g fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="5">'
        '<g stroke="#F2D9A4" stroke-opacity="0.45" transform="translate(0,1.6)">'
        f'{_monogramm()}</g>'
        f'<g stroke="#5E4116" stroke-opacity="0.85">{_monogramm()}</g>'
        "</g>"
        f'<path d="M{cx - 46} {cy - 40}a58 58 0 0 1 46 -24" fill="none" '
        'stroke="#FBE9C4" stroke-opacity="0.45" stroke-width="3"/>'
    )
    return svg(200, 200, body, "Wachssiegel mit dem Monogramm des Paares",
               bg="none", defs=defs)


def main() -> None:
    blaetter = {
        "siegel.svg": siegel(),
        "g-ringe.svg": ringe(),
        "g-tafel.svg": tafel(),
        "g-bogen.svg": bogen(),
        "g-kronleuchter.svg": kronleuchter(),
        "g-gut.svg": gut(),
    }
    for name, markup in blaetter.items():
        (OUT / name).write_text(markup, encoding="utf-8")
        print(f"  {name:22} {len(markup):>6} B")
    print(f"{len(blaetter)} Blaetter nach {OUT.relative_to(OUT.parents[4])}")


if __name__ == "__main__":
    main()
