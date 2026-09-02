# 02 — Produkt & Preis
*Deliverables 7–10: Hero Products, Produktarchitektur, Preisstrategie, Bundles*

---

## 7. Hero Products (Deliverable 7)

### Bewertungsmethode

Jedes Produkt bewertet nach: **Nachfrage · Zahlungsbereitschaft · Differenzierung ·
Wiederverwendung der Engine ÷ Bauaufwand ÷ Supportlast.**

Skala 1–5. „Engine" = wie viel des Kerns wiederverwendet wird (hoher Wert = billig zu bauen,
sobald der Kern steht).

### WEDDINGS

| Produkt | Nachfrage | Zahlungsbereit. | Differenz. | Engine | Aufwand | Support | **Rolle** |
|---|---|---|---|---|---|---|---|
| **Wedding Website + RSVP** | 5 | 5 | 4 | — Kern — | hoch | mittel | **HERO** |
| **Digital Invitation** | 5 | 3 | 3 | 5 | niedrig | niedrig | **ENTRY / Türöffner** |
| **Photo QR** | 4 | 4 | 5 | 4 | mittel | niedrig | **HERO-UPSELL** |
| Digital Guestbook | 3 | 3 | 4 | 5 | niedrig | niedrig | Upsell (Bundle mit Photo QR) |
| **Weekend Website** | 3 | 5 | 4 | 5 | niedrig | mittel | **SIGNATURE-Tier** — kein eigener Build |
| QR Games | 3 | 2 | 5 | 3 | mittel | niedrig | Bundle-Zugabe + Social-Hook |
| Kartenset (Dateien) | 4 | 2 | 2 | — | niedrig | keine | Etsy/SEO-Volumen |
| ~~Complete Wedding Planner (Software)~~ | 4 | 2 | 1 | 1 | **sehr hoch** | **hoch** | ❌ **streichen** |
| Wedding Planner (Datei/Notion) | 4 | 2 | 2 | — | niedrig | keine | Lead-Magnet mit Preisschild |

**Drei Entscheidungen daraus:**

1. **Wedding Website + RSVP ist der Kern von allem.** Es hat die höchste Nachfrage, die
   höchste Zahlungsbereitschaft, und es *ist* die Engine. Jede Stunde, die hier investiert
   wird, zahlt auf jedes andere Produkt ein. Wenn nur ein Produkt zum Launch fertig ist, dann
   dieses.

2. **Weekend Website ist kein Produkt, sondern eine Preisstufe.** Mehrtägig, mehrere Orte,
   Reise-/Hotelblöcke, zwei Sprachen — das sind Konfigurationsoptionen derselben Engine.
   Als eigenes Produkt gebaut wäre es doppelte Arbeit für dieselbe Sache. Als SIGNATURE-Tier
   verkauft, verdoppelt es den Preis. Das ist der beste Hebel im gesamten Sortiment.

3. **Photo QR ist das beste Marketing-Produkt.** Niedriger Bauaufwand auf der Engine, hohe
   wahrgenommene Wertigkeit, und es ist das einzige Produkt, das sich **von selbst zeigt**:
   Jeder Gast auf jeder Hochzeit sieht den Aufsteller und scannt. Das ist organische
   Reichweite, für die niemand sonst bezahlt. Und es ist der beste TikTok-/Reels-Hook, den
   das Sortiment hat.

### HOSPITALITY

| Produkt | Nachfrage | Zahlungsbereit. | Differenz. | Engine | Aufwand | Zyklus | **Rolle** |
|---|---|---|---|---|---|---|---|
| **Digital Guest Guide** | 5 | 4 | 3 | 5 | niedrig | kurz | **HERO (Wave 2)** |
| Done-for-you Setup | 4 | 5 | 4 | — | Zeit | kurz | **Margen- & Retentionshebel** |
| Hotel Guest Portal | 3 | 5 | 4 | 4 | mittel | **lang** | High-ACV, Wave 3 |
| Multi-Property / White Label | 2 | 5 | 3 | 3 | mittel | lang | Wave 4 |

**Der Guest Guide ist billig zu bauen** (es ist dieselbe Engine mit anderer Blockbibliothek)
und **teuer zu verkaufen** (B2B braucht Referenzen). Deshalb: Produkt früh fertig, Vertrieb
spät starten, erste drei Kunden manuell und günstig gewinnen.

**Done-for-you Setup ist unterschätzt.** Der häufigste Grund, warum B2B-Kunden solche Tools
kündigen: sie füllen die Inhalte nie aus. Wenn wir für 190 € den kompletten Guide befüllen,
ist der Kunde ab Tag 1 im Wert — und kündigt viel seltener. Das ist gleichzeitig Marge und
Retention.

---

## 8. Produktarchitektur (Deliverable 8)

### Die zwei Produkttypen — technisch und rechtlich verschieden

| | **Typ A — Dateien** | **Typ B — Hosted Experiences** |
|---|---|---|
| Beispiele | Kartensets, Planer-Datei | Website, Invitation, Photo QR, Gästebuch, Games, Guides, Portale |
| Lieferung | Download nach Kauf | Provisionierung + Zugangslink |
| Laufende Kosten | keine | Hosting, Speicher, Support |
| Support | fast keiner | real |
| Rechtlich | Digitale Inhalte | **Digitale Dienstleistung** — anderer Widerruf, AVV nötig |
| Marge | ~98 % | ~85–92 % |
| Kanäle | Shop **+ Etsy** | Shop **nur** |

Diese Trennung muss sich durch den gesamten Shop ziehen: eigener Produkttyp, eigener
Checkout-Text, eigene Widerrufsbelehrung, eigene Auslieferung.

### Weddings — Sortiment

```
ENTRY          Digital Invitation ····························· Türöffner
               Kartenset (5 Karten) ··························· Etsy-Volumen
               Wedding Planner (Datei) ························ Lead-Magnet

HERO           Wedding Website + RSVP ························· Umsatzkern

UPSELL         Photo QR ······································· höchster Attach-Rate-Kandidat
               Digital Guestbook ······························ Bundle mit Photo QR
               QR Games ······································· Bundle-Zugabe

SIGNATURE      Wedding Weekend Website ························ dieselbe Engine, doppelter Preis

ADD-ONS        Zweite Sprache · eigene Domain · Laufzeit +12 Mon.
               Priority Setup · Done-for-you Aufbau

CUSTOM         Signature Custom Wedding Experience ············ 4 Slots pro Saison
```

### Hospitality — Sortiment

```
ENTRY          Guest Guide Solo (1 Objekt) ···················· Self-Service-Abo
CORE           Guest Guide Host (bis 5) ······················· Kernprodukt
PRO            Guest Guide Pro (bis 15, eigene Domain) ········ Margenträger
HIGH-ACV       Hotel Guest Portal ····························· Setup + Abo
ADD-ONS        Done-for-you Setup · Fotoproduktion · Mehrsprachigkeit
CUSTOM         Individuelle Hospitality Experience
```

### Die Engine dahinter (Kurzfassung)

Ein Kern, sechs Blockfamilien, zwei Themes. Ausführlich in [07 — MVP & Technik](07-mvp-and-tech.md).

| Block | Weddings | Hospitality |
|---|---|---|
| Hero / Cover | ✅ | ✅ |
| Rich Content (Text/Bild/Galerie) | ✅ | ✅ |
| Programm / Timeline | Ablauf des Tages | Check-in/out, Frühstückszeiten |
| Orte & Karte | Location, Anfahrt, Hotels | Local Guide, Empfehlungen |
| FAQ / Info-Liste | Dresscode, Geschenke | Hausregeln, WLAN, Technik |
| Formular-Input | **RSVP** | Anfrage an Gastgeber |
| Upload | Fotos, Gästebuch | (aus) |
| Interaktion | Spiele | (aus) |

Ein Hotel Guest Portal ist derselbe Code wie eine Wedding Website — nur mit anderer
Blockfreischaltung, anderem Theme und anderem Preis. **Das ist der ganze Trick.**

---

## 9. Preisstrategie (Deliverable 9)

### Grundsätze

1. **Keine 9er-Preise.** 89 €, nicht 89,99 €. Runde Preise wirken souverän, krumme wirken
   nach Rabattlogik.
2. **B2C: Bruttopreise inkl. USt.** ausgezeichnet — Pflicht nach PAngV.
   **B2B: Nettopreise** mit klarem „zzgl. USt.".
3. **Laufzeit ist Teil des Preises.** Ein gehostetes Produkt ohne Laufzeitbegrenzung ist eine
   unbegrenzte Verbindlichkeit. Jedes Typ-B-Produkt hat eine **eingeschlossene Laufzeit**,
   danach optionale Verlängerung. Das ist ehrlich, kalkulierbar und schafft einen
   wiederkehrenden Umsatzschwanz.
4. **Nie den niedrigsten Preis anbieten.** Wir gewinnen über Ausführung, nicht über Preis.

### Warum die Preise im Briefing zu niedrig sind

Das Briefing setzt die Wedding Website bei 49 €. Dagegen spricht:

- Es ist ein **betriebener Dienst über 18 Monate**, kein Download. Hosting, Speicher, Support,
  Verfügbarkeit am Hochzeitstag sind reale laufende Kosten.
- Bei 49 € brutto bleiben nach USt. und Zahlungsgebühren rund **38 €**. Ein einziger
  Support-Fall von 25 Minuten frisst den Deckungsbeitrag.
- 49 € **untergräbt die Positionierung.** Wer eine Premium-Experience für 49 € verkauft,
  sagt dem Kunden, dass es keine ist. Im Kontext eines Hochzeitsbudgets von 20.000 € ist der
  Unterschied zwischen 49 € und 89 € für den Käufer irrelevant — für dich ist er der
  Unterschied zwischen tragfähig und nicht tragfähig.

**Empfehlung: 89 €.** Immer noch deutlich unter individueller Gestaltung, klar über
Template-Niveau, und es erlaubt echten Service.

### WEDDINGS — Preisliste (brutto, inkl. USt.)

**Typ A — Dateien**

| Produkt | Preis | Laufzeit |
|---|---|---|
| Einzelkarte (Save the Date / Menü / Danke) | **14 €** | — |
| Kartenset (5 aufeinander abgestimmte Karten) | **39 €** | — |
| Wedding Planner (Notion/Sheet) | **19 €** | — |

**Typ B — Hosted Experiences**

| Produkt | Preis | Enthaltene Laufzeit |
|---|---|---|
| Digital Invitation (eine Seite, RSVP-light) | **29 €** | 12 Monate |
| **Wedding Website + RSVP** | **89 €** | 18 Monate |
| Photo QR | **39 €** | 12 Mon. aktiv + 12 Mon. Download |
| Digital Guestbook | **39 €** | 12 Mon. aktiv + Export |
| QR Games (3 Spiele) | **29 €** | 12 Monate |
| **Wedding Weekend Website** (SIGNATURE) | **179 €** | 18 Monate |

**Add-ons**

| Add-on | Preis |
|---|---|
| Zweite Sprache | **29 €** |
| Eigene Domain (Anbindung, ohne Domainkosten) | **39 €** |
| Laufzeitverlängerung +12 Monate | **19 €** |
| Priority Setup (48 h) | **49 €** |
| Done-for-you Aufbau (wir bauen es fertig) | **149 €** |

**Custom**

| | |
|---|---|
| Signature Custom Wedding Experience | **ab 490 €**, typisch **890–2.500 €** |
| Verfügbarkeit | **4 Slots pro Saison** — echte Knappheit, nicht inszenierte |

### HOSPITALITY — Preisliste (netto, zzgl. USt.)

| Paket | Monatlich | Jährlich | Enthalten |
|---|---|---|---|
| **Guest Guide Solo** | 19 € | **190 €** *(2 Monate frei)* | 1 Objekt, Themes, QR, unbegrenzte Änderungen |
| **Guest Guide Host** | 39 € | **390 €** | bis 5 Objekte, Mehrsprachigkeit |
| **Guest Guide Pro** | 79 € | **790 €** | bis 15 Objekte, eigene Domain, eigenes Branding, Priority Support |
| **Hotel Guest Portal** | **ab 149 €** | ab 1.490 € | 1 Haus, individuelle Struktur, AVV, EU-Hosting, benannter Kontakt |
| Hotelgruppe / Multi-Property | auf Anfrage | | |

**Einmalige Leistungen**

| Leistung | Preis |
|---|---|
| Done-for-you Setup Solo/Host | **190 €** *(bei Jahresabo im Launch kostenlos)* |
| Done-for-you Setup Pro | **490 €** |
| Hotel Portal Setup | **990 – 2.900 €** je nach Inhaltstiefe |
| Individuelles Hospitality-Projekt | **2.500 – 9.000 €** |

**Warum Jahresabo bevorzugt:** Cash im Voraus, deutlich weniger Kündigungen, keine
fehlgeschlagenen Zahlungen, kein monatlicher Verwaltungsaufwand. Zwei Monate zu verschenken
ist der günstigste Weg zu planbarem Umsatz.

### Preisarchitektur im Überblick

| Stufe | Weddings | Hospitality |
|---|---|---|
| ENTRY | 14 – 39 € | 190 €/Jahr |
| PREMIUM | 39 – 89 € | 390 €/Jahr |
| SIGNATURE | 129 – 279 € | 790 €/Jahr + Setup |
| CUSTOM | 490 – 2.500 € | 1.490 – 9.000 € |

---

## 10. Bundles (Deliverable 10)

Bundles sind der wichtigste Hebel für den durchschnittlichen Bestellwert — **wenn** sie
dreistufig sind. Drei Optionen führen dazu, dass die mittlere überproportional oft gewählt
wird. Zwei Optionen führen dazu, dass die billigere gewählt wird.

| Bundle | Enthalten | Einzelwert | **Bundle** | Ersparnis |
|---|---|---|---|---|
| **ESSENTIALS** | Invitation + Kartenset + Wedding Website | 157 € | **129 €** | 28 € |
| **THE EXPERIENCE** ⭐ | Wedding Website + Photo QR + Guestbook + Games | 196 € | **169 €** | 27 € |
| **THE COMPLETE WEDDING** | Weekend Website + Invitation + Kartenset + Photo QR + Guestbook + Games | 354 € | **279 €** | 75 € |

**⭐ THE EXPERIENCE ist das Zielbundle.** Es wird auf jeder Produktseite als empfohlen
markiert, es ist im Warenkorb-Upsell die Standardoption, und alle Preise sind so gesetzt,
dass es rational die beste Wahl ist.

### Warum diese Zusammenstellungen

- **ESSENTIALS** deckt den Pflichtteil ab (einladen, informieren, Rückmeldung sammeln). Es ist
  der Einstieg für preisbewusste Paare — und lässt Photo QR und Gästebuch als spätere
  Nachkäufe offen.
- **THE EXPERIENCE** ist der Sweet Spot: alles, was am Hochzeitstag selbst passiert. Der
  Kunde kauft hier den *Tag*, nicht die *Einladung*. Höchster wahrgenommener Wert pro Euro.
- **THE COMPLETE WEDDING** existiert vor allem als **Preisanker**. Selbst wenn nur 5 % es
  kaufen, lässt es 169 € vernünftig aussehen. Für Destination Weddings ist es das
  offensichtlich richtige Produkt.

### Bundle-Regeln

1. Ein Bundle darf **nie** teurer sein als die Summe der Einzelteile.
2. Die Ersparnis wird **in Euro** genannt, nicht in Prozent (28 € klingt konkreter als 18 %).
3. **Kein Bundle enthält ein Add-on.** Add-ons bleiben Zusatzumsatz nach dem Kauf.
4. Nach dem Kauf eines Einzelprodukts: **Upgrade-Angebot** auf das Bundle zum
   Differenzbetrag, gültig 7 Tage. Das ist der einfachste AOV-Hebel überhaupt.

### Erwartete Wirkung auf den Warenkorb

| Szenario | Ø Bestellwert |
|---|---|
| Nur Einzelprodukte, kein Upsell | ~42 € |
| Mit Bundles, ohne Upgrade-Flow | ~58 € |
| Mit Bundles + Post-Purchase-Upgrade + Add-ons | **~72 €** |

Diese Zahlen sind Planungsannahmen, keine Prognose — sie sind ab dem ersten Monat live gegen
echte Daten zu prüfen. Der AOV ist die Kennzahl, die im ersten Jahr am meisten über
Profitabilität entscheidet; siehe [09 — Finanzen](09-financials.md).
