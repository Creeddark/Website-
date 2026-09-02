# 07 — MVP & Technische Architektur
*Deliverable 24 (MVP) und Briefing §31 (Shopify-Architektur)*

---

## Die Grundentscheidung

**Shopify ist Schaufenster und Kasse. Das Produkt läuft daneben.**

Alles, was der Kunde nach dem Kauf *benutzt*, ist eine eigene Anwendung — die **Experience
Engine**. Der Versuch, Editor, Gästeansicht, RSVP und Fotouploads innerhalb von Shopify zu
bauen, scheitert an Shopifys Zweck: Shopify ist ein Verkaufssystem, kein Anwendungs-Framework.

```
   ┌─────────────────────────────┐        ┌──────────────────────────────┐
   │  SHOPIFY                    │        │  EXPERIENCE ENGINE           │
   │                             │        │  (eigene App, EU-Hosting)    │
   │  · Storefront, 2 Themes     │ ─────► │                              │
   │  · Warenkorb & Checkout     │webhook │  · Editor (Kunde)            │
   │  · Zahlungen                │        │  · Gästeansicht (öffentlich) │
   │  · Kundenkonten             │        │  · RSVP · Uploads · Spiele   │
   │  · Bestellungen             │        │  · QR-Erzeugung              │
   │  · Dateiauslieferung (Typ A)│ ◄───── │  · Abo-Status (B2B)          │
   │  · Rechtstexte              │ status │                              │
   └─────────────────────────────┘        └──────────────────────────────┘
```

---

## Die Experience Engine

### Ein Kern, viele Produkte

Alle Hosted-Produkte sind **dieselbe Anwendung** mit unterschiedlicher Konfiguration:

```
EXPERIENCE
├─ tenant           wem gehört sie
├─ product_type     wedding_site | invitation | weekend | guest_guide | hotel_portal
├─ theme            weddings | hospitality  (+ Design-Variante)
├─ locale[]         1–n Sprachen
├─ license          gültig bis · Status · Verlängerung
└─ blocks[]         die freigeschalteten Inhaltsblöcke
```

### Blockbibliothek

| Block | Wedding Site | Invitation | Weekend | Guest Guide | Hotel Portal |
|---|:--:|:--:|:--:|:--:|:--:|
| Cover / Hero | ✅ | ✅ | ✅ | ✅ | ✅ |
| Rich Content | ✅ | ✅ | ✅ | ✅ | ✅ |
| Timeline / Ablauf | ✅ | — | ✅ | ✅ | ✅ |
| Orte & Karte | ✅ | — | ✅ | ✅ | ✅ |
| Info-Liste / FAQ | ✅ | — | ✅ | ✅ | ✅ |
| Empfehlungen | — | — | ✅ | ✅ | ✅ |
| **RSVP** | ✅ | ✅ (light) | ✅ | — | — |
| **Foto-Upload** | ✅ | — | ✅ | — | — |
| **Gästebuch** | ✅ | — | ✅ | — | — |
| **Spiele** | ✅ | — | ✅ | — | — |
| Kontaktformular | — | — | — | ✅ | ✅ |
| Mehrsprachigkeit | Add-on | Add-on | ✅ | ✅ | ✅ |

Ein Hotel Guest Portal ist derselbe Code wie eine Wedding Website. Nur andere Blöcke, anderes
Theme, anderer Preis. **Das zweite Produkt kostet Tage statt Monate.**

### Technologie-Empfehlung

| Ebene | Empfehlung | Begründung |
|---|---|---|
| Framework | **Next.js (App Router), TypeScript** | Serverseitiges Rendering für Ladezeit + SEO, ein Stack für Editor und Gästeansicht |
| Datenbank | **PostgreSQL, EU-Region** | Relationale Struktur passt, ausgereift, überall betreibbar |
| Objektspeicher | **S3-kompatibel, EU** | Fotos, Uploads. Direkt-Upload per vorsignierter URL |
| Bilder | On-the-fly-Resize, AVIF/WebP | Gästeuploads sind riesig, müssen komprimiert werden |
| Auth (Kunde) | **Magic Link, kein Passwort** | Weniger Support, weniger Sicherheitsrisiko, weniger gespeicherte Daten |
| Auth (Gast) | **gar keine** | Gäste dürfen nie ein Konto brauchen — Conversion-Killer und Datenschutzlast |
| Hosting | **EU-Region, ausschließlich** | Verkaufsargument im B2B, vermeidet Drittlandtransfer-Diskussion |
| E-Mail (System) | Transaktionsdienst mit EU-Verarbeitung | RSVP-Benachrichtigungen, Magic Links |
| QR | Serverseitig erzeugt, Level H | Nie Drittanbieter-QR — die Fremd-URL kann jederzeit verschwinden |

### Der wichtigste architektonische Kniff: statische Gästeansicht

Die Gästeansicht muss **am Hochzeitstag funktionieren**. Ein Datenbankausfall an einem
Samstag im Juli ist kein Bug, sondern ein zerstörter Tag, eine 1-Stern-Bewertung und ein
Rückerstattungsfall.

**Lösung:** Beim Speichern (bzw. „Veröffentlichen") erzeugt die Engine einen **unveränderlichen
statischen Schnappschuss** der Gästeansicht und legt ihn auf ein CDN.

- Gästeansicht wird vom CDN ausgeliefert → keine Datenbank im Leseweg, Ladezeit unter einer
  Sekunde, praktisch unbegrenzt belastbar
- Nur **Schreibvorgänge** (RSVP, Foto-Upload, Gästebucheintrag, Spielstand) berühren
  Backend-Dienste — und deren Ausfall ist sichtbar begrenzt und nachholbar
- Foto-Uploads laufen per vorsignierter URL **direkt** in den Objektspeicher, nie über den
  Anwendungsserver

Das kostet in der Umsetzung wenig zusätzlichen Aufwand und beseitigt die größte
Betriebsgefahr des Geschäftsmodells. **Diese Entscheidung von Anfang an mitbauen** — sie
nachträglich einzuziehen ist teuer.

### Adressierung
Wildcard-Subdomains: `annaundlukas.[marke].com`. Für Pro/Hotel: eigene Domain per CNAME plus
automatisches Zertifikat. Jede Experience zusätzlich unter einer kurzen QR-URL erreichbar.

---

## Shopify-Architektur (Briefing §31)

### Einordnung nach Lösungsweg

| Anforderung | Lösung | Warum |
|---|---|---|
| Storefront, zwei Welten | **Shopify nativ** — Custom Theme auf Basis von Dawn | Dawn ist schnell, kostenlos, OS-2-Sections. Ein gekauftes Premium-Theme bringt Ballast, den wir ohnehin ersetzen |
| Welten-Trennung | **Shopify nativ** — Template-Suffix + `data-world` + CSS-Variablen | Kein zweiter Shop, keine App |
| Dateiauslieferung (Typ A) | **Shopify App: Digital Downloads** (Erstanbieter, kostenlos) | Genügt vollständig |
| Hosted Experiences (Typ B) | **Custom** — `orders/paid`-Webhook → Provisionierung | Kein Standardweg vorhanden |
| Zwei Sprachen / Märkte | **Shopify nativ** — Markets + Translate & Adapt | hreflang, Währung, Rechtstexte je Markt |
| Bewertungen | **App** — Anbieter mit kostenlosem Einstieg | Erst relevant ab echten Bewertungen |
| E-Mail | **Shopify Email** → später **Klaviyo** | Nicht zu früh Fixkosten aufbauen |
| B2B-Abos | **Zunächst extern**: Angebot + Rechnung/Lastschrift, später Abo-App | Bei 3–20 B2B-Kunden ist manuelle Rechnungsstellung schneller und billiger als jedes Abo-System |
| B2B-Anfragen | **Shopify nativ** — Formular + E-Mail | Kein CRM bei null Umsatz |
| Consent-Banner | **App** mit Consent Mode v2 | Rechtlich erforderlich |
| Analytics | Shopify Analytics + GA4 | Reicht lange |

### Praktische Einschränkung: Zustimmung im Checkout

Für digitale Dienstleistungen und Inhalte braucht es eine **ausdrückliche Zustimmung des
Kunden zum vorzeitigen Beginn der Leistung** (und, bei digitalen Inhalten, die Kenntnisnahme
des Erlöschens des Widerrufsrechts). Der Shopify-Checkout ist auf Standardtarifen nur
begrenzt anpassbar — eine zusätzliche Pflicht-Checkbox direkt im Checkout ist dort nicht
ohne Weiteres umsetzbar.

**Praktikabler Weg:** Die Zustimmung wird **auf der Warenkorbseite** als Pflicht-Checkbox
erhoben, als Warenkorb-Attribut an die Bestellung gehängt und in der Bestellbestätigung
dokumentiert. Die genaue Ausgestaltung gehört in die anwaltliche Prüfung
(siehe [10 — Recht](10-legal-and-limits.md)) — technisch ist dieser Weg gangbar und wird
so von vielen deutschen Shops genutzt.

**Zu prüfen vor Vertragsabschluss:** aktuelle Shopify-Tarifpreise und der genaue Umfang der
Checkout-Anpassbarkeit im gewählten Tarif. Beides ändert sich regelmäßig.

### Was wir NICHT tun

- ❌ Kein Headless-Storefront zum Start. Verdoppelt den Aufwand, bringt bei diesem
  Seitenumfang keinen Vorteil.
- ❌ Keine 15 Apps. Jede App ist ein Fixkostenblock, ein Performance-Risiko und ein weiterer
  Auftragsverarbeiter, den man im Verzeichnis führen und im AVV benennen muss.
- ❌ Kein Page-Builder-Plugin. Es erzeugt genau das generische Aussehen, das wir vermeiden wollen.
- ❌ Kein eigenes Zahlungssystem. Shopify Payments oder etablierte Anbieter, fertig.

---

## 24. MVP-Definition (Deliverable 24)

Leitfrage: **Was ist das Minimum, das trotzdem wie eine echte Premium-Marke aussieht?**
Nicht: was ist das Minimum, das verkauft.

### ✅ MUSS zum Launch fertig sein

**Marke & Website**
- Markenname, markenrechtlich vorab recherchiert, Domain gesichert
- Logo-System, beide Themes, Design-Tokens umgesetzt
- Homepage · Weddings-LP · Hospitality-LP · About · FAQ · Kontakt
- **Alle Rechtstexte** (Impressum, DSE, AGB, Widerruf, AVV, Cookie-Consent)
- DE + EN
- Core Web Vitals im grünen Bereich

**Produkte — bewusst nur diese vier**
1. **Wedding Website + RSVP** (89 €) — vollständig, mit Editor
2. **Digital Invitation** (29 €) — dieselbe Engine, reduzierter Umfang
3. **Photo QR** (39 €) — Upload-Modul
4. **Kartenset** (39 €) — Dateiprodukt, 5 Karten
+ Bundle **ESSENTIALS** und **THE EXPERIENCE**

**Engine**
- Multi-Tenant-Kern, Blocksystem, beide Themes
- Editor mit Magic-Link-Zugang
- Statische Gästeansicht auf CDN (siehe oben)
- RSVP mit Export · Foto-Upload mit Löschfunktion
- QR-Erzeugung · Laufzeitverwaltung
- Automatische Provisionierung aus Shopify-Bestellungen
- Tägliche Backups, Wiederherstellung **einmal getestet** (nicht nur eingerichtet)

**Vertrauen**
- **3 öffentliche Live-Demos**, ohne Formular erreichbar
- 2 Produktvideos (Bildschirmaufnahmen)
- Echte About-Seite mit echten Personen

**Hospitality zum Launch: nur eine Landingpage mit Anfrageformular.** Kein Produkt, kein
Preis-Checkout, kein Vertrieb. Sie sammelt Interessenten und validiert Nachfrage, während
Weddings verkauft.

### ⏳ SPÄTER (Monat 4–9)

- Digital Guestbook, QR Games (Engine-Module, kleiner Aufwand)
- Wedding Weekend Website als SIGNATURE-Tier
- **Guest Guide** als vollwertiges Produkt + Abo-Abwicklung
- Etsy-Shop
- Weitere Kartensets (auf insgesamt 6–8)
- Wedding-Planer-Datei
- Custom-Experiences-Seite mit echten Referenzprojekten
- Klaviyo mit datumsbasierten Flows
- Bewertungssystem (sobald genug echte Bewertungen existieren)

### ❌ NICHT in Jahr 1

| Nicht bauen | Warum |
|---|---|
| **Complete Wedding Planner als Software** | Höchster Aufwand, niedrigste Zahlungsbereitschaft. Siehe [00](00-executive-summary.md#5-was-ich-aus-dem-sortiment-streichen-würde) |
| Hotel Guest Portal als Self-Service | Die ersten 3 Hotels **manuell** bedienen. Man lernt mehr und verkauft besser |
| White Label / Multi-Property-Verwaltung | Erst wenn mehrere Pro-Kunden danach fragen |
| Native App | Der gesamte Produktvorteil ist „ohne App" |
| Eigenes Analytics-/AB-Test-System | Bei diesen Besucherzahlen statistisch bedeutungslos |
| Marktplatz, Partnerportal, Wiederverkäufer-Dashboard | Erst ab echtem Partnerbedarf |
| KI-Funktionen ohne Geschäftszweck | Kein Feature ohne Business Case |

### Aufwandsschätzung MVP

| Bereich | Aufwand |
|---|---|
| Design System + Markenidentität | 2–3 Wochen |
| Shopify-Theme (2 Welten, alle Seiten) | 3–4 Wochen |
| Experience Engine (Kern, Editor, 3 Produkte) | **6–9 Wochen** |
| Provisionierung + Shopify-Anbindung | 1 Woche |
| Rechtstexte, Datenschutz, Zustimmungsprozesse | 1–2 Wochen (+ externe Prüfung) |
| Inhalte, Demos, Fotos, Videos | 2 Wochen |
| **Gesamt (überlappend gerechnet)** | **11–14 Wochen** |

Die Engine ist der kritische Pfad. Alles andere lässt sich parallel erledigen. Wenn der
Zeitrahmen eng wird, wird **Umfang gestrichen, nicht Qualität**: eher zwei Produkte
exzellent als vier mittelmäßig.
