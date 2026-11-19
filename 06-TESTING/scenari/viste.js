const { chromium } = require('playwright');
(async () => {
  const OUT = process.argv[2];
  const b = await chromium.launch({ args: ['--use-gl=swiftshader','--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 1300, height: 820 } });
  const w = (ms) => p.waitForTimeout(ms);
  await p.goto('http://127.0.0.1:8765/'); await w(1200);
  for (const nome of ['C5_telaio_due_piani', 'C12_trapezio_parziale', 'C7_carico_concentrato', 'C4_portale_carico_uniforme', 'C21_inclinata_trapezio_cedimento', 'C22_gerber_trapezio_molla', 'C23_combinazione_termica', 'C13_triangolare_incastrata', 'C14_termica_incastrata', 'C24_due_piani_combinazione', 'C25_tre_cerniere_trapezio_cedimento', 'C28_portale_asimmetrico', 'C29_due_piani_trapezio_cedimento', 'C30_tre_piani_misti']) {
    await p.selectOption('#sel-caso', nome); await w(700); await p.click('#btn-calcola'); await w(900);
    await p.locator('#vista').screenshot({ path: `${OUT}/v_${nome.slice(0, 3)}.png` });
  }
  await b.close();
})();
