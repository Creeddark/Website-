"""
AMBRA — Hochzeits-Suite.
Stil: flach, editorial, Goldfolien-Optik. Elfenbein, Sand, Taupe, Gold.
Vier Seiten: Einladung, Ablauf, RSVP, Danksagung.
"""

import math
import art
from common import W, H, page, text, svg_layer, document

IVORY = "#FBF8F3"
SAND = "#EFE6D8"
INK = "#2A2621"
INK_SOFT = "#6B655C"
GOLD = "#B08D57"
GREEN = "#9BA88C"

FAMILIES = {"Playfair Display", "Montserrat", "Great Vibes", "Cormorant Garamond"}

# Kein Verlauf auf Text: Canva liest beim HTML-Import die effektive Textfarbe.
# background-clip:text mit transparenter Fuellung kommt dort als Schwarz an.
# Deshalb bekommt Foliengold eine echte Farbe — die metallische Wirkung traegt
# die Grafikebene, die als Bild eingebettet wird.
GOLD_FOIL = "#A8823F"


def _defs():
    return (art.paper_grain("grain", opacity=0.05, freq=0.9)
            + art.gold_gradient("gold")
            + art.soft_shadow("sh", dy=3, blur=7, opacity=0.10))


def _frame(inset=38, inner=9):
    """Doppelter Haarlinien-Rahmen — aussen fein, innen noch feiner."""
    return (f'<rect x="{inset}" y="{inset}" width="{W - inset * 2}" '
            f'height="{H - inset * 2}" fill="none" stroke="{GOLD}" '
            f'stroke-width="1.1" opacity="0.85"/>'
            f'<rect x="{inset + inner}" y="{inset + inner}" '
            f'width="{W - (inset + inner) * 2}" height="{H - (inset + inner) * 2}" '
            f'fill="none" stroke="{GOLD}" stroke-width="0.55" opacity="0.5"/>')


def _grain():
    return (f'<rect width="{W}" height="{H}" fill="#8A7A62" '
            f'filter="url(#grain)" opacity="0.9"/>')


GREEN_TINT = "#E7EBE1"
GOLD_TINT = "#F6EFE0"


def _arch_botanicals():
    """Hoher Eukalyptus-Bogen, der die Namen einfasst.

    Die Zweige wachsen von unten nach oben und treffen sich ueber der Mitte.
    Grosse Blaetter am Fuss, feine an der Spitze — dadurch rahmt der Bogen den
    Text, statt ein leeres Rund in die Seite zu stanzen.
    Drei Tiefenebenen: blasser Hintergrund, goldener Akzent, kraeftige Front.
    """
    CX, CY, RX, RY = 375, 486, 214, 318
    A0, A1 = 148, 392
    spine = (f'<path d="M{CX + math.cos(math.radians(A0)) * RX:.1f},'
             f'{CY + math.sin(math.radians(A0)) * RY:.1f} '
             f'A{RX},{RY} 0 1 1 '
             f'{CX + math.cos(math.radians(A1)) * RX:.1f},'
             f'{CY + math.sin(math.radians(A1)) * RY:.1f}" '
             f'fill="none" stroke="{GREEN}" stroke-width="1.2" opacity="0.5"/>')
    back = art.foliage_arc(CX, CY, RX + 16, RY + 16, A0 + 4, A1 - 4, sprigs=30,
                           stroke=GREEN, fill=GREEN_TINT, stroke_width=1.15,
                           length=40, leaf_r=12.5, seed=41, outward=1,
                           density_ends=0.5, spread=22, aspect=1.5)
    gold = art.foliage_arc(CX, CY, RX - 6, RY - 6, A0 + 10, A1 - 10, sprigs=16,
                           stroke=GOLD, fill=GOLD_TINT, stroke_width=1.0,
                           length=34, leaf_r=8, seed=8, outward=1,
                           density_ends=0.5, spread=34, aspect=2.2)
    front = art.foliage_arc(CX, CY, RX, RY, A0, A1, sprigs=36,
                            stroke=GREEN, fill=GREEN_TINT, stroke_width=1.45,
                            length=46, leaf_r=16, seed=21, outward=1,
                            density_ends=0.46, spread=18, aspect=1.3)
    inner = art.foliage_arc(CX, CY, RX, RY, A0 + 16, A1 - 16, sprigs=14,
                            stroke=GREEN, fill=GREEN_TINT, stroke_width=1.2,
                            length=26, leaf_r=10, seed=77, outward=-1,
                            density_ends=0.55, spread=18, aspect=1.35)
    return (f'<g opacity="0.4">{back}</g>{spine}'
            f'<g opacity="0.6">{gold}</g>'
            f'<g opacity="0.45">{inner}</g>'
            f'<g opacity="0.96">{front}</g>')


def _spray(cx, cy, *, scale=1.0, opacity=0.9, gold=False, seed=5):
    """Waagerechte Blattgarnitur — das Schlusszeichen unter Ueberschriften.

    Zwei gespiegelte Faecher aus kurzen Zweigen. Die aeusseren sind laenger und
    flacher, die inneren kuerzer und steiler; dadurch entsteht die typische
    Tropfenform einer gebundenen Garnitur.
    """
    col = GOLD if gold else GREEN
    tint = GOLD_TINT if gold else GREEN_TINT
    parts = []
    plan = [(0, 1.00, 4), (16, 0.72, 3), (-15, 0.58, 3)]
    for side in (1, -1):
        for i, (tilt, ln, lv) in enumerate(plan):
            ang = (0 if side > 0 else 180) + tilt * side
            parts.append(art.sprig(
                cx + 5 * side, cy, ang, leaves=lv,
                length=74 * ln * scale, leaf_r=11.5 * ln * scale,
                curve=16 * scale, stroke=col, fill=tint,
                stroke_width=1.25, seed=seed + i * 7 + (0 if side > 0 else 3),
                aspect=1.36))
    return f'<g opacity="{opacity}">{"".join(parts)}</g>'


# ------------------------------------------------------------------- Seite 1

def p_invitation():
    svg = svg_layer(_defs(),
                    _grain() + _frame() + _arch_botanicals()
                    + art.tapered_rule(W / 2, 786, 140, color=GOLD, thickness=1.5))
    t = [
        text("TOGETHER WITH THEIR FAMILIES", left=195, top=332, width=360,
             size=10.5, family="Montserrat", weight=400, color=INK_SOFT,
             tracking=0.3),
        text("Amelia", left=155, top=364, width=440, size=68,
             family="Playfair Display", weight=400, color=INK, line=1.04,
             tracking=0.005),
        text("&amp;", left=155, top=442, width=440, size=48,
             family="Great Vibes", weight=400, color=GOLD_FOIL, line=1.0),
        text("Julian", left=155, top=492, width=440, size=68,
             family="Playfair Display", weight=400, color=INK, line=1.04,
             tracking=0.005),
        text("REQUEST THE PLEASURE OF YOUR COMPANY", left=75, top=812,
             width=600, size=10.5, family="Montserrat", weight=400,
             color=INK_SOFT, tracking=0.26),
        text("Saturday, the Twelfth of June", left=75, top=842, width=600,
             size=28, family="Cormorant Garamond", weight=400, color=INK,
             line=1.2),
        text("TWO THOUSAND TWENTY-SEVEN &nbsp;·&nbsp; HALF PAST THREE",
             left=75, top=886, width=600, size=10, family="Montserrat",
             weight=400, color=INK_SOFT, tracking=0.22),
        text("VILLA ASTORIA", left=75, top=920, width=600, size=15,
             family="Montserrat", weight=500, color=INK, tracking=0.3),
        text("Lake Como &nbsp;·&nbsp; Italy &nbsp;—&nbsp; dinner and dancing to follow",
             left=75, top=948, width=600, size=17,
             family="Cormorant Garamond", weight=300, color=INK_SOFT,
             style="italic"),
    ]
    return page("\n".join([svg] + t), "Invitation", bg=IVORY)


# ------------------------------------------------------------------- Seite 2

def _schedule_row(top, time, title, note):
    return "\n".join([
        text(time, left=112, top=top + 6, width=104, size=12.5,
             family="Montserrat", weight=500, color=GOLD, tracking=0.18,
             align="right"),
        text(title, left=262, top=top, width=380, size=25,
             family="Cormorant Garamond", weight=400, color=INK, align="left",
             line=1.15),
        text(note, left=262, top=top + 32, width=380, size=10,
             family="Montserrat", weight=400, color=INK_SOFT, tracking=0.18,
             align="left"),
    ])


def p_schedule():
    rows = [(348, "15:30", "Ceremony", "GARDEN TERRACE"),
            (452, "16:30", "Aperitivo", "LEMON COURTYARD"),
            (556, "18:30", "Dinner", "THE ORANGERY"),
            (660, "21:00", "First Dance", "BALLROOM"),
            (764, "22:00", "Dancing", "UNTIL THE LAST SONG")]
    lines = "".join(
        f'<line x1="112" y1="{y}" x2="638" y2="{y}" stroke="{GOLD}" '
        f'stroke-width="0.6" opacity="0.4"/>' for y in (432, 536, 640, 744))
    svg = svg_layer(_defs(),
                    _grain() + _frame()
                    + _spray(W / 2, 282, scale=0.82, opacity=0.88)
                    + lines
                    + _spray(W / 2, 916, scale=0.62, opacity=0.7, gold=True, seed=31))
    t = [
        text("THE DAY", left=75, top=168, width=600, size=11,
             family="Montserrat", weight=400, color=INK_SOFT, tracking=0.38),
        text("Order of Events", left=75, top=198, width=600, size=54,
             family="Playfair Display", weight=400, color=INK, line=1.1),
    ] + [_schedule_row(*r) for r in rows] + [
        text("We would love to see you in soft neutrals", left=115, top=852,
             width=520, size=21, family="Cormorant Garamond",
             weight=300, color=INK_SOFT, style="italic"),
    ]
    return page("\n".join([svg] + t), "Order of Events", bg=IVORY)


# ------------------------------------------------------------------- Seite 3

def p_rsvp():
    field_y = (392, 484, 576)
    fields = "".join(
        f'<line x1="142" y1="{y}" x2="608" y2="{y}" stroke="{GOLD}" '
        f'stroke-width="0.9" opacity="0.5"/>' for y in field_y)
    boxes = "".join(
        f'<rect x="{x}" y="654" width="18" height="18" rx="1" fill="none" '
        f'stroke="{GOLD}" stroke-width="1.1"/>' for x in (176, 404))
    svg = svg_layer(_defs(),
                    _grain() + _frame()
                    + _spray(W / 2, 286, scale=0.78, opacity=0.88)
                    + fields + boxes
                    + art.tapered_rule(W / 2, 744, 130, color=GOLD, thickness=1.3)
                    + _spray(W / 2, 906, scale=0.6, opacity=0.68, gold=True, seed=44))
    t = [
        text("PLEASE REPLY", left=75, top=170, width=600, size=11,
             family="Montserrat", weight=400, color=INK_SOFT, tracking=0.38),
        text("R.S.V.P.", left=75, top=200, width=600, size=58,
             family="Playfair Display", weight=400, color=INK, tracking=0.05),
        text("NAME", left=142, top=362, width=466, size=9,
             family="Montserrat", weight=500, color=GOLD, tracking=0.32,
             align="left"),
        text("NUMBER ATTENDING", left=142, top=454, width=466, size=9,
             family="Montserrat", weight=500, color=GOLD, tracking=0.32,
             align="left"),
        text("DIETARY REQUIREMENTS", left=142, top=546, width=466, size=9,
             family="Montserrat", weight=500, color=GOLD, tracking=0.32,
             align="left"),
        text("Joyfully accepts", left=206, top=650, width=180, size=21,
             family="Cormorant Garamond", weight=400, color=INK, align="left"),
        text("Regretfully declines", left=434, top=650, width=200, size=21,
             family="Cormorant Garamond", weight=400, color=INK, align="left"),
        text("KINDLY REPLY BY THE FIRST OF MAY", left=75, top=776, width=600,
             size=10, family="Montserrat", weight=400, color=INK_SOFT,
             tracking=0.28),
        text("amelia-and-julian.com", left=75, top=808, width=600, size=19,
             family="Cormorant Garamond", weight=400, color=INK,
             style="italic"),
    ]
    return page("\n".join([svg] + t), "RSVP", bg=IVORY)


# ------------------------------------------------------------------- Seite 4

def p_thanks():
    svg = svg_layer(_defs(),
                    f'<rect width="{W}" height="{H}" fill="{SAND}"/>'
                    + _grain() + _frame()
                    + art.wreath(W / 2, 402, 206, ry=186, stroke=GREEN,
                                 fill=GREEN_TINT, stroke_width=1.35, seed=9,
                                 leaf_r=14, sprigs=21, length=42, gap_deg=44)
                    + art.wreath(W / 2, 402, 179, ry=161, stroke=GOLD,
                                 fill=GOLD_TINT, stroke_width=1.0, seed=23,
                                 leaf_r=7.5, sprigs=14, length=28, gap_deg=64,
                                 aspect=2.2)
                    + art.tapered_rule(W / 2, 668, 128, color=GOLD, thickness=1.3))
    t = [
        text("Thank you", left=175, top=344, width=400, size=60,
             family="Great Vibes", weight=400, color=GOLD_FOIL, line=1.1),
        text("FOR CELEBRATING WITH US", left=175, top=444, width=400, size=10.5,
             family="Montserrat", weight=400, color=INK_SOFT, tracking=0.3),
        text("Your presence made our day complete.<br>We are so grateful for "
             "your kindness,<br>your laughter and your love.",
             left=145, top=716, width=460, size=22,
             family="Cormorant Garamond", weight=300, color=INK, line=1.75,
             style="italic"),
        text("AMELIA &amp; JULIAN", left=75, top=880, width=600, size=11.5,
             family="Montserrat", weight=500, color=INK, tracking=0.34),
    ]
    return page("\n".join([svg] + t), "Thank You", bg=SAND)


def build():
    return document("AMBRA — Wedding Suite", FAMILIES,
                    [p_invitation(), p_schedule(), p_rsvp(), p_thanks()])


if __name__ == "__main__":
    import pathlib
    out = pathlib.Path(__file__).resolve().parent.parent / "dist" / "01-wedding-ambra.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build(), encoding="utf-8")
    print(f"wrote {out} ({out.stat().st_size // 1024} KB)")
