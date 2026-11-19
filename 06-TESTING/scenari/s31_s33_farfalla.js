const { chromium } = require('playwright');
(async () => {
  const OUT = process.argv[2];
  const b = await chromium.launch({ args: ['--use-gl=swiftshader','--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 1300, height: 820 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  const w = (ms) => p.waitForTimeout(ms); const st = () => p.textContent('#stato'); const rs = () => p.textContent('#pannello-risultati');
  const es = {};
  await p.goto('http://127.0.0.1:8765/'); await w(1200);
  const box = await p.locator('#vista canvas').boundingBox();
  const scr = (X, Y, S, cx, cy) => { const a = box.width / box.height, m = 0.85 * S;
    return [box.x + box.width / 2 + (X - cx) / (m * a) * box.width / 2, box.y + box.height / 2 - (Y - cy) / m * box.height / 2]; };
  // S31 — D17: trave nuova (appoggiata), ΔT a farfalla +10 °C → nessuna reazione, freccia −κL²/8 = −1,80 mm in mezzeria
  await p.click('#btn-nuovo'); await w(500);
  await p.mouse.click(...scr(3, 0, 6, 3, 0)); await w(300);
  es.S31_nota = (await p.textContent('#pannello-modifica')).match(/ΔT a farfalla = [^.]*/)?.[0];
  await p.fill('#m-dtg', '10'); await p.click('#m-add-dt'); await w(300); es.S31_msg = await st();
  await p.click('#btn-calcola'); await w(900);
  es.S31 = [await st(), (await rs()).match(/Spostamento massimo[^(]*/)?.[0]];
  // trapezio dopo il ΔT: lo schema resta 1.2 e il calcolo riesce
  await p.mouse.click(...scr(3, 0, 6, 3, 0)); await w(300);
  await p.click('#m-add-trap'); await w(300); await p.click('#btn-calcola'); await w(900); es.S31_trap = await st();
  // S32 — mancanza di h: nuova sezione senza h → messaggio
  await p.mouse.click(...scr(3, 0, 6, 3, 0)); await w(300);
  await p.click('#p-nuova-sez'); await w(300);
  await p.fill('[data-valore="sez.h"]', ''); await w(100);
  await p.evaluate(() => { const i = document.querySelector('[data-valore="sez.h"]'); i.value = '-1'; i.dispatchEvent(new Event('change')); });
  await w(200); es.S32_h_rifiutato = await p.inputValue('[data-valore="sez.h"]');
  // S33 — ΔT uniforme su trave appoggiata (carrello libero): nessuna forza, solo allungamento
  await p.fill('#m-dtu', '20'); await p.fill('#m-dtg', '0'); await p.click('#m-add-dt'); await w(300);
  await p.click('#btn-calcola'); await w(900); es.S33 = [await st(), (await rs()).slice(0, 60)];
  es.errori_console = errs;
  console.log(JSON.stringify(es, null, 1));
  await b.close();
})();
