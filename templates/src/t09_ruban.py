"""
RUBAN — Coquette-Suiten.

Der Gegenentwurf zu ORNAMENT: fast leeres Papier, ein einziges gezeichnetes
Objekt und sehr feine Typografie. Die Wirkung entsteht aus Zurueckhaltung,
also darf nichts Zweites um Aufmerksamkeit bitten.

Drei Farbwelten, drei Anlaesse. Objekte: Coupe-Glas mit Schleife, Perlenbogen,
Schleife allein.
"""

import ornament as orn
import art
from common import W, H, page, text, svg_layer, document

FAMILIES = {"Italiana", "Pinyon Script", "Montserrat", "Antic Didone",
            "EB Garamond"}

THEMES = {
    "noir": dict(paper="#FBFAF7", paper2="#F3F1EC", ink="#141414",
                 soft="#6E6A63", hair="#D8D4CC", ribbon="#141414",
                 glass="#DAD6CE", rim="#B4AFA4", liquid="#EFE3C4",
                 pearl="#EDE8DE", pearl_rim="#CBC4B6"),
    "blush": dict(paper="#FDF8F6", paper2="#F7EDE9", ink="#3A2A2A",
                  soft="#8C7470", hair="#E6D8D2", ribbon="#B87C7C",
                  glass="#EAD9D5", rim="#C9AEA8", liquid="#F3D9D2",
                  pearl="#F7E9E4", pearl_rim="#DCC3BC"),
    "sage": dict(paper="#FAFBF7", paper2="#EFF2EA", ink="#2C332A",
                 soft="#6E7768", hair="#D9DFD2", ribbon="#7C8B70",
                 glass="#DCE2D6", rim="#AEB8A6", liquid="#E4EBDC",
                 pearl="#EDF1E7", pearl_rim="#C3CBBA"),
}


def _defs(t):
    return (art.paper_grain("grain", opacity=0.035, freq=0.95)
            + art.radial_bg("soft", [(0, t["hair"], 0.5), (1, t["hair"], 0)], r=0.5))


def _ground(t, bg=None):
    return (f'<rect width="{W}" height="{H}" fill="{bg or t["paper"]}"/>'
            f'<circle cx="620" cy="120" r="300" fill="url(#soft)" opacity="0.55"/>'
            f'<rect width="{W}" height="{H}" fill="#8A857A" '
            f'filter="url(#grain)" opacity="0.8"/>')


def _hairline(t, y, x0=150, x1=600, w=0.7):
    return (f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{t["hair"]}" '
            f'stroke-width="{w}"/>')


# --------------------------------------------------------------------- Motive

def motif_coupe(t):
    """Glas am linken Rand, angeschnitten — die Komposition der Referenz."""
    return (f'<g transform="translate(152,338)">'
            + orn.coupe_glass(0, 0, 336, glass=t["glass"], rim=t["rim"],
                              liquid=t["liquid"], seed=7)
            + orn.bow(10, 108, 132, color=t["ribbon"], tilt=-5, tail_len=1.1)
            + '</g>')


def motif_bow(t, cy=210, size=150):
    return (f'<g transform="translate({W / 2},{cy})">'
            + orn.bow(0, 0, size, color=t["ribbon"], tilt=-2, tail_len=1.15)
            + '</g>')


def motif_pearls(t, cy=214):
    return (orn.pearl_arc(W / 2, cy + 60, 168, 116, 196, 344, n=26, r=6.2,
                          color=t["pearl"], stroke=t["pearl_rim"], seed=5)
            + f'<g transform="translate({W / 2},{cy - 44})">'
            + orn.bow(0, 0, 92, color=t["ribbon"], tilt=-3, tail_len=0.7)
            + '</g>')


MOTIFS = {"coupe": motif_coupe, "bow": motif_bow, "pearls": motif_pearls}


# ---------------------------------------------------------------- Seitentypen

def p_invitation(t, c):
    left = c["align_left"]
    x, w, al = (368, 316, "left") if left else (125, 500, "center")
    svg = svg_layer(_defs(t),
                    _ground(t) + MOTIFS[c["motif"]](t)
                    + _hairline(t, 690, x0=x, x1=x + w)
                    + _hairline(t, 902, x0=x, x1=x + w))
    tt = [
        text(c["eyebrow"], left=x, top=418, width=w, size=10,
             family="Montserrat", weight=400, color=t["soft"], tracking=0.36,
             align=al),
        text(c["name"], left=x - 8, top=444, width=w + 16, size=76,
             family="Pinyon Script", weight=400, color=t["ink"], line=1.1,
             align=al),
        text(c["occasion"], left=x, top=556, width=w, size=27,
             family="Italiana", weight=400, color=t["ink"], tracking=0.14,
             align=al),
        text(c["date"], left=x, top=610, width=w, size=13,
             family="Montserrat", weight=400, color=t["soft"], tracking=0.24,
             align=al),
        text(c["venue"], left=x, top=716, width=w, size=12,
             family="Montserrat", weight=500, color=t["ink"], tracking=0.26,
             align=al),
        text(c["address"], left=x, top=746, width=w, size=11,
             family="Montserrat", weight=400, color=t["soft"], tracking=0.22,
             line=1.7, align=al),
        text("R.s.v.p.", left=x, top=826, width=w, size=34,
             family="Pinyon Script", weight=400, color=t["ink"], align=al),
        text(c["rsvp"], left=x, top=930, width=w, size=11,
             family="Montserrat", weight=400, color=t["soft"], tracking=0.22,
             line=1.7, align=al),
    ]
    return page("\n".join([svg] + tt), "Invitation", bg=t["paper"])


def _row(t, top, label, value, note):
    return "\n".join([
        text(label, left=140, top=top, width=470, size=9, family="Montserrat",
             weight=500, color=t["soft"], tracking=0.36, align="left"),
        text(value, left=140, top=top + 20, width=470, size=27,
             family="Italiana", weight=400, color=t["ink"], align="left",
             line=1.15),
        text(note, left=140, top=top + 60, width=470, size=14,
             family="EB Garamond", weight=400, color=t["soft"], style="italic",
             align="left", line=1.5),
    ])


def p_details(t, c):
    tops = (352, 486, 620, 754)
    svg = svg_layer(_defs(t),
                    _ground(t, t["paper2"])
                    + f'<g transform="translate({W / 2},218)">'
                    + orn.bow(0, 0, 96, color=t["ribbon"], tilt=-3, tail_len=0.8)
                    + '</g>'
                    + "".join(_hairline(t, y, x0=140, x1=610)
                              for y in (462, 596, 730)))
    tt = [
        text(c["details_eyebrow"], left=125, top=286, width=500, size=10,
             family="Montserrat", weight=400, color=t["soft"], tracking=0.4),
        text(c["details_title"], left=125, top=312, width=500, size=44,
             family="Italiana", weight=400, color=t["ink"], line=1.1),
    ] + [_row(t, tops[i], *c["details"][i]) for i in range(4)] + [
        text(c["details_foot"], left=145, top=884, width=460, size=19,
             family="EB Garamond", weight=400, color=t["soft"], style="italic",
             line=1.6),
    ]
    return page("\n".join([svg] + tt), "Details", bg=t["paper2"])


def p_rsvp(t, c):
    lines = "".join(_hairline(t, y, x0=150, x1=600, w=0.9)
                    for y in (452, 552, 652))
    boxes = "".join(
        f'<rect x="{x}" y="722" width="17" height="17" fill="none" '
        f'stroke="{t["ink"]}" stroke-width="1"/>' for x in (196, 424))
    svg = svg_layer(_defs(t),
                    _ground(t)
                    + orn.pearl_arc(W / 2, 268, 196, 96, 198, 342, n=26, r=8.5,
                                    color=t["pearl"], stroke=t["pearl_rim"],
                                    seed=9)
                    + lines + boxes)
    tt = [
        text("KINDLY REPLY", left=125, top=306, width=500, size=10,
             family="Montserrat", weight=400, color=t["soft"], tracking=0.4),
        text("R.s.v.p.", left=125, top=332, width=500, size=64,
             family="Pinyon Script", weight=400, color=t["ink"], line=1.1),
        text("NAME", left=150, top=424, width=450, size=8.5,
             family="Montserrat", weight=500, color=t["soft"], tracking=0.34,
             align="left"),
        text("NUMBER ATTENDING", left=150, top=524, width=450, size=8.5,
             family="Montserrat", weight=500, color=t["soft"], tracking=0.34,
             align="left"),
        text("ANYTHING WE SHOULD KNOW", left=150, top=624, width=450, size=8.5,
             family="Montserrat", weight=500, color=t["soft"], tracking=0.34,
             align="left"),
        text("Delighted", left=224, top=718, width=170, size=21,
             family="EB Garamond", weight=400, color=t["ink"], align="left"),
        text("Sadly unable", left=452, top=718, width=180, size=21,
             family="EB Garamond", weight=400, color=t["ink"], align="left"),
        text(c["rsvp_by"], left=125, top=828, width=500, size=10,
             family="Montserrat", weight=400, color=t["soft"], tracking=0.28),
        text(c["rsvp_contact"], left=125, top=858, width=500, size=21,
             family="EB Garamond", weight=400, color=t["ink"], style="italic"),
    ]
    return page("\n".join([svg] + tt), "RSVP", bg=t["paper"])


def p_thanks(t, c):
    svg = svg_layer(_defs(t),
                    _ground(t, t["paper2"])
                    + f'<g transform="translate({W / 2},252)">'
                    + orn.bow(0, 0, 138, color=t["ribbon"], tilt=-2, tail_len=1.2)
                    + '</g>'
                    + _hairline(t, 636, x0=280, x1=470))
    tt = [
        text("Thank you", left=95, top=470, width=560, size=84,
             family="Pinyon Script", weight=400, color=t["ink"], line=1.1),
        text(c["thanks_sub"], left=125, top=590, width=500, size=10,
             family="Montserrat", weight=400, color=t["soft"], tracking=0.36),
        text(c["thanks_body"], left=145, top=690, width=460, size=21,
             family="EB Garamond", weight=400, color=t["ink"], line=1.8,
             style="italic"),
        text(c["signature"], left=125, top=868, width=500, size=11,
             family="Montserrat", weight=500, color=t["ink"], tracking=0.36),
    ]
    return page("\n".join([svg] + tt), "Thank You", bg=t["paper2"])


# -------------------------------------------------------------------- Inhalte

SUITES = [
    dict(file="09-ruban-birthday", theme="noir", motif="coupe", align_left=True,
         title="RUBAN — Coquette Birthday Suite",
         eyebrow="JOIN US TO CELEBRATE", name="Olivia", occasion="30TH BIRTHDAY",
         date="SATURDAY, 5 JUNE &nbsp;·&nbsp; 2 PM",
         venue="THE GARDEN ROOM",
         address="123 Party Street<br>California, 123456",
         rsvp="To Charlotte on 0170 000 0000<br>before the first of May",
         details_eyebrow="THE AFTERNOON", details_title="How It Goes",
         details=[("ARRIVAL", "Two O&rsquo;Clock", "champagne and something small to eat"),
                  ("LUNCH", "Half Past Three", "one long table, no seating plan"),
                  ("CAKE", "Five O&rsquo;Clock", "and a short speech, we promise"),
                  ("ONWARDS", "Seven O&rsquo;Clock", "for anyone still standing")],
         details_foot="Wear something you can dance in",
         rsvp_by="KINDLY REPLY BEFORE THE FIRST OF MAY",
         rsvp_contact="charlotte &middot; 0170 000 0000",
         thanks_sub="FOR MAKING THIRTY LOOK EASY",
         thanks_body="For the flowers, the toasts<br>and for staying far too late.",
         signature="OLIVIA"),

    dict(file="09-ruban-bridal", theme="blush", motif="pearls", align_left=False,
         title="RUBAN — Bridal Shower Suite",
         eyebrow="YOU ARE INVITED TO A BRIDAL SHOWER FOR",
         name="Isabella", occasion="BRIDE TO BE",
         date="SUNDAY, 18 MAY &nbsp;·&nbsp; 1 PM",
         venue="THE ORANGERY",
         address="8 Rosewood Lane<br>Hampstead, London",
         rsvp="To Marie on 0170 000 0000<br>before the first of May",
         details_eyebrow="THE AFTERNOON", details_title="What to Expect",
         details=[("ARRIVAL", "One O&rsquo;Clock", "fizz on the terrace, weather willing"),
                  ("LUNCH", "Two O&rsquo;Clock", "long table, short speeches"),
                  ("GAMES", "Four O&rsquo;Clock", "gentle ones. Nothing embarrassing."),
                  ("GIFTS", "Five O&rsquo;Clock", "opened slowly, with commentary")],
         details_foot="Dress code: soft neutrals and something borrowed",
         rsvp_by="KINDLY REPLY BEFORE THE FIRST OF MAY",
         rsvp_contact="marie &middot; 0170 000 0000",
         thanks_sub="FOR SPOILING THE BRIDE",
         thanks_body="For the advice, the laughter<br>and for making the day so soft.",
         signature="ISABELLA"),

    dict(file="09-ruban-baby", theme="sage", motif="bow", align_left=False,
         title="RUBAN — Baby Shower Suite",
         eyebrow="PLEASE JOIN US FOR A BABY SHOWER HONOURING",
         name="Marlene", occasion="MOTHER TO BE",
         date="SATURDAY, 9 MARCH &nbsp;·&nbsp; 2 PM",
         venue="THE GREENHOUSE",
         address="Parkstrasse 8<br>Leipzig",
         rsvp="To Anna on 0170 000 0000<br>before the first of March",
         details_eyebrow="THE AFTERNOON", details_title="What to Expect",
         details=[("ARRIVAL", "Two O&rsquo;Clock", "tea, cake and quiet conversation"),
                  ("ADVICE", "Three O&rsquo;Clock", "one card each, honest ones welcome"),
                  ("GUESSES", "Four O&rsquo;Clock", "date, weight and the name"),
                  ("GIFTS", "Five O&rsquo;Clock", "nappies gratefully received")],
         details_foot="No need to bring anything but yourself",
         rsvp_by="KINDLY REPLY BEFORE THE FIRST OF MARCH",
         rsvp_contact="anna &middot; 0170 000 0000",
         thanks_sub="FOR SHOWERING US WITH LOVE",
         thanks_body="For the gifts, the good advice<br>and for a very gentle afternoon.",
         signature="MARLENE &amp; JONAS"),
]


def build(c):
    t = THEMES[c["theme"]]
    return document(c["title"], FAMILIES,
                    [p_invitation(t, c), p_details(t, c), p_rsvp(t, c),
                     p_thanks(t, c)],
                    body_bg="#4A4842")


if __name__ == "__main__":
    import pathlib
    out_dir = pathlib.Path(__file__).resolve().parent.parent / "dist"
    out_dir.mkdir(parents=True, exist_ok=True)
    for c in SUITES:
        out = out_dir / f"{c['file']}.html"
        out.write_text(build(c), encoding="utf-8")
        print(f"wrote {out.name} ({out.stat().st_size // 1024} KB)")
