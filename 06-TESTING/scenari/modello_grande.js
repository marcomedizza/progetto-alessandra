const { chromium } = require('playwright');
(async () => {
  const OUT = process.argv[2];
  const b = await chromium.launch({ args: ['--use-gl=swiftshader','--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 1300, height: 820 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  const w = (ms) => p.waitForTimeout(ms); const st = () => p.textContent('#stato');
  await p.goto('http://127.0.0.1:8765/'); await w(1200);
  // C20: leggibilità
  await p.selectOption('#sel-caso', 'C20_gerber_trapezio'); await w(700); await p.click('#btn-calcola'); await w(900);
  console.log('C20', await p.$$eval('.etichetta', (l) => l.map((x) => x.textContent)), (await p.textContent('#pannello-risultati')).match(/Spostamento massimo[^(]*/)?.[0]);
  await p.locator('#vista').screenshot({ path: OUT + '/c20.png' });
  // modello grande
  let t = Date.now();
  await p.setInputFiles('#file-modello', OUT + '/grande.json');
  await p.waitForFunction(() => document.querySelector('#stato').textContent.includes('4681 nodi'), null, { timeout: 120000 });
  console.log('caricamento e disegno', (Date.now() - t) / 1000, 's |', await st());
  t = Date.now();
  await p.click('#btn-calcola');
  await p.waitForFunction(() => /Calcolo completato|Errore/.test(document.querySelector('#stato').textContent), null, { timeout: 180000 });
  console.log('calcolo e disegno dei risultati', (Date.now() - t) / 1000, 's |', await st());
  // Annulla dopo una modifica (aggiunta di un nodo dal pannello)
  await p.fill('#m-x', '500'); await p.fill('#m-y', '0'); t = Date.now(); await p.click('#m-add-nodo');
  await p.waitForFunction(() => document.querySelector('#stato').textContent.includes('Aggiunto il nodo'), null, { timeout: 120000 });
  console.log('modifica', (Date.now() - t) / 1000, 's');
  t = Date.now(); await p.click('#btn-annulla');
  await p.waitForFunction(() => document.querySelector('#stato').textContent.includes('annullata'), null, { timeout: 120000 });
  console.log('annulla', (Date.now() - t) / 1000, 's |', await st());
  const mem = await p.evaluate(() => performance.memory ? Math.round(performance.memory.usedJSHeapSize / 1e6) : null);
  console.log('memoria JavaScript', mem, 'MB');
  await p.locator('#vista').screenshot({ path: OUT + '/grande.png' });
  console.log('errori', errs);
  await b.close();
})();
