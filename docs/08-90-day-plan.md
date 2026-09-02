# 08 — 90-Tage-Plan
*Deliverable 25*

**Ziel nach 90 Tagen:** Eine live geschaltete Premium-Marke mit vier verkaufsfertigen
Wedding-Produkten, drei öffentlichen Live-Demos, vollständiger Rechtsgrundlage, laufendem
Pinterest-Kanal und den ersten echten Verkäufen.

**Ausdrücklich nicht das Ziel:** Etsy, Instagram, TikTok, SEO, Hospitality-Vertrieb und
Custom-Services parallel zu starten. Die Begründung steht in
[00 — Executive Summary](00-executive-summary.md#6-was-am-zeitplan-nicht-funktioniert).

---

## Übersicht

| Phase | Wochen | Schwerpunkt | Ergebnis am Ende |
|---|---|---|---|
| **0 — Fundament** | 1–2 | Name, Recht, Werkzeuge | Marke ist entscheidungsfähig |
| **1 — Identität** | 3–4 | Design System, Pinterest-Start | Sichtbares Markenbild |
| **2 — Engine** | 5–8 | Produkt bauen | Es funktioniert wirklich |
| **3 — Storefront** | 9–10 | Shop, Inhalte, Demos | Verkaufbar |
| **4 — Absicherung** | 11–12 | Recht, Tests, Beta | Verkaufsfähig **und** rechtssicher |
| **5 — Launch** | 13 | Live | Erste Verkäufe |

---

## PHASE 0 — Fundament (Woche 1–2)

### Woche 1 — Entscheiden

| # | Aufgabe | Warum kritisch |
|---|---|---|
| 1 | **Markennamen festlegen** (Shortlist in [11](11-open-decisions.md)) | Blockiert Logo, Domain, Shop, Markenanmeldung — **alles** |
| 2 | **Markenrecherche** DPMA + EUIPO, Klassen 09/35/42 | Ein Namenswechsel nach dem Launch kostet ein Vielfaches |
| 3 | Domains sichern (.com + .de) | |
| 4 | Sprachentscheidung DE/EN treffen | Bestimmt Rechtstexte, Keywords, Textmenge |
| 5 | Anwaltliche Erstberatung beauftragen | Vorlaufzeit — jetzt starten, nicht in Woche 11 |
| 6 | Steuerberater: Rechtsform, USt., OSS klären | Siehe [10](10-legal-and-limits.md) |
| 7 | Konten anlegen: Shopify (Testphase), Hosting, Objektspeicher, E-Mail | |

> **Gate 1 — ohne diese Punkte geht Woche 2 nicht los:** Name entschieden, Recherche
> unauffällig, Domain gesichert.

### Woche 2 — Rahmen setzen

| # | Aufgabe |
|---|---|
| 8 | Moodboard je Welt (je 20 Referenzen, **keine** einzelne Marke als Vorlage) |
| 9 | Logo-System entwerfen: Wortmarke, zwei Lockups, Signet |
| 10 | Farbtokens und Typo-Skala festlegen und als Code anlegen |
| 11 | Bildstrategie entscheiden: eigene Produktion vs. lizenzierte Bilder — **inkl. Model Releases** |
| 12 | Repository und Deployment aufsetzen (EU-Region) |
| 13 | Produkt- und Preisliste final bestätigen ([02](02-product-and-pricing.md)) |
| 14 | Alle Texte für Homepage und beide Welten-LPs schreiben (DE + EN) |

---

## PHASE 1 — Identität (Woche 3–4)

| # | Aufgabe |
|---|---|
| 15 | Design System als Code: Tokens, Typo, Spacing, Buttons, Cards, Formulare |
| 16 | Beide Theme-Varianten (warm / kühl) umsetzen und gegeneinander prüfen |
| 17 | Homepage-Layout bauen — inklusive der Zwei-Welten-Sektion (die wichtigste der Seite) |
| 18 | Motion-Bibliothek: eine Kurve, drei Dauern, `prefers-reduced-motion` |
| 19 | **★ Pinterest starten** — Konto, 10 Pinnwände je Cluster, Rich Pins aktivieren |
| 20 | **★ Erste 40 Pins** planen und veröffentlichen (Moodboard-, Ideen- und Zitat-Pins) |
| 21 | Produktfotografie / Mockup-Aufbau vorbereiten |

> **Warum Pinterest schon jetzt, ohne Produkt?** Weil der Kanal 60–120 Tage Vorlauf braucht.
> Wer erst zum Launch beginnt, hat im Launchmonat null Traffic. Anfangs werden Ideen- und
> Inspirations-Pins gepostet, ab Woche 9 Produkt-Pins.

---

## PHASE 2 — Engine (Woche 5–8) · kritischer Pfad

### Woche 5 — Kern
| # | Aufgabe |
|---|---|
| 22 | Datenmodell: Tenant, Experience, Block, Locale, License |
| 23 | Multi-Tenancy + Wildcard-Subdomains + Zertifikate |
| 24 | Magic-Link-Authentifizierung für Kunden |
| 25 | Block-Rendering-Engine + Theme-Umschaltung |

### Woche 6 — Editor & Ausgabe
| # | Aufgabe |
|---|---|
| 26 | Editor: Blöcke hinzufügen, sortieren, bearbeiten, Vorschau |
| 27 | **Statische Veröffentlichung auf CDN** (siehe [07](07-mvp-and-tech.md#der-wichtigste-architektonische-kniff-statische-gästeansicht)) |
| 28 | Blöcke: Cover, Rich Content, Timeline, Orte & Karte, FAQ |
| 29 | Mehrsprachigkeit im Datenmodell (auch wenn erst später verkauft) |

### Woche 7 — Interaktion
| # | Aufgabe |
|---|---|
| 30 | **RSVP**: Formular, Begleitpersonen, Bestätigungsmail, Übersicht, CSV-Export |
| 31 | **Foto-Upload**: vorsignierte URLs, Komprimierung, Galerie, Lösch- und Meldefunktion |
| 32 | QR-Erzeugung serverseitig + druckfertige Aufsteller-Vorlage (PDF) |
| 33 | Datenschutzfunktionen: Löschung, Export, automatische Löschfrist nach Laufzeitende |

### Woche 8 — Anbindung & Härtung
| # | Aufgabe |
|---|---|
| 34 | Shopify-Webhook `orders/paid` → automatische Provisionierung + Zugangs-E-Mail |
| 35 | Laufzeitverwaltung: Ablauf, Erinnerungen, Verlängerung |
| 36 | Backups einrichten **und eine Wiederherstellung tatsächlich durchspielen** |
| 37 | Lasttest der Gästeansicht (500 gleichzeitige Zugriffe — ein realistischer Hochzeitsabend) |
| 38 | Fehlerüberwachung + Benachrichtigung bei Ausfall |

> **Gate 2:** Eine Testbestellung in Shopify erzeugt automatisch eine funktionierende
> Experience, die auf einem echten Telefon in unter 2 Sekunden lädt.

---

## PHASE 3 — Storefront & Inhalte (Woche 9–10)

### Woche 9
| # | Aufgabe |
|---|---|
| 39 | Shopify-Theme: Homepage, Weddings-LP, Hospitality-LP fertigstellen |
| 40 | Produktseiten für alle vier MVP-Produkte + zwei Bundles |
| 41 | **★ Drei Live-Demos aufsetzen** — eine klassische, eine moderne, eine Destination-Wedding |
| 42 | Kartenset gestalten (5 Karten) + Lizenzen jedes Elements dokumentieren |
| 43 | **★ Pinterest: Produkt-Pins starten** (3–5 pro Tag ab jetzt dauerhaft) |

### Woche 10
| # | Aufgabe |
|---|---|
| 44 | Produktvideos: 2 Bildschirmaufnahmen (12 s, stumm, Loop) |
| 45 | About-Seite mit echten Personen und echtem Foto |
| 46 | FAQ aus den tatsächlichen Fragen der Testnutzer |
| 47 | E-Mail-Anmeldung + Welcome-Flow (3 Mails) |
| 48 | Digital Downloads für das Kartenset einrichten |
| 49 | Shopify Markets: DE/EN, hreflang, Währungen |

---

## PHASE 4 — Absicherung (Woche 11–12)

### Woche 11 — Recht
| # | Aufgabe |
|---|---|
| 50 | **Impressum, Datenschutzerklärung, AGB, Widerrufsbelehrung + Musterformular** — anwaltlich geprüft |
| 51 | **AVV-Vorlage** (Art. 28 DSGVO) + Unterauftragsverarbeiter-Liste veröffentlichen |
| 52 | Verzeichnis von Verarbeitungstätigkeiten + TOM-Dokumentation anlegen |
| 53 | Zustimmungsprozess zum vorzeitigen Leistungsbeginn im Warenkorb umsetzen |
| 54 | Cookie-Consent mit Consent Mode v2; **keine Tracker in der Gästeansicht** |
| 55 | Löschkonzept und Aufbewahrungsfristen je Datenart festschreiben |
| 56 | Markenanmeldung einreichen (DPMA oder EUIPO) |

### Woche 12 — Testen
| # | Aufgabe |
|---|---|
| 57 | **Beta mit 5 echten Paaren** — kostenlos, im Austausch gegen ehrliches Feedback |
| 58 | Vollständiger Kaufdurchlauf auf iOS, Android, Desktop, Safari, Chrome |
| 59 | Performance-Budget prüfen (LCP, CLS, INP) und einhalten |
| 60 | Barrierefreiheit: Tastaturbedienung, Fokuszustände, Kontraste, Screenreader-Stichprobe |
| 61 | E-Mail-Zustellbarkeit: SPF, DKIM, DMARC eingerichtet und geprüft |
| 62 | Alle Preise, Steuersätze und Rechnungsangaben gegenprüfen |
| 63 | Fehler aus der Beta beheben — **priorisiert nach dem, was Käufe verhindert** |

> **Gate 3 — Launch nur, wenn alle vier Punkte erfüllt sind:**
> Rechtstexte vollständig · Kaufdurchlauf fehlerfrei auf allen Geräten · Backup-Wiederherstellung
> getestet · mindestens 3 Beta-Paare haben ihre Experience tatsächlich genutzt.

---

## PHASE 5 — Launch (Woche 13)

| # | Aufgabe |
|---|---|
| 64 | Live schalten. Ohne Ankündigungsfeuerwerk, ohne Rabattaktion. |
| 65 | Pinterest auf Produkt-Pins hochfahren (5/Tag) |
| 66 | Beta-Paare um eine **echte** Bewertung bitten |
| 67 | Persönliche Ansprache: Hochzeitsplaner, Fotografen, Locations im eigenen Umfeld |
| 68 | Erste 20 Bestellungen einzeln begleiten — jede Rückfrage ist Produktwissen |
| 69 | Kennzahlen aufsetzen: `demo_opened`, Conversion, AOV, Fehlerquote |
| 70 | Hospitality-Warteliste: die ersten Interessenten persönlich anrufen |

**Kein Launch-Rabatt.** Ein Premium-Start mit 20 % Nachlass sagt dem Markt, dass der Preis
nicht ernst gemeint ist — und die ersten Käufer werden zur Referenz für alle Späteren.

---

## Was in Tag 91–180 folgt

| Monat | Schwerpunkt |
|---|---|
| **4** | Gästebuch + Games ausliefern · Etsy-Shop starten · Instagram/TikTok beginnen |
| **5** | **Guest Guide fertigstellen** · 3 Hospitality-Design-Partner gewinnen (stark vergünstigt, gegen Referenz) |
| **6** | Weekend-Website-Tier · SEO-Landingpages · Klaviyo mit datumsbasierten Flows |
| **7–9** | Hospitality-Vertrieb mit echten Referenzen · erstes Hotel individuell umsetzen |
| **10–12** | Partnerprogramm für Planer und Locations · Custom-Experiences aktiv anbieten |

---

## Realistische Erwartung an Tag 90

| | |
|---|---|
| Umsatz Monat 3 | **0 – 600 €** |
| Verkäufe | 0 – 10 |
| Pinterest | erste stetige Klicks, noch kein Volumen |
| Hospitality | 10–40 Wartelisten-Einträge |
| Wichtigstes Ergebnis | **Das Produkt existiert, funktioniert und ist verkaufbar** |

Wer in Monat 3 auf nennenswerten Umsatz plant, plant falsch — und trifft dann aus Panik
schlechte Entscheidungen (Rabatte, Ads, Sortimentsaufblähung). Die ersten 90 Tage bauen das
Fundament. Verkauft wird ab Monat 4. Der Zahlenkorridor steht in
[09 — Finanzen](09-financials.md).
