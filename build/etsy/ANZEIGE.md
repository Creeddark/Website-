# Die Etsy-Anzeige

Alles zum Kopieren. Die **fett markierten Lücken** musst du füllen, bevor du
veröffentlichst.

---

## Zuerst: die Demo online stellen

Der QR-Code auf Bild 3 ist der wichtigste Teil der Anzeige — er lässt jemanden
das Produkt anfassen, bevor er zahlt. Er braucht eine Adresse, die dir gehört.

```bash
# 1. netlify.com/drop öffnen, den Ordner themes/ambra daraufziehen.
#    Du bekommst eine Adresse wie zarte-torte-1a2b3c.netlify.app

# 2. Alle Bilder mit dieser Adresse neu erzeugen:
python3 build/etsy/bilder.py https://deine-adresse.netlify.app
python3 build/etsy/pruefung.py https://deine-adresse.netlify.app
```

Die Prüfung liest den QR-Code aus dem fertigen Bild — einmal in voller Größe
und einmal auf 800 Punkte verkleinert, so wie er auf einem Telefonbildschirm
ankommt. Erst wenn beides durchgeht, ist er hochladbar.

---

## Titel

Etsy erlaubt 140 Zeichen. Die ersten 40 entscheiden, ob die Anzeige gefunden
wird — dort gehören die Wörter hin, die jemand wirklich eintippt.

> Digitale Hochzeitseinladung mit RSVP, Umschlag zum Öffnen, Film & Countdown
> – fertig für euch eingerichtet, keine Vorlage, Server in Deutschland

---

## Schlagwörter

Dreizehn Stück, je höchstens zwanzig Zeichen.

```
hochzeitseinladung    digitale einladung    einladung rsvp
save the date         hochzeit website      rsvp online
einladungskarte       hochzeitspapeterie    countdown einladung
digital invitation    wedding website       wedding invitation
elegante einladung
```

---

## Beschreibung

> **Eure Gäste öffnen einen Umschlag.**
>
> Kein PDF im Gruppenchat. Eine eigene Seite unter eurer eigenen Adresse: ein
> cremefarbener Umschlag mit Wachssiegel, der sich auf ein Tippen öffnet.
> Dahinter eure Namen über eurem Film, ein Countdown, eure Geschichte, eure
> Fotos, der Ablauf des Tages — und ein Formular, mit dem eure Gäste antworten.
>
> **Probiert sie aus, bevor ihr bestellt:**
> **‹DEMO-ADRESSE›**
>
> ---
>
> **Was ihr bekommt**
>
> • Eure eigene Adresse, per Nachricht weiterzureichen. Wer den Link teilt,
>   sieht eine Vorschaukarte mit euren Namen.
> • Umschlag mit Wachssiegel, Lasche in echtem 3D.
> • Euer Film als Titelbild — fünf Sekunden in Schleife, stumm.
> • Countdown, eure Geschichte als Zeitstrahl, Galerie, Ablauf des Tages.
> • Karten- und Kalenderknopf: ein Tippen öffnet die Navigation, eines legt
>   den Termin in den Kalender.
> • Rückmeldung, die bei euch ankommt: Zu- und Absage, Personenzahl,
>   Essenswunsch, eine Nachricht. Ihr seht sie jederzeit als Liste und ladet
>   sie als Tabelle herunter.
> • Deutsch und Englisch auf einen Knopfdruck.
> • Server in Deutschland. Keine Cookies, keine Zählpixel, keine Anfragen an
>   fremde Server. Die Antworten eurer Gäste werden vier Wochen nach der
>   Hochzeit von selbst gelöscht.
>
> ---
>
> **So läuft es**
>
> 1. Ihr schreibt uns: Namen, Termin, Ort.
> 2. Wir schicken einen Fragebogen. Eure Geschichte, der Ablauf des Tages,
>    eure Fotos.
> 3. Nach drei Werktagen bekommt ihr einen Link auf eure fertige Einladung.
>    **Erst wenn sie euch gefällt, kommt die Rechnung.**
> 4. Wir schalten sie frei. Ihr bekommt die endgültige Adresse und einen
>    eigenen Zugang zu den Rückmeldungen.
>
> **89 € einmalig, 18 Monate online.** Änderungen in dieser Zeit kosten nichts.
> **Deutsch und Englisch sind enthalten**, wenn ihr die Texte in beiden
> Sprachen liefert. Sollen wir übersetzen, kostet das 29 €.
> Eigene Domain angebunden 39 € · Verlängerung um 12 Monate 19 €
>
> ---
>
> **Ehrlich dazu**
>
> Das hier ist **keine Vorlage zum Selbstbauen**. Ihr bekommt kein Canva-Konto
> und kein Programm, sondern eine fertige Seite, die wir für euch einrichten.
> Sie ersetzt auch keine gedruckte Karte für die Großeltern — wer eine
> braucht, druckt sie zusätzlich.
>
> Sitzplan und Gästeverwaltung kann sie nicht. Sie lädt ein und nimmt
> Antworten entgegen. Mehr nicht, und das mit Absicht.
>
> ---
>
> Fragen? Schreibt uns einfach. Wir antworten am selben Tag.

---

## Einstellungen in Etsy

| Feld | Wert |
|---|---|
| Art | **Digitaler Artikel**, aber **nicht** „Sofort-Download" |
| Herstellung | **Auf Bestellung angefertigt** |
| Bearbeitungszeit | 3–5 Werktage |
| Personalisierung | **an** — Feld: „Eure Namen und euer Hochzeitsdatum" |
| Preis | 89 € |
| Rückgabe | Bei personalisierten digitalen Artikeln ausgeschlossen. **Sag das auch in der Beschreibung**, sonst gibt es Ärger. |

**Kein Sofort-Download.** Etsy würde sonst nach einer Datei fragen, die es
nicht gibt — du lieferst einen Link, und zwar erst, wenn die Seite steht.
„Auf Bestellung angefertigt" ist die richtige Wahl und schützt dich zugleich
beim Widerrufsrecht.

---

## Was Etsy kostet

Bei 89 € gehen etwa **8 €** an Etsy: 0,18 € Einstellgebühr, 6,5 %
Transaktionsgebühr, dazu die Zahlungsabwicklung (rund 4 % + 0,30 €). Rechne
mit **81 € netto** je Verkauf, bevor deine Steuer darauf anfällt.

Ein Verkauf über deine eigene Seite bringt dir die vollen 89 €. Etsy ist
trotzdem der schnellere Anfang: dort suchen Leute bereits nach genau diesem
Produkt. Nimm es als Schaufenster, nicht als Zuhause.

---

## Was du noch brauchst

- **Impressum im Etsy-Shop.** Unter *Shop-Manager → Einstellungen → Info und
  Erscheinungsbild*. Dieselben Angaben wie auf deiner Verkaufsseite.
- **Gewerbeanmeldung**, bevor der erste Verkauf kommt.
- **Kleinunternehmerregelung** in den Steuereinstellungen hinterlegen, falls
  sie für dich gilt.
- **Ein Video.** Etsy erlaubt eines, 5–15 Sekunden, und Anzeigen mit Video
  werden deutlich öfter geklickt. Nimm mit dem Telefon auf, wie sich der
  Umschlag öffnet — das ist der stärkste Moment, den du hast.
