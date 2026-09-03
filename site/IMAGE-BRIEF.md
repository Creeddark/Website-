# Bild-Briefing

Die Website läuft mit **gestalteten Platzhalterflächen** (`.plate`). Sie sehen
absichtlich nach Kunstrichtung aus und nicht nach grauem Kasten — aber sie sind
kein Ersatz für echte Bilder.

## So ersetzt man einen Platzhalter

Jede Fläche trägt ein `data-img`-Attribut mit ihrem Namen:

```html
<div class="plate plate--3x2" data-img="hero-ferien"></div>
```

wird zu

```html
<img class="plate plate--3x2" src="assets/img/hero-ferien.avif"
     alt="Beschreibender Alternativtext" width="1600" height="1067" loading="lazy">
```

Die Klasse bleibt — sie trägt Seitenverhältnis und Radius. Bei allen `hero-*`
und `*-cover` **kein** `loading="lazy"`, die stehen oberhalb des Falzes.

**Technisch:** AVIF mit WebP-Fallback, `srcset` in vier Größen, Hero-Bilder
unter 180 KB. Jedes Bild braucht einen sinnvollen `alt`-Text — das ist SEO
*und* Barrierefreiheitspflicht.

> **Vor Veröffentlichung klären:** Model Release für jedes Bild mit erkennbaren
> Personen, Lizenz für jedes Element schriftlich dokumentieren. Details in
> `docs/10-legal-and-limits.md`.

---

## Bildsprache

Kühl, architektonisch, real. Räume ohne Menschen oder mit Menschen als kleine
Figur im Raum. Klare Linien, Materialtextur: Holz, Stein, Leinen, Metall.

**Nicht:** gestellte Business-Fotografie, Handshakes, Menschen die auf Laptops
zeigen, übersättigte Bearbeitung.

**Wichtig:** Alle `hero-*` und `*-cover` tragen Text. Sie brauchen eine
**ruhige, eher dunkle Bildhälfte** dort, wo die Typo steht — sonst greift der
Scrim zu stark und das Bild verschwindet.

---

## Marke

| Name | Format | Motiv |
|---|---|---|
| `hero-home` | füllend | Das wichtigste Bild. Muss **alle Bereiche** tragen: eine Schwelle, ein Eingang, ein Ankommen. Weder klar Ferienhaus noch klar Büro. Licht auf einer Tür, ein gedeckter Tisch, ein Flur. Untere Hälfte ruhig |
| `about-portrait` | 3:2 | **Echtes Foto der Gründerinnen und Gründer.** Bis dahin bleibt die Seite ehrlich unbesetzt |
| `produkt-uebersicht` | 16:9 | Echter Screenshot: mehrere Ansichten nebeneinander, auf Gerät oder als Fläche |
| `produkt-technik` | 4:5 | Detail des Editors oder der Gastansicht — **echter Screenshot**, kein Mockup |
| `app-welcome` | füllend | Coverbild in der Telefonvorschau auf der Startseite |

## Segment-Heros

Alle füllend, quer, mit ruhiger unterer Bildhälfte.

| Name | Motiv |
|---|---|
| `hero-ferien` | Ferienhaus-Innenraum oder Eingang, Morgenlicht, aufgeräumt, keine Menschen |
| `hero-hotels` | Boutique-Hotel: Empfang, Flur oder Zimmerdetail. Material und Licht |
| `hero-camping` | Campingplatz früh am Morgen: Stellplätze, Bäume, Sanitärhaus. Nicht Werbe-Camping |
| `hero-events` | Firmenevent: gedeckte Tische im Hof, Lichterkette, vor dem Eintreffen der Gäste |
| `hero-verwaltung` | Mehrfamilienhaus: Eingang, Briefkästen, Treppenhaus. Nüchtern, gepflegt |
| `hero-seminar` | Seminarraum: Stuhlkreis oder U-Form, Tageslicht, leer |

## Demo: Ferienhaus

| Name | Format | Motiv |
|---|---|---|
| `demo-guide-cover` | füllend | Ferienhaus an der Küste. Untere Hälfte ruhig |
| `demo-guide-entrance` | 3:2 | Eingang mit Schlüsseltresor |
| `demo-guide-kitchen` | 3:2 | Küche mit Induktionsfeld und Geschirrspüler |
| `demo-guide-living` | 3:2 | Wohnbereich mit Kamin |
| `demo-guide-beach` | 3:2 | Strand, Dünen, Umgebung |
| `demo-guide-exit` | 3:2 | Aufgeräumter Raum, Abreisesituation |
| `demo-guide-host` | 3:2 | Gastgeberin im Türrahmen — **Model Release erforderlich** |

## Demo: Firmenevent

| Name | Format | Motiv |
|---|---|---|
| `demo-event-cover` | füllend | Gutshof mit gedeckten Tischen, später Nachmittag |
| `demo-event-map` | 3:2 | Statische Karte im Markenstil. **Kartenlizenz prüfen** |

## Demo: Hausinformation

| Name | Format | Motiv |
|---|---|---|
| `demo-haus-cover` | füllend | Mehrfamilienhaus von außen, sachlich |
| `demo-haus-eingang` | 3:2 | Hauseingang mit Klingelschildern und Briefkästen |
| `demo-haus-hof` | 3:2 | Innenhof mit Mülltonnen-Standplatz |
| `demo-haus-flur` | 3:2 | Treppenhaus, Tageslicht |
| `demo-haus-keller` | 3:2 | Waschküche oder Kellergang |
| `demo-haus-technik` | 3:2 | Heizungsraum oder Zählerschrank |

---

## Reihenfolge bei begrenztem Budget

1. **`hero-home`** — die Startseite entscheidet über alles Weitere
2. **`produkt-uebersicht`, `produkt-technik`** — echte Screenshots, kosten nur
   Zeit und wirken stärker als jedes gekaufte Bild
3. **`demo-*-cover`** — die Live-Beispiele sind der wichtigste Conversion-Hebel
4. **`hero-ferien`, `hero-verwaltung`** — die beiden Segmente mit dem größten Potenzial
5. Restliche Segment-Heros
6. **`about-portrait`** — sobald es die Personen zu zeigen gibt

Die Screenshots unter Punkt 2 sind kostenlos und wirken besser als Stockmaterial.
Sie sollten zuerst entstehen, nicht zuletzt.
