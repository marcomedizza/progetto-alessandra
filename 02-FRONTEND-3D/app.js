// Collegamento tra vista (Irene), pannello proprietà (Lucia), risultati (Mariana) e servizio (Natalia).
import { Vista } from './vista.js';
import { pannelloProprieta } from './proprieta.js';
import { disegnaRisultati, tabellaRisultati } from './risultati.js';
import { pannelloModifica, modelloNuovo } from './modifica.js';

const $ = (s) => document.querySelector(s);
const esc = (v) => String(v ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

// Caso effettivo: un caso di carico, oppure una combinazione resa come caso con carichi moltiplicati (sola lettura).
function casoEffettivo(m, valore) {
  if (!valore?.startsWith('comb:')) return m.casi_di_carico.find((c) => c.id === valore) || m.casi_di_carico[0];
  const comb = (m.combinazioni || []).find((c) => c.id === valore.slice(5));
  const out = { id: comb.id, nome: comb.nome, _combinazione: true, carichi_nodali: [], carichi_aste: [], peso_proprio: false };
  for (const [cid, f] of Object.entries(comb.coefficienti)) {
    const c = m.casi_di_carico.find((x) => x.id === cid);
    if (!c) continue;
    for (const q of c.carichi_nodali || []) out.carichi_nodali.push({ nodo: q.nodo, Fx: f * (q.Fx || 0), Fy: f * (q.Fy || 0), Mz: f * (q.Mz || 0) });
    for (const q of c.carichi_aste || []) out.carichi_aste.push(q.tipo === 'concentrato' ? { ...q, P: f * q.P } : { ...q, q: f * q.q });
    if (c.peso_proprio) {   // peso proprio come carico uniforme equivalente su ogni asta
      for (const a of m.aste) {
        const mat = m.materiali.find((x) => x.id === a.materiale), se = m.sezioni.find((x) => x.id === a.sezione);
        if (mat?.peso_specifico) out.carichi_aste.push({ asta: a.id, tipo: 'distribuito_uniforme', direzione: 'globale_y', q: -f * mat.peso_specifico * se.A });
      }
    }
  }
  return out;
}
const stato = { modello: null, caso: null, ris: null, selezione: null, servizio: false };

const vista = new Vista($('#vista'), (sel) => { stato.selezione = sel; aggiorna(); });

function messaggio(testo, tipo = '') { const e = $('#stato'); e.textContent = testo; e.className = tipo; }

function opzioni() {
  return { deformata: $('#chk-def').checked, diagramma: document.querySelector('input[name=diag]:checked').value };
}

function aggiorna(ridisegnaModello = true) {
  const m = stato.modello;
  if (!m) return;
  stato.caso = casoEffettivo(m, $('#sel-carico').value);
  if (ridisegnaModello) vista.disegna(m, stato.caso, stato.selezione);
  vista.impostaEtichette(disegnaRisultati(vista.gruppoRisultati, m, stato.ris, opzioni(), vista.S, stato.caso));
  const modificato = (testo = 'Modello modificato', deseleziona = false) => {
    stato.ris = null;
    if (deseleziona) stato.selezione = null;
    messaggio(`${testo}: premi «Calcola» per aggiornare i risultati`);
    aggiorna();
  };
  pannelloProprieta($('#pannello-proprieta'), m, stato.caso, stato.selezione, stato.ris, () => modificato());
  pannelloModifica($('#pannello-modifica'), m, stato.caso, stato.selezione, (t, d) => { modificato(t, d); vista.vista(vista.vistaCorrente); },
    (err) => messaggio(err, 'errore'));
  $('#pannello-risultati').innerHTML = tabellaRisultati(m, stato.ris);
}

function caricaModello(m) {
  stato.modello = m; stato.ris = null; stato.selezione = null;
  $('#sel-carico').innerHTML = m.casi_di_carico.map((c) => `<option value="${esc(c.id)}">${esc(c.id)} · ${esc(c.nome)}</option>`).join('')
    + (m.combinazioni || []).map((c) => `<option value="comb:${esc(c.id)}">combinazione ${esc(c.id)} · ${esc(c.nome)}</option>`).join('');
  aggiorna();
  vista.vista(vista.vistaCorrente);
  messaggio(`${m.progetto.nome}: ${m.nodi.length} nodi, ${m.aste.length} aste`);  // textContent: nessun rischio
}

async function calcola() {
  if (!stato.modello) return;
  if (!stato.servizio) { messaggio('Servizio di calcolo non raggiungibile', 'errore'); return; }
  messaggio('Calcolo in corso...');
  try {
    const par = stato.caso._combinazione ? `combinazione=${encodeURIComponent(stato.caso.id)}` : `caso=${encodeURIComponent(stato.caso.id)}`;
    const r = await fetch(`/api/calcola?${par}`, {
      method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(stato.modello),
    });
    const j = await r.json();
    if (!r.ok) {
      const d = j.detail;
      const txt = typeof d === 'string' ? d : [...(d.schema || []).map((e) => `${e.percorso}: ${e.messaggio}`), ...(d.coerenza || [])].join(' · ');
      messaggio('Errore: ' + txt, 'errore');
      return;
    }
    stato.ris = j.risultati[0];
    messaggio(`Calcolo completato (${stato.ris.solutore})`, 'ok');
    aggiorna(false);
  } catch (e) {
    messaggio('Servizio di calcolo non raggiungibile: avviarlo con uvicorn (vedi README)', 'errore');
  }
}

async function avvio() {
  try {
    const casi = await (await fetch('/api/casi')).json();
    stato.servizio = true;
    const esempio = { nome: '__esempio', titolo: 'Esempio di riferimento (con combinazione SLU)' };
    $('#sel-caso').innerHTML = [...casi, esempio].map((c) => `<option value="${esc(c.nome)}">${esc(c.titolo)}</option>`).join('');
    const pref = casi.find((c) => c.nome.startsWith('C4')) || casi[0];
    $('#sel-caso').value = pref.nome;
    caricaModello(await (await fetch(`/api/casi/${pref.nome}`)).json());
  } catch (e) {
    messaggio('Servizio non raggiungibile: si può aprire un modello da file, ma non calcolare', 'errore');
  }
}

$('#sel-caso').addEventListener('change', async (e) => {
  const url = e.target.value === '__esempio' ? '/api/esempio' : `/api/casi/${encodeURIComponent(e.target.value)}`;
  caricaModello(await (await fetch(url)).json());
});
$('#file-modello').addEventListener('change', async (e) => {
  const f = e.target.files[0];
  if (!f) return;
  try { caricaModello(JSON.parse(await f.text())); } catch { messaggio('File non leggibile come modello JSON', 'errore'); }
});
$('#sel-carico').addEventListener('change', () => { stato.ris = null; aggiorna(); });
$('#btn-nuovo').addEventListener('click', () => caricaModello(modelloNuovo()));
$('#btn-calcola').addEventListener('click', calcola);
$('#chk-def').addEventListener('change', () => aggiorna(false));
document.querySelectorAll('input[name=diag]').forEach((r) => r.addEventListener('change', () => aggiorna(false)));
document.querySelectorAll('[data-vista]').forEach((b) => b.addEventListener('click', () => {
  document.querySelectorAll('[data-vista]').forEach((x) => x.classList.toggle('attivo', x === b));
  vista.vista(b.dataset.vista);
}));

avvio();
