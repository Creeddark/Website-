# RSVP

Der Dienst hinter dem Antwortformular. Nimmt Rückmeldungen entgegen, legt sie
in eine SQLite-Datei, zeigt sie dem Paar und gibt sie als CSV heraus.

**Keine Abhängigkeiten.** Node 22 bringt HTTP und SQLite mit. Was nicht
installiert wird, kann auch nicht veralten, und es gibt keinen Anbieter, an
dem man später hängt: der Dienst läuft auf jedem Server in der EU, auf dem
Node liegt. Ein Ein-Kern-Server für vier Euro im Monat trägt hunderte
Einladungen gleichzeitig.

```
engine/rsvp/
  server.mjs               der ganze Dienst, eine Datei
  test.sh                  27 Prüfungen gegen den Dienst allein
  test-ende-zu-ende.sh     ein echter Browser durch das echte Formular
  browser.py               was der Browser dabei tut
```

## Prüfen

```bash
bash engine/rsvp/test.sh              # 27 Prüfungen
bash engine/rsvp/test-ende-zu-ende.sh # 9 Prüfungen, braucht Playwright
```

Der zweite Lauf verstellt die Einladung kurzzeitig auf einen lokalen Dienst
und setzt sie danach zurück, auch wenn er abbricht.

---

## Starten

```bash
TOKEN=… HERKUNFT=https://marlene-anton.example node engine/rsvp/server.mjs
```

| Variable | Vorgabe | Bedeutung |
|---|---|---|
| `TOKEN` | — | **Pflicht**, mindestens 24 Zeichen. Damit holt das Paar seine Liste. `openssl rand -base64 33` |
| `HERKUNFT` | leer | Adressen, von denen gesendet werden darf, mit Komma getrennt. **Leer heißt: niemand.** Ein offener Endpunkt ist eine Einladung an jeden Spam-Roboter. |
| `PORT` | 8787 | |
| `DB` | `./rsvp.sqlite` | Pfad der Datenbank |
| `FESTE` | leer | `kennung=YYYY-MM-DD`, mit Komma getrennt. Grundlage der Löschfrist. |
| `FRIST_TAGE` | 28 | Tage nach dem Fest, nach denen die Antworten von selbst verschwinden |

Ohne `FESTE` löscht der Dienst nichts von selbst. Dann muss jemand daran
denken, und irgendwann denkt niemand mehr daran.

## Wege

| Weg | Wer | Wozu |
|---|---|---|
| `POST /rsvp` | der Gast | die Antwort. Nur von einer Adresse aus `HERKUNFT`. |
| `GET /uebersicht?kennung=…` | das Paar | Seite mit Zahlen, Tabelle und CSV-Knopf |
| `GET /liste?kennung=…` | das Paar | dasselbe als JSON, Token im `Authorization`-Kopf |
| `GET /export?kennung=…` | das Paar | CSV, mit BOM, damit Excel die Umlaute richtig zeigt |
| `DELETE /rsvp?kennung=…` | das Paar | alles zu einer Einladung löschen |
| `GET /gesundheit` | die Überwachung | |

Das Token steht immer im Kopf `Authorization: Bearer …`, nie in der Adresse.
Adressen landen in Verläufen, Lesezeichen und Serverprotokollen.

---

## Was der Dienst gegen Missbrauch tut

- **Herkunft.** Nur von den eingetragenen Adressen wird etwas angenommen.
- **Ratenbremse.** Zwölf Anfragen je zehn Minuten und IP-Adresse. Die
  Adressen stehen dabei nur im Arbeitsspeicher und nie in der Datenbank.
- **Honigtopf.** Ein Feld, das niemand sieht. Wer es ausfüllt, ist kein
  Mensch und bekommt trotzdem „in Ordnung" zurück — wer erfährt, dass er
  erkannt wurde, probiert es anders herum nochmal.
- **Zeitbremse.** Wer in unter anderthalb Sekunden absendet, hat nicht
  gelesen. Kein Bilderrätsel, kein fremdes Skript, keine Daten an Dritte.
- **Token zeitgleich verglichen.** Über den Hash, damit die Dauer des
  Vergleichs nichts über die Länge verrät.
- **Grenzen überall.** 16 KB Körper, Längen je Feld, feste Auswahl bei
  Zusage und Essen, Kennung nur aus Kleinbuchstaben, Ziffern und Strich.

Doppelte Antworten derselben Adresse **ersetzen** die vorige. Menschen
antworten zweimal: weil sie sich vertippt haben, weil sie umdisponieren.
Ohne das steht dieselbe Person dreimal auf der Gästeliste.

---

## Dauerhaft betreiben

### systemd

```ini
# /etc/systemd/system/rsvp.service
[Unit]
Description=RSVP
After=network.target

[Service]
Type=simple
User=rsvp
WorkingDirectory=/opt/rsvp
Environment=PORT=8787
Environment=DB=/var/lib/rsvp/rsvp.sqlite
Environment=HERKUNFT=https://marlene-anton.example
Environment=FESTE=marlene-anton=2027-06-13
EnvironmentFile=/etc/rsvp.env
ExecStart=/usr/bin/node /opt/rsvp/server.mjs
Restart=always
RestartSec=3

# Der Dienst braucht nichts vom System ausser seiner Datenbank.
NoNewPrivileges=yes
PrivateTmp=yes
ProtectSystem=strict
ProtectHome=yes
ReadWritePaths=/var/lib/rsvp

[Install]
WantedBy=multi-user.target
```

Das Token gehört in `/etc/rsvp.env` mit `chmod 600`, nicht in die Unit —
Units liest jeder auf dem Rechner.

```
TOKEN=hier-das-lange-zufaellige-token
```

### Davor ein Proxy mit TLS

```
# /etc/caddy/Caddyfile
rsvp.marke.example {
    reverse_proxy 127.0.0.1:8787
}
```

Caddy holt das Zertifikat von selbst. Der Dienst spricht bewusst kein TLS:
das kann ein Proxy besser, und beim nächsten Zertifikatsproblem muss niemand
den Dienst anfassen.

### Sicherung

Die Datenbank ist eine Datei. Für eine konsistente Kopie im laufenden
Betrieb:

```bash
sqlite3 /var/lib/rsvp/rsvp.sqlite ".backup /sicherung/rsvp-$(date +%F).sqlite"
```

Täglich per Cron, und die Kopie liegt woanders als der Server. Eine
Gästeliste, die drei Wochen vor der Hochzeit weg ist, ist ein Anruf, den
niemand führen will.

---

## Die Einladung anschließen

In `themes/<theme>/daten.json`:

```json
"rsvp": {
  "endpunkt": "https://rsvp.marke.example",
  "kennung": "marlene-anton"
}
```

Dann `python3 build/einladung.py`. Das erzeugt die Einladung neu **und legt
die Datenschutzseite an** — ohne Endpunkt gibt es sie nicht, weil dann auch
nichts verarbeitet wird.

Die `kennung` muss zu der in `FESTE` passen, sonst greift die Löschfrist
nicht.

---

## Was der Dienst absichtlich nicht tut

- **Keine E-Mail.** Es gibt keine Benachrichtigung bei einer neuen Antwort.
  Das bräuchte einen Mailversand-Dienst und damit einen weiteren
  Auftragsverarbeiter im Vertrag. Das Paar sieht seine Liste unter
  `/uebersicht`.
- **Keine Anmeldung für Gäste.** Gäste bekommen nie ein Konto. Das wäre ein
  Conversion-Killer und zusätzliche Datenlast, siehe `docs/07-mvp-and-tech.md`.
- **Keine Abfrage von Allergien.** Das sind Gesundheitsdaten nach Art. 9
  DSGVO. Das Formular fragt eine Vorliebe am Tisch, mehr nicht.
- **Keine Zugriffsprotokolle mit Inhalten.** Protokolliert werden Kennung,
  Zusage und Anzahl — nicht Name, Mail oder Nachricht.

## Bevor das erste Exemplar verkauft wird

- [ ] Auftragsverarbeitungsvertrag mit dem Paar. Vorlage: `site/recht/avv.html`
- [ ] Server in der EU, Vertrag mit dem Rechenzentrum
- [ ] Datenschutzseite anwaltlich prüfen lassen — der Text in
      `build/datenschutz.py` ist ein Entwurf, siehe `docs/10-legal-and-limits.md`
- [ ] Sicherung eingerichtet und einmal zurückgespielt
- [ ] `FESTE` eingetragen, Löschfrist einmal beobachtet
- [ ] Token je Kunde verschieden
