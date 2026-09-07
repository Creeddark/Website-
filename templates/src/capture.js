/*
 * Nimmt eine Szene Bild fuer Bild auf.
 *
 * Die Seite bringt ihre eigene Funktion seek(t) mit, die den Zustand zum
 * Zeitpunkt t setzt. Statt eine Bildschirmaufnahme zu machen, rufen wir sie
 * fuer jedes Einzelbild auf und schiessen ein Foto. Ergebnis: gleichmaessige
 * Bildabstaende und ein Ergebnis, das bei jedem Lauf identisch ist.
 *
 *   node capture.js <datei.html> <ziel-ordner> <breite> <hoehe> [scale] [fps]
 *   node capture.js <datei.html> <ziel.png> <breite> <hoehe> <scale> peek t1,t2,..
 */
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const a = process.argv.slice(2);
  const [htmlFile, outDir, wArg, hArg] = a;
  const w = Number(wArg), h = Number(hArg);
  const scale = Number(a[4] || 1);
  const peek = a[5] === 'peek' ? a[6].split(',').map(Number) : null;
  const fps = Number(a[5] === 'peek' ? 30 : (a[5] || 30));

  const browser = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--no-sandbox', '--font-render-hinting=none', '--disable-lcd-text'],
  });
  const ctx = await browser.newContext({
    viewport: { width: w, height: h }, deviceScaleFactor: scale,
  });
  const page = await ctx.newPage();
  await page.goto('file://' + path.resolve(htmlFile), { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(500);
  const stage = await page.$('#stage');

  if (peek) {
    // Kontaktabzug: mehrere Zeitpunkte nebeneinander, um die Szene zu pruefen
    fs.mkdirSync(path.dirname(outDir), { recursive: true });
    const shots = [];
    for (const t of peek) {
      await page.evaluate((tt) => window.seek(tt), t);
      await page.waitForTimeout(30);
      shots.push((await stage.screenshot()).toString('base64'));
    }
    const cols = Math.min(3, shots.length);
    const sheet = await ctx.newPage();
    await sheet.setViewportSize({ width: cols * 420 + (cols + 1) * 12, height: 100 });
    await sheet.setContent(`<style>*{margin:0}body{background:#222;display:grid;
      grid-template-columns:repeat(${cols},420px);gap:12px;padding:12px}
      figure{margin:0}img{width:420px;display:block}
      figcaption{color:#bbb;font:11px monospace;padding:3px 0}</style>` +
      shots.map((s, i) => `<figure><img src="data:image/png;base64,${s}">
        <figcaption>t = ${peek[i]}s</figcaption></figure>`).join(''));
    await sheet.waitForTimeout(300);
    await sheet.screenshot({ path: outDir, fullPage: true });
    await browser.close();
    console.log('wrote ' + outDir);
    return;
  }

  fs.mkdirSync(outDir, { recursive: true });
  const dur = await page.evaluate(() => window.__duration);
  const total = Math.round(dur * fps);
  for (let i = 0; i < total; i++) {
    await page.evaluate((tt) => window.seek(tt), i / fps);
    await stage.screenshot({
      path: path.join(outDir, `f${String(i).padStart(5, '0')}.png`),
    });
    if (i % 60 === 0) process.stderr.write(`  ${i}/${total}\r`);
  }
  await browser.close();
  console.log(`${total} frames @ ${fps}fps  (${dur}s)`);
})();
