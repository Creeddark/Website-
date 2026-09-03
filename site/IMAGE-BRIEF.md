# Bildmaterial

Die Website läuft **nicht mehr mit Platzhaltern**. Alle 26 Bildflächen sind
mit eigenen Strichzeichnungen belegt — architektonische Aufrisse im Markenstil,
erzeugt aus `build/art/make.py`.

```bash
python3 build/art/make.py      # erzeugt site/assets/img/*.svg
```

Zusammen 128 KB für 26 Motive. Sie sind Vektorgrafik, also auf jedem Display
scharf, und brauchen keine Lizenz, kein Model Release und keine Bildagentur.

## Warum Zeichnungen und keine Fotos

Wir haben keine lizenzierten Fotos, und ein gekauftes Stockfoto von einem
fremden Ferienhaus wäre eine Behauptung über etwas, das uns nicht gehört. Eine
Zeichnung ist ehrlich: sie erklärt, statt vorzugeben.

Für den Start reicht das vollständig. **Fotos lohnen sich erst, wenn es echte
Kundenobjekte zu zeigen gibt** — dann aber mit schriftlicher Freigabe des
Betreibers.

## Bildsprache

Flacher Aufriss auf einer durchgehenden Grundlinie, feine Linien (2,4–2,8 px im
Koordinatenraum), genau eine getönte Fläche je Motiv — der Telefonbildschirm im
Segmentton. Die linken 25–30 % bleiben bei allen Hero-Motiven frei, dort steht
die Überschrift.

## Motive

| Datei | Einsatz |
|---|---|
| `hero-home` | Startseite. Haus, Wohnblock, Zelt, Telefon — ein Code, viele Orte |
| `hero-ferien` · `hero-hotels` · `hero-camping` | Segment-Heros |
| `hero-events` · `hero-verwaltung` · `hero-seminar` | Segment-Heros |
| `demo-*-cover` | Titelbilder der drei Live-Beispiele |
| `produkt-uebersicht` | Diagramm: aus Bausteinen wird eine Seite |
| `produkt-technik` | Diagramm: Editor → Erzeugung → CDN → Gast |
| `app-welcome` | Telefoninhalt in der Vorschau |
| `demo-guide-*` | Vignetten: Eingang, Küche, Wohnraum, Strand, Abreise, Gastgeberin |
| `demo-haus-*` | Vignetten: Eingang, Hof, Treppenhaus, Waschküche, Technik |
| `demo-event-map` | Schematische Anfahrtskarte |
| `wifi-*` | WLAN-QR-Codes, erzeugt aus den Fakten der Gästeseiten (`build/art/wifi.py`) |

## Ein Motiv ändern

Szenen sind Funktionen in `build/art/make.py`, zusammengesetzt aus Primitiven
(`house`, `block`, `tent`, `tree`, `pavilion`, `phone`, `qr_sign`,
`letterboxes`, `barrier`, `chairs_u`). Funktion anpassen, Skript laufen lassen,
fertig — die Website bindet die Dateien unverändert ein.

Farben kommen aus den Konstanten oben im Skript und entsprechen den
CSS-Tokens. Wird die Palette geändert, muss das Skript einmal neu laufen.

## Wenn später Fotos dazukommen

Ein `<img class="plate …">` gegen ein anderes tauschen — Klasse und
Seitenverhältnis bleiben. Für Hero-Motive gilt dann: **ruhige, eher dunkle
Bildhälfte dort, wo die Typo steht**, sonst greift der Scrim zu stark.

Vor Veröffentlichung: Model Release für erkennbare Personen, Lizenz je Bild
schriftlich dokumentieren (`docs/10-legal-and-limits.md`).
