// Renders endcard_overlay.png (transparent, for compositing over live footage)
// and endcard_full.png (cream background preview). Run: node render.js
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  const src = fs.readFileSync(__dirname + '/endcard.html', 'utf8');
  for (const m of ['overlay', 'full']) {
    const tmp = __dirname + '/_tmp.html';
    fs.writeFileSync(tmp, src.replace('__MODE__', m));
    await p.goto('file://' + tmp);
    await p.waitForTimeout(400);
    await p.screenshot({ path: __dirname + '/endcard_' + m + '.png', omitBackground: m === 'overlay' });
    fs.unlinkSync(tmp);
  }
  await b.close();
})();
