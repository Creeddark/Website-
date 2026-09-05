#!/usr/bin/env python3
"""
Ein Kunde, immer und immer wieder.

Ein verkauftes Theme darf nicht bedeuten, dass jemand einen 2,3-MB-Ordner
kopiert und darin Namen sucht. Bei fuenfzig Paaren laegen fuenfzig Kopien
derselben Schriften, desselben Films und desselben Programmcodes im Repo,
und beim Aendern einer Kleinigkeit muesste jemand fuenfzig Ordner anfassen.

Darum getrennt:

    themes/<theme>/           das Theme. Einmal da, fuer alle.
    kunden/<kennung>/         nur was diesem Paar gehoert.
      daten.json              Namen, Termin, Ort, Texte
      bilder/                 eigene Fotos, ueberlagern die des Themes
      film/                   eigener Hero-Film, optional
    auslieferung/<kennung>/   das Ergebnis. Genau das wird hochgeladen.

Befehle:

    python3 build/kunde.py neu    <kennung> [theme]
    python3 build/kunde.py bauen  <kennung>
    python3 build/kunde.py liste

`kunden/` und `auslieferung/` sind bewusst nicht eingecheckt: darin stehen
Namen, Adressen und Fotos echter Menschen. Die haben in einem Git-Repo
nichts verloren, schon gar nicht in einem, das jemand spaeter oeffentlich
macht.
"""
from __future__ import annotations

import json
import pathlib
import re
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
KUNDEN = ROOT / "kunden"
AUSLIEFERUNG = ROOT / "auslieferung"
KENNUNG = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")

# Was ein Kunde selbst ausfuellen muss. Steht eines davon noch auf dem Wert
# des Themes, ist es vergessen worden — und niemand merkt es, bis in der
# Einladung eines fremden Paares "Gut Morgentau" steht.
PFLICHT = [
    ("paar", "a"), ("paar", "b"),
    ("termin", "tag"), ("termin", "beginn"),
    ("ort", "name"), ("ort", "strasse"), ("ort", "stadt"),
    ("kontakt", "mail"),
]


def hole(d: dict, pfad: tuple[str, ...]):
    for teil in pfad:
        d = d.get(teil) if isinstance(d, dict) else None
        if d is None:
            return None
    return d


def laden(pfad: pathlib.Path) -> dict:
    return json.loads(pfad.read_text(encoding="utf-8"))


def sichern(pfad: pathlib.Path, daten: dict) -> None:
    pfad.write_text(json.dumps(daten, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")


# --------------------------------------------------------------------- neu --

def neu(kennung: str, theme: str = "ambra") -> int:
    if not KENNUNG.match(kennung):
        print("Die Kennung darf nur Kleinbuchstaben, Ziffern und Striche "
              "enthalten und muss mit einem Zeichen davon beginnen.\n"
              "Sie wird zur Subdomain und steht im RSVP-Dienst.")
        return 2

    ordner = KUNDEN / kennung
    if ordner.exists():
        print(f"{ordner.relative_to(ROOT)} gibt es schon.")
        return 1

    vorlage = laden(ROOT / "themes" / theme / "daten.json")

    # Die Identitaet wird geleert, die Texte bleiben als Anfang stehen. Ein
    # vollstaendig leeres Formular ist schwerer auszufuellen als eines, in dem
    # steht, was an die Stelle gehoert.
    for pfad in PFLICHT:
        ziel = vorlage
        for teil in pfad[:-1]:
            ziel = ziel[teil]
        ziel[pfad[-1]] = ""
    vorlage["termin"]["lang"] = {"de": "", "en": ""}
    vorlage["termin"]["kurz"] = {"de": "", "en": ""}
    vorlage["termin"]["siegel"] = ""
    vorlage["ort"]["kurz"] = {"de": "", "en": ""}
    vorlage["ort"]["karte"] = ""
    vorlage["kalender"] = {k: "" for k in vorlage["kalender"]}
    vorlage["adresse"] = ""
    vorlage["theme"] = theme
    vorlage["vorschau"] = False        # ein echter Kunde ist keine Vorschau
    vorlage["rsvp"]["endpunkt"] = ""
    vorlage["rsvp"]["kennung"] = kennung
    vorlage["recht"]["verantwortlich"] = {"de": "", "en": ""}

    (ordner / "bilder").mkdir(parents=True)
    (ordner / "film").mkdir()
    sichern(ordner / "daten.json", vorlage)
    (ordner / "bilder" / "HIERHIN.txt").write_text(
        "Fotos dieses Paares. Sie überlagern beim Bauen die des Themes.\n"
        "Namen wie im Theme: hero.webp, g-1.webp … g-4.webp, siegel.webp.\n"
        "Zuschneiden macht build/art/ambra_fotos.py.\n", encoding="utf-8")
    (ordner / "film" / "HIERHIN.txt").write_text(
        "hero.mp4 und hero.webm dieses Paares, erzeugt mit\n"
        "build/art/ambra_film.py. Fehlen sie, bleibt der Film des Themes.\n",
        encoding="utf-8")

    print(f"Angelegt: {ordner.relative_to(ROOT)}")
    print()
    print("  1. daten.json ausfüllen — leere Felder sind Pflicht")
    print(f"  2. Fotos nach {ordner.relative_to(ROOT)}/bilder/")
    print(f"  3. python3 build/kunde.py bauen {kennung}")
    return 0


# ------------------------------------------------------------------- bauen --

def bauen(kennung: str) -> int:
    ordner = KUNDEN / kennung
    if not ordner.is_dir():
        print(f"{ordner.relative_to(ROOT)} gibt es nicht. "
              f"Erst: python3 build/kunde.py neu {kennung}")
        return 1

    daten = laden(ordner / "daten.json")
    theme = daten.get("theme", "ambra")
    quelle = ROOT / "themes" / theme
    if not quelle.is_dir():
        print(f"Theme {theme} gibt es nicht.")
        return 1

    fehlt = [".".join(p) for p in PFLICHT if not hole(daten, p)]
    if fehlt:
        print("Diese Felder sind noch leer:\n  " + "\n  ".join(fehlt))
        print("\nGebaut wird trotzdem, aber so darf es nicht ausgeliefert "
              "werden — in der Einladung stünde dann nichts oder das Falsche.")

    ziel = AUSLIEFERUNG / kennung
    if ziel.exists():
        shutil.rmtree(ziel)
    ziel.mkdir(parents=True)

    # 1. Das Theme, ohne seine Demo-Daten und ohne die erzeugten Seiten.
    shutil.copytree(quelle / "assets", ziel / "assets")

    # 2. Darueber, was dem Paar gehoert. Gleiche Namen gewinnen.
    eigene = []
    for unter, nach in (("bilder", "assets/img"), ("film", "assets/video")):
        for datei in sorted((ordner / unter).glob("*")):
            if datei.name == "HIERHIN.txt" or not datei.is_file():
                continue
            shutil.copy2(datei, ziel / nach / datei.name)
            eigene.append(f"{nach}/{datei.name}")

    # 3. daten.json mit, die Vorschaukarte liest sie.
    sichern(ziel / "daten.json", daten)

    # 4. Die Seiten.
    sys.path.insert(0, str(ROOT / "build"))
    import einladung
    einladung.schreiben(ziel, daten, theme)

    # 5. Die Vorschaukarte mit den Namen dieses Paares. Ohne sie traegt jede
    #    geteilte Nachricht den Namen des Demo-Paares.
    karte = subprocess.run(
        [sys.executable, str(ROOT / "build" / "art" / "ambra_og.py"), str(ziel)],
        capture_output=True, text=True)
    if karte.returncode == 0:
        print(karte.stdout.strip().splitlines()[-1])
    else:
        print("  og.png            nicht erzeugt — Playwright fehlt?")
        print("                    Die Karte des Themes bleibt liegen.")

    (ziel / "daten.json").unlink()      # gehoert nicht auf den Webserver

    groesse = sum(f.stat().st_size for f in ziel.rglob("*") if f.is_file())
    anzahl = sum(1 for f in ziel.rglob("*") if f.is_file())
    print()
    print(f"Fertig: {ziel.relative_to(ROOT)}  ({anzahl} Dateien, {groesse // 1024} KB)")
    if eigene:
        print("Eigene Dateien: " + ", ".join(eigene))
    else:
        print("Eigene Dateien: keine — es laufen noch die Bilder des Themes.")
    if not daten.get("adresse"):
        print("\nOhne \"adresse\" bleibt die Vorschaukarte relativ. Beim Teilen "
              "über\nWhatsApp erscheint dann eine leere Fläche.")
    return 0


# ------------------------------------------------------------------- liste --

def liste() -> int:
    if not KUNDEN.is_dir() or not any(KUNDEN.iterdir()):
        print("Noch keine Kunden. Anlegen: python3 build/kunde.py neu <kennung>")
        return 0
    print(f"{'Kennung':22} {'Theme':8} {'Termin':12} {'RSVP':6} Fehlt")
    for ordner in sorted(KUNDEN.iterdir()):
        if not (ordner / "daten.json").is_file():
            continue
        d = laden(ordner / "daten.json")
        fehlt = [".".join(p) for p in PFLICHT if not hole(d, p)]
        print(f"{ordner.name:22} {d.get('theme',''):8} "
              f"{d.get('termin',{}).get('tag',''):12} "
              f"{'ja' if d.get('rsvp',{}).get('endpunkt') else 'nein':6} "
              f"{len(fehlt) or ''}")
    return 0


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__.strip())
        return 2
    befehl, rest = argv[0], argv[1:]
    if befehl == "neu" and rest:
        return neu(rest[0], rest[1] if len(rest) > 1 else "ambra")
    if befehl == "bauen" and rest:
        return bauen(rest[0])
    if befehl == "liste":
        return liste()
    print(__doc__.strip())
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
