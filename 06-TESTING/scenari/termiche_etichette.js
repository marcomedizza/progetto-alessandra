const { chromium } = require('playwright');
(async () => {
  const OUT = process.argv[2];
  const b = await chromium.launch({ args: ['--use-gl=swiftshader','--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 1300, height: 820 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  const w = (ms) => p.waitForTimeout(ms);
  await p.goto('http://127.0.0.1:8765/'); await w(1200);
  for (const [nome, d] of [['C14_termica_incastrata', 'N'], ['C18_termica_appoggiata', 'M'], ['C19_gerber_termica', 'M']]) {
    await p.selectOption('#sel-caso', nome); await w(700); await p.click('#btn-calcola'); await w(900);
    await p.check(`input[name=diag][value="${d}"]`); await w(300);
    await p.locator('#vista').screenshot({ path: `${OUT}/m_${nome.slice(0, 3)}.png` });
    console.log(nome, await p.$$eval('.etichetta', (l) => l.map((x) => x.textContent)), (await p.textContent('#pannello-risultati')).match(/Spostamento massimo[^(]*/)?.[0]);
  }
  console.log('errori', errs);
  await b.close();
})();
