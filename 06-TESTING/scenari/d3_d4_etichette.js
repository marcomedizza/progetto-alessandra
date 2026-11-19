const { chromium } = require('playwright');
(async () => {
  const OUT = process.argv[2];
  const b = await chromium.launch({ args: ['--use-gl=swiftshader','--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 1300, height: 820 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  const w = (ms) => p.waitForTimeout(ms); const st = () => p.textContent('#stato');
  const es = {};
  await p.goto('http://127.0.0.1:8765/'); await w(1200);
  // D3 su C4
  await p.click('#btn-calcola'); await w(800);
  const lab = await p.$$eval('.etichetta', (l) => l.map((x) => x.textContent));
  es.D3_C4 = lab; 
  await p.screenshot({ path: OUT + '/d3.png' });
  // D4: nuovo modello, carico su asta, calcolo
  await p.click('#btn-nuovo'); await w(500);
  const box = await p.locator('#vista canvas').boundingBox();
  await p.mouse.click(box.x + box.width / 2, box.y + box.height / 2); await w(300);
  es.sel = (await p.textContent('#pannello-proprieta')).slice(0, 30);
  await p.fill('#m-q', '-10'); await p.click('#m-add-q'); await w(300);
  await p.click('#btn-calcola'); await w(800);
  es.trave_msg = await st(); es.trave_lab = await p.$$eval('.etichetta', (l) => l.map((x) => x.textContent));
  // aggiunge una mensola verticale: nodo (0,3), asta 1→3
  await p.fill('#m-x', '0'); await p.fill('#m-y', '3'); await p.click('#m-add-nodo'); await w(300);
  await p.selectOption('#m-ni', '1'); await p.selectOption('#m-nj', '3'); await p.selectOption('#m-sez', 'HEA200'); await p.click('#m-add-asta'); await w(300);
  es.dopo_asta = await st();
  await p.click('#btn-calcola'); await w(800);
  es.calc2 = await st(); es.reaz = (await p.textContent('#pannello-risultati')).slice(0, 120);
  await p.screenshot({ path: OUT + '/d4.png' });
  // errore: nodo duplicato
  await p.fill('#m-x', '0'); await p.fill('#m-y', '3'); await p.click('#m-add-nodo'); await w(200);
  es.duplicato = await st();
  // elimina il nodo 3 selezionandolo dal pannello? si seleziona col clic sul nodo (0,3)
  console.log(JSON.stringify(es, null, 1), errs);
  await b.close();
})();
