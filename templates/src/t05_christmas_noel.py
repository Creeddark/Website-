"""
NOEL — Weihnachts-Suite.
Stil: 3D. Glaenzende Kugeln in Gold und Burgunder, Tannengruen, Schneefall.
Drei Seiten: Einladung, Menue, Grusskarte.
"""

import art
from common import W, H, page, text, svg_layer, document

FOREST = "#0D2820"
FOREST_2 = "#16412F"
PINE = "#2E6247"
PINE_LIGHT = "#5C8F6E"
BURGUNDY = "#7A1F2B"
GOLD = "#D9B369"
GOLD_LIGHT = "#F2DFAE"
CREAM = "#F8F1E2"
CREAM_SOFT = "#D9CDB4"

FAMILIES = {"Cinzel", "Cinzel Decorative", "Montserrat", "Great Vibes"}


def _defs():
    return (
        art.linear_bg("bg", [(0, "#08201A"), (0.5, FOREST), (1, FOREST_2)],
                      angle=110)
        + art.radial_bg("warm", [(0, GOLD, 0.28), (1, GOLD, 0)], r=0.5)
        + art.radial_bg("warm2", [(0, BURGUNDY, 0.4), (1, BURGUNDY, 0)], r=0.5)
        + art.sphere_gradients("oGold", GOLD, light="#FFF6DE", shade="#8E6B22")
        + art.sphere_gradients("oRed", "#9E2A38", light="#F0B6BC", shade="#5A1019")
        + art.sphere_gradients("oCream", CREAM, light="#FFFFFF", shade="#B4A98C")
        + art.sphere_gradients("oGreen", PINE, light="#B9D9C4", shade="#123425")
        + art.paper_grain("grain", opacity=0.06, freq=0.85)
    )


def _backdrop(snow_avoid=()):
    return (f'<rect width="{W}" height="{H}" fill="url(#bg)"/>'
            f'<circle cx="375" cy="180" r="380" fill="url(#warm)" opacity="0.9"/>'
            f'<circle cx="90" cy="900" r="280" fill="url(#warm2)" opacity="0.5"/>'
            + art.snowfall(140, W, H, seed=3, color=CREAM, avoid=snow_avoid))


def _grain():
    return (f'<rect width="{W}" height="{H}" fill="{CREAM}" '
            f'filter="url(#grain)" opacity="0.4"/>')


def _frame():
    return (f'<rect x="36" y="36" width="{W - 72}" height="{H - 72}" fill="none" '
            f'stroke="{GOLD}" stroke-width="1.1" opacity="0.6"/>'
            f'<rect x="45" y="45" width="{W - 90}" height="{H - 90}" fill="none" '
            f'stroke="{GOLD}" stroke-width="0.5" opacity="0.35"/>')


def _pine_swag(cy=150, half_w=252, sag=86):
    """Tannengirlande aus gestreuten Wedeln in zwei Tiefen."""
    back = art.pine_garland(W / 2, cy - 10, half_w + 14, sag * 0.82, n=17,
                            length=17, stroke="#1E4A36", stroke_width=1.0,
                            seed=9, pairs=11, spread=30)
    front = art.pine_garland(W / 2, cy, half_w, sag, n=21, length=21,
                             stroke=PINE, stroke_light=PINE_LIGHT,
                             stroke_width=1.15, seed=4, pairs=13, spread=24)
    return f'<g opacity="0.6">{back}</g><g opacity="0.95">{front}</g>'


def _ornaments():
    """Kugeln haengen an der Girlande — verschiedene Hoehen und Groessen."""
    return (
        art.bauble(196, 300, 30, "oRed", cap=GOLD, string_top=176, tilt=-4)
        + art.bauble(286, 352, 24, "oCream", cap=GOLD, string_top=196, tilt=3)
        + art.bauble(375, 316, 38, "oGold", cap=GOLD, string_top=182, tilt=-2)
        + art.bauble(464, 358, 22, "oGreen", cap=GOLD, string_top=196, tilt=4)
        + art.bauble(556, 296, 28, "oRed", cap=GOLD, string_top=176, tilt=-3)
    )


def _sprig_pair(cx, cy, *, scale=1.0, opacity=0.9):
    a = art.fern_frond((cx - 96 * scale, cy), (cx - 56 * scale, cy - 16 * scale),
                       (cx - 26 * scale, cy - 8 * scale), (cx, cy),
                       pairs=14, length=17 * scale, stroke=PINE_LIGHT,
                       stroke_width=1.1, seed=5)
    b = art.fern_frond((cx + 96 * scale, cy), (cx + 56 * scale, cy - 16 * scale),
                       (cx + 26 * scale, cy - 8 * scale), (cx, cy),
                       pairs=14, length=17 * scale, stroke=PINE_LIGHT,
                       stroke_width=1.1, seed=12)
    berries = "".join(
        f'<circle cx="{cx + dx * scale}" cy="{cy + dy * scale}" '
        f'r="{3.4 * scale}" fill="{BURGUNDY}"/>'
        for dx, dy in ((-13, 3), (0, -4), (12, 4)))
    return f'<g opacity="{opacity}">{a}{b}{berries}</g>'


# ------------------------------------------------------------------- Seite 1

def p_invitation():
    svg = svg_layer(_defs(),
                    _backdrop([(64, 440, 622, 470)]) + _frame() + _pine_swag(150, 252, 88)
                    + _ornaments() + _grain()
                    + "".join(art.snowflake(x, y, r, color=CREAM, opacity=op,
                                            stroke_width=1.2, seed=s)
                              for x, y, r, op, s in
                              ((96, 470, 17, 0.4, 1), (662, 560, 13, 0.32, 2),
                               (84, 720, 11, 0.28, 3), (668, 296, 15, 0.3, 4)))
                    + art.tapered_rule(W / 2, 690, 150, color=GOLD, thickness=1.5)
                    + _sprig_pair(W / 2, 940, scale=0.85, opacity=0.88))
    t = [
        text("YOU ARE WARMLY INVITED TO", left=105, top=452, width=540,
             size=10, family="Montserrat", weight=400, color=CREAM_SOFT,
             tracking=0.34),
        text("NOEL", left=75, top=482, width=600, size=82,
             family="Cinzel Decorative", weight=700, color=GOLD, tracking=0.1,
             line=1.1),
        text("a christmas dinner", left=75, top=606, width=600, size=34,
             family="Great Vibes", weight=400, color=CREAM, line=1.2),
        text("Saturday, the Twentieth of December", left=75, top=716,
             width=600, size=26, family="Cinzel", weight=400, color=CREAM,
             line=1.3, tracking=0.02),
        text("SEVEN IN THE EVENING", left=75, top=762, width=600, size=10,
             family="Montserrat", weight=400, color=CREAM_SOFT, tracking=0.3),
        text("THE OLD MILL &nbsp;·&nbsp; AM MUEHLENWEG 3, WEIMAR", left=75,
             top=808, width=600, size=10, family="Montserrat", weight=400,
             color=CREAM_SOFT, tracking=0.24),
        text("BLACK TIE &nbsp;·&nbsp; RSVP BY 10 DECEMBER", left=75, top=868,
             width=600, size=10, family="Montserrat", weight=400, color=GOLD,
             tracking=0.26),
    ]
    return page("\n".join([svg] + t), "Invitation", bg=FOREST)


# ------------------------------------------------------------------- Seite 2

def _course(top, label, dish, note):
    return "\n".join([
        text(label, left=105, top=top, width=540, size=9.5,
             family="Montserrat", weight=500, color=GOLD, tracking=0.38),
        text(dish, left=105, top=top + 22, width=540, size=27,
             family="Cinzel", weight=400, color=CREAM, line=1.25),
        text(note, left=140, top=top + 62, width=470, size=17,
             family="Great Vibes", weight=400, color=CREAM_SOFT),
    ])


def p_menu():
    courses = [(336, "TO BEGIN", "Chestnut Velouté", "brown butter, sage, hazelnut"),
               (466, "THE FISH", "Cured Trout", "beetroot, dill, horseradish cream"),
               (596, "THE ROAST", "Venison &amp; Red Cabbage", "juniper jus, potato gratin"),
               (726, "TO FINISH", "Spiced Pear Tart", "vanilla, clove, warm cream")]
    rules = "".join(art.tapered_rule(W / 2, y, 96, color=GOLD, thickness=1.1)
                    for y in (438, 568, 698))
    svg = svg_layer(_defs(),
                    _backdrop([(84, 160, 582, 720)]) + _frame()
                    + _sprig_pair(W / 2, 294, scale=0.8, opacity=0.9)
                    + rules + _grain()
                    + art.bauble(96, 132, 24, "oRed", cap=GOLD, string_top=46, tilt=-5)
                    + art.bauble(654, 118, 21, "oGold", cap=GOLD, string_top=46, tilt=5)
                    + _sprig_pair(W / 2, 912, scale=0.78, opacity=0.85))
    t = [
        text("CHRISTMAS DINNER", left=75, top=168, width=600, size=10,
             family="Montserrat", weight=400, color=CREAM_SOFT, tracking=0.4),
        text("MENU", left=75, top=196, width=600, size=58,
             family="Cinzel Decorative", weight=700, color=GOLD, tracking=0.14,
             line=1.1),
    ] + [_course(*c) for c in courses] + [
        text("with mulled wine on arrival", left=75, top=846, width=600,
             size=22, family="Great Vibes", weight=400, color=CREAM_SOFT),
    ]
    return page("\n".join([svg] + t), "Menu", bg=FOREST)


# ------------------------------------------------------------------- Seite 3

def p_greeting():
    svg = svg_layer(_defs(),
                    _backdrop([(110, 320, 530, 580)]) + _frame()
                    + art.wreath(W / 2, 388, 190, ry=176, stroke=PINE_LIGHT,
                                 stroke_width=1.15, seed=17, leaf_r=10,
                                 sprigs=22, length=34, gap_deg=40, aspect=2.6)
                    + "".join(
                        f'<circle cx="{375 + dx}" cy="{388 + dy}" r="{r}" '
                        f'fill="{BURGUNDY}" opacity="0.9"/>'
                        for dx, dy, r in ((-168, -66, 5), (162, -78, 4.4),
                                          (-150, 96, 4.8), (156, 92, 5.2),
                                          (-14, 190, 4.6), (26, 186, 4)))
                    + art.bauble(375, 196, 26, "oGold", cap=GOLD, string_top=92,
                                 tilt=0)
                    + _grain()
                    + art.tapered_rule(W / 2, 664, 140, color=GOLD, thickness=1.4))
    t = [
        text("Merry Christmas", left=155, top=336, width=440, size=54,
             family="Great Vibes", weight=400, color=GOLD, line=1.15),
        text("AND A BRIGHT NEW YEAR", left=155, top=436, width=440, size=10,
             family="Montserrat", weight=400, color=CREAM_SOFT, tracking=0.34),
        text("Thank you for the warmth you bring<br>"
             "to our table and to our year.",
             left=135, top=716, width=480, size=22, family="Cinzel",
             weight=400, color=CREAM, line=1.75),
        text("THE HOFFMANN FAMILY", left=75, top=872, width=600, size=10.5,
             family="Montserrat", weight=500, color=GOLD, tracking=0.36),
    ]
    return page("\n".join([svg] + t), "Christmas Greeting", bg=FOREST)


def build():
    return document("NOEL — Christmas Suite", FAMILIES,
                    [p_invitation(), p_menu(), p_greeting()],
                    body_bg="#1A1A18")


if __name__ == "__main__":
    import pathlib
    out = pathlib.Path(__file__).resolve().parent.parent / "dist" / "05-christmas-noel.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build(), encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size // 1024} KB)")
