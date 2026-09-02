# 03 — Design System & Visuelle Identität
*Briefing §13–16: Design, visuelle Identität, Animationen, Produkt-Mockups*

Ziel: eine Marke, die aussieht wie ein internationales Premium-Haus — ohne Kopie einer
bestehenden Marke. Die Differenzierung entsteht **nicht** über ein auffälliges Element,
sondern über **Zurückhaltung mit Präzision**: großes Typo-Kontrastverhältnis, viel Luft,
wenige Farben, langsame Bewegung, fehlerfreie Details.

---

## 1. Das Grundprinzip: ein System, zwei Belichtungen

Weddings und Hospitality nutzen **dieselbe Typo-Skala, dasselbe Spacing, dieselbe Geometrie,
dieselbe Motion-Kurve**. Sie unterscheiden sich in genau drei Variablen:

| Variable | Weddings | Hospitality |
|---|---|---|
| **Farbe** | warm (Ivory / Sand / Taupe) | kühl (Off-white / Stone / Slate-Green) |
| **Typo-Verhältnis** | ~60 % Serif | ~30 % Serif |
| **Bildsprache** | Menschen, Haut, Licht, warm gradet | Räume, Architektur, Material, kühl gradet |

Das reicht vollständig aus, damit sich zwei Welten anfühlen — und ist gleichzeitig billig zu
bauen und zu pflegen (ein Token-Set, zwei Wertelisten).

---

## 2. Logo-System

**Wortmarke, keine Bildmarke.** Begründung: eine Bildmarke muss man bekannt machen, bevor sie
etwas bedeutet — das kostet Jahre und Budget. Eine gut gesetzte Wortmarke wirkt ab Tag 1
souverän und ist markenrechtlich leichter durchzusetzen.

```
Primär          [MARKE]                      Serif, Versalien, Tracking +0.18em
Welt-Lockup     [MARKE]                      Deskriptor: Sans, 11px, Tracking +0.22em,
                W E D D I N G S              optisch 40 % der Wortmarkenbreite, linksbündig

                [MARKE]
                H O S P I T A L I T Y

Signet          [M]                          Nur für Favicon, App-Icon, QR-Mitte, Siegel
Endorsement     A [MARKE] EXPERIENCE         Fußzeile in jeder ausgelieferten Kunden-Experience
```

**Regeln**
- Schutzraum = Höhe des Versalbuchstabens rundum.
- Minimalgröße: 96 px Breite digital, 24 mm Print.
- Nur einfarbig: `ink-900` auf hell, `ivory` auf dunkel. Kein Verlauf, kein Schatten, keine Outline.
- Das Logo wird **nie** eingefärbt, nie verzerrt, nie gedreht, nie über unruhige Bildbereiche
  gelegt.
- In jeder ausgelieferten Kunden-Experience steht dezent das Endorsement im Footer. Das ist
  auf Dauer die günstigste Reichweitenquelle des Unternehmens — jeder Hochzeitsgast sieht es.
  (Bei Hospitality Pro/Hotel entfernbar — genau deshalb ist White Label ein bezahltes Feature.)

---

## 3. Typografie

### Schriftwahl — und warum Open Source hier die bessere Entscheidung ist

Wir liefern Schrift **nicht nur auf unserer Website aus, sondern in jede Kunden-Experience**.
Kommerzielle Webfont-Lizenzen sind fast immer nach Domains oder Pageviews bemessen — bei
tausenden Kunden-Subdomains ist das rechtlich und finanziell nicht handhabbar. Open-Source-
Schriften (SIL OFL) lösen das Problem vollständig und kosten nichts.

| Rolle | Schrift | Lizenz | Warum |
|---|---|---|---|
| **Display / Serif** | **Fraunces** (Variable) | SIL OFL | Editorial, hoher Kontrast, optische Größenachse — wirkt bei großen Headlines teuer, bleibt klein lesbar |
| **UI / Sans** | **Inter** (Variable) | SIL OFL | Neutral, exzellent bei kleinen Größen, sehr breite Sprachabdeckung (wichtig für internationale Gästelisten) |
| Alternative Serif | Instrument Serif | SIL OFL | Höherer Kontrast, noch editorialer — Option, falls Fraunces zu weich wirkt |

Alle Fonts werden **selbst gehostet** (WOFF2, `font-display: swap`, subsetted, preload für
den Display-Cut). Kein Google-Fonts-CDN — das ist gleichzeitig schneller und erspart die
DSGVO-Diskussion.

### Typo-Skala (Major Third, 1.250)

| Token | Desktop | Mobile | Schrift | Tracking | Zeilenhöhe |
|---|---|---|---|---|---|
| `display-xl` | 88 px | 44 px | Fraunces 300 | −0.02em | 1.02 |
| `display-l` | 64 px | 36 px | Fraunces 300 | −0.02em | 1.06 |
| `display-m` | 44 px | 30 px | Fraunces 400 | −0.01em | 1.12 |
| `heading` | 28 px | 24 px | Fraunces 400 | 0 | 1.24 |
| `subhead` | 20 px | 18 px | Inter 400 | 0 | 1.45 |
| `body` | 17 px | 16 px | Inter 400 | 0 | 1.62 |
| `small` | 14 px | 14 px | Inter 400 | 0 | 1.55 |
| `label` | 11 px | 11 px | Inter 500, Versalien | **+0.22em** | 1.2 |

Der `label`-Stil mit weitem Tracking ist das wiedererkennbarste Element des Systems. Er
markiert Sektionen, Kategorien und Buttons — und ist der Hauptgrund, warum die Seite
„editorial" statt „Web" wirkt.

**Satzregeln**
- Fließtext max. **68 Zeichen** pro Zeile.
- Headlines mit manuellen Umbrüchen an sinnvollen Stellen, nie automatisch umbrechen lassen.
- Keine Blocksatz-Ausrichtung, keine Silbentrennung in Headlines.
- Deutsche Anführungszeichen im DE-Text („…"), englische im EN-Text ("…").

---

## 4. Farbe

### Neutrale Basis (in beiden Welten identisch)

| Token | Hex | Verwendung |
|---|---|---|
| `ink-900` | `#1C1A17` | Text, Logo, Primär-Button |
| `ink-700` | `#3A3630` | Überschriften auf hell |
| `ink-500` | `#6B655C` | Sekundärtext |
| `ink-300` | `#A8A197` | Hinweise, deaktiviert |
| `line` | `#E2DCD2` | Trennlinien (1 px) |

### WEDDINGS — warm

| Token | Hex | Verwendung |
|---|---|---|
| `bg` | `#FBF8F3` | Ivory — Seitenhintergrund |
| `surface` | `#F4EEE5` | Karten, abgesetzte Sektionen |
| `sand` | `#E8DCCB` | Flächen, Bildrahmen |
| `accent` | `#B79C86` | Taupe — Links, Hover, feine Akzente |
| `deep` | `#2A2521` | Dunkle Sektionen, Footer |

### HOSPITALITY — kühl

| Token | Hex | Verwendung |
|---|---|---|
| `bg` | `#F7F7F5` | Off-white |
| `surface` | `#ECECE8` | Karten |
| `stone` | `#DCDCD6` | Flächen |
| `accent` | `#3D4A43` | Slate-Green — Links, Hover |
| `deep` | `#1B1E1C` | Dunkle Sektionen |

### Farbregeln

1. **Maximal zwei Nicht-Neutrale pro Screen.** Alles andere ist Neutral.
2. Der Akzent wird **nie** großflächig eingesetzt — nur als Linie, Link, kleiner Punkt oder
   Hover-Zustand. Premium entsteht durch Zurückhaltung.
3. Keine reinen Schwarz-/Weißwerte (`#000` / `#FFF`) — sie wirken hart und billig.
4. Kontrast: Fließtext ≥ 4.5:1, große Typo ≥ 3:1 (WCAG AA). `ink-300` nie für Fließtext.
5. **Systemfarben** (Erfolg / Warnung / Fehler) sind gedeckt, nicht grell:
   `#4A6355` / `#8A6A34` / `#8B4438`.

---

## 5. Raster, Abstand, Geometrie

| | |
|---|---|
| **Grid** | 12 Spalten, Gutter 24 px |
| **Content-Breite** | max. 1.280 px; Fließtext max. 720 px |
| **Seitenränder** | 20 px mobil · 48 px Tablet · 80 px Desktop |
| **Spacing-Skala** | 4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 96 · 128 · 160 |
| **Sektionsabstand** | 96 px mobil · 160 px Desktop |
| **Radius** | **2 px** — fast eckig. Runde Ecken lesen als „App", Kanten lesen als „Print" |
| **Rahmen** | 1 px `line`. Nie 2 px, nie gestrichelt |
| **Schatten** | grundsätzlich **keine**. Tiefe entsteht über Fläche und Abstand, nicht über Weichzeichner |

---

## 6. Komponenten

### Buttons

| Variante | Aussehen | Einsatz |
|---|---|---|
| **Primary** | Fläche `ink-900`, Text `bg`, Höhe 56 px, `label`-Stil, Radius 2 px | Ein Primär-CTA pro Sichtbereich |
| **Secondary** | 1 px Rahmen `ink-900`, transparent | Zweite Option (z. B. die andere Welt) |
| **Tertiary** | Text + 1 px Unterlinie mit 6 px Abstand, Pfeil → | Inline-Links, „Alle ansehen" |

Hover: 180 ms, Fläche → `ink-700`, kein Skalieren, kein Schatten, kein Farbwechsel.
Fokus: 2 px Outline `accent`, Offset 3 px — **nie** entfernen (Barrierefreiheit + Rechtssicherheit).

### Cards
Kein Rahmen, kein Schatten. Struktur: Bild (4:5 Weddings · 3:2 Hospitality) → `label`-Kategorie
→ `heading`-Titel → einzeiliger Text → Preis. Hover: nur das Bild zoomt auf 1.03 über 700 ms.

### Formulare
Feldhöhe 56 px, Label **über** dem Feld (nie Placeholder als Label), 1 px Unterlinie statt
Box, Fehlermeldung unter dem Feld in gedecktem Rot, nie als Popup.

### Icons
24 px Raster, 1.25 px Strichstärke, keine Füllung, runde Enden. Sparsam — maximal ein
Icon-Set pro Sektion. Nie Emoji in der Produktoberfläche.

---

## 7. Bildsprache

**Weddings** — Menschen, Nähe, Bewegungsunschärfe erlaubt, natürliches Licht, warme
Gradierung (+ leichter Gelb/Magenta-Lift in den Lichtern). Detailaufnahmen (Hände, Stoff,
Tisch, Blumen) sind oft stärker als Gesichter — und rechtlich einfacher.

**Hospitality** — Räume ohne Menschen oder mit Menschen als kleine Figur im Raum,
architektonische Linien, kühle Gradierung, klare Kanten, Materialtextur (Holz, Stein, Leinen).

**Verboten in beiden Welten**
- Offensichtliche Stockfotografie mit posierten Gesichtern in die Kamera
- Confetti-, Glitzer-, Herz-Overlays
- Übersättigte oder HDR-artige Bearbeitung
- Bilder mit erkennbaren Personen **ohne schriftliches Model Release**
  (siehe [10 — Recht](10-legal-and-limits.md#6-lizenzen-und-rechte-an-material))

**Technisch:** AVIF mit WebP-Fallback, `srcset` in 4 Größen, LQIP-Platzhalter,
Hero-Bild < 180 KB, alles unterhalb des Falzes `loading="lazy"`, jedes Bild mit sinnvollem
`alt` (SEO **und** Barrierefreiheitspflicht).

---

## 8. Motion

**Prinzip: Premium = Kontrolle.** Bewegung darf nie um ihrer selbst willen stattfinden. Jede
Animation hat genau einen Zweck — Aufmerksamkeit lenken, Zustandswechsel erklären oder
räumliche Beziehung zeigen.

| Token | Wert |
|---|---|
| `ease` | `cubic-bezier(0.22, 1, 0.36, 1)` — **die einzige erlaubte Kurve** |
| `fast` | 180 ms — Hover, Fokus |
| `base` | 400 ms — Ein-/Ausblenden, Akkordeon |
| `slow` | 700 ms — Bild-Reveals, Sektionswechsel |

**Erlaubtes Repertoire**

| Effekt | Umsetzung |
|---|---|
| Fade + Rise | `opacity 0→1`, `translateY 16px→0`, 700 ms, Trigger bei 12 % Sichtbarkeit |
| Stagger | 60 ms Versatz, max. 5 Elemente in Folge |
| Image Reveal | Maske von unten, 900 ms, nur bei Hero- und Sektionsbildern |
| Text Reveal | zeilenweise, nur für **eine** Headline pro Seite (Hero) |
| Sticky Section | Weltenwahl auf der Homepage, Produkt-Feature-Scroll |
| Hover | Bildzoom 1.03, Linien-Underline, Button-Flächenwechsel |
| Parallax | max. **6 %** Versatz, **nur Desktop**, nur Hintergrundbilder |

**Hart verboten:** Bounce, Elastic, Rotation, Konfetti, automatisch laufende Karussells,
Scroll-Hijacking, Ladeanimationen über 400 ms, Zahlen-Counter, Cursor-Follower.

**Pflicht:** `@media (prefers-reduced-motion: reduce)` schaltet alle Reveals, Parallax und
Bild-Zooms ab — Inhalte erscheinen sofort in ihrem Endzustand. Das ist keine Option.

### Performance-Budget (verbindlich)

| Kennzahl | Grenze |
|---|---|
| LCP | < 2,0 s (4G, Mobile) |
| CLS | < 0,05 |
| INP | < 200 ms |
| JS gesamt (Storefront) | < 150 KB gzip |
| Hero-Bild | < 180 KB |
| Fonts | ≤ 3 Cuts, WOFF2, subsetted |

Wenn eine Animation das Budget bricht, fliegt die Animation — nicht das Budget.

---

## 9. Produkt-Mockups & Live-Demos

Digitale Produkte haben ein Grundproblem: **man kann sie nicht anfassen.** Deshalb ist die
Darstellung des Produkts nicht Deko, sondern der wichtigste Conversion-Faktor.

### Rangfolge der Wirksamkeit

1. **Live-Demo** — der Kunde öffnet das echte Produkt. Nichts überzeugt so stark. **Pflicht
   für jedes Hero-Produkt.** Ohne Login, ohne Formular, ein Klick.
2. **Bildschirmaufnahme (Video, 8–15 s, stumm, Loop)** — echtes Scrollen, echte Interaktion.
3. **Statisches Gerätemockup** — schön, aber am schwächsten. Nur als Ergänzung.

### Regeln für Mockups
- Nur **echte** Screenshots aus dem echten Produkt. Nie gezeichnete Fake-Oberflächen.
- Neutrale Geräterahmen, keine Markenlogos auf den Geräten, keine schrägen 3D-Perspektiven.
- Realistischer Inhalt (echte Namen, echte Zeiten, echte Orte) — Lorem Ipsum zerstört Vertrauen.
- Immer auch die **Gästesicht** zeigen, nicht nur die Adminsicht. Der Käufer will wissen:
  *„Was sehen meine Gäste?"*

### QR-Interaktion als Signature-Element
Der QR-Code ist das einzige Element, das digital und physisch verbindet — und damit unser
stärkstes visuelles Erkennungszeichen. Regeln: immer im Markenrahmen mit `label`-Zeile
darunter, ausreichend Ruhezone, Signet in der Mitte, Fehlerkorrektur Level H, nie kleiner als
28 mm im Print, **immer vor dem Druck auf drei Geräten getestet**.
