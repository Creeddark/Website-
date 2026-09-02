# Website

Statische Website für die Marke aus [`../docs/`](../docs/) — beide Welten, alle Seiten,
zwei Live-Demos. Kein Framework, keine Build-Abhängigkeiten, keine Drittanbieter-Anfragen
zur Laufzeit.

```
site/                     ← das ist die Website. Ordner hochladen, fertig.
  index.html              Startseite
  weddings.html           Welt 1
  hospitality.html        Welt 2
  produkte/               Produktseiten und Bundles
  hospitality/            B2B-Landingpages
  demo/                   Live-Demos (eigenes, schlankes Gerüst)
  recht/                  Rechtstexte — Entwürfe, siehe unten
  assets/css|js|fonts|img
  sitemap.xml · robots.txt · 404.html

build/                    Generator (nur für die Entwicklung)
  build.py                setzt pages/ + layout ins fertige HTML
  layout.html             Gerüst mit Header, Navigation, Footer
  layout-bare.html        Gerüst für die Demos
  pages/                  Seiteninhalte mit JSON-Front-Matter
```

## Anschauen

```bash
cd site && python3 -m http.server 8000
```

Dann <http://localhost:8000>. **Über HTTP öffnen, nicht per Doppelklick** — `file://`
blockiert das Laden der Schriften.

## Ändern

Inhalte liegen in `build/pages/`, nicht in `site/`. Nach jeder Änderung:

```bash
python3 build/build.py
```

Der Generator existiert nur, damit Header, Navigation und Footer nicht 22-mal dupliziert
werden. Das Ergebnis in `site/` ist eingecheckt — die Website funktioniert also auch, wenn
niemand den Generator ausführt.

## Markennamen austauschen

`CONVIVIO` ist ein **Arbeitstitel** (Begründung und Alternativen:
[`../docs/11-open-decisions.md`](../docs/11-open-decisions.md)). Zum Wechseln genügt eine
Zeile in `build/build.py`:

```python
BRAND = "CONVIVIO"   # → gewünschter Name
```

Danach neu bauen. Zusätzlich anzupassen: `assets/img/favicon.svg` (der Buchstabe),
die Domain in `sitemap.xml`, `robots.txt` und den `canonical`-Angaben in beiden Layouts.

---

## Was fertig ist

- **Design System** als Token-Satz — eine Typo-Skala, ein Spacing-Raster, eine Motion-Kurve.
  Die beiden Welten unterscheiden sich über `data-world` in genau drei Variablen:
  Farbe, Serif-Anteil, Bildsprache.
- **Selbst gehostete Schriften** (Fraunces + Inter, beide SIL OFL). Keine Anfrage an ein
  fremdes CDN — schneller und ohne Datenschutzfrage.
- **Animationen** nach den Regeln aus `docs/03`: eine Easing-Kurve, drei Dauern,
  Fade-and-Rise, Bild-Reveals, zeilenweiser Text-Reveal, Sticky-Scroll mit wechselnder
  Telefonansicht, Parallax bei maximal 6 % und nur auf Desktop.
  `prefers-reduced-motion` schaltet alles ab.
- **Echte, scannbare QR-Codes** (Fehlerkorrektur H), erzeugt mit `segno` und mit einem
  Decoder gegengeprüft — keine dekorativen Fake-Muster.
- **Zwei Live-Demos** mit funktionierender Interaktion: RSVP, Gästebuch, Foto-Upload
  (alles rein im Browser), Reiter-Navigation in der Gästemappe.
- **Barrierefreiheit:** Sprunglink, sichtbare Fokuszustände, vollständige
  Tastaturbedienung, semantische Überschriften, beschriftete Formularfelder.
  Sämtlicher Text über Bildflächen erreicht WCAG AA (gemessen, nicht geschätzt).
- **Ohne JavaScript** bleiben alle Inhalte lesbar und alle Seiten navigierbar.

## Was noch fehlt

Ehrliche Liste — nichts davon ist versteckt, alles ist im Interface benannt:

| Fehlt | Auswirkung | Nächster Schritt |
|---|---|---|
| **Markenname** | Überall steht der Arbeitstitel | Entscheidung + Markenrecherche |
| **Echte Bilder** | Alle Bildflächen sind gestaltete Platzhalter | [`IMAGE-BRIEF.md`](IMAGE-BRIEF.md) |
| **Checkout** | „In den Warenkorb" sagt, dass noch nichts angebunden ist | Shopify-Storefront, siehe `docs/07` |
| **Formular-Empfänger** | Formulare validieren, senden aber nichts | Endpunkt eintragen, Bestätigungsmail |
| **Rechtstexte** | `recht/` ist ein Gerüst, kein Rechtstext. Per `robots.txt` von der Indexierung ausgenommen | Fachanwalt für IT-Recht, `docs/10` |
| **Experience Engine** | Die Demos sind statisch nachgebaut, es gibt kein Backend | `docs/07-mvp-and-tech.md` |
| **Zweite Sprache** | Aktuell nur Deutsch mit englischen Markenclaims | `hreflang` + EN-Variante, `docs/11` |

Kein Formular und kein Knopf täuscht Erfolg vor. Wo etwas noch nicht funktioniert, steht
das dort, wo geklickt wird.

## Weg nach Shopify

Die Seiten sind so geschnitten, dass sie sich als Sections übertragen lassen: jede Sektion
ist ein eigener `<section>`-Block mit Kommentarkopf, alle Farben und Abstände kommen aus
CSS-Variablen. Für die Übernahme in ein Dawn-basiertes Theme wird aus jedem Block eine
`.liquid`-Section; `site.css` und `site.js` wandern unverändert in `assets/`.
Die Welten-Umschaltung läuft über `data-world` am `<body>` und lässt sich in Liquid direkt
aus dem Template-Suffix setzen.
