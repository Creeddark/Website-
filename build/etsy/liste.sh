#!/usr/bin/env bash
# =========================================================================
# Eine Aufnahme der Liste, die nur das Paar sieht.
#
# Startet den RSVP-Dienst mit einer Wegwerf-Datenbank, legt sieben erfundene
# Antworten hinein und nimmt die Uebersicht auf. Danach ist alles wieder weg.
#
#     bash build/etsy/liste.sh
# =========================================================================
set -u

HIER="$(cd "$(dirname "$0")" && pwd)"
WURZEL="$(cd "$HIER/../.." && pwd)"
PORT=8796
DB="$(mktemp -d)/schau.sqlite"
TOKEN="schaubild-token-mit-genug-zeichen"
VON="https://schau.example"
URL="http://127.0.0.1:$PORT"

TOKEN="$TOKEN" DB="$DB" PORT="$PORT" HERKUNFT="$VON" \
  FESTE="marlene-anton=2027-06-13" FRIST_TAGE=28 \
  node "$WURZEL/engine/rsvp/server.mjs" >/dev/null 2>&1 &
DIENST=$!
trap 'kill $DIENST 2>/dev/null; rm -rf "$(dirname "$DB")"' EXIT

for _ in $(seq 40); do
  curl -sf "$URL/gesundheit" >/dev/null 2>&1 && break
  sleep 0.1
done

senden() {
  curl -s -o /dev/null -X POST "$URL/rsvp" -H "content-type: application/json" \
    -H "origin: $VON" -d "$1"
}

# Erfundene Gaeste, example.org — die Adresse ist fuer genau das reserviert.
senden '{"kennung":"marlene-anton","name":"Katharina Vogt","mail":"katharina.vogt@example.org","zusage":"ja","anzahl":2,"essen":"vegetarisch","gruss":"Wir freuen uns riesig! Kommen schon Samstag an.","dauer":9000}'
senden '{"kennung":"marlene-anton","name":"Jonas Feld","mail":"jonas@example.org","zusage":"nein","gruss":"Leider verhindert — feiert schön!","dauer":9000}'
senden '{"kennung":"marlene-anton","name":"Ada Reiter","mail":"a.reiter@example.org","zusage":"ja","anzahl":1,"essen":"alles","gruss":"","dauer":9000}'
senden '{"kennung":"marlene-anton","name":"Familie Sandberg","mail":"sandberg@example.org","zusage":"ja","anzahl":4,"essen":"alles","gruss":"Die Kinder kommen mit, zwei Hochstühle wären toll.","dauer":9000}'
senden '{"kennung":"marlene-anton","name":"Milan Örs","mail":"milan.oers@example.org","zusage":"ja","anzahl":1,"essen":"vegan","gruss":"","dauer":9000}'
senden '{"kennung":"marlene-anton","name":"Beate Lindqvist","mail":"beate@example.org","zusage":"nein","gruss":"","dauer":9000}'
senden '{"kennung":"marlene-anton","name":"Tobias Achterberg","mail":"t.achterberg@example.org","zusage":"ja","anzahl":2,"essen":"alles","gruss":"Bringen die gute Gitarre mit.","dauer":9000}'

python3 "$HIER/liste.py" "$PORT" "$TOKEN"
