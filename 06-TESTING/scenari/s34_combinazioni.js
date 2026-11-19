const { chromium } = require('playwright');
(async () => {
  const OUT = process.argv[2];
  const b = await chromium.launch({ args: ['--use-gl=swiftshader','--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 1300, height: 760 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  const w = (ms) => p.waitForTimeout(ms), esito = {};
  await p.goto('http://127.0.0.1:8765/'); await w(1200);
  for (const nome of ['C23_combinazione_termica', 'C24_due_piani_combinazione', 'C26_continua_carico_cedimento', 'C27_due_piani_termica', 'C30_tre_piani_misti']) {
    await p.selectOption('#sel-caso', nome); await w(900);
    await p.selectOption('#sel-carico', 'comb:SLU1'); await w(300); await p.click('#btn-calcola'); await w(1200);
    const rs = await p.textContent('#pannello-risultati');
    esito[nome] = { stato: await p.textContent('#stato'), valori: (rs.match(/-?\d+,\d+/g) || []).slice(0, 14) };
    await p.screenshot({ path: `${OUT}/s34_${nome.slice(0, 3)}.png` });
  }
  esito.errori = errs; console.log(JSON.stringify(esito, null, 1)); await b.close();
})();
