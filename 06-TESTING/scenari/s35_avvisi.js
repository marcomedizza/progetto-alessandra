const { chromium } = require('playwright');
(async () => {
  const OUT = process.argv[2];
  const b = await chromium.launch({ args: ['--use-gl=swiftshader','--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 1300, height: 760 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('http://127.0.0.1:8765/'); await p.waitForTimeout(1200);
  const m = await (await fetch('http://127.0.0.1:8765/api/casi/C1_trave_appoggiata')).json();
  m.casi_di_carico[0].carichi_aste[0].q = -1e9; m.progetto.id = 'C1_avviso';
  const fs = require('fs'); fs.writeFileSync(OUT + '/c1_avviso.json', JSON.stringify(m));
  await p.setInputFiles('input[type=file]', OUT + '/c1_avviso.json'); await p.waitForTimeout(900);
  await p.click('#btn-calcola'); await p.waitForTimeout(1200);
  console.log(JSON.stringify({ stato: await p.textContent('#stato'), classe: await p.getAttribute('#stato', 'class'), errs }));
  await p.screenshot({ path: OUT + '/avviso.png' }); await b.close();
})();
