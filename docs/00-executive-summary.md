# 00 — Executive Summary

Du hast im Briefing geschrieben: *„Du darfst mich nicht einfach bestätigen."*
Also fange ich damit an.

---

## 1. Was am Briefing trägt

- **Die Markenidee ist richtig.** „Digital Experiences" statt „Templates" ist eine echte
  Positionierung mit Preissetzungsmacht. Der Markt ist voll von 12-€-Canva-Dateien; ein
  Anbieter, der sich wie eine Marke verhält, kann das 5-fache verlangen.
- **Zwei Welten unter einem Dach ist strukturell klug** — aber aus einem anderen Grund, als
  du annimmst (siehe Punkt 4 unten).
- **Premium-Ästhetik als Differenzierung** funktioniert in genau diesen zwei Märkten
  besonders gut, weil beide Kunden Ästhetik *als Produktnutzen* kaufen, nicht als Verpackung.
- **Der Fokus auf wenige, exzellent präsentierte Produkte** statt 30 Listings ist die
  richtige Entscheidung und der häufigste Fehler, den Wettbewerber machen.

---

## 2. Der größte blinde Fleck: Das sind keine Templates

Das Briefing behandelt „Digital Wedding Invitation" und „Hotel Guest Portal" wie dieselbe
Art Produkt — eine Datei, die man einmal designt und beliebig oft verkauft. Das stimmt für
fast nichts auf deiner Liste.

| Produkt | Was es wirklich ist |
|---|---|
| Wedding Website | Gehostete Webanwendung, Editor, Uptime, Support, jahrelange Laufzeit |
| RSVP | Erhebung personenbezogener Daten Dritter (Gäste) → Auftragsverarbeitung |
| Digital Guestbook | User-Generated Content, Moderation, Speicher, Missbrauchsrisiko |
| Photo QR | Fotouploads Dritter → Speicherkosten, Bildrechte, Löschpflichten |
| QR Games | Live-State, Punktestand, Concurrency |
| Wedding Planner | Vollwertige App mit Account und Datenhaltung |
| Guest Guide / Hotel Portal | Dauerhaft laufender, vom Kunden editierbarer Dienst |
| Save the Date / Menu / Thank You Cards | ✅ **Das** sind echte Dateiprodukte |

**Konsequenz:** Wir bauen kein Template-Business mit ein bisschen Technik. Wir bauen ein
kleines Softwareunternehmen mit einem sehr guten Shop davor. Das ist machbar — aber der
Aufwand, das Risiko und die Rechtslage sind eine andere Kategorie, und die Planung muss das
abbilden. Wer das ignoriert, verkauft im Monat 3 Produkte, die er im Monat 9 nicht mehr
betreiben kann.

---

## 3. Die Entscheidung, die alles rettet: eine Engine, nicht sieben Produkte

Schau dir die Liste noch einmal an. Wedding Website, Weekend Website, Digital Invitation,
Guest Guide, Hotel Portal — das sind **nicht fünf Produkte**. Das ist **ein Produkt in fünf
Konfigurationen**:

> Eine gehostete, mobil-first Micro-Site mit modularen Inhaltsblöcken, einem Editor für den
> Besitzer, einem QR-/Link-Einstieg und optionalen Gast-Input-Modulen
> (RSVP, Gästebuch, Fotoupload, Spiel).

Der Unterschied zwischen einer Wedding Website und einem Hotel Guest Portal ist:
**welche Blöcke freigeschaltet sind, welches Theme greift, welcher Preis dranhängt.**

Das ist die wichtigste technische *und* wirtschaftliche Entscheidung des ganzen Projekts:

- **Sieben Produkte einzeln bauen** → ~7× Entwicklungszeit, 7× Wartung, du wirst nie fertig.
- **Eine Engine + Blockbibliothek** → das zweite Produkt kostet Tage statt Monate, und jede
  Verbesserung am Kern verbessert das gesamte Sortiment gleichzeitig.

Alles Weitere in dieser Strategie baut darauf auf. Details: [07 — MVP & Technik](07-mvp-and-tech.md).

---

## 4. Cross-Selling ist die falsche Begründung für zwei Welten

Im Briefing (§4) ist Cross-Selling die Klammer zwischen Weddings und Hospitality. Ehrlich:
**das wird kaum Umsatz bringen.** Ein Paar, das eine digitale Einladung für 29 € kauft, wird
nie ein Hotel Guest Portal kaufen — es besitzt kein Hotel. Der einzige echte Überschneidungs-
fall ist die Destination Wedding, und das ist ein schmales Segment.

Die zwei Welten sind trotzdem richtig — aus drei **anderen** Gründen:

1. **Gegensaisonalität.** Wedding-Käufe konzentrieren sich stark (Verlobungen um den
   Jahreswechsel, Käufe Januar–Juni für Sommerhochzeiten). September–November ist schwach.
   Hospitality läuft ganzjährig und trägt genau diese Monate.
2. **Wiederkehrender Umsatz.** Eine Hochzeit passiert einmal — der Kunde ist danach weg.
   Ein Gastgeber zahlt jedes Jahr. Hospitality macht aus einem Projektgeschäft ein
   Unternehmen mit planbarem Cashflow. **Das** ist die Säule, von der man leben kann.
3. **Grenzkosten nahe null.** Weil beides dieselbe Engine ist, kostet die zweite Welt fast
   nur Marketing, nicht Entwicklung.

Cross-Selling bauen wir trotzdem ein — aber als eleganten Randfall (Destination-Wedding-
Paare, die Gästeunterkünfte organisieren; Gastgeber, die Hochzeitslocation sind), nicht als
Geschäftsmodell. Details: [01 — Brand](01-brand.md#5-die-verbindung-deliverable-5).

---

## 5. Was ich aus dem Sortiment streichen würde

**`COMPLETE WEDDING PLANNER` — nicht bauen. Jedenfalls nicht als Software, nicht in Jahr 1.**

Budget + Gästeliste + Sitzplan + Timeline + To-dos + Dienstleister ist eine vollwertige
Projektmanagement-App. Sie konkurriert gegen etablierte, teilweise kostenlose Tools, hat den
höchsten Entwicklungsaufwand deiner ganzen Liste, erzeugt den meisten Support, und die
Zahlungsbereitschaft ist niedriger als bei allem anderen — weil Excel „auch geht".

*Stattdessen:* ein sehr gut gestalteter Planer als **Dateiprodukt** (Notion-Template oder
Spreadsheet) für 19 €. Kostet 2–3 Tage statt 3 Monate, besetzt das SEO-Keyword, generiert
E-Mail-Adressen von Menschen, die *gerade mit der Planung beginnen* — also genau die
Zielgruppe für alle anderen Produkte. Wenn es sich verkauft, reden wir in Jahr 2 über Software.

**`QR WEDDING GAMES` — nicht als Hero-Produkt.** Charmant und differenzierend, aber die
Zahlungsbereitschaft als Einzelprodukt ist niedrig und der Build (Live-State, Punktestand)
ist überproportional. Richtige Rolle: **Bundle-Zugabe und Social-Content-Magnet.** Als
TikTok-Hook ist es besser als als Produkt.

**30 Kartendesigns — nein.** 6–8 exzellente, in sich stimmige Sets schlagen 30 mittelmäßige.
Mehr Designs erhöhen die Auswahlparalyse, nicht den Umsatz.

---

## 6. Was am Zeitplan nicht funktioniert

Das Briefing (§33) will in 90 Tagen: Brand + Website + Hero Products + Launch + Etsy +
Pinterest + Instagram/TikTok + SEO + Hospitality B2B + Custom Services. Das sind **sechs
parallele Go-to-Market-Motionen** plus ein Software-Build, vermutlich mit 1–2 Personen.

Das geht nicht schief, weil es zu ehrgeizig ist. Es geht schief, weil **jeder einzelne
Kanal nur mit Beharrlichkeit funktioniert** — Pinterest braucht 60–120 Tage konsequentes
Pinnen, bevor Traffic entsteht; B2B-Hospitality braucht Referenzen, die man erst haben muss.
Sechs Kanäle halbherzig sind schlechter als zwei konsequent.

**Mein Vorschlag für die ersten 90 Tage:**

| | |
|---|---|
| **Bauen** | Engine + Wedding Website/RSVP + Digital Invitation + Photo QR + 1 Kartenset |
| **Marke** | Vollständige Identität, beide Themes, Website live, Recht vollständig |
| **Kanäle** | **Nur** Pinterest (ab Woche 3, täglich) + Etsy (ab Woche 9, nur Dateiprodukte) |
| **Hospitality** | Nur Landingpage mit Warteliste/Anfrage — **kein** Produkt, **kein** Vertrieb |
| **Später (Monat 4–6)** | Gästebuch, Games, Weekend-Tier, Hospitality-Pilot mit 3 Design-Partnern |
| **Später (Monat 6–12)** | Instagram/TikTok systematisch, SEO-Cluster, Hotel Portal individuell |

Hospitality wird dadurch nicht unwichtiger — es wird nur *nach* dem Beweis gebaut, dass die
Engine trägt. Die drei ersten Hospitality-Kunden bedient man **manuell** (Done-for-you-Setup),
nicht mit Self-Service-Software. Das ist schneller, lehrreicher und verkauft besser.

---

## 7. Die sieben Entscheidungen, an denen alles hängt

| # | Entscheidung | Meine Empfehlung |
|---|---|---|
| 1 | Template-Shop oder Software-Produkt? | **Software** — mit einer Engine, nicht sieben Builds |
| 2 | Shopify als Produkt oder als Kasse? | **Kasse + Storefront.** Die Experiences laufen außerhalb |
| 3 | Ein Shop oder zwei? | **Ein Shop**, zwei Themes/Templates. Zwei Shops = doppelte Kosten, halbierte SEO-Autorität |
| 4 | Weddings und Hospitality parallel? | **Sequenziell.** Weddings zuerst, Hospitality ab Monat 4 |
| 5 | Abo oder Einmalkauf? | **Weddings: Einmalkauf mit befristeter Laufzeit** (18 Monate inkl.). **Hospitality: Abo, jährlich bevorzugt** |
| 6 | Deutsch oder Englisch? | **Beides, DE als Primärmarkt.** Markenkommunikation englisch, Recht + Verkaufsprozess deutsch — siehe [11](11-open-decisions.md) |
| 7 | Preisniveau | **Höher als im Briefing.** 49 € für eine gehostete Wedding Website mit 18 Monaten Betrieb ist zu billig — siehe [02](02-product-and-pricing.md) |

---

## 8. Die ehrliche Einschätzung zum Ziel „davon leben"

Das Ziel ist erreichbar. Der Zeitrahmen im Kopf ist es meistens nicht. Realistischer Korridor,
**unter der Bedingung, dass die Engine wirklich fertig wird und Pinterest konsequent läuft**:

| Meilenstein | Realistisch ab |
|---|---|
| Erste Verkäufe | Monat 2–3 |
| 1.000 €/Monat | Monat 4–7 |
| 3.000 €/Monat | Monat 9–14 |
| 5.000 €/Monat | Monat 12–20 |
| 10.000 €/Monat | Monat 18–30 — **nur mit funktionierendem Hospitality-Abo** |

Der Sprung von 3.000 € auf 10.000 € kommt **nicht** aus mehr Wedding-Verkäufen. Er kommt aus
wiederkehrendem Hospitality-Umsatz, der sich stapelt. 40 Gastgeber à 65 €/Monat sind
2.600 € planbarer Umsatz, jeden Monat, ohne neuen Traffic. Das ist der eigentliche Motor.

Rechenwege, Kostenstruktur und Sensitivitäten: [09 — Finanzen](09-financials.md).

---

## 9. Die vier größten Risiken

1. **Betriebsrisiko.** Du verkaufst Dienste, die am Hochzeitstag funktionieren müssen. Ein
   Ausfall an einem Samstag im Juli ist kein Bug, sondern ein zerstörter Tag und eine
   öffentliche Rezension. → Uptime, Backups, Read-only-Fallback und Support-Fenster am
   Wochenende sind Produktanforderungen, keine Kür. Siehe [10](10-legal-and-limits.md).
2. **Rechtsrisiko.** RSVP-, Gästebuch- und Foto-Module verarbeiten personenbezogene Daten
   *Dritter*. Du wirst dabei mit hoher Wahrscheinlichkeit Auftragsverarbeiter — mit
   AVV-Pflicht gegenüber **jedem einzelnen Kunden**. Das muss in AGB und Checkout eingebaut
   sein, bevor der erste Verkauf stattfindet.
3. **Saisonrisiko.** Ohne Hospitality hast du drei schwache Monate pro Jahr.
4. **Fokusrisiko.** Das größte. Neun Phasen parallel ist der wahrscheinlichste Grund,
   warum dieses Projekt scheitert.

---

## 10. Was als Nächstes passiert

Diese Strategie ist die Grundlage — jetzt braucht sie **deine Entscheidungen** zu den offenen
Punkten in [11 — Offene Entscheidungen](11-open-decisions.md), allen voran dem Markennamen.
Ohne Namen kein Logo, keine Domain, kein Shop, keine Markenanmeldung.

Danach beginnt die Umsetzung in dieser Reihenfolge: Design System → Engine-Kern →
Wedding Website als erstes Produkt → Shopify-Storefront → Recht → Launch.
