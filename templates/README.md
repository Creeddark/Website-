# Event-Vorlagen — Baukasten

Verkaufsfertige Einladungs-Suiten für Etsy. Jede Vorlage ist ein mehrseitiges
Set, das Käufer **in Canva selbst personalisieren**, und liegt gleichzeitig als
Druckdatei in 300 DPI vor.

## Warum das hier Code ist und keine Klick-Arbeit

Drei Gründe, die alle auf denselben Punkt hinauslaufen — Wiederholbarkeit:

1. **Keine fremden Cliparts.** Jedes Blatt, jeder Ballon, jede Fledermaus wird
   von `art.py` gerechnet. Damit gibt es beim Weiterverkauf keine Lizenzfrage,
   und Canvas Einschränkung für Pro-Inhalte greift gar nicht erst.
2. **Eine Änderung, alle Seiten.** Farbe, Format oder Schrift ändern heißt eine
   Zeile ändern und neu bauen — nicht 21 Seiten von Hand nachziehen.
3. **Neue Anlässe kosten Stunden, nicht Tage.** Konfirmation, Einschulung,
   Silvester: neue Datei, vorhandene Bausteine, fertig.

## Aufbau

```
src/
  art.py          Vektor-Kunst: Blattwerk, Kränze, Girlanden, 3D-Kugeln,
                  Schnee, Fledermäuse, Spinnennetz, Verläufe
  common.py       Seitenformat, Schrifteinbettung, Text- und SVG-Helfer
  t01…t06_*.py    je eine Suite
  listings.py     Etsy-Verkaufsbilder aus den gerenderten Seiten
  render.js       schießt Seiten als PNG (Faktor 2 = 300 DPI)
  sheet.js        Kontaktbogen zum Prüfen mehrerer Seiten auf einen Blick
dist/             fertige HTML-Dateien — das ist, was Canva importiert
previews/         Druckvorlagen 1500 × 2100 px
listings/         Etsy-Bilder 2000 × 2000 px
fonts/            Schriften unter SIL Open Font License
```

## Format

750 × 1050 CSS-Pixel = 5 × 7 Zoll. Gerendert mit `deviceScaleFactor 2` sind das
1500 × 2100 Bildpunkte, also echte 300 DPI — die Auflösung, die Käufer für den
Druck erwarten.

## Bauen

```bash
python3 src/t01_wedding_ambra.py          # HTML nach dist/
node src/render.js dist/01-wedding-ambra.html previews
node src/sheet.js /tmp/pruef.png 4 330 previews/01-*.png

python3 src/listings.py                   # alle Verkaufsbilder
node src/render.js dist/_listings.html listings 2 ".sheet" "data-name"
```

## Weg nach Canva

Canva importiert HTML über eine öffentliche HTTPS-Adresse und legt dabei
**jedes `data-document-role="page"` als eigene Designseite** an. Der Text bleibt
echter Text und damit bearbeitbar; die SVG-Ebene wird zu einem Hintergrundbild.
Genau diese Struktur — festes Bild plus freie Textfelder — haben professionelle
Etsy-Vorlagen.

```
https://raw.githubusercontent.com/Creeddark/Website-/refs/heads/<branch>/templates/dist/<datei>.html
```

## Zwei Fallen, die schon zugeschnappt sind

- **Kein Verlauf auf Text.** `background-clip:text` mit transparenter Füllung
  kommt in Canva als *Schwarz* an. Foliengold braucht eine echte Farbe; die
  metallische Wirkung trägt die Grafikebene.
- **Verlaufsradius bei Lichthöfen.** `radial_bg(..., r=0.5)` lässt den Verlauf
  genau am Kreisrand enden. Größere Werte schneiden ihn mittendrin ab — sichtbar
  als harte Kreiskante.
