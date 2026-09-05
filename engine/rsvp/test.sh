#!/usr/bin/env bash
# =========================================================================
# RSVP — Prüflauf.
#
# Startet den Dienst auf einem eigenen Port mit einer Wegwerf-Datenbank und
# geht durch, was im Betrieb wirklich passiert: gültige Antworten, doppelte
# Antworten, Unsinn, Roboter, fremde Herkunft, falsches Token, Löschfrist.
#
#     bash engine/rsvp/test.sh
#
# Gibt am Ende die Zahl der Fehlschläge zurück.
# =========================================================================
set -u

HIER="$(cd "$(dirname "$0")" && pwd)"
PORT=8791
DB="$(mktemp -d)/pruef.sqlite"
TOKEN="pruef-token-mit-genug-zeichen-1234"
VON="https://paar.example"
URL="http://127.0.0.1:$PORT"

TOKEN="$TOKEN" DB="$DB" PORT="$PORT" HERKUNFT="$VON" \
  FESTE="alt-fest=2020-01-01,marlene-anton=2027-06-13" FRIST_TAGE=28 \
  node "$HIER/server.mjs" >/tmp/rsvp.log 2>&1 &
DIENST=$!
trap 'kill $DIENST 2>/dev/null; rm -rf "$(dirname "$DB")"' EXIT

for _ in $(seq 40); do
  curl -sf "$URL/gesundheit" >/dev/null 2>&1 && break
  sleep 0.1
done

GUT=0; SCHLECHT=0
pruef() { # name, erwartet, bekommen
  if [ "$2" = "$3" ]; then GUT=$((GUT+1)); printf '  ok    %s\n' "$1"
  else SCHLECHT=$((SCHLECHT+1)); printf '  FEHLT %s — erwartet %s, bekommen %s\n' "$1" "$2" "$3"; fi
}

senden() { # koerper, [herkunft]
  curl -s -o /tmp/rsvp.out -w "%{http_code}" -X POST "$URL/rsvp" \
    -H "content-type: application/json" -H "origin: ${2:-$VON}" -d "$1"
}

echo "— Absenden —"
pruef "gültige Antwort" 200 "$(senden '{"kennung":"marlene-anton","name":"Katharina Vogt","mail":"k@example.org","zusage":"ja","anzahl":2,"essen":"vegetarisch","gruss":"Wir freuen uns!","dauer":9000}')"
pruef "zweite Person"   200 "$(senden '{"kennung":"marlene-anton","name":"Jonas Feld","mail":"j@example.org","zusage":"nein","dauer":7000}')"
pruef "dieselbe Person nochmal" 200 "$(senden '{"kennung":"marlene-anton","name":"Katharina Vogt","mail":"K@Example.ORG","zusage":"ja","anzahl":3,"dauer":6000}')"

echo "— Abwehr —"
pruef "fremde Herkunft"   403 "$(senden '{"kennung":"marlene-anton","name":"X","mail":"x@example.org","zusage":"ja","dauer":9000}' 'https://fremd.example')"
pruef "ohne Herkunft"     403 "$(curl -s -o /dev/null -w '%{http_code}' -X POST "$URL/rsvp" -H 'content-type: application/json' -d '{}')"
pruef "kaputtes JSON"     400 "$(senden 'kein json')"
pruef "Name fehlt"        422 "$(senden '{"kennung":"marlene-anton","mail":"y@example.org","zusage":"ja","dauer":9000}')"
pruef "Mail unbrauchbar"  422 "$(senden '{"kennung":"marlene-anton","name":"Y","mail":"keine-mail","zusage":"ja","dauer":9000}')"
pruef "Zusage fehlt"      422 "$(senden '{"kennung":"marlene-anton","name":"Y","mail":"y@example.org","dauer":9000}')"
pruef "Kennung mit Pfad"  422 "$(senden '{"kennung":"../etc","name":"Y","mail":"y@example.org","zusage":"ja","dauer":9000}')"
pruef "Honigtopf gefüllt" 200 "$(senden '{"kennung":"marlene-anton","name":"Bot","mail":"bot@example.org","zusage":"ja","hp":"x","dauer":9000}')"
pruef "zu schnell"        200 "$(senden '{"kennung":"marlene-anton","name":"Bot2","mail":"bot2@example.org","zusage":"ja","dauer":200}')"
pruef "Vorflug erlaubt"   204 "$(curl -s -o /dev/null -w '%{http_code}' -X OPTIONS "$URL/rsvp" -H "origin: $VON")"
pruef "Vorflug fremd"     403 "$(curl -s -o /dev/null -w '%{http_code}' -X OPTIONS "$URL/rsvp" -H 'origin: https://fremd.example')"

echo "— Auswertung —"
pruef "Liste ohne Token" 401 "$(curl -s -o /dev/null -w '%{http_code}' "$URL/liste?kennung=marlene-anton")"
pruef "Liste falsches Token" 401 "$(curl -s -o /dev/null -w '%{http_code}' -H 'authorization: Bearer falsch' "$URL/liste?kennung=marlene-anton")"
LISTE="$(curl -s -H "authorization: Bearer $TOKEN" "$URL/liste?kennung=marlene-anton")"
pruef "zwei Antworten (kein Doppel)" 2 "$(node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>console.log(JSON.parse(s).antworten.length))' <<<"$LISTE")"
pruef "Köpfe zusammengezählt"        3 "$(node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>console.log(JSON.parse(s).summe.koepfe))' <<<"$LISTE")"
pruef "Roboter nicht gespeichert"    2 "$(node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>console.log(JSON.parse(s).antworten.filter(a=>a.name.startsWith("Bot")).length+2))' <<<"$LISTE")"

CSV="$(curl -s -H "authorization: Bearer $TOKEN" "$URL/export?kennung=marlene-anton")"
# Die Pruefung laeuft ueber node, nicht ueber grep: grep deutet \xef nicht,
# und ein Gruss darf einen Zeilenumbruch enthalten — dann zaehlt "wc -l"
# falsch, die Zeile steht ja in Anfuehrungszeichen.
csv_pruef() { node -e '
  let s = ""; process.stdin.on("data", d => s += d).on("end", () => {
    const bom = s.charCodeAt(0) === 0xFEFF;
    const kopf = s.slice(1).startsWith(`"Name";"E-Mail"`);
    // Datensaetze zaehlen: eine Zeile beginnt mit einem Anfuehrungszeichen
    // am Zeilenanfang, Fortsetzungen eines Grusses nicht.
    const zeilen = s.slice(1).split(/\r\n(?=")/).filter(Boolean).length;
    console.log(`${bom ? 1 : 0} ${kopf ? 1 : 0} ${zeilen}`);
  });'; }
read -r BOM KOPF ZEILEN <<<"$(csv_pruef <<<"$CSV")"
pruef "CSV beginnt mit BOM"  1 "$BOM"
pruef "CSV hat die Kopfzeile" 1 "$KOPF"
pruef "CSV: Kopf und zwei Antworten" 3 "$ZEILEN"

echo "— Frist und Löschen —"
pruef "altes Fest ist weg" 0 "$(node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>console.log(JSON.parse(s).antworten.length))' <<<"$(curl -s -H "authorization: Bearer $TOKEN" "$URL/liste?kennung=alt-fest")")"
pruef "Löschen ohne Token" 401 "$(curl -s -o /dev/null -w '%{http_code}' -X DELETE "$URL/rsvp?kennung=marlene-anton")"
pruef "Löschen mit Token"  200 "$(curl -s -o /dev/null -w '%{http_code}' -X DELETE -H "authorization: Bearer $TOKEN" "$URL/rsvp?kennung=marlene-anton")"
pruef "danach leer"          0 "$(node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>console.log(JSON.parse(s).antworten.length))' <<<"$(curl -s -H "authorization: Bearer $TOKEN" "$URL/liste?kennung=marlene-anton")")"

echo "— Ratenbremse —"
for i in $(seq 14); do senden "{\"kennung\":\"marlene-anton\",\"name\":\"P$i\",\"mail\":\"p$i@example.org\",\"zusage\":\"ja\",\"dauer\":9000}" >/dev/null; done
pruef "greift nach zwölf" 429 "$(senden '{"kennung":"marlene-anton","name":"Z","mail":"z@example.org","zusage":"ja","dauer":9000}')"

echo
echo "$GUT bestanden, $SCHLECHT fehlgeschlagen"
exit $SCHLECHT
