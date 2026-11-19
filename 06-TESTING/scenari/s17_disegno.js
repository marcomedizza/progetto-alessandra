const { chromium } = require('playwright');
(async () => {
  const OUT = process.argv[2];
  const b = await chromium.launch({ args: ['--use-gl=swiftshader','--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 1300, height: 820 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  const w = (ms) => p.waitForTimeout(ms); const st = () => p.textContent('#stato'); const pr = () => p.textContent('#pannello-proprieta');
  const es = {};
  await p.goto('http://127.0.0.1:8765/'); await w(1200);
  const box = await p.locator('#vista canvas').boundingBox();
  // vista frontale: centro del modello al centro, semialtezza 0,85·S
  const scr = (X, Y, S, cx, cy) => { const a = box.width / box.height, m = 0.85 * S;
    return [box.x + box.width / 2 + (X - cx) / (m * a) * box.width / 2, box.y + box.height / 2 - (Y - cy) / m * box.height / 2]; };
  // S17 — D10: Nuovo (nodi 0,0 e 6,0: S = 6, centro 3,0), disegno 1 → (0,3) → (6,3) → 2
  await p.click('#btn-nuovo'); await w(500);
  await p.click('#btn-disegna'); await w(200);
  es.S17_avvio = await st();
  let c = scr(0, 0, 6, 3, 0); await p.mouse.click(...c); await w(300); es.S17_a = await st();
  c = scr(0.1, 3.12, 6, 3, 0); await p.mouse.click(...c); await w(300); es.S17_b = await st();
  c = scr(6.05, 2.9, 6, 3, 0); await p.mouse.click(...c); await w(300); es.S17_c = await st();
  c = scr(6, 0, 6, 3, 0); await p.mouse.click(...c); await w(300); es.S17_d = await st();
  await p.keyboard.press('Escape'); await w(100);
  await p.screenshot({ path: OUT + '/s17.png' });
  await p.click('#btn-disegna'); await w(200);
  es.S17_fine = await st();
  c = scr(0, 3, 6, 3, 0); await p.mouse.click(...c); await w(300); es.S17_nodo3 = (await pr()).match(/x = [^m]*m · y = [^m]*m/)?.[0];
  // carico orizzontale 10 kN nel nodo 3 e calcolo del portale disegnato
  await p.fill('[data-forza=Fx]', '10'); await p.dispatchEvent('[data-forza=Fx]', 'change'); await w(200);
  await p.click('#btn-calcola'); await w(900);
  es.S17_calc = await st(); es.S17_ris = (await p.textContent('#pannello-risultati')).slice(0, 160);
  // S18 — revisione 14 su C1: I raddoppiato → freccia dimezzata (9,617 → 4,808 mm)
  await p.selectOption('#sel-caso', 'C1_trave_appoggiata'); await w(700);
  c = scr(1.5, 0, 6, 3, 0); await p.mouse.click(...c); await w(300);
  es.S18_sel = (await pr()).slice(0, 40);
  await p.fill('[data-valore="sez.I"]', String(2 * 8356)); await p.dispatchEvent('[data-valore="sez.I"]', 'change'); await w(200);
  await p.click('#btn-calcola'); await w(900);
  c = scr(3, 0, 6, 3, 0); await p.mouse.click(...c); await w(300);
  es.S18_uy = (await pr()).match(/uy = [^m]*mm/)?.[0];
  // valore non positivo rifiutato, copia di sezione e materiale
  c = scr(1.5, 0, 6, 3, 0); await p.mouse.click(...c); await w(300);
  await p.fill('[data-valore="mat.E"]', '-5'); await p.dispatchEvent('[data-valore="mat.E"]', 'change'); await w(200);
  es.S18_E_rifiutato = await p.inputValue('[data-valore="mat.E"]');
  await p.click('#p-nuova-sez'); await w(200); es.S18_nuova_sez = await p.inputValue('#p-sezione');
  await p.click('#p-nuovo-mat'); await w(200); es.S18_nuovo_mat = await p.inputValue('#p-materiale');
  await p.fill('[data-valore="mat.E"]', '70000'); await p.dispatchEvent('[data-valore="mat.E"]', 'change'); await w(200);
  await p.click('#btn-calcola'); await w(900); es.S18_calc = await st();
  c = scr(3, 0, 6, 3, 0); await p.mouse.click(...c); await w(300);
  es.S18_uy_alluminio = (await pr()).match(/uy = [^m]*mm/)?.[0];
  // S19 — D8: C6 deformata con cerniera
  await p.selectOption('#sel-caso', 'C6_trave_gerber'); await w(700);
  await p.click('#btn-calcola'); await w(900); es.S19 = await st();
  es.S19_nota = (await p.textContent('#pannello-risultati')).includes('comprese quelle alle cerniere');
  await p.screenshot({ path: OUT + '/s19.png' });
  es.errori_console = errs;
  console.log(JSON.stringify(es, null, 1));
  await b.close();
})();
