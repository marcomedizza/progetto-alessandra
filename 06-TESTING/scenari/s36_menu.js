const { chromium } = require('playwright');
(async () => {
  const OUT = process.argv[2];
  const b = await chromium.launch({ args: ['--use-gl=swiftshader','--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 1300, height: 760 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('http://127.0.0.1:8765/'); await p.waitForTimeout(1200);
  const testo = () => p.$eval('#sel-caso', (s) => s.options[s.selectedIndex].text);
  const e = {};
  e.iniziale = await testo();
  await p.setInputFiles('#file-modello', OUT + '/c1_avviso.json'); await p.waitForTimeout(800);
  e.dopo_file = await testo(); e.stato_file = await p.textContent('#stato');
  await p.click('#btn-nuovo'); await p.waitForTimeout(500);
  e.dopo_nuovo = await testo(); e.voci_locali = await p.$$eval('#sel-caso option[value="__locale"]', (o) => o.length);
  await p.selectOption('#sel-caso', 'C2_mensola'); await p.waitForTimeout(800);
  e.dopo_scelta = await testo(); e.stato_scelta = await p.textContent('#stato');
  e.errori = errs; console.log(JSON.stringify(e, null, 1)); await b.close();
})();
