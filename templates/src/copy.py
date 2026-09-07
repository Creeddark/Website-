"""
Angebotstexte fuer Etsy: Titel, Tags und Beschreibung je Suite.

Etsys Grenzen sind hart und werden hier geprueft, nicht geschaetzt:
  Titel    hoechstens 140 Zeichen
  Tags     hoechstens 13 Stueck, jeder hoechstens 20 Zeichen inklusive
           Leerzeichen — daran scheitern die meisten Wunsch-Tags

Die Tags sind Suchbegriffe, keine Hashtags: Etsy hat kein Rautezeichen und
gewichtet die genaue Wortfolge. Darum stehen hier Mehrwortphrasen, wie
Kaeufer sie tippen ("wedding invite set"), und nicht einzelne Schlagworte.

Ein Teil der Tags wiederholt sich absichtlich ueber alle Angebote — das sind
die, die den Kauftyp beschreiben (canva template, instant download). Der Rest
ist je Suite verschieden, damit sich die Angebote nicht gegenseitig
Konkurrenz um dieselbe Suchanfrage machen.
"""

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

TITLE_MAX = 140
TAG_MAX = 20
TAG_COUNT = 13

# Der Ablauf ist bei allen Suiten gleich und steht darum nur einmal hier.
HOW = [
    "Open the link in the PDF — a free Canva account is all you need.",
    "Choose “Use template”. Canva makes a private copy that is yours; "
    "the original stays untouched.",
    "Type over the text. Names, dates, colours and fonts are all editable.",
    "Share → Download → PDF Print, then print at home or at any print shop.",
]

NOTE = ("Digital product — nothing is posted to you. Personal use only; "
        "please do not resell or share the template link.")

SPECS = "5 × 7 inches · 300 DPI · edits on phone, tablet or computer"


SUITES = [
    dict(
        slug="01-wedding-ambra", name="AMBRA",
        cards=["Invitation", "Order of Events", "RSVP card", "Thank you card"],
        title="Wedding Invitation Template Set, Editable in Canva | Printable "
              "Invite, Order of Events, RSVP & Thank You Card | Instant Download",
        what="A four-card wedding suite in warm ivory and gold, with a hand-drawn "
             "eucalyptus arch. Calm, classic, and quiet enough that your names "
             "are the loudest thing on the page.",
        tags=["wedding invitation", "wedding invite set", "editable invitation",
              "canva template", "printable invite", "rsvp card template",
              "wedding suite", "instant download", "elegant wedding",
              "diy wedding invite", "thank you card", "eucalyptus invite",
              "5x7 invitation"],
    ),
    dict(
        slug="02-birthday-confetti", name="CONFETTI",
        cards=["Invitation", "The Plan", "Thank you card"],
        title="Birthday Party Invitation Template, Editable in Canva | Confetti "
              "Invite, Party Plan & Thank You Card | Printable Instant Download",
        what="A three-card birthday set on deep violet with gold confetti and a "
             "balloon cluster. Grown-up rather than childish — it works for a "
             "thirtieth as well as a seventieth.",
        tags=["birthday invitation", "birthday invite", "party invitation",
              "canva template", "editable invitation", "printable invite",
              "instant download", "confetti invite", "adult birthday",
              "thank you card", "birthday party", "5x7 invitation",
              "diy invitation"],
    ),
    dict(
        slug="03-gender-reveal", name="REVEAL",
        cards=["Invitation", "Cast Your Vote", "It's a Girl / Boy",
               "Thank you card"],
        title="Gender Reveal Invitation Template, Editable in Canva | Invite, "
              "Voting Card, Announcement & Thank You | Printable Instant Download",
        what="A four-card gender reveal set in blush and sky. Includes a voting "
             "card for guests to pick a side and an announcement card you fill in "
             "on the day.",
        tags=["gender reveal", "gender reveal invite", "baby reveal invite",
              "boy or girl", "canva template", "editable invitation",
              "printable invite", "instant download", "reveal party",
              "voting card", "thank you card", "baby announcement",
              "5x7 invitation"],
    ),
    dict(
        slug="04-baby-shower", name="OH BABY",
        cards=["Invitation", "Advice card", "Guess the Baby game",
               "Thank you card"],
        title="Baby Shower Invitation Template Set, Editable in Canva | Invite, "
              "Advice Card, Shower Game & Thank You | Printable Instant Download",
        what="A four-card baby shower set in sage and warm clay, gender neutral "
             "throughout. Two of the cards are the games, so the afternoon plans "
             "itself.",
        tags=["baby shower invite", "baby shower", "shower invitation",
              "canva template", "editable invitation", "printable invite",
              "instant download", "advice for mom", "baby shower game",
              "gender neutral", "thank you card", "5x7 invitation",
              "diy invitation"],
    ),
    dict(
        slug="05-christmas-noel", name="NOËL",
        cards=["Invitation", "Dinner menu", "Christmas greeting"],
        title="Christmas Party Invitation Template, Editable in Canva | Holiday "
              "Invite, Dinner Menu & Christmas Card | Printable Instant Download",
        what="A three-card Christmas set in forest green and gold, with a pine "
             "garland and falling snow. The menu card turns a dinner into an "
             "occasion.",
        tags=["christmas invite", "christmas party", "holiday invitation",
              "dinner party menu", "canva template", "editable invitation",
              "printable invite", "instant download", "christmas card",
              "holiday party", "christmas dinner", "5x7 invitation",
              "festive invite"],
    ),
    dict(
        slug="06-halloween-midnight", name="MIDNIGHT",
        cards=["Invitation", "The Night (details)", "Thank you card"],
        title="Halloween Party Invitation Template, Editable in Canva | Spooky "
              "Invite, Details Card & Thank You | Printable Instant Download",
        what="A three-card Halloween set: bats across a full moon, bare branches, "
             "orange on near-black. Built for a grown-up party, not a children's "
             "one.",
        tags=["halloween invite", "halloween party", "spooky invitation",
              "party invitation", "canva template", "editable invitation",
              "printable invite", "instant download", "gothic invite",
              "adult halloween", "thank you card", "5x7 invitation",
              "bats and moon"],
    ),
    dict(
        slug="07-ornament-birthday", name="ORNEMENT · Birthday",
        cards=["Invitation", "Details", "RSVP card", "Thank you card"],
        title="Victorian Birthday Invitation Template, Editable in Canva | Ornate "
              "Invite, Details, RSVP & Thank You Card | Printable Instant Download",
        what="A four-card birthday suite in oxblood and antique gold, framed by "
             "engraved scrollwork drawn line by line. For a birthday that wants to "
             "feel like an event.",
        tags=["victorian invite", "birthday invitation", "ornate invitation",
              "vintage invitation", "canva template", "editable invitation",
              "printable invite", "instant download", "baroque invite",
              "gold invitation", "rsvp card", "thank you card",
              "5x7 invitation"],
    ),
    dict(
        slug="07-ornament-wedding", name="ORNEMENT · Wedding",
        cards=["Invitation", "Details", "RSVP card", "Thank you card"],
        title="Victorian Wedding Invitation Suite, Editable in Canva | Ornate "
              "Invite, Details, RSVP & Thank You Card | Printable Instant Download",
        what="A four-card wedding suite in deep emerald and gold, with engraved "
             "corners, a swan crest and a pearl border. Formal without being "
             "stiff.",
        tags=["victorian wedding", "wedding invitation", "ornate invitation",
              "vintage wedding", "canva template", "editable invitation",
              "printable invite", "instant download", "emerald wedding",
              "wedding suite", "rsvp card template", "gold invitation",
              "5x7 invitation"],
    ),
    dict(
        slug="07-ornament-ivory", name="ORNEMENT · Ivory",
        cards=["Invitation", "Details", "RSVP card", "Thank you card"],
        title="Ivory Wedding Invitation Suite, Editable in Canva | Classic Ornate "
              "Invite, Details, RSVP & Thank You Card | Printable Instant Download",
        what="The same engraved suite in ivory and soft gold — the version for a "
             "daytime wedding, a registry office or anyone who wants the "
             "ornament without the drama.",
        tags=["wedding invitation", "ivory invitation", "classic wedding",
              "ornate invitation", "canva template", "editable invitation",
              "printable invite", "instant download", "wedding suite",
              "formal invitation", "rsvp card template", "thank you card",
              "5x7 invitation"],
    ),
    dict(
        slug="07-ornament-gothic", name="ORNEMENT · Gothic",
        cards=["Invitation", "Details", "RSVP card", "Thank you card"],
        title="Gothic Wedding Invitation Suite, Editable in Canva | Dark Ornate "
              "Invite, Details, RSVP & Thank You Card | Printable Instant Download",
        what="The engraved suite in near-black and cold silver. Made for winter "
              "weddings, evening ceremonies and Halloween weddings that still want "
              "to look expensive.",
        tags=["gothic wedding", "gothic invitation", "dark wedding",
              "black invitation", "canva template", "editable invitation",
              "printable invite", "instant download", "moody wedding",
              "halloween wedding", "rsvp card template", "wedding suite",
              "5x7 invitation"],
    ),
    dict(
        slug="08-times-birthday", name="THE TIMES · Birthday",
        photo=True,
        cards=["Front page", "Inside page", "The Particulars",
               "Notice of Thanks"],
        title="Newspaper Birthday Invitation Template, Editable in Canva | Retro "
              "Front Page Invite with Your Photo, 4 Pages | Instant Download",
        what="A four-page birthday invitation laid out as a newspaper: blackletter "
             "masthead, a headline you write yourself, and a photo area you fill "
             "with your own picture.",
        tags=["newspaper invite", "birthday invitation", "retro invitation",
              "vintage newspaper", "photo invitation", "canva template",
              "editable invitation", "printable invite", "instant download",
              "40th birthday", "funny invitation", "newspaper template",
              "5x7 invitation"],
    ),
    dict(
        slug="08-times-wedding", name="THE TIMES · Wedding",
        photo=True,
        cards=["Front page", "Order of the day", "The Particulars",
               "Notice of Thanks"],
        title="Wedding Newspaper Invitation Template, Editable in Canva | Photo "
              "Front Page, Order of the Day, RSVP & Thanks | Instant Download",
        what="A four-page wedding invitation as a newspaper. Your photo runs "
             "across the front page, the order of the day sits inside, and the "
             "details read like classified ads.",
        tags=["wedding newspaper", "newspaper invite", "wedding invitation",
              "photo invitation", "vintage newspaper", "canva template",
              "editable invitation", "printable invite", "instant download",
              "wedding programme", "retro wedding", "wedding suite",
              "5x7 invitation"],
    ),
    dict(
        slug="08-times-baby", name="THE TIMES · Baby",
        photo=True,
        cards=["Front page", "The first few days", "The Particulars",
               "Notice of Thanks"],
        title="Newspaper Baby Announcement Template, Editable in Canva | Birth "
              "Announcement Front Page with Photo, 4 Pages | Instant Download",
        what="A four-page birth announcement as a newspaper front page. Weight, "
             "length, time of arrival and your photo — a keepsake as much as an "
             "announcement.",
        tags=["baby announcement", "birth announcement", "newspaper invite",
              "baby newspaper", "photo announcement", "canva template",
              "editable template", "printable card", "instant download",
              "newborn card", "baby keepsake", "vintage newspaper", "5x7 card"],
    ),
    dict(
        slug="09-ruban-birthday", name="RUBAN · Birthday",
        cards=["Invitation", "Details", "RSVP card", "Thank you card"],
        title="Coquette Birthday Invitation Template, Editable in Canva | Bow and "
              "Pearl Invite, Details, RSVP & Thank You | Instant Download",
        what="A four-card birthday suite in the coquette style: a single satin bow, "
             "a strand of pearls, a great deal of white space. Quiet, girlish and "
             "very current.",
        tags=["coquette invite", "bow invitation", "birthday invitation",
              "ribbon invitation", "canva template", "editable invitation",
              "printable invite", "instant download", "pearl invitation",
              "girly invitation", "soft aesthetic", "thank you card",
              "5x7 invitation"],
    ),
    dict(
        slug="09-ruban-bridal", name="RUBAN · Bridal",
        cards=["Invitation", "Details", "RSVP card", "Thank you card"],
        title="Bridal Shower Invitation Template, Editable in Canva | Coquette Bow "
              "Invite, Details, RSVP & Thank You Card | Instant Download",
        what="The coquette suite in dusty rose, for a bridal shower or hen party. "
             "Four cards, one bow, and room for everything the guests need to "
             "know.",
        tags=["bridal shower", "bridal shower invite", "coquette invite",
              "bow invitation", "hen party invite", "canva template",
              "editable invitation", "printable invite", "instant download",
              "ribbon invitation", "bride to be", "thank you card",
              "5x7 invitation"],
    ),
    dict(
        slug="09-ruban-baby", name="RUBAN · Baby",
        cards=["Invitation", "Details", "RSVP card", "Thank you card"],
        title="Baby Shower Invitation Template, Editable in Canva | Coquette Bow "
              "Invite, Details, RSVP & Thank You Card | Instant Download",
        what="The coquette suite in soft sage, gender neutral. Four cards with a "
             "single ribbon motif — the calm alternative to pastel cartoons.",
        tags=["baby shower invite", "coquette invite", "bow invitation",
              "baby shower", "canva template", "editable invitation",
              "printable invite", "instant download", "sage baby shower",
              "gender neutral", "ribbon invitation", "thank you card",
              "5x7 invitation"],
    ),
    dict(
        slug="10-cover-birthday", name="COVER · Birthday",
        photo=True,
        cards=["Magazine cover", "Feature page", "The Details", "Back cover"],
        title="Magazine Cover Birthday Invitation, Editable in Canva | Photo Cover, "
              "Feature Page, Details & Thanks, 4 Pages | Instant Download",
        what="A four-page birthday invitation built like a magazine: your photo "
             "full-bleed on the cover, the masthead running behind their head, a "
             "feature spread inside.",
        tags=["magazine invite", "magazine template", "birthday invitation",
              "photo invitation", "canva template", "editable invitation",
              "printable invite", "instant download", "magazine cover",
              "30th birthday", "custom magazine", "party invitation",
              "5x7 invitation"],
    ),
    dict(
        slug="10-cover-wedding", name="COVER · Wedding",
        photo=True,
        cards=["Magazine cover", "Cover story", "The Details", "Back cover"],
        title="Wedding Magazine Cover Invitation, Editable in Canva | Photo Cover, "
              "Cover Story, Details & Thanks, 4 Pages | Instant Download",
        what="A four-page wedding invitation as a magazine issue. Your photo "
             "carries the cover; inside, the story of how you met reads like an "
             "editorial.",
        tags=["wedding magazine", "magazine invite", "wedding invitation",
              "photo invitation", "magazine cover", "canva template",
              "editable invitation", "printable invite", "instant download",
              "modern wedding", "editorial wedding", "wedding suite",
              "5x7 invitation"],
    ),
]


def check():
    """Prueft gegen Etsys Grenzen. Ein zu langer Tag wird beim Einfuegen
    stillschweigend abgeschnitten — darum lieber hier auffallen."""
    problems = []
    for s in SUITES:
        if len(s["title"]) > TITLE_MAX:
            problems.append(f"{s['slug']}: Titel {len(s['title'])} Zeichen")
        if len(s["tags"]) != TAG_COUNT:
            problems.append(f"{s['slug']}: {len(s['tags'])} Tags")
        if len(set(s["tags"])) != len(s["tags"]):
            problems.append(f"{s['slug']}: doppelter Tag")
        for t in s["tags"]:
            if len(t) > TAG_MAX:
                problems.append(f"{s['slug']}: Tag „{t}“ {len(t)} Zeichen")
    return problems


def description(s):
    """Die Angebotsbeschreibung als fertiger Text zum Einfuegen."""
    photo_line = ("\n· A short video showing how to drop your own photo into "
                  "the design" if s.get("photo") else "")
    return (
        f"{s['what']}\n"
        f"\n"
        f"{SPECS}\n"
        f"\n"
        f"WHAT YOU GET\n"
        + "".join(f"· {c}\n" for c in s["cards"])
        + f"· A PDF with your personal Canva template link{photo_line}\n"
        f"\n"
        f"HOW IT WORKS\n"
        + "".join(f"{i + 1}. {h}\n" for i, h in enumerate(HOW))
        + f"\n{NOTE}\n")


def main():
    problems = check()
    for p in problems:
        print(f"  PROBLEM  {p}")
    data = [dict(slug=s["slug"], name=s["name"], title=s["title"],
                 tags=s["tags"], cards=s["cards"], photo=s.get("photo", False),
                 what=s["what"], description=description(s))
            for s in SUITES]
    out = ROOT / "listing-copy.json"
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False),
                   encoding="utf-8")
    longest = max(len(s["title"]) for s in SUITES)
    widest = max(len(t) for s in SUITES for t in s["tags"])
    print(f"{len(SUITES)} Angebote nach {out.name}")
    print(f"laengster Titel {longest}/{TITLE_MAX}, breitester Tag "
          f"{widest}/{TAG_MAX}, {len(problems)} Probleme")


if __name__ == "__main__":
    main()
