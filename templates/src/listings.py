"""
Erzeugt die Etsy-Verkaufsbilder aus den gerenderten Vorlagen-Seiten.

Etsy zeigt das erste Bild quadratisch — deshalb 2000 x 2000 Bildpunkte.
Zwei Sorten je Suite:
  hero      eine gekippte Karte mit Schatten, dahinter die zweite Seite
  included  alle Seiten der Suite nebeneinander mit Beschriftung

Das Aufbau-HTML ist 1000 x 1000; gerendert wird mit Faktor 2.
"""

import pathlib
import re

BASE = pathlib.Path(__file__).resolve().parent.parent
PREV = BASE / "previews"
PREV_DEMO = BASE / "previews-demo"      # dieselben Seiten mit Beispielfoto
OUT = BASE / "listings"

SUITES = [
    dict(slug="01-wedding-ambra", badge_ink="#3A342B", name="AMBRA",
         kind="Wedding Invitation Suite",
         bg="linear-gradient(150deg,#EFE7DA 0%,#E4D8C6 55%,#D8C9B3 100%)",
         ink="#3A342B", accent="#A8823F", badge_bg="#FFFFFF"),
    dict(slug="02-birthday-confetti", badge_ink="#2A1550", name="CONFETTI",
         kind="Birthday Invitation Suite",
         bg="linear-gradient(150deg,#2A1550 0%,#3E1F63 55%,#5C2A78 100%)",
         ink="#FFF6E6", accent="#F3C75E", badge_bg="#FFF6E6"),
    dict(slug="03-gender-reveal", badge_ink="#3B3340", name="REVEAL",
         kind="Gender Reveal Suite",
         bg="linear-gradient(150deg,#FBE6EC 0%,#F6EDE6 50%,#E2EEF8 100%)",
         ink="#3B3340", accent="#CFA45F", badge_bg="#FFFFFF"),
    dict(slug="04-baby-shower", badge_ink="#39382F", name="OH BABY",
         kind="Baby Shower Suite",
         bg="linear-gradient(150deg,#EDF0E8 0%,#F3EDE2 55%,#E7DACB 100%)",
         ink="#39382F", accent="#C58A69", badge_bg="#FFFFFF"),
    dict(slug="05-christmas-noel", badge_ink="#0D2820", name="NO\u00cbL",
         kind="Christmas Invitation Suite",
         bg="linear-gradient(150deg,#0D2820 0%,#16412F 55%,#1E5038 100%)",
         ink="#F8F1E2", accent="#D9B369", badge_bg="#F8F1E2"),
    dict(slug="06-halloween-midnight", badge_ink="#141020", name="MIDNIGHT",
         kind="Halloween Party Suite",
         bg="linear-gradient(150deg,#0A0912 0%,#1B1428 55%,#2B1B3E 100%)",
         ink="#EDE6D6", accent="#FF7A29", badge_bg="#EDE6D6"),

    dict(slug="07-ornament-birthday", badge_ink="#2A1219", name="ORNEMENT",
         kind="Victorian Birthday Suite",
         bg="linear-gradient(150deg,#2A1219 0%,#3B1D23 55%,#4A252C 100%)",
         ink="#F2E7CE", accent="#D8B87E", badge_bg="#F2E7CE"),
    dict(slug="07-ornament-wedding", badge_ink="#0D211C", name="ORNEMENT",
         kind="Victorian Wedding Suite",
         bg="linear-gradient(150deg,#0D211C 0%,#153029 55%,#1D3E34 100%)",
         ink="#EFE6D2", accent="#D6B87C", badge_bg="#EFE6D2"),
    dict(slug="07-ornament-ivory", badge_ink="#33291E", name="ORNEMENT",
         kind="Ivory Wedding Suite",
         bg="linear-gradient(150deg,#F4EDE0 0%,#EAE0CD 55%,#DFD3BC 100%)",
         ink="#33291E", accent="#9C7A3C", badge_bg="#FFFFFF"),
    dict(slug="07-ornament-gothic", badge_ink="#0B0A12", name="ORNEMENT",
         kind="Gothic Night Suite",
         bg="linear-gradient(150deg,#0B0A12 0%,#14131E 55%,#1E1C2C 100%)",
         ink="#EAECF3", accent="#C3C6D4", badge_bg="#EAECF3"),

    dict(slug="08-times-birthday", badge_ink="#16150F", name="THE TIMES",
         kind="Birthday Newspaper Suite",
         bg="linear-gradient(150deg,#EFEADC 0%,#E6E0CF 55%,#D8D0B9 100%)",
         ink="#16150F", accent="#7A6E4E", badge_bg="#FFFFFF"),
    dict(slug="08-times-wedding", badge_ink="#16150F", name="THE TIMES",
         kind="Wedding Newspaper Suite",
         bg="linear-gradient(150deg,#EFEADC 0%,#E4DDCA 55%,#D3CAB2 100%)",
         ink="#16150F", accent="#7A6E4E", badge_bg="#FFFFFF"),
    dict(slug="08-times-baby", badge_ink="#16150F", name="THE TIMES",
         kind="Baby Announcement Suite",
         bg="linear-gradient(150deg,#EFEADC 0%,#E8E2D2 55%,#DAD3BE 100%)",
         ink="#16150F", accent="#7A6E4E", badge_bg="#FFFFFF"),

    dict(slug="09-ruban-birthday", badge_ink="#141414", name="RUBAN",
         kind="Coquette Birthday Suite",
         bg="linear-gradient(150deg,#FBFAF7 0%,#F1EFE9 55%,#E4E1D8 100%)",
         ink="#141414", accent="#8A8378", badge_bg="#FFFFFF"),
    dict(slug="09-ruban-bridal", badge_ink="#3A2A2A", name="RUBAN",
         kind="Bridal Shower Suite",
         bg="linear-gradient(150deg,#FDF8F6 0%,#F7EDE9 55%,#EEDFD8 100%)",
         ink="#3A2A2A", accent="#B87C7C", badge_bg="#FFFFFF"),
    dict(slug="09-ruban-baby", badge_ink="#2C332A", name="RUBAN",
         kind="Baby Shower Suite",
         bg="linear-gradient(150deg,#FAFBF7 0%,#EFF2EA 55%,#E1E7DA 100%)",
         ink="#2C332A", accent="#7C8B70", badge_bg="#FFFFFF"),

    dict(slug="10-cover-birthday", badge_ink="#12100F", name="COVER",
         kind="Birthday Magazine Suite",
         bg="linear-gradient(150deg,#12100F 0%,#232019 55%,#332E24 100%)",
         ink="#FBF7EF", accent="#E4C98E", badge_bg="#FBF7EF"),
    dict(slug="10-cover-wedding", badge_ink="#1A1214", name="COVER",
         kind="Wedding Magazine Suite",
         bg="linear-gradient(150deg,#1A1214 0%,#2C1F21 55%,#3D2B2C 100%)",
         ink="#FDF6F3", accent="#E8B7B0", badge_bg="#FDF6F3"),
]


def pages_of(slug, demo=True):
    """Seiten einer Suite. Wo es eine Fassung mit eingesetztem Beispielfoto
    gibt, gewinnt sie — im Verkaufsbild soll kein grauer Kasten stehen."""
    plain = sorted(PREV.glob(f"{slug}-*.png"))
    if not demo:
        return plain
    return [(PREV_DEMO / f.name) if (PREV_DEMO / f.name).exists() else f
            for f in plain]


def has_photo(slug):
    return bool(list(PREV_DEMO.glob(f"{slug}-*.png")))


CSS = """
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#222;font-family:'Montserrat',system-ui,sans-serif;}
.sheet{position:relative;width:1000px;height:1000px;overflow:hidden;}
.sheet .surface{position:absolute;inset:0;}
/* feines Rauschen nimmt der Flaeche das Digitale */
.grain{position:absolute;inset:0;opacity:.5;
  background-image:url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='140' height='140'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='4'/><feColorMatrix type='saturate' values='0'/><feComponentTransfer><feFuncA type='linear' slope='.07'/></feComponentTransfer></filter><rect width='140' height='140' filter='url(%23n)'/></svg>");}
.card{position:absolute;border-radius:3px;
  box-shadow:0 34px 70px rgba(0,0,0,.34),0 8px 18px rgba(0,0,0,.2);}
.label{position:absolute;letter-spacing:.30em;text-transform:uppercase;}
.badge{position:absolute;display:flex;align-items:center;gap:9px;
  padding:11px 20px;border-radius:100px;letter-spacing:.20em;
  font-size:14px;font-weight:600;text-transform:uppercase;}
.grid{position:absolute;display:flex;gap:26px;align-items:flex-start;}
.grid figure{margin:0;text-align:center;}
.grid img{display:block;border-radius:2px;
  box-shadow:0 18px 38px rgba(0,0,0,.3),0 4px 9px rgba(0,0,0,.16);}
.grid figcaption{margin-top:15px;font-size:13px;letter-spacing:.22em;
  text-transform:uppercase;font-weight:500;}
.rule{position:absolute;height:1px;}
/* --- Ablaufblatt --------------------------------------------------- */
.step{position:absolute;display:flex;gap:26px;align-items:flex-start;}
.step .num{flex:0 0 62px;height:62px;border-radius:50%;display:flex;
  align-items:center;justify-content:center;font-family:'Playfair Display',serif;
  font-size:27px;border:1.5px solid currentColor;}
.step h3{font-family:'Playfair Display',Georgia,serif;font-size:34px;
  font-weight:400;line-height:1.2;margin-bottom:9px;}
.step p{font-size:16px;line-height:1.62;font-weight:400;}
/* --- Vorher/Nachher ------------------------------------------------ */
.pair{position:absolute;display:flex;gap:56px;align-items:center;}
.pair figure{margin:0;text-align:center;}
.pair figcaption{margin-top:18px;font-size:13px;letter-spacing:.24em;
  text-transform:uppercase;font-weight:500;}
.arrow{display:flex;flex-direction:column;align-items:center;gap:10px;
  margin-top:-30px;}
"""


def hero(s):
    pages = pages_of(s["slug"])
    front, back = pages[0], (pages[1] if len(pages) > 1 else pages[0])
    count = f"{len(pages)} CARDS"
    return f"""
<div class="sheet" data-name="{s['slug']}-1-hero">
  <div class="surface" style="background:{s['bg']}"></div>
  <div class="grain"></div>

  <img class="card" src="file://{back}"
       style="width:330px;left:530px;top:214px;transform:rotate(7.5deg);opacity:.97">
  <img class="card" src="file://{front}"
       style="width:392px;left:196px;top:172px;transform:rotate(-4deg)">

  <div class="label" style="left:0;top:66px;width:1000px;text-align:center;
       font-size:15px;color:{s['ink']};opacity:.62;font-weight:500">
    {s['kind']}
  </div>
  <div style="position:absolute;left:0;top:96px;width:1000px;text-align:center;
       font-family:'Playfair Display',Georgia,serif;font-size:74px;
       color:{s['ink']};letter-spacing:.03em;line-height:1.1">{s['name']}</div>
  <div class="rule" style="left:440px;top:196px;width:120px;
       background:{s['accent']};opacity:.85"></div>

  <div class="badge" style="left:70px;bottom:72px;background:{s['badge_bg']};
       color:{s['badge_ink']}">Editable in Canva</div>
  <div class="badge" style="left:330px;bottom:72px;
       background:transparent;border:1.5px solid {s['accent']};
       color:{s['accent']}">{count}</div>
  <div class="badge" style="left:520px;bottom:72px;
       background:transparent;border:1.5px solid {s['accent']};
       color:{s['accent']}">Print &amp; Digital</div>
</div>"""


def included(s):
    pages = pages_of(s["slug"])
    n = len(pages)
    # Die Karten bekommen den Platz, der zwischen Kopfzeile und Fusszeile
    # tatsaechlich frei ist, statt an einer festen Hoehe zu kleben.
    card_w = 216 if n >= 4 else 262
    gap = 20
    card_h = card_w * 1050 / 750
    block_h = card_h + 15 + 16
    top = 246 + (900 - 246 - block_h) / 2
    cells = ""
    for p in pages:
        # Dateiname ist <slug>-<nr>-<name>; nur der Name gehoert unter das Bild.
        cap = re.sub(r"^.*?-\d+-", "", p.stem).replace("-", " ")
        cells += (f'<figure><img src="file://{p}" style="width:{card_w}px">'
                  f'<figcaption style="color:{s["ink"]};opacity:.72">{cap}</figcaption>'
                  f'</figure>')
    total_w = n * card_w + (n - 1) * gap
    left = (1000 - total_w) / 2
    return f"""
<div class="sheet" data-name="{s['slug']}-2-included">
  <div class="surface" style="background:{s['bg']}"></div>
  <div class="grain"></div>
  <div class="label" style="left:0;top:96px;width:1000px;text-align:center;
       font-size:14px;color:{s['ink']};opacity:.6;font-weight:500">What you get</div>
  <div style="position:absolute;left:0;top:126px;width:1000px;text-align:center;
       font-family:'Playfair Display',Georgia,serif;font-size:56px;
       color:{s['ink']};letter-spacing:.02em">{s['name']}</div>
  <div class="rule" style="left:440px;top:214px;width:120px;
       background:{s['accent']};opacity:.85"></div>
  <div class="grid" style="left:{left:.0f}px;top:{top:.0f}px;gap:{gap}px">{cells}</div>
  <div class="badge" style="left:0;bottom:78px;width:1000px;justify-content:center;
       background:transparent;color:{s['ink']};opacity:.72;font-size:13px">
    5 &times; 7 in &nbsp;·&nbsp; 300 DPI &nbsp;·&nbsp; Fully editable in Canva
  </div>
</div>"""


STEPS = [
    ("Buy and download",
     "You receive a PDF straight away. Inside is your personal link to the "
     "template &mdash; nothing to unzip, nothing to install."),
    ("Open it in Canva",
     "A free Canva account is all you need. Click &ldquo;Use template&rdquo; "
     "and Canva makes a private copy that is yours to change."),
    ("Type over the text, print it",
     "Names, dates, colours, fonts &mdash; everything is editable. Then "
     "download as PDF for the printer, or as PNG to send by message."),
]


def how(s):
    """Drittes Verkaufsbild: der Ablauf.

    Auf Etsy ist die haeufigste unausgesprochene Frage bei einer digitalen
    Vorlage nicht "gefaellt sie mir", sondern "kriege ich das hin". Dieses
    Bild beantwortet sie, bevor sie gestellt wird.
    """
    rows = ""
    for i, (title, body) in enumerate(STEPS):
        rows += f"""
  <div class="step" style="left:112px;top:{330 + i * 186}px;width:776px;
       color:{s['ink']}">
    <div class="num" style="color:{s['accent']}">{i + 1}</div>
    <div><h3 style="color:{s['ink']}">{title}</h3>
         <p style="color:{s['ink']};opacity:.74">{body}</p></div>
  </div>"""
    return f"""
<div class="sheet" data-name="{s['slug']}-3-how-it-works">
  <div class="surface" style="background:{s['bg']}"></div>
  <div class="grain"></div>
  <div class="label" style="left:0;top:108px;width:1000px;text-align:center;
       font-size:14px;color:{s['ink']};opacity:.6;font-weight:500">How it works</div>
  <div style="position:absolute;left:0;top:138px;width:1000px;text-align:center;
       font-family:'Playfair Display',Georgia,serif;font-size:60px;
       color:{s['ink']};letter-spacing:.02em">Three steps</div>
  <div class="rule" style="left:440px;top:246px;width:120px;
       background:{s['accent']};opacity:.85"></div>
  {rows}
  <div class="badge" style="left:0;bottom:80px;width:1000px;justify-content:center;
       background:transparent;color:{s['ink']};opacity:.7;font-size:13px">
    Works on phone, tablet or computer &nbsp;·&nbsp; No software to install
  </div>
</div>"""


def photo_sheet(s):
    """Viertes Verkaufsbild, nur fuer Suiten mit Bildfenster: derselbe
    Entwurf einmal leer und einmal mit Foto. Das ist die Frage, die bei
    Fotovorlagen sonst per Nachricht kommt."""
    empty = pages_of(s["slug"], demo=False)[0]
    filled = pages_of(s["slug"])[0]
    return f"""
<div class="sheet" data-name="{s['slug']}-4-your-photo">
  <div class="surface" style="background:{s['bg']}"></div>
  <div class="grain"></div>
  <div class="label" style="left:0;top:104px;width:1000px;text-align:center;
       font-size:14px;color:{s['ink']};opacity:.6;font-weight:500">
    Add your own photo</div>
  <div style="position:absolute;left:0;top:134px;width:1000px;text-align:center;
       font-family:'Playfair Display',Georgia,serif;font-size:58px;
       color:{s['ink']};letter-spacing:.02em">Drop it in. It fits.</div>
  <div class="rule" style="left:440px;top:240px;width:120px;
       background:{s['accent']};opacity:.85"></div>

  <div class="pair" style="left:118px;top:300px">
    <figure><img class="card" src="file://{empty}" style="width:340px;
        position:static;display:block">
      <figcaption style="color:{s['ink']};opacity:.7">The template</figcaption>
    </figure>
    <div class="arrow" style="color:{s['accent']}">
      <svg width="66" height="26" viewBox="0 0 66 26">
        <path d="M0,13 H58 M48,4 L60,13 L48,22" fill="none"
              stroke="currentColor" stroke-width="1.6"/></svg>
      <span style="font-size:11px;letter-spacing:.22em;text-transform:uppercase;
            font-weight:500">Your photo</span>
    </div>
    <figure><img class="card" src="file://{filled}" style="width:340px;
        position:static;display:block">
      <figcaption style="color:{s['ink']};opacity:.7">Yours</figcaption>
    </figure>
  </div>

  <div class="badge" style="left:0;bottom:74px;width:1000px;justify-content:center;
       background:transparent;color:{s['ink']};opacity:.72;font-size:13px">
    Drag your picture onto the frame in Canva &mdash; it crops itself
  </div>
</div>"""


def build():
    from common import font_css
    sheets = ""
    for s in SUITES:
        sheets += hero(s) + included(s) + how(s)
        if has_photo(s["slug"]):
            sheets += photo_sheet(s)
    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Etsy listing images</title>
<style>
{font_css({"Playfair Display", "Montserrat"})}
{CSS}
</style></head>
<body>{sheets}</body></html>"""


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    out = BASE / "dist" / "_listings.html"
    out.write_text(build(), encoding="utf-8")
    print(f"wrote {out}")
