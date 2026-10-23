// uso: node frames.js eventos.json saida/ [t1,t2,...] | --range ini fim fps
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const [evFile, outDir, ...rest] = process.argv.slice(2);
  fs.mkdirSync(outDir, { recursive: true });
  const events = JSON.parse(fs.readFileSync(evFile, 'utf8'));
  let times;
  if (rest[0] === '--range') {
    const [a, b, fps] = rest.slice(1).map(Number);
    times = []; for (let f = Math.round(a * fps); f < Math.round(b * fps); f++) times.push(f / fps);
  } else times = rest[0].split(',').map(Number);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto('file://' + path.resolve(__dirname, 'overlay.html'));
  await page.evaluate(ev => window.build(ev), events);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);
  for (let i = 0; i < times.length; i++) {
    await page.evaluate(t => window.render(t), times[i]);
    await page.screenshot({ path: path.join(outDir, `f${String(i).padStart(6, '0')}.png`), omitBackground: true });
  }
  await browser.close();
})();
