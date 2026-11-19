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
  // S27 punto 32: trave nuova, trapezio orizzontale (globale_x) −10 kN/m su tutta la luce → Rx1 = +60 kN
  await p.click('#btn-nuovo'); await w(500);
  await p.mouse.click(...scr(3, 0, 6, 3, 0)); await w(300);
  await p.selectOption('#m-tdir', 'globale_x'); await p.fill('#m-qi', '-10'); await p.fill('#m-qj', '-10');
  await p.click('#m-add-trap'); await w(300); await p.click('#btn-calcola'); await w(900);
  es.S27 = [await st(), (await rs()).slice(0, 60)];
  // S28 C17 e S29 C14, C18 (v1.2)
  for (const [k, nome, att] of [['S28', 'C17_inclinata_normale', ['-18,00', '5,25', '18,75']], ['S29', 'C14_termica_incastrata', ['271,20']], ['S30', 'C18_termica_appoggiata', ['-1,80']]]) {
    await p.selectOption('#sel-caso', nome); await w(700); await p.click('#btn-calcola'); await w(900);
    const t = await rs(); es[k] = [await st(), att.map((v) => t.includes(v))];
  }
  await p.mouse.click(...scr(1.5, 0, 6, 3, 0)); await w(300);
  es.S30_pannello = (await p.textContent('#pannello-proprieta')).match(/Distorsione termica[^\n]*/)?.[0];
  await p.screenshot({ path: OUT + '/s30.png' });
  es.errori_console = errs;
  console.log(JSON.stringify(es, null, 1));
  await b.close();
})();
