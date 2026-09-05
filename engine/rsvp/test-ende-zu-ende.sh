#!/usr/bin/env bash
# =========================================================================
# RSVP — Prüflauf durch den ganzen Weg.
#
# Der Dienst für sich ist geprüft (test.sh). Hier geht es um das, was
# dazwischen liegt: ein echter Browser füllt das echte Formular aus, die
# Antwort landet wirklich in der Datenbank, und wenn der Dienst weg ist,
# verhält sich die Seite so, wie ein Gast es aushält.
#
#     bash engine/rsvp/test-ende-zu-ende.sh
# =========================================================================
set -u

HIER="$(cd "$(dirname "$0")" && pwd)"
WURZEL="$(cd "$HIER/../.." && pwd)"
THEME="$WURZEL/themes/ambra"
PORT=8796
WEB=8100
TOKEN="ende-zu-ende-token-mit-zeichen-99"
TMP="$(mktemp -d)"
DB="$TMP/e2e.sqlite"

sicherung="$TMP/daten.json"
cp "$THEME/daten.json" "$sicherung"

aufraeumen() {
  kill "${DIENST:-}" "${SEITE:-}" 2>/dev/null
  cp "$sicherung" "$THEME/daten.json"
  (cd "$WURZEL" && python3 build/einladung.py >/dev/null)
  rm -rf "$TMP"
}
trap aufraeumen EXIT

# ---- Einladung auf den Dienst zeigen lassen und neu erzeugen
python3 - "$THEME/daten.json" "http://127.0.0.1:$PORT" <<'PY'
import json, sys, pathlib
p = pathlib.Path(sys.argv[1]); d = json.loads(p.read_text(encoding="utf-8"))
d["rsvp"]["endpunkt"] = sys.argv[2]
d["vorschau"] = False
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
PY
(cd "$WURZEL" && python3 build/einladung.py)

# ---- Dienst und Webserver
TOKEN="$TOKEN" DB="$DB" PORT="$PORT" HERKUNFT="http://localhost:$WEB" \
  FESTE="marlene-anton=2027-06-13" node "$HIER/server.mjs" >"$TMP/dienst.log" 2>&1 &
DIENST=$!
(cd "$THEME" && python3 -m http.server "$WEB" >/dev/null 2>&1) &
SEITE=$!
for _ in $(seq 40); do curl -sf "http://127.0.0.1:$PORT/gesundheit" >/dev/null && break; sleep 0.1; done
for _ in $(seq 40); do curl -sf "http://localhost:$WEB/" >/dev/null && break; sleep 0.1; done

GUT=0; SCHLECHT=0
pruef() {
  if [ "$2" = "$3" ]; then GUT=$((GUT+1)); printf '  ok    %s\n' "$1"
  else SCHLECHT=$((SCHLECHT+1)); printf '  FEHLT %s — erwartet %s, bekommen %s\n' "$1" "$2" "$3"; fi
}

echo "— Ein Gast antwortet —"
ERGEBNIS="$(WEB="$WEB" python3 "$HIER/browser.py" senden 2>&1)"
echo "$ERGEBNIS" | sed 's/^/    /'
pruef "Quittung erscheint" 1 "$(grep -c 'quittung=danke' <<<"$ERGEBNIS")"
pruef "keine Fehlermeldung" 1 "$(grep -c 'fehlerklasse=nein' <<<"$ERGEBNIS")"
pruef "Datenschutzhinweis am Formular" 1 "$(grep -c 'hinweis=ja' <<<"$ERGEBNIS")"

LISTE="$(curl -s -H "authorization: Bearer $TOKEN" "http://127.0.0.1:$PORT/liste?kennung=marlene-anton")"
pruef "Antwort ist in der Datenbank" 1 "$(node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>console.log(JSON.parse(s).antworten.length))' <<<"$LISTE")"
pruef "Name kam richtig an" "Theresa Baumgartner" "$(node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>console.log(JSON.parse(s).antworten[0].name))' <<<"$LISTE")"
pruef "Personenzahl kam an" 3 "$(node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>console.log(JSON.parse(s).summe.koepfe))' <<<"$LISTE")"

echo "— Der Dienst ist weg —"
kill "$DIENST" 2>/dev/null; wait "$DIENST" 2>/dev/null; DIENST=""
AUS="$(WEB="$WEB" python3 "$HIER/browser.py" fehler 2>&1)"
echo "$AUS" | sed 's/^/    /'
pruef "Fehler wird gemeldet"      1 "$(grep -c 'fehlerklasse=ja' <<<"$AUS")"
pruef "Knopf kommt zurück"        1 "$(grep -c 'knopf=bereit' <<<"$AUS")"
pruef "Eingaben bleiben stehen"   1 "$(grep -c 'name=erhalten' <<<"$AUS")"

echo
echo "$GUT bestanden, $SCHLECHT fehlgeschlagen"
exit $SCHLECHT
