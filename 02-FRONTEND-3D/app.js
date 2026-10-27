// Collegamento tra vista (Irene), pannello proprietà (Lucia), risultati (Mariana) e servizio (Natalia).
import { Vista } from './vista.js';
import { pannelloProprieta } from './proprieta.js';
import { disegnaRisultati, tabellaRisultati } from './risultati.js';

const $ = (s) => document.querySelector(s);
const stato = { modello: null, caso: null, ris: null, selezione: null, servizio: false };

const vista = new Vista($('#vista'), (sel) => { stato.selezione = sel; aggiorna(); });

function messaggio(testo, tipo = '') { const e = $('#stato'); e.textContent = testo; e.className = tipo; }

function opzioni() {
  return { deformata: $('#chk-def').checked, diagramma: document.querySelector('input[name=diag]:checked').value };
}

function aggiorna(ridisegnaModello = true) {
  const m = stato.modello;
  if (!m) return;
  stato.caso = m.casi_di_carico.find((c) => c.id === $('#sel-carico').value) || m.casi_di_carico[0];
  if (ridisegnaModello) vista.disegna(m, stato.caso, stato.selezione);
  disegnaRisultati(vista.gruppoRisultati, m, stato.ris, opzioni(), vista.S);
  pannelloProprieta($('#pannello-proprieta'), m, stato.caso, stato.selezione, stato.ris, () => {
    stato.ris = null;
    messaggio('Modello modificato: premi «Calcola» per aggiornare i risultati');
    aggiorna();
  });
  $('#pannello-risultati').innerHTML = tabellaRisultati(m, stato.ris);
}

function caricaModello(m) {
  stato.modello = m; stato.ris = null; stato.selezione = null;
  $('#sel-carico').innerHTML = m.casi_di_carico.map((c) => `<option value="${c.id}">${c.id} · ${c.nome}</option>`).join('');
  aggiorna();
  vista.vista(vista.vistaCorrente);
  messaggio(`${m.progetto.nome}: ${m.nodi.length} nodi, ${m.aste.length} aste`);
}

async function calcola() {
  if (!stato.modello) return;
  if (!stato.servizio) { messaggio('Servizio di calcolo non raggiungibile', 'errore'); return; }
  messaggio('Calcolo in corso...');
  try {
    const r = await fetch(`/api/calcola?caso=${encodeURIComponent(stato.caso.id)}`, {
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
    $('#sel-caso').innerHTML = casi.map((c) => `<option value="${c.nome}">${c.titolo}</option>`).join('');
    const pref = casi.find((c) => c.nome.startsWith('C4')) || casi[0];
    $('#sel-caso').value = pref.nome;
    caricaModello(await (await fetch(`/api/casi/${pref.nome}`)).json());
  } catch (e) {
    messaggio('Servizio non raggiungibile: si può aprire un modello da file, ma non calcolare', 'errore');
  }
}

$('#sel-caso').addEventListener('change', async (e) => caricaModello(await (await fetch(`/api/casi/${e.target.value}`)).json()));
$('#file-modello').addEventListener('change', async (e) => {
  const f = e.target.files[0];
  if (!f) return;
  try { caricaModello(JSON.parse(await f.text())); } catch { messaggio('File non leggibile come modello JSON', 'errore'); }
});
$('#sel-carico').addEventListener('change', () => { stato.ris = null; aggiorna(); });
$('#btn-calcola').addEventListener('click', calcola);
$('#chk-def').addEventListener('change', () => aggiorna(false));
document.querySelectorAll('input[name=diag]').forEach((r) => r.addEventListener('change', () => aggiorna(false)));
document.querySelectorAll('[data-vista]').forEach((b) => b.addEventListener('click', () => {
  document.querySelectorAll('[data-vista]').forEach((x) => x.classList.toggle('attivo', x === b));
  vista.vista(b.dataset.vista);
}));

avvio();
