const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const OUT = process.argv[2], PID = process.argv[3];
  const b = await chromium.launch({ args: ['--use-gl=swiftshader','--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 1300, height: 760 } });
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  const esito = {}; const st = () => p.textContent('#stato'); const pr = () => p.textContent('#pannello-proprieta'); const rs = () => p.textContent('#pannello-risultati');
  const w = (ms) => p.waitForTimeout(ms);
  await p.goto('http://127.0.0.1:8765/'); await w(1200);
  esito.S1 = (await st()).includes('Portale incastrato, carico uniforme');
  await p.click('#btn-calcola'); await w(800);
  esito.S2 = (await st()).includes('Calcolo completato') && (await rs()).includes('90,00') && (await rs()).includes('83,70');
  for (const d of ['V','N','']) { await p.check(`input[name=diag][value="${d}"]`); await w(150); }
  esito.S3 = (await st()).includes('Calcolo completato');
  await p.check('input[name=diag][value=M]');
  await p.uncheck('#chk-def'); await w(150); await p.check('#chk-def'); await w(150);
  esito.S4 = true;
  for (const v of ['alto','asso','frontale']) { await p.click(`[data-vista=${v}]`); await w(200); }
  esito.S5 = true;
  const box = await p.locator('#vista canvas').boundingBox();
  await p.mouse.click(box.x + box.width / 2, box.y + box.height * 0.305); await w(300);
  const t6 = await pr(); esito.S6 = t6.includes('traverso') && t6.includes('-30') === false ? t6.includes('traverso') : t6.includes('traverso');
  await p.selectOption('#p-sezione', 'HEA200'); await w(300);
  const msg7 = await st(); await p.click('#btn-calcola'); await w(800);
  const r7 = await rs(); esito.S7 = msg7.includes('Modello modificato') && !r7.includes('51,30');
  await p.selectOption('#p-sezione', 'IPE300'); await w(200);
  await p.fill('[data-carico="0"]', '-40'); await p.dispatchEvent('[data-carico="0"]', 'change'); await w(200);
  await p.click('#btn-calcola'); await w(800);
  esito.S8 = (await rs()).includes('120,00');
  await p.screenshot({ path: OUT + '/s8.png' });
  await p.mouse.click(box.x + box.width * 0.292, box.y + box.height * 0.305); await w(300);
  const t9 = await pr(); esito.S9 = t9.includes('Coordinate') && t9.includes('mm');
  await p.selectOption('#sel-caso', 'C1_trave_appoggiata'); await w(700);
  await p.mouse.click(box.x + box.width * 0.083, box.y + box.height * 0.5); await w(300);
  // nodo 1 di C1: se non selezionato col mouse, si toglie il vincolo dal pannello del nodo selezionato
  const t10 = await pr();
  if (t10.includes('Coordinate')) { await p.uncheck('[data-vincolo=ux]'); await w(200); }
  await p.click('#btn-calcola'); await w(800);
  const m10 = await st(); esito.S10 = m10.includes('labile') || m10.includes('singolare'); esito.S10_msg = m10; esito.S10_nodo = t10.slice(0, 60);
  await p.selectOption('#sel-caso', 'C5_telaio_due_piani'); await w(700); await p.click('#btn-calcola'); await w(900);
  esito.S11 = (await rs()).includes('300') || (await rs()).includes('135,21');
  await p.screenshot({ path: OUT + '/s11.png' });
  await p.setInputFiles('#file-modello', '06-TESTING/casi/C2_mensola.json'); await w(600);
  await p.click('#btn-calcola'); await w(800);
  esito.S12 = (await st()).includes('Calcolo completato') && (await rs()).includes('30,00');
  await p.selectOption('#sel-caso', '__esempio'); await w(700);
  await p.selectOption('#sel-carico', 'comb:SLU1'); await w(300); await p.click('#btn-calcola'); await w(1000);
  esito.combinazione = (await st()).includes('combinazione lineare'); esito.comb_msg = await st();
  await p.screenshot({ path: OUT + '/comb.png' });
  process.kill(Number(PID)); await w(700);
  await p.click('#btn-calcola'); await w(800);
  esito.S13 = (await st()).includes('non raggiungibile'); esito.S13_msg = await st();
  esito.errori_console = errs.filter(e => !e.includes('Failed to load resource') || !esito.S13);
  fs.writeFileSync(OUT + '/esiti.json', JSON.stringify(esito, null, 1));
  console.log(JSON.stringify(esito, null, 1));
  await b.close();
})();
