# Produktbilder

Zehn Quadrate für Etsy, gebaut aus der Einladung selbst — dieselben Schriften,
dieselben Farben, dieselben Aufnahmen. Nichts wird in einem Grafikprogramm
nachgebaut, das dann doch anders aussieht.

```
build/etsy/
  aufnahmen.py    Telefonaufnahmen aus der laufenden Einladung
  liste.sh        die Liste des Paares, mit erfundenen Antworten
  bilder.py       daraus die zehn Produktbilder
  film.py         das Produktvideo, aufgenommen aus der echten Seite
  pruefung.py     Maße, Dateigröße, und ob der QR-Code wirklich liest
  werkstatt.py    Schriften, Farben, Telefonrahmen
  ANZEIGE.md      Titel, Schlagwörter, Beschreibung zum Kopieren
```

## Erzeugen

```bash
cd themes/ambra && python3 -m http.server 8100 &
python3 build/etsy/aufnahmen.py
bash    build/etsy/liste.sh
python3 build/etsy/bilder.py https://deine-demo-adresse.de
python3 build/etsy/film.py
python3 build/etsy/pruefung.py https://deine-demo-adresse.de
```

Ohne Adresse steht im QR-Code ein Platzhalter, und das Bild sagt das auch —
so lädt niemand versehentlich einen toten Code hoch.

## Die zehn Bilder

| | | |
|---|---|---|
| 0 | Start | Umschlag, Countdown, und die beiden Abzeichen: RSVP und Musik. |
| 1 | Titel | Das Vorschaubild in der Suche. Es hat eine Aufgabe: dass jemand klickt. |
| 2 | Mehr als eine Einladung | Vier Telefone: Umschlag, Film, Countdown, Rückmeldung. |
| 3 | Live-Demo | Der QR-Code. Der wichtigste Teil der Anzeige. |
| 4 | Was Gäste tun können | Karte, Kalender, Galerie, Antwort. |
| 5 | Die Liste | Was nur das Paar sieht. Der Unterschied zur Vorlage von der Stange. |
| 6 | Preis | 15 €, und der Satz „Ihr seht sie, bevor ihr zahlt". |
| 7 | Ablauf | Vier Schritte, fünf Tage. |
| 9 | Zwei Sprachen, ein Server | Deutsch/Englisch, Datenschutz. |
| 10 | Ehrlich dazu | Was sie nicht ist. Das verkauft mehr, als es kostet. |

## Das Video

`film.py` nimmt die echte Seite auf, nicht einen nachgestellten
Zusammenschnitt: der Umschlag öffnet sich wirklich, der Film läuft wirklich,
der Bilderstreifen wandert wirklich. 1080 × 1080, 13 Sekunden, ohne Ton —
Etsy lässt fünf bis fünfzehn Sekunden zu und schaltet den Ton ohnehin stumm.
Die Länge wird nach dem Umwandeln geprüft; liegt sie daneben, bricht das
Skript mit einer Meldung ab.

## Warum der QR-Code geprüft wird

Ein Code, den keine Kamera liest, fällt erst auf, wenn ein Kunde ihn scannt
und nichts passiert. `pruefung.py` liest ihn aus dem fertigen Bild zurück —
einmal in voller Größe und einmal auf 800 Punkte verkleinert, so wie er auf
einem Telefonbildschirm ankommt.

## Wenn sich die Einladung ändert

Aufnahmen neu machen, Bilder neu erzeugen. Beide Schritte dauern zusammen
keine zwei Minuten, und die Bilder zeigen dann wieder das, was du wirklich
lieferst.
