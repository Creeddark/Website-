#!/usr/bin/env python3
"""
Die Produktbilder fuer Etsy.

Zehn Quadrate, 2000 x 2000, gebaut aus den Telefonaufnahmen und den Schriften
der Einladung selbst. Etsy zeigt das erste in der Suche — es entscheidet, ob
jemand ueberhaupt klickt — und die uebrigen erst, wenn er drin ist.

    python3 build/etsy/aufnahmen.py          # Telefonaufnahmen
    bash    build/etsy/liste.sh              # die Liste des Paares
    python3 build/etsy/bilder.py https://eure-adresse.de

Ohne Adresse steht im QR-Code ein Platzhalter, und das Bild sagt das auch.
Sobald die Demo online ist, denselben Befehl mit der echten Adresse — dann
sind alle Bilder neu.
"""
from __future__ import annotations

import pathlib
import sys
import urllib.parse

import segno
from playwright.sync_api import sync_playwright

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from werkstatt import (KANTE, SIEGEL, bild, daten, ersetzen,  # noqa: E402
                       fon, kopf)

CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
ZIEL = pathlib.Path(__file__).resolve().parent / "bilder"
# Wie viel Schmuck der Code vertraegt, wurde nicht geschaetzt, sondern
# gemessen: bilder.py erzeugen, den Code aus dem fertigen Produktbild
# zurueckleseFn, das Bild dabei Schritt fuer Schritt verkleinern. Ergebnis am
# Beispiel simeah.netlify.app, Karte 540 Punkte im 2000er Bild:
#
#   Module rund 0,20   durchgehend lesbar ab 440 px   — kostenlos
#   Module rund 0,32   ab 840 px
#   Module rund 0,45   ab 1560 px                     — unbrauchbar
#   Ecken rund 0,6     ab 520 px                      — bezahlbar
#   Ecken rund 0,9     ab 1480 px                     — Abriss
#   Siegel 5 / 7 / 9   unveraendert
#
# Die Ecken sind die empfindliche Stelle: der Leser sucht dort das Verhaeltnis
# 1:1:3:1:1, und runde Ecken ziehen es diagonal zusammen. Genommen ist darum
# die vorsichtige Seite jeder Messung.
RUND = 0.20      # Rundung der einzelnen Module
ECKE = 0.6       # Rundung der drei Erkennungsmarken
LOCH = 7         # Module, die das Siegel in der Mitte verdeckt
PLATZHALTER = "https://eure-marke.de/demo"


def knapp(adresse: str) -> str:
    """Dieselbe Adresse, aber in moeglichst wenigen Zeichen fuer den Code.

    Schema und Rechnername sind gross- und kleinschreibungsblind (RFC 3986),
    ein Pfad ist es nicht. Hat die Adresse keinen Pfad, darf man sie also in
    Grossbuchstaben schreiben — dann faellt sie in den alphanumerischen
    Modus des QR-Codes statt in den Byte-Modus und braucht eine Version
    weniger: 29 statt 33 Module. Bei gleicher Druckgroesse sind die Kacheln
    damit ein Siebtel groesser, und der Code liest sich aus mehr Abstand und
    schraeger. Auf dem Bild steht die Adresse trotzdem klein geschrieben —
    lesen soll sie ein Mensch, scannen eine Kamera."""
    t = urllib.parse.urlsplit(adresse)
    if t.path in ("", "/") and not t.query and not t.fragment:
        return f"{t.scheme}://{t.netloc}".upper()
    return adresse


def qr(adresse: str, dunkel: str = "#1B150F") -> str:
    """Der QR-Code, von Hand gezeichnet.

    Ein Code von der Stange ist ein Raster harter schwarzer Quadrate. Neben
    einem Wachssiegel sieht das aus wie ein Paketaufkleber. Also werden die
    Module einzeln gesetzt: weich in den Ecken, in der Tinte der Einladung
    statt in Schwarz, und in der Mitte das Siegel.

    Das Siegel darf dort stehen, weil die Fehlerkorrektur auf H liegt — bis
    zu dreissig Prozent duerfen fehlen, es verdeckt knapp sechs. Der Rand von
    vier Modulen gehoert zum Code und nicht zum Layout; ohne ihn findet keine
    Kamera den Anfang.

    Wie weich die Formen sein duerfen, steht oben bei RUND, ECKE und LOCH —
    gemessen, nicht geschaetzt."""
    code = segno.make(knapp(adresse), error="h")
    m = [list(z) for z in code.matrix]
    n = len(m)
    rand = 4
    k = n + 2 * rand
    ecken = [(0, 0), (0, n - 7), (n - 7, 0)]
    von = (n - LOCH) // 2

    def in_ecke(y, x):
        return any(ey <= y < ey + 7 and ex <= x < ex + 7 for ey, ex in ecken)

    def in_mitte(y, x):
        return bool(LOCH) and von <= y < von + LOCH and von <= x < von + LOCH

    teile = [f'<rect x="{rand+x}" y="{rand+y}" width="1" height="1"'
             f' rx="{RUND}" fill="{dunkel}"/>'
             for y in range(n) for x in range(n)
             if m[y][x] and not in_ecke(y, x) and not in_mitte(y, x)]

    for ey, ex in ecken:
        X, Y = rand + ex, rand + ey
        teile.append(f'<rect x="{X}" y="{Y}" width="7" height="7"'
                     f' rx="{ECKE}" fill="{dunkel}"/>')
        teile.append(f'<rect x="{X+1}" y="{Y+1}" width="5" height="5"'
                     f' rx="{max(0, ECKE-0.6)}" fill="#FBF6EE"/>')
        teile.append(f'<rect x="{X+2}" y="{Y+2}" width="3" height="3"'
                     f' rx="{max(0, ECKE-1.0)}" fill="{dunkel}"/>')

    if LOCH:
        c = rand + n / 2
        sg = LOCH - 0.4
        teile.append(f'<rect x="{c-LOCH/2-0.3}" y="{c-LOCH/2-0.3}"'
                     f' width="{LOCH+0.6}" height="{LOCH+0.6}" rx="1.6"'
                     f' fill="#FBF6EE"/>')
        teile.append(f'<image href="{daten(SIEGEL)}" x="{c-sg/2}"'
                     f' y="{c-sg*549/512/2}" width="{sg}"'
                     f' height="{sg*549/512}"/>')

    return (f'<svg viewBox="0 0 {k} {k}" width="100%" height="100%">'
            f'<rect width="{k}" height="{k}" fill="#FBF6EE"/>'
            + "".join(teile) + "</svg>")


# ====================================================================== 01 ==
def b01_titel() -> str:
    """Das Vorschaubild. Es hat eine Aufgabe: dass jemand klickt.

    In der Etsy-Suche ist es dreihundert Punkte gross. Drei Telefone waeren
    dort ein grauer Fleck — also eines, gross, mit dem Siegel darauf, und
    daneben vier Worte."""
    return """
<div class="buehne nacht" style="flex-direction:row; align-items:center;
     gap:90px">
  <div class="spalte" style="flex:1">
    <p class="marke">Digitale Hochzeitseinladung</p>
    <h1 style="margin-top:44px; font-size:124px">
      Eure Gäste<br>öffnen einen<br>Umschlag.
    </h1>
    <p class="lede" style="margin-top:44px; font-size:36px; max-width:800px">
      Eine eigene Seite mit Wachssiegel, Film und Countdown — und einer
      Rückmeldung, die bei euch ankommt.
    </p>
    <p style="margin-top:56px; font-size:26px; letter-spacing:0.24em;
              text-transform:uppercase; color:var(--brass-lit)">
      89&thinsp;€ · in fünf Tagen fertig
    </p>
  </div>
  <div style="position:relative; width:880px; height:1330px; flex:none">
    <div style="position:absolute; right:0; top:0">@@fon_hero@@</div>
    <div style="position:absolute; left:0; bottom:0">@@fon_umschlag@@</div>
  </div>
</div>"""


# ====================================================================== 02 ==
def b02_mehr() -> str:
    return """
<div class="buehne papier">
  <p class="marke">Mehr als eine Einladung</p>
  <h2 style="margin-top:34px; max-width:1450px">
    Sie öffnet sich, sie läuft, sie antwortet.
  </h2>
  <div class="reihe schub" style="gap:44px; align-items:flex-start;
       justify-content:space-between">
    <div class="spalte">@@f1@@<p class="unter"><b>Umschlag</b>
      <span>Wachssiegel, Lasche in echtem 3D. Zwei Sekunden, die niemand
      vergisst.</span></p></div>
    <div class="spalte">@@f2@@<p class="unter"><b>Euer Film</b>
      <span>Fünf Sekunden in Schleife, stumm, hinter euren Namen.</span></p></div>
    <div class="spalte">@@f3@@<p class="unter"><b>Countdown</b>
      <span>Läuft mit, bis der Tag da ist.</span></p></div>
    <div class="spalte">@@f4@@<p class="unter"><b>Rückmeldung</b>
      <span>Zusage, Personenzahl, Essenswunsch — direkt zu euch.</span></p></div>
  </div>
</div>"""


# ====================================================================== 03 ==
def b03_demo(adresse: str, echt: bool) -> str:
    return """
<div class="buehne nacht">
  <p class="marke">Live-Demo</p>
  <h2 style="margin-top:34px; max-width:1400px">
    Probiert sie aus, bevor ihr bestellt.
  </h2>
  <div class="reihe" style="flex:1; align-items:center; gap:80px;
       margin-top:60px">
    <div class="spalte" style="align-items:center; flex:none">
      <div style="background:var(--paper); padding:36px; border-radius:20px;
                  width:540px; height:540px">@@qr@@</div>
      <p style="margin-top:32px; font-size:29px; letter-spacing:0.04em;
                color:var(--brass-lit); text-align:center; max-width:540px;
                word-break:break-all">@@adresse@@</p>
      @@hinweis@@
    </div>
    <div class="spalte" style="flex:1">
      <p style="font-size:46px; line-height:1.32; color:var(--on-night)">
        Scannt den Code mit der Kamera.
      </p>
      <p class="klein" style="margin-top:34px; font-size:30px">
        Ihr seht genau das, was eure Gäste sehen — den ganzen Weg vom Siegel
        bis zur Antwort. Nichts wird installiert, nichts gespeichert.
      </p>
    </div>
    @@fon@@
  </div>
</div>"""


# ====================================================================== 04 ==
def b04_gaeste() -> str:
    return """
<div class="buehne papier">
  <p class="marke">Was eure Gäste tun können</p>
  <h2 style="margin-top:34px; max-width:1300px">
    Ein Tippen genügt.
  </h2>
  <div class="reihe" style="gap:80px; align-items:center; flex:1;
       margin-top:70px">
    <div class="spalte" style="flex:1; gap:50px">
      @@punkte@@
    </div>
    <div class="reihe" style="gap:44px; align-items:center; flex:none">
      @@f1@@ @@f2@@
    </div>
  </div>
</div>"""


def punkt(titel: str, text: str) -> str:
    return f"""
      <div style="display:grid; grid-template-columns:22px 1fr; gap:0 30px;
                  align-items:baseline">
        <span style="width:11px; height:11px; border-radius:50%;
                     background:var(--brass); display:block"></span>
        <div>
          <b style="font-size:35px; font-weight:500">{titel}</b>
          <p class="klein" style="margin-top:10px; font-size:28px">{text}</p>
        </div>
      </div>"""


# ====================================================================== 05 ==
def b05_liste() -> str:
    return """
<div class="buehne papier">
  <p class="marke">Was nur ihr seht</p>
  <h2 style="margin-top:34px; max-width:1400px">
    Und ihr wisst, wer kommt.
  </h2>
  <p class="lede" style="margin-top:32px; max-width:1400px; font-size:34px">
    Jede Antwort steht Sekunden später in eurer Liste. Nur ihr könnt sie
    öffnen — mit einem Link und einem Zugangswort, die sonst niemand hat.
  </p>
  <div class="schub" style="margin-top:70px">
    <div style="border:1px solid var(--line); border-radius:14px;
                overflow:hidden; box-shadow:0 40px 80px rgba(36,31,24,0.14)">
      <img src="@@liste@@" alt="" style="width:100%; display:block">
    </div>
    <p class="klein" style="margin-top:34px; text-align:center">
      Beispieldaten · Ein Knopf lädt alles als Tabelle für Excel oder Numbers
    </p>
  </div>
</div>"""


# ====================================================================== 06 ==
def b06_preis() -> str:
    return """
<div class="buehne nacht" style="justify-content:center; text-align:center;
     align-items:center">
  <p class="marke">Was es kostet</p>
  <p style="font-family:var(--ff-display); font-size:340px; line-height:1;
            margin-top:40px">89&thinsp;€</p>
  <p style="margin-top:24px; font-size:28px; letter-spacing:0.24em;
            text-transform:uppercase; color:var(--brass-lit)">
    einmalig · 18 Monate online</p>
  <p class="lede" style="margin-top:60px; max-width:1150px; font-size:38px;
            color:var(--on-night)">
    Fertig eingerichtet mit euren Namen, eurem Termin, euren Texten und euren
    Fotos. Änderungen in dieser Zeit kosten nichts.
  </p>
  <hr class="strich" style="margin:70px auto">
  <p style="font-family:var(--ff-display); font-size:56px; line-height:1.25;
            max-width:1200px">
    Ihr seht sie fertig,<br>bevor ihr zahlt.
  </p>
  <p class="klein" style="margin-top:46px; font-size:26px">
    Zweite Sprache enthalten · Eigene Domain 39 € · Verlängerung 12 Monate 19 €
  </p>
</div>"""


# ====================================================================== 07 ==
def b07_ablauf() -> str:
    return """
<div class="buehne papier">
  <p class="marke">So läuft es</p>
  <h2 style="margin-top:34px">In fünf Tagen steht sie.</h2>
  <div style="display:flex; flex-direction:column; gap:56px; flex:1;
       justify-content:center; margin-top:60px">
    @@schritte@@
  </div>
</div>"""


def schritt(nr: int, titel: str, text: str) -> str:
    return f"""
    <div style="display:grid; grid-template-columns:104px 1fr; gap:0 46px;
                align-items:start">
      <span style="width:104px; height:104px; border:1px solid var(--brass);
                   border-radius:50%; display:grid; place-items:center;
                   font-family:var(--ff-display); font-size:46px;
                   color:var(--brass)">{nr}</span>
      <div>
        <b style="font-size:44px; font-weight:500">{titel}</b>
        <p class="lede" style="margin-top:14px; font-size:32px">{text}</p>
      </div>
    </div>"""


# ====================================================================== 08 ==
def b08_eure() -> str:
    return """
<div class="buehne papier">
  <p class="marke">Ihr müsst nichts bauen</p>
  <h2 style="margin-top:34px; max-width:1300px">
    Ihr schickt uns eure Sachen.<br>Wir richten sie ein.
  </h2>
  <div class="reihe schub" style="gap:80px; align-items:center">
    <div class="spalte" style="flex:1; gap:38px">
      @@punkte@@
    </div>
    @@fon@@
  </div>
</div>"""


# ====================================================================== 09 ==
def b09_zwei() -> str:
    return """
<div class="buehne nacht">
  <p class="marke">Zwei Sprachen, ein Server</p>
  <h2 style="margin-top:34px; max-width:1300px">
    Ein Knopf schaltet um.
  </h2>
  <div class="reihe schub" style="gap:90px; align-items:center">
    <div class="reihe" style="gap:40px; align-items:center">
      @@f1@@ @@f2@@
    </div>
    <div class="spalte" style="flex:1; gap:40px">
      @@punkte@@
    </div>
  </div>
</div>"""


def punkt_dunkel(titel: str, text: str) -> str:
    return f"""
      <div>
        <b style="font-size:36px; font-weight:500; color:var(--on-night)">{titel}</b>
        <p class="klein" style="margin-top:12px; font-size:28px">{text}</p>
      </div>"""


# ====================================================================== 10 ==
def b10_ehrlich() -> str:
    return """
<div class="buehne papier">
  <p class="marke">Ehrlich dazu</p>
  <h2 style="margin-top:34px; max-width:1300px">Was sie nicht ist.</h2>
  <div style="display:flex; flex-direction:column; gap:56px; flex:1;
       justify-content:center; margin-top:60px">
    @@punkte@@
  </div>
  <p class="klein" style="font-size:29px;
     border-top:1px solid var(--line); padding-top:44px">
    Wer eine gedruckte Einladung für die Großeltern braucht, druckt sie
    zusätzlich. Das eine ersetzt das andere nicht.
  </p>
</div>"""


def punkt_nicht(titel: str, text: str) -> str:
    return f"""
      <div style="display:grid; grid-template-columns:26px 1fr; gap:0 32px;
                  align-items:baseline">
        <span style="display:block; width:26px; height:2px;
                     background:var(--brass); transform:translateY(-12px)"></span>
        <div>
          <b style="font-size:38px; font-weight:500">{titel}</b>
          <p class="lede" style="margin-top:12px; font-size:30px">{text}</p>
        </div>
      </div>"""


# ================================================================== bauen ==
def seiten(adresse: str, echt: bool) -> dict[str, str]:
    hinweis = "" if echt else (
        '<p style="margin-top:26px; font-size:24px; color:#B8724A;'
        ' text-align:center; max-width:640px">Platzhalter — mit der echten'
        ' Adresse neu erzeugen</p>')

    return {
        "01-titel": ersetzen(b01_titel(), {
            "fon_hero": fon("03-hero", 440),
            "fon_umschlag": fon("01-umschlag", 540),
        }),
        "02-mehr": ersetzen(b02_mehr(), {
            "f1": fon("02-oeffnet", 360),
            "f2": fon("03-hero", 360),
            "f3": fon("04-countdown", 360),
            "f4": fon("09-rsvp", 360),
        }),
        "03-demo": ersetzen(b03_demo(adresse, echt), {
            "qr": qr(adresse),
            "adresse": adresse.replace("https://", "").rstrip("/"),
            "hinweis": hinweis,
            "fon": fon("03-hero", 380),
        }),
        "04-gaeste": ersetzen(b04_gaeste(), {
            "f1": fon("08-ort", 500),
            "f2": fon("10-lupe", 500),
            "punkte": "".join([
                punkt("Umschlag öffnen",
                      "Ein Tippen aufs Siegel, und die Karte steigt heraus."),
                punkt("Weg zum Ort",
                      "Ein Tippen öffnet die Navigation. Kein Abtippen."),
                punkt("Termin in den Kalender",
                      "Mit Uhrzeit, Adresse und einem Wort zum Ablauf."),
                punkt("Fotos groß ansehen",
                      "Der Bilderstreifen läuft von selbst; antippen zeigt "
                      "ein Foto ganz."),
                punkt("Antworten",
                      "Zusage oder Absage, Personenzahl, Essenswunsch, "
                      "ein Gruß."),
            ]),
        }),
        "05-liste": ersetzen(b05_liste(), {"liste": bild("12-liste")}),
        "06-preis": b06_preis(),
        "07-ablauf": ersetzen(b07_ablauf(), {
            "schritte": "".join([
                schritt(1, "Ihr schreibt uns",
                        "Namen, Termin, Ort. Mehr braucht es für den Anfang "
                        "nicht."),
                schritt(2, "Wir schicken einen Fragebogen",
                        "Eure Geschichte, der Ablauf des Tages, was die Gäste "
                        "wissen müssen. Dazu ladet ihr eure Fotos hoch."),
                schritt(3, "Ihr seht sie, bevor ihr zahlt",
                        "Nach drei Werktagen bekommt ihr einen Link auf eure "
                        "fertige Einladung."),
                schritt(4, "Wir schalten sie frei",
                        "Ihr bekommt die Adresse zum Weitergeben und einen "
                        "eigenen Zugang zu den Rückmeldungen."),
            ]),
        }),
        "08-eure": ersetzen(b08_eure(), {
            "fon": fon("05-weg", 560),
            "punkte": "".join([
                punkt("Eure Namen und euer Termin",
                      "So, wie sie auf der Einladung stehen sollen."),
                punkt("Eure Geschichte",
                      "Drei bis vier Stationen. Jahr, Überschrift, zwei Sätze."),
                punkt("Der Ablauf des Tages",
                      "Uhrzeit, was passiert, ein Satz dazu."),
                punkt("Eure Fotos",
                      "Ein hochkantes Titelbild und drei bis fünf weitere. "
                      "Wenn ihr einen kurzen Film habt: her damit."),
                punkt("Wir bauen daraus die Seite",
                      "Ihr braucht kein Konto, keine Vorlage und kein "
                      "Programm."),
            ]),
        }),
        "09-zwei": ersetzen(b09_zwei(), {
            "f1": fon("07-ablauf", 470),
            "f2": fon("11-englisch", 470),
            "punkte": "".join([
                punkt_dunkel("Deutsch und Englisch",
                             "Ein Knopf schaltet um — auch die "
                             "Bildbeschreibungen."),
                punkt_dunkel("Server in Deutschland",
                             "Keine Cookies, keine Zählpixel, keine Anfragen "
                             "an fremde Server."),
                punkt_dunkel("Löscht sich von selbst",
                             "Die Antworten eurer Gäste verschwinden vier "
                             "Wochen nach der Hochzeit."),
                punkt_dunkel("Läuft auf jedem Telefon",
                             "Auch mit wenig Empfang. Wer weniger Bewegung "
                             "eingestellt hat, bekommt sie ruhig."),
            ]),
        }),
        "10-ehrlich": ersetzen(b10_ehrlich(), {
            "punkte": "".join([
                punkt_nicht("Keine Vorlage zum Selbstbauen",
                            "Ihr bekommt kein Programm und kein Konto, "
                            "sondern eine fertige Seite."),
                punkt_nicht("Kein Sitzplan, keine Gästeverwaltung",
                            "Sie lädt ein und nimmt Antworten entgegen. "
                            "Mehr nicht, und das mit Absicht."),
                punkt_nicht("Keine Karte, die man anfassen kann",
                            "Sie lebt in der Hand, nicht im Karton."),
            ]),
        }),
    }


def main(argv: list[str]) -> int:
    adresse = argv[0] if argv else PLATZHALTER
    echt = bool(argv)
    if not echt:
        print(f"  Keine Adresse angegeben — QR zeigt auf {PLATZHALTER}")

    ZIEL.mkdir(parents=True, exist_ok=True)
    huelle = ("<!doctype html><meta charset=utf-8>" + kopf() + "@@rumpf@@")

    with sync_playwright() as p:
        b = p.chromium.launch(executable_path=CHROME)
        pg = b.new_page(viewport={"width": KANTE, "height": KANTE})
        for name, rumpf in seiten(adresse, echt).items():
            datei = ZIEL / f"{name}.png"
            pg.set_content(ersetzen(huelle, {"rumpf": rumpf}),
                           wait_until="load")
            pg.evaluate("document.fonts.ready")
            pg.wait_for_timeout(260)
            pg.screenshot(path=str(datei))
            print(f"  {name}.png  {datei.stat().st_size // 1024} KB")
        b.close()
    print(f"\nLiegt in {ZIEL}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
