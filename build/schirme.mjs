/* Erzeugt die Telefon-Aufnahmen fuer die Startseite aus der echten
   Live-Demo. Kein Nachbau: was hier herauskommt, ist genau das, was ein
   Gast sieht.

   Bewusst NICHT Teil von build.py — das Bauen der Seite bleibt ohne
   Abhaengigkeiten. Dieses Skript braucht Playwright und wird von Hand
   ausgefuehrt, wenn sich die Demo geaendert hat:

       node build/schirme.mjs        # schreibt PNG nach /tmp/velora/schirme
       python3 build/schirme.py      # skaliert, fuellt auf, schreibt WebP

   Die Aufnahmen haben das Seitenverhaeltnis des Telefons auf der
   Startseite (270x592). Geschnitten wird nie mitten im Satz: der Schnitt
   endet auf der Unterkante des letzten Elements, das noch ganz passt. */

import { chromium } from "playwright";
const AUS = "/tmp/velora/schirme/";
// Das Telefon auf der Startseite ist 270x592 gross. Wir nehmen bei 390
// Breite auf, also im selben Seitenverhaeltnis, und skalieren beim
// Einsetzen herunter — so bleibt die Schrift bei doppelter Aufloesung scharf.
const BREIT = 390, HOCH = Math.round(390 * 592 / 270);
// Oben bleibt Platz: im Mockup liegt dort der Lautsprecherbalken, und
// ohne Luft klebt die Ueberschrift am Rand.
const LUFT = 44;

const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: BREIT, height: HOCH }, deviceScaleFactor: 2 });
await p.goto("file:///home/user/Website-/site/demo/gaestemappe.html");
await p.waitForTimeout(700);
// Seitenchrom raus: Demoband, Kopfleiste und Assistent gehoeren nicht
// eingefroren in eine Produktaufnahme.
await p.addStyleTag({ content: `
  .demobar, .site-header, .skip-link, #eli, .eli, [data-eli] { display: none !important; }
  [data-reveal] { opacity: 1 !important; transform: none !important; }
  * { scroll-behavior: auto !important; }
` });
await p.waitForTimeout(300);

// Schneidet ab der Oberkante von "sel" und endet auf der Unterkante des
// letzten Elements, das noch ganz hineinpasst — nie mitten im Satz.
const schuss = async (name, sel, wurzelSel) => {
  const el = p.locator(sel).first();
  await el.evaluate(e => e.scrollIntoView({ block: "start", behavior: "instant" }));
  await p.waitForTimeout(400);
  const plan = await p.evaluate(([s, hoch, w]) => {
    const start = document.querySelector(s);
    const wurzel = document.querySelector(w || s);
    const oben = start.getBoundingClientRect().top;
    const ziel = oben + hoch;
    let schnitt = oben;
    const lauf = (e) => {
      for (const k of e.children) {
        const r = k.getBoundingClientRect();
        if (r.height === 0) continue;
        if (r.bottom <= ziel && r.bottom > schnitt) schnitt = r.bottom;
        if (r.bottom > ziel) lauf(k);
      }
    };
    lauf(wurzel);
    return { oben, hoehe: Math.max(120, Math.round(schnitt - oben)) };
  }, [sel, HOCH - LUFT, wurzelSel]);
  await p.screenshot({ path: AUS + name + ".png",
    clip: { x: 0, y: Math.max(0, plan.oben), width: BREIT, height: Math.min(plan.hoehe, HOCH - LUFT) } });
  console.log(name.padEnd(12), "Höhe", plan.hoehe, "von", HOCH - LUFT);
};

// Der dunkle Auftakt allein liesse 40% tote Flaeche; der Schnitt darf
// deshalb in den folgenden Abschnitt hineinlaufen.
await schuss("willkommen", ".cover", "#main");
for (const t of ["technik", "umgebung", "kontakt"]) {
  await p.click(`[data-guide-tab="${t}"]`);
  await p.waitForTimeout(450);
  await schuss(t, "#p-" + t);
}
await b.close();
