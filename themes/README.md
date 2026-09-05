# Themes

Ein **Theme** ist eine fertige, ausgelieferte Experience: ein Ordner, den man
auf einen statischen Hoster hochlädt, und der unter einer eigenen Subdomain
läuft. Genau so arbeitet der Wettbewerb auch — die Demo im Referenzvideo lief
unter `<themename>.<marke>.com`.

```
themes/
  ambra/                  ← das Theme. Ordner hochladen, fertig.
    index.html            die ganze Einladung, eine Datei
    assets/css|js|fonts|img|audio
```

Keine Frameworks, keine Build-Abhängigkeiten, keine Anfragen an Dritte zur
Laufzeit. Schriften, Musik und Bilder liegen im Ordner.

## Anschauen

```bash
cd themes/ambra && python3 -m http.server 8100
```

Dann <http://localhost:8100>. **Über HTTP öffnen, nicht per Doppelklick** —
`file://` blockiert das Laden der Schriften.

---

## AMBRA

Eine Hochzeitseinladung. Der Umschlag liegt im Dunkeln, im Inneren ist Licht:
die Seite beginnt nachtdunkel, wird beim Lesen zu Papier und endet wieder im
Dunkeln, dort wo die Antwort abgegeben wird.

| Baustein | Zustand |
|---|---|
| Umschlag mit Wachssiegel, 3D-Öffnung | fertig |
| Hero mit Namen, Datum, Ort, langsamer Bildfahrt | fertig, Foto fehlt |
| Countdown, live, mit Zustand „danach" | fertig |
| Zeitstrahl „Unser Weg", zeichnet sich beim Scrollen | fertig |
| Galerie mit Lichtkasten (`<dialog>`) | fertig, Zeichnungen statt Fotos |
| Ablauf des Tages | fertig |
| Ort mit Karten- und Kalenderknopf (.ics im Browser erzeugt) | fertig |
| RSVP mit allen acht Zustandsformen | fertig, sendet nichts |
| Sprachumschalter DE/EN | fertig |
| Musik mit Ein/Aus und weichem Einblenden | fertig, selbst erzeugter Klang |
| `prefers-reduced-motion`, Tastaturbedienung, Kontrast ≥ 4,5:1 | geprüft |

### Was noch fehlt

**Die Fotos.** Der Hero und die Galerie sind für Fotos gebaut, ausgeliefert
werden vorerst Zeichnungen. Das ist kein Notbehelf: ein verkauftes Theme
braucht ein fertiges Aussehen, *bevor* ein Paar eigene Bilder hochlädt.

**Die Anbindung.** Das RSVP-Formular behält alles im Browser. Für einen echten
Kunden muss es an die Engine senden, siehe unten.

---

## Eigene Fotos einsetzen

Die Bildplätze sind bereits verdrahtet. Es reicht, Dateien abzulegen:

| Datei | Format | Wo |
|---|---|---|
| `assets/img/hero.webp` | hochkant, 9:16, ca. 1150 × 2048 | Titelbild. Fehlt es, bleibt Kerzenlicht im Dunkeln stehen. |
| `assets/img/g-1.webp` … `g-5.webp` | hochkant, 3:4, ca. 900 × 1200 | Galerie |

Für die Galerie danach in `index.html` die fünf `src`-Angaben von
`g-ringe.svg` … `g-gut.svg` auf die neuen Dateien umstellen und die
`alt`-Texte anpassen. Die `alt`-Texte sind Pflicht, nicht Zierde.

Der Hero braucht kein Umstellen: `hero.webp` wird bereits geladen und
verschwindet lautlos, solange die Datei fehlt (`data-optional`).

### Bilder erzeugen

Wenn keine echten Fotos vorliegen, lassen sie sich über Higgsfield erzeugen.
Bewährt hat sich `soul_2` (0,12 Credits je Bild); `nano_banana_pro` kostet
rund 2 Credits und lohnt nur für freigestellte Objekte.

Für ein durchgehend gleiches Paar über alle Bilder hinweg: **ein** Porträt
erzeugen, dann dessen `job_id` bei allen weiteren Aufnahmen als
`medias: [{role: "image", value: "<job_id>"}]` mitgeben. Ohne diese Referenz
sieht das Paar auf jedem Bild anders aus, und das fällt sofort auf.

---

## Musik austauschen

`assets/audio/ambra.m4a` ist selbst synthetisiert (`build/art/ambra_ton.py`)
und damit lizenzfrei. **Für eine verkaufte Einladung ist das der Punkt, an dem
man aufpassen muss:** Hintergrundmusik braucht eine Lizenz, auch auf einer
privaten Seite, sobald sie öffentlich abrufbar ist. Epidemic Sound, Artlist
oder eine direkte Lizenz vom Komponisten. Datei ersetzen, Name beibehalten.

Autoplay gibt es nicht, und zwar absichtlich: Browser unterbinden es, und es
gehört sich auch nicht.

---

## Neu erzeugen

```bash
python3 build/art/ambra.py        # Siegel und Galeriezeichnungen (SVG)
python3 build/art/ambra_ton.py    # Klangteppich (24 s, nahtlose Schleife)
python3 build/art/ambra_og.py     # Vorschaukarte 1200×630 für WhatsApp & Co.
```

Alle drei Ergebnisse sind eingecheckt. Die Skripte laufen nur, wenn etwas
geändert werden soll.

---

## Inhalte ändern

Alles steht in `index.html`. Es gibt keine Datenbank und keine Vorlagensprache.

- **Namen, Datum, Ort**: im Hero, im `<title>`, in den `og:`-Angaben und im Fuß.
- **Countdown**: `data-ziel="2027-06-13T14:00:00+02:00"` am Element `[data-uhr]`.
  Zeitzone mit angeben, sonst rechnet jedes Gerät anders.
- **Kalendereintrag**: die `DTSTART`/`DTEND`-Zeilen in `assets/js/einladung.js`
  stehen in UTC.
- **Zweite Sprache**: jedes übersetzbare Element trägt ein `data-en="…"`.
  Der deutsche Text bleibt im Element stehen. Bei Texten mit einem Link darin
  wird nur der Textknoten getauscht, der Link bleibt.

### Weitere Sprachen, auch von rechts nach links

Das Stylesheet arbeitet durchgehend mit logischen Eigenschaften
(`inset-inline-start`, `padding-block`, `border-block-end`). Für Arabisch oder
Hebräisch genügen deshalb `dir="rtl"` am `<html>` und eine passende Schrift;
das Layout spiegelt sich von selbst. Ein weiteres `data-xx`-Attribut je Sprache
und eine dritte Taste in der Leiste, mehr ist nicht nötig.

---

## RSVP wirklich anschließen

Heute fängt `assets/js/einladung.js` das Absenden ab und zeigt nur eine
Quittung. Für einen zahlenden Kunden wird daraus ein `fetch` an die Engine.

Ab diesem Moment werden **Daten fremder Gäste** verarbeitet — von Menschen,
die nie einen Vertrag mit uns geschlossen haben. Damit gilt:

- Auftragsverarbeitungsvertrag mit dem Paar, EU-Hosting, benannte Löschfrist.
- Keine Gratis-Formulardienste für echte Kunden.
- **Keine Abfrage von Allergien oder Unverträglichkeiten.** Das sind
  Gesundheitsdaten nach Art. 9 DSGVO. Das Formular fragt bewusst nur nach einer
  Vorliebe am Tisch (alles / vegetarisch / vegan). Wer mehr braucht, erhebt es
  getrennt, mit eigenem Hinweis und eigener Rechtsgrundlage.

Einzelheiten in `docs/10-legal-and-limits.md` und `docs/07-mvp-and-tech.md`.

---

## Ausliefern

1. Ordner `themes/ambra/` auf einen statischen Hoster laden
   (Cloudflare Pages, Netlify, jeder Webspace).
2. Subdomain darauf zeigen lassen: `ambra.<marke>.de` für die Demo,
   `<paarname>.<marke>.de` für einen Kunden.
3. In `index.html` die `og:image`-Angabe auf die **absolute** Adresse setzen.
   Ein relativer Pfad wird von keinem Vorschaudienst aufgelöst, und dann zeigt
   die geteilte Nachricht eine leere Fläche.
4. `<meta name="robots" content="noindex, nofollow">` steht drin und bleibt
   drin: die Einladung eines Paares gehört nicht in eine Suchmaschine.

---

## Ein neues Theme anlegen

`themes/ambra/` kopieren, umbenennen, Farben in den Tokens oben in
`assets/css/einladung.css` ändern, Zeichnungen neu erzeugen. Aufbau, Bewegung
und Formular bleiben. Das zweite Theme kostet Tage statt Wochen — das ist
derselbe Gedanke wie bei der Engine in `docs/07-mvp-and-tech.md`.
