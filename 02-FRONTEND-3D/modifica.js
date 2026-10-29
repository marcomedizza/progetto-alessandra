// Modifica del modello (Irene, Lucia — difetto D4): nuovo modello, aggiunta ed eliminazione di nodi e aste.
// Inserimento numerico (coordinate in m). La validazione completa la fa il servizio al momento del calcolo.

const esc = (v) => String(v ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

const SEZIONI_BASE = [
  { id: 'IPE300', nome: 'IPE 300', A: 53.81e-4, I: 8356e-8, W: 557.1e-6, fonte: 'sagomario profili IPE, asse forte' },
  { id: 'HEA200', nome: 'HE 200 A', A: 53.83e-4, I: 3692e-8, W: 388.6e-6, fonte: 'sagomario profili HE A, asse forte' },
];

export function modelloNuovo() {
  return {
    schema_version: '1.0',
    progetto: { id: 'nuovo', nome: 'Nuovo modello', tipo_modello: 'telaio_piano', unita: { lunghezza: 'm', forza: 'kN' } },
    nodi: [{ id: 1, x: 0, y: 0 }, { id: 2, x: 6, y: 0 }],
    materiali: [{ id: 'S275', nome: 'Acciaio S275', tipo: 'acciaio', E: 2.1e8, peso_specifico: 78.5 }],
    sezioni: SEZIONI_BASE.map((s) => ({ ...s })),
    aste: [{ id: 1, nodo_i: 1, nodo_j: 2, materiale: 'S275', sezione: 'IPE300' }],
    vincoli: [{ nodo: 1, ux: true, uy: true }, { nodo: 2, uy: true }],
    casi_di_carico: [{ id: 'Q', nome: 'Carichi variabili', categoria: 'Q', carichi_nodali: [], carichi_aste: [] }],
    analisi: { tipo: 'statica_lineare', deformabilita_assiale: true, punti_diagramma: 11 },
  };
}

const prossimoId = (lista) => lista.reduce((m, x) => Math.max(m, x.id), 0) + 1;

export function aggiungiNodo(m, x, y) {
  if (!Number.isFinite(x) || !Number.isFinite(y)) return 'Coordinate non valide';
  if (m.nodi.some((n) => Math.hypot(n.x - x, n.y - y) < 1e-6)) return 'Esiste già un nodo in quella posizione';
  const id = prossimoId(m.nodi);
  m.nodi.push({ id, x, y });
  return id;
}

export function aggiungiAsta(m, ni, nj, sezione) {
  if (ni === nj) return "I due nodi dell'asta devono essere diversi";
  if (!m.nodi.some((n) => n.id === ni) || !m.nodi.some((n) => n.id === nj)) return 'Nodo inesistente';
  if (m.aste.some((a) => (a.nodo_i === ni && a.nodo_j === nj) || (a.nodo_i === nj && a.nodo_j === ni))) return 'Esiste già un\'asta tra questi nodi';
  const id = prossimoId(m.aste);
  m.aste.push({ id, nodo_i: ni, nodo_j: nj, materiale: m.materiali[0].id, sezione });
  return id;
}

export function eliminaAsta(m, id) {
  m.aste = m.aste.filter((a) => a.id !== id);
  for (const c of m.casi_di_carico) c.carichi_aste = (c.carichi_aste || []).filter((q) => q.asta !== id);
}

export function eliminaNodo(m, id) {
  for (const a of m.aste.filter((x) => x.nodo_i === id || x.nodo_j === id)) eliminaAsta(m, a.id);
  m.nodi = m.nodi.filter((n) => n.id !== id);
  m.vincoli = m.vincoli.filter((v) => v.nodo !== id);
  for (const c of m.casi_di_carico) c.carichi_nodali = (c.carichi_nodali || []).filter((q) => q.nodo !== id);
}

export function aggiungiCaricoUniforme(m, caso, asta, q) {
  if (!caso || caso._combinazione) return 'Scegliere un caso di carico, non una combinazione';
  (caso.carichi_aste ||= []).push({ asta, tipo: 'distribuito_uniforme', direzione: 'globale_y', q });
  return true;
}

export function pannelloModifica(el, m, caso, selezione, onCambio, onErrore) {
  if (!m) { el.innerHTML = ''; return; }
  const opzNodi = m.nodi.map((n) => `<option value="${n.id}">${n.id} (${n.x}; ${n.y})</option>`).join('');
  const opzSez = m.sezioni.map((s) => `<option value="${esc(s.id)}">${esc(s.nome)}</option>`).join('');
  let h = `
    <div class="riga-campo"><span class="nota">Nodo x, y [m]</span>
      <span class="gruppo"><input type="number" step="any" id="m-x" value="0" aria-label="x"><input type="number" step="any" id="m-y" value="0" aria-label="y"><button id="m-add-nodo">+ nodo</button></span></div>
    <div class="riga-campo"><span class="nota">Asta i → j</span>
      <span class="gruppo"><select id="m-ni" aria-label="Nodo iniziale">${opzNodi}</select><select id="m-nj" aria-label="Nodo finale">${opzNodi}</select></span></div>
    <div class="riga-campo"><span class="nota">Sezione</span>
      <span class="gruppo"><select id="m-sez" aria-label="Sezione">${opzSez}</select><button id="m-add-asta">+ asta</button></span></div>`;
  if (selezione?.tipo === 'asta') {
    h += `<div class="riga-campo"><span class="nota">q [kN/m] su asta ${selezione.id}</span>
      <span class="gruppo"><input type="number" step="any" id="m-q" value="-10" aria-label="Carico uniforme"><button id="m-add-q">+ carico</button></span></div>`;
  }
  if (selezione) h += `<button id="m-elimina">Elimina ${selezione.tipo} ${selezione.id}</button>`;
  el.innerHTML = h;
  if (m.nodi.length > 1) el.querySelector('#m-nj').value = String(m.nodi[m.nodi.length - 1].id);

  const esito = (r, msg) => { if (typeof r === 'string') onErrore(r); else onCambio(msg); };
  el.querySelector('#m-add-nodo').addEventListener('click', () => {
    const r = aggiungiNodo(m, Number(el.querySelector('#m-x').value), Number(el.querySelector('#m-y').value));
    esito(r, `Aggiunto il nodo ${r}`);
  });
  el.querySelector('#m-add-asta').addEventListener('click', () => {
    const r = aggiungiAsta(m, Number(el.querySelector('#m-ni').value), Number(el.querySelector('#m-nj').value), el.querySelector('#m-sez').value);
    esito(r, `Aggiunta l'asta ${r}`);
  });
  el.querySelector('#m-add-q')?.addEventListener('click', () => {
    const r = aggiungiCaricoUniforme(m, caso, selezione.id, Number(el.querySelector('#m-q').value));
    esito(r, `Carico aggiunto all'asta ${selezione.id}`);
  });
  el.querySelector('#m-elimina')?.addEventListener('click', () => {
    if (selezione.tipo === 'asta') eliminaAsta(m, selezione.id); else eliminaNodo(m, selezione.id);
    onCambio(`Eliminato ${selezione.tipo} ${selezione.id}`, true);
  });
}
