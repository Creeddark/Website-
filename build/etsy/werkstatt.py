#!/usr/bin/env python3
"""
Das Handwerkszeug fuer die Produktbilder: Schriften, Farben, Telefonrahmen.

Die Bilder werden als HTML gebaut und im Browser aufgenommen. Das klingt
umstaendlich und ist es nicht: dieselben Schriften, dieselben Farben und
dieselben Kurven wie in der Einladung selbst, ohne dass jemand in einem
Grafikprogramm etwas nachbaut, das dann doch anders aussieht.

Wird von bilder.py benutzt.
"""
from __future__ import annotations

import base64
import pathlib

WURZEL = pathlib.Path(__file__).resolve().parents[2]
SCHRIFT = WURZEL / "themes/ambra/assets/fonts"
AUFNAHMEN = pathlib.Path(__file__).resolve().parent / "aufnahmen"
SIEGEL = WURZEL / "themes/ambra/assets/img/siegel.webp"

# Etsy zeigt Quadrate. Wer ein anderes Verhaeltnis hochlaedt, bekommt einen
# Beschnitt, den er nicht selbst gewaehlt hat.
KANTE = 2000


def daten(datei: pathlib.Path) -> str:
    typ = {"woff2": "font/woff2", "png": "image/png", "webp": "image/webp"}[
        datei.suffix.lstrip(".")]
    return f"data:{typ};base64," + base64.b64encode(datei.read_bytes()).decode()


def bild(name: str) -> str:
    """Eine Telefonaufnahme als Daten-URL."""
    return daten(AUFNAHMEN / f"{name}.png")


def ersetzen(vorlage: str, werte: dict[str, str]) -> str:
    """@@name@@ ersetzen. Kein .format(), sonst kollidieren CSS-Klammern."""
    for k, v in werte.items():
        vorlage = vorlage.replace(f"@@{k}@@", v)
    return vorlage


# --------------------------------------------------------------------- CSS --

KOPF = """
<style>
  :root {
    --night:      #14100C;
    --night-2:    #1E1811;
    --night-line: #3A3026;
    --on-night:   #F2E7D3;
    --on-night-2: #A2957E;
    --paper:      #FBF6EE;
    --paper-2:    #F3EADB;
    --line:       #E2D7C4;
    --ink:        #241F18;
    --ink-2:      #565042;
    --brass:      #82632E;
    --brass-lit:  #D8B677;
    --ff-display: "Playfair Display", Georgia, serif;
    --ff-text:    "Montserrat", "Helvetica Neue", Arial, sans-serif;
  }
  @font-face {
    font-family: "Playfair Display";
    src: url("@@playfair@@") format("woff2");
    font-weight: 400 700; font-display: block;
  }
  @font-face {
    font-family: "Montserrat";
    src: url("@@montserrat@@") format("woff2");
    font-weight: 300 700; font-display: block;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { width: @@kante@@px; height: @@kante@@px; }
  body {
    font-family: var(--ff-text);
    -webkit-font-smoothing: antialiased;
    overflow: hidden;
  }

  /* Die Buehne. Jedes Bild ist ein Quadrat mit ordentlich Luft am Rand —
     Etsy beschneidet in der Suche leicht, und ein Wort, das dabei
     halbiert wird, ist schlimmer als etwas Leere. */
  .buehne {
    width: @@kante@@px; height: @@kante@@px;
    padding: 150px;
    display: flex; flex-direction: column;
    position: relative; overflow: hidden;
  }
  .nacht { background: var(--night); color: var(--on-night); }
  .papier { background: var(--paper); color: var(--ink); }
  /* Ein Lichtschein von oben, damit die dunkle Flaeche nicht tot wirkt. */
  .nacht::before {
    content: ""; position: absolute; inset: 0;
    background: radial-gradient(62% 44% at 50% 22%,
                rgba(216,182,119,0.17), transparent 72%);
  }
  .buehne > * { position: relative; }

  h1 {
    font-family: var(--ff-display); font-weight: 400;
    font-size: 118px; line-height: 1.03; letter-spacing: -0.022em;
    text-wrap: balance;
  }
  h2 {
    font-family: var(--ff-display); font-weight: 400;
    font-size: 76px; line-height: 1.06; letter-spacing: -0.018em;
    text-wrap: balance;
  }
  .marke {
    font-size: 26px; font-weight: 500; letter-spacing: 0.34em;
    text-transform: uppercase; color: var(--brass);
  }
  .nacht .marke { color: var(--brass-lit); }
  .lede { font-size: 38px; line-height: 1.5; color: var(--ink-2); }
  .nacht .lede { color: var(--on-night-2); }
  .klein { font-size: 27px; line-height: 1.5; color: var(--ink-2); }
  .nacht .klein { color: var(--on-night-2); }

  /* Ein Telefon. Rahmen aus CSS statt einer Attrappe von der Stange —
     eine fremde Attrappe traegt immer die Handschrift von jemand anderem. */
  .fon {
    --b: 300px;
    width: var(--b); height: calc(var(--b) * 844 / 390);
    border-radius: calc(var(--b) * 0.135);
    padding: calc(var(--b) * 0.026);
    background: linear-gradient(150deg, #3B342A, #16120D 42%, #2A241C);
    /* Der Lichtsaum haelt das Geraet vom nachtdunklen Grund getrennt. Ohne
       ihn steht auf Bild eins nur die Karte mit dem Siegel im Nichts. */
    box-shadow: 0 calc(var(--b) * 0.09) calc(var(--b) * 0.16) rgba(0,0,0,0.42),
                inset 0 0 0 1px rgba(242,231,211,0.13);
    flex: none;
  }
  .fon img {
    width: 100%; height: 100%; display: block; object-fit: cover;
    border-radius: calc(var(--b) * 0.112);
  }

  .reihe { display: flex; gap: 60px; align-items: flex-end; }
  .spalte { display: flex; flex-direction: column; }
  .schub { margin-top: auto; }

  /* Eine Bildunterschrift unter einem Telefon. */
  .unter {
    margin-top: 34px; text-align: center;
    font-size: 24px; letter-spacing: 0.16em; text-transform: uppercase;
    color: var(--brass);
  }
  .nacht .unter { color: var(--brass-lit); }
  .unter b { display: block; font-weight: 500; }
  .unter span {
    display: block; margin-top: 12px;
    font-size: 23px; letter-spacing: 0; text-transform: none;
    color: var(--ink-2); line-height: 1.4;
  }
  .nacht .unter span { color: var(--on-night-2); }

  .strich {
    width: 190px; height: 1px; background: var(--line); border: 0;
  }
  .nacht .strich { background: var(--night-line); }

  .fuss {
    display: flex; justify-content: space-between; align-items: baseline;
    font-size: 24px; letter-spacing: 0.22em; text-transform: uppercase;
    color: var(--brass);
  }
  .nacht .fuss { color: var(--brass-lit); }
</style>
"""


def kopf() -> str:
    return ersetzen(KOPF, {
        "playfair": daten(SCHRIFT / "playfair-latin.woff2"),
        "montserrat": daten(SCHRIFT / "montserrat-latin.woff2"),
        "kante": str(KANTE),
    })


def fon(name: str, breite: int = 300, klasse: str = "") -> str:
    """Ein Telefon mit einer Aufnahme darin."""
    return (f'<div class="fon {klasse}" style="--b:{breite}px">'
            f'<img src="{bild(name)}" alt=""></div>')
