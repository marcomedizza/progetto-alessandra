const { chromium } = require('playwright');
(async () => {
  const OUT = process.argv[2];
  const b = await chromium.launch({ args: ['--use-gl=swiftshader','--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 1300, height: 820 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message));
  const w = (ms) => p.waitForTimeout(ms);
  await p.goto('http://127.0.0.1:8765/'); await w(1200);
  for (const nome of ['C22_gerber_trapezio_molla', 'C8_molla_in_mezzeria', 'C9_portale_tre_cerniere_molla']) {
    await p.selectOption('#sel-caso', nome); await w(700);
    await p.locator('#vista').screenshot({ path: `${OUT}/k_${nome.slice(0, 3)}.png` });
  }
  console.log('errori', errs); await b.close();
})();
