"""
REVEAL — Gender-Reveal-Suite.
Stil: 3D, hell. Glaenzende Ballons in Rosa und Blau, weiche Lichtstimmung.
Vier Seiten: Einladung, Stimmkarte, Verkuendung, Danke.
"""

import art
from common import W, H, page, text, svg_layer, document

CREAM = "#FFF9F5"
CREAM_2 = "#FDEFE8"
INK = "#3B3340"
INK_SOFT = "#8A7F90"
PINK = "#F191AF"
PINK_DEEP = "#D95A85"
BLUE = "#8CC0E6"
BLUE_DEEP = "#4A87BE"
GOLD = "#CFA45F"

FAMILIES = {"Fredoka", "Poppins", "Playfair Display", "Great Vibes"}


def _defs():
    return (
        art.linear_bg("bg", [(0, CREAM), (0.5, "#FFF4EE"), (1, CREAM_2)], angle=115)
        + art.radial_bg("glowP", [(0, PINK, 0.4), (1, PINK, 0)], r=0.5)
        + art.radial_bg("glowB", [(0, BLUE, 0.4), (1, BLUE, 0)], r=0.5)
        + art.sphere_gradients("bPink", PINK, light="#FFE1EB", shade="#C05579")
        + art.sphere_gradients("bBlue", BLUE, light="#DCF0FF", shade="#3E77A8")
        + art.sphere_gradients("bCream", "#FFFFFF", light="#FFFFFF", shade="#E4D8D2")
        + art.sphere_gradients("bGold", "#EBC98A", light="#FFF6E0", shade="#B18B45")
        + art.paper_grain("grain", opacity=0.045, freq=0.9)
    )


def _backdrop():
    return (
        f'<rect width="{W}" height="{H}" fill="url(#bg)"/>'
        f'<circle cx="70" cy="300" r="330" fill="url(#glowP)" opacity="0.75"/>'
        f'<circle cx="690" cy="380" r="330" fill="url(#glowB)" opacity="0.75"/>'
        f'<circle cx="400" cy="1010" r="290" fill="url(#glowP)" opacity="0.4"/>'
    )


def _grain():
    return (f'<rect width="{W}" height="{H}" fill="#8A7B72" '
            f'filter="url(#grain)" opacity="0.85"/>')


def _confetti(seed, n, avoid=()):
    return art.confetti(n, W, H, [PINK, BLUE, "#FFFFFF", GOLD, PINK, BLUE],
                        seed=seed, rmin=4, rmax=12, avoid=avoid)


def _cluster_hero():
    """Grosser heller Ballon in der Mitte, Rosa links, Blau rechts."""
    return (
        f'<g opacity="0.6">'
        + art.balloon(126, 230, 40, "bPink", tilt=-15, string_len=170, string_sway=24)
        + art.balloon(636, 214, 36, "bBlue", tilt=13, string_len=160, string_sway=-22)
        + '</g>'
        + art.balloon(214, 208, 62, "bPink", tilt=-10, string_len=228, string_sway=32)
        + art.balloon(540, 202, 60, "bBlue", tilt=11, string_len=222, string_sway=-30)
        + art.balloon(376, 168, 88, "bCream", tilt=2, string_len=252, string_sway=-20)
    )


# ------------------------------------------------------------------- Seite 1

def p_invitation():
    svg = svg_layer(_defs(),
                    _backdrop() + _confetti(4, 44, avoid=[(60, 400, 630, 520)])
                    + _cluster_hero() + _grain()
                    + art.tapered_rule(W / 2, 636, 140, color=GOLD, thickness=1.4))
    t = [
        # Das Fragezeichen sitzt auf dem hellen Ballon.
        text("?", left=276, top=118, width=200, size=96, family="Fredoka",
             weight=600, color="#D8C7CE", line=1.0),
        text("PLEASE JOIN US AS WE FIND OUT", left=75, top=414, width=600,
             size=10.5, family="Poppins", weight=400, color=INK_SOFT,
             tracking=0.38),
        text('<span style="color:' + BLUE_DEEP + '">HE</span> '
             '<span style="color:' + INK_SOFT + '">or</span> '
             '<span style="color:' + PINK_DEEP + '">SHE</span>',
             left=75, top=446, width=600, size=74, family="Fredoka",
             weight=600, color=INK, line=1.1, tracking=0.01),
        text("BABY WEBER", left=75, top=558, width=600, size=13,
             family="Poppins", weight=600, color=INK, tracking=0.42),
        text("Sunday, the Fourteenth of September", left=75, top=670,
             width=600, size=27, family="Playfair Display", weight=400,
             color=INK, line=1.25),
        text("AT THREE IN THE AFTERNOON", left=75, top=714, width=600,
             size=10, family="Poppins", weight=400, color=INK_SOFT,
             tracking=0.28),
        text("THE GARDEN HOUSE &nbsp;·&nbsp; SEESTRASSE 4, POTSDAM",
             left=75, top=760, width=600, size=10, family="Poppins",
             weight=400, color=INK_SOFT, tracking=0.24),
        text("Wear pink or blue &mdash; and pick your team", left=75, top=822,
             width=600, size=23, family="Great Vibes", weight=400, color=GOLD),
        text("RSVP BY 1 SEPTEMBER &nbsp;·&nbsp; 0170 000 0000", left=75,
             top=896, width=600, size=10, family="Poppins", weight=400,
             color=INK_SOFT, tracking=0.26),
    ]
    return page("\n".join([svg] + t), "Invitation", bg=CREAM)


# ------------------------------------------------------------------- Seite 2

def p_vote():
    """Stimmkarte: zwei Felder, eines rosa, eines blau."""
    cards = ""
    for x, col, tint in ((84, BLUE_DEEP, "#E6F1FA"), (390, PINK_DEEP, "#FCE8EF")):
        cards += (f'<rect x="{x}" y="352" width="276" height="330" rx="16" '
                  f'fill="{tint}" stroke="{col}" stroke-width="1.6" '
                  f'opacity="0.95"/>')
    boxes = "".join(
        f'<rect x="{x}" y="596" width="22" height="22" rx="4" fill="#FFFFFF" '
        f'stroke="{col}" stroke-width="1.6"/>'
        for x, col in ((211, BLUE_DEEP), (517, PINK_DEEP)))
    lines = "".join(
        f'<line x1="120" y1="{y}" x2="630" y2="{y}" stroke="{GOLD}" '
        f'stroke-width="0.9" opacity="0.5"/>' for y in (786, 866))
    svg = svg_layer(_defs(),
                    _backdrop() + _confetti(21, 30, avoid=[(70, 180, 610, 730)])
                    + _grain()
                    + art.balloon(96, 148, 34, "bPink", tilt=-14, string_len=120,
                                  string_sway=20)
                    + art.balloon(658, 140, 32, "bBlue", tilt=12, string_len=110,
                                  string_sway=-18)
                    + cards + boxes + lines)
    t = [
        text("CAST YOUR VOTE", left=75, top=206, width=600, size=10.5,
             family="Poppins", weight=400, color=INK_SOFT, tracking=0.42),
        text("What Do You Think?", left=75, top=238, width=600, size=48,
             family="Playfair Display", weight=400, color=INK, line=1.15),
        text("TEAM", left=84, top=396, width=276, size=11, family="Poppins",
             weight=500, color=BLUE_DEEP, tracking=0.4),
        text("BOY", left=84, top=424, width=276, size=62, family="Fredoka",
             weight=600, color=BLUE_DEEP, line=1.05),
        text("blue eyes &amp; muddy knees", left=84, top=514, width=276,
             size=19, family="Great Vibes", weight=400, color=INK_SOFT),
        text("TEAM", left=390, top=396, width=276, size=11, family="Poppins",
             weight=500, color=PINK_DEEP, tracking=0.4),
        text("GIRL", left=390, top=424, width=276, size=62, family="Fredoka",
             weight=600, color=PINK_DEEP, line=1.05),
        text("ribbons &amp; wild flowers", left=390, top=514, width=276,
             size=19, family="Great Vibes", weight=400, color=INK_SOFT),
        text("YOUR NAME", left=120, top=756, width=510, size=9,
             family="Poppins", weight=500, color=GOLD, tracking=0.34,
             align="left"),
        text("YOUR GUESS FOR THE NAME", left=120, top=836, width=510, size=9,
             family="Poppins", weight=500, color=GOLD, tracking=0.34,
             align="left"),
        text("Winners get the first slice of cake", left=75, top=916,
             width=600, size=21, family="Great Vibes", weight=400, color=INK_SOFT),
    ]
    return page("\n".join([svg] + t), "Cast Your Vote", bg=CREAM)


# ------------------------------------------------------------------- Seite 3

def p_announcement():
    """Verkuendung. Ein Wort wird ausgetauscht — der Rest bleibt stehen."""
    svg = svg_layer(_defs(),
                    _backdrop() + _confetti(33, 78, avoid=[(60, 430, 630, 330)])
                    + art.balloon(150, 246, 46, "bPink", tilt=-13, string_len=190,
                                  string_sway=28)
                    + art.balloon(600, 232, 44, "bBlue", tilt=12, string_len=180,
                                  string_sway=-26)
                    + art.balloon(258, 176, 58, "bCream", tilt=-5, string_len=230,
                                  string_sway=24)
                    + art.balloon(492, 182, 56, "bGold", tilt=8, string_len=224,
                                  string_sway=-22)
                    + art.balloon(376, 138, 74, "bPink", tilt=1, string_len=250,
                                  string_sway=-18)
                    + _grain()
                    + art.tapered_rule(W / 2, 806, 150, color=GOLD, thickness=1.5))
    t = [
        text("IT&rsquo;S A", left=75, top=468, width=600, size=13,
             family="Poppins", weight=500, color=INK_SOFT, tracking=0.5),
        text("GIRL", left=75, top=500, width=600, size=136, family="Fredoka",
             weight=600, color=PINK_DEEP, line=1.0, tracking=0.02),
        text("Amalia Rose", left=75, top=672, width=600, size=52,
             family="Great Vibes", weight=400, color=GOLD, line=1.2),
        text("ARRIVING FEBRUARY 2028", left=75, top=848, width=600, size=11,
             family="Poppins", weight=400, color=INK_SOFT, tracking=0.36),
        text("with all our love &mdash; Lena &amp; Tom", left=75, top=896,
             width=600, size=20, family="Playfair Display", weight=400,
             color=INK, style="italic"),
    ]
    return page("\n".join([svg] + t), "It's a Girl", bg=CREAM)


# ------------------------------------------------------------------- Seite 4

def p_thanks():
    svg = svg_layer(_defs(),
                    _backdrop() + _confetti(47, 40, avoid=[(60, 330, 630, 560)])
                    + art.balloon(228, 214, 52, "bPink", tilt=-12, string_len=200,
                                  string_sway=30)
                    + art.balloon(376, 166, 66, "bCream", tilt=2, string_len=232,
                                  string_sway=-22)
                    + art.balloon(524, 220, 50, "bBlue", tilt=12, string_len=196,
                                  string_sway=26)
                    + _grain()
                    + art.tapered_rule(W / 2, 656, 130, color=GOLD, thickness=1.4))
    t = [
        text("Thank you", left=75, top=444, width=600, size=78,
             family="Great Vibes", weight=400, color=GOLD, line=1.1),
        text("FOR GUESSING WITH US", left=75, top=566, width=600, size=10.5,
             family="Poppins", weight=400, color=INK_SOFT, tracking=0.36),
        text("Thank you for the confetti, the guesses<br>"
             "and for celebrating our little secret.",
             left=125, top=712, width=500, size=21,
             family="Playfair Display", weight=400, color=INK, line=1.8,
             style="italic"),
        text("LENA &amp; TOM", left=75, top=872, width=600, size=11.5,
             family="Poppins", weight=600, color=INK, tracking=0.4),
    ]
    return page("\n".join([svg] + t), "Thank You", bg=CREAM)


def build():
    return document("REVEAL — Gender Reveal Suite", FAMILIES,
                    [p_invitation(), p_vote(), p_announcement(), p_thanks()])


if __name__ == "__main__":
    import pathlib
    out = pathlib.Path(__file__).resolve().parent.parent / "dist" / "03-gender-reveal.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build(), encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size // 1024} KB)")
