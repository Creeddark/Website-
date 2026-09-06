/*
 * Rendert jede .page eines Vorlagen-HTML als eigenes PNG.
 *
 * deviceScaleFactor 2 macht aus 750 x 1050 CSS-Pixeln 1500 x 2100 Bildpunkte —
 * das sind echte 300 DPI auf 5 x 7 Zoll, also Druckaufloesung.
 *
 *   node render.js <datei.html> <ziel-ordner> [scale]
 */
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path');
const fs = require('fs');

(async () => {
  const [, , htmlFile, outDir, scaleArg] = process.argv;
  if (!htmlFile || !outDir) {
    console.error('usage: node render.js <datei.html> <ziel-ordner> [scale]');
    process.exit(1);
  }
  const scale = Number(scaleArg || 2);
  fs.mkdirSync(outDir, { recursive: true });

  const browser = await chromium.launch({
    executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
    args: ['--no-sandbox', '--font-render-hinting=none', '--disable-lcd-text'],
  });
  const ctx = await browser.newContext({ deviceScaleFactor: scale });
  const page = await ctx.newPage();
  await page.goto('file://' + path.resolve(htmlFile), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(400);

  const base = path.basename(htmlFile, '.html');
  const pages = await page.$$('.page');
  const written = [];
  for (let i = 0; i < pages.length; i++) {
    const label = await pages[i].getAttribute('data-label');
    const slug = (label || `page-${i + 1}`).toLowerCase()
      .replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
    const file = path.join(outDir, `${base}-${i + 1}-${slug}.png`);
    await pages[i].screenshot({ path: file });
    written.push(file);
  }
  await browser.close();
  console.log(written.join('\n'));
})();
