"""
OH BABY — Baby-Shower-Suite.
Stil: flach und weich. Salbei, Creme, Terrakotta, feines Blattwerk.
Vier Seiten: Einladung, Ratschlaege, Ratekarte, Danke.
"""

import art
from common import W, H, page, text, svg_layer, document

CREAM = "#FDFAF3"
CREAM_2 = "#F5EFE2"
SAGE = "#A6B79A"
SAGE_DEEP = "#778B6A"
SAGE_TINT = "#E9EEE3"
TERRA = "#C58A69"
TERRA_TINT = "#F6E7DE"
INK = "#39382F"
INK_SOFT = "#7A7768"

FAMILIES = {"Cormorant Garamond", "Montserrat", "Great Vibes"}


def _defs():
    return (art.paper_grain("grain", opacity=0.05, freq=0.88)
            + art.radial_bg("warm", [(0, TERRA, 0.14), (1, TERRA, 0)], r=0.5))


def _paper(bg=CREAM):
    return (f'<rect width="{W}" height="{H}" fill="{bg}"/>'
            f'<circle cx="640" cy="120" r="300" fill="url(#warm)" opacity="0.9"/>'
            f'<rect width="{W}" height="{H}" fill="#8A7F66" '
            f'filter="url(#grain)" opacity="0.85"/>')


def _frame():
    return (f'<rect x="34" y="34" width="{W - 68}" height="{H - 68}" fill="none" '
            f'stroke="{SAGE}" stroke-width="1" opacity="0.55"/>')


def _crown(cy=300, rx=196, ry=150):
    """Halbkranz oben — der Bogen bleibt der Hochzeit vorbehalten."""
    back = art.foliage_arc(W / 2, cy, rx + 14, ry + 14, 186, 354, sprigs=20,
                           stroke=SAGE, fill=SAGE_TINT, stroke_width=1.1,
                           length=36, leaf_r=11, seed=61, outward=1,
                           density_ends=0.45, spread=24, aspect=1.5)
    terra = art.foliage_arc(W / 2, cy, rx - 8, ry - 8, 196, 344, sprigs=11,
                            stroke=TERRA, fill=TERRA_TINT, stroke_width=1.0,
                            length=30, leaf_r=7, seed=12, outward=1,
                            density_ends=0.5, spread=36, aspect=2.2)
    front = art.foliage_arc(W / 2, cy, rx, ry, 190, 350, sprigs=24,
                            stroke=SAGE_DEEP, fill=SAGE_TINT, stroke_width=1.35,
                            length=42, leaf_r=14, seed=23, outward=1,
                            density_ends=0.42, spread=20, aspect=1.32)
    return (f'<g opacity="0.42">{back}</g><g opacity="0.7">{terra}</g>'
            f'<g opacity="0.95">{front}</g>')


def _spray(cx, cy, *, scale=1.0, opacity=0.9, terra=False, seed=5):
    col = TERRA if terra else SAGE_DEEP
    tint = TERRA_TINT if terra else SAGE_TINT
    parts = []
    for side in (1, -1):
        for i, (tilt, ln, lv) in enumerate([(0, 1.0, 4), (17, 0.7, 3), (-16, 0.55, 3)]):
            parts.append(art.sprig(
                cx + 4 * side, cy, (0 if side > 0 else 180) + tilt * side,
                leaves=lv, length=70 * ln * scale, leaf_r=11 * ln * scale,
                curve=15 * scale, stroke=col, fill=tint, stroke_width=1.2,
                seed=seed + i * 5 + (0 if side > 0 else 4), aspect=1.34))
    return f'<g opacity="{opacity}">{"".join(parts)}</g>'


def _corner(x, y, angle, *, scale=1.0, seed=3, opacity=0.85):
    """Eck-Zweig — bringt Bewegung in sonst leere Seitenraender."""
    parts = []
    for i, (tilt, ln) in enumerate([(0, 1.0), (26, 0.74), (-24, 0.66), (52, 0.5)]):
        parts.append(art.sprig(x, y, angle + tilt, leaves=4,
                               length=92 * ln * scale, leaf_r=12.5 * ln * scale,
                               curve=22 * scale, stroke=SAGE_DEEP,
                               fill=SAGE_TINT, stroke_width=1.25,
                               seed=seed + i * 9, aspect=1.36))
    return f'<g opacity="{opacity}">{"".join(parts)}</g>'


# ------------------------------------------------------------------- Seite 1

def p_invitation():
    svg = svg_layer(_defs(),
                    _paper() + _frame() + _crown(cy=304, rx=200, ry=154)
                    + art.tapered_rule(W / 2, 700, 140, color=TERRA, thickness=1.4)
                    + _spray(W / 2, 950, scale=0.72, opacity=0.75))
    t = [
        text("PLEASE JOIN US FOR A BABY SHOWER HONOURING", left=105, top=372,
             width=540, size=10, family="Montserrat", weight=400,
             color=INK_SOFT, tracking=0.26),
        text("Oh Baby", left=155, top=404, width=440, size=92,
             family="Great Vibes", weight=400, color=SAGE_DEEP, line=1.15),
        text("CLARA &amp; MATHIS", left=155, top=548, width=440, size=13,
             family="Montserrat", weight=500, color=INK, tracking=0.4),
        text("are expecting a little one", left=155, top=580, width=440,
             size=21, family="Cormorant Garamond", weight=300, color=INK_SOFT,
             style="italic"),
        text("Saturday, the Ninth of March", left=75, top=728, width=600,
             size=28, family="Cormorant Garamond", weight=400, color=INK,
             line=1.2),
        text("AT TWO IN THE AFTERNOON", left=75, top=772, width=600, size=10,
             family="Montserrat", weight=400, color=INK_SOFT, tracking=0.28),
        text("THE GREENHOUSE &nbsp;·&nbsp; PARKSTRASSE 8, LEIPZIG", left=75,
             top=818, width=600, size=10, family="Montserrat", weight=400,
             color=INK_SOFT, tracking=0.24),
        text("RSVP BY 1 MARCH &nbsp;·&nbsp; clara-and-mathis.com", left=75,
             top=880, width=600, size=10, family="Montserrat", weight=400,
             color=TERRA, tracking=0.24),
    ]
    return page("\n".join([svg] + t), "Invitation", bg=CREAM)


# ------------------------------------------------------------------- Seite 2

def p_advice():
    lines = "".join(
        f'<line x1="118" y1="{y}" x2="632" y2="{y}" stroke="{SAGE}" '
        f'stroke-width="0.9" opacity="0.6"/>'
        for y in (452, 528, 604, 680, 756, 832))
    svg = svg_layer(_defs(),
                    _paper() + _frame()
                    + _spray(W / 2, 352, scale=0.78, opacity=0.9)
                    + lines
                    + _spray(W / 2, 936, scale=0.62, opacity=0.7, terra=True,
                             seed=41))
    t = [
        text("A LITTLE WISDOM", left=75, top=180, width=600, size=10.5,
             family="Montserrat", weight=400, color=INK_SOFT, tracking=0.38),
        text("Advice for the<br>New Parents", left=75, top=210, width=600,
             size=50, family="Cormorant Garamond", weight=400, color=INK,
             line=1.18),
        text("The best thing we ever learned was&hellip;", left=118, top=396,
             width=514, size=21, family="Cormorant Garamond", weight=300,
             color=INK_SOFT, style="italic", align="left"),
        text("FROM", left=118, top=880, width=250, size=9,
             family="Montserrat", weight=500, color=TERRA, tracking=0.34,
             align="left"),
    ]
    return page("\n".join([svg] + t), "Advice Card", bg=CREAM)


# ------------------------------------------------------------------- Seite 3

def _guess_row(top, label, hint):
    return "\n".join([
        text(label, left=118, top=top, width=514, size=9.5,
             family="Montserrat", weight=500, color=TERRA, tracking=0.34,
             align="left"),
        text(hint, left=118, top=top + 20, width=514, size=19,
             family="Cormorant Garamond", weight=300, color=INK_SOFT,
             style="italic", align="left"),
    ])


def p_guess():
    rows = [(396, "DATE OF ARRIVAL", "my guess for the big day"),
            (516, "WEIGHT &amp; LENGTH", "how big will the little one be"),
            (636, "EYE COLOUR", "mother&rsquo;s or father&rsquo;s"),
            (756, "THE NAME", "what will they choose")]
    lines = "".join(
        f'<line x1="118" y1="{y}" x2="632" y2="{y}" stroke="{SAGE}" '
        f'stroke-width="0.9" opacity="0.6"/>' for y in (466, 586, 706, 826))
    svg = svg_layer(_defs(),
                    _paper(CREAM_2) + _frame()
                    + _spray(W / 2, 300, scale=0.8, opacity=0.9, terra=True, seed=19)
                    + lines
                    + art.tapered_rule(W / 2, 892, 120, color=TERRA, thickness=1.3))
    t = [
        text("PLACE YOUR BETS", left=75, top=180, width=600, size=10.5,
             family="Montserrat", weight=400, color=INK_SOFT, tracking=0.38),
        text("Guess the Baby", left=75, top=210, width=600, size=52,
             family="Cormorant Garamond", weight=400, color=INK, line=1.15),
    ] + [_guess_row(*r) for r in rows] + [
        text("Closest guess wins a prize", left=75, top=920, width=600,
             size=24, family="Great Vibes", weight=400, color=SAGE_DEEP),
    ]
    return page("\n".join([svg] + t), "Guess the Baby", bg=CREAM_2)


# ------------------------------------------------------------------- Seite 4

def p_thanks():
    svg = svg_layer(_defs(),
                    _paper() + _frame()
                    + art.wreath(W / 2, 406, 200, ry=180, stroke=SAGE_DEEP,
                                 fill=SAGE_TINT, stroke_width=1.3, seed=31,
                                 leaf_r=13.5, sprigs=20, length=40, gap_deg=46)
                    + art.wreath(W / 2, 406, 172, ry=154, stroke=TERRA,
                                 fill=TERRA_TINT, stroke_width=1.0, seed=44,
                                 leaf_r=7, sprigs=13, length=26, gap_deg=68,
                                 aspect=2.2)
                    + art.tapered_rule(W / 2, 674, 128, color=TERRA, thickness=1.3))
    t = [
        text("Thank you", left=175, top=350, width=400, size=62,
             family="Great Vibes", weight=400, color=SAGE_DEEP, line=1.1),
        text("FOR SHOWERING US WITH LOVE", left=175, top=450, width=400,
             size=10, family="Montserrat", weight=400, color=INK_SOFT,
             tracking=0.28),
        text("Thank you for the gifts, the good advice<br>"
             "and for making this day so warm.",
             left=145, top=722, width=460, size=21,
             family="Cormorant Garamond", weight=300, color=INK, line=1.75,
             style="italic"),
        text("CLARA &amp; MATHIS", left=75, top=884, width=600, size=11,
             family="Montserrat", weight=500, color=INK, tracking=0.34),
    ]
    return page("\n".join([svg] + t), "Thank You", bg=CREAM)


def build():
    return document("OH BABY — Baby Shower Suite", FAMILIES,
                    [p_invitation(), p_advice(), p_guess(), p_thanks()])


if __name__ == "__main__":
    import pathlib
    out = pathlib.Path(__file__).resolve().parent.parent / "dist" / "04-baby-shower.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build(), encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size // 1024} KB)")
