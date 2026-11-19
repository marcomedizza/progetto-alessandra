const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ args: ['--use-gl=swiftshader','--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 1300, height: 760 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  await p.goto('http://127.0.0.1:8765/'); await p.waitForTimeout(1200);
  await p.selectOption('#sel-caso', 'C1_trave_appoggiata'); await p.waitForTimeout(700);
  const box = await p.locator('#vista canvas').boundingBox();
  const a = box.width / box.height, m = 6 * 0.85;
  const px = box.x + box.width / 2 + (0 - 3) / (m * a) * (box.width / 2), py = box.y + box.height / 2;
  await p.mouse.click(px, py); await p.waitForTimeout(300);
  const t = await p.textContent('#pannello-proprieta');
  console.log('nodo selezionato:', t.slice(0, 50));
  await p.uncheck('[data-vincolo=ux]'); await p.waitForTimeout(200);
  await p.click('#btn-calcola'); await p.waitForTimeout(800);
  console.log('S10:', await p.textContent('#stato'), errs);
  await b.close();
})();
