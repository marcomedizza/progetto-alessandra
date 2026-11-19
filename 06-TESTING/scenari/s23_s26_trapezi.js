const { chromium } = require('playwright');
(async () => {
  const OUT = process.argv[2];
  const b = await chromium.launch({ args: ['--use-gl=swiftshader','--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 1300, height: 820 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  const w = (ms) => p.waitForTimeout(ms); const st = () => p.textContent('#stato'); const rs = () => p.textContent('#pannello-risultati'); const pr = () => p.textContent('#pannello-proprieta');
  const es = {};
  await p.goto('http://127.0.0.1:8765/'); await w(1200);
  const box = await p.locator('#vista canvas').boundingBox();
  const scr = (X, Y, S, cx, cy) => { const a = box.width / box.height, m = 0.85 * S;
    return [box.x + box.width / 2 + (X - cx) / (m * a) * box.width / 2, box.y + box.height / 2 - (Y - cy) / m * box.height / 2]; };
  // S23 — D15 trapezio dal pannello: trave nuova 6 m, da −10 a −20 kN/m su tutta la luce → R1 = 40, R2 = 50
  await p.click('#btn-nuovo'); await w(500);
  await p.mouse.click(...scr(3, 0, 6, 3, 0)); await w(300);
  await p.click('#m-add-trap'); await w(300); es.S23_msg = await st();
  await p.click('#btn-calcola'); await w(900);
  const r23 = await rs(); es.S23 = [await st(), r23.includes('40,00'), r23.includes('50,00')];
  // S26 — D14 spostamento massimo lungo l'asta (la trave ha solo due nodi, entrambi vincolati)
  es.S26 = r23.match(/Spostamento massimo[^.]*/)?.[0];
  // trapezio fuori dall'asta rifiutato
  await p.mouse.click(...scr(3, 0, 6, 3, 0)); await w(300);
  await p.fill('#m-tb', '7'); await p.click('#m-add-trap'); await w(200); es.S23_rifiuto = await st();
  // S25 — D13 Annulla: toglie il trapezio aggiunto, il ricalcolo dà reazioni nulle
  await p.click('#btn-annulla'); await w(300); es.S25_msg = await st();
  await p.click('#btn-calcola'); await w(900);
  es.S25 = (await rs()).includes('40,00') === false;
  await p.click('#btn-annulla'); await w(300); es.S25_vuoto = await st();
  // S24 — D15 cedimento: C1, nodo 3 (appoggio), uy = −10 mm → trave isostatica: reazioni nulle, uy nodo 3 = −10 mm
  await p.selectOption('#sel-caso', 'C1_trave_appoggiata'); await w(700);
  await p.mouse.click(...scr(6, 0, 6, 3, 0)); await w(300);
  es.S24_campi = await p.$$eval('[data-ced]', (l) => l.map((x) => x.dataset.ced));
  await p.fill('[data-ced=uy]', '-10'); await p.click('#m-ced'); await w(300); es.S24_msg = await st();
  await p.click('#btn-calcola'); await w(900); es.S24_calc = await st();
  es.S24_reaz = (await rs()).slice(0, 70);
  await p.mouse.click(...scr(6, 0, 6, 3, 0)); await w(300);
  es.S24_nodo = (await pr()).match(/uy = [^m]*mm/)?.[0];
  await p.screenshot({ path: OUT + '/s24.png' });
  es.errori_console = errs;
  console.log(JSON.stringify(es, null, 1));
  await b.close();
})();
