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

// Carico lineare su un tratto dell'asta (D15, Lucia e Daniela): parziale, trapezoidale o triangolare.
// Porta il modello alla versione 1.1 dello schema, che lo prevede.
export function aggiungiCaricoTrapezio(m, caso, asta, qi, qj, a, b, direzione = 'globale_y') {
  if (!caso || caso._combinazione) return 'Scegliere un caso di carico, non una combinazione';
  const el = m.aste.find((x) => x.id === asta);
  const ni = m.nodi.find((n) => n.id === el.nodo_i), nj = m.nodi.find((n) => n.id === el.nodo_j);
  const L = Math.hypot(nj.x - ni.x, nj.y - ni.y);
  if (![qi, qj, a, b].every(Number.isFinite)) return 'Valori del trapezio non validi';
  if (!(a >= 0 && a < b && b <= L + 1e-9)) return `Il tratto deve stare dentro l'asta: 0 ≤ a < b ≤ ${+L.toFixed(3)} m`;
  if (!['globale_y', 'globale_x', 'locale_y'].includes(direzione)) return 'Direzione del carico non valida';
  (caso.carichi_aste ||= []).push({ asta, tipo: 'distribuito_trapezio', direzione, q_i: qi, q_j: qj, a, b: Math.min(b, L) });
  m.schema_version = '1.1';
  return true;
}

// Cedimento impresso (D15, Lucia e Carla): solo sulle componenti vincolate del nodo. Valori in m e rad.
export function impostaCedimento(m, caso, nodo, valori) {
  if (!caso || caso._combinazione) return 'Scegliere un caso di carico, non una combinazione';
  const v = m.vincoli.find((x) => x.nodo === nodo) || {};
  for (const k of ['ux', 'uy', 'rz']) {
    if (!Number.isFinite(valori[k])) return 'Valori del cedimento non validi';
    if (valori[k] && !v[k]) return `Cedimento ${k} non ammesso: il nodo ${nodo} non ha ${k} vincolato`;
  }
  caso.cedimenti = (caso.cedimenti || []).filter((d) => d.nodo !== nodo);
  const d = { nodo };
  for (const k of ['ux', 'uy', 'rz']) if (valori[k]) d[k] = valori[k];
  if (Object.keys(d).length > 1) caso.cedimenti.push(d);
  if (!caso.cedimenti.length) delete caso.cedimenti;
  m.schema_version = '1.1';
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
    const a = m.aste.find((x) => x.id === selezione.id);
    const ni = m.nodi.find((n) => n.id === a.nodo_i), nj = m.nodi.find((n) => n.id === a.nodo_j);
    const L = +Math.hypot(nj.x - ni.x, nj.y - ni.y).toFixed(6);
    h += `<div class="riga-campo"><span class="nota">q [kN/m] su asta ${selezione.id}</span>
      <span class="gruppo"><input type="number" step="any" id="m-q" value="-10" aria-label="Carico uniforme"><button id="m-add-q">+ carico</button></span></div>
    <div class="riga-campo"><span class="nota">Trapezio, direzione</span>
      <span class="gruppo"><select id="m-tdir" aria-label="Direzione del trapezio"><option value="globale_y">verticale (Y)</option><option value="globale_x">orizzontale (X)</option><option value="locale_y">normale all'asta</option></select></span></div>
    <div class="riga-campo"><span class="nota">q_i, q_j [kN/m]</span>
      <span class="gruppo"><input type="number" step="any" id="m-qi" value="-10" aria-label="q iniziale"><input type="number" step="any" id="m-qj" value="-20" aria-label="q finale"></span></div>
    <div class="riga-campo"><span class="nota">da a, a b [m]</span>
      <span class="gruppo"><input type="number" step="any" id="m-ta" value="0" aria-label="Inizio del tratto"><input type="number" step="any" id="m-tb" value="${L}" aria-label="Fine del tratto"><button id="m-add-trap">+ trapezio</button></span></div>`;
  }
  if (selezione?.tipo === 'nodo' && caso && !caso._combinazione) {
    const v = m.vincoli.find((x) => x.nodo === selezione.id) || {};
    const d = (caso.cedimenti || []).find((x) => x.nodo === selezione.id) || {};
    const comp = [['ux', 'mm', 1000], ['uy', 'mm', 1000], ['rz', 'mrad', 1000]].filter(([k]) => v[k]);
    if (comp.length) {
      h += `<div class="riga-campo"><span class="nota">Cedimento ${comp.map(([k, u]) => `${k} [${u}]`).join(', ')}</span>
        <span class="gruppo">${comp.map(([k, , f]) => `<input type="number" step="any" data-ced="${k}" value="${(d[k] || 0) * f}" aria-label="Cedimento ${k}">`).join('')}<button id="m-ced">imposta</button></span></div>`;
    }
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
  el.querySelector('#m-add-trap')?.addEventListener('click', () => {
    const val = (id) => Number(el.querySelector(id).value);
    const r = aggiungiCaricoTrapezio(m, caso, selezione.id, val('#m-qi'), val('#m-qj'), val('#m-ta'), val('#m-tb'), el.querySelector('#m-tdir').value);
    esito(r, `Carico trapezoidale aggiunto all'asta ${selezione.id} (schema 1.1)`);
  });
  el.querySelector('#m-ced')?.addEventListener('click', () => {
    const valori = { ux: 0, uy: 0, rz: 0 };
    el.querySelectorAll('[data-ced]').forEach((i) => { valori[i.dataset.ced] = Number(i.value) / 1000; });
    const r = impostaCedimento(m, caso, selezione.id, valori);
    esito(r, `Cedimento del nodo ${selezione.id} aggiornato (schema 1.1)`);
  });
  el.querySelector('#m-elimina')?.addEventListener('click', () => {
    if (selezione.tipo === 'asta') eliminaAsta(m, selezione.id); else eliminaNodo(m, selezione.id);
    onCambio(`Eliminato ${selezione.tipo} ${selezione.id}`, true);
  });
}
