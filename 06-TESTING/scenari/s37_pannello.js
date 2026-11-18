// S37 (Lucia, Renata, 18/11/2026): pannello di modifica su C2, mensola HE 200 A, L = 3 m, 10 kN in punta.
// Trapezio, ΔT senza α, cedimento, annullamento con Ctrl+Z; controlli sui valori risolti a mano.
// Uso, con il servizio avviato sulla porta 8765 (README del servizio):
//   node 06-TESTING/scenari/s37_pannello.js <cartella per i file temporanei>
// Esce con codice 1 se un controllo non passa.
const { chromium } = require('playwright');
(async () => {
  const OUT = process.argv[2];
  const b = await chromium.launch({ args: ['--use-gl=swiftshader','--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 1300, height: 760 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  const w = (ms) => p.waitForTimeout(ms), st = () => p.textContent('#stato');
  const reazione = async () => { const t = await p.$$eval('#pannello-risultati table tr', (r) => r.map((x) => x.innerText)); return t.slice(0, 3).join(' | '); };
  const calcola = async () => { await p.click('#btn-calcola'); await w(900); return reazione(); };
  const e = {};
  await p.goto('http://127.0.0.1:8765/'); await w(1200);
  await p.selectOption('#sel-caso', 'C2_mensola'); await w(900);
  e.iniziale = await calcola();
  const box = await (await p.$('canvas')).boundingBox();
  async function seleziona(selettore, fx) {
    for (let fy = 0.3; fy <= 0.7; fy += 0.005) {
      await p.mouse.click(box.x + box.width * fx, box.y + box.height * fy); await w(60);
      if (await p.$(selettore)) return fy;
    }
    return null;
  }
  e.asta_y = await seleziona('#m-add-trap', 0.5);
  await p.fill('#m-qi', '-10'); await p.fill('#m-qj', '-20'); await p.fill('#m-ta', '0'); await p.fill('#m-tb', '3');
  await p.click('#m-add-trap'); await w(400); e.stato_trap = await st();
  e.con_trapezio = await calcola();
  await p.click('body', { position: { x: 5, y: 5 } }).catch(() => {}); await p.keyboard.press('Control+z'); await w(400);
  e.stato_annulla = await st(); e.dopo_annulla = await calcola();
  e.asta_y2 = await seleziona('#m-add-dt', 0.5);
  await p.fill('#m-dtg', '20'); await p.click('#m-add-dt'); await w(400); e.stato_dt = await st();
  e.nodo_x = null;
  for (let fx = 0.05; fx <= 0.5 && e.nodo_x === null; fx += 0.005) {
    await p.mouse.click(box.x + box.width * fx, box.y + box.height * e.asta_y); await w(50);
    if (await p.$('#m-ced')) e.nodo_x = fx;
  }
  e.nodo_y = e.nodo_x;
  if (e.nodo_y !== null) {
    await p.fill('[data-ced=uy]', '-10'); await p.click('#m-ced'); await w(400); e.stato_ced = await st();
    e.con_cedimento = await calcola(); e.spost_ced = (await p.textContent('#pannello-risultati')).match(/Spostamento massimo[^(]*/)?.[0];
    await p.click('body', { position: { x: 5, y: 5 } }).catch(() => {}); await p.keyboard.press('Control+z'); await w(400);
    e.dopo_annulla_ced = await calcola(); e.spost_dopo = (await p.textContent('#pannello-risultati')).match(/Spostamento massimo[^(]*/)?.[0];
  }
  e.errori = errs; console.log(JSON.stringify(e, null, 1)); await b.close();
  // valori attesi: senza trapezio Ry = 10 kN, Mz = 30 kNm; con il trapezio 10→20 kN/m su 3 m Ry += 45 kN e
  // Mz += ∫(10x + 10x²/3)dx = 75 kNm; freccia in punta PL³/3EI = 11,61 mm, più 10 mm con il cedimento
  const controlli = {
    iniziale: e.iniziale.includes('10,00\t30,00'), trapezio: e.con_trapezio?.includes('55,00\t105,00'),
    annulla: e.dopo_annulla?.includes('10,00\t30,00'), dt_senza_alfa: e.stato_dt?.startsWith('Manca α'),
    cedimento_reazioni: e.con_cedimento?.includes('10,00\t30,00'), cedimento_freccia: e.spost_ced?.includes('uy = -21,61'),
    annulla_cedimento: e.spost_dopo?.includes('uy = -11,61'), console: errs.length === 0,
  };
  console.log(JSON.stringify(controlli));
  process.exit(Object.values(controlli).every(Boolean) ? 0 : 1);
})();
