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
  t01…t11_*.py    je ein System (t11 ist das Anleitungsblatt A4)
  listings.py     Etsy-Verkaufsbilder aus den gerenderten Seiten
  photo_crops.py  schneidet das Beispielfoto auf die vier Bildfenster zu
  demo_render.py  zweiter Durchlauf der Foto-Suiten mit eingesetztem Foto
  video.py        Erklärvideo und Angebotsvideo als HTML-Szene
  copy.py         Etsy-Angebotstexte, geprüft gegen Titel- und Tag-Grenzen
  render.js       schießt Seiten als PNG (Faktor 2 = 300 DPI)
  capture.js      nimmt eine Video-Szene Bild für Bild auf
  encode.sh       Einzelbilder → mp4 (H.264)
  sheet.js        Kontaktbogen zum Prüfen mehrerer Seiten auf einen Blick
dist/             fertige HTML-Dateien — das ist, was Canva importiert
dist-demo/        dieselben Suiten mit Beispielfoto, nur für Verkaufsbilder
previews/         Druckvorlagen 1500 × 2100 px
previews-demo/    dieselben Seiten mit Foto
listings/         Etsy-Bilder 2000 × 2000 px
listing-copy.json Titel, Tags und Beschreibung je Suite
video/            Erklärvideo (1920 × 1080) und Angebotsvideo (1080 × 1080)
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

python3 src/photo_crops.py                # Beispielfoto → vier Zuschnitte
python3 src/demo_render.py                # Foto-Suiten nach previews-demo/

python3 src/copy.py                       # Angebotstexte + Grenzen prüfen
python3 src/listings.py                   # alle Verkaufsbilder
node src/render.js dist/_listings.html listings 2 ".sheet" "data-name"

python3 src/video.py                      # Szenen nach video/*.html
node src/capture.js video/howto-photo-de.html /tmp/f 1280 720 1.5 30
sh src/encode.sh /tmp/f video/howto-photo-de.mp4 30
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

## Verkaufsbilder

Fünf Blätter je Suite, 2000 × 2000 px, alle aus `listings.py`:

| Blatt | Was es beantwortet |
|---|---|
| `-1-hero` | Wie sieht es aus? Zwei Karten gekippt, mit Schatten. |
| `-2-included` | Was bekomme ich? Alle Seiten nebeneinander. |
| `-3-how-it-works` | Kriege ich das hin? Drei Schritte, in den Farben der Suite. |
| `-4-your-photo` | Nur bei Bildfenster: derselbe Entwurf leer und mit Foto. |
| `-5-close-up` | Grossaufnahme, angeschnitten — fällt in der Kachelwand auf. |

## Beispielfoto und Bildfenster

Fünf Suiten haben ein Bildfenster: **THE TIMES** (drei Anlässe) und **COVER**
(zwei). Canva macht daraus beim Import ein austauschbares Bildfeld — der Käufer
zieht sein eigenes Foto darauf und es rastet ein.

Zwei getrennte Fassungen, mit Absicht:

- **Ausgeliefert** wird die Vorlage mit dem neutralen Platzhalter
  (`assets/photo-*.png`, „YOUR PHOTO HERE"). Der sagt dem Käufer im Design
  selbst, was er dort tun soll.
- **Verkaufsbilder und Video** zeigen dieselben Seiten mit einem echten Foto
  (`assets/demo-<anlass>-<fenster>.png`, zugeschnitten aus
  `assets/photo-example-<anlass>.*`). Ein grauer Kasten im Angebotsbild
  verkauft nichts.

Jeder Anlass hat sein eigenes Foto — ein Hochzeitskuss in einer Geburtsanzeige
wäre schlimmer als ein grauer Platzhalter. `demo_render.DEMO_SUITES` ordnet
Suite und Anlass einander zu; wer dort fehlt, behält auch im Verkaufsbild den
Platzhalter. Belegt sind **wedding**, **baby** und **birthday** — damit
haben alle fünf Suiten mit Bildfenster ein Beispielfoto.

Umgeschaltet wird über `common.DEMO_PHOTOS`; `demo_render.py` setzt die
Variable je Suite und schreibt nach `dist-demo/` und `previews-demo/`.

> Die Beispielfotos zeigen erkennbare Personen und stehen in öffentlichen
> Verkaufsbildern — sie brauchen die Zustimmung der Abgebildeten und des
> Fotografen. Zum Austauschen genügt eine neue `photo-example-<anlass>.*`,
> ein Bezugspunkt in `photo_crops.PHOTOS` und ein Lauf von `photo_crops.py`
> und `demo_render.py`.

## Videos

`video.py` baut zwei Szenen als HTML mit einer Funktion `seek(t)`. `capture.js`
ruft sie für jedes Einzelbild auf und schießt ein Foto — kein Bildschirmmitschnitt,
sondern gerechnete Einzelbilder. Dadurch sitzt jedes Bild exakt und ein zweiter
Lauf ergibt dasselbe Ergebnis.

- `howto-photo-<anlass>-{de,en}.mp4` — 1920 × 1080, ~19 s. Nachgebauter
  Canva-Editor, der das Einsetzen des Fotos einmal komplett vorführt. Für den
  Käufer nach dem Kauf.
- `listing-photo-<anlass>-{de,en}.mp4` — 1080 × 1080, 12 s. Nur die Karten,
  das Foto fliegt in den Rahmen. Für das Videofeld der Angebotsseite: dort
  läuft es stumm und klein, eine Bedienoberfläche wäre darin nicht lesbar.

Der Ablauf ist überall derselbe, die Karte und das Foto nicht — `video.SCENES`
hält je Anlass Suite, Foto, Bildfenster und die Texte des Angebotsvideos. Wer
ein Baby-Set kauft, soll im Video sein Set sehen und nicht das der Hochzeit.

Das gebündelte ffmpeg von Playwright kann nur VP8/WebM. Für H.264 kommt das
vollständige ffmpeg aus dem PyPI-Paket `imageio-ffmpeg`.

## Zwei Fallen, die schon zugeschnappt sind

- **Kein Verlauf auf Text.** `background-clip:text` mit transparenter Füllung
  kommt in Canva als *Schwarz* an. Foliengold braucht eine echte Farbe; die
  metallische Wirkung trägt die Grafikebene.
- **Verlaufsradius bei Lichthöfen.** `radial_bg(..., r=0.5)` lässt den Verlauf
  genau am Kreisrand enden. Größere Werte schneiden ihn mittendrin ab — sichtbar
  als harte Kreiskante.
