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

### Prüfen

```bash
python3 themes/pruefung/galerie.py   # 12 Prüfungen, braucht den Server oben
```

Der Bilderstreifen rückt von selbst weiter und muss dabei ein halbes Dutzend
Regeln einhalten — wer selbst wischt, hat das Sagen; ein Tipp aufs Foto ist
kein Wischen; bei reduzierter Bewegung passiert nichts. Die stehen dort als
Prüfungen, damit der nächste Umbau sie nicht still umdreht.

### Zum Verschicken

```bash
python3 build/artefakt.py themes/ambra vorschau.html "Marlene &amp; Anton"
```

Faltet den ganzen Ordner in **eine** Datei: Schriften, Fotos, Film und Ton
wandern als Daten-URLs ins HTML. Die Datei läuft ohne Server und ohne
Nachbardateien — gut für eine Vorschau, die jemand nur anschauen soll.

Für die Auslieferung ist das der falsche Weg: dort will man den Film erst
auf Verlangen laden und Dateien, die der Browser behalten kann. Darum fehlt
in der gefalteten Datei das WebM, und der Kalenderknopf sagt statt zu laden,
dass er das nur auf der fertigen Seite tut.

---

## AMBRA

Eine Hochzeitseinladung. Der Umschlag liegt im Dunkeln, im Inneren ist Licht:
die Seite beginnt nachtdunkel, wird beim Lesen zu Papier und endet wieder im
Dunkeln, dort wo die Antwort abgegeben wird.

| Baustein | Zustand |
|---|---|
| Umschlag mit Wachssiegel, 3D-Öffnung | fertig |
| Hero als Film, stumm in Schleife, mit Standbild als Rückfallebene | fertig |
| Countdown, live, mit Zustand „danach" | fertig |
| Zeitstrahl „Unser Weg", zeichnet sich beim Scrollen | fertig |
| Galerie mit Lichtkasten (`<dialog>`) | fertig, vier Fotos |
| Ablauf des Tages | fertig |
| Ort mit Karten- und Kalenderknopf (.ics im Browser erzeugt) | fertig |
| RSVP mit allen acht Zustandsformen | fertig, sendet an den Dienst |
| Sprachumschalter DE/EN | fertig |
| Musik mit Ein/Aus und weichem Einblenden | fertig, selbst erzeugter Klang |
| `prefers-reduced-motion`, Tastaturbedienung, Kontrast ≥ 4,5:1 | geprüft |
| Inhalt in `daten.json`, HTML wird erzeugt | fertig |
| Datenschutzseite, sobald gesendet wird | fertig, Entwurf |

### Was noch fehlt

**Mehr Abwechslung in der Galerie.** Vier Kacheln im Zweierraster, davon zwei
Porträts. Weitere Aufnahmen sollten Details ohne Gesichter sein (Hände, Tafel,
Schleier), weil die Frage der Wiedererkennbarkeit dort gar nicht erst entsteht
und die Galerie sonst zu porträtlastig wird.

---

## Eigene Fotos einsetzen

Es gibt ein Skript dafür, damit bei jedem Kunden nicht von Hand zugeschnitten
werden muss:

```bash
python3 build/art/ambra_fotos.py <hero> <siegel> <papier> <kachel> [<kachel> ...]
```

Es beschneidet auf das richtige Verhältnis, verkleinert auf die Zielgröße,
schreibt WebP und **stellt das Siegel frei**: der weiße Grund wird von den
Bildecken her weggeflutet, die Glanzlichter im Wachs bleiben stehen. Ein
globaler Helligkeitsfilter würde die mit wegnehmen.

| Datei | Format | Wo |
|---|---|---|
| `assets/img/hero.webp` | hochkant 9:16, Ziel 1080 × 1920 | Titelbild. Fehlt es, bleibt Kerzenlicht im Dunkeln stehen. |
| `assets/img/siegel.webp` | freigestellt, mit Alphakanal | das Siegel auf dem Umschlag |
| `assets/img/papier.webp` | quadratisch, Ziel 700 × 700 | Faserung aller Papierflächen des Umschlags |
| `assets/img/g-1.webp` … | hochkant 3:4, Ziel 900 × 1200 | Galerie |

Hochskaliert wird bewusst nicht: ein weichgerechnetes Bild sieht schlechter
aus als ein kleines, das der Browser selbst skaliert.

Kommen weitere Kacheln dazu, in `index.html` ein `<li>` ergänzen. Die
`alt`-Texte sind Pflicht, nicht Zierde, und jedes Bild trägt zusätzlich ein
`data-alt-en` für die englische Fassung.

### Vorlagen hereinreichen

**Der Weg über den Chat verkleinert Bilder auf 384 px Breite.** Was dort
angezeigt wird, ist eine Vorschau; wer sie sichert, sichert die Vorschau. Die
Originale gibt es nur über den Download-Knopf beim Generator selbst.

Der zuverlässige Weg: die Dateien direkt in den Branch laden, auf GitHub
**Add file → Upload files** in `themes/ambra/assets/img/`, dann
`build/art/ambra_fotos.py` laufen lassen und die Vorlagen wieder löschen.
Sie gehören nicht in einen Ordner, der als fertiges Theme ausgeliefert wird.

Video verkleinert der Chat nicht, das kommt unangetastet durch.

Die gezeichneten Blätter (`g-ringe.svg` und die vier anderen) bleiben im
Ordner. Sie sind der Stand für ein Paar, das noch keine Fotos hochgeladen hat.

### Bilder erzeugen

Wenn keine echten Fotos vorliegen, lassen sie sich über Higgsfield erzeugen.
Bewährt hat sich `soul_2` (0,12 Credits je Bild); `nano_banana_pro` kostet
rund 2 Credits und lohnt nur für freigestellte Objekte.

Für ein durchgehend gleiches Paar über alle Bilder hinweg: **ein** Porträt
erzeugen, dann dessen `job_id` bei allen weiteren Aufnahmen als
`medias: [{role: "image", value: "<job_id>"}]` mitgeben. Ohne diese Referenz
sieht das Paar auf jedem Bild anders aus, und das fällt sofort auf.

Zwei Fallstricke, beide selbst erlebt:

- **Sobald ein Referenzbild anhängt, schreibt Higgsfield den Prompt um**
  (`enhance_prompt`). Aus „Eröffnungstanz unter dem Kronleuchter" wurde
  dreimal dieselbe Nahaufnahme wie im Referenzbild. Szenen also ohne Referenz
  erzeugen, Wiedererkennbarkeit über Aufnahmen ohne Gesichter lösen.
- **`nano_banana` stempelt auf dem Free-Plan ein Wasserzeichen unten rechts
  hinein**, `soul_2` nicht. `ambra_fotos.py` fängt das ab: beim Papier wird
  nur die Mitte des Bogens genommen, beim Siegel bleibt nach dem Freistellen
  nur der größte zusammenhängende Fleck stehen und der Stempel fällt heraus.
  Verlassen sollte man sich darauf trotzdem nicht.

---

## Der Hero-Film

`assets/video/hero.mp4` und `hero.webm` sind derselbe fünf Sekunden lange
Clip in zwei Formaten. Der Browser nimmt das erste, das er abspielen kann:
VP9 ist kleiner, H.264 läuft überall, insbesondere auf älteren iPhones.

Erzeugt hat ihn `build/art/ambra_film.py` aus einem Rohclip von 15 MB. Übrig
bleiben 0,49 bzw. 0,63 MB. Drei Dinge sind dabei nicht verhandelbar:

- **`-movflags +faststart`.** Ohne das liegen die Kopfdaten am Dateiende und
  die Wiedergabe beginnt erst, wenn alles geladen ist.
- **Keine Tonspur.** Der Film ist stumm, die Musik läuft getrennt und nur auf
  Knopfdruck.
- **Das Standbild kommt aus dem Film selbst** (erstes Vollbild). Käme es aus
  einer anderen Quelle, sähe man beim Übergang einen Sprung in Farbe und
  Ausschnitt.

So verhält sich die Seite:

| Fall | Was passiert |
|---|---|
| Vor dem Öffnen | Film wird **nicht** angefordert, erste Ansicht bleibt bei 264 KB |
| Nach dem Öffnen | lädt, spielt stumm in Schleife, blendet über 1,2 s ein |
| Sobald er läuft | die Kamerafahrt des Standbilds hält an |
| Datei fehlt oder Format wird nicht unterstützt | Videoelement verschwindet lautlos, Standbild plus Kamerafahrt bleiben |
| `prefers-reduced-motion` | Film wird nie angefordert |

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
python3 build/art/ambra_film.py <rohclip.mp4>   # Hero-Film in Webgröße
```

Alle drei Ergebnisse sind eingecheckt. Die Skripte laufen nur, wenn etwas
geändert werden soll.

---

## Inhalte ändern

**Alles steht in `themes/<theme>/daten.json`.** Das HTML wird daraus erzeugt:

```bash
python3 build/einladung.py ambra
```

Für einen neuen Kunden wird `daten.json` kopiert und geändert, nicht das HTML
durchgesehen. Sonst steht nach dem dritten Paar im Fuß noch das Datum des
zweiten.

Das erzeugte `index.html` ist eingecheckt — die Einladung funktioniert also
auch ohne den Generator. Er existiert nur, damit derselbe Text nicht an neun
Stellen steht.

Jeder Text steht als `{de, en}` da. Fehlt `en`, bleibt beim Umschalten der
deutsche Text stehen; eine leere Zeile wäre schlimmer.

| Feld in `daten.json` | wirkt auf |
|---|---|
| `paar`, `termin`, `ort` | Hero, `<title>`, `og:`-Angaben, Fuß, Beschreibung |
| `termin.beginn` | den Countdown. **Zeitzone mit angeben**, sonst rechnet jedes Gerät anders |
| `weg.punkte` | den Zeitstrahl. Beliebig viele; die Einblendung staffelt sich von selbst |
| `galerie.bilder` | die Kacheln. Beliebig viele, `alt` ist Pflicht |
| `ablauf.punkte`, `wo.hinweise` | Tagesablauf und die Liste darunter |
| `rsvp.endpunkt` | ob wirklich gesendet wird, siehe unten |
| `vorschau` | den Streifen am Fuß, der sagt, dass alles erfunden ist |

Der Kalendereintrag kommt aus `kalender` in derselben Datei, Zeiten in UTC.
Er steht als Attribute am Knopf, nicht im JavaScript — stünde er dort, trüge
das zweite Paar die Hochzeit des ersten in seinen Kalender ein.

### Weitere Sprachen, auch von rechts nach links

Das Stylesheet arbeitet durchgehend mit logischen Eigenschaften
(`inset-inline-start`, `padding-block`, `border-block-end`). Für Arabisch oder
Hebräisch genügen deshalb `dir="rtl"` am `<html>` und eine passende Schrift;
das Layout spiegelt sich von selbst. Ein weiteres `data-xx`-Attribut je Sprache
und eine dritte Taste in der Leiste, mehr ist nicht nötig.

---

## RSVP anschließen

Ohne `rsvp.endpunkt` bleibt die Antwort im Browser — so verhält sich die
öffentliche Vorschau, und der Hinweis unter dem Knopf sagt das auch. Mit
Endpunkt geht sie an den Dienst unter `engine/rsvp/`:

```json
"rsvp": {
  "endpunkt": "https://rsvp.marke.example",
  "kennung": "marlene-anton",
  "frist": "2027-03-01"
}
```

Danach `python3 build/einladung.py`. Das erzeugt zusätzlich
`datenschutz.html` und verlinkt sie unter dem Formular und im Fuß.

Aufbau und Betrieb des Dienstes: **`engine/rsvp/README.md`**.

### Ab hier gilt Datenschutzrecht

Vom ersten gesendeten Byte an werden **Daten fremder Gäste** verarbeitet — von
Menschen, die nie einen Vertrag mit uns geschlossen haben. Damit gilt:

- Auftragsverarbeitungsvertrag mit dem Paar, EU-Hosting, benannte Löschfrist.
  Die Frist greift im Dienst von selbst; ein Löschversprechen, an das sich
  jemand erinnern muss, wird irgendwann vergessen.
- Keine Gratis-Formulardienste für echte Kunden.
- **Keine Abfrage von Allergien oder Unverträglichkeiten.** Das sind
  Gesundheitsdaten nach Art. 9 DSGVO. Das Formular fragt bewusst nur nach
  einer Vorliebe am Tisch (alles / vegetarisch / vegan). Wer mehr braucht,
  erhebt es getrennt, mit eigenem Hinweis und eigener Rechtsgrundlage.
- Der Text der Datenschutzseite (`build/datenschutz.py`) ist ein **Entwurf**.
  Vor dem ersten verkauften Exemplar muss ihn jemand prüfen, der das darf.

Einzelheiten in `docs/10-legal-and-limits.md` und `docs/07-mvp-and-tech.md`.

---

## Eine Einladung ausliefern

### Ein Theme, viele Kunden

Ein verkauftes Theme darf nicht bedeuten, dass jemand einen 2,3-MB-Ordner
kopiert und darin Namen sucht. Bei fünfzig Paaren lägen fünfzig Kopien
derselben Schriften, desselben Films und desselben Programmcodes im Repo, und
beim Ändern einer Kleinigkeit müsste jemand fünfzig Ordner anfassen.

```
themes/<theme>/           das Theme. Einmal da, für alle.
kunden/<kennung>/         nur was diesem Paar gehört   ← nicht eingecheckt
  daten.json              Namen, Termin, Ort, Texte
  bilder/                 eigene Fotos, überlagern die des Themes
  film/                   eigener Hero-Film, optional
auslieferung/<kennung>/   das Ergebnis                 ← nicht eingecheckt
```

**`kunden/` und `auslieferung/` stehen in `.gitignore`, und das ist kein
Versehen.** Darin stehen Namen, Adressen und Fotos echter Menschen. Die haben
in einem Git-Repo nichts verloren, schon gar nicht in einem, aus dem sich
nichts mehr löschen lässt, ohne die Historie umzuschreiben.

### Einmal je Marke

1. Einen kleinen Server in der EU. Node 22 darauf.
2. `engine/rsvp/` hinlegen, Dienst als systemd-Unit einrichten, Caddy davor.
   Anleitung: `engine/rsvp/README.md`.
3. Wildcard auf die Marke zeigen lassen: `*.marke.de` auf den Webspace,
   `rsvp.marke.de` auf den Dienst.

### Je Kunde

```bash
python3 build/kunde.py neu   clara-und-jonas
# daten.json ausfüllen, Fotos nach kunden/clara-und-jonas/bilder/
python3 build/kunde.py bauen clara-und-jonas
# auslieferung/clara-und-jonas/ hochladen
```

`bauen` legt das Theme, die Fotos des Paares und die erzeugten Seiten
zusammen, erneuert die Vorschaukarte mit **den Namen dieses Paares** und sagt,
was noch fehlt. `python3 build/kunde.py liste` zeigt alle Kunden mit ihrem
Stand.

Checkliste:

- [ ] `daten.json` ausgefüllt — `bauen` nennt die Felder, die noch leer sind
- [ ] `adresse` eingetragen, sonst zeigt WhatsApp beim Teilen eine leere Fläche
- [ ] Fotos in `bilder/`, mit `build/art/ambra_fotos.py` zugeschnitten
- [ ] Musik ersetzt, **mit Lizenz** (siehe oben)
- [ ] `rsvp.endpunkt` und die `kennung` eingetragen
- [ ] `kennung=YYYY-MM-DD` in `FESTE` des Dienstes ergänzt, Dienst neu gestartet
- [ ] Ordner hochgeladen, Subdomain `<kennung>.marke.de` daraufgezeigt
- [ ] **Einmal selbst geantwortet** und in `/uebersicht` nachgesehen, dass es ankam
- [ ] Dem Paar die Adresse von `/uebersicht` und sein Token gegeben

`vorschau` steht bei einem neuen Kunden von selbst auf `false` — der Streifen
gehört nicht auf eine echte Einladung. `<meta name="robots" content="noindex,
nofollow">` bleibt drin: die Einladung eines Paares gehört nicht in eine
Suchmaschine.

### Was beim Verkauf mitgeht

| | |
|---|---|
| Die Einladung | unter eigener Subdomain, Laufzeit nach `docs/02-product-and-pricing.md` |
| Die Gästeliste | `/uebersicht` mit eigenem Token, CSV jederzeit |
| Der AVV | Vorlage in `site/recht/avv.html` |
| Die Löschung | greift von selbst, Frist steht in der Datenschutzseite |

---

## Ein neues Theme anlegen

`themes/ambra/` kopieren, umbenennen, Farben in den Tokens oben in
`assets/css/einladung.css` ändern, Zeichnungen neu erzeugen. Aufbau, Bewegung
und Formular bleiben. Das zweite Theme kostet Tage statt Wochen — das ist
derselbe Gedanke wie bei der Engine in `docs/07-mvp-and-tech.md`.
