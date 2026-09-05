#!/usr/bin/env python3
"""
AMBRA — Vorschaukarte fuer geteilte Nachrichten.

Eine Einladung wird per WhatsApp weitergereicht. Ohne og:image zeigt die
Nachricht eine leere Flaeche, und genau dort entsteht der erste Eindruck.
Die Karte wird aus denselben Schriften und Farben gebaut wie die Einladung
selbst, damit beides zusammengehoert.

    python3 build/art/ambra_og.py [ordner]

Der Ordner ist ein fertig gebauter Kundenordner; ohne Angabe das Theme
selbst. Die Namen und der Termin kommen aus der daten.json daneben — traegt
jede Karte dasselbe Paar, steht in jeder geteilten Nachricht das falsche.

Braucht Playwright und ein Chromium. Faellt eines von beidem aus, bleibt die
vorhandene og.png liegen — sie ist eingecheckt.
"""
from __future__ import annotations

import contextlib
import functools
import http.server
import pathlib
import socketserver
import sys
import threading

ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
THEME = ROOT / "themes" / "ambra"
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"

SEITE = """<meta charset="utf-8">
<link rel="stylesheet" href="assets/css/einladung.css">
<style>
  html,body{margin:0;height:100%}
  body{background:#14100C;display:grid;place-items:center;text-align:center;
       font-family:"Montserrat",sans-serif}
  .b{position:absolute;inset:0;background:
     radial-gradient(58% 62% at 50% 44%, rgba(216,182,119,.20), transparent 70%)}
  .i{position:relative;color:#F2E7D3}
  .k{font-size:15px;letter-spacing:.42em;text-transform:uppercase;color:#D8B677;margin:0 0 34px}
  h1{font-family:"Playfair Display",serif;font-weight:400;font-size:104px;line-height:.98;
     letter-spacing:-.025em;margin:0}
  .a{display:block;font-size:42px;color:#D8B677;line-height:1.5}
  .d{margin:38px 0 0;font-size:17px;letter-spacing:.28em;text-transform:uppercase}
  .o{margin:12px 0 0;font-size:16px;color:#A2957E;letter-spacing:.06em}
  svg{width:200px;margin:40px auto 0;color:#3A3026;display:block}
</style>
<div class="b"></div>
<div class="i">
  <p class="k">@@kicker@@</p>
  <h1>@@a@@<span class="a">&amp;</span>@@b@@</h1>
  <p class="d">@@datum@@</p>
  <p class="o">@@ort@@</p>
  <svg viewBox="0 0 240 16"><g fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round">
    <path d="M0 8h96M144 8h96"/><path d="M120 2l7 6-7 6-7-6z"/>
    <path d="M104 8c4-4 8-4 9 0-1 4-5 4-9 0zM136 8c-4-4-8-4-9 0 1 4 5 4 9 0z"/></g></svg>
</div>
"""


@contextlib.contextmanager
def server(verzeichnis: pathlib.Path):
    """Die Schriften laden nur ueber HTTP, file:// blockiert sie."""
    handler = functools.partial(http.server.SimpleHTTPRequestHandler,
                                directory=str(verzeichnis))
    with socketserver.TCPServer(("127.0.0.1", 0), handler) as srv:
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        try:
            yield srv.server_address[1]
        finally:
            srv.shutdown()


def main(argv: list[str] | None = None) -> None:
    import html
    import json
    from playwright.sync_api import sync_playwright

    argv = argv if argv is not None else sys.argv[1:]
    ordner = pathlib.Path(argv[0]).resolve() if argv else THEME
    daten = json.loads((ordner / "daten.json").read_text(encoding="utf-8"))

    def z(feld, sprache="de"):
        return (feld.get(sprache) or feld.get("de") or "") if isinstance(feld, dict) else (feld or "")

    # Kein .format(): die Vorlage steckt voller CSS-Klammern, und die muesste
    # man alle verdoppeln. Ein Platzhalter, der im CSS nicht vorkommt, ist
    # weniger fehleranfaellig als eine Regel, an die sich jeder halten muss.
    seite = SEITE
    for name, wert in (
        ("kicker", z(daten["hero"]["kicker"])),
        ("a", daten["paar"]["a"]),
        ("b", daten["paar"]["b"]),
        ("datum", z(daten["termin"]["lang"])),
        ("ort", z(daten["ort"]["kurz"])),
    ):
        seite = seite.replace("@@%s@@" % name, html.escape(wert))

    tmp = ordner / "_og.html"
    tmp.write_text(seite, encoding="utf-8")
    try:
        with server(ordner) as port, sync_playwright() as p:
            b = p.chromium.launch(executable_path=CHROME)
            pg = b.new_page(viewport={"width": 1200, "height": 630})
            pg.goto(f"http://127.0.0.1:{port}/_og.html", wait_until="networkidle")
            pg.wait_for_timeout(400)
            ziel = ordner / "assets" / "img" / "og.png"
            pg.screenshot(path=str(ziel))
            b.close()
        print(f"  og.png            {ziel.stat().st_size // 1024:>4} KB  (1200x630)")
    finally:
        tmp.unlink(missing_ok=True)


if __name__ == "__main__":
    main(sys.argv[1:])
