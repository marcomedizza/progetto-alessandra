// Pannello proprietà (Lucia): mostra e modifica l'elemento selezionato.
// I campi seguono 01-ARCHITETTURA/DATA_SCHEMA.json v1.0. Ogni modifica chiama onCambio().

const esc = (v) => String(v ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const num = (v, d = 4) => Number(v).toLocaleString('it-IT', { maximumSignificantDigits: d });

export function pannelloProprieta(el, modello, caso, selezione, ris, onCambio) {
  if (!selezione) { el.innerHTML = '<p class="vuoto">Nessun elemento selezionato.</p>'; return; }
  if (selezione.tipo === 'asta') return pannelloAsta(el, modello, caso, selezione.id, ris, onCambio);
  return pannelloNodo(el, modello, caso, selezione.id, ris, onCambio);
}

function pannelloAsta(el, modello, caso, id, ris, onCambio) {
  const a = modello.aste.find((x) => x.id === id);
  const nodi = new Map(modello.nodi.map((n) => [n.id, n]));
  const ni = nodi.get(a.nodo_i), nj = nodi.get(a.nodo_j);
  const L = Math.hypot(nj.x - ni.x, nj.y - ni.y);
  const sez = modello.sezioni.find((s) => s.id === a.sezione);
  const mat = modello.materiali.find((m) => m.id === a.materiale);
  const carichi = (caso?.carichi_aste || []).filter((q) => q.asta === id);
  let h = `<table>
    <tr><td>Asta</td><td>${esc(a.id)}${a.nome ? ' · ' + esc(a.nome) : ''}</td></tr>
    <tr><td>Nodi</td><td>${a.nodo_i} → ${a.nodo_j}</td></tr>
    <tr><td>Lunghezza</td><td class="num">${num(L)} m</td></tr>
    <tr><td>Materiale</td><td>${esc(mat?.nome)} · E = ${num(mat?.E / 1000)} MPa</td></tr>
    <tr><td>Sezione</td><td><select id="p-sezione">${modello.sezioni.map((s) => `<option value="${esc(s.id)}"${s.id === a.sezione ? ' selected' : ''}>${esc(s.nome)}</option>`).join('')}</select></td></tr>
    <tr><td></td><td class="nota">A = ${num(sez.A * 1e4)} cm² · I = ${num(sez.I * 1e8)} cm⁴${sez.W ? ' · W = ' + num(sez.W * 1e6) + ' cm³' : ''}</td></tr>
    <tr><td>Cerniere</td><td><label><input type="checkbox" id="p-rzi"${a.svincoli?.rz_i ? ' checked' : ''}> in i</label> <label><input type="checkbox" id="p-rzj"${a.svincoli?.rz_j ? ' checked' : ''}> in j</label></td></tr>
  </table>`;
  h += `<p class="nota">Carichi sull'asta, caso ${esc(caso?.id)}:</p>`;
  if (!carichi.length) h += '<p class="vuoto">Nessuno.</p>';
  carichi.forEach((q, k) => {
    const etich = q.tipo === 'distribuito_uniforme' ? `q [kN/m] ${q.direzione}` : `P [kN] ${q.direzione}, a = ${num(q.a)} m`;
    h += `<div class="riga-campo"><span class="nota">${esc(etich)}</span><input type="number" step="any" data-carico="${k}" value="${q.tipo === 'distribuito_uniforme' ? q.q : q.P}"></div>`;
  });
  if (ris) {
    const s = ris.sollecitazioni.find((x) => x.asta === id);
    const mx = (c) => Math.max(...s[c].map(Math.abs));
    h += `<p class="nota">Sollecitazioni massime: |M| = ${num(mx('M'))} kNm · |V| = ${num(mx('V'))} kN · |N| = ${num(mx('N'))} kN</p>`;
  }
  el.innerHTML = h;
  el.querySelector('#p-sezione').addEventListener('change', (e) => { a.sezione = e.target.value; onCambio(); });
  for (const [sel, k] of [['#p-rzi', 'rz_i'], ['#p-rzj', 'rz_j']]) {
    el.querySelector(sel).addEventListener('change', (e) => { a.svincoli = { ...(a.svincoli || {}), [k]: e.target.checked }; onCambio(); });
  }
  el.querySelectorAll('[data-carico]').forEach((inp) => inp.addEventListener('change', (e) => {
    const q = carichi[Number(e.target.dataset.carico)], v = Number(e.target.value);
    if (!Number.isFinite(v)) return;
    if (q.tipo === 'distribuito_uniforme') q.q = v; else q.P = v;
    onCambio();
  }));
}

function pannelloNodo(el, modello, caso, id, ris, onCambio) {
  const n = modello.nodi.find((x) => x.id === id);
  let v = modello.vincoli.find((x) => x.nodo === id);
  let c = (caso?.carichi_nodali || []).find((x) => x.nodo === id);
  let h = `<table>
    <tr><td>Nodo</td><td>${esc(n.id)}${n.nome ? ' · ' + esc(n.nome) : ''}</td></tr>
    <tr><td>Coordinate</td><td class="num">x = ${num(n.x)} m · y = ${num(n.y)} m</td></tr>
    <tr><td>Vincolo</td><td>${['ux', 'uy', 'rz'].map((k) => `<label><input type="checkbox" data-vincolo="${k}"${v?.[k] ? ' checked' : ''}> ${k}</label>`).join(' ')}</td></tr>
  </table>
  <p class="nota">Carichi nodali, caso ${esc(caso?.id)}:</p>`;
  for (const [k, u] of [['Fx', 'kN'], ['Fy', 'kN'], ['Mz', 'kNm']]) {
    h += `<div class="riga-campo"><span class="nota">${k} [${u}]</span><input type="number" step="any" data-forza="${k}" value="${c?.[k] ?? 0}"></div>`;
  }
  if (ris) {
    const u = ris.spostamenti.find((x) => x.nodo === id), r = ris.reazioni.find((x) => x.nodo === id);
    h += `<p class="nota">ux = ${num(u.ux * 1000)} mm · uy = ${num(u.uy * 1000)} mm · rz = ${num(u.rz * 1000)} mrad</p>`;
    if (r) h += `<p class="nota">Reazioni: Rx = ${num(r.Rx)} kN · Ry = ${num(r.Ry)} kN · Mz = ${num(r.Mz)} kNm</p>`;
  }
  el.innerHTML = h;
  el.querySelectorAll('[data-vincolo]').forEach((inp) => inp.addEventListener('change', (e) => {
    if (!v) { v = { nodo: id }; modello.vincoli.push(v); }
    v[e.target.dataset.vincolo] = e.target.checked;
    if (!v.ux && !v.uy && !v.rz && !v.molle) modello.vincoli.splice(modello.vincoli.indexOf(v), 1);
    onCambio();
  }));
  el.querySelectorAll('[data-forza]').forEach((inp) => inp.addEventListener('change', (e) => {
    const val = Number(e.target.value);
    if (!Number.isFinite(val) || !caso) return;
    if (!c) { c = { nodo: id }; (caso.carichi_nodali ||= []).push(c); }
    c[e.target.dataset.forza] = val;
    onCambio();
  }));
}
