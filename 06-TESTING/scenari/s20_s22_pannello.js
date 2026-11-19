const { chromium } = require('playwright');
(async () => {
  const OUT = process.argv[2];
  const b = await chromium.launch({ args: ['--use-gl=swiftshader','--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 1300, height: 820 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  const w = (ms) => p.waitForTimeout(ms); const st = () => p.textContent('#stato'); const rs = () => p.textContent('#pannello-risultati');
  const es = {};
  await p.goto('http://127.0.0.1:8765/'); await w(1200);
  for (const [k, nome, attesi] of [['S20', 'C11_cedimento_appoggio', ['-4,87', '2,44', '14,62']], ['S21', 'C12_trapezio_parziale', ['25,00', '20,00']], ['S22', 'C13_triangolare_incastrata', ['18,00', '42,00', '36,00']]]) {
    await p.selectOption('#sel-caso', nome); await w(700);
    await p.click('#btn-calcola'); await w(900);
    const t = await rs();
    es[k] = { msg: await st(), valori: attesi.map((v) => [v, t.includes(v)]), etichette: await p.$$eval('.etichetta', (l) => l.map((x) => x.textContent)) };
    await p.screenshot({ path: `${OUT}/${k}.png` });
  }
  // nodo 2 di C11: cedimento mostrato nel pannello
  await p.selectOption('#sel-caso', 'C11_cedimento_appoggio'); await w(700);
  const box = await p.locator('#vista canvas').boundingBox();
  await p.mouse.click(box.x + box.width / 2, box.y + box.height / 2); await w(300);
  es.S20_nodo = (await p.textContent('#pannello-proprieta')).match(/Cedimento impresso[^\n]*/)?.[0];
  es.errori_console = errs;
  console.log(JSON.stringify(es, null, 1));
  await b.close();
})();
