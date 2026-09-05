#!/usr/bin/env python3
"""
Einen fertigen Ordner in eine einzige Datei falten.

Fuer eine Vorschau, die man verschicken kann, ohne vorher irgendwo etwas
einzurichten: Schriften, Bilder, Film, Musik, CSS und JavaScript wandern als
Daten-URLs in das HTML. Heraus kommt eine Datei, die ohne Server und ohne
Nachbarn funktioniert.

    python3 build/artefakt.py themes/ambra  vorschau-einladung.html
    python3 build/artefakt.py verkauf       vorschau-verkauf.html  "AMBRA"

Der dritte Wert ist ein anderer Titel. Ohne ihn steht der Titel der Seite
selbst darueber — der ist auf Suchmaschinen zugeschnitten und dafuer meist
zu lang.

Fuer die Auslieferung an Kunden ist das der falsche Weg — dort will man
zwischengespeicherte Dateien und einen Film, der erst auf Verlangen laedt.
Eine Daten-URL laedt immer alles sofort mit. Darum bleibt der Film hier auf
MP4 beschraenkt: WebM waere ein zweites Mal dasselbe, und jedes Byte muss
vor dem ersten Bild ueber die Leitung.
"""
from __future__ import annotations

import base64
import mimetypes
import pathlib
import re
import sys

# Nur diese Anhaengsel werden eingebettet. Alles andere waere ein Versehen.
TYPEN = {
    ".woff2": "font/woff2", ".webp": "image/webp", ".png": "image/png",
    ".jpg": "image/jpeg", ".svg": "image/svg+xml",
    ".mp4": "video/mp4", ".m4a": "audio/mp4",
}
# WebM fliegt raus: siehe oben.
UEBERSPRINGEN = {".webm"}


# Der Kalenderknopf legt eine ICS-Datei an und laesst sie herunterladen. Eine
# eingebettete Vorschau darf keine Dateien speichern — der Knopf taete dort
# still nichts. Auf der ausgelieferten Seite bleibt er unberuehrt; nur hier
# sagt er, warum er wartet.
KALENDERNOTIZ = """
<style>
  .vorschau-notiz {
    margin: 0.875rem 0 0; text-align: center;
    font-size: 0.75rem; line-height: 1.5; letter-spacing: 0.02em;
    color: var(--brass, #82632E);
  }
</style>
<script>
(function () {
  var knopf = document.querySelector("[data-ics]");
  if (!knopf) return;
  var notiz = document.createElement("p");
  notiz.className = "vorschau-notiz";
  notiz.hidden = true;
  notiz.textContent = "Der Kalendereintrag wird auf der fertigen Seite "
    + "geladen \u2014 diese Vorschau darf keine Dateien speichern.";
  notiz.dataset.en = "The calendar file downloads on the finished page "
    + "\u2014 this preview is not allowed to save files.";
  knopf.parentNode.insertAdjacentElement("afterend", notiz);

  // Im Einfangen am Dokument: so kommt der Klick gar nicht erst am Knopf an,
  // egal in welcher Reihenfolge die Zuhoerer eingetragen wurden.
  document.addEventListener("click", function (e) {
    if (!e.target.closest || !e.target.closest("[data-ics]")) return;
    e.preventDefault();
    e.stopPropagation();
    notiz.hidden = false;
  }, true);
})();
</script>"""

def daten_url(datei: pathlib.Path) -> str:
    typ = TYPEN.get(datei.suffix.lower()) or mimetypes.guess_type(datei.name)[0] \
          or "application/octet-stream"
    roh = base64.b64encode(datei.read_bytes()).decode("ascii")
    return f"data:{typ};base64,{roh}"


def css_einbetten(css: str, basis: pathlib.Path) -> str:
    """url(...) im Stylesheet durch Daten-URLs ersetzen. Was schon eine
    Daten-URL ist — etwa das Rauschen der Papierfaser — bleibt stehen."""
    def ersetzen(m: re.Match) -> str:
        pfad = m.group(2).strip()
        if pfad.startswith(("data:", "http:", "https:", "#")):
            return m.group(0)
        datei = (basis / pfad).resolve()
        if not datei.is_file():
            return m.group(0)
        return f'url("{daten_url(datei)}")'
    return re.sub(r'url\((["\']?)([^)"\']+)\1\)', ersetzen, css)


def main(argv: list[str]) -> int:
    if not 2 <= len(argv) <= 3:
        print(__doc__.strip())
        return 2
    ordner = pathlib.Path(argv[0]).resolve()
    ziel = pathlib.Path(argv[1])
    html = (ordner / "index.html").read_text(encoding="utf-8")

    if len(argv) == 3:
        titel = argv[2]
    else:
        titel_m = re.search(r"<title>(.*?)</title>", html, re.S)
        titel = titel_m.group(1).strip() if titel_m else ordner.name

    # Nur der Rumpf. Kopf und Huelle stellt die Vorschau selbst.
    rumpf = re.search(r"<body[^>]*>(.*)</body>", html, re.S)
    inhalt = rumpf.group(1) if rumpf else html

    # Das Attribut am body geht dabei verloren. Ohne data-state waere der
    # Umschlag von Anfang an offen und die Seite scrollbar. Beim Einbetten
    # liegt der Rumpf spaeter in einem fremden <body>, den es hier noch nicht
    # gibt — darum wartet das Setzen notfalls auf das fertige Geruest.
    zustand = ""
    m = re.search(r'<body[^>]*data-state="([^"]+)"', html)
    if m:
        zustand = (
            "<script>(function(){function s(){document.body.dataset.state="
            f'"{m.group(1)}"' ";}document.body?s():addEventListener("
            '"DOMContentLoaded",s);})()</script>')

    teile = []

    # Stylesheets
    for m in re.finditer(r'<link[^>]+rel="stylesheet"[^>]+href="([^"]+)"[^>]*>', html):
        datei = (ordner / m.group(1)).resolve()
        css = css_einbetten(datei.read_text(encoding="utf-8"), datei.parent)
        teile.append(f"<style>\n{css}\n</style>")

    # Bilder, Film, Musik im Rumpf
    def medien(m: re.Match) -> str:
        attribut, pfad = m.group(1), m.group(2)
        if pfad.startswith(("data:", "http:", "https:", "#", "mailto:", "tel:")):
            return m.group(0)
        datei = (ordner / pfad).resolve()
        if not datei.is_file() or datei.suffix.lower() in UEBERSPRINGEN:
            return ""
        return f'{attribut}="{daten_url(datei)}"'

    inhalt = re.sub(r'\b(src|data-quelle)="([^"]+)"', medien, inhalt)
    # Leergeraeumte <source> ohne Quelle wieder entfernen.
    inhalt = re.sub(r"<source\s+type=\"[^\"]*\"\s*>", "", inhalt)

    # JavaScript
    skripte = []
    for m in re.finditer(r'<script[^>]+src="([^"]+)"[^>]*></script>', html):
        datei = (ordner / m.group(1)).resolve()
        if datei.is_file():
            skripte.append(f"<script>\n{datei.read_text(encoding='utf-8')}\n</script>")
    inhalt = re.sub(r'<script[^>]+src="[^"]+"[^>]*></script>', "", inhalt)

    seite = "\n".join([f"<title>{titel}</title>", *teile, zustand, inhalt,
                       *skripte, KALENDERNOTIZ if "data-ics" in inhalt else ""])
    ziel.write_text(seite, encoding="utf-8")

    mb = ziel.stat().st_size / 1048576
    print(f"  {ziel}  {mb:.2f} MB")
    if mb > 14:
        print("  Achtung: über 14 MB, die Grenze für eine Vorschau liegt bei 16.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
