"""
Anleitungsblatt — die Datei, die der Kaeufer bei Etsy herunterlaedt.

Etsy liefert Dateien, keine Links. Der Vorlagen-Link muss also in einem
Dokument stehen, das der Shop ausliefert. Genau das ist dieses Blatt.

Es ist selbst ein Canva-Design und kein fertiges PDF, weil der Link pro
Angebot ein anderer ist: Blatt in Canva duplizieren, Link und Namen
eintragen, als PDF herunterladen, bei Etsy hochladen.

Format A4, damit es sich ohne Zuschnitt drucken und lesen laesst.
"""

import art
import ornament as orn
from common import page, text, svg_layer, document

AW, AH = 794, 1123          # A4 bei 96 px je Zoll

IVORY = "#FBF8F3"
SURFACE = "#F4EEE5"
INK = "#1C1A17"
INK_2 = "#3A3630"
INK_3 = "#6B655C"
LINE = "#E2DCD2"
GOLD = "#A8823F"
GOLD_SOFT = "#C6A96B"

FAMILIES = {"Playfair Display", "Montserrat", "Cormorant Garamond",
            "Great Vibes"}


def _defs():
    return art.paper_grain("grain", opacity=0.045, freq=0.9)


def _ground():
    return (f'<rect width="{AW}" height="{AH}" fill="{IVORY}"/>'
            f'<rect width="{AW}" height="{AH}" fill="#8A7A62" '
            f'filter="url(#grain)" opacity="0.85"/>')


def _rule(y, x0=64, x1=AW - 64, w=0.8, color=LINE):
    return (f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{color}" '
            f'stroke-width="{w}"/>')


def _link_box(y=336, h=132):
    """Der Link ist das Herz des Blatts und bekommt darum einen eigenen Rahmen."""
    return (f'<rect x="64" y="{y}" width="{AW - 128}" height="{h}" '
            f'fill="{SURFACE}" stroke="{GOLD}" stroke-width="1.4"/>'
            f'<rect x="72" y="{y + 8}" width="{AW - 144}" height="{h - 16}" '
            f'fill="none" stroke="{GOLD}" stroke-width="0.5" opacity="0.5"/>')


def _step_marks(tops):
    return "".join(
        f'<circle cx="84" cy="{t + 8}" r="14" fill="none" stroke="{GOLD}" '
        f'stroke-width="1"/>' for t in tops)


def _spray(cx, cy, scale=1.0, opacity=0.8):
    parts = []
    for side in (1, -1):
        for i, (tilt, ln, lv) in enumerate([(0, 1.0, 4), (16, 0.7, 3)]):
            parts.append(orn.__dict__ and art.sprig(
                cx + 4 * side, cy, (0 if side > 0 else 180) + tilt * side,
                leaves=lv, length=62 * ln * scale, leaf_r=9.5 * ln * scale,
                curve=13 * scale, stroke=GOLD_SOFT, fill="#F6EFE0",
                stroke_width=1.1, seed=5 + i * 4 + (0 if side > 0 else 3),
                aspect=1.36))
    return f'<g opacity="{opacity}">{"".join(parts)}</g>'


STEPS = [
    ("Open the link above",
     "It works on a phone, a tablet or a computer. You will need a free Canva "
     "account &mdash; signing up takes a minute and costs nothing."),
    ("Choose &ldquo;Use template&rdquo;",
     "Canva makes a private copy just for you. The original stays untouched, so "
     "nothing you do here can go wrong."),
    ("Replace the text with your own",
     "Click any text to edit it. Colours, fonts and sizes can all be changed. "
     "Photo areas are swapped by clicking the image and choosing your own."),
    ("Download and print",
     "Share &rarr; Download &rarr; PDF Print. Choose <b>crop marks and bleed</b> "
     "if your printer asks for them."),
]


def p_sheet():
    step_tops = (596, 692, 788, 884)
    svg = svg_layer(_defs(),
                    _ground()
                    + _rule(112, w=1.6, color=GOLD)
                    + _rule(118, w=0.5, color=GOLD)
                    + _link_box(336, 132)
                    + _rule(548)
                    + _step_marks(step_tops)
                    + _rule(986)
                    + _spray(AW / 2, 1058, scale=0.7, opacity=0.7),
                    w=AW, h=AH)
    tt = [
        text("YOUR SHOP NAME", left=64, top=76, width=AW - 128, size=11,
             family="Montserrat", weight=500, color=INK_3, tracking=0.42,
             align="left"),
        text("Thank you for your order", left=64, top=152, width=AW - 128,
             size=54, family="Playfair Display", weight=400, color=INK,
             line=1.1, align="left"),
        text("NAME OF THE TEMPLATE SUITE", left=64, top=232, width=AW - 128,
             size=11, family="Montserrat", weight=500, color=GOLD,
             tracking=0.36, align="left"),
        text("Everything you need is behind the link below. Nothing to install, "
             "nothing to unzip.", left=64, top=262, width=AW - 220, size=17,
             family="Cormorant Garamond", weight=400, color=INK_2, line=1.5,
             align="left", style="italic"),

        text("YOUR TEMPLATE LINK", left=96, top=362, width=AW - 192, size=10,
             family="Montserrat", weight=500, color=INK_3, tracking=0.34,
             align="left"),
        text("paste-your-canva-template-link-here", left=96, top=392,
             width=AW - 192, size=17, family="Montserrat", weight=500,
             color=GOLD, tracking=0.01, align="left", line=1.5),
        text("Tap the link, or copy it into your browser.", left=96, top=428,
             width=AW - 192, size=13, family="Cormorant Garamond", weight=400,
             color=INK_3, style="italic", align="left"),

        text("HOW IT WORKS", left=64, top=506, width=AW - 128, size=10,
             family="Montserrat", weight=500, color=INK_3, tracking=0.42,
             align="left"),
    ]
    for i, (title, body) in enumerate(STEPS):
        top = step_tops[i]
        tt += [
            text(f"{i + 1}", left=64, top=top, width=40, size=15,
                 family="Playfair Display", weight=400, color=GOLD, line=1.2),
            text(title, left=124, top=top - 4, width=AW - 190, size=21,
                 family="Playfair Display", weight=400, color=INK, align="left",
                 line=1.25),
            text(body, left=124, top=top + 26, width=AW - 200, size=13,
                 family="Montserrat", weight=400, color=INK_3, align="left",
                 line=1.6),
        ]
    tt += [
        text("Personal use only. Please do not resell, share or redistribute "
             "this template or the link. &nbsp;·&nbsp; Questions? Message me "
             "through the shop &mdash; I answer every one.",
             left=64, top=1012, width=AW - 128, size=11,
             family="Montserrat", weight=400, color=INK_3, align="left",
             line=1.7),
    ]
    return page("\n".join([svg] + tt), "Delivery Sheet", bg=IVORY,
                w=AW, h=AH)


def p_printing():
    """Zweites Blatt: Druckhinweise. Beantwortet die haeufigsten Rueckfragen,
    bevor sie als Nachricht im Shop landen."""
    rows = [
        ("SIZE", "5 &times; 7 inches",
         "The standard invitation size. Envelopes labelled A7 fit it exactly."),
        ("RESOLUTION", "300 DPI",
         "Print quality. Do not scale the file up &mdash; it is already at the "
         "right resolution."),
        ("PAPER", "250&ndash;300 g/m&sup2; card",
         "Matte or lightly textured card looks closest to letterpress. Glossy "
         "photo paper does not suit these designs."),
        ("AT HOME", "Print &ldquo;actual size&rdquo;",
         "Turn off &ldquo;fit to page&rdquo; &mdash; it shrinks the design and "
         "leaves a white margin."),
        ("AT A PRINT SHOP", "Send the PDF",
         "Ask for 5 &times; 7 inches on card, trimmed. Most shops will ask for "
         "bleed; Canva adds it in the download dialog."),
        ("DIGITAL ONLY", "Download as PNG",
         "For sending by message or e-mail. Choose PNG rather than PDF for "
         "phones."),
    ]
    tops = [260 + i * 122 for i in range(len(rows))]
    svg = svg_layer(_defs(),
                    _ground()
                    + _rule(112, w=1.6, color=GOLD) + _rule(118, w=0.5, color=GOLD)
                    + "".join(_rule(t + 100) for t in tops[:-1])
                    + _rule(1010)
                    + _spray(AW / 2, 1070, scale=0.62, opacity=0.65),
                    w=AW, h=AH)
    tt = [
        text("YOUR SHOP NAME", left=64, top=76, width=AW - 128, size=11,
             family="Montserrat", weight=500, color=INK_3, tracking=0.42,
             align="left"),
        text("Printing your cards", left=64, top=152, width=AW - 128, size=48,
             family="Playfair Display", weight=400, color=INK, line=1.1,
             align="left"),
        text("A few notes that make the difference between a card that looks "
             "printed and one that looks made.",
             left=64, top=214, width=AW - 220, size=16,
             family="Cormorant Garamond", weight=400, color=INK_2,
             style="italic", align="left", line=1.5),
    ]
    for i, (label, value, note) in enumerate(rows):
        top = tops[i]
        tt += [
            text(label, left=64, top=top, width=190, size=9.5,
                 family="Montserrat", weight=500, color=GOLD, tracking=0.34,
                 align="left"),
            text(value, left=272, top=top - 8, width=AW - 340, size=24,
                 family="Playfair Display", weight=400, color=INK, align="left",
                 line=1.2),
            text(note, left=272, top=top + 26, width=AW - 340, size=12.5,
                 family="Montserrat", weight=400, color=INK_3, align="left",
                 line=1.6),
        ]
    tt.append(
        text("Thank you for choosing a small shop. It genuinely matters.",
             left=64, top=1036, width=AW - 128, size=18,
             family="Great Vibes", weight=400, color=GOLD, align="left"))
    return page("\n".join([svg] + tt), "Printing Notes", bg=IVORY,
                w=AW, h=AH)


def build():
    return document("DELIVERY — Template Link & Printing Sheet", FAMILIES,
                    [p_sheet(), p_printing()], body_bg="#5A5750")


if __name__ == "__main__":
    import pathlib
    out = (pathlib.Path(__file__).resolve().parent.parent / "dist"
           / "11-delivery-sheet.html")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(build(), encoding="utf-8")
    print(f"wrote {out.name} ({out.stat().st_size // 1024} KB)")
