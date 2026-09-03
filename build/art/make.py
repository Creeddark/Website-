#!/usr/bin/env python3
"""
VELORA — Illustrationsgenerator.

Erzeugt die Strichgrafiken der Website als SVG. Bewusst als Zeichnung und
nicht als Fotomontage: wir haben keine lizenzierten Fotos, und eine ehrliche
Zeichnung ist besser als ein erfundenes Bild.

Bildsprache: architektonische Aufrisszeichnung. Eine Grundlinie, flache
Frontalansicht, feine Linien, genau eine getönte Fläche je Motiv.

    python3 build/art/make.py
"""
from __future__ import annotations
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent.parent / "site" / "assets" / "img"
OUT.mkdir(parents=True, exist_ok=True)

# Palette — identisch zu den CSS-Tokens von VELORA
DARK_BG   = "#1A1A1A"
DARK_LINE = "#D8CDB8"      # warmes Elfenbein auf Charcoal
DARK_SOFT = "#6E6455"
LIGHT_BG  = "#F5EFE6"
LIGHT_LINE= "#4A4238"      # warmes Dunkelbraun statt Neutralschwarz
LIGHT_SOFT= "#AFA99E"

SEG = {
    "ferien":     "#A55E3E", "hotels":  "#49637F",
    "camping":    "#5A7147", "events": "#895367",
    "verwaltung": "#796954", "seminar": "#8D6B23",
    "brand":      "#D4AF37",
}

def svg(w, h, body, bg, title, fit="slice"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="100%" height="100%" preserveAspectRatio="xMidYMid slice" '
            f'role="img" aria-label="{title}">'
            f'<rect width="{w}" height="{h}" fill="{bg}"/>{body}</svg>')

def g(stroke, sw=2.4, fill="none", extra=""):
    return (f'<g fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" {extra}>')

# ---------- Primitive ------------------------------------------------------

def ground(y, x0, x1):
    return f'<path d="M{x0} {y}H{x1}"/>'

def house(x, y, w, h, roof=70):
    """Giebelhaus mit Tür und Fenstern. y = Grundlinie."""
    t = y - h
    d = f'<path d="M{x} {y}V{t}h{w}v{h}"/>'
    d += f'<path d="M{x-16} {t}L{x+w/2} {t-roof}L{x+w+16} {t}"/>'
    dw, dh = 34, 62
    dx = x + w/2 - dw/2
    d += f'<path d="M{dx} {y}v{-dh}h{dw}v{dh}"/>'
    for wx in (x + 26, x + w - 26 - 30):
        d += f'<rect x="{wx}" y="{t+28}" width="30" height="30"/>'
    return d

def block(x, y, w, h, cols=4, rows=4):
    """Mehrgeschossiges Gebäude mit Fensterraster."""
    t = y - h
    d = f'<path d="M{x} {y}V{t}h{w}v{h}"/>'
    ww, wh = 22, 26
    gx = (w - cols*ww) / (cols + 1)
    gy = (h - 70 - rows*wh) / (rows + 1)
    for r in range(rows):
        for c in range(cols):
            wx = x + gx + c*(ww+gx)
            wy = t + gy + r*(wh+gy)
            d += f'<rect x="{wx:.1f}" y="{wy:.1f}" width="{ww}" height="{wh}"/>'
    d += f'<path d="M{x+w/2-24} {y}v-56h48v56"/>'
    return d

def tent(x, y, w, h):
    return (f'<path d="M{x} {y}L{x+w/2} {y-h}L{x+w} {y}Z"/>'
            f'<path d="M{x+w/2} {y-h}V{y}"/>'
            f'<path d="M{x+w*0.32} {y}l{w*0.18} {-h*0.46}l{w*0.18} {h*0.46}"/>')

def tree(x, y, h):
    """Stamm mit gerundeter Krone — Dreiecke lasen sich als Pfeil."""
    r = h * 0.30
    cy = y - h * 0.62
    return (f'<path d="M{x} {y}v{-h*0.40:.0f}"/>'
            f'<path d="M{x-r*0.55:.0f} {y-h*0.34:.0f}'
            f'q{-r*0.55:.0f} {-r*0.30:.0f} {r*0.10:.0f} {-r*0.75:.0f}'
            f'q{r*0.25:.0f} {-r*0.70:.0f} {r*0.90:.0f} {-r*0.55:.0f}'
            f'q{r*0.85:.0f} {-r*0.10:.0f} {r*0.75:.0f} {r*0.62:.0f}'
            f'q{r*0.40:.0f} {r*0.45:.0f} {-r*0.35:.0f} {r*0.68:.0f}Z"/>'
            f'<path d="M{x} {y-h*0.40:.0f}l{-r*0.34:.0f} {-r*0.30:.0f}"/>')

def pavilion(x, y, w, h):
    t = y - h
    d = f'<path d="M{x} {y}V{t+40}"/><path d="M{x+w} {y}V{t+40}"/>'
    d += f'<path d="M{x-18} {t+40}L{x+w/2} {t}L{x+w+18} {t+40}Z"/>'
    d += f'<path d="M{x-18} {t+40}h{w+36}"/>'
    return d

def table(x, y, w=110, h=42):
    d = f'<path d="M{x} {y-h}h{w}"/>'
    d += f'<path d="M{x+10} {y-h}v{h}"/><path d="M{x+w-10} {y-h}v{h}"/>'
    return d

def chairs_u(x, y, w):
    """Stuhlreihe im Aufriss: Sitzfläche, Lehne, Beine."""
    d = ""
    n = 5
    cw = 62
    step = (w - cw) / (n - 1)
    for i in range(n):
        cx = x + i*step
        d += f'<path d="M{cx:.0f} {y}v-44h{cw}v44"/>'          # Sitz
        d += f'<path d="M{cx:.0f} {y-44}v-52h10v52"/>'          # Lehne
        d += f'<path d="M{cx:.0f} {y-44}h{cw}"/>'
    return d

def phone(x, y, w=190, h=380, screen=""):
    r = 22
    d = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/>'
         f'<rect x="{x+11}" y="{y+11}" width="{w-22}" height="{h-22}" rx="{r-9}"/>'
         f'<path d="M{x+w/2-22} {y+22}h44"/>')
    return d + screen

def screen_lines(x, y, w, h, seg_fill):
    """Inhalt im Telefon: Bildfläche + Textzeilen."""
    ix, iy, iw = x + 22, y + 34, w - 44
    d = f'<rect x="{ix}" y="{iy}" width="{iw}" height="{h*0.30:.0f}" fill="{seg_fill}" stroke="none" opacity="0.55"/>'
    d += f'<rect x="{ix}" y="{iy}" width="{iw}" height="{h*0.30:.0f}"/>'
    ty = iy + h*0.30 + 26
    for i, frac in enumerate([0.82, 0.62, 0.94, 0.70, 0.88, 0.55]):
        d += f'<path d="M{ix} {ty + i*22}h{iw*frac:.0f}"/>'
    return d

def qr_sign(x, y, s=86, post=64):
    """Aufsteller mit QR-Symbol."""
    d = f'<path d="M{x+s/2} {y}v{-post}"/>'
    top = y - post - s
    d += f'<rect x="{x}" y="{top}" width="{s}" height="{s}" rx="4"/>'
    m = s/9
    for (cx, cy) in [(1,1), (6,1), (1,6)]:
        d += (f'<rect x="{x+cx*m:.1f}" y="{top+cy*m:.1f}" width="{2*m:.1f}" height="{2*m:.1f}"/>')
    for (cx, cy) in [(5,5),(7,5),(5,7),(6,6),(7,7),(4,6)]:
        d += f'<rect x="{x+cx*m:.1f}" y="{top+cy*m:.1f}" width="{m*0.8:.1f}" height="{m*0.8:.1f}" stroke="none" fill="currentColor"/>'
    return d

def barrier(x, y, w=150):
    return (f'<path d="M{x} {y}v-70"/><path d="M{x} {y-58}h{w}"/>'
            f'<path d="M{x+30} {y-58}v-14M{x+70} {y-58}v-14M{x+110} {y-58}v-14"/>')

def letterboxes(x, y, w=120, h=90):
    d = f'<rect x="{x}" y="{y-h}" width="{w}" height="{h}"/>'
    for r in range(3):
        d += f'<path d="M{x} {y-h+ (r+1)*h/3:.1f}h{w}"/>'
    d += f'<path d="M{x+w/2} {y-h}v{h}"/>'
    return d


# ---------- Szenen ---------------------------------------------------------

W, H = 1600, 900          # Hero / Cover
DW, DH = 1200, 800        # Detailvignette 3:2

def hero_scene(inner, seg, title, shift=0):
    """Dunkler Aufriss mit Grundlinie. currentColor -> Linienfarbe.

    shift verschiebt das Motiv nach rechts, damit die Textspalte links
    frei bleibt. Die Grundlinie wird separat über die volle Breite gezogen.
    """
    inner = f'<g transform="translate({shift},0)">{inner}</g>' if shift else inner
    body = g(DARK_LINE, 2.6) + ground(700, 0, W) + inner + "</g>"
    body = body.replace("currentColor", DARK_LINE)
    return svg(W, H, body, DARK_BG, title)

def light_scene(inner, title, w=DW, h=DH, sw=2.6, fit="slice"):
    body = g(LIGHT_LINE, sw) + inner + "</g>"
    body = body.replace("currentColor", LIGHT_LINE)
    return svg(w, h, body, LIGHT_BG, title, fit)


def make_hero_home():
    """Ein Produkt, viele Orte — die Kernaussage als Bild.

    Linke 400 px bleiben frei: dort steht auf der Startseite die Headline.
    """
    y = 700
    s  = house(430, y, 205, 175)
    s += qr_sign(575, y, 50, 38)
    s += block(700, y, 190, 290, cols=4, rows=5)
    s += qr_sign(840, y, 50, 38)
    s += tent(950, y, 170, 140)
    s += qr_sign(1075, y, 50, 38)
    s += tree(1185, y, 200)
    scr = screen_lines(1300, 300, 185, 375, SEG["brand"])
    s += phone(1300, 300, 185, 375, scr)
    s += '<path d="M1235 440h48" stroke-dasharray="9 11"/>'
    return hero_scene(s, "brand", "Ferienhaus, Hotel, Campingplatz und Veranstaltung — überall derselbe QR-Code")


def make_hero_ferien():
    y = 700
    s = ""
    s += house(360, y, 380, 250, roof=110)
    s += qr_sign(770, y, 74, 60)
    s += tree(210, y, 250) + tree(1060, y, 220)
    s += f'<path d="M980 {y}h180" stroke-dasharray="8 14"/>'
    scr = screen_lines(1230, 250, 190, 380, SEG["ferien"])
    s += phone(1230, 250, 190, 380, scr)
    return hero_scene(s, "ferien", "Ferienhaus mit QR-Aufsteller und Gästeseite", 150)


def make_hero_hotels():
    y = 700
    s = ""
    s += block(300, y, 480, 470, cols=6, rows=6)
    s += f'<path d="M{300+480/2-90} {y-72}h180v22h-180Z"/>'   # Vordach
    s += qr_sign(830, y, 74, 60)
    s += tree(180, y, 200)
    scr = screen_lines(1200, 270, 190, 380, SEG["hotels"])
    s += phone(1200, 270, 190, 380, scr)
    return hero_scene(s, "hotels", "Hotelfassade mit digitalem Gästeportal", 160)


def make_hero_camping():
    y = 700
    s = ""
    s += tent(210, y, 220, 180) + tent(470, y, 175, 145)
    s += tree(700, y, 280) + tree(830, y, 210)
    s += block(940, y, 200, 140, cols=3, rows=1)      # Sanitärhaus
    s += barrier(150, y, 130)
    s += qr_sign(1180, y, 74, 60)
    scr = screen_lines(1310, 260, 190, 380, SEG["camping"])
    s += phone(1310, 260, 190, 380, scr)
    return hero_scene(s, "camping", "Campingplatz mit Schranke, Sanitärhaus und QR-Aufsteller", 60)


def make_hero_events():
    y = 700
    s = ""
    s += pavilion(300, y, 520, 300)
    for i in range(3):
        s += table(360 + i*160, y, 120, 48)
    # Lichterkette
    s += '<path d="M240 380q300 120 600 0" stroke-dasharray="2 26"/>'
    s += qr_sign(880, y, 74, 60)
    s += tree(180, y, 230)
    scr = screen_lines(1230, 250, 190, 380, SEG["events"])
    s += phone(1230, 250, 190, 380, scr)
    return hero_scene(s, "events", "Festzelt mit Tischen und Eventseite", 150)


def make_hero_verwaltung():
    y = 700
    s = ""
    s += block(320, y, 420, 500, cols=5, rows=7)
    s += letterboxes(790, y, 130, 100)
    s += qr_sign(960, y, 74, 60)
    s += tree(200, y, 210)
    scr = screen_lines(1230, 280, 190, 380, SEG["verwaltung"])
    s += phone(1230, 280, 190, 380, scr)
    return hero_scene(s, "verwaltung", "Mehrfamilienhaus mit Briefkästen und Hausinformation", 140)


def make_hero_seminar():
    y = 700
    s = ""
    # Raum als Aufriss: Fensterwand
    s += f'<path d="M280 {y}V300h560v{y-300}"/>'
    for i in range(4):
        s += f'<rect x="{320+i*135}" y="340" width="95" height="150"/>'
    s += chairs_u(340, y, 440)
    s += f'<path d="M560 {y-40}h0"/>'
    s += f'<rect x="880" y="330" width="150" height="105"/>'   # Flipchart
    s += f'<path d="M955 435v{y-435}"/><path d="M905 {y}h100"/>'
    s += qr_sign(1080, y, 74, 60)
    scr = screen_lines(1250, 260, 190, 380, SEG["seminar"])
    s += phone(1250, 260, 190, 380, scr)
    return hero_scene(s, "seminar", "Seminarraum mit Stuhlkreis und Teilnehmerseite", 130)


def make_produkt_uebersicht():
    """Bausteinsystem: aus Blöcken wird eine Seite."""
    s = ""
    names = ["Titel", "Text & Bild", "Zeitplan", "Info-Liste", "Orte", "Formular", "Kontakt"]
    for i, n in enumerate(names):
        yy = 70 + i*95
        s += f'<rect x="70" y="{yy}" width="330" height="70" rx="4"/>'
        s += (f'<text x="105" y="{yy+44}" font-family="Inter,sans-serif" font-size="26" '
              f'fill="{LIGHT_LINE}" stroke="none">{n}</text>')
        s += f'<rect x="76" y="{yy+6}" width="8" height="58" fill="{SEG["brand"]}" stroke="none"/>'
    s += '<path d="M440 400h120" stroke-dasharray="10 12"/>'
    s += '<path d="M540 385l24 15-24 15"/>'
    scr = screen_lines(620, 190, 240, 480, SEG["brand"])
    s += phone(620, 190, 240, 480, scr)
    s += (f'<text x="905" y="330" font-family="Fraunces,Georgia,serif" font-size="44" '
          f'fill="{LIGHT_LINE}" stroke="none">Eine Seite,</text>')
    s += (f'<text x="905" y="386" font-family="Fraunces,Georgia,serif" font-size="44" '
          f'fill="{LIGHT_LINE}" stroke="none">zusammengesetzt</text>')
    s += (f'<text x="905" y="442" font-family="Fraunces,Georgia,serif" font-size="44" '
          f'fill="{LIGHT_LINE}" stroke="none">aus Bausteinen.</text>')
    s += f'<path d="M905 480h300"/>'
    return light_scene(s, "Bausteine setzen sich zu einer Seite zusammen", 1400, 800, 2.4, "meet")


def make_produkt_technik():
    """Warum die Gastansicht auch bei Ausfall lädt."""
    s = ""
    def box(x, y, w, h, label, sub=""):
        d = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5"/>'
        d += (f'<text x="{x+w/2}" y="{y+h/2 - (6 if sub else -10)}" text-anchor="middle" '
              f'font-family="Inter,sans-serif" font-size="27" fill="{LIGHT_LINE}" stroke="none">{label}</text>')
        if sub:
            d += (f'<text x="{x+w/2}" y="{y+h/2+30}" text-anchor="middle" '
                  f'font-family="Inter,sans-serif" font-size="21" fill="{LIGHT_SOFT}" stroke="none">{sub}</text>')
        return d
    s += box(90, 40, 420, 118, "Sie ändern etwas", "im Editor")
    s += '<path d="M300 158v58"/><path d="M285 202l15 16 15-16"/>'
    s += box(90, 226, 420, 118, "Seite wird erzeugt", "einmal, nicht bei jedem Aufruf")
    s += '<path d="M300 344v58"/><path d="M285 388l15 16 15-16"/>'
    s += f'<rect x="90" y="412" width="420" height="118" rx="5" fill="{SEG["brand"]}" opacity="0.14" stroke="none"/>'
    s += box(90, 412, 420, 118, "Auslieferung über CDN", "keine Datenbank im Leseweg")
    s += '<path d="M300 530v58"/><path d="M285 574l15 16 15-16"/>'
    s += box(90, 598, 420, 118, "Gast sieht die Seite", "unter einer Sekunde")
    return light_scene(s, "Vom Editor über das CDN zur Gastansicht", 600, 750, 2.2, "meet")


def make_app_welcome():
    scr = screen_lines(0, 0, 300, 420, SEG["ferien"])
    s = f'<g transform="translate(30,40)">{scr}</g>'
    return light_scene(s, "Gastansicht auf dem Telefon", 360, 500, 2.2)


# ---------- Detailvignetten ------------------------------------------------

def vignette(inner, title):
    return light_scene(inner, title, DW, DH, 2.8)

def make_entrance():
    y = 640
    s  = ground(y, 80, DW-80)
    s += f'<path d="M330 {y}V240h250v{y-240}"/>'
    s += f'<path d="M400 {y}v-190h110v190"/>'          # Tür
    s += f'<circle cx="490" cy="{y-95}" r="7"/>'
    s += f'<rect x="640" y="{y-230}" width="90" height="120" rx="6"/>'  # Schlüsseltresor
    s += f'<path d="M660 {y-190}h50M660 {y-160}h50M660 {y-130}h50"/>'
    s += qr_sign(800, y, 80, 70)
    s += tree(200, y, 260)
    return vignette(s, "Hauseingang mit Schlüsseltresor und QR-Aufsteller")

def make_kitchen():
    y = 620
    s  = ground(y, 80, DW-80)
    s += f'<path d="M200 {y}v-160h700v160"/>'                       # Arbeitsplatte
    s += f'<path d="M200 {y-160}h700"/>'
    for x in (330, 470, 610, 750):
        s += f'<path d="M{x} {y}v-160"/>'
    s += f'<rect x="240" y="{y-140}" width="60" height="60"/>'      # Spülmaschine
    s += f'<circle cx="530" cy="{y-190}" r="18"/><circle cx="580" cy="{y-190}" r="18"/>'  # Kochfeld
    s += f'<path d="M480 {y-215}h150"/>'
    s += f'<rect x="380" y="200" width="420" height="140" rx="4"/>'  # Hängeschrank
    s += qr_sign(960, y, 70, 60)
    return vignette(s, "Küche mit Kochfeld, Geschirrspüler und QR-Code")

def make_living():
    y = 620
    s  = ground(y, 80, DW-80)
    # Sofa: Lehne, Sitz, zwei Armlehnen
    s += f'<path d="M250 {y}v-40"/><path d="M590 {y}v-40"/>'
    s += f'<path d="M250 {y-40}h340v-46h-340Z"/>'                    # Sitzfläche
    s += f'<path d="M262 {y-86}v-84h316v84"/>'                       # Rückenlehne
    s += f'<path d="M250 {y-86}v-56h24v56"/>'                        # Armlehne links
    s += f'<path d="M566 {y-86}v-56h24v56"/>'                        # Armlehne rechts
    s += f'<path d="M420 {y-170}v84"/>'                              # Kissennaht
    # Kamin mit Sims und Feuerraum
    s += f'<path d="M690 {y}v-250h190v250"/>'
    s += f'<path d="M672 {y-250}h226"/>'                             # Sims
    s += f'<path d="M726 {y}v-118h118v118"/>'
    s += f'<path d="M760 {y}q25 -60 50 0"/>'                         # Flamme
    s += f'<rect x="742" y="{y-232}" width="86" height="60"/>'       # Bild überm Kamin
    s += tree(1030, y, 210)
    return vignette(s, "Wohnbereich mit Sofa und Kamin")

def make_beach():
    y = 600
    s  = f'<path d="M80 {y}q220 -40 440 0t440 0t160 -20"/>'
    s += f'<path d="M80 {y+70}q260 -30 520 0t520 0"/>'
    for i, x in enumerate((260, 520, 800)):
        s += f'<path d="M{x} {y-10}q30 -70 60 0Z"/>'                 # Dünengras
    s += f'<circle cx="960" cy="230" r="70"/>'
    s += f'<path d="M300 {y-20}v-120M270 {y-140}h60v70h-60Z"/>'      # Strandkorb
    return vignette(s, "Strand mit Dünen und Strandkorb")

def make_exit():
    y = 620
    s  = ground(y, 80, DW-80)
    s += f'<path d="M300 {y}V260h300v{y-260}"/>'
    s += f'<path d="M380 {y}v-200h140v200"/>'
    s += f'<path d="M700 {y}v-150h180v150"/>'                        # Koffer
    s += f'<path d="M760 {y-150}v-40h60v40"/>'
    s += f'<path d="M700 {y-90}h180"/>'
    s += f'<path d="M960 {y-60}l40 -40 40 40" />'                    # Pfeil raus
    s += f'<path d="M1000 {y-100}v90"/>'
    return vignette(s, "Abreise: aufgeräumter Raum mit Koffer")

def make_host():
    y = 620
    s  = ground(y, 80, DW-80)
    s += f'<path d="M400 {y}V240h320v{y-240}"/>'
    s += f'<path d="M470 {y}v-200h130v200"/>'
    s += f'<circle cx="800" cy="{y-250}" r="42"/>'                   # Person
    s += f'<path d="M800 {y-208}v120M800 {y-88}l-40 88M800 {y-88}l40 88"/>'
    s += f'<path d="M800 {y-180}l-70 50M800 {y-180}l70 50"/>'
    s += tree(230, y, 240)
    return vignette(s, "Gastgeberin am Eingang")

def make_haus_eingang():
    y = 640
    s  = ground(y, 80, DW-80)
    s += f'<path d="M280 {y}V180h420v{y-180}"/>'
    s += f'<path d="M420 {y}v-210h140v210"/>'
    s += letterboxes(740, y, 150, 120)
    s += f'<rect x="740" y="{y-190}" width="150" height="50" rx="4"/>' # Klingeltableau
    s += qr_sign(960, y, 70, 60)
    return vignette(s, "Hauseingang mit Briefkästen und Klingeln")

def make_haus_hof():
    y = 640
    s  = ground(y, 80, DW-80)
    s += f'<path d="M120 {y}V220h180v{y-220}"/>'
    for i in range(4):
        x = 420 + i*130
        s += f'<rect x="{x}" y="{y-140}" width="100" height="140" rx="6"/>'
        s += f'<path d="M{x} {y-110}h100"/>'
    s += f'<path d="M400 {y-170}h550"/>'
    s += tree(1060, y, 230)
    return vignette(s, "Innenhof mit Mülltonnen")

def make_haus_flur():
    y = 660
    s  = ground(y, 80, DW-80)
    s += f'<path d="M240 {y}V150h520v{y-150}"/>'
    for i in range(6):
        s += f'<path d="M{300+i*30} {y - i*70}h180"/>'                # Treppe
        s += f'<path d="M{300+i*30} {y - i*70}v-70"/>'
    s += f'<rect x="820" y="240" width="130" height="230"/>'          # Fenster
    s += f'<path d="M885 240v230M820 355h130"/>'
    return vignette(s, "Treppenhaus mit Fenster")

def make_haus_keller():
    y = 640
    s  = ground(y, 80, DW-80)
    s += f'<path d="M180 {y}V200h840v{y-200}"/>'
    for i, x in enumerate((300, 470, 640)):
        s += f'<rect x="{x}" y="{y-150}" width="130" height="150" rx="4"/>'
        s += f'<circle cx="{x+65}" cy="{y-75}" r="34"/>'              # Waschmaschine
    s += f'<path d="M840 {y}v-220h120v220"/>'
    s += f'<path d="M840 {y-160}h120M840 {y-100}h120"/>'
    return vignette(s, "Waschküche mit Maschinen und Regal")

def make_haus_technik():
    y = 620
    s  = ground(y, 80, DW-80)
    s += f'<rect x="300" y="200" width="280" height="330" rx="6"/>'   # Zählerschrank
    for r in range(3):
        s += f'<rect x="340" y="{240+r*100}" width="200" height="70" rx="3"/>'
        s += f'<circle cx="380" cy="{275+r*100}" r="16"/>'
    s += f'<path d="M440 530v{y-530}"/>'
    s += f'<rect x="680" y="260" width="240" height="270" rx="6"/>'   # Heizung
    s += f'<path d="M720 320h160M720 370h160M720 420h160"/>'
    s += f'<path d="M800 530v{y-530}"/>'
    return vignette(s, "Zählerschrank und Heizungsanlage")

def make_event_map():
    s  = f'<rect x="90" y="70" width="{DW-180}" height="{DH-140}" rx="6"/>'
    s += f'<path d="M90 480q260 -120 520 -40t500 -110" stroke-dasharray="14 16"/>'  # Route
    s += f'<path d="M240 300q180 60 360 -20"/>'
    s += pavilion(720, 400, 220, 150)
    s += f'<circle cx="300" cy="520" r="16"/>'
    s += (f'<text x="300" y="580" text-anchor="middle" font-family="Inter,sans-serif" '
          f'font-size="26" fill="{LIGHT_SOFT}" stroke="none">Start</text>')
    s += (f'<text x="830" y="620" text-anchor="middle" font-family="Inter,sans-serif" '
          f'font-size="26" fill="{LIGHT_SOFT}" stroke="none">Gut Hohenstein</text>')
    s += f'<path d="M980 180h120M1040 120v120"/>'                     # Kompass
    return vignette(s, "Schematische Anfahrtskarte")


SCENES = {
    "hero-home": make_hero_home, "hero-ferien": make_hero_ferien,
    "hero-hotels": make_hero_hotels, "hero-camping": make_hero_camping,
    "hero-events": make_hero_events, "hero-verwaltung": make_hero_verwaltung,
    "hero-seminar": make_hero_seminar,
    "demo-guide-cover": make_hero_ferien, "demo-event-cover": make_hero_events,
    "demo-haus-cover": make_hero_verwaltung,
    "produkt-uebersicht": make_produkt_uebersicht, "produkt-technik": make_produkt_technik,
    "app-welcome": make_app_welcome,
    "demo-guide-entrance": make_entrance, "demo-guide-kitchen": make_kitchen,
    "demo-guide-living": make_living, "demo-guide-beach": make_beach,
    "demo-guide-exit": make_exit, "demo-guide-host": make_host,
    "demo-haus-eingang": make_haus_eingang, "demo-haus-hof": make_haus_hof,
    "demo-haus-flur": make_haus_flur, "demo-haus-keller": make_haus_keller,
    "demo-haus-technik": make_haus_technik, "demo-event-map": make_event_map,
    "about-portrait": make_entrance,
}

if __name__ == "__main__":
    total = 0
    for name, fn in SCENES.items():
        data = fn()
        (OUT / f"{name}.svg").write_text(data, encoding="utf-8")
        total += len(data)
        print(f"  {name:24} {len(data)/1024:5.1f} KB")
    print(f"\n{len(SCENES)} Illustrationen, {total/1024:.0f} KB gesamt.")
