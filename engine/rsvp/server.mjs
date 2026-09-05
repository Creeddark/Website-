/* =========================================================================
   RSVP — der Dienst hinter dem Formular.

   Nimmt Rückmeldungen entgegen, legt sie in eine SQLite-Datei und gibt sie
   dem Paar als CSV zurück. Mehr nicht, und das ist Absicht.

   Keine Abhängigkeiten. Node 22 bringt HTTP und SQLite mit, und was nicht
   installiert wird, kann auch nicht veralten. Läuft auf jedem Server in der
   EU, auf dem Node liegt — kein Anbieter, an dem man später hängt.

   Start:
       TOKEN=… HERKUNFT=https://paar.example node server.mjs

   Alle Schalter über Umgebungsvariablen, siehe README.md.

   Hier werden Daten von Menschen verarbeitet, die nie einen Vertrag mit uns
   geschlossen haben: den Gästen. Deshalb steht in diesem Dienst nichts, was
   nicht gebraucht wird — keine IP-Adressen in der Datenbank, keine Zugriffs-
   protokolle mit Inhalten, und eine Löschfrist, die von selbst greift.
   ========================================================================= */

import { createServer } from "node:http";
import { DatabaseSync } from "node:sqlite";
import { createHash, timingSafeEqual } from "node:crypto";

/* ------------------------------------------------------------ Einstellung -- */

const CFG = {
  port: Number(process.env.PORT || 8787),
  datei: process.env.DB || "./rsvp.sqlite",
  token: process.env.TOKEN || "",
  // Wer darf das Formular abschicken. Leer heisst: niemand von aussen —
  // ein offener Endpunkt waere eine Einladung an jeden Spam-Roboter.
  herkunft: (process.env.HERKUNFT || "").split(",").map(s => s.trim()).filter(Boolean),
  // Tage nach dem Fest, nach denen die Antworten von selbst verschwinden.
  frist_tage: Number(process.env.FRIST_TAGE || 28),
  // Ab wann eine Einladung als vorbei gilt: kennung=YYYY-MM-DD, mehrfach.
  feste: Object.fromEntries((process.env.FESTE || "").split(",")
    .map(s => s.split("=").map(t => t.trim())).filter(p => p.length === 2)),
  max_body: 16 * 1024,
  limit_anzahl: 12,          // Anfragen
  limit_fenster: 10 * 60_000, // je zehn Minuten und Adresse
};

if (!CFG.token || CFG.token.length < 24) {
  console.error("TOKEN fehlt oder ist zu kurz (mindestens 24 Zeichen).");
  process.exit(1);
}

/* --------------------------------------------------------------- Ablage -- */

const db = new DatabaseSync(CFG.datei);
db.exec(`
  PRAGMA journal_mode = WAL;
  CREATE TABLE IF NOT EXISTS antwort (
    id       INTEGER PRIMARY KEY,
    kennung  TEXT NOT NULL,
    name     TEXT NOT NULL,
    mail     TEXT NOT NULL,
    zusage   TEXT NOT NULL CHECK (zusage IN ('ja','nein')),
    anzahl   INTEGER NOT NULL DEFAULT 1,
    essen    TEXT NOT NULL DEFAULT 'alles',
    gruss    TEXT NOT NULL DEFAULT '',
    erstellt TEXT NOT NULL,
    geaendert TEXT NOT NULL,
    UNIQUE (kennung, mail)
  );
  CREATE INDEX IF NOT EXISTS idx_kennung ON antwort (kennung);
`);

/* Dieselbe Person antwortet zweimal — weil sie sich vertippt hat, weil sie
   umdisponiert, weil sie den Link nochmal oeffnet. Dann wird die Antwort
   ersetzt und nicht verdoppelt. Alles andere gibt eine Gaesteliste, in der
   dieselben Leute dreimal stehen. */
const einfuegen = db.prepare(`
  INSERT INTO antwort (kennung,name,mail,zusage,anzahl,essen,gruss,erstellt,geaendert)
  VALUES (?,?,?,?,?,?,?,?,?)
  ON CONFLICT (kennung, mail) DO UPDATE SET
    name=excluded.name, zusage=excluded.zusage, anzahl=excluded.anzahl,
    essen=excluded.essen, gruss=excluded.gruss, geaendert=excluded.geaendert
`);
const lesen = db.prepare(
  "SELECT name,mail,zusage,anzahl,essen,gruss,erstellt,geaendert " +
  "FROM antwort WHERE kennung=? ORDER BY erstellt");
const zaehlen = db.prepare(
  "SELECT zusage, COUNT(*) n, COALESCE(SUM(anzahl),0) koepfe " +
  "FROM antwort WHERE kennung=? GROUP BY zusage");
const loeschen = db.prepare("DELETE FROM antwort WHERE kennung=?");

/* --------------------------------------------------------------- Pruefen -- */

const MAIL = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;
const KENNUNG = /^[a-z0-9][a-z0-9-]{0,63}$/;
const ESSEN = new Set(["alles", "vegetarisch", "vegan"]);

function text(wert, max) {
  if (typeof wert !== "string") return null;
  // Steuerzeichen raus, Rest beschneiden. Ein Zeilenumbruch im Namen ist
  // kein Angriff, aber er zerlegt spaeter die CSV-Zeile.
  const t = wert.replace(/[\u0000-\u001F\u007F]/g, " ").trim();
  return t.length === 0 || t.length > max ? null : t;
}

function pruefen(k) {
  const fehler = [];
  const kennung = text(k.kennung, 64);
  if (!kennung || !KENNUNG.test(kennung)) fehler.push("kennung");

  const name = text(k.name, 120);
  if (!name) fehler.push("name");

  const mail = text(k.mail, 190);
  if (!mail || !MAIL.test(mail)) fehler.push("mail");

  const zusage = k.zusage === "ja" || k.zusage === "nein" ? k.zusage : null;
  if (!zusage) fehler.push("zusage");

  let anzahl = Number.parseInt(k.anzahl ?? 1, 10);
  if (!Number.isFinite(anzahl) || anzahl < 1 || anzahl > 12) anzahl = 1;
  if (zusage === "nein") anzahl = 0;

  // Wer absagt, sitzt an keinem Tisch. Sonst stuende in der Liste des Paares
  // neben jeder Absage eine Essenswahl, die niemand getroffen hat.
  let essen = ESSEN.has(k.essen) ? k.essen : "alles";
  if (zusage === "nein") essen = "";
  const gruss = typeof k.gruss === "string"
    ? k.gruss.replace(/[\u0000-\u0009\u000B\u000C\u000E-\u001F\u007F]/g, " ")
        .trim().slice(0, 1000)
    : "";

  return { fehler, satz: { kennung, name, mail: mail?.toLowerCase(), zusage, anzahl, essen, gruss } };
}

/* Zwei stille Bremsen gegen Roboter. Beide kosten einen Menschen nichts:
   ein Feld, das niemand sieht und darum leer bleibt, und die Zeit zwischen
   dem Anzeigen des Formulars und dem Absenden. Kein Bilderraetsel, kein
   fremdes Skript, keine Daten an Dritte. */
function roboter(k) {
  if (typeof k.hp === "string" && k.hp.length > 0) return true;
  const dauer = Number(k.dauer);
  return Number.isFinite(dauer) && dauer >= 0 && dauer < 1500;
}

/* ---------------------------------------------------------- Ratenbremse -- */

const spuren = new Map();     // Adresse -> Zeitstempel der letzten Anfragen
function zu_oft(adresse) {
  const jetzt = Date.now();
  const liste = (spuren.get(adresse) || []).filter(t => jetzt - t < CFG.limit_fenster);
  liste.push(jetzt);
  spuren.set(adresse, liste);
  return liste.length > CFG.limit_anzahl;
}
// Die Karte darf nicht unbegrenzt wachsen.
setInterval(() => {
  const jetzt = Date.now();
  for (const [k, v] of spuren) {
    if (v.every(t => jetzt - t >= CFG.limit_fenster)) spuren.delete(k);
  }
}, CFG.limit_fenster).unref();

/* ------------------------------------------------------------ Loeschfrist -- */

/* Die Frist greift von selbst. Ein Loeschversprechen, das jemand von Hand
   einhalten muss, wird irgendwann nicht eingehalten. */
function aufraeumen() {
  const heute = new Date();
  for (const [kennung, tag] of Object.entries(CFG.feste)) {
    const ende = new Date(tag + "T00:00:00Z");
    if (Number.isNaN(ende.getTime())) continue;
    ende.setUTCDate(ende.getUTCDate() + CFG.frist_tage);
    if (heute > ende) {
      const weg = loeschen.run(kennung);
      if (weg.changes) console.log(`[frist] ${kennung}: ${weg.changes} Antworten gelöscht`);
    }
  }
}
aufraeumen();
setInterval(aufraeumen, 6 * 60 * 60_000).unref();

/* ---------------------------------------------------------------- Token -- */

function token_stimmt(gegeben) {
  if (typeof gegeben !== "string" || !gegeben) return false;
  // Ueber den Hash vergleichen: dann sind beide Seiten gleich lang und die
  // Dauer des Vergleichs verraet nichts ueber die Laenge des Tokens.
  const a = createHash("sha256").update(gegeben).digest();
  const b = createHash("sha256").update(CFG.token).digest();
  return timingSafeEqual(a, b);
}

/* ------------------------------------------------------------ Uebersicht -- */

/* Eine Seite fuer das Paar. Ohne sie muesste jemand curl bedienen, um seine
   eigene Gaesteliste zu sehen — das ist kein Produkt.

   Das Token wird nur im Speicher des Reiters gehalten und wandert nie in die
   Adresszeile: Adressen landen in Verlaeufen, Lesezeichen und Protokollen. */
const UEBERSICHT = `<!doctype html>
<html lang="de"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>Rückmeldungen</title>
<style>
  :root { color-scheme: light }
  /* form.tor traegt display:grid und wuerde das UA-Stylesheet ueberstimmen —
     ohne diese Zeile bleibt das Token-Feld nach dem Anmelden stehen. */
  [hidden] { display: none !important }
  body { margin:0; background:#FBF6EE; color:#241F18;
         font:400 16px/1.6 "Helvetica Neue",Arial,sans-serif }
  main { width:min(100% - 2.5rem, 54rem); margin-inline:auto; padding-block:3rem }
  h1 { font-weight:400; font-size:1.75rem; margin:0 0 .25rem }
  p.k { color:#565042; margin:0 0 2rem; font-size:.9375rem }
  form.tor { display:grid; gap:.75rem; max-width:22rem }
  label { font-size:.75rem; letter-spacing:.14em; text-transform:uppercase; color:#565042 }
  input { font:inherit; padding:.625rem .75rem; border:1px solid #E2D7C4;
          border-radius:3px; background:#fff; min-height:2.75rem }
  button { font:500 .8125rem/1 inherit; letter-spacing:.12em; text-transform:uppercase;
           padding:.9rem 1.25rem; border:1px solid #82632E; border-radius:999px;
           background:#82632E; color:#FBF6EE; cursor:pointer }
  button.leer { background:transparent; color:#82632E }
  .zahlen { display:flex; gap:2.5rem; margin:0 0 1.75rem; flex-wrap:wrap }
  .zahlen div { display:grid }
  .zahlen b { font-size:2rem; font-weight:400 }
  .zahlen span { font-size:.6875rem; letter-spacing:.2em; text-transform:uppercase; color:#565042 }
  table { border-collapse:collapse; width:100%; font-size:.9375rem }
  th,td { text-align:left; padding:.625rem .5rem; border-bottom:1px solid #E2D7C4;
          vertical-align:top }
  th { font-size:.6875rem; letter-spacing:.14em; text-transform:uppercase; color:#565042;
       font-weight:500 }
  td.nein { color:#8A8172 }
  .werkzeug { display:flex; gap:.625rem; margin-top:1.75rem; flex-wrap:wrap }
  .warn { color:#8C3A22 }
  @media (max-width:34rem){ td.g,th.g { display:none } }
</style></head><body><main>
<h1>Rückmeldungen</h1>
<p class="k" id="wer"></p>
<form class="tor" id="tor">
  <label for="t">Zugangstoken</label>
  <input id="t" type="password" autocomplete="current-password" required>
  <button type="submit">Anzeigen</button>
  <p class="warn" id="fehler" hidden></p>
</form>
<div id="inhalt" hidden></div>
</main><script>
(function(){
  var p = new URLSearchParams(location.search), kennung = p.get("kennung") || "";
  document.getElementById("wer").textContent = kennung;
  var tor = document.getElementById("tor"), fehler = document.getElementById("fehler");
  var inhalt = document.getElementById("inhalt");

  function hole(token){
    return fetch("liste?kennung=" + encodeURIComponent(kennung),
                 { headers: { authorization: "Bearer " + token } })
      .then(function(a){ if(!a.ok) throw new Error(a.status); return a.json(); });
  }
  function zeichne(d, token){
    tor.hidden = true; inhalt.hidden = false;
    var s = d.summe || {};
    var zeilen = (d.antworten || []).map(function(a){
      return "<tr><td>" + esc(a.name) + "</td><td>" + esc(a.mail) + "</td>" +
        "<td class='" + (a.zusage === "ja" ? "" : "nein") + "'>" +
        (a.zusage === "ja" ? "Ja" : "Nein") + "</td>" +
        "<td>" + (a.zusage === "ja" ? a.anzahl : "—") + "</td>" +
        "<td class='g'>" + (a.essen ? esc(a.essen) : "—") + "</td>" +
        "<td class='g'>" + esc(a.gruss) + "</td></tr>";
    }).join("");
    inhalt.innerHTML =
      '<div class="zahlen"><div><b>' + (s.koepfe||0) + '</b><span>Personen</span></div>' +
      '<div><b>' + (s.ja||0) + '</b><span>Zusagen</span></div>' +
      '<div><b>' + (s.nein||0) + '</b><span>Absagen</span></div></div>' +
      (zeilen ? '<table><thead><tr><th>Name</th><th>E-Mail</th><th>Zusage</th>' +
        '<th>Personen</th><th class="g">Am Tisch</th><th class="g">Nachricht</th></tr></thead>' +
        '<tbody>' + zeilen + '</tbody></table>'
        : '<p class="k">Noch keine Rückmeldung.</p>') +
      '<div class="werkzeug"><button class="leer" id="csv">Als CSV laden</button></div>';
    var csv = document.getElementById("csv");
    if (csv) csv.addEventListener("click", function(){
      fetch("export?kennung=" + encodeURIComponent(kennung),
            { headers: { authorization: "Bearer " + token } })
        .then(function(a){ return a.blob(); })
        .then(function(b){
          var u = URL.createObjectURL(b), a = document.createElement("a");
          a.href = u; a.download = "rsvp-" + kennung + ".csv";
          document.body.appendChild(a); a.click(); a.remove();
          setTimeout(function(){ URL.revokeObjectURL(u); }, 1000);
        });
    });
  }
  function esc(t){ var d = document.createElement("span"); d.textContent = t == null ? "" : t; return d.innerHTML; }

  tor.addEventListener("submit", function(e){
    e.preventDefault();
    fehler.hidden = true;
    var token = document.getElementById("t").value;
    hole(token).then(function(d){
      try { sessionStorage.setItem("rsvp-token", token); } catch(_){}
      zeichne(d, token);
    }).catch(function(){
      fehler.textContent = "Das Token stimmt nicht.";
      fehler.hidden = false;
    });
  });

  // Beim Neuladen nicht noch einmal fragen — aber nur fuer diesen Reiter.
  var gemerkt = null;
  try { gemerkt = sessionStorage.getItem("rsvp-token"); } catch(_){}
  if (gemerkt) hole(gemerkt).then(function(d){ zeichne(d, gemerkt); }).catch(function(){});
})();
</script></body></html>`;

/* ----------------------------------------------------------------- HTTP -- */

function kopf(res, herkunft, extra = {}) {
  const h = {
    "Cache-Control": "no-store",
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "no-referrer",
    ...extra,
  };
  if (herkunft) {
    h["Access-Control-Allow-Origin"] = herkunft;
    h["Vary"] = "Origin";
    h["Access-Control-Allow-Headers"] = "content-type";
    h["Access-Control-Allow-Methods"] = "POST, OPTIONS";
    h["Access-Control-Max-Age"] = "86400";
  }
  for (const [k, v] of Object.entries(h)) res.setHeader(k, v);
}

function json(res, code, koerper, herkunft) {
  kopf(res, herkunft, { "Content-Type": "application/json; charset=utf-8" });
  res.writeHead(code).end(JSON.stringify(koerper));
}

function koerper_lesen(req) {
  return new Promise((fertig, fehler) => {
    let laenge = 0;
    const teile = [];
    req.on("data", d => {
      laenge += d.length;
      if (laenge > CFG.max_body) { fehler(new Error("zu gross")); req.destroy(); return; }
      teile.push(d);
    });
    req.on("end", () => fertig(Buffer.concat(teile).toString("utf8")));
    req.on("error", fehler);
  });
}

function csv(zeilen) {
  const feld = w => `"${String(w ?? "").replace(/"/g, '""')}"`;
  const kopfzeile = ["Name", "E-Mail", "Zusage", "Personen", "Am Tisch",
                     "Nachricht", "Eingegangen", "Geaendert"];
  const inhalt = zeilen.map(z => [z.name, z.mail, z.zusage === "ja" ? "Ja" : "Nein",
    z.anzahl, z.essen, z.gruss, z.erstellt, z.geaendert].map(feld).join(";"));
  // Mit BOM, sonst zeigt Excel die Umlaute falsch an. Das ist kein
  // Schoenheitsfehler: die Gaesteliste wird in Excel geoeffnet.
  return "\uFEFF" + [kopfzeile.map(feld).join(";"), ...inhalt].join("\r\n") + "\r\n";
}

const server = createServer(async (req, res) => {
  const url = new URL(req.url, "http://x");
  const pfad = url.pathname.replace(/\/+$/, "") || "/";
  const von = req.headers.origin;
  const erlaubt = von && CFG.herkunft.includes(von) ? von : null;

  if (pfad === "/gesundheit") return json(res, 200, { ok: true }, null);

  if (pfad === "/uebersicht" && req.method === "GET") {
    // Die Seite selbst ist oeffentlich, die Daten dahinter nicht: ohne
    // Token zeigt sie nur ein Eingabefeld.
    kopf(res, null, { "Content-Type": "text/html; charset=utf-8" });
    return res.writeHead(200).end(UEBERSICHT);
  }

  /* ---- Absenden ---- */
  if (pfad === "/rsvp" && req.method === "OPTIONS") {
    kopf(res, erlaubt);
    return res.writeHead(erlaubt ? 204 : 403).end();
  }

  if (pfad === "/rsvp" && req.method === "POST") {
    if (!erlaubt) return json(res, 403, { fehler: "herkunft" }, null);

    const adresse = (req.headers["x-forwarded-for"] || "").split(",")[0].trim()
      || req.socket.remoteAddress || "?";
    if (zu_oft(adresse)) return json(res, 429, { fehler: "zu_oft" }, erlaubt);

    let k;
    try { k = JSON.parse(await koerper_lesen(req)); }
    catch { return json(res, 400, { fehler: "unlesbar" }, erlaubt); }
    if (!k || typeof k !== "object") return json(res, 400, { fehler: "unlesbar" }, erlaubt);

    // Roboter bekommen dieselbe Antwort wie ein Mensch. Wer erfaehrt, dass
    // er erkannt wurde, probiert es anders herum nochmal.
    if (roboter(k)) return json(res, 200, { ok: true }, erlaubt);

    const { fehler, satz } = pruefen(k);
    if (fehler.length) return json(res, 422, { fehler: "ungueltig", felder: fehler }, erlaubt);

    const jetzt = new Date().toISOString();
    try {
      einfuegen.run(satz.kennung, satz.name, satz.mail, satz.zusage,
                    satz.anzahl, satz.essen, satz.gruss, jetzt, jetzt);
    } catch (e) {
      console.error("[db]", e.message);
      return json(res, 500, { fehler: "ablage" }, erlaubt);
    }
    console.log(`[rsvp] ${satz.kennung} ${satz.zusage} (${satz.anzahl})`);
    return json(res, 200, { ok: true }, erlaubt);
  }

  /* ---- Auswertung fuer das Paar. Token im Header, nicht in der Adresse:
          Adressen landen in Verlaeufen und Serverprotokollen. ---- */
  const gegeben = (req.headers.authorization || "").replace(/^Bearer\s+/i, "");
  const kennung = url.searchParams.get("kennung") || "";

  if ((pfad === "/liste" || pfad === "/export") && req.method === "GET") {
    if (!token_stimmt(gegeben)) return json(res, 401, { fehler: "token" }, null);
    if (!KENNUNG.test(kennung)) return json(res, 400, { fehler: "kennung" }, null);

    const zeilen = lesen.all(kennung);
    if (pfad === "/liste") {
      const summe = { ja: 0, nein: 0, koepfe: 0 };
      for (const z of zaehlen.all(kennung)) {
        summe[z.zusage] = z.n;
        if (z.zusage === "ja") summe.koepfe = z.koepfe;
      }
      return json(res, 200, { kennung, summe, antworten: zeilen }, null);
    }
    kopf(res, null, {
      "Content-Type": "text/csv; charset=utf-8",
      "Content-Disposition": `attachment; filename="rsvp-${kennung}.csv"`,
    });
    return res.writeHead(200).end(csv(zeilen));
  }

  if (pfad === "/rsvp" && req.method === "DELETE") {
    if (!token_stimmt(gegeben)) return json(res, 401, { fehler: "token" }, null);
    if (!KENNUNG.test(kennung)) return json(res, 400, { fehler: "kennung" }, null);
    const weg = loeschen.run(kennung);
    console.log(`[loeschen] ${kennung}: ${weg.changes}`);
    return json(res, 200, { ok: true, geloescht: weg.changes }, null);
  }

  json(res, 404, { fehler: "unbekannt" }, null);
});

server.listen(CFG.port, () => {
  console.log(`RSVP hört auf ${CFG.port}`);
  console.log(`  Ablage:      ${CFG.datei}`);
  console.log(`  Herkunft:    ${CFG.herkunft.join(", ") || "(keine — Absenden ist gesperrt)"}`);
  console.log(`  Löschfrist:  ${CFG.frist_tage} Tage nach dem Fest`);
  console.log(`  Feste:       ${Object.keys(CFG.feste).join(", ") || "(keine eingetragen)"}`);
});

for (const zeichen of ["SIGINT", "SIGTERM"]) {
  process.on(zeichen, () => {
    server.close(() => { db.close(); process.exit(0); });
  });
}
