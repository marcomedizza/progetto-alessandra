// Prove delle funzioni di modifica del modello (Natalia, 06/11). Uso: node 02-FRONTEND-3D/prove_modifica.mjs
import assert from 'node:assert/strict';
import { modelloNuovo, aggiungiNodo, aggiungiAsta, aggiungiCaricoTrapezio, impostaCedimento, aggiungiTermico } from './modifica.js';

const prove = {
  'punto 43: la versione dello schema sale e non scende'() {
    const m = modelloNuovo(), c = m.casi_di_carico[0];
    assert.equal(m.schema_version, '1.0');
    assert.equal(aggiungiCaricoTrapezio(m, c, 1, -10, -20, 0, 6), true);
    assert.equal(m.schema_version, '1.1');
    assert.equal(aggiungiTermico(m, c, 1, 0, 10), true);
    assert.equal(m.schema_version, '1.2');
    assert.equal(aggiungiCaricoTrapezio(m, c, 1, -5, -5, 1, 2), true);
    assert.equal(impostaCedimento(m, c, 2, { ux: 0, uy: -0.01, rz: 0 }), true);
    assert.equal(m.schema_version, '1.2');
  },
  'trapezio fuori dall\'asta e direzione non valida rifiutati'() {
    const m = modelloNuovo(), c = m.casi_di_carico[0];
    assert.match(aggiungiCaricoTrapezio(m, c, 1, -10, -10, 0, 7), /dentro l'asta/);
    assert.match(aggiungiCaricoTrapezio(m, c, 1, -10, -10, 0, 6, 'obliqua'), /Direzione/);
  },
  'cedimento solo sulle componenti vincolate'() {
    const m = modelloNuovo(), c = m.casi_di_carico[0];
    assert.match(impostaCedimento(m, c, 2, { ux: 0.01, uy: 0, rz: 0 }), /non ha ux vincolato/);
    assert.equal(impostaCedimento(m, c, 2, { ux: 0, uy: -0.01, rz: 0 }), true);
    assert.deepEqual(c.cedimenti, [{ nodo: 2, uy: -0.01 }]);
    assert.equal(impostaCedimento(m, c, 2, { ux: 0, uy: 0, rz: 0 }), true);   // azzerato: rimosso
    assert.equal(c.cedimenti, undefined);
  },
  'ΔT: servono α e h, niente ΔT uniforme con assiale rigida'() {
    const m = modelloNuovo(), c = m.casi_di_carico[0];
    delete m.sezioni[0].h;
    assert.match(aggiungiTermico(m, c, 1, 0, 10), /altezza h/);
    delete m.materiali[0].alfa_t;
    assert.match(aggiungiTermico(m, c, 1, 20, 0), /Manca α/);
    const m2 = modelloNuovo();
    m2.analisi.deformabilita_assiale = false;
    assert.match(aggiungiTermico(m2, m2.casi_di_carico[0], 1, 20, 0), /deformabilità assiale/);
  },
  'nodi e aste: doppioni rifiutati, identificativi progressivi'() {
    const m = modelloNuovo();
    assert.equal(aggiungiNodo(m, 0, 3), 3);
    assert.match(String(aggiungiNodo(m, 0, 3)), /Esiste già/);
    assert.equal(aggiungiAsta(m, 1, 3, 'IPE300'), 2);
    assert.match(String(aggiungiAsta(m, 3, 1, 'IPE300')), /Esiste già/);
  },
};

let n = 0;
for (const [nome, f] of Object.entries(prove)) { f(); n++; console.log('✓', nome); }
console.log(`${n} prove superate`);
