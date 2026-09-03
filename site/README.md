# Website

Statische Website für **VELORA** — *Premium hospitality. Intelligently
connected.* Die digitale Infomappe für Orte, an denen Menschen ankommen.
Kein Framework, keine Build-Abhängigkeiten, keine Drittanbieter-Anfragen
zur Laufzeit.

```
site/                     ← das ist die Website. Ordner hochladen, fertig.
  index.html              Startseite: was es ist → für wen → Rechner → Preise
  produkt.html            Bausteine, Funktionen, Grenzen
  preise.html             Tarife und Sonderfälle
  segmente/               Sechs Zielgruppenseiten
  demo/                   Drei Live-Beispiele (eigenes, schlankes Gerüst)
  recht/                  Rechtstexte — Entwürfe, siehe unten
  assets/css|js|fonts|img
  sitemap.xml · robots.txt · 404.html

build/                    Generator (nur für die Entwicklung)
  build.py                setzt pages/ + layout ins fertige HTML
  layout.html             Gerüst mit Header, Navigation, Footer
  layout-bare.html        Gerüst für die Live-Beispiele
  pages/                  Seiteninhalte mit JSON-Front-Matter
```

## Anschauen

```bash
cd site && python3 -m http.server 8000
```

Dann <http://localhost:8000>. **Über HTTP öffnen, nicht per Doppelklick** —
`file://` blockiert das Laden der Schriften.

## Ändern

Inhalte liegen in `build/pages/`, nicht in `site/`. Nach jeder Änderung:

```bash
python3 build/build.py
```

Das Ergebnis in `site/` ist eingecheckt — die Website funktioniert also auch
ohne den Generator. Er existiert nur, damit Header, Navigation und Footer
nicht in 22 Seiten dupliziert werden.

## Markennamen austauschen

Zum Wechseln genügt eine Zeile in `build/build.py`:

```python
BRAND = "VELORA"   # → gewünschter Name
```

Danach neu bauen. Zusätzlich anzupassen: `assets/img/favicon.svg` (der
Buchstabe), die Domain in `sitemap.xml`, `robots.txt` und den
`canonical`-Angaben in beiden Layouts.

---

## Aufbau der Startseite

Die Reihenfolge ist bewusst gewählt: **erst verstehen, dann einordnen.**

1. **Hero** — was es ist, für wen, was es kostet. Die sechs Angebote wechseln
   automatisch durch, jedes sechs Sekunden; Preis und Zielgruppe stehen im
   Hero, nicht drei Klicks später. Die Punkte darunter sind Knöpfe: wer nicht
   warten will, springt direkt zu seinem Bereich. Daneben ein Pause-Knopf.
   Ohne JavaScript und bei reduzierter Bewegung wird daraus ein Raster mit
   allen sechs gleichzeitig — siehe unten.
2. **Problem** — ein Nachrichtenfenster, in dem sich der Verlauf einmal selbst
   schreibt: Tippanzeige, Blase, Uhrzeit, von 21:47 bis 22:26. Der Absatz
   darüber behauptet „sie kommen abends" — hier sieht man es.
3. **So funktioniert es** — drei Schritte.
4. **Segmente** — sechs Karten zur Auswahl. Bewusst *nach* der Erklärung: ein
   Auswahlgitter vor dem Verständnis ist eine Schleuse, keine Hilfe.
5. **Was drin ist** — Sticky-Scroll mit wechselnder Telefonansicht.
6. **Rechner** — mit den Zahlen des Besuchers, inklusive Regler für den Anteil
   der Fragen, der tatsächlich wegfällt. Wir behaupten keine Quote.
7. **Preise** — drei Tarife, umschaltbar zwischen monatlich, jährlich und
   einmalig. Kein „Preis auf Anfrage", auch nicht für die Fälle, die von der
   Anzahl abhängen: die haben eine Rechnung zum Selbstnachrechnen.
8. **Vertrauen** — EU-Hosting, AVV, Export, kein Tracking.
9. **Was wir nicht sind** — die Grenzen, offen benannt.

## Was fertig ist

- **Design System** als Token-Satz. Sechs Segmentakzente über ein einziges
  Attribut (`data-seg`), alle stark entsättigt — sie wirken nur als Linie,
  Label und Kartenrahmen.
- **Selbst gehostete Schriften**: Playfair Display für Überschriften,
  Montserrat für alles andere. Beide SIL OFL, keine Anfrage an ein fremdes CDN.
- **Animationen**: eine Easing-Kurve, drei Dauern, Fade-and-Rise, Bild-Reveals,
  zeilenweiser Text-Reveal, Sticky-Scroll, Parallax bei max. 6 % nur auf
  Desktop. `prefers-reduced-motion` schaltet alles ab.
- **Angebots-Karussell im Hero**: 36 s Rundlauf, 6 s je Angebot. Die Bewegung
  kommt aus CSS und läuft auch ohne JavaScript; JavaScript ergänzt nur die
  Bedienung. Anhalten geht über den beschrifteten Knopf, über Tastaturfokus
  und über den Zeiger (WCAG 2.2.2 — der Zeiger allein reicht auf dem Telefon
  nicht). Ohne JavaScript und bei reduzierter Bewegung steht dort statt der
  Reihe ein Raster mit allen sechs Angeboten: niemand verliert Inhalt, weil
  eine Animation ausbleibt.
- **Echte, scannbare QR-Codes** (Fehlerkorrektur H), erzeugt mit `segno` und
  mit einem Decoder gegengeprüft.
- **Aufwandsrechner**, geprüft gegen Handrechnung und an den Tarifgrenzen.
- **Abrechnung wählbar**: monatlich (aufs Jahr rund 20 % mehr), jährlich
  (günstigster laufender Preis) oder einmalig für drei Jahre Laufzeit. Jede
  Kachel zeigt, was die gewählte Art aufs Jahr gerechnet bedeutet — der
  Vergleich steht dabei, nicht in einer Fußnote. Die Auswahl reist über die
  Adresszeile ins Kontaktformular und steht dort vorausgefüllt.
- **Nachrichtenfenster** im Abschnitt „Das Problem": läuft einmal, 8,4 Sekunden,
  mit „Überspringen"-Knopf sowie Anhalten per Zeiger und Tastaturfokus
  (WCAG 2.2.2). Bewusst nicht in den Farben und Zeichen eines bestimmten
  Messengers — das wäre fremde Marke.
- **Drei Live-Beispiele** mit funktionierender Interaktion: Reiter-Navigation,
  Anmeldung, Schadensmeldung mit Foto — alles rein im Browser.
- **Barrierefreiheit**: Sprunglink, sichtbare Fokuszustände, Tastaturbedienung,
  semantische Überschriften, beschriftete Formularfelder. **274 Textstellen auf
  22 Seiten gemessen, alle über der Schwelle** — nicht geschätzt.
- **Zwei Goldtöne, und das ist Absicht.** `--gold` (#D4AF37) ist die Signatur:
  Flächen, Marke, feine Linien. Als Schrift auf Creme kommt sie auf **1,98:1**
  und wäre unlesbar — deshalb gibt es `--gold-ink` (#7B641A), denselben Ton so
  weit abgedunkelt, dass er 4,5:1 auch auf der getönten Fläche erreicht.
  Knöpfe mit Goldfläche tragen **dunkle** Schrift (8,3:1), nie weiße (2,1:1).
  Jeder Segmentton hat zusätzlich eine Fassung für dunklen Grund (`--seg-deep`).
- **26 eigene Illustrationen** als SVG, erzeugt aus `build/art/make.py`.
  Zusammen 128 KB, lizenzfrei, auf jedem Display scharf.
- **Eli**, der Assistent. Ein schwebender Knopf mit Elis Porträt; das Fenster
  öffnet sich auf Klick, auf dem Telefon als Blatt von unten. Er kennt die
  Seite, auf der er steht, und schlägt passende Themen vor. Der Angebots-Berater
  fragt zweimal und empfiehlt dann einen Tarif **mit Begründung** — und sagt
  ehrlich, wenn das günstigere Angebot reicht. Vollständig tastaturbedienbar,
  Esc schließt.

  **Auf den Gästeseiten ist er kein Menü mehr, sondern ein Werkzeug.** Er
  liest die Fakten des Objekts aus der Seite (`<script id="velora-facts">`,
  gespeist aus dem Front-Matter) und handelt damit:

  | Frage | Was Eli tut |
  |---|---|
  | WLAN | Netzwerk und Passwort, **ein Tipp kopiert es** — oder ein QR-Code, mit dem sich das Telefon selbst verbindet |
  | Anreise, Check-out | Zeiten und Schlüssel, dazu der Sprung in den richtigen Abschnitt |
  | Adresse, Parken | Adresse kopieren oder auf der Karte zeigen |
  | Kontakt | Anrufen oder schreiben, mit einem Tipp |
  | **Alles andere** | **Die Frage wird fertig vorbereitet an den Gastgeber geschickt** |

  Die letzte Zeile ist die wichtigste: Eli ist nie eine Sackgasse. Was nicht
  hinterlegt ist, geht mit Betreff und Objektnamen an den Gastgeber — und der
  sieht damit selbst, welche Angabe in seiner Mappe fehlt.

  Die Fakten stehen **nicht** im Skript. Eine Kopie im Code läuft irgendwann
  auseinander, und dann nennt der Assistent ein Passwort, das nicht mehr gilt.
  Was der Gastgeber nicht hinterlegt hat, taucht gar nicht erst als Vorschlag
  auf — Eli erfindet nichts.

  **Eli ist kein Sprachmodell**, und die Seite sagt das an drei Stellen offen.
  Es gibt kein Backend, an das er fragen könnte. Er führt durch feste Themen
  und gibt wieder, was ohnehin auf der Website steht. Auf freie Fragen sucht er
  das nächstliegende Thema; findet er keins, sagt er das und verweist auf den
  Kontakt. Ein Chat, der freie Antworten vortäuscht, wäre genau die Sorte
  Versprechen, die der Rest dieser Seite vermeidet.
- **Ohne JavaScript** bleiben alle 22 Seiten vollständig lesbar. Der
  Preisumschalter ist dann ausgeblendet und **alle drei Beträge stehen
  untereinander** in der Kachel — es fehlt keine Angabe, nur die Auswahl.
  Im Nachrichtenfenster stehen alle sechs Nachrichten ohne Tippanzeige.
  Eli erscheint gar nicht, statt als toter Knopf dazustehen.

## Was noch fehlt

| Fehlt | Auswirkung | Nächster Schritt |
|---|---|---|
| **Markenrecht** | Der Name VELORA steht, die Recherche nicht | DPMA/EUIPO prüfen, bevor die Seite live geht |
| **Elis Porträt** | Aus dem gelieferten Markenbild freigestellt | Für die Veröffentlichung eine saubere Freistellung mit Alphakanal, idealerweise in mehreren Blickrichtungen |
| **Eli als KI** | Er führt durch feste Themen, er versteht keine freien Fragen | Für echte Antworten braucht es ein Backend und ein Sprachmodell — und dann auch einen Absatz im Datenschutz |
| **Der Lückenbericht** | Der Gastgeber sieht unbeantwortete Fragen nur einzeln per Mail, nicht gesammelt | Braucht ein Backend. Bis dahin ist die vorbereitete Mail der ehrliche Ersatz — sie kommt wirklich an |
| **Fotos** | Alle Flächen tragen eigene Strichzeichnungen — Fotos erst, wenn es echte Kundenobjekte zu zeigen gibt | [`IMAGE-BRIEF.md`](IMAGE-BRIEF.md) |
| **Formular-Empfänger** | Formulare validieren, senden aber nichts | Endpunkt eintragen, Bestätigungsmail |
| **Zahlung** | Preise und Abrechnung stehen auf der Seite, gezahlt wird per Rechnung. Der „Starten"-Knopf führt ins Formular, nicht in einen Checkout — und die Seite sagt das dort auch | Zahlungsanbieter anbinden, dann wird aus der Auswahl ein Kauf |
| **Preishöhe** | Die Jahrespreise standen schon vorher fest. Monatlich (Jahr ÷ 10), einmalig (≈ 2,5 Jahrespreise für drei Jahre) und die Staffeln sind daraus abgeleitet | Vom Betreiber bestätigen lassen, bevor die Seite live geht |
| **Rechtstexte** | `recht/` ist ein Gerüst. Per `robots.txt` von der Indexierung ausgenommen | Fachanwalt für IT-Recht |
| **Das Produkt selbst** | Die Demos sind statisch nachgebaut, es gibt kein Backend | Experience Engine, siehe `docs/07` |

Kein Formular und kein Knopf täuscht Erfolg vor. Wo etwas noch nicht
funktioniert, steht das dort, wo geklickt wird.
