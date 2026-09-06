# Heute verkaufen

Der kürzeste Weg vom jetzigen Stand zur ersten Rechnung. Kein Shop, keine
Kasse, keine Freischaltung bei einem Zahlungsanbieter — das dauert Tage. Eine
Seite mit Preis und eine E-Mail-Adresse dauern Stunden.

**Der Trick liegt in der Reihenfolge:** Du verkaufst heute und lieferst in
fünf Tagen. Genau das steht auch auf der Verkaufsseite. Damit hast du die
Woche, um den RSVP-Server aufzusetzen, während schon Anfragen hereinkommen.

---

## Heute · rund zwei Stunden

### 1 · Die Demo online stellen — 5 Minuten

**netlify.com/drop** öffnen, den Ordner `themes/ambra` daraufziehen. Fertig,
du hast eine HTTPS-Adresse. Notiere sie, nennen wir sie **DEMO-ADRESSE**.

Kein Konto nötig. Wenn du die Adresse hübscher willst: bei Netlify anmelden,
dann lässt sich der Name ändern.

### 2 · Die Verkaufsseite ausfüllen — 30 Minuten

In `verkauf/index.html` stehen **zehn Lücken**. Alle finden:

```bash
grep -n "data-luecke\|DEMO-ADRESSE\|BESTELL-ADRESSE\|TELEFONNUMMER" verkauf/index.html
```

| Was | Wo |
|---|---|
| `DEMO-ADRESSE` (zweimal) | Kopf und Fuß — die Adresse aus Schritt 1 |
| `BESTELL-ADRESSE` | deine E-Mail für Anfragen |
| `TELEFONNUMMER` (zweimal) | oder den Satz ganz löschen |
| Name, Straße, PLZ, Ort | Impressum |
| E-Mail, Telefon | Impressum |
| Umsatzsteuer | entweder deine USt-IdNr. **oder** den Satz zum Kleinunternehmer |
| Verantwortlich für den Inhalt | meist du selbst |
| Löschfrist für Anfragen | z. B. „sechs Monate nach Abschluss" |
| Widerruf an | Name und E-Mail wie im Impressum |
| Markenname | im Fuß |

**Das Impressum ist nicht optional.** Ein geschäftliches Angebot ohne
vollständiges Impressum ist in Deutschland abmahnfähig (§ 5 DDG). Es kostet
dich zwanzig Minuten und spart dir vierstellige Beträge.

### 3 · Die Verkaufsseite online stellen — 5 Minuten

Wieder **netlify.com/drop**, diesmal den Ordner `verkauf`. Das ist die
Adresse, die du überall hinschreibst.

### 4 · Posten — 20 Minuten

Das Video, das du ohnehin drehen wolltest: Umschlag öffnet sich, Countdown,
Galerie. Die Adresse aus Schritt 3 in die Bio.

Was in der Bildunterschrift funktioniert: **was es kostet und wie lange es
dauert.** „15 €, in fünf Tagen fertig" beantwortet die zwei Fragen, die sonst
in den Kommentaren stehen.

### 5 · Auf die erste Anfrage antworten

Antworte am selben Tag, auch wenn es nur zwei Sätze sind. Dann schick den
Fragebogen unten.

---

## Geld nehmen

Für die ersten Kunden brauchst du **keinen Zahlungsanbieter**. Eine Rechnung
per E-Mail und eine Überweisung sind vollkommen ausreichend und sofort
möglich.

Auf die Rechnung gehören: dein Name und deine Anschrift, die des Kunden,
Rechnungsnummer, Datum, Leistung, Betrag — und wenn du Kleinunternehmer bist,
der Satz **„Gemäß § 19 UStG wird keine Umsatzsteuer berechnet."**

Erst wenn regelmäßig Bestellungen kommen, lohnt ein Stripe Payment Link.
Vorher ist es Aufwand ohne Ertrag.

**Kassiere nach der Vorschau, nicht davor.** Das steht so auf der
Verkaufsseite und es ist der beste Verkäufer, den du hast: niemand zahlt für
etwas, das er noch nicht gesehen hat, und fast jeder zahlt für etwas, das ihm
gefällt.

---

## Der Fragebogen

Nach der ersten Antwort. Kopieren, abschicken, fertig.

> Schön, dass ihr dabei seid. Damit wir loslegen können, brauchen wir das hier
> — schreibt einfach in die Mail zurück, Stichworte reichen.
>
> **Ihr beide**
> Wie sollen eure Namen auf der Einladung stehen?
>
> **Der Termin**
> Datum, ab wann die Gäste kommen dürfen, wann die Trauung beginnt.
>
> **Der Ort**
> Name, Straße, PLZ, Ort.
>
> **Eure Geschichte** — drei bis vier Stationen
> Jahr, eine Überschrift, zwei Sätze. Zum Beispiel: „2019 — Ein geliehener
> Schirm — Ein Wolkenbruch vor dem Volkstheater, ein Schirm für zwei."
>
> **Der Ablauf des Tages**
> Uhrzeit, was passiert, ein Satz dazu.
>
> **Was die Gäste wissen müssen**
> Kleiderordnung, Übernachtung, Geschenke. Je drei Zeilen.
>
> **Bis wann sollen die Gäste antworten?**
>
> **Fotos**
> Ein hochkantes Titelbild und drei bis fünf weitere. Am liebsten so groß,
> wie sie aus der Kamera kommen. Wenn ihr einen kurzen Film habt: her damit.
>
> **Auf Englisch dazu?**
> Wenn ja, schickt die Texte gern gleich in beiden Sprachen — sonst
> übersetzen wir.

---

## Die Einladung bauen und ausliefern

```bash
python3 build/kunde.py neu   anna-und-max
# daten.json ausfüllen, Fotos nach kunden/anna-und-max/bilder/
python3 build/art/ambra_fotos.py - - - <foto1> <foto2> <foto3> <foto4>
python3 build/kunde.py bauen anna-und-max
# auslieferung/anna-und-max/ hochladen
```

Ausführlich in `themes/README.md`.

---

## Diese Woche · vor der ersten Auslieferung

### Der RSVP-Server — etwa eine Stunde

Ohne ihn nimmt das Formular keine Antworten entgegen, und Rückmeldungen
stehen auf deiner Verkaufsseite. Ein Server für gut vier Euro im Monat
reicht. Anleitung: `engine/rsvp/README.md`.

### Eine eigene Domain — 15 Minuten, ~15 € im Jahr

Damit aus `zarte-torte-1a2b3c.netlify.app` etwas wird, das man vorlesen kann.
Bei einem Registrar kaufen, dann in Netlify unter *Domain management*
eintragen. Für die Einladungen deiner Kunden brauchst du eine **Wildcard**
`*.deine-marke.de`.

### Gewerbe anmelden

Wer regelmäßig und mit Gewinnabsicht verkauft, betreibt ein Gewerbe. Die
Anmeldung beim Gewerbeamt kostet je nach Stadt 20 bis 60 € und dauert online
oft eine Viertelstunde. Das ist kein Detail, das man nachholt.

### Musik lizenzieren — ~15 € im Monat

Der Klangteppich in der Demo ist selbst erzeugt und damit frei, aber er ist
ein Platzhalter. Für verkaufte Einladungen: Epidemic Sound oder Artlist.

### Die Rechtstexte prüfen lassen

Impressum, Widerruf und die Datenschutzseite der Einladung sind Entwürfe.
Vor dem zehnten Kunden sollte jemand darübersehen, der das darf. Vor dem
ersten reicht Sorgfalt.

---

## Was du heute *nicht* brauchst

Damit du dich nicht daran aufhältst:

- **Keinen Shop.** Bestellungen per E-Mail sind für die ersten zwanzig
  Kunden schneller und persönlicher.
- **Keinen Zahlungsanbieter.** Überweisung genügt.
- **Keine fertige Marke.** Der Name steht im Fuß und lässt sich in einer
  Minute ändern. Warten kostet Wochen.
- **Kein zweites Theme.** Eines, das gut ist, verkauft besser als drei
  mittelmäßige.
- **Keine perfekten Fotos.** Die Demo hat welche. Deine ersten Kunden
  bringen ihre eigenen mit.

---

## Die drei Zahlen

| | |
|---|---|
| Einladung | **15 €**, 18 Monate online |
| Deine Kosten je Kunde | rund **0 €** — Server und Domain laufen ohnehin |
| Deine Zeit je Kunde | **2 bis 3 Stunden**, davon eine für die Fotos |

Ab dem vierten verkauften Exemplar im Monat trägt sich der Server. Alles
darüber ist Ertrag.
