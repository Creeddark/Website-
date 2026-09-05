#!/usr/bin/env python3
"""
AMBRA — Einladung aus daten.json erzeugen.

Solange der Inhalt im HTML steht, ist eine Einladung ein Einzelstueck. Fuer
Kunde Nummer zwei muesste jemand die Datei durchgehen und Namen tauschen, und
irgendwann steht im Fuss noch das Datum des vorigen Paares. Darum liegt der
ganze Inhalt in themes/<theme>/daten.json, und dieses Skript setzt ihn in das
Geruest unter build/vorlagen/.

    python3 build/einladung.py [theme]

Erzeugt:
    themes/<theme>/index.html        die Einladung
    themes/<theme>/datenschutz.html  die Datenschutzseite, sobald gesendet wird

Beides ist eingecheckt — die Einladung funktioniert also auch ohne dieses
Skript. Es existiert nur, damit derselbe Text nicht an neun Stellen steht.
"""
from __future__ import annotations

import html
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
VORLAGEN = ROOT / "build" / "vorlagen"


# ------------------------------------------------------------- Werkzeuge --

def e(text: str) -> str:
    """Alles, was aus der Datendatei kommt, wird maskiert. Ein Apostroph im
    Namen des Gutshofs darf das Attribut daneben nicht sprengen."""
    return html.escape(str(text), quote=True)


def zweisprachig(feld, sprache: str = "de") -> str:
    """Ein Feld ist entweder ein Text oder {de, en}. Fehlt die zweite Sprache,
    wird der deutsche Text genommen: eine leere Zeile waere schlimmer."""
    if isinstance(feld, dict):
        return feld.get(sprache) or feld.get("de") or ""
    return feld or ""


def de(feld) -> str: return e(zweisprachig(feld, "de"))
def en(feld) -> str: return e(zweisprachig(feld, "en"))


def stufen(anzahl: int, start: int, schritt: int) -> list[int]:
    """Die Verzoegerungen der Einblendung. Sie stehen im HTML, damit die
    Reihenfolge aus dem Markup ablesbar bleibt."""
    return [start + i * schritt for i in range(anzahl)]


# ------------------------------------------------------------- Bausteine --

def hero_medien(d: dict) -> str:
    h = d["hero"]
    b, hh = h.get("bild_masse", [1080, 1920])
    zeilen = [
        f'      <img src="{e(h["bild"])}" alt="" width="{b}" height="{hh}"',
        '           fetchpriority="high" data-optional>',
    ]
    filme = h.get("film") or []
    if filme:
        typ = {"webm": "video/webm", "mp4": "video/mp4"}
        zeilen += [
            '      <video class="hero__video" data-hero-video',
            '             muted loop playsinline disablepictureinpicture preload="none">',
        ]
        for f in filme:
            zeilen.append(f'        <source data-quelle="{e(f)}" '
                          f'type="{typ.get(f.rsplit(".", 1)[-1], "video/mp4")}">')
        zeilen.append("      </video>")
    return "\n".join(zeilen)


def weg_punkte(d: dict) -> str:
    p = d["weg"]["punkte"]
    aus = []
    for punkt, ms in zip(p, stufen(len(p), 200, 120)):
        aus.append(
            f'        <li style="--d:{ms}ms">\n'
            f'          <time datetime="{e(punkt["zeit"])}" data-en="{en(punkt["wann"])}">'
            f'{de(punkt["wann"])}</time>\n'
            f'          <h3 data-en="{en(punkt["titel"])}">{de(punkt["titel"])}</h3>\n'
            f'          <p data-en="{en(punkt["text"])}">{de(punkt["text"])}</p>\n'
            f'        </li>')
    return "\n\n".join(aus)


def galerie(d: dict) -> str:
    aus = []
    for bild in d["galerie"]["bilder"]:
        aus.append(
            f'      <li><button type="button"><img src="{e(bild["datei"])}" '
            f'width="900" height="1200" loading="lazy"\n'
            f'        alt="{de(bild["alt"])}"\n'
            f'        data-alt-en="{en(bild["alt"])}"></button></li>')
    return "\n".join(aus)


def ablauf(d: dict) -> str:
    p = d["ablauf"]["punkte"]
    aus = []
    for punkt, ms in zip(p, stufen(len(p), 120, 80)):
        aus.append(
            f'        <li class="rise" style="--d:{ms}ms">\n'
            f'          <time datetime="{e(punkt["zeit"])}">{e(punkt["zeit"])}</time>\n'
            f'          <h3 data-en="{en(punkt["titel"])}">{de(punkt["titel"])}</h3>\n'
            f'          <p data-en="{en(punkt["text"])}">{de(punkt["text"])}</p>\n'
            f'        </li>')
    return "\n".join(aus)


def hinweise(d: dict) -> str:
    aus = []
    for h in d["wo"]["hinweise"]:
        aus.append(
            f'        <li><time data-en="{en(h["marke"])}">{de(h["marke"])}</time>\n'
            f'          <h3 data-en="{en(h["titel"])}">{de(h["titel"])}</h3>\n'
            f'          <p data-en="{en(h["text"])}">{de(h["text"])}</p>\n'
            f'        </li>')
    return "\n".join(aus)


def rsvp_hinweis(d: dict) -> str:
    """Der Satz unter dem Absendeknopf. Sobald wirklich gesendet wird, muss
    dort stehen, wohin und wie lange — vorher waere es eine Behauptung."""
    if not d["rsvp"].get("endpunkt"):
        return ('        <p class="hinweis" data-en="Nothing is sent in this preview. '
                'Your reply stays in your browser.">In dieser Vorschau wird nichts '
                'gesendet. Eure Antwort bleibt in eurem Browser.</p>')
    frist = de(d["recht"]["loeschfrist"])
    frist_en = en(d["recht"]["loeschfrist"])
    return (
        '        <p class="hinweis">\n'
        f'          <span data-en="Your reply goes to {en(d["recht"]["verantwortlich"])} '
        f'and is deleted {frist_en}. ">Eure Antwort geht an '
        f'{de(d["recht"]["verantwortlich"])} und wird {frist} gelöscht. </span>'
        '<a class="link" href="datenschutz.html" data-en="More on data protection">'
        'Mehr zum Datenschutz</a>\n'
        '        </p>')


def fuss_recht(d: dict) -> str:
    if not d["rsvp"].get("endpunkt"):
        return ""
    return ('    <p><a href="datenschutz.html" data-en="Data protection">'
            'Datenschutz</a></p>')


def vorschau(d: dict) -> str:
    if not d.get("vorschau"):
        return ""
    return (
        '<!-- Der Vorschaustreifen. Er steht am Ende, damit er die Einladung nicht\n'
        '     stört, und sagt unmissverständlich, was das hier ist. -->\n'
        '<div class="vorschau">\n'
        f'  <p><b>Live-Vorschau</b> · Theme {d["theme"].upper()}. Namen, Daten und '
        'Bilder sind erfunden.\n'
        '     In dieser Vorschau wird nichts gesendet und nichts gespeichert.</p>\n'
        '</div>')


# ----------------------------------------------------------------- Bauen --

def felder(d: dict) -> dict[str, str]:
    paar = d["paar"]
    t, o, k = d["termin"], d["ort"], d["kalender"]
    # Vorschaudienste loesen relative Pfade nicht auf. Solange keine Adresse
    # eingetragen ist, bleibt es relativ — die Vorschau ist dann eben leer,
    # das ist ehrlicher als ein Pfad, der ins Leere zeigt.
    adresse = d.get("adresse", "")
    if adresse and not adresse.endswith("/"):
        adresse += "/"
    namen = f'{paar["a"]} & {paar["b"]}'
    return {
        "titel": f'{e(namen)} — {de(t["kurz"])}',
        "beschreibung": (f'Wir heiraten. Am {de(t["kurz"])} auf {e(o["name"])}, '
                         f'{e(o["stadt"])}. Alle Angaben zum Tag und zur Rückmeldung.'),
        "og_text": f'Wir heiraten. {de(o["kurz"])}.',
        "og_bild": e(adresse + d.get("og_bild", "assets/img/og.png")),
        "og_url": e(adresse or "index.html"),

        "umschlag_de": de(d["umschlag"]["zeile"]), "umschlag_en": en(d["umschlag"]["zeile"]),
        "siegel_datum": e(t["siegel"]),

        "hero_medien": hero_medien(d),
        "kicker_de": de(d["hero"]["kicker"]), "kicker_en": en(d["hero"]["kicker"]),
        "name_a": e(paar["a"]), "name_b": e(paar["b"]),
        "tag": e(t["tag"]), "datum_de": de(t["lang"]), "datum_en": en(t["lang"]),
        "datum_kurz": de(t["kurz"]),
        "ortkurz_de": de(o["kurz"]), "ortkurz_en": en(o["kurz"]),
        "beginn": e(t["beginn"]),

        "weg_eyebrow_de": de(d["weg"]["eyebrow"]), "weg_eyebrow_en": en(d["weg"]["eyebrow"]),
        "weg_titel_de": de(d["weg"]["titel"]), "weg_titel_en": en(d["weg"]["titel"]),
        "weg_punkte": weg_punkte(d),

        "gal_eyebrow_de": de(d["galerie"]["eyebrow"]), "gal_eyebrow_en": en(d["galerie"]["eyebrow"]),
        "gal_titel_de": de(d["galerie"]["titel"]), "gal_titel_en": en(d["galerie"]["titel"]),
        "galerie": galerie(d),

        "tag_eyebrow_de": de(d["ablauf"]["eyebrow"]), "tag_eyebrow_en": en(d["ablauf"]["eyebrow"]),
        "tag_titel_de": de(d["ablauf"]["titel"]), "tag_titel_en": en(d["ablauf"]["titel"]),
        "ablauf": ablauf(d),

        "wo_eyebrow_de": de(d["wo"]["eyebrow"]), "wo_eyebrow_en": en(d["wo"]["eyebrow"]),
        "wo_titel_de": de(d["wo"]["titel"]), "wo_titel_en": en(d["wo"]["titel"]),
        "ort_name": e(o["name"]), "ort_strasse": e(o["strasse"]), "ort_stadt": e(o["stadt"]),
        "ort_karte": e(o["karte"]),
        "hinweise": hinweise(d),

        "rsvp_eyebrow_de": de(d["rsvp"]["eyebrow"]), "rsvp_eyebrow_en": en(d["rsvp"]["eyebrow"]),
        "rsvp_lede_de": de(d["rsvp"]["lede"]), "rsvp_lede_en": en(d["rsvp"]["lede"]),
        "rsvp_endpunkt": e(d["rsvp"].get("endpunkt", "")),
        "rsvp_kennung": e(d["rsvp"].get("kennung", "")),
        "rsvp_hinweis": rsvp_hinweis(d),

        "ics_start": e(k["start_utc"]), "ics_ende": e(k["ende_utc"]),
        "ics_titel": e(k["titel"]), "ics_text": e(k["text"]),
        "ics_ort": e(f'{o["name"]}, {o["strasse"]}, {o["stadt"]}'),
        "ics_datei": e(k["datei"]),

        "mail": e(d["kontakt"]["mail"]),
        "fuss_recht": fuss_recht(d),
        "vorschau": vorschau(d),
        "musik": e(d["musik"]),
    }


def setzen(vorlage: str, werte: dict[str, str]) -> str:
    fehlt = sorted(set(re.findall(r"\{\{(\w+)\}\}", vorlage)) - set(werte))
    if fehlt:
        raise SystemExit("Platzhalter ohne Wert: " + ", ".join(fehlt))
    # Ein leerer Wert nimmt seine ganze Zeile mit. Sonst bleibt dort eine
    # Leerzeile stehen, und wer den Quelltext liest, sucht nach dem Fehler.
    # Global zusammenzustreichen waere falsch: die Absaetze zwischen den
    # Abschnitten sind Absicht.
    for k, v in werte.items():
        if not v:
            vorlage = re.sub(r"\n[ \t]*\{\{%s\}\}(?=\n|$)" % k, "", vorlage)
    for k, v in werte.items():
        vorlage = vorlage.replace("{{%s}}" % k, v)
    return vorlage


def rendern(daten: dict, theme: str) -> tuple[str, str | None]:
    """Aus Daten und Geruest die fertigen Seiten machen. Gibt die Einladung
    zurueck und, sobald wirklich gesendet wird, die Datenschutzseite."""
    werte = felder(daten)
    seite = setzen((VORLAGEN / f"{theme}.html").read_text(encoding="utf-8"), werte)
    if not daten["rsvp"].get("endpunkt"):
        return seite, None
    import datenschutz
    return seite, datenschutz.bauen(daten, werte)


def schreiben(ordner: pathlib.Path, daten: dict, theme: str) -> None:
    """Beide Seiten in einen Ordner legen. Die Datenschutzseite verschwindet
    wieder, wenn der Endpunkt entfernt wurde — eine Seite ueber die
    Verarbeitung von Daten, die niemand verarbeitet, verwirrt mehr als sie
    hilft."""
    seite, schutz = rendern(daten, theme)
    (ordner / "index.html").write_text(seite, encoding="utf-8")
    print(f"  index.html        {len(seite) // 1024:>4} KB")

    ziel = ordner / "datenschutz.html"
    if schutz:
        ziel.write_text(schutz, encoding="utf-8")
        print(f"  datenschutz.html  {len(schutz) // 1024:>4} KB")
    elif ziel.exists():
        ziel.unlink()
        print("  datenschutz.html  entfernt (es wird nichts gesendet)")


def main(argv: list[str]) -> int:
    theme = argv[0] if argv else "ambra"
    ordner = ROOT / "themes" / theme
    daten = json.loads((ordner / "daten.json").read_text(encoding="utf-8"))
    schreiben(ordner, daten, theme)
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT / "build"))
    raise SystemExit(main(sys.argv[1:]))
