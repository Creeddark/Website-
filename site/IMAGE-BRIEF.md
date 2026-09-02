# Bild-Briefing

Die Website läuft mit **gestalteten Platzhalterflächen** (`.plate`). Sie sehen absichtlich
wie Kunst­richtung aus und nicht wie graue Kästen — aber sie sind kein Ersatz für echte
Bilder. Dieses Dokument sagt, was wohin gehört.

## So ersetzt man einen Platzhalter

Jede Fläche trägt ein `data-img`-Attribut mit ihrem Namen:

```html
<div class="plate plate--4x5" data-img="product-website"></div>
```

wird zu

```html
<img class="plate plate--4x5" src="assets/img/product-website.avif"
     alt="Beschreibender Alternativtext" width="1200" height="1500" loading="lazy">
```

Die Klasse bleibt — sie trägt Seitenverhältnis und Radius. Für Bilder oberhalb des Falzes
(alle `hero-*`, `world-*`, `*-cover`) **kein** `loading="lazy"` setzen.

**Technisch:** AVIF mit WebP-Fallback, `srcset` in vier Größen, Hero-Bilder unter 180 KB.
Jedes Bild braucht einen sinnvollen `alt`-Text — das ist SEO *und* Barrierefreiheitspflicht.

---

## Vor der ersten Veröffentlichung klären

> **Model Release.** Für jedes Bild mit erkennbaren Personen ist eine schriftliche
> Einwilligung nötig — auch bei Kundenfotos, auch „nur für Instagram".
>
> **Lizenz dokumentieren.** Für jedes Element Herkunft und Lizenz schriftlich festhalten.
> Details in `docs/10-legal-and-limits.md`, Abschnitt 6.

Detailaufnahmen (Hände, Stoff, Tisch, Papier, Licht) sind für Weddings oft stärker als
Gesichter — und rechtlich deutlich einfacher.

---

## WEDDINGS — warm, editorial, natürliches Licht

Warme Gradierung, Hautton, Naturmaterialien. Bewegungsunschärfe erlaubt. Keine posierten
Gesichter in die Kamera, kein Konfetti, kein Glitzer.

| Name | Format | Motiv |
|---|---|---|
| `hero-weddings` | füllend, quer | Weite Szene, spätes Licht. Paar klein im Bild oder nur angedeutet. **Dunkle untere Bildhälfte**, dort steht die Typo |
| `world-weddings` | füllend, hoch | Emotionales Schlüsselbild für die Startseite. Nähe, Wärme |
| `product-website` | 4:5 | Handy mit geöffneter Wedding Website, auf einem gedeckten Tisch |
| `product-bundle` | 4:5 | Mehrere Elemente zusammen: Karte, Handy, QR-Aufsteller |
| `product-photoqr` | 4:5 | QR-Aufsteller zwischen Gläsern und Kerzen |
| `invitation`, `inv-main` | 4:5 | Gedruckte Karte mit QR, in der Hand gehalten |
| `inv-paper-vs-digital` | 3:2 | Papierkarte neben Handy mit derselben Gestaltung |
| `inv-thumb-1…4` | 1:1 | Detailaufnahmen: Papierkante, Siegel, QR, Schrift |
| `photoqr-main` | 4:5 | Gast scannt den Code, Bewegung, Abendlicht |
| `photoqr-table` | 3:2 | Aufsteller auf dem Tisch, aus Gastperspektive |
| `photoqr-thumb-1…4` | 1:1 | Galerie-Ausschnitte, wie von Gästen fotografiert |
| `guestbook`, `cross-guestbook` | 3:2 | Jemand tippt eine Nachricht ins Handy, Tisch im Hintergrund |
| `cross-photoqr`, `cross-games` | 3:2 | Gäste in Interaktion mit dem Code |
| `planner` | 3:2 | Aufgeschlagener Planer, Stift, Kaffee, ruhige Draufsicht |
| `site-cover` | füllend | Coverbild wie es in der Wedding Website erscheint |
| `site-map`, `demo-map` | 16:9 / 3:2 | Statische Karte im Markenstil. **Kartenlizenz prüfen** |
| `pdp-guestview-1` | 4:5 | Echter Screenshot der Gästeansicht auf dem Handy |
| `pdp-guestview-wide` | 16:9 | Echter Screenshot im Browserfenster |
| `pdp-thumb-timeline/rsvp/editor/lang` | 1:1 | Echte Screenshots der jeweiligen Ansicht |
| `demo-preview` | 3:4 | Coverbild für die Telefonvorschau auf der Startseite |
| `demo-wedding-cover` | füllend | Coverbild der Demo-Hochzeit. **Untere Hälfte dunkel** |
| `demo-hotel-1…3` | 3:2 | Drei Unterkünfte: Hotel, Landhaus, Ferienhaus |
| `demo-photo-1…4` | 1:1 | Bewusst „von Gästen geknipst" wirkend, nicht perfekt |

---

## HOSPITALITY — kühl, architektonisch, Material

Räume ohne Menschen oder mit Menschen als kleine Figur im Raum. Klare Linien, kühle
Gradierung, Materialtextur: Holz, Stein, Leinen. Lizenzierte Architekturaufnahmen sind hier
unproblematischer als bei Weddings.

| Name | Format | Motiv |
|---|---|---|
| `hero-hospitality` | füllend, quer | Ruhiger Innenraum, Morgenlicht, keine Menschen |
| `world-hospitality` | füllend, hoch | Architektonisches Schlüsselbild für die Startseite |
| `rental-hero` | füllend | Ferienhaus, Küche oder Wohnbereich, aufgeräumt |
| `rental-interior` | 3:2 | Wohnraum mit Charakter, nicht steril |
| `rental-before-after` | 3:2 | **Split:** links Nachrichtenverlauf mit denselben fünf Fragen, rechts der Guide auf dem Handy. Muss ohne Text funktionieren |
| `hotel-hero` | füllend | Boutique-Hotel, Eingang oder Lobby, Abendlicht |
| `hotel-lobby` | 3:2 | Detail mit Handschrift des Hauses: Material, Licht, Objekt |
| `demo-guide-cover` | füllend | Ferienhaus an der Küste. **Untere Hälfte dunkel** |
| `demo-guide-entrance` | 3:2 | Eingang mit Schlüsseltresor |
| `demo-guide-kitchen` | 3:2 | Küche mit Induktionsfeld und Geschirrspüler |
| `demo-guide-living` | 3:2 | Wohnbereich mit Kamin |
| `demo-guide-beach` | 3:2 | Strand, Dünen, Umgebung |
| `demo-guide-exit` | 3:2 | Aufgeräumter Raum, Abreisesituation |
| `demo-guide-host` | 3:2 | Gastgeberin im Türrahmen — **Model Release erforderlich** |

---

## MARKE

| Name | Format | Motiv |
|---|---|---|
| `hero-home` | füllend | Das wichtigste Bild der Marke. Muss **beide Welten** tragen: ein Moment des Empfangens, weder klar Hochzeit noch klar Hotel. Gedeckter Tisch, offene Tür, Licht auf einer Schwelle. **Untere Hälfte dunkel** |
| `custom-hero` | 16:9 | Werkstattcharakter: Entwürfe, Skizzen, Bildschirm |
| `about-portrait` | 3:2 | **Echtes Foto der Gründerinnen und Gründer.** Bis dahin bleibt die About-Seite ehrlich unbesetzt |

---

## Reihenfolge, falls das Budget begrenzt ist

1. `hero-home`, `world-weddings`, `world-hospitality` — die Startseite entscheidet
2. `pdp-guestview-*` und alle `*-thumb-*` — **echte Screenshots**, kosten nur Zeit und wirken stärker als jedes Stockfoto
3. `demo-wedding-cover`, `demo-guide-cover` — die Demos sind der wichtigste Conversion-Hebel
4. `product-*` — Produktkarten
5. `about-portrait` — sobald es die Personen zu zeigen gibt
6. Alles Übrige

**Wichtig:** Die Screenshots unter Punkt 2 sind kostenlos und wirken besser als gekaufte
Bilder. Sie sollten zuerst entstehen, nicht zuletzt.
