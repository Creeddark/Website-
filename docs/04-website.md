# 04 — Website
*Deliverables 12–17: Sitemap, Homepage-Wireframe, Weddings-LP, Hospitality-LP, Produktseiten, B2B-LP*

---

## 12. Shopify Sitemap (Deliverable 12)

### Navigation (Desktop)

```
[MARKE]        Weddings    Hospitality    Shop    Custom    About         [Suche] [Konto] [Warenkorb]
```

Sechs Punkte. Keine Mega-Dropdowns auf oberster Ebene — die Welten-Landingpages **sind** die
Navigation. Ein Dropdown, das alle Produkte zeigt, macht die Trennung der beiden Welten
kaputt und nimmt den Landingpages ihre Aufgabe.

Beim Hover über *Weddings* / *Hospitality* öffnet ein **weltinternes** Panel:

```
WEDDINGS                                  HOSPITALITY
─────────────────────────────────────     ─────────────────────────────────────
Wedding Websites                          Vacation Rentals
Digital Invitations                        Digital Guest Guides
Guest Experiences                          Hotels
QR Experiences                             Guest Portals
Bundles                                    For Property Managers
Custom Wedding Experience                  Book a Demo
→ Explore Weddings                        → Explore Hospitality
```

### Seitenstruktur

```
/                                    Homepage — verkauft die Marke, teilt in zwei Welten

/weddings                            WELT 1 — Landingpage
  /weddings/wedding-websites         Kategorie
  /weddings/invitations              Kategorie
  /weddings/guest-experiences        Kategorie (Gästebuch, Photo QR)
  /weddings/qr-experiences           Kategorie (Photo QR, Games)
  /weddings/bundles                  Kategorie
  /weddings/custom                   Custom-Anfrage Weddings
  /weddings/demo/[slug]              Live-Demos (indexierbar, eigene SEO-Assets)

/hospitality                         WELT 2 — Landingpage
  /hospitality/vacation-rentals      Segment-LP (H1/H2)
  /hospitality/hotels                Segment-LP (H3)
  /hospitality/guest-guides          Produkt
  /hospitality/guest-portals         Produkt
  /hospitality/pricing               Preise B2B
  /hospitality/demo/[slug]           Live-Demos
  /hospitality/contact               B2B-Anfrage / Demo-Termin

/products/[handle]                   Produktseiten (Shopify)
/collections/[handle]                Kategorien (Shopify)
/pages/custom                        Custom Experiences (beide Welten)
/pages/about                         Über uns — echte Personen, echte Geschichte
/pages/faq                           FAQ (getrennt nach Welt)
/pages/contact                       Kontakt

/blog                                SEO-Content (Guides, Ratgeber)
/blog/[handle]

RECHT (im Footer, nicht in der Hauptnavigation)
/policies/legal-notice               Impressum
/policies/privacy-policy             Datenschutzerklärung
/policies/terms-of-service           AGB
/policies/refund-policy              Widerrufsbelehrung + Muster-Widerrufsformular
/pages/dpa                           Auftragsverarbeitungsvertrag (AVV)
/pages/subprocessors                 Liste der Unterauftragsverarbeiter
/pages/accessibility                 Barrierefreiheitserklärung
```

### Grundsatzentscheidung: ein Shop, nicht zwei

| | Ein Shop, zwei Themes ✅ | Zwei Shops ❌ |
|---|---|---|
| Kosten | eine Subscription | zwei |
| SEO | eine Domain-Autorität | halbiert, zwei Mal aufbauen |
| Pflege | ein Theme, zwei Token-Sets | doppelt alles |
| Marke | „zwei Welten, ein Haus" | zwei Fremde |
| Checkout | einer | zwei |

Die Welten-Trennung entsteht über **Template-Zuordnung + CSS-Variablen-Set**, nicht über
getrennte Systeme. In Shopify: eigene Section-Group und Template-Suffix pro Welt, das
`data-world="weddings|hospitality"` am `<body>` setzt und darüber die Token umschaltet.

---

## 13. Homepage-Wireframe (Deliverable 13)

**Aufgabe der Homepage:** Sie verkauft **kein Produkt**. Sie verkauft die Marke und sortiert
den Besucher in die richtige Welt. Erfolgsmetrik ist nicht „Add to Cart", sondern **Anteil
der Besucher, die eine Welt betreten** (Ziel: > 55 %).

```
┌────────────────────────────────────────────────────────────────────────┐
│ 01  HERO                                                    100 vh     │
│                                                                        │
│     Vollflächiges Video oder Standbild, sehr ruhig, langsamer Zoom     │
│     Dunkler Verlauf unten für Lesbarkeit                               │
│                                                                        │
│                  DIGITAL EXPERIENCES,                                  │
│                  BEAUTIFULLY MADE.                     display-xl      │
│                                                                        │
│                  Thoughtfully designed digital experiences             │
│                  for weddings, guests and unforgettable moments.       │
│                                                                        │
│                  [ EXPLORE WEDDINGS ]  [ EXPLORE HOSPITALITY ]         │
│                       primary              secondary                   │
│                                                                        │
│     Text-Reveal zeilenweise, 900 ms. Kein Autoplay-Ton. Kein Scroll-   │
│     Indikator-Gimmick.                                                 │
├────────────────────────────────────────────────────────────────────────┤
│ 02  DIE KLAMMER                                            ~40 vh      │
│                                                                        │
│                  TWO WORLDS. ONE SIGNATURE.            label           │
│                                                                        │
│         For everyone who welcomes someone — couples, hosts and         │
│         hoteliers — we design the digital side of hospitality.         │
│                                                display-m, 2 Zeilen     │
├────────────────────────────────────────────────────────────────────────┤
│ 03  DIE ZWEI WELTEN            ← die wichtigste Sektion der Website    │
│                                                                        │
│  ┌───────────────────────────────┬──────────────────────────────────┐  │
│  │                               │                                  │  │
│  │   [warmes Wedding-Visual]     │   [kühles Hospitality-Visual]    │  │
│  │   Ivory/Sand-Overlay          │   Off-white/Stone-Overlay        │  │
│  │                               │                                  │  │
│  │   WEDDINGS            label   │   HOSPITALITY           label    │  │
│  │                               │                                  │  │
│  │   Make every moment           │   Make every stay                │  │
│  │   unforgettable.  display-l   │   feel exceptional.  display-l   │  │
│  │                               │                                  │  │
│  │   Websites, invitations and   │   Guest guides and portals for   │  │
│  │   guest experiences for your  │   rentals and hotels that answer │  │
│  │   wedding day.                │   before guests ask.             │  │
│  │                               │                                  │  │
│  │   EXPLORE WEDDINGS   →        │   EXPLORE HOSPITALITY   →        │  │
│  └───────────────────────────────┴──────────────────────────────────┘  │
│                                                                        │
│  Desktop: 50/50, volle Bildschirmhöhe, keine Lücke dazwischen.         │
│  Hover: die eigene Hälfte wächst auf 54 %, die andere entsättigt auf   │
│  85 % — 700 ms. Der Nutzer *spürt* die Entscheidung.                   │
│  Mobil: gestapelt, je 70 vh, kein Hover-Effekt.                        │
├────────────────────────────────────────────────────────────────────────┤
│ 04  WARUM WIR                                                          │
│                                                                        │
│   Drei Spalten, nur Typo, keine Icons:                                 │
│                                                                        │
│   DESIGNED, NOT           BUILT TO BE            HOSTED AND            │
│   TEMPLATED               USED                   MAINTAINED            │
│   Jede Experience wird    Ihre Gäste öffnen es   Wir betreiben es.     │
│   gestaltet, nicht aus    auf dem Handy, ohne    EU-Hosting, Backups,  │
│   Bausteinen              App, ohne Konto,       Support — bis zum     │
│   zusammengesetzt.        in unter 2 Sekunden.   Tag danach.           │
├────────────────────────────────────────────────────────────────────────┤
│ 05  LIVE-DEMO                              ← der eigentliche Beweis    │
│                                                                        │
│   SEE IT, DON'T IMAGINE IT.                            display-m       │
│                                                                        │
│   Großes Gerätemockup, echtes Scrollvideo (stumm, Loop, 12 s)          │
│   [ OPEN A LIVE DEMO → ]   öffnet echte Demo in neuem Tab, kein Formular│
├────────────────────────────────────────────────────────────────────────┤
│ 06  BEWEIS                                                             │
│                                                                        │
│   Vor dem ersten echten Kunden: NUR harte Fakten                       │
│   „EU-Hosting · Kein Konto für Gäste · DSGVO-konform · Ø Ladezeit 1,2 s"│
│                                                                        │
│   Ab dem ersten echten Kunden: 3 echte Zitate mit Namen + Datum.        │
│   ⚠ Keine erfundenen Reviews. Keine Platzhalter-Testimonials.          │
│   Ein leerer Bereich ist besser als ein erfundener.                    │
├────────────────────────────────────────────────────────────────────────┤
│ 07  E-MAIL                                                             │
│   Ein Feld, ein Satz, ein Button. Kein Popup, kein Rabatt-Rad.         │
│   „Neue Kollektionen und Ideen. Etwa einmal im Monat."                 │
│   Double-Opt-in. Checkbox unangehakt. Link zur Datenschutzerklärung.   │
├────────────────────────────────────────────────────────────────────────┤
│ 08  FOOTER                                                             │
│   Weddings | Hospitality | Shop | Custom | About | FAQ | Kontakt       │
│   Impressum · Datenschutz · AGB · Widerruf · AVV · Barrierefreiheit    │
│   Sprache: DE / EN     ·     Zahlungsarten     ·     © [MARKE]         │
└────────────────────────────────────────────────────────────────────────┘
```

**Was bewusst NICHT auf der Homepage steht:** Produktraster, Preise, Rabattbanner,
Instagram-Feed, Countdown, Chat-Bubble, Cookie-Wall über dem Hero. Jedes dieser Elemente
kostet Markenwahrnehmung und bringt hier keine Conversion — die Entscheidung an dieser Stelle
ist „welche Welt", nicht „welches Produkt".

---

## 14. Weddings-Landingpage (Deliverable 14)

Ab hier gilt: der Besucher hat die Welt betreten. Theme wechselt auf **warm**. Ab jetzt
darf verkauft werden.

```
01  HERO (70 vh, warm)
    WEDDINGS                                                   label
    Your wedding. Your story. Your experience.            display-xl
    Everything your guests need — invitation, details, RSVP and the
    memories afterwards. In one place, beautifully made.
    [ SEE A LIVE DEMO ]  [ BROWSE THE COLLECTION ]

02  BEST SELLERS                                    3 Produkte, mehr nicht
    Wedding Website + RSVP · The Experience Bundle ⭐ · Photo QR
    Karte: Bild 4:5 → label → Titel → Nutzen in einem Satz → Preis

03  WEDDING WEBSITES                    ← Hero-Produkt, größte Sektion
    Sticky Split: links Text scrollt, rechts Telefon-Mockup wechselt Screen
      Your details, without the group chat.
      · Alle Infos an einem Ort — Ablauf, Anfahrt, Dresscode, Hotels
      · RSVP mit Rückmeldung direkt an euch
      · Auf dem Handy in unter 2 Sekunden geladen
      · Zwei Sprachen für internationale Gäste
      · 18 Monate enthalten — vom Save the Date bis zum Dankeschön
    [ SEE THE LIVE DEMO → ]      ab 89 €

04  INVITATIONS
    Nebeneinander: Papier-Einladung vs. digitale Einladung, die sich öffnet
      An invitation that opens into everything else.        ab 29 €

05  GUEST EXPERIENCES
    Photo QR · Digital Guestbook — mit echtem Aufsteller-Foto auf einem Tisch
      The part your guests actually take part in.

06  QR EXPERIENCES
    Kurzvideo: Handy scannt QR → Spiel öffnet sich. Der stärkste Social-Clip.
      One code. No app. No account.

07  WEDDING PLANNING
    Der Planer als Dateiprodukt — ehrlich als Vorlage bezeichnet, nicht als Software
      Start with a clear head.                                    19 €

08  BUNDLES                                        ← höchster AOV-Hebel
    Drei Spalten, Mitte hervorgehoben und leicht größer:
    ESSENTIALS 129 €  ·  THE EXPERIENCE 169 € ⭐  ·  COMPLETE 279 €
    Vergleichstabelle darunter, Ersparnis in Euro

09  HOW IT WORKS
    01 Auswählen  →  02 Inhalte einfügen  →  03 Teilen  →  04 Erinnerungen behalten
    „Die meisten Paare sind in unter 30 Minuten fertig."
    (Diese Zahl erst veröffentlichen, wenn sie durch echte Daten gedeckt ist.)

10  FAQ  — 8 Fragen, die wirklich gestellt werden, nicht 20 Marketingfragen

11  CUSTOM WEDDING EXPERIENCE
    Dunkle Sektion (`deep`), Kontrastbruch
      Your vision. Our experience.        ab 490 € · 4 Slots pro Saison

12  CROSS-WORLD (dezent, eine Zeile, kein Bild)
    Planning a destination weekend? See how hosts welcome guests →
```

---

## 15. Hospitality-Landingpage (Deliverable 15)

Theme wechselt auf **kühl**. Ton wechselt von emotional zu nutzenorientiert. Der Kunde hier
will in 10 Sekunden wissen, was es kostet und was es ihm spart.

```
01  HERO (60 vh, kühl, ruhiger als Weddings)
    HOSPITALITY                                                label
    Make every stay feel exceptional.                    display-xl
    A digital guest guide your guests actually use — everything they
    ask, answered before they ask.
    [ SEE A LIVE GUIDE ]  [ SEE PRICING ]

02  DAS PROBLEM        ← hier zuerst der Nutzen, nicht die Schönheit
    Drei Spalten, nüchtern:
      „Wie ist das WLAN?"  ·  „Wann ist Check-out?"  ·  „Wo kann man essen?"
      Dieselben Fragen. Jede Woche. Von jedem Gast.

03  DIE LÖSUNG
    Ein QR-Code im Objekt → ein Guide, immer aktuell, ohne App, ohne Konto.
    Großes Mockup: QR-Aufsteller auf einem Küchentresen + Handy daneben

04  VACATION RENTALS                                 → /hospitality/vacation-rentals
    Für Gastgeber mit 1–15 Einheiten. Selbst pflegbar, in 30 Minuten startklar.
    [ SEE A LIVE GUIDE → ]                                    ab 190 €/Jahr

05  DIGITAL GUEST GUIDES — was drin ist
    Zweispaltige Liste, ohne Icons:
    Welcome · Check-in · Check-out · WLAN · Hausregeln · Parken · Heizung &
    Technik · Müll · Local Guide · Restaurants · Cafés · Aktivitäten ·
    Sehenswürdigkeiten · Notfall · Kontakt · FAQ

06  HOTELS                                                  → /hospitality/hotels
    Für Boutique-Hotels und kleine Häuser. Individuelle Struktur, Ihr Branding,
    eigene Domain, AVV und EU-Hosting.
    [ TALK TO US → ]                          Setup ab 990 € · ab 149 €/Monat

07  GUEST PORTALS — Umfang
    Welcome · Zimmerinfos · Frühstück · Restaurant · Bar · Spa & Wellness ·
    Aktivitäten · Local Guide · Hotelinfos · Kontakt · FAQ · Check-out

08  WAS WIR NICHT SIND                    ← Vertrauensanker, kein Nachteil
    Wir sind kein PMS, keine Buchungsmaschine und kein Schlüsselsystem.
    Wir sind die digitale Gästeinformation — und die machen wir sehr gut.
    (Diese Sektion gewinnt Deals. Hoteliers haben genug Anbieter erlebt,
     die alles versprechen.)

09  PREISE                                            → /hospitality/pricing
    Drei Karten, Jahrespreis groß, Monatspreis klein darunter.
    Solo 190 €/J · Host 390 €/J ⭐ · Pro 790 €/J · Hotel → auf Anfrage
    Alle Preise netto zzgl. USt.

10  ZUVERLÄSSIGKEIT & RECHT              ← B2B-Kaufvoraussetzung, nicht Kür
    EU-Hosting · AVV nach Art. 28 DSGVO · tägliche Backups ·
    Datenexport jederzeit · keine Weitergabe von Gästedaten

11  CUSTOM HOSPITALITY EXPERIENCE
      Your house. Your voice. Your guest journey.                ab 2.500 €

12  B2B-ANFRAGE                                       → /hospitality/contact
    Formular + Alternative: 20-minütiger Termin

13  CROSS-WORLD (eine Zeile)
    Hosting weddings at your property? See our wedding experiences →
```

---

## 16. Produktseiten (Deliverable 16)

### Aufbau für ein Hosted-Produkt (Typ B)

```
┌─────────────────────────────┬──────────────────────────────────────┐
│                             │  WEDDINGS                     label  │
│  GALERIE (sticky)           │  Wedding Website + RSVP    display-m │
│                             │                                      │
│  1  Gästesicht auf dem Handy│  89 €  inkl. MwSt.                   │
│  2  Scrollvideo (12 s, Loop)│  18 Monate Laufzeit enthalten        │
│  3  RSVP-Ansicht            │                                      │
│  4  Editor-Ansicht          │  Alles, was eure Gäste wissen        │
│  5  Zweisprachig            │  müssen — an einem Ort, auf jedem    │
│                             │  Handy, ohne App.                    │
│                             │                                      │
│                             │  ▸ Design wählen:  ○ ○ ○ ○           │
│                             │  ▸ Sprachen:  1 · 2 (+29 €)          │
│                             │                                      │
│                             │  [ SEE THE LIVE DEMO → ]  ← zuerst!  │
│                             │  [ ADD TO CART ]                     │
│                             │                                      │
│                             │  ✓ Sofort nach dem Kauf einsatzbereit│
│                             │  ✓ Unbegrenzte Änderungen            │
│                             │  ✓ EU-Hosting, tägliche Backups      │
│                             │  ✓ Support bis zum Tag danach        │
│                             │                                      │
│                             │  ⓘ Digitale Dienstleistung — der     │
│                             │    Widerruf erlischt mit Freischaltung│
│                             │    Details ▾  (Pflicht, siehe Recht) │
└─────────────────────────────┴──────────────────────────────────────┘

WAS EURE GÄSTE SEHEN     ← der wichtigste Abschnitt der Seite
  Ganzbreiter Screenshot der Gästesicht. Der Käufer kauft nicht das
  Admin-Tool — er kauft den Eindruck, den seine Gäste bekommen.

FUNKTIONEN               Zweispaltig, konkret, keine Adjektive
  Ablaufplan · Anfahrt & Karte · Hotelempfehlungen · Dresscode · FAQ ·
  RSVP mit Begleitpersonen · Notizfeld · Export als Liste ·
  Zwei Sprachen · Eigene Domain möglich · QR-Code inklusive

SO FUNKTIONIERT ES       01 Kaufen → 02 Zugang per E-Mail → 03 Inhalte
                         einfügen → 04 Link/QR teilen

HÄUFIG DAZU GEKAUFT      Photo QR 39 € · Guestbook 39 € · Games 29 €
                         → oder alles zusammen: THE EXPERIENCE 169 € (spart 27 €)

FAQ                      6 Fragen, produktspezifisch

BEWERTUNGEN              Nur echte. Solange keine da sind: Bereich weglassen.
```

**Die vier Regeln jeder Produktseite**

1. **Live-Demo steht über „In den Warenkorb".** Bei einem 89-€-Produkt, das man nicht anfassen
   kann, ist Ausprobieren der Conversion-Treiber Nummer eins. Der Klick auf die Demo ist
   wertvoller als ein früher Warenkorb-Klick.
2. **Immer die Gästesicht zeigen**, nicht nur die Verwaltungsoberfläche.
3. **Laufzeit und Grenzen stehen sichtbar**, nicht im Kleingedruckten. Ehrlichkeit hier
   verhindert Rückbuchungen und schlechte Bewertungen später.
4. **Bundle-Hinweis mit Ersparnis in Euro** direkt unter dem Cross-Sell.

### Abweichung für Dateiprodukte (Typ A)
Kein Demo-Button, dafür Vorschau-Galerie und klare Angaben: enthaltene Formate,
Bearbeitungsweg, was **nicht** enthalten ist (kein Druck, keine Schriftlizenz zur
Weitergabe), plus der abweichende Widerrufshinweis für digitale Inhalte.

---

## 17. B2B-Landingpage (Deliverable 17)
`/hospitality/vacation-rentals` und `/hospitality/hotels` — gleiche Struktur, andere Zahlen.

```
01  HERO
    FOR HOSTS                                                  label
    Stop answering the same five questions.              display-xl
    Ein Guide für Ihr Objekt. Immer aktuell. Ohne App, ohne Konto für Gäste.
    [ SEE A LIVE GUIDE ]  [ PRICING ]

02  DER WIRTSCHAFTLICHE NUTZEN     ← keine Ästhetik, sondern Argumente
    ┌──────────────┬──────────────┬──────────────┬──────────────┐
    │ Weniger      │ Bessere      │ Professio-   │ In Minuten   │
    │ Rückfragen   │ Bewertungen  │ neller       │ aktualisiert │
    │              │              │ Auftritt     │              │
    │ Alle Antwor- │ Gäste finden │ Ihr Objekt   │ Neue Öffnungs│
    │ ten stehen   │ sich zurecht │ wirkt geführt│ zeiten? Zwei │
    │ vor Ort      │ und beschwe- │ statt        │ Minuten,     │
    │ bereit       │ ren sich     │ improvisiert │ sofort für   │
    │              │ seltener     │              │ alle Gäste   │
    └──────────────┴──────────────┴──────────────┴──────────────┘

    ⚠ Keine erfundenen Prozentzahlen. Sobald echte Kundendaten vorliegen,
      werden sie mit Quelle und Zeitraum genannt — vorher nicht.

03  VORHER / NACHHER
    Links: WhatsApp-Verlauf mit denselben fünf Fragen
    Rechts: der Guide auf dem Handy
    Ein Bild, das ohne Text funktioniert.

04  SO SIEHT ES FÜR IHRE GÄSTE AUS
    [ LIVE-GUIDE ÖFFNEN → ]   ohne Formular, ohne Termin

05  UMFANG        Vollständige Blockliste, ehrlich und komplett

06  SETUP         01 Objektdaten senden → 02 Wir bauen (optional, 190 €)
                  → 03 QR erhalten → 04 Aufstellen. Fertig.
                  „Die meisten Gastgeber sind an einem Nachmittag fertig."

07  PREISE        Solo 190 €/J · Host 390 €/J ⭐ · Pro 790 €/J
                  Alle Preise netto zzgl. USt. · jährlich kündbar
                  Bei Jahresabo: Setup im Launch-Zeitraum kostenlos

08  RECHT & BETRIEB       ← ohne diesen Abschnitt kauft kein Hotel
    EU-Hosting · AVV nach Art. 28 DSGVO auf Anfrage · TOM-Übersicht ·
    tägliche Backups · Datenexport jederzeit · keine Werbung, keine
    Weitergabe von Gästedaten · keine Tracker in der Gästeansicht

09  WAS WIR NICHT SIND    Kein PMS. Keine Buchung. Kein Zahlungssystem.
                          Keine Schlüssel. Kein Live-Concierge.

10  FAQ                   Die echten Einwände: „Muss ich das selbst pflegen?",
                          „Was, wenn ich kündige?", „Kann ich meine Daten mitnehmen?"

11  ANFRAGE
    Formular: Name · Unternehmen · Anzahl Objekte · Website · Nachricht
    Oder: [ 20-MINUTEN-TERMIN BUCHEN ]
    Antwortzusage: werktags innerhalb von 24 Stunden — nur versprechen, was
    eingehalten wird.
```
