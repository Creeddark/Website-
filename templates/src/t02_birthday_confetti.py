"""
CONFETTI — Geburtstags-Suite.
Stil: 3D. Ballons mit Glanzlicht und Bodenreflex, Konfetti mit Tiefenschaerfe,
tiefes Indigo mit Gold. Drei Seiten: Einladung, Ablauf, Danke.
"""

import art
from common import W, H, page, text, svg_layer, document

NIGHT = "#140F33"
NIGHT_2 = "#3B1F63"
PLUM = "#5C2A78"
GOLD = "#F3C75E"
GOLD_DEEP = "#C99327"
CORAL = "#FF6E8A"
MINT = "#5FDFC0"
CREAM = "#FFF6E6"
WHITE_SOFT = "#EDE6F5"

FAMILIES = {"Bebas Neue", "Poppins", "Playfair Display"}

CONFETTI_COLORS = [GOLD, CORAL, MINT, "#FFFFFF", "#B98BE0", GOLD]


def _defs():
    return (
        art.linear_bg("bg", [(0, NIGHT), (0.45, "#2A1550"), (1, PLUM)], angle=105)
        + art.radial_bg("halo", [(0, GOLD, 0.5), (0.5, GOLD, 0.1), (1, GOLD, 0)], r=0.5)
        + art.radial_bg("halo2", [(0, CORAL, 0.36), (1, CORAL, 0)], r=0.5)
        + art.sphere_gradients("bGold", GOLD, light="#FFF3CE", shade="#A9741A")
        + art.sphere_gradients("bCoral", CORAL, light="#FFD3DC", shade="#B33C58")
        + art.sphere_gradients("bMint", MINT, light="#D6FFF4", shade="#2A9C82")
        + art.sphere_gradients("bPlum", "#9B6BD6", light="#E8D8FF", shade="#5A3390")
        + art.paper_grain("grain", opacity=0.07, freq=0.85)
        + art.soft_shadow("drop", dy=10, blur=16, opacity=0.4)
    )


def _backdrop():
    """Verlauf, Lichthoefe, Bokeh und Konfetti — die Tiefe der Seite."""
    return (
        f'<rect width="{W}" height="{H}" fill="url(#bg)"/>'
        f'<circle cx="{W * 0.52}" cy="240" r="420" fill="url(#halo)" opacity="0.75"/>'
        f'<circle cx="120" cy="880" r="300" fill="url(#halo2)" opacity="0.5"/>'
        + art.bokeh(11, W, H, CREAM, seed=6, rmin=10, rmax=34, opacity=0.055)
        + art.starfield(64, W, H, seed=12, color=CREAM, rmin=0.5, rmax=1.7)
    )


def _grain():
    return (f'<rect width="{W}" height="{H}" fill="{CREAM}" '
            f'filter="url(#grain)" opacity="0.5"/>')


def _balloon_cluster():
    """Ballontraube. Unterschiedliche Groesse, Neigung und Tiefe je Ballon."""
    b = []
    # hintere Ebene, kleiner und blasser
    b.append(f'<g opacity="0.55">'
             + art.balloon(148, 214, 40, "bPlum", tilt=-13, string_len=180,
                           string_sway=26)
             + art.balloon(612, 186, 34, "bMint", tilt=11, string_len=150,
                           string_sway=-22) + '</g>')
    # vordere Ebene
    b.append(art.balloon(232, 178, 60, "bCoral", tilt=-9, string_len=230,
                         string_sway=34))
    b.append(art.balloon(376, 138, 78, "bGold", tilt=3, string_len=250,
                         string_sway=-28))
    b.append(art.balloon(524, 190, 56, "bMint", tilt=12, string_len=220,
                         string_sway=30))
    return "".join(b)


def _confetti_layer(seed=4, n=54, avoid=()):
    return art.confetti(n, W, H, CONFETTI_COLORS, seed=seed, rmin=4, rmax=13,
                        avoid=avoid)


# ------------------------------------------------------------------- Seite 1

def p_invitation():
    svg = svg_layer(_defs(),
                    _backdrop() + _confetti_layer(seed=4, n=64,
                        avoid=[(60, 410, 630, 500)])
                    + _balloon_cluster() + _grain()
                    + art.tapered_rule(W / 2, 700, 150, color=GOLD, thickness=1.6))
    t = [
        text("PLEASE JOIN US TO CELEBRATE", left=75, top=422, width=600,
             size=11, family="Poppins", weight=400, color=WHITE_SOFT,
             tracking=0.4),
        text("MIA", left=75, top=452, width=600, size=96, family="Bebas Neue",
             weight=400, color=CREAM, tracking=0.06, line=1.0),
        text("TURNS", left=75, top=556, width=600, size=13, family="Poppins",
             weight=400, color=WHITE_SOFT, tracking=0.5),
        text("30", left=75, top=580, width=600, size=118, family="Bebas Neue",
             weight=400, color=GOLD, tracking=0.02, line=1.0),
        text("SATURDAY, 12 JUNE &nbsp;·&nbsp; 8 PM", left=75, top=730,
             width=600, size=13, family="Poppins", weight=600, color=CREAM,
             tracking=0.24),
        text("THE ROOFTOP &nbsp;·&nbsp; ODERBERGER STRASSE 12, BERLIN",
             left=75, top=766, width=600, size=10.5, family="Poppins",
             weight=400, color=WHITE_SOFT, tracking=0.22),
        text("Dress code: black &amp; gold", left=75, top=828, width=600,
             size=22, family="Playfair Display", weight=400, color=GOLD,
             style="italic"),
        text("RSVP BY 1 JUNE &nbsp;·&nbsp; +49 170 000 000", left=75, top=896,
             width=600, size=10, family="Poppins", weight=400, color=WHITE_SOFT,
             tracking=0.26),
    ]
    return page("\n".join([svg] + t), "Invitation", bg=NIGHT)


# ------------------------------------------------------------------- Seite 2

def _plan_row(top, time, title, note):
    return "\n".join([
        text(time, left=104, top=top + 5, width=108, size=13,
             family="Bebas Neue", weight=400, color=GOLD, tracking=0.14,
             align="right"),
        text(title, left=254, top=top, width=392, size=26, family="Bebas Neue",
             weight=400, color=CREAM, align="left", tracking=0.06, line=1.1),
        text(note, left=254, top=top + 34, width=392, size=10,
             family="Poppins", weight=400, color=WHITE_SOFT, tracking=0.18,
             align="left"),
    ])


def p_programme():
    rows = [(346, "20:00", "DOORS &amp; DRINKS", "ROOFTOP BAR"),
            (452, "21:00", "DINNER", "LONG TABLE"),
            (558, "22:30", "CAKE &amp; SPEECHES", "TERRACE"),
            (664, "23:00", "DANCEFLOOR OPENS", "UNTIL SUNRISE")]
    lines = "".join(
        f'<line x1="104" y1="{y}" x2="646" y2="{y}" stroke="{GOLD}" '
        f'stroke-width="0.7" opacity="0.35"/>' for y in (430, 536, 642))
    svg = svg_layer(_defs(),
                    _backdrop() + _confetti_layer(seed=17, n=48,
                        avoid=[(84, 206, 582, 700)]) + _grain()
                    + f'<g opacity="0.9">'
                    + art.balloon(96, 132, 40, "bCoral", tilt=-14, string_len=140,
                                  string_sway=22)
                    + art.balloon(662, 118, 34, "bGold", tilt=10, string_len=120,
                                  string_sway=-18) + '</g>'
                    + lines
                    + art.tapered_rule(W / 2, 782, 130, color=GOLD, thickness=1.4))
    t = [
        text("HOW THE NIGHT GOES", left=75, top=232, width=600, size=11,
             family="Poppins", weight=400, color=WHITE_SOFT, tracking=0.42),
        text("THE PLAN", left=75, top=262, width=600, size=72,
             family="Bebas Neue", weight=400, color=GOLD, tracking=0.05,
             line=1.0),
    ] + [_plan_row(*r) for r in rows] + [
        text("Getting here", left=104, top=812, width=542, size=24,
             family="Playfair Display", weight=400, color=CREAM, align="left",
             style="italic"),
        text("U2 Eberswalder Strasse, 4 minutes on foot.<br>"
             "Taxis stop at the corner of Kastanienallee.",
             left=104, top=852, width=542, size=12, family="Poppins",
             weight=300, color=WHITE_SOFT, line=1.85, align="left"),
    ]
    return page("\n".join([svg] + t), "The Plan", bg=NIGHT)


# ------------------------------------------------------------------- Seite 3

def p_thanks():
    svg = svg_layer(_defs(),
                    _backdrop() + _confetti_layer(seed=29, n=70,
                        avoid=[(60, 456, 630, 420)]) + _grain()
                    + art.balloon(200, 224, 54, "bMint", tilt=-11, string_len=200,
                                  string_sway=30)
                    + art.balloon(378, 176, 70, "bGold", tilt=4, string_len=220,
                                  string_sway=-24)
                    + art.balloon(552, 232, 48, "bCoral", tilt=13, string_len=190,
                                  string_sway=26)
                    + art.tapered_rule(W / 2, 662, 140, color=GOLD, thickness=1.5))
    t = [
        text("THANK YOU", left=75, top=470, width=600, size=86,
             family="Bebas Neue", weight=400, color=GOLD, tracking=0.06,
             line=1.0),
        text("FOR MAKING IT UNFORGETTABLE", left=75, top=572, width=600,
             size=11, family="Poppins", weight=400, color=WHITE_SOFT,
             tracking=0.36),
        text("What a night. Thank you for the dancing,<br>"
             "the toasts and every single laugh.",
             left=125, top=706, width=500, size=21,
             family="Playfair Display", weight=400, color=CREAM, line=1.8,
             style="italic"),
        text("MIA", left=75, top=846, width=600, size=13, family="Poppins",
             weight=600, color=WHITE_SOFT, tracking=0.4),
    ]
    return page("\n".join([svg] + t), "Thank You", bg=NIGHT)


def build():
    return document("CONFETTI — Birthday Suite", FAMILIES,
                    [p_invitation(), p_programme(), p_thanks()])


if __name__ == "__main__":
    import pathlib
    out = pathlib.Path(__file__).resolve().parent.parent / "dist" / "02-birthday-confetti.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build(), encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size // 1024} KB)")
