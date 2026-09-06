/*
 * Baut aus mehreren PNGs eine Kontaktbogen-Uebersicht.
 * So laesst sich eine ganze Suite in einem Bild pruefen, statt Seite fuer Seite.
 *
 *   node sheet.js <ziel.png> <spalten> <breite-pro-karte> <bild1> <bild2> ...
 */
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');

(async () => {
  const [, , out, colsArg, cardArg, ...images] = process.argv;
  if (!out || images.length === 0) {
    console.error('usage: node sheet.js <ziel.png> <spalten> <breite> <bilder...>');
    process.exit(1);
  }
  const cols = Number(colsArg || 4);
  const card = Number(cardArg || 360);

  const cells = images.map((img) => {
    const name = path.basename(img).replace(/\.png$/, '');
    return `<figure><img src="file://${path.resolve(img)}"><figcaption>${name}</figcaption></figure>`;
  }).join('');

  const html = `<!doctype html><meta charset="utf-8"><style>
    body{margin:0;background:#3C3A36;padding:22px;
         font:11px/1.4 -apple-system,system-ui,sans-serif;color:#C9C4BA;}
    .grid{display:grid;grid-template-columns:repeat(${cols},${card}px);gap:22px;}
    figure{margin:0;}
    img{width:${card}px;display:block;box-shadow:0 6px 22px rgba(0,0,0,.45);}
    figcaption{padding-top:7px;letter-spacing:.04em;}
  </style><div class="grid">${cells}</div>`;

  const browser = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--no-sandbox'],
  });
  // Ueber eine echte Datei laden statt setContent: eine about:blank-Seite darf
  // keine file://-Bilder nachladen, die Kacheln blieben sonst leer.
  const fs = require('fs');
  const os = require('os');
  const tmp = path.join(fs.mkdtempSync(path.join(os.tmpdir(), 'sheet-')), 'sheet.html');
  fs.writeFileSync(tmp, html);

  const page = await browser.newPage({ deviceScaleFactor: 1 });
  await page.goto('file://' + tmp, { waitUntil: 'networkidle' });
  await page.evaluate(() => Promise.all(
    Array.from(document.images).map((i) => i.complete
      ? null : new Promise((r) => { i.onload = i.onerror = r; }))));
  await page.screenshot({ path: out, fullPage: true });
  await browser.close();
  console.log(out);
})();
