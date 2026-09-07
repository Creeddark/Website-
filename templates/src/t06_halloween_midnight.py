"""
MIDNIGHT — Halloween-Suite.
Stil: flach und grafisch. Vollmond, Fledermausschwarm, Spinnennetz,
giftiges Orange auf Mitternachtsblau. Drei Seiten: Einladung, Details, Danke.
"""

import art
from common import W, H, page, text, svg_layer, document

NIGHT = "#0A0912"
NIGHT_2 = "#171029"
PLUM = "#241736"
ORANGE = "#FF7A29"
ORANGE_SOFT = "#FFA95E"
TOXIC = "#A7E05A"
BONE = "#EDE6D6"
BONE_SOFT = "#B7AE9B"
BLOOD = "#9E1F1B"

FAMILIES = {"Creepster", "Cinzel Decorative", "Poppins", "Montserrat"}


def _defs():
    return (
        art.linear_bg("bg", [(0, NIGHT), (0.55, NIGHT_2), (1, PLUM)], angle=100)
        + art.radial_bg("moonGlow", [(0, "#FFF3C8", 0.5), (0.4, "#FFD98A", 0.16),
                                     (1, "#FFD98A", 0)], r=0.5)
        + art.radial_bg("acid", [(0, TOXIC, 0.22), (1, TOXIC, 0)], r=0.5)
        + art.radial_bg("ember", [(0, ORANGE, 0.3), (1, ORANGE, 0)], r=0.5)
        + art.paper_grain("grain", opacity=0.08, freq=0.8)
    )


def _sky():
    return (f'<rect width="{W}" height="{H}" fill="url(#bg)"/>'
            + art.starfield(120, W, H, seed=7, color=BONE, rmin=0.4, rmax=1.8)
            + f'<circle cx="120" cy="930" r="290" fill="url(#acid)" opacity="0.8"/>'
            + f'<circle cx="660" cy="820" r="240" fill="url(#ember)" opacity="0.55"/>')


def _grain():
    return (f'<rect width="{W}" height="{H}" fill="{BONE}" '
            f'filter="url(#grain)" opacity="0.35"/>')


def _frame():
    return (f'<rect x="34" y="34" width="{W - 68}" height="{H - 68}" fill="none" '
            f'stroke="{ORANGE}" stroke-width="1.1" opacity="0.5"/>')


def _moon(cx=375, cy=252, r=124):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r * 2.3}" fill="url(#moonGlow)"/>'
            + art.moon(cx, cy, r, color="#F8ECC4", crater_color="#DCCB9C",
                       craters=9, seed=6))


def _dead_branch(x0, y0, x1, y1, cx1, cy1, cx2, cy2, *, width=3.2, twigs=5,
                 seed=1, color=NIGHT):
    """Kahler Ast — die Zweige sitzen unregelmaessig und werden zur Spitze duenner."""
    import math
    import random
    rnd = random.Random(seed)
    out = [f'<path d="M{x0},{y0} C{cx1},{cy1} {cx2},{cy2} {x1},{y1}" '
           f'fill="none" stroke="{color}" stroke-width="{width}" '
           f'stroke-linecap="round"/>']
    for i in range(twigs):
        t = 0.18 + (i / max(twigs - 1, 1)) * 0.7
        u = 1 - t
        px = (u ** 3 * x0 + 3 * u * u * t * cx1 + 3 * u * t * t * cx2 + t ** 3 * x1)
        py = (u ** 3 * y0 + 3 * u * u * t * cy1 + 3 * u * t * t * cy2 + t ** 3 * y1)
        ln = (34 + rnd.random() * 46) * (1 - t * 0.5)
        ang = math.radians(rnd.uniform(-140, -40) if y1 < y0 else rnd.uniform(40, 140))
        ex, ey = px + math.cos(ang) * ln, py + math.sin(ang) * ln
        mx, my = px + math.cos(ang - 0.4) * ln * 0.6, py + math.sin(ang - 0.4) * ln * 0.6
        out.append(f'<path d="M{px:.1f},{py:.1f} Q{mx:.1f},{my:.1f} {ex:.1f},{ey:.1f}" '
                   f'fill="none" stroke="{color}" stroke-width="{width * 0.5:.1f}" '
                   f'stroke-linecap="round"/>')
    return "".join(out)


# ------------------------------------------------------------------- Seite 1

def p_invitation():
    svg = svg_layer(_defs(),
                    _sky() + _moon(375, 250, 126)
                    + _dead_branch(-30, 62, 292, 286, 116, 54, 168, 258,
                                   width=5.4, twigs=7, seed=3, color="#050409")
                    + _dead_branch(782, 104, 528, 318, 654, 86, 606, 286,
                                   width=4.2, twigs=6, seed=9, color="#050409")
                    + art.bat(336, 306, 62, color="#050409", flap=0.55, rotate=-11)
                    + art.bat(438, 258, 48, color="#050409", flap=-0.45, rotate=9)
                    + art.bat(394, 348, 36, color="#050409", flap=0.15, rotate=-4)
                    + art.bat_swarm(6, 60, 430, 620, 130, seed=15,
                                    color="#120F1E", size=26)
                    + art.spider_web(38, 38, 168, spokes=8, rings=5,
                                     color=BONE_SOFT, stroke_width=1,
                                     start=0, end=90)
                    + _grain() + _frame()
                    + art.tapered_rule(W / 2, 664, 150, color=ORANGE, thickness=1.6))
    t = [
        text("YOU ARE SUMMONED TO A", left=105, top=442, width=540, size=10.5,
             family="Poppins", weight=400, color=BONE_SOFT, tracking=0.4),
        text("HALLOWEEN", left=55, top=474, width=640, size=76,
             family="Creepster", weight=400, color=ORANGE, line=1.05,
             tracking=0.02),
        text("PARTY", left=55, top=558, width=640, size=76, family="Creepster",
             weight=400, color=TOXIC, line=1.05, tracking=0.02),
        text("Friday, the Thirty-First of October", left=75, top=692,
             width=600, size=25, family="Cinzel Decorative", weight=400,
             color=BONE, line=1.3),
        text("FROM EIGHT UNTIL THE WITCHING HOUR", left=75, top=744,
             width=600, size=10, family="Poppins", weight=400, color=BONE_SOFT,
             tracking=0.28),
        text("THE CELLAR &nbsp;·&nbsp; RABENGASSE 13, DRESDEN", left=75,
             top=790, width=600, size=10, family="Poppins", weight=400,
             color=BONE_SOFT, tracking=0.24),
        text("COSTUMES ESSENTIAL", left=75, top=848, width=600, size=11,
             family="Poppins", weight=600, color=ORANGE, tracking=0.34),
        text("RSVP BY 24 OCTOBER &nbsp;·&nbsp; 0170 000 0000", left=75,
             top=898, width=600, size=9.5, family="Poppins", weight=400,
             color=BONE_SOFT, tracking=0.24),
    ]
    return page("\n".join([svg] + t), "Invitation", bg=NIGHT)


# ------------------------------------------------------------------- Seite 2

def _detail_row(top, label, title, note):
    return "\n".join([
        text(label, left=104, top=top, width=542, size=9.5, family="Poppins",
             weight=500, color=ORANGE, tracking=0.38, align="left"),
        text(title, left=104, top=top + 22, width=542, size=27,
             family="Cinzel Decorative", weight=400, color=BONE, align="left",
             line=1.2),
        text(note, left=104, top=top + 62, width=542, size=11,
             family="Poppins", weight=300, color=BONE_SOFT, align="left",
             line=1.6),
    ])


def p_details():
    rows = [(354, "THE RULES", "Come As You Fear",
             "Best costume takes the crown &mdash; and the last bottle."),
            (496, "THE POTIONS", "Blood Punch &amp; Bone Dry Gin",
             "Something warm in the cauldron for the brave."),
            (638, "THE SUMMONING", "Midnight Séance",
             "Bring a story. The lights go out at twelve.")]
    lines = "".join(
        f'<line x1="104" y1="{y}" x2="646" y2="{y}" stroke="{ORANGE}" '
        f'stroke-width="0.7" opacity="0.34"/>' for y in (472, 614))
    svg = svg_layer(_defs(),
                    _sky()
                    + art.bat_swarm(5, 96, 88, 560, 92, seed=21,
                                    color="#120F1E", size=30)
                    + art.spider_web(712, 38, 150, spokes=7, rings=4,
                                     color=BONE_SOFT, stroke_width=0.95,
                                     start=90, end=180)
                    + lines + _grain() + _frame()
                    + art.tapered_rule(W / 2, 790, 130, color=TOXIC, thickness=1.4))
    t = [
        text("WHAT AWAITS YOU", left=75, top=204, width=600, size=10.5,
             family="Poppins", weight=400, color=BONE_SOFT, tracking=0.42),
        text("THE NIGHT", left=75, top=234, width=600, size=64,
             family="Creepster", weight=400, color=TOXIC, tracking=0.04,
             line=1.1),
    ] + [_detail_row(*r) for r in rows] + [
        text("Getting out alive", left=104, top=820, width=542, size=25,
             family="Cinzel Decorative", weight=400, color=BONE, align="left"),
        text("Tram 7 runs until one. After that, you are on your own.",
             left=104, top=864, width=542, size=11.5, family="Poppins",
             weight=300, color=BONE_SOFT, align="left", line=1.7),
    ]
    return page("\n".join([svg] + t), "The Night", bg=NIGHT)


# ------------------------------------------------------------------- Seite 3

def p_thanks():
    svg = svg_layer(_defs(),
                    _sky() + _moon(375, 292, 106)
                    + _dead_branch(-30, 84, 268, 300, 110, 76, 152, 272,
                                   width=4.8, twigs=6, seed=13, color="#050409")
                    + _dead_branch(782, 120, 504, 322, 660, 100, 588, 292,
                                   width=3.8, twigs=5, seed=27, color="#050409")
                    + art.bat(344, 330, 54, color="#050409", flap=0.5, rotate=-9)
                    + art.bat(428, 288, 42, color="#050409", flap=-0.5, rotate=8)
                    + art.bat_swarm(6, 60, 452, 620, 140, seed=52,
                                    color="#120F1E", size=26)
                    + _grain() + _frame()
                    + art.tapered_rule(W / 2, 648, 150, color=ORANGE, thickness=1.5))
    t = [
        text("THANK YOU", left=55, top=470, width=640, size=80,
             family="Creepster", weight=400, color=ORANGE, line=1.05,
             tracking=0.02),
        text("FOR HAUNTING WITH US", left=75, top=572, width=600, size=10.5,
             family="Poppins", weight=400, color=BONE_SOFT, tracking=0.36),
        text("The costumes were terrifying,<br>the punch was worse.<br>"
             "Same time next year.",
             left=125, top=692, width=500, size=22,
             family="Cinzel Decorative", weight=400, color=BONE, line=1.7),
        text("UNTIL THE NEXT ALL HALLOWS&rsquo; EVE", left=75, top=884,
             width=600, size=10, family="Poppins", weight=500, color=TOXIC,
             tracking=0.34),
    ]
    return page("\n".join([svg] + t), "Thank You", bg=NIGHT)


def build():
    return document("MIDNIGHT — Halloween Suite", FAMILIES,
                    [p_invitation(), p_details(), p_thanks()],
                    body_bg="#1A1A18")


if __name__ == "__main__":
    import pathlib
    out = pathlib.Path(__file__).resolve().parent.parent / "dist" / "06-halloween-midnight.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build(), encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size // 1024} KB)")
