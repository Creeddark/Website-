"""
ORNAMENT — viktorianisch gravierte Suiten.

Ein Seitengeruest, vier Farbwelten, vier verkaufbare Produkte. Der Hebel liegt
genau hier: die Gravur ist teuer zu bauen und billig zu variieren.

  oxblood   Ochsenblut und Gold   — Geburtstag
  emerald   Smaragd und Gold      — Hochzeit
  ivory     Elfenbein und Messing — Hochzeit, hell
  midnight  Tinte und Silber      — Gothic, Halloween

Motive: Schwan, Monogramm-Kartusche, Mond. Alles prozedural.
"""

import art
import ornament as orn
from common import W, H, page, text, svg_layer, document

FAMILIES = {"Italiana", "Pinyon Script", "Montserrat", "EB Garamond", "Cinzel"}

THEMES = {
    "oxblood": dict(
        bg="#3B1D23", bg2="#2A1219", gold="#D8B87E", light="#F2E7CE",
        soft="#C9AC85", motif="#F2E7CE", grain="#E8D5A8"),
    "emerald": dict(
        bg="#153029", bg2="#0D211C", gold="#D6B87C", light="#EFE6D2",
        soft="#B7AE8E", motif="#EFE6D2", grain="#D8E0C8"),
    "ivory": dict(
        bg="#F4EDE0", bg2="#EAE0CD", gold="#9C7A3C", light="#33291E",
        soft="#6E6046", motif="#B99451", grain="#8A7550"),
    "midnight": dict(
        bg="#14131E", bg2="#0B0A12", gold="#C3C6D4", light="#EAECF3",
        soft="#8E93A6", motif="#EAECF3", grain="#B8BCCB"),
}


def _defs(t):
    return (art.linear_bg("bg", [(0, t["bg2"]), (0.5, t["bg"]), (1, t["bg2"])],
                          angle=115)
            + art.radial_bg("halo", [(0, t["gold"], 0.16), (1, t["gold"], 0)], r=0.5)
            + art.paper_grain("grain", opacity=0.07, freq=0.85))


def _ground(t):
    return (f'<rect width="{W}" height="{H}" fill="url(#bg)"/>'
            f'<circle cx="375" cy="330" r="420" fill="url(#halo)" opacity="0.9"/>'
            f'<rect width="{W}" height="{H}" fill="{t["grain"]}" '
            f'filter="url(#grain)" opacity="0.55"/>')


def _frame(t, *, corner=124, weight=1.0):
    return orn.engraved_frame(26, 26, W - 52, H - 52, color=t["gold"],
                              corner=corner, weight=weight)


def _divider(t, cy, w=150):
    """Trennzeichen: Perlreihe, Raute, Perlreihe."""
    half = w / 2
    d = (f'<path d="M{W/2},{cy - 5} L{W/2 + 7},{cy} L{W/2},{cy + 5} '
         f'L{W/2 - 7},{cy} Z" fill="{t["gold"]}"/>')
    return (orn.beading((W / 2 - 14, cy), (W / 2 - half, cy), n=7, r0=2.0, r1=0.7,
                        color=t["gold"])
            + orn.beading((W / 2 + 14, cy), (W / 2 + half, cy), n=7, r0=2.0, r1=0.7,
                          color=t["gold"]) + d)


# ---------------------------------------------------------------------- Motive

def motif_swan(t, cy=176, size=104):
    return (orn.sparkle(W / 2 - 78, cy - 34, 9, color=t["gold"], opacity=0.85)
            + orn.sparkle(W / 2 + 84, cy - 12, 6.5, color=t["gold"], opacity=0.7)
            + orn.swan(W / 2 + 4, cy + 24, size, color=t["motif"]))


def motif_monogram(t, initials="A&amp;J", cy=180, r=54):
    """Kartusche mit Initialen — der Ersatz fuer ein Wappen bei Hochzeiten."""
    ring = (f'<circle cx="{W/2}" cy="{cy}" r="{r}" fill="none" '
            f'stroke="{t["gold"]}" stroke-width="1.6"/>'
            f'<circle cx="{W/2}" cy="{cy}" r="{r - 7}" fill="none" '
            f'stroke="{t["gold"]}" stroke-width="0.6" opacity="0.7"/>')
    wings = "".join(
        f'<g transform="translate({W/2 + s * (r + 6)},{cy}) scale({s},1)">'
        f'<path d="{orn.acanthus(0, 0, 62, 20, -18, lobes=4)}" fill="{t["gold"]}"/>'
        f'<path d="{orn.scroll(56, 14, 12, turns=1.2, start_deg=-90, w0=2.6, w1=0.3)}" '
        f'fill="{t["gold"]}"/></g>' for s in (1, -1))
    crown = (f'<g transform="translate({W/2},{cy - r - 10})">'
             f'<path d="{orn.scroll(-16, 0, 13, turns=1.15, start_deg=0, w0=2.6, w1=0.3, direction=1)}" '
             f'fill="{t["gold"]}"/>'
             f'<path d="{orn.scroll(16, 0, 13, turns=1.15, start_deg=180, w0=2.6, w1=0.3, direction=-1)}" '
             f'fill="{t["gold"]}"/></g>')
    return wings + ring + crown


def motif_moon(t, cy=178, r=52):
    return (f'<circle cx="{W/2}" cy="{cy}" r="{r + 26}" fill="{t["gold"]}" '
            f'opacity="0.07"/>'
            + art.moon(W / 2, cy, r, color=t["motif"], crater_color=t["soft"],
                       craters=8, seed=5)
            + orn.sparkle(W / 2 - 84, cy - 26, 9, color=t["gold"])
            + orn.sparkle(W / 2 + 88, cy + 8, 7, color=t["gold"], opacity=0.75))


MOTIFS = {"swan": motif_swan, "monogram": motif_monogram, "moon": motif_moon}


# ----------------------------------------------------------------- Seitentypen

def _monogram_text(t, c, cy):
    """Initialen als eigenes Textfeld — in der Grafikebene waeren sie fest."""
    if c["motif"] != "monogram":
        return []
    return [text(c["initials"], left=W / 2 - 100, top=cy - 27, width=200,
                 size=38, family="Italiana", weight=400, color=t["light"],
                 tracking=0.04, line=1.0)]


def p_invitation(t, c):
    svg = svg_layer(_defs(t),
                    _ground(t) + _frame(t) + MOTIFS[c["motif"]](t)
                    + _divider(t, 636)
                    + f'<g transform="translate({W/2},958) scale(0.62)">'
                    + f'<g transform="translate(-110,0)">'
                    + f'<path d="{orn.acanthus(0, 0, 110, 30, 0, lobes=4)}" '
                    + f'fill="{t["gold"]}"/></g>'
                    + f'<g transform="translate(110,0) scale(-1,1)">'
                    + f'<path d="{orn.acanthus(0, 0, 110, 30, 0, lobes=4)}" '
                    + f'fill="{t["gold"]}"/></g></g>')
    tt = [
        text(c["eyebrow"], left=125, top=286, width=500, size=11,
             family="Montserrat", weight=400, color=t["soft"], tracking=0.34),
        text(c["host"], left=125, top=318, width=500, size=25,
             family="Italiana", weight=400, color=t["light"], tracking=0.2),
        text(c["headline"], left=95, top=356, width=560, size=104,
             family="Pinyon Script", weight=400, color=t["light"], line=1.05),
        text(c["subhead"], left=125, top=488, width=500, size=62,
             family="Pinyon Script", weight=400, color=t["gold"], line=1.05),
        text(c["place"], left=125, top=672, width=500, size=13,
             family="Montserrat", weight=500, color=t["light"], tracking=0.28),
        text(c["address"], left=125, top=702, width=500, size=11,
             family="Montserrat", weight=400, color=t["soft"], tracking=0.24),
        text(c["time"], left=125, top=752, width=500, size=12,
             family="Montserrat", weight=400, color=t["soft"], tracking=0.3),
        text(c["month"], left=125, top=800, width=500, size=44,
             family="Italiana", weight=400, color=t["light"], line=1.1),
        text(c["day"], left=125, top=852, width=500, size=66,
             family="Pinyon Script", weight=400, color=t["gold"], line=1.05),
    ] + _monogram_text(t, c, 180)
    return page("\n".join([svg] + tt), "Invitation", bg=t["bg"])


def _detail_row(t, top, label, title, note):
    return "\n".join([
        text(label, left=118, top=top, width=514, size=9.5, family="Montserrat",
             weight=500, color=t["gold"], tracking=0.36),
        text(title, left=118, top=top + 22, width=514, size=30,
             family="Italiana", weight=400, color=t["light"], line=1.15),
        text(note, left=158, top=top + 66, width=434, size=15,
             family="EB Garamond", weight=400, color=t["soft"], style="italic",
             line=1.5),
    ])


def p_details(t, c):
    rows = c["details"]
    tops = (352, 494, 636)
    svg = svg_layer(_defs(t),
                    _ground(t) + _frame(t, corner=104, weight=0.85)
                    + _divider(t, 300, w=120)
                    + "".join(_divider(t, y, w=90) for y in (470, 612))
                    + _divider(t, 792, w=120))
    tt = [
        text(c["details_eyebrow"], left=125, top=196, width=500, size=10.5,
             family="Montserrat", weight=400, color=t["soft"], tracking=0.4),
        text(c["details_title"], left=95, top=224, width=560, size=54,
             family="Italiana", weight=400, color=t["light"], line=1.1),
    ] + [_detail_row(t, tops[i], *rows[i]) for i in range(3)] + [
        text(c["details_foot"], left=145, top=836, width=460, size=19,
             family="EB Garamond", weight=400, color=t["soft"], style="italic",
             line=1.6),
    ]
    return page("\n".join([svg] + tt), "Details", bg=t["bg"])


def p_rsvp(t, c):
    lines = "".join(
        f'<line x1="140" y1="{y}" x2="610" y2="{y}" stroke="{t["gold"]}" '
        f'stroke-width="0.9" opacity="0.55"/>' for y in (446, 546, 646))
    boxes = "".join(
        f'<rect x="{x}" y="716" width="18" height="18" fill="none" '
        f'stroke="{t["gold"]}" stroke-width="1.2"/>' for x in (186, 414))
    svg = svg_layer(_defs(t),
                    _ground(t) + _frame(t, corner=104, weight=0.85)
                    + _divider(t, 320, w=130) + lines + boxes
                    + _divider(t, 830, w=110))
    tt = [
        text("KINDLY RESPOND", left=125, top=210, width=500, size=10.5,
             family="Montserrat", weight=400, color=t["soft"], tracking=0.4),
        text("R.S.V.P.", left=125, top=240, width=500, size=58,
             family="Italiana", weight=400, color=t["light"], tracking=0.1),
        text("NAME", left=140, top=416, width=470, size=9, family="Montserrat",
             weight=500, color=t["gold"], tracking=0.34, align="left"),
        text("NUMBER ATTENDING", left=140, top=516, width=470, size=9,
             family="Montserrat", weight=500, color=t["gold"], tracking=0.34,
             align="left"),
        text("ANYTHING WE SHOULD KNOW", left=140, top=616, width=470, size=9,
             family="Montserrat", weight=500, color=t["gold"], tracking=0.34,
             align="left"),
        text("Delighted to attend", left=216, top=712, width=200, size=21,
             family="EB Garamond", weight=400, color=t["light"], align="left"),
        text("Sadly unable", left=444, top=712, width=180, size=21,
             family="EB Garamond", weight=400, color=t["light"], align="left"),
        text(c["rsvp_by"], left=125, top=862, width=500, size=10.5,
             family="Montserrat", weight=400, color=t["soft"], tracking=0.28),
        text(c["rsvp_contact"], left=125, top=894, width=500, size=20,
             family="EB Garamond", weight=400, color=t["light"], style="italic"),
    ]
    return page("\n".join([svg] + tt), "RSVP", bg=t["bg"])


def p_thanks(t, c):
    svg = svg_layer(_defs(t),
                    _ground(t) + _frame(t) + MOTIFS[c["motif"]](t, cy=250)
                    + _divider(t, 686, w=150))
    tt = [
        text(c["thanks_head"], left=95, top=396, width=560, size=98,
             family="Pinyon Script", weight=400, color=t["light"], line=1.05),
        text(c["thanks_sub"], left=125, top=536, width=500, size=10.5,
             family="Montserrat", weight=400, color=t["soft"], tracking=0.36),
        text(c["thanks_body"], left=145, top=736, width=460, size=21,
             family="EB Garamond", weight=400, color=t["light"], line=1.75,
             style="italic"),
        text(c["signature"], left=125, top=886, width=500, size=11,
             family="Montserrat", weight=500, color=t["gold"], tracking=0.36),
    ] + _monogram_text(t, c, 250)
    return page("\n".join([svg] + tt), "Thank You", bg=t["bg"])


# ------------------------------------------------------------------- Inhalte

SUITES = [
    dict(key="birthday", theme="oxblood", motif="swan",
         title="ORNEMENT — Victorian Birthday Suite",
         file="07-ornament-birthday",
         initials="E", eyebrow="YOU ARE INVITED TO", host="EMMA&rsquo;S",
         headline="Birthday", subhead="party",
         place="THE OLD LIBRARY", address="42 CORNELIA STREET, NEW YORK",
         time="SEVEN IN THE EVENING", month="April", day="Twelfth",
         details_eyebrow="THE EVENING", details_title="How It Unfolds",
         details=[("ARRIVAL", "Champagne at Seven",
                   "in the reading room, by the fire"),
                  ("DINNER", "A Long Table at Eight",
                   "four courses, and speeches between"),
                  ("AFTER", "Dancing at Eleven",
                   "until the candles have burned down")],
         details_foot="Black tie, or the closest thing you own",
         rsvp_by="KINDLY REPLY BEFORE THE FIRST OF APRIL",
         rsvp_contact="emma@example.com",
         thanks_head="Thank you", thanks_sub="FOR AN UNFORGETTABLE EVENING",
         thanks_body="For the toasts, the dancing<br>and for staying "
                     "until the very last song.",
         signature="EMMA"),
    dict(key="wedding", theme="emerald", motif="monogram",
         title="ORNEMENT — Victorian Wedding Suite",
         file="07-ornament-wedding",
         initials="E &amp; A", eyebrow="TOGETHER WITH THEIR FAMILIES",
         host="ELEANOR &amp; AUGUST",
         headline="Wedding", subhead="celebration",
         place="ASHFORD HALL", address="ASHFORD-IN-THE-WATER, DERBYSHIRE",
         time="HALF PAST THREE IN THE AFTERNOON", month="September",
         day="Twentieth",
         details_eyebrow="THE DAY", details_title="Order of Events",
         details=[("CEREMONY", "Half Past Three",
                   "in the chapel, please be seated by ten past"),
                  ("RECEPTION", "Five O&rsquo;Clock",
                   "drinks on the south lawn"),
                  ("DINNER", "Seven O&rsquo;Clock",
                   "in the great hall, dancing to follow")],
         details_foot="Black tie &mdash; and comfortable shoes for the lawn",
         rsvp_by="KINDLY REPLY BEFORE THE FIRST OF JULY",
         rsvp_contact="eleanor-and-august.com",
         thanks_head="Thank you", thanks_sub="FOR CELEBRATING WITH US",
         thanks_body="Your presence made the day complete.<br>"
                     "We are grateful beyond words.",
         signature="ELEANOR &amp; AUGUST"),
    dict(key="wedding-ivory", theme="ivory", motif="monogram",
         title="ORNEMENT — Ivory Wedding Suite",
         file="07-ornament-ivory",
         initials="R &amp; T", eyebrow="REQUEST THE PLEASURE OF YOUR COMPANY",
         host="ROSE &amp; THEODORE",
         headline="Marriage", subhead="of",
         place="THE ORANGERY AT KEW", address="RICHMOND, LONDON",
         time="FOUR O&rsquo;CLOCK IN THE AFTERNOON", month="June",
         day="Fourteenth",
         details_eyebrow="THE DAY", details_title="Order of Events",
         details=[("CEREMONY", "Four O&rsquo;Clock",
                   "under the glass roof of the orangery"),
                  ("APERITIF", "Half Past Five",
                   "on the terrace, weather permitting"),
                  ("DINNER", "Seven O&rsquo;Clock",
                   "in the long gallery, dancing after")],
         details_foot="Garden formal &mdash; the lawn is soft underfoot",
         rsvp_by="KINDLY REPLY BEFORE THE FIRST OF APRIL",
         rsvp_contact="rose-and-theodore.com",
         thanks_head="Thank you", thanks_sub="FOR SHARING OUR DAY",
         thanks_body="For every kindness, every toast<br>"
                     "and for being there when it mattered.",
         signature="ROSE &amp; THEODORE"),
    dict(key="gothic", theme="midnight", motif="moon",
         title="ORNEMENT — Gothic Night Suite",
         file="07-ornament-gothic",
         initials="R", eyebrow="YOU ARE SUMMONED TO", host="A GATHERING AT",
         headline="Midnight", subhead="soirée",
         place="RAVENSCOURT HOUSE", address="13 HOLLOWAY LANE",
         time="FROM NINE UNTIL THE SMALL HOURS", month="October",
         day="Thirty-first",
         details_eyebrow="THE NIGHT", details_title="What Awaits",
         details=[("THE DRESS", "Black, and Nothing Else",
                   "masks are welcome, faces optional"),
                  ("THE TABLE", "A Supper at Ten",
                   "served by candlelight, as it should be"),
                  ("THE HOUR", "Midnight",
                   "the lights go out. Be somewhere interesting.")],
         details_foot="No telephones after eleven. We mean it.",
         rsvp_by="REPLY BEFORE THE TWENTY-FOURTH",
         rsvp_contact="ravenscourt@example.com",
         thanks_head="Thank you", thanks_sub="FOR A NIGHT WELL HAUNTED",
         thanks_body="The candles are out, the wine is gone<br>"
                     "and the house is quiet again.",
         signature="UNTIL NEXT OCTOBER"),
]


def build(suite):
    t = THEMES[suite["theme"]]
    return document(suite["title"], FAMILIES,
                    [p_invitation(t, suite), p_details(t, suite),
                     p_rsvp(t, suite), p_thanks(t, suite)],
                    body_bg="#232028")


if __name__ == "__main__":
    import pathlib
    out_dir = pathlib.Path(__file__).resolve().parent.parent / "dist"
    out_dir.mkdir(parents=True, exist_ok=True)
    for suite in SUITES:
        out = out_dir / f"{suite['file']}.html"
        out.write_text(build(suite), encoding="utf-8")
        print(f"wrote {out.name} ({out.stat().st_size // 1024} KB)")
