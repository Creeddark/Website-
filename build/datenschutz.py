#!/usr/bin/env python3
"""
Die Datenschutzseite einer Einladung.

Wird von build/einladung.py mitgebaut, sobald ein RSVP-Endpunkt eingetragen
ist. Vorher gibt es sie nicht: eine Seite ueber die Verarbeitung von Daten,
die niemand verarbeitet, verwirrt mehr als sie hilft.

Der Text steht hier und nicht in daten.json, weil er sich zwischen Kunden
nicht aendert — nur die Namen, Fristen und Adressen darin. Sonst haette man
in kurzer Zeit zwanzig leicht abweichende Fassungen.

WICHTIG: Das ist ein Entwurf, kein anwaltlich geprueftes Dokument. Vor dem
ersten verkauften Exemplar muss ihn jemand pruefen, der das darf. Siehe
docs/10-legal-and-limits.md.
"""
from __future__ import annotations

ABSCHNITTE = [
    (
        "Wer ist verantwortlich",
        "Who is responsible",
        "Für diese Einladung und die darüber abgegebenen Rückmeldungen sind "
        "{verantwortlich} verantwortlich, erreichbar unter "
        '<a class="link" href="mailto:{mail}">{mail}</a>. '
        "Die technische Bereitstellung übernimmt {betreiber} als "
        "Auftragsverarbeiter nach Art. 28 DSGVO.",
        "This invitation and the replies given through it are the "
        "responsibility of {verantwortlich}, reachable at "
        '<a class="link" href="mailto:{mail}">{mail}</a>. '
        "{betreiber} provides the technical service as a processor under "
        "Art. 28 GDPR.",
    ),
    (
        "Was erhoben wird",
        "What is collected",
        "Nur das, was im Formular steht: Name, E-Mail-Adresse, Zu- oder "
        "Absage, die Anzahl der Personen, eine Vorliebe am Tisch und eine "
        "freiwillige Nachricht. Mehr wird nicht abgefragt und mehr wird nicht "
        "gespeichert. Insbesondere werden <strong>keine Angaben zu "
        "Unverträglichkeiten, Allergien oder Gesundheit</strong> erhoben; das "
        "wären besondere Kategorien nach Art. 9 DSGVO und gehören nicht in "
        "ein offenes Formular.",
        "Only what the form asks for: name, email address, acceptance or "
        "decline, the number of people, a preference at the table and an "
        "optional message. Nothing else is asked and nothing else is stored. "
        "In particular <strong>no information about intolerances, allergies "
        "or health</strong> is collected; that would be a special category "
        "under Art. 9 GDPR and does not belong in an open form.",
    ),
    (
        "Wozu und auf welcher Grundlage",
        "Why, and on what basis",
        "Die Angaben dienen ausschließlich der Planung des Festes: der "
        "Gästezahl, der Sitzordnung und dem Essen. Rechtsgrundlage ist das "
        "berechtigte Interesse an der Durchführung einer privaten Feier "
        "(Art. 6 Abs. 1 lit. f DSGVO). Eine Weitergabe zu Werbezwecken findet "
        "nicht statt, und es gibt keine automatisierte Entscheidungsfindung.",
        "The information is used solely to plan the celebration: the number "
        "of guests, the seating and the catering. The legal basis is the "
        "legitimate interest in holding a private celebration (Art. 6(1)(f) "
        "GDPR). Nothing is passed on for advertising, and there is no "
        "automated decision-making.",
    ),
    (
        "Wie lange",
        "How long",
        "Die Rückmeldungen werden {loeschfrist} gelöscht. Das geschieht "
        "selbsttätig und nicht von Hand — ein Löschversprechen, an das sich "
        "jemand erinnern muss, wird irgendwann vergessen.",
        "Replies are deleted {loeschfrist_en}. This happens automatically "
        "rather than by hand: a promise to delete that someone has to "
        "remember eventually gets forgotten.",
    ),
    (
        "Wo die Daten liegen",
        "Where the data is held",
        "Auf einem Server in der Europäischen Union. Es findet keine "
        "Übermittlung in Drittländer statt. Die Seite selbst lädt zur "
        "Laufzeit nichts von fremden Servern nach: Schriften, Bilder, Musik "
        "und Programmcode liegen alle beim Angebot selbst. Es werden "
        "<strong>keine Cookies</strong> gesetzt und es findet keine Analyse "
        "des Nutzungsverhaltens statt.",
        "On a server in the European Union. There is no transfer to third "
        "countries. The page itself loads nothing from foreign servers at "
        "runtime: fonts, images, music and code all sit with the site. "
        "<strong>No cookies</strong> are set and no usage analysis takes "
        "place.",
    ),
    (
        "Eure Rechte",
        "Your rights",
        "Ihr könnt jederzeit Auskunft über eure gespeicherten Daten "
        "verlangen, sie berichtigen oder löschen lassen, die Verarbeitung "
        "einschränken und der Verarbeitung widersprechen (Art. 15 bis 21 "
        "DSGVO). Eine formlose Nachricht an "
        '<a class="link" href="mailto:{mail}">{mail}</a> genügt. '
        "Außerdem steht euch ein Beschwerderecht bei einer "
        "Datenschutzaufsichtsbehörde zu.",
        "You may at any time request information about your stored data, "
        "have it corrected or deleted, restrict processing and object to it "
        "(Art. 15 to 21 GDPR). An informal message to "
        '<a class="link" href="mailto:{mail}">{mail}</a> is enough. '
        "You also have the right to complain to a data protection "
        "supervisory authority.",
    ),
    (
        "Freiwilligkeit",
        "It is voluntary",
        "Die Rückmeldung ist freiwillig. Ohne sie könnt ihr nur nicht "
        "eingeplant werden — es entstehen keine weiteren Nachteile.",
        "Replying is voluntary. Without it you simply cannot be counted in; "
        "there is no other disadvantage.",
    ),
]

SEITE = """<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Datenschutz — {namen}</title>
<meta name="theme-color" content="#14100C">
<meta name="robots" content="noindex, nofollow">
<link rel="preload" href="assets/fonts/playfair-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/montserrat-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/css/einladung.css">
<link rel="icon" href="assets/img/siegel.svg" type="image/svg+xml">
<style>
  /* Diese Seite hat keinen Umschlag und keine Bewegung. Sie soll gelesen
     werden, nicht wirken. */
  body {{ background: var(--paper); }}
  .recht {{ padding-block: clamp(3.5rem, 12vw, 5.5rem); }}
  .recht h2 {{ font-size: 1.375rem; margin-block: 2.5rem 0.625rem; }}
  .recht h2:first-of-type {{ margin-block-start: 1.5rem; }}
  .recht p {{ color: var(--ink-2); }}
  .zurueck {{
    display: inline-flex; align-items: center; gap: 0.5rem;
    font-size: 0.6875rem; letter-spacing: 0.22em; text-transform: uppercase;
    color: var(--brass); text-decoration: none;
  }}
  .zurueck:hover {{ text-decoration: underline; text-underline-offset: 4px; }}
</style>
</head>
<body class="on-paper">

<main class="section recht" id="main">
  <div class="wrap">
    <a class="zurueck" href="index.html" data-en="Back to the invitation">Zurück zur Einladung</a>
    <p class="eyebrow" style="margin-block-start:2rem">{namen}</p>
    <h1 class="section__title" data-en="Data protection">Datenschutz</h1>
    <p class="lede" data-en="What happens to what you enter in the reply form. Short, because little happens.">Was mit dem geschieht, was ihr im Antwortformular eintragt. Kurz, weil wenig geschieht.</p>

{inhalt}

    <svg class="orn" viewBox="0 0 240 16" aria-hidden="true">
      <g fill="none" stroke="currentColor" stroke-width="1" stroke-linecap="round">
        <path d="M0 8h96M144 8h96"/><path d="M120 2l7 6-7 6-7-6z"/>
        <path d="M104 8c4-4 8-4 9 0-1 4-5 4-9 0zM136 8c-4-4-8-4-9 0 1 4 5 4 9 0z"/>
      </g>
    </svg>
    <p class="small" style="color:var(--ink-2);font-size:.8125rem">
      Stand: {stand}.
    </p>
  </div>
</main>

<script src="assets/js/einladung.js" defer></script>
</body>
</html>
"""


def bauen(daten: dict, werte: dict) -> str:
    """Wird aus build/einladung.py aufgerufen. `werte` sind die bereits
    maskierten Felder der Einladung, damit beide Seiten dieselben Namen
    tragen."""
    import datetime
    import html

    def z(feld, sprache="de"):
        if isinstance(feld, dict):
            return feld.get(sprache) or feld.get("de") or ""
        return feld or ""

    ersatz = {
        "verantwortlich": html.escape(z(daten["recht"]["verantwortlich"])),
        "verantwortlich_en": html.escape(z(daten["recht"]["verantwortlich"], "en")),
        "mail": html.escape(daten["kontakt"]["mail"]),
        "loeschfrist": html.escape(z(daten["recht"]["loeschfrist"])),
        "loeschfrist_en": html.escape(z(daten["recht"]["loeschfrist"], "en")),
        "betreiber": html.escape(daten["recht"].get("betreiber", "der Betreiber dieser Seite")),
    }

    teile = []
    for titel_de, titel_en, text_de, text_en in ABSCHNITTE:
        de = text_de.format(**ersatz)
        en = text_en.format(**{**ersatz, "verantwortlich": ersatz["verantwortlich_en"]})
        # Die englische Fassung steht als Attribut daneben, wie ueberall.
        # Markup im Attribut geht nicht, darum wird sie dort entschaerft.
        en_flach = html.escape(_ohne_markup(en), quote=True)
        teile.append(
            f'    <h2 data-en="{html.escape(titel_en, quote=True)}">{titel_de}</h2>\n'
            f'    <p data-en="{en_flach}">{de}</p>')

    namen = f'{daten["paar"]["a"]} & {daten["paar"]["b"]}'
    return SEITE.format(
        namen=html.escape(namen),
        inhalt="\n\n".join(teile),
        stand=datetime.date.today().strftime("%d.%m.%Y"),
    )


def _ohne_markup(text: str) -> str:
    import re
    return re.sub(r"<[^>]+>", "", text)
