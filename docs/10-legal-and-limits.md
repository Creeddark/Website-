# 10 — Rechtliche und technische Grenzen
*Deliverable 27 · Briefing §30*

> **Wichtiger Hinweis:** Das ist eine strukturierte Auflistung der Themen, die geklärt werden
> müssen, und keine Rechtsberatung. Ich bin kein Anwalt. Rechtstexte, der AVV, die
> Widerrufsprozesse und die steuerliche Einordnung gehören vor dem ersten Verkauf zu einem
> Fachanwalt für IT-Recht und zu einem Steuerberater. Das Budget dafür steht in
> [09 — Finanzen](09-financials.md#7-break-even-und-kapitalbedarf).
>
> Der Aufwand ist real, aber überschaubar — und **er ist deutlich kleiner, wenn er vorher
> passiert statt nachher.**

---

## 1. Die zentrale Frage: Wessen Daten verarbeiten wir eigentlich?

Das ist der rechtlich anspruchsvollste Punkt des gesamten Geschäftsmodells, und er wird von
fast allen Wettbewerbern ignoriert.

Unsere Produkte erheben Daten von **Dritten** — nicht vom Käufer, sondern von dessen Gästen:
Namen, Zusagen, Begleitpersonen, Nachrichten, Fotos, gelegentlich Ernährungshinweise.

### Hospitality (eindeutig)
Ein Hotel oder ein gewerblicher Gastgeber ist **Verantwortlicher** im Sinne der DSGVO, wir
sind **Auftragsverarbeiter**. Daraus folgt zwingend:

- **AVV nach Art. 28 DSGVO mit jedem einzelnen B2B-Kunden.** Lösung: als Anlage in die AGB
  integriert und beim Vertragsschluss aktiv bestätigt, zusätzlich als PDF abrufbar.
- **Liste der Unterauftragsverarbeiter** öffentlich (Hosting, Speicher, E-Mail-Versand,
  Zahlungsdienstleister) mit Änderungshinweis-Verfahren.
- **TOM-Dokumentation** nach Art. 32 — Hotels fragen im Einkaufsprozess danach.
- **Weisungsgebundenheit, Löschung nach Vertragsende, Unterstützung bei Betroffenenrechten.**

### Weddings (rechtlich weniger eindeutig)
Ein privates Brautpaar handelt möglicherweise im Rahmen der **Haushaltsausnahme**
(Art. 2 Abs. 2 lit. c DSGVO) — dann gilt die DSGVO für das Paar selbst nicht. Für **uns als
Diensteanbieter** gilt sie nach herrschender Auffassung trotzdem, und wir wären hier eher
selbst Verantwortlicher als Auftragsverarbeiter.

Das ist eine echte juristische Weichenstellung mit Folgen für AGB, Datenschutzerklärung und
Löschkonzept. **Diese Einordnung gehört ausdrücklich in die anwaltliche Prüfung.**

### Praktische Konsequenz für das Produktdesign — unabhängig von der Einordnung

Wir minimieren so weit, dass die Frage an Schärfe verliert:

| Maßnahme | Umsetzung |
|---|---|
| **Datensparsamkeit** | RSVP fragt Name und Zusage. Alles Weitere ist optional. |
| **Keine strukturierten Gesundheitsdaten** | Keine Auswahlliste für Allergien oder Unverträglichkeiten — das wären besondere Kategorien nach Art. 9. Stattdessen ein freies Feld „Anmerkungen an das Paar" mit klarem Hinweis. |
| **Keine Gastkonten** | Gäste legen nie ein Konto an. Kein Passwort, kein Profil, keine Historie. |
| **Kein Tracking in der Gästeansicht** | Keine Analytics, keine Werbepixel, keine Drittanbieter-Skripte. Das ist gleichzeitig Datenschutz, Ladezeit und Verkaufsargument. |
| **Automatische Löschung** | Alle Gästedaten werden nach Ablauf der Laufzeit + Karenzfrist automatisch gelöscht. Fristen dokumentiert, technisch erzwungen. |
| **Export und Löschung jederzeit** | Für den Kunden per Knopfdruck, nicht per Support-Ticket. |
| **EU-Hosting ausschließlich** | Vermeidet die gesamte Drittlandtransfer-Diskussion. |

### Fotouploads — der heikelste Bereich

Gäste laden Bilder hoch, auf denen andere Menschen zu sehen sind. Damit berühren wir
gleichzeitig Datenschutz, das Recht am eigenen Bild und das Urheberrecht des Fotografierenden.
Erforderlich:

- Klarer Hinweis **vor** dem Upload: wer die Bilder sieht, wie lange sie gespeichert werden,
  wie man sie entfernen lässt
- **Löschfunktion für den Kunden** (Bild einzeln entfernen) und eine erreichbare
  Meldemöglichkeit für Betroffene
- Verfahren für gemeldete rechtswidrige Inhalte — als Hostingdienst bestehen
  Reaktionspflichten (Digital Services Act); für sehr kleine Anbieter sind sie abgestuft,
  aber nicht null
- **Nicht öffentlich indexierbar**: `noindex`, nicht erratbare URLs, optionaler Zugriffsschutz
- Speicherbegrenzung pro Experience (technisch **und** in der Produktbeschreibung genannt)
- Automatische Löschung nach Ablauf, mit vorheriger Erinnerung zum Download

---

## 2. Pflichtangaben und Rechtstexte

| Dokument | Grundlage | Anmerkung |
|---|---|---|
| **Impressum** | § 5 DDG (vormals § 5 TMG) | Vollständig, leicht erreichbar, nicht hinter Klicks versteckt |
| **Datenschutzerklärung** | Art. 13/14 DSGVO | Muss **alle** eingesetzten Dienste benennen — jede App ist ein Empfänger |
| **AGB** | — | Getrennte Regelungen für Dateiprodukte, gehostete Dienste und B2B-Abos |
| **Widerrufsbelehrung + Musterformular** | §§ 355 ff. BGB | Siehe Abschnitt 3 |
| **AVV** | Art. 28 DSGVO | Mindestens für B2B, siehe oben |
| **Unterauftragsverarbeiter** | Art. 28 Abs. 2 | Öffentliche Liste |
| **Cookie-/Consent-Banner** | § 25 TDDDG, DSGVO | Ablehnen so einfach wie Zustimmen. Kein Nudging |
| **Barrierefreiheitserklärung** | BFSG | Siehe Abschnitt 7 |

Zusätzlich intern: **Verzeichnis von Verarbeitungstätigkeiten** (Art. 30), **TOM-Dokumentation**
(Art. 32), **Löschkonzept**, **Verfahren für Betroffenenanfragen** und **Meldeprozess für
Datenschutzverletzungen** (Art. 33, 72 Stunden).

---

## 3. Widerrufsrecht bei digitalen Produkten

Der Bereich, in dem am meisten falsch gemacht wird — und der bei Rückbuchungen und
Abmahnungen unmittelbar teuer wird.

**Die Grundlogik:** Verbraucher haben grundsätzlich 14 Tage Widerrufsrecht. Bei digitalen
Inhalten und Dienstleistungen kann es vorzeitig erlöschen — aber **nur**, wenn der Anbieter
den Ablauf korrekt gestaltet:

1. Der Kunde **stimmt ausdrücklich zu**, dass mit der Leistung vor Ablauf der Widerrufsfrist
   begonnen wird.
2. Der Kunde **bestätigt seine Kenntnis**, dass er dadurch sein Widerrufsrecht verliert
   (bei digitalen Inhalten) bzw. bei vollständiger Erbringung verliert (bei Dienstleistungen).
3. Der Anbieter **dokumentiert und bestätigt** das auf einem dauerhaften Datenträger.

Beides passiv über die AGB abzudecken genügt **nicht**. Es braucht eine aktive, separate,
nicht vorangehakte Bestätigung.

| Produkttyp | Einordnung | Was zu tun ist |
|---|---|---|
| **Typ A — Dateien** | Digitale Inhalte | Zustimmung + Kenntnisnahme vor dem Download |
| **Typ B — Hosted Experiences** | Eher digitale Dienstleistung | Zustimmung zum vorzeitigen Leistungsbeginn; Erlöschen erst bei vollständiger Erbringung — **die genaue Ausgestaltung anwaltlich klären** |
| **B2B-Abos** | Kein Verbrauchergeschäft | Kein Widerrufsrecht, aber saubere Kündigungs- und Laufzeitregeln |

**Technische Umsetzung:** Der Shopify-Checkout ist auf Standardtarifen nur begrenzt
anpassbar. Praktikabler Weg: Pflicht-Checkbox auf der **Warenkorbseite**, als
Bestellattribut gespeichert und in der Bestellbestätigung wiedergegeben. Siehe
[07 — Technik](07-mvp-and-tech.md#praktische-einschränkung-zustimmung-im-checkout).

---

## 4. Steuern und Rechnungsstellung

| Thema | Was zu klären ist |
|---|---|
| **Rechtsform** | Einzelunternehmen / GbR / UG / GmbH — Haftung ist hier das Hauptargument: wir verarbeiten Daten Dritter |
| **Kleinunternehmerregelung** | Schließt Vorsteuerabzug aus und wirkt im B2B unprofessionell. Bei geplantem Wachstum meist nicht sinnvoll — mit dem Steuerberater abwägen |
| **Umsatzsteuer B2C grenzüberschreitend** | Bei elektronisch erbrachten Leistungen an Verbraucher in anderen EU-Staaten kann die Steuer im **Land des Kunden** anfallen. Dafür gibt es das **OSS-Verfahren**. Ob und ab wann das greift, hängt von Schwellenwerten und der eigenen Konstellation ab — **vor dem Verkaufsstart klären** |
| **Umsatzsteuer B2B EU** | Reverse-Charge bei gültiger USt-IdNr., korrekter Rechnungshinweis, Prüfung der ID |
| **Rechnungspflichtangaben** | § 14 UStG. Shopify erstellt **nicht automatisch** rechtskonforme Rechnungen — eine App oder ein nachgelagerter Prozess ist nötig |
| **Preisangaben** | PAngV: gegenüber Verbrauchern **Bruttopreise inkl. USt.** Bei Abos zusätzlich Laufzeit und Gesamtpreis klar angeben |
| **Streichpreise** | Nur mit tatsächlich zuvor verlangtem Referenzpreis. Erfundene UVP sind wettbewerbswidrig |
| **Aufbewahrung** | Gesetzliche Fristen für Belege und Buchhaltung (mehrjährig) — aktuelle Dauer beim Steuerberater erfragen, sie wurde zuletzt geändert |

Shopify kann Steuersätze berechnen — **die Anmeldung und Abführung übernimmt es nicht.**
Das ist ein eigener Prozess.

---

## 5. Werbung, Bewertungen, Aussagen

- **Newsletter:** Double-Opt-in, Nachweis der Einwilligung, funktionierender Abmeldelink,
  Impressum in jeder Mail (§ 7 UWG).
- **Bewertungen:** Es muss dargelegt werden, ob und wie sichergestellt wird, dass sie von
  echten Käufern stammen. **Erfundene oder gekaufte Bewertungen sind wettbewerbswidrig und
  abmahnfähig** — und zerstören eine Premium-Positionierung dauerhaft.
- **Werbeaussagen:** Zeitangaben („in 30 Minuten fertig"), Erfolgsangaben („weniger
  Rückfragen") und Zahlen dürfen nur genannt werden, wenn sie belegbar sind. Bis dahin:
  qualitativ formulieren, nicht quantitativ.
- **Keine erfundene Knappheit** bei digitalen Produkten. Der einzige echte Knappheitshinweis
  sind die vier Custom-Slots pro Saison.

---

## 6. Lizenzen und Rechte an Material

| Material | Anforderung |
|---|---|
| **Schriften** | SIL-OFL-Schriften (Fraunces, Inter) — kommerziell nutzbar und **einbettbar in Kundenprodukte**. Kommerzielle Webfonts sind meist nach Domains lizenziert und bei tausenden Kunden-Subdomains nicht handhabbar. Siehe [03](03-design-system.md#schriftwahl--und-warum-open-source-hier-die-bessere-entscheidung-ist) |
| **Bilder mit Personen** | **Schriftliches Model Release erforderlich.** Auch bei Kundenfotos. Auch bei „nur für Instagram". Ohne Release nicht verwendbar |
| **Stockmaterial** | Lizenz je Bild prüfen und **dokumentieren**. Viele Lizenzen verbieten die Nutzung in weiterverkauften Vorlagen |
| **Icons / Grafiken** | Nur eigene oder eindeutig weiterverkaufslizenzierte |
| **⚠ Design-Werkzeuge** | Lizenzen gängiger Gestaltungswerkzeuge untersagen in der Regel den **Weiterverkauf von Designs, die im Wesentlichen aus deren eigenen Stock-Elementen bestehen**. Das ist der häufigste Grund für Shop-Sperrungen bei Hochzeitsvorlagen. Jedes verkaufte Design braucht eine dokumentierte Herkunft aller Elemente |
| **Karten / Karteninhalte** | Kartendienste haben Nutzungsbedingungen und Kosten. Alternative: statische Karte + Link zum Routenplaner — günstiger, schneller, datensparsamer |
| **Eigene Marke** | Recherche **vor** Gestaltung (DPMA + EUIPO, Klassen 09/35/42), Anmeldung zeitnah. Ein Namenswechsel nach dem Launch kostet ein Vielfaches |
| **Kundeninhalte** | AGB müssen regeln: der Kunde versichert, die Rechte an hochgeladenen Inhalten zu haben; wir erhalten nur ein Nutzungsrecht zur Erbringung der Leistung — **kein** Recht zur Eigenwerbung ohne gesonderte Einwilligung |

---

## 7. Barrierefreiheit

Das **Barrierefreiheitsstärkungsgesetz (BFSG)** stellt seit dem 28. Juni 2025 Anforderungen
an bestimmte Dienstleistungen im elektronischen Geschäftsverkehr gegenüber Verbrauchern.
Für **Kleinstunternehmen** (weniger als 10 Beschäftigte und begrenzter Jahresumsatz) gelten
bei Dienstleistungen Ausnahmen — die konkrete Einordnung gehört in die anwaltliche Prüfung.

**Unabhängig von der Pflicht bauen wir barrierefrei**, aus drei Gründen: die Ausnahme kann
mit Wachstum entfallen, es ist deutlich billiger als eine spätere Nachrüstung, und es
verbessert Bedienbarkeit und SEO ohnehin. Konkret: Kontraste nach WCAG AA, sichtbare
Fokuszustände, vollständige Tastaturbedienbarkeit, sinnvolle Alt-Texte, `prefers-reduced-motion`,
korrekte Formularbeschriftungen, semantisches HTML.

---

## 8. Technische Grenzen und Betriebsanforderungen

### Was wir zusagen können — und was nicht

| Zusage | Bewertung |
|---|---|
| „EU-Hosting" | ✅ Zusagbar, wenn tatsächlich umgesetzt |
| „Tägliche Backups" | ✅ Zusagbar, **wenn die Wiederherstellung getestet wurde**. Ein ungetestetes Backup ist kein Backup |
| „Datenexport jederzeit" | ✅ Zusagbar, wenn die Funktion existiert |
| „99,9 % Verfügbarkeit" | ⚠️ **Nur mit Messung und Konsequenz.** Ohne Statusseite und ohne Regelung für den Ausfall besser gar nicht zusagen |
| „Unbegrenzter Speicher" | ❌ Nie. Fotouploads sind der größte Kostentreiber. Grenzen nennen |
| „DSGVO-konform" | ⚠️ Zulässig als Beschreibung der eigenen Maßnahmen, nicht als Garantie für den Kunden |
| „Zertifiziert nach …" | ❌ Nur mit echtem Zertifikat |

### Betriebsanforderungen, die aus dem Geschäftsmodell folgen

1. **Der Hochzeitstag ist samstags.** Ausfälle passieren am Wochenende, wenn niemand arbeitet.
   → Statische Gästeansicht auf CDN (siehe [07](07-mvp-and-tech.md#der-wichtigste-architektonische-kniff-statische-gästeansicht)),
   Benachrichtigung bei Ausfall, und eine erreichbare Kontaktmöglichkeit an Wochenenden in
   der Hochsaison.
2. **Lastspitzen sind extrem.** 200 Gäste öffnen die Seite innerhalb weniger Minuten.
   → CDN, Lasttest vor dem Launch.
3. **Speicher wächst schneller als der Umsatz.** Eine Hochzeit erzeugt schnell mehrere
   Gigabyte an Fotos. → Kompression, Grenzen, automatische Löschung nach Ablauf.
4. **Missbrauch ist einkalkuliert.** Offene Uploadformulare werden früher oder später
   missbraucht. → Ratenbegrenzung, Dateityp- und Größenprüfung, Meldefunktion, Löschwerkzeuge.
5. **Sicherheit.** Keine Passwörter speichern (Magic Link), Verschlüsselung im Transport und
   bei Ablage, minimale Rechte, Abhängigkeiten aktuell halten, keine Gästedaten in Logs.
6. **Datenübertragbarkeit ist Vertrauen.** Wer jederzeit exportieren kann, kündigt seltener —
   und fragt im B2B-Einkauf zuerst danach.

---

## 9. Aussagen, die wir niemals treffen

Aus [01 — Hospitality-Konzept](01-brand.md#die-harte-grenze-7-des-briefings-verschärft), hier
als verbindliche Regel:

> Kein PMS. Keine Buchungsmaschine. Keine Zahlungsabwicklung. Keine digitalen Zimmerschlüssel.
> Keine Live-Verfügbarkeiten. Kein Echtzeit-Concierge. Keine Housekeeping-Steuerung.
> Keine Erfolgszahlen ohne Beleg. Keine Bewertungen ohne echten Käufer.

Diese Grenze ist kein Nachteil. Auf der B2B-Landingpage wird sie ausdrücklich als eigene
Sektion ausgespielt — Hoteliers haben genug Anbieter erlebt, die alles versprochen haben.
**Ehrliche Grenzen verkaufen besser als vage Versprechen.**

---

## 10. Checkliste vor dem ersten Verkauf

- [ ] Rechtsform gewählt, Gewerbe angemeldet
- [ ] Steuerliche Einordnung geklärt (USt., ggf. OSS, Rechnungsstellung)
- [ ] Impressum, Datenschutzerklärung, AGB, Widerrufsbelehrung + Musterformular geprüft
- [ ] AVV-Vorlage vorhanden, Unterauftragsverarbeiter veröffentlicht
- [ ] Verzeichnis von Verarbeitungstätigkeiten und TOM dokumentiert
- [ ] Löschkonzept technisch umgesetzt, nicht nur beschrieben
- [ ] Zustimmung zum vorzeitigen Leistungsbeginn im Bestellablauf umgesetzt
- [ ] Consent-Banner mit gleichwertiger Ablehnen-Option
- [ ] Keine Tracker in der Gästeansicht — verifiziert
- [ ] Alle Schriften, Bilder und Grafiken lizenziert und **dokumentiert**
- [ ] Model Releases für alle Bilder mit erkennbaren Personen
- [ ] Markenrecherche durchgeführt, Anmeldung eingereicht
- [ ] Backup-Wiederherstellung **einmal tatsächlich durchgeführt**
- [ ] Lasttest der Gästeansicht bestanden
- [ ] Keine unbelegten Zahlen in Werbetexten
- [ ] Bewertungsbereich leer statt gefüllt mit Erfundenem
