"""
THE TIMES — Zeitungs-Suiten.

Eine Zeitungs-Engine, drei Anlaesse. Der Reiz dieses Stils liegt in Details,
die echte Zeitungen haben und Vorlagen meistens weglassen: Haarlinien ueber
und unter dem Titelkopf, ein Datumsband mit Ausgabenzeile, Spalten mit
Initiale, Bildunterschriften in Kursiv, ein Kleinanzeigen-Raster.

Fotos sitzen als eigene Bildfelder auf der Seite. Der Kaeufer klickt sie in
Canva an und ersetzt sie durch eigene Aufnahmen; bis dahin steht dort ein
Halbtonraster, das zum Druckbild passt.
"""

import art
from common import W, H, page, text, svg_layer, document, image

FAMILIES = {"UnifrakturMaguntia", "Archivo Black", "EB Garamond", "Oswald",
            "Montserrat", "Pinyon Script", "Abril Fatface"}

PAPER = "#EFEADC"
PAPER_2 = "#E6E0CF"
INK = "#16150F"
INK_2 = "#3E3A2E"
INK_3 = "#6E6858"
RULE = "#B3AC98"


def _defs():
    return (art.paper_grain("grain", opacity=0.10, freq=0.9)
            + art.linear_bg("age", [(0, "#D8CFB4", 0.55), (0.4, "#D8CFB4", 0),
                                    (1, "#C8BE9E", 0.5)], angle=125))


def _ground():
    """Papier mit Alterung an den Raendern und Druckkorn."""
    return (f'<rect width="{W}" height="{H}" fill="{PAPER}"/>'
            f'<rect width="{W}" height="{H}" fill="url(#age)"/>'
            f'<rect width="{W}" height="{H}" fill="#5C5334" '
            f'filter="url(#grain)" opacity="0.85"/>')


def _rule(y, *, x0=42, x1=W - 42, w=1.0, op=1.0):
    return (f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{INK}" '
            f'stroke-width="{w}" opacity="{op}"/>')


def _double_rule(y, gap=4):
    return _rule(y, w=2.2) + _rule(y + gap, w=0.7)


def _vrule(x, y0, y1, *, w=0.7, op=0.5):
    return (f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y1}" stroke="{INK}" '
            f'stroke-width="{w}" opacity="{op}"/>')


def _photo_border(x, y, w, h):
    return (f'<rect x="{x - 2}" y="{y - 2}" width="{w + 4}" height="{h + 4}" '
            f'fill="none" stroke="{INK}" stroke-width="1.1"/>')


# ------------------------------------------------------------------- Seite 1

def p_front(c):
    svg = svg_layer(_defs(),
                    _ground()
                    + _rule(104, w=0.8) + _double_rule(186)
                    + _rule(222, w=0.8, op=0.6)
                    + _rule(430, w=1.6)
                    + _photo_border(64, 462, 622, 366)
                    + _rule(866, w=0.8, op=0.6)
                    + _double_rule(972))
    tt = [
        text(c["kicker_l"], left=48, top=82, width=210, size=8.5,
             family="Montserrat", weight=500, color=INK_2, tracking=0.22,
             align="left"),
        text(c["price"], left=W - 258, top=82, width=210, size=8.5,
             family="Montserrat", weight=500, color=INK_2, tracking=0.22,
             align="right"),
        text(c["masthead"], left=40, top=112, width=W - 80, size=62,
             family="UnifrakturMaguntia", weight=400, color=INK, line=1.05),
        text(c["dateline"], left=48, top=196, width=W - 96, size=9,
             family="Montserrat", weight=500, color=INK_2, tracking=0.26),
        text(c["headline"], left=52, top=246, width=W - 104, size=54,
             family="Archivo Black", weight=400, color=INK, line=1.02,
             tracking=-0.02),
        text(c["deck"], left=92, top=372, width=W - 184, size=19,
             family="EB Garamond", weight=400, color=INK_2, style="italic",
             line=1.35),
        text(c["caption"], left=64, top=840, width=622, size=11,
             family="EB Garamond", weight=400, color=INK_3, style="italic"),
        text(c["strap"], left=48, top=894, width=W - 96, size=13,
             family="Oswald", weight=400, color=INK, tracking=0.3),
        text(c["strap_2"], left=48, top=924, width=W - 96, size=10,
             family="Montserrat", weight=400, color=INK_3, tracking=0.22),
        text(c["folio"], left=48, top=990, width=W - 96, size=8.5,
             family="Montserrat", weight=400, color=INK_3, tracking=0.24),
    ]
    img = image("photo-landscape.png", left=64, top=462, width=622, height=366,
                alt="Foto des Gastgebers")
    return page("\n".join([svg, img] + tt), "Front Page", bg=PAPER)


# ------------------------------------------------------------------- Seite 2

def p_inside(c):
    svg = svg_layer(_defs(),
                    _ground()
                    + _rule(84, w=1.8) + _rule(88, w=0.6)
                    + _rule(268, w=1.2)
                    + _vrule(372, 292, 700)
                    + _photo_border(48, 292, 300, 190)
                    + _photo_border(48, 502, 300, 198)
                    + _rule(730, w=1.2)
                    + f'<rect x="48" y="756" width="{W - 96}" height="152" '
                      f'fill="none" stroke="{INK}" stroke-width="1.6"/>'
                    + _vrule(232, 756, 908, w=1.0, op=0.9)
                    + _double_rule(946))
    tt = [
        text(c["masthead_small"], left=48, top=56, width=W - 96, size=11,
             family="Montserrat", weight=500, color=INK_2, tracking=0.34),
        text(c["inside_script"], left=92, top=104, width=W - 184, size=52,
             family="Pinyon Script", weight=400, color=INK, line=1.0),
        text(c["inside_headline"], left=52, top=178, width=W - 104, size=46,
             family="Archivo Black", weight=400, color=INK, line=1.0,
             tracking=-0.02),
        text(c["photo_caption_1"], left=48, top=486, width=300, size=9.5,
             family="EB Garamond", weight=400, color=INK_3, style="italic",
             align="left"),
        text(c["column_title"], left=392, top=290, width=310, size=24,
             family="Abril Fatface", weight=400, color=INK, align="left",
             line=1.15),
        text(c["column_body"], left=392, top=344, width=310, size=12.5,
             family="EB Garamond", weight=400, color=INK_2, align="left",
             line=1.62),
        text(c["box_day"], left=64, top=790, width=152, size=42,
             family="Archivo Black", weight=400, color=INK, line=1.0),
        text(c["box_month"], left=64, top=846, width=152, size=13,
             family="Oswald", weight=400, color=INK_2, tracking=0.3),
        text(c["box_line_1"], left=252, top=788, width=430, size=26,
             family="Pinyon Script", weight=400, color=INK, align="left"),
        text(c["box_line_2"], left=252, top=832, width=430, size=11,
             family="Montserrat", weight=500, color=INK_2, tracking=0.24,
             align="left"),
        text(c["box_line_3"], left=252, top=862, width=430, size=11,
             family="Montserrat", weight=400, color=INK_3, tracking=0.2,
             align="left"),
        text(c["folio_2"], left=48, top=964, width=W - 96, size=8.5,
             family="Montserrat", weight=400, color=INK_3, tracking=0.24),
    ]
    imgs = (image("photo-landscape.png", left=48, top=292, width=300, height=190,
                  alt="Foto eins")
            + image("photo-portrait.png", left=48, top=502, width=300, height=198,
                    alt="Foto zwei"))
    return page("\n".join([svg, imgs] + tt), "Inside", bg=PAPER)


# ------------------------------------------------------------------- Seite 3

def _classified(x, y, w, label, title, body):
    return "\n".join([
        text(label, left=x, top=y, width=w, size=8.5, family="Montserrat",
             weight=600, color=INK_2, tracking=0.3, align="left"),
        text(title, left=x, top=y + 20, width=w, size=21, family="Abril Fatface",
             weight=400, color=INK, align="left", line=1.15),
        text(body, left=x, top=y + 54, width=w, size=11.5, family="EB Garamond",
             weight=400, color=INK_2, align="left", line=1.6),
    ])


def p_classifieds(c):
    cols = c["classifieds"]
    svg = svg_layer(_defs(),
                    _ground()
                    + _rule(84, w=1.8) + _rule(88, w=0.6)
                    + _rule(228, w=1.2)
                    + _vrule(W / 2, 258, 862, w=0.7, op=0.45)
                    + "".join(_rule(y, x0=48, x1=W / 2 - 18, w=0.6, op=0.4)
                              for y in (410, 562, 714))
                    + "".join(_rule(y, x0=W / 2 + 18, x1=W - 48, w=0.6, op=0.4)
                              for y in (410, 562, 714))
                    + _rule(890, w=1.2)
                    + _double_rule(966))
    tt = [
        text(c["masthead_small"], left=48, top=56, width=W - 96, size=11,
             family="Montserrat", weight=500, color=INK_2, tracking=0.34),
        text("THE PARTICULARS", left=48, top=110, width=W - 96, size=10,
             family="Montserrat", weight=500, color=INK_3, tracking=0.4),
        text(c["classified_title"], left=52, top=136, width=W - 104, size=54,
             family="Archivo Black", weight=400, color=INK, line=1.0,
             tracking=-0.02),
    ]
    xs = (48, W / 2 + 18)
    ys = (262, 414, 566, 718)
    for i, item in enumerate(cols[:8]):
        tt.append(_classified(xs[i % 2], ys[i // 2], 300, *item))
    tt.append(text(c["classified_foot"], left=92, top=912, width=W - 184,
                   size=19, family="EB Garamond", weight=400, color=INK_2,
                   style="italic"))
    return page("\n".join([svg] + tt), "The Particulars", bg=PAPER_2)


# ------------------------------------------------------------------- Seite 4

def p_notice(c):
    svg = svg_layer(_defs(),
                    _ground()
                    + _rule(84, w=1.8) + _rule(88, w=0.6)
                    + _photo_border(212, 172, 326, 240)
                    + _rule(470, w=1.2)
                    + f'<rect x="70" y="512" width="{W - 140}" height="300" '
                      f'fill="none" stroke="{INK}" stroke-width="1.4"/>'
                    + f'<rect x="78" y="520" width="{W - 156}" height="284" '
                      f'fill="none" stroke="{INK}" stroke-width="0.5" opacity="0.6"/>'
                    + _double_rule(940))
    tt = [
        text(c["masthead_small"], left=48, top=56, width=W - 96, size=11,
             family="Montserrat", weight=500, color=INK_2, tracking=0.34),
        text(c["notice_caption"], left=212, top=424, width=326, size=10,
             family="EB Garamond", weight=400, color=INK_3, style="italic"),
        text("WITH THANKS", left=48, top=498, width=W - 96, size=9,
             family="Montserrat", weight=600, color=INK_3, tracking=0.4),
        text(c["notice_head"], left=110, top=556, width=W - 220, size=44,
             family="Abril Fatface", weight=400, color=INK, line=1.08),
        text(c["notice_body"], left=126, top=648, width=W - 252, size=14,
             family="EB Garamond", weight=400, color=INK_2, line=1.75),
        text(c["signature"], left=110, top=756, width=W - 220, size=11,
             family="Montserrat", weight=500, color=INK, tracking=0.32),
        text(c["folio_3"], left=48, top=958, width=W - 96, size=8.5,
             family="Montserrat", weight=400, color=INK_3, tracking=0.24),
    ]
    img = image("photo-square.png", left=212, top=172, width=326, height=240,
                alt="Erinnerungsfoto")
    return page("\n".join([svg, img] + tt), "Notice of Thanks", bg=PAPER)


# -------------------------------------------------------------------- Inhalte

SUITES = [
    dict(file="08-times-birthday", title="THE TIMES — Birthday Newspaper Suite",
         kicker_l="NO. 30 &nbsp;·&nbsp; BIRTHDAY EDITION", price="ONE SLICE OF CAKE",
         masthead="The Birthday Times",
         masthead_small="THE BIRTHDAY TIMES &nbsp;·&nbsp; BIRTHDAY EDITION",
         dateline="FRIDAY &nbsp;·&nbsp; THE TWENTY-FOURTH OF MARCH &nbsp;·&nbsp; "
                  "PUBLISHED FOR ONE NIGHT ONLY",
         headline="EMMA IS<br>TURNING THIRTY",
         deck="Sources confirm the guest of honour intends to dance<br>"
              "until the neighbours complain.",
         caption="The birthday girl, photographed shortly before the candles.",
         strap="AN INVITATION IS EXTENDED TO ALL READERS",
         strap_2="SATURDAY, 24 MARCH &nbsp;·&nbsp; 8 PM &nbsp;·&nbsp; "
                 "12 CORNELIA STREET",
         folio="PAGE ONE &nbsp;·&nbsp; THE BIRTHDAY TIMES &nbsp;·&nbsp; "
               "PRINTED WITH LOVE",
         inside_script="Happy Birthday",
         inside_headline="IT&rsquo;S PARTY TIME",
         photo_caption_1="Previous celebrations, from the archive.",
         column_title="Thirty Never<br>Looked So Good",
         column_body="I have been dreaming about this birthday for what feels "
                     "like forever, and now it is finally here. I want it to be "
                     "nothing less than perfect.<br><br>"
                     "This is not just another birthday. It is a milestone, and "
                     "a moment that marks a new chapter.<br><br>"
                     "Join me for an evening of glamour, laughter and "
                     "unforgettable memories, surrounded by the most fabulous "
                     "company.",
         box_day="24", box_month="MARCH",
         box_line_1="Let&rsquo;s celebrate together",
         box_line_2="THE ROOFTOP &nbsp;·&nbsp; 12 CORNELIA STREET",
         box_line_3="EIGHT IN THE EVENING &nbsp;·&nbsp; DRESS TO BE PHOTOGRAPHED",
         folio_2="PAGE TWO &nbsp;·&nbsp; THE BIRTHDAY TIMES",
         classified_title="THE FINE PRINT",
         classifieds=[
             ("WHEN", "Saturday, 24 March",
              "Doors at eight. The cake will not wait, and neither will we."),
             ("WHERE", "The Rooftop",
              "12 Cornelia Street. Take the lift to the top and follow the noise."),
             ("DRESS", "Black &amp; Gold",
              "Wear something you would be happy to be photographed in."),
             ("GIFTS", "Your Presence",
              "Genuinely enough. If you insist, bring something to drink."),
             ("MUSIC", "Requests Welcome",
              "Send your song before the night and it will be played."),
             ("GETTING HOME", "Taxis at One",
              "The rank is on the corner. Do not attempt to walk it."),
         ],
         classified_foot="Kindly reply before the first of March",
         notice_caption="Thank you for coming, and for staying late.",
         notice_head="A Notice<br>of Thanks",
         notice_body="To everyone who came, who danced, who toasted and who "
                     "stayed until the very last song &mdash; thank you. It was "
                     "the night I had hoped for, and then some.",
         signature="EMMA", folio_3="THE BIRTHDAY TIMES &nbsp;·&nbsp; FINAL EDITION"),

    dict(file="08-times-wedding", title="THE TIMES — Wedding Newspaper Suite",
         kicker_l="WEDDING EDITION &nbsp;·&nbsp; VOL. I", price="ONE GLASS OF CHAMPAGNE",
         masthead="The Wedding Times",
         masthead_small="THE WEDDING TIMES &nbsp;·&nbsp; WEDDING EDITION",
         dateline="SATURDAY &nbsp;·&nbsp; THE TWELFTH OF JUNE &nbsp;·&nbsp; "
                  "ONE EDITION, ONE DAY",
         headline="SHE SAID YES.<br>NOW IT&rsquo;S OFFICIAL",
         deck="After a long engagement and several arguments about seating,<br>"
              "the happy couple will finally be married.",
         caption="The couple, photographed the summer they met.",
         strap="ALL READERS ARE WARMLY INVITED",
         strap_2="SATURDAY, 12 JUNE &nbsp;·&nbsp; 3 PM &nbsp;·&nbsp; "
                 "ASHFORD HALL, DERBYSHIRE",
         folio="PAGE ONE &nbsp;·&nbsp; THE WEDDING TIMES &nbsp;·&nbsp; "
               "PRINTED WITH LOVE",
         inside_script="Our Wedding Day",
         inside_headline="THE ORDER<br>OF EVENTS",
         photo_caption_1="From the archive: the proposal, and the morning after.",
         column_title="How We Got<br>Here",
         column_body="We met at a wedding, which everyone finds funnier than we "
                     "do. Eight years, two cities and one very patient dog later, "
                     "here we are.<br><br>"
                     "We are not doing speeches at dinner. We are doing them "
                     "between courses, so nobody has to wait.<br><br>"
                     "Come early, stay late, and please do not bring a gift that "
                     "needs carrying home.",
         box_day="12", box_month="JUNE",
         box_line_1="Come and celebrate with us",
         box_line_2="ASHFORD HALL &nbsp;·&nbsp; ASHFORD-IN-THE-WATER",
         box_line_3="CEREMONY AT THREE &nbsp;·&nbsp; DINNER AND DANCING TO FOLLOW",
         folio_2="PAGE TWO &nbsp;·&nbsp; THE WEDDING TIMES",
         classified_title="THE FINE PRINT",
         classifieds=[
             ("CEREMONY", "Three O&rsquo;Clock",
              "In the chapel. Please be seated by ten minutes past."),
             ("RECEPTION", "The South Lawn",
              "Drinks from five. The grass is soft &mdash; choose shoes wisely."),
             ("DRESS", "Black Tie",
              "Or the most elegant thing already hanging in your wardrobe."),
             ("GIFTS", "No Boxes, Please",
              "We are saving for a roof. There is a link on the website."),
             ("CHILDREN", "Very Welcome",
              "There is a room with films and someone sensible watching them."),
             ("STAYING", "Rooms in the Village",
              "The inn holds a block until the first of May. Mention our names."),
         ],
         classified_foot="Kindly reply before the first of April",
         notice_caption="Our first dance, and the last of the light.",
         notice_head="With Our<br>Deepest Thanks",
         notice_body="For travelling, for toasting, for dancing badly and for "
                     "being the reason the day felt like ours. We will be "
                     "grateful for a very long time.",
         signature="ELEANOR &amp; AUGUST",
         folio_3="THE WEDDING TIMES &nbsp;·&nbsp; FINAL EDITION"),

    dict(file="08-times-baby", title="THE TIMES — Baby Announcement Suite",
         kicker_l="SPECIAL DELIVERY &nbsp;·&nbsp; FIRST EDITION",
         price="PRICELESS",
         masthead="The Daily Bundle",
         masthead_small="THE DAILY BUNDLE &nbsp;·&nbsp; SPECIAL DELIVERY",
         dateline="TUESDAY &nbsp;·&nbsp; THE NINTH OF FEBRUARY &nbsp;·&nbsp; "
                  "FIRST AND ONLY EDITION",
         headline="SHE&rsquo;S HERE.<br>AND SHE&rsquo;S LOUD",
         deck="Arrived at 04:12, weighing 3,410 grams,<br>"
              "with strong opinions about sleep.",
         caption="The new arrival, minutes old and already unimpressed.",
         strap="INTRODUCING AMALIA ROSE",
         strap_2="BORN 9 FEBRUARY &nbsp;·&nbsp; 3,410 G &nbsp;·&nbsp; 51 CM",
         folio="PAGE ONE &nbsp;·&nbsp; THE DAILY BUNDLE &nbsp;·&nbsp; "
               "PRINTED WITH LOVE",
         inside_script="Welcome, little one",
         inside_headline="THE FIRST<br>FEW DAYS",
         photo_caption_1="Ten fingers, ten toes, and a full set of lungs.",
         column_title="A Small Person<br>Moves In",
         column_body="She arrived three days late and in a considerable hurry, "
                     "which we are told says everything about what comes next."
                     "<br><br>"
                     "We are tired, unwashed and completely, hopelessly taken "
                     "with her.<br><br>"
                     "Visitors are welcome once we have found the kettle. Please "
                     "text before you come, and bring food rather than flowers.",
         box_day="09", box_month="FEBRUARY",
         box_line_1="Amalia Rose",
         box_line_2="3,410 GRAMS &nbsp;·&nbsp; 51 CENTIMETRES &nbsp;·&nbsp; 04:12",
         box_line_3="DAUGHTER OF LENA AND TOM",
         folio_2="PAGE TWO &nbsp;·&nbsp; THE DAILY BUNDLE",
         classified_title="THE SMALL PRINT",
         classifieds=[
             ("THE NAME", "Amalia Rose",
              "Amalia after her great-grandmother. Rose because it suited her."),
             ("THE STATS", "3,410 g &amp; 51 cm",
              "Born at 04:12 on a Tuesday, after a long and dramatic night."),
             ("VISITING", "After the First Week",
              "Text first. We will almost certainly say yes, just not at dawn."),
             ("GIFTS", "Nappies, Honestly",
              "Or a meal. Nobody has cooked anything here since Sunday."),
             ("SLEEP", "Reports Are Mixed",
              "She sleeps beautifully between four and six in the afternoon."),
             ("THANK YOU", "To the Midwives",
              "Who were calm when we were not. We will not forget it."),
         ],
         classified_foot="With love from all three of us",
         notice_caption="Her first week, and our favourite photograph.",
         notice_head="Thank You<br>For the Love",
         notice_body="For the messages, the meals left on the doorstep and the "
                     "patience while we did not reply. It carried us through the "
                     "strangest, best weeks of our lives.",
         signature="LENA, TOM &amp; AMALIA",
         folio_3="THE DAILY BUNDLE &nbsp;·&nbsp; KEEPSAKE EDITION"),
]


def build(c):
    return document(c["title"], FAMILIES,
                    [p_front(c), p_inside(c), p_classifieds(c), p_notice(c)],
                    body_bg="#2E2C26")


if __name__ == "__main__":
    import pathlib
    out_dir = pathlib.Path(__file__).resolve().parent.parent / "dist"
    out_dir.mkdir(parents=True, exist_ok=True)
    for c in SUITES:
        out = out_dir / f"{c['file']}.html"
        out.write_text(build(c), encoding="utf-8")
        print(f"wrote {out.name} ({out.stat().st_size // 1024} KB)")
