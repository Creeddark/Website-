"""
COVER — Magazin-Suiten.

Das Foto traegt die Seite, die Typografie macht daraus ein Cover. Was ein
echtes Titelblatt ausmacht und Vorlagen oft weglassen: der Titelkopf laeuft
hinter die Person, Coverzeilen stehen links und rechts in unterschiedlichen
Groessen, unten sitzen Strichcode und Ausgabenzeile.

Das Bild ist ein eigenes Feld. Der Kaeufer ersetzt es in Canva durch ein
eigenes Portrait — ohne dieses Foto bleibt die Vorlage ein Geruest, deshalb
ist es der eine Punkt, an dem diese Suite auf Zuarbeit angewiesen ist.
"""

import art
from common import W, H, page, text, svg_layer, document, image

FAMILIES = {"Bodoni Moda", "Abril Fatface", "Montserrat", "Pinyon Script",
            "EB Garamond", "Oswald"}


def _defs(t):
    return (art.scrim("top", stops=((0, 0.62), (0.30, 0.20), (1, 0.06)), angle=90)
            + art.scrim("bottom", stops=((0, 0.0), (0.42, 0.14), (1, 0.86)),
                        angle=90)
            + art.paper_grain("grain", opacity=0.05, freq=0.9)
            + art.linear_bg("edge", [(0, t["ink"], 0.35), (0.3, t["ink"], 0),
                                     (0.7, t["ink"], 0), (1, t["ink"], 0.35)],
                            angle=0))


def _overlay(t):
    return (f'<rect width="{W}" height="{H}" fill="url(#top)"/>'
            f'<rect width="{W}" height="{H}" fill="url(#bottom)"/>'
            f'<rect width="{W}" height="{H}" fill="url(#edge)"/>'
            f'<rect width="{W}" height="{H}" fill="{t["light"]}" '
            f'filter="url(#grain)" opacity="0.5"/>')


# ------------------------------------------------------------------- Seite 1

def p_cover(t, c):
    svg = svg_layer(_defs(t),
                    _overlay(t)
                    + f'<line x1="52" y1="196" x2="{W - 52}" y2="196" '
                      f'stroke="{t["light"]}" stroke-width="0.8" opacity="0.5"/>'
                    + art.barcode(52, 946, 108, 40, seed=11, color=t["light"],
                                  digits=c["barcode"])
                    + f'<line x1="{W - 232}" y1="946" x2="{W - 52}" y2="946" '
                      f'stroke="{t["light"]}" stroke-width="0.8" opacity="0.5"/>')
    img = image("photo-tall.png", left=0, top=0, width=W, height=H,
                alt="Portrait des Gastgebers")
    tt = [
        text(c["strapline"], left=52, top=64, width=W - 104, size=10,
             family="Montserrat", weight=500, color=t["light"], tracking=0.42),
        text(c["masthead"], left=30, top=88, width=W - 60, size=96,
             family="Bodoni Moda", weight=700, color=t["light"], line=0.98,
             tracking=0.01),
        text(c["masthead_sub"], left=52, top=206, width=250, size=19,
             family="EB Garamond", weight=400, color=t["light"], style="italic",
             align="left"),
        text(c["edition"], left=W - 302, top=210, width=250, size=10,
             family="Montserrat", weight=500, color=t["light"], tracking=0.32,
             align="right"),
        text(c["kicker"], left=52, top=520, width=300, size=30,
             family="Pinyon Script", weight=400, color=t["accent"], align="left",
             line=1.1),
        text(c["star"], left=52, top=566, width=340, size=34,
             family="Bodoni Moda", weight=700, color=t["light"], align="left",
             line=1.06, tracking=0.02),
        text(c["date_big"], left=W - 302, top=560, width=250, size=44,
             family="Bodoni Moda", weight=400, color=t["light"], align="right",
             line=1.02),
        text(c["headline"], left=52, top=680, width=250, size=22,
             family="Oswald", weight=500, color=t["light"], align="left",
             line=1.2, tracking=0.02),
        text(c["blurb"], left=336, top=676, width=362, size=12,
             family="EB Garamond", weight=400, color=t["light"], align="left",
             line=1.68),
        text(c["footline"], left=52, top=884, width=W - 104, size=11,
             family="EB Garamond", weight=400, color=t["light"], style="italic",
             align="left"),
        text(c["issue"], left=W - 232, top=956, width=180, size=9.5,
             family="Montserrat", weight=400, color=t["light"], tracking=0.26,
             align="right"),
    ]
    return page("\n".join([img, svg] + tt), "Cover", bg=t["ink"])


# ------------------------------------------------------------------- Seite 2

def p_feature(t, c):
    """Innenseite: Spalte mit Initiale, zwei Bilder, Ausklang."""
    svg = svg_layer(_defs(t),
                    f'<rect width="{W}" height="{H}" fill="{t["paper"]}"/>'
                    + f'<rect width="{W}" height="{H}" fill="{t["ink"]}" '
                      f'filter="url(#grain)" opacity="0.35"/>'
                    + f'<line x1="52" y1="150" x2="{W - 52}" y2="150" '
                      f'stroke="{t["ink"]}" stroke-width="1.4"/>'
                    + f'<line x1="52" y1="856" x2="{W - 52}" y2="856" '
                      f'stroke="{t["ink"]}" stroke-width="0.7" opacity="0.4"/>'
                    + f'<rect x="410" y="196" width="288" height="360" '
                      f'fill="none" stroke="{t["ink"]}" stroke-width="1"/>')
    img = image("photo-portrait.png", left=410, top=196, width=288, height=360,
                alt="Foto aus der Reportage")
    tt = [
        text(c["feature_kicker"], left=52, top=112, width=W - 104, size=10,
             family="Montserrat", weight=500, color=t["ink_soft"], tracking=0.42,
             align="left"),
        text(c["feature_title"], left=52, top=186, width=326, size=44,
             family="Bodoni Moda", weight=700, color=t["ink"], align="left",
             line=1.02),
        text(c["feature_deck"], left=52, top=396, width=326, size=15,
             family="EB Garamond", weight=400, color=t["ink_soft"],
             style="italic", align="left", line=1.55),
        text(c["feature_body"], left=52, top=502, width=326, size=12.5,
             family="EB Garamond", weight=400, color=t["ink"], align="left",
             line=1.72),
        text(c["feature_caption"], left=410, top=566, width=288, size=10,
             family="EB Garamond", weight=400, color=t["ink_soft"],
             style="italic", align="left"),
        text(c["feature_pull"], left=410, top=624, width=288, size=25,
             family="Bodoni Moda", weight=400, color=t["accent_dark"],
             align="left", line=1.25),
        text(c["feature_foot"], left=52, top=884, width=W - 104, size=13,
             family="Oswald", weight=400, color=t["ink"], tracking=0.28,
             align="left"),
        text(c["feature_foot_2"], left=52, top=914, width=W - 104, size=10.5,
             family="Montserrat", weight=400, color=t["ink_soft"], tracking=0.22,
             align="left"),
    ]
    return page("\n".join([svg, img] + tt), "Feature", bg=t["paper"])


# ------------------------------------------------------------------- Seite 3

def p_details(t, c):
    rows = c["details"]
    lines = "".join(
        f'<line x1="52" y1="{y}" x2="{W - 52}" y2="{y}" stroke="{t["ink"]}" '
        f'stroke-width="0.7" opacity="0.35"/>' for y in (452, 572, 692))
    svg = svg_layer(_defs(t),
                    f'<rect width="{W}" height="{H}" fill="{t["paper2"]}"/>'
                    + f'<rect width="{W}" height="{H}" fill="{t["ink"]}" '
                      f'filter="url(#grain)" opacity="0.3"/>'
                    + f'<line x1="52" y1="150" x2="{W - 52}" y2="150" '
                      f'stroke="{t["ink"]}" stroke-width="1.4"/>' + lines
                    + f'<rect x="52" y="798" width="{W - 104}" height="148" '
                      f'fill="none" stroke="{t["ink"]}" stroke-width="1.4"/>')
    tt = [
        text(c["details_kicker"], left=52, top=112, width=W - 104, size=10,
             family="Montserrat", weight=500, color=t["ink_soft"], tracking=0.42,
             align="left"),
        text(c["details_title"], left=52, top=186, width=W - 104, size=52,
             family="Bodoni Moda", weight=700, color=t["ink"], align="left",
             line=1.02),
    ]
    for i, (label, value, note) in enumerate(rows[:4]):
        top = 352 + i * 120
        tt += [
            text(label, left=52, top=top, width=180, size=9,
                 family="Montserrat", weight=600, color=t["accent_dark"],
                 tracking=0.34, align="left"),
            text(value, left=248, top=top - 6, width=450, size=30,
                 family="Bodoni Moda", weight=400, color=t["ink"], align="left",
                 line=1.15),
            text(note, left=248, top=top + 34, width=450, size=13,
                 family="EB Garamond", weight=400, color=t["ink_soft"],
                 style="italic", align="left", line=1.5),
        ]
    tt += [
        text(c["cta_script"], left=76, top=820, width=W - 152, size=32,
             family="Pinyon Script", weight=400, color=t["accent_dark"]),
        text(c["cta_line"], left=76, top=876, width=W - 152, size=11,
             family="Montserrat", weight=500, color=t["ink"], tracking=0.26),
        text(c["cta_line_2"], left=76, top=906, width=W - 152, size=10,
             family="Montserrat", weight=400, color=t["ink_soft"], tracking=0.22),
    ]
    return page("\n".join([svg] + tt), "The Details", bg=t["paper2"])


# ------------------------------------------------------------------- Seite 4

def p_back(t, c):
    svg = svg_layer(_defs(t),
                    _overlay(t)
                    + art.barcode(W - 160, 946, 108, 40, seed=23,
                                  color=t["light"], digits=c["barcode"]))
    img = image("photo-square.png", left=0, top=0, width=W, height=H,
                alt="Erinnerungsfoto")
    tt = [
        text(c["back_kicker"], left=52, top=560, width=W - 104, size=10,
             family="Montserrat", weight=500, color=t["light"], tracking=0.42,
             align="left"),
        text(c["back_title"], left=52, top=592, width=W - 104, size=62,
             family="Bodoni Moda", weight=700, color=t["light"], align="left",
             line=1.0),
        text(c["back_body"], left=52, top=750, width=440, size=14,
             family="EB Garamond", weight=400, color=t["light"], align="left",
             line=1.75),
        text(c["signature"], left=52, top=886, width=W - 104, size=11,
             family="Montserrat", weight=500, color=t["light"], tracking=0.34,
             align="left"),
    ]
    return page("\n".join([img, svg] + tt), "Back Cover", bg=t["ink"])


# -------------------------------------------------------------------- Inhalte

THEMES = {
    "noir": dict(ink="#12100F", ink_soft="#5B554E", light="#FBF7EF",
                 paper="#F5F0E6", paper2="#EDE7DB", accent="#E4C98E",
                 accent_dark="#9A7A3C"),
    "rose": dict(ink="#1A1214", ink_soft="#6B5A5C", light="#FDF6F3",
                 paper="#F8EFEC", paper2="#F2E5E1", accent="#E8B7B0",
                 accent_dark="#A76A63"),
}

SUITES = [
    dict(file="10-cover-birthday", theme="noir",
         title="COVER — Birthday Magazine Suite",
         strapline="ICONIC &nbsp;·&nbsp; MAJOR &nbsp;·&nbsp; FLAWLESS",
         masthead="BIRTHDAY", masthead_sub="magazine",
         edition="18TH EDITION", barcode="0 001824 000018",
         kicker="The best of&hellip;", star="DAISY<br>CAMPBELL",
         date_big="APRIL<br>2027",
         headline="ONE NIGHT<br>ONLY",
         blurb="A once-in-a-year issue dedicated entirely to a one-of-a-kind "
               "soul. More than a birthday — a tribute to her sparkle, her "
               "kindness, and the countless ways she has made life more "
               "colourful for everyone around her.",
         footline="From laughter to legacy, she turns every step into strength.",
         issue="NO. 18 &nbsp;·&nbsp; APRIL",
         feature_kicker="THE COVER STORY",
         feature_title="Eighteen<br>Never Looked<br>So Good",
         feature_deck="In which our cover star reveals her plans for the "
                      "evening, and none of them involve an early night.",
         feature_body="She has been planning this for months, which anyone who "
                      "knows her will find entirely in character.<br><br>"
                      "There will be music, there will be cake, and there will "
                      "be a playlist she has been curating since February."
                      "<br><br>"
                      "Come as you are, but come photographed-ready. The camera "
                      "will be out and it will not be kind to anyone who left "
                      "early.",
         feature_caption="Backstage, moments before the doors opened.",
         feature_pull="&ldquo;I want it to be nothing less than perfect.&rdquo;",
         feature_foot="SATURDAY, 24 APRIL &nbsp;·&nbsp; 8 PM",
         feature_foot_2="THE ROOFTOP &nbsp;·&nbsp; 12 CORNELIA STREET",
         details_kicker="THE PARTICULARS",
         details_title="Everything<br>You Need to Know",
         details=[("WHEN", "Saturday, 24 April",
                   "Doors at eight. The cake will not wait."),
                  ("WHERE", "The Rooftop",
                   "12 Cornelia Street. Take the lift to the top."),
                  ("DRESS", "Black &amp; Gold",
                   "Something you would happily be photographed in."),
                  ("R.S.V.P.", "Before 1 April",
                   "To Charlotte on 0170 000 0000.")],
         cta_script="Let&rsquo;s celebrate together",
         cta_line="SATURDAY, 24 APRIL &nbsp;·&nbsp; EIGHT IN THE EVENING",
         cta_line_2="THE ROOFTOP &nbsp;·&nbsp; 12 CORNELIA STREET",
         back_kicker="THE LAST WORD",
         back_title="Thank You<br>For Coming",
         back_body="For the dancing, the toasts and for staying until the very "
                   "last song. This issue is closed, and it was a good one.",
         signature="DAISY"),

    dict(file="10-cover-wedding", theme="rose",
         title="COVER — Wedding Magazine Suite",
         strapline="LOVE &nbsp;·&nbsp; VOWS &nbsp;·&nbsp; FOREVER",
         masthead="THE VOWS", masthead_sub="a wedding issue",
         edition="FIRST EDITION", barcode="0 001206 000012",
         kicker="Presenting&hellip;", star="ELEANOR<br>&amp; AUGUST",
         date_big="JUNE<br>2027",
         headline="THEY SAID<br>YES",
         blurb="Eight years, two cities and one very patient dog later, our "
               "cover couple are finally getting married. Inside: the plan, "
               "the promises, and strict instructions about the seating.",
         footline="A single issue, printed for one day only.",
         issue="NO. 1 &nbsp;·&nbsp; JUNE",
         feature_kicker="THE COVER STORY",
         feature_title="How We<br>Got Here",
         feature_deck="Our cover couple on meeting at a wedding — a fact "
                      "everyone finds funnier than they do.",
         feature_body="We are not doing speeches at dinner. We are doing them "
                      "between courses, so nobody has to wait through three "
                      "of them on an empty stomach.<br><br>"
                      "Come early. The light on the lawn at five is the reason "
                      "we chose the place.<br><br>"
                      "Please do not bring a gift that needs carrying home on "
                      "a train.",
         feature_caption="The summer we met, and the summer we decided.",
         feature_pull="&ldquo;Come early, stay late, dance badly.&rdquo;",
         feature_foot="SATURDAY, 12 JUNE &nbsp;·&nbsp; 3 PM",
         feature_foot_2="ASHFORD HALL &nbsp;·&nbsp; DERBYSHIRE",
         details_kicker="THE PARTICULARS",
         details_title="The Order<br>of the Day",
         details=[("CEREMONY", "Three O&rsquo;Clock",
                   "In the chapel. Seated by ten past, please."),
                  ("RECEPTION", "The South Lawn",
                   "Drinks from five. The grass is soft."),
                  ("DRESS", "Black Tie",
                   "Or the most elegant thing you already own."),
                  ("R.S.V.P.", "Before 1 April",
                   "eleanor-and-august.com")],
         cta_script="Come and celebrate with us",
         cta_line="SATURDAY, 12 JUNE &nbsp;·&nbsp; CEREMONY AT THREE",
         cta_line_2="ASHFORD HALL &nbsp;·&nbsp; ASHFORD-IN-THE-WATER",
         back_kicker="THE LAST WORD",
         back_title="With Our<br>Deepest Thanks",
         back_body="For travelling, for toasting, and for being the reason the "
                   "day felt like ours. We will be grateful for a very long time.",
         signature="ELEANOR &amp; AUGUST"),
]


def build(c):
    t = THEMES[c["theme"]]
    return document(c["title"], FAMILIES,
                    [p_cover(t, c), p_feature(t, c), p_details(t, c),
                     p_back(t, c)],
                    body_bg="#1E1C1A")


if __name__ == "__main__":
    import pathlib
    out_dir = pathlib.Path(__file__).resolve().parent.parent / "dist"
    out_dir.mkdir(parents=True, exist_ok=True)
    for c in SUITES:
        out = out_dir / f"{c['file']}.html"
        out.write_text(build(c), encoding="utf-8")
        print(f"wrote {out.name} ({out.stat().st_size // 1024} KB)")
