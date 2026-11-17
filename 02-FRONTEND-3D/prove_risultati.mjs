// Prove del massimo interno del momento (punto 85; Mariana, 17/11/2026). Uso: node prove_risultati.mjs
// La funzione massimoInterno è estratta dal sorgente perché risultati.js importa three dal navigatore.
import fs from 'fs';
import assert from 'assert';
import path from 'path';
import { fileURLToPath } from 'url';

const qui = path.dirname(fileURLToPath(import.meta.url));
const src = fs.readFileSync(path.join(qui, 'risultati.js'), 'utf8');
const corpo = src.slice(src.indexOf('export function massimoInterno'), src.indexOf('function disegnaDiagramma'));
const massimoInterno = new Function(corpo.replace('export ', '') + '; return massimoInterno;')();

function campiona(passo, n, M, V) {
  const x = [], m = [], v = [];
  for (let i = 0; i <= n; i++) { const t = i * passo; x.push(t); m.push(M(t)); v.push(V(t)); }
  let im = 0;
  for (let i = 1; i < n; i++) if (Math.abs(m[i]) > Math.abs(m[im])) im = i;
  return [x, m, v, im];
}

let n = 0;
// 1. parabola: colonna sinistra di C28, M = HA·y − 2y², massimo HA²/8 in y = HA/4
const HA = 10.529411764705882;
let r = massimoInterno(...campiona(0.25, 20, (y) => HA * y - 2 * y * y, (y) => HA - 4 * y));
assert(Math.abs(r.v - HA * HA / 8) < 1e-3 && Math.abs(r.x - HA / 4) < 0.01); n++;
// 2. cubica: trave appoggiata con trapezio 10→30 kN/m, L = 6 m
r = massimoInterno(...campiona(0.6, 10, (t) => 50 * t - 5 * t * t - 20 / 36 * t ** 3, (t) => 50 - 10 * t - 20 / 12 * t * t));
assert(Math.abs(r.v - 90.6165) < 1e-3); n++;
// 3. taglio senza cambio di segno nei tratti vicini: resta il valore campionato
const [x, m, v] = campiona(1, 4, (t) => t, () => 1);
r = massimoInterno(x, m, v, 3);
assert(r.v === 3 && r.x === 3); n++;
// 4. momento negativo (fibre superiori tese): cerca il massimo in valore assoluto
r = massimoInterno(...campiona(0.25, 20, (y) => -(HA * y - 2 * y * y), (y) => -(HA - 4 * y)));
assert(Math.abs(r.v + HA * HA / 8) < 1e-3); n++;
console.log(`${n} prove superate`);
