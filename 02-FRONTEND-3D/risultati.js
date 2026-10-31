// Visualizzazione dei risultati (Mariana): deformata e diagrammi N, V, M sulla vista di Irene.
// Convenzioni dello schema v1.0: M positivo se tende le fibre dal lato −y locale,
// quindi il diagramma di M è disegnato dal lato delle fibre tese.
import * as THREE from 'three';

const COLORI = { M: 0x2f5fa7, V: 0x2d7a46, N: 0xc07a1a };

function geometriaAsta(modello, a) {
  const nodi = new Map(modello.nodi.map((n) => [n.id, n]));
  const ni = nodi.get(a.nodo_i), nj = nodi.get(a.nodo_j);
  const dx = nj.x - ni.x, dy = nj.y - ni.y, L = Math.hypot(dx, dy);
  return { ni, nj, L, c: dx / L, s: dy / L };
}

export function disegnaRisultati(gruppo, modello, ris, opzioni, S, caso) {
  while (gruppo.children.length) { const o = gruppo.children.pop(); o.geometry?.dispose(); o.material?.dispose(); }
  if (!ris) return [];
  const etichette = opzioni.diagramma ? disegnaDiagramma(gruppo, modello, ris, opzioni.diagramma, S) : [];
  if (opzioni.deformata) disegnaDeformata(gruppo, modello, ris, S, caso);
  return etichette;
}

const fmtE = (v) => (Math.abs(v) < 5e-3 ? 0 : v).toLocaleString('it-IT', { maximumFractionDigits: Math.abs(v) >= 100 ? 0 : 1 });

// Carichi d'asta in componenti locali trasversali (wy uniforme, Py concentrati, trapezi), come nel convertitore.
function carichiTrasversali(modello, caso, a, c, s) {
  const out = { wy: 0, P: [], T: [] };
  const loc = (dir, v) => (dir === 'globale_y' ? v * c : dir === 'globale_x' ? -v * s : v);
  for (const q of caso?.carichi_aste || []) {
    if (q.asta !== a.id) continue;
    if (q.tipo === 'distribuito_uniforme') out.wy += loc(q.direzione, q.q);
    else if (q.tipo === 'distribuito_trapezio') out.T.push([loc(q.direzione, q.q_i), q.a, loc(q.direzione, q.q_j), q.b]);
    else out.P.push([loc(q.direzione, q.P), q.a]);
  }
  if (caso?.peso_proprio) {
    const m = modello.materiali.find((x) => x.id === a.materiale), se = modello.sezioni.find((x) => x.id === a.sezione);
    if (m?.peso_specifico) out.wy += loc('globale_y', -m.peso_specifico * se.A);
  }
  return out;
}

// Inflessione dell'asta a estremi incastrati sotto i carichi d'asta (soluzione particolare).
// Sommata all'interpolazione di Hermite degli spostamenti nodali dà la deformata esatta
// della trave di Eulero-Bernoulli per aste senza cerniere interne.
function inflessioneIncastrata(X, L, EI, car) {
  // spostamento in X dovuto alla forza P in a, trave incastrata (funzione di Green)
  const green = (P, a) => {
    const b = L - a;
    if (X <= a) return P * b * b * X * X * (3 * a * L - (3 * a + b) * X) / (6 * L ** 3 * EI);
    const Y = L - X;
    return P * a * a * Y * Y * (3 * b * L - (3 * b + a) * Y) / (6 * L ** 3 * EI);
  };
  let v = car.wy * X * X * (L - X) ** 2 / (24 * EI);
  for (const [P, a] of car.P) v += green(P, a);
  // trapezi (v1.1): integrale della funzione di Green per il carico lineare, diviso in X dove la
  // funzione ha il punto angoloso; Gauss a 3 punti, esatto per integrandi di quarto grado
  const g = [-Math.sqrt(0.6), 0, Math.sqrt(0.6)], p = [5 / 9, 8 / 9, 5 / 9];
  for (const [qi, a, qj, b] of car.T || []) {
    for (const [s0, s1] of [[a, Math.min(X, b)], [Math.max(X, a), b]]) {
      if (s1 <= s0) continue;
      const m = (s0 + s1) / 2, h = (s1 - s0) / 2;
      for (let k = 0; k < 3; k++) { const s = m + h * g[k]; v += p[k] * h * green(qi + (qj - qi) * (s - a) / (b - a), s); }
    }
  }
  return v;
}

function disegnaDiagramma(gruppo, modello, ris, comp, S) {
  const max = Math.max(1e-12, ...ris.sollecitazioni.flatMap((s) => s[comp].map(Math.abs)));
  const k = (S * 0.15) / max;
  const segno = comp === 'M' ? -1 : 1;
  const matRiemp = new THREE.MeshBasicMaterial({ color: COLORI[comp], transparent: true, opacity: 0.28, side: THREE.DoubleSide, depthWrite: false });
  const matLinea = new THREE.LineBasicMaterial({ color: COLORI[comp] });
  const etichette = [];
  for (const s of ris.sollecitazioni) {
    const a = modello.aste.find((x) => x.id === s.asta);
    const { ni, c, s: sn } = geometriaAsta(modello, a);
    const asse = (x) => [ni.x + c * x, ni.y + sn * x];
    const punto = (x, v) => { const [px, py] = asse(x); const o = segno * k * v; return [px - sn * o, py + c * o]; };
    const pos = [], curva = [];
    for (let i = 0; i < s.x.length - 1; i++) {
      const a0 = asse(s.x[i]), a1 = asse(s.x[i + 1]);
      const d0 = punto(s.x[i], s[comp][i]), d1 = punto(s.x[i + 1], s[comp][i + 1]);
      pos.push(...a0, 0, ...d0, 0, ...d1, 0, ...a0, 0, ...d1, 0, ...a1, 0);
    }
    for (let i = 0; i < s.x.length; i++) curva.push(...punto(s.x[i], s[comp][i]), 0);
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(pos, 3));
    gruppo.add(new THREE.Mesh(g, matRiemp));
    const gl = new THREE.BufferGeometry();
    gl.setAttribute('position', new THREE.Float32BufferAttribute(curva, 3));
    gruppo.add(new THREE.Line(gl, matLinea));
    // valori alle estremità e, se maggiore, il massimo interno (D3)
    const n = s.x.length, val = s[comp];
    const indici = [0, n - 1];
    let im = 0;
    for (let i = 1; i < n - 1; i++) if (Math.abs(val[i]) > Math.abs(val[im])) im = i;
    if (im > 0 && Math.abs(val[im]) > Math.max(Math.abs(val[0]), Math.abs(val[n - 1])) * 1.01) indici.push(im);
    for (const i of indici) {
      if (Math.abs(val[i]) < max * 0.02) continue;
      const [px, py] = punto(s.x[i], val[i] * 1.15);
      // M in valore assoluto: il lato del diagramma indica già le fibre tese; N e V con il segno
      etichette.push({ x: px, y: py, testo: fmtE(comp === 'M' ? Math.abs(val[i]) : val[i]) });
    }
  }
  return etichette;
}

function disegnaDeformata(gruppo, modello, ris, S, caso) {
  const sp = new Map(ris.spostamenti.map((u) => [u.nodo, u]));
  const rot = new Map((ris.rotazioni_aste || []).map((r) => [r.asta, r]));
  // scala riferita a traslazioni e rotazioni (×S/10): evita amplificazioni enormi quando
  // le traslazioni sono quasi nulle (aste assialmente indeformabili, schemi simmetrici)
  const max = Math.max(1e-12, ...ris.spostamenti.map((u) => Math.max(Math.hypot(u.ux, u.uy), Math.abs(u.rz) * S * 0.1)));
  const k = (S * 0.08) / max;
  const mat = new THREE.LineDashedMaterial({ color: 0x2f5fa7, dashSize: S * 0.015, gapSize: S * 0.01 });
  for (const a of modello.aste) {
    const { ni, L, c, s } = geometriaAsta(modello, a);
    const ui = sp.get(a.nodo_i), uj = sp.get(a.nodo_j);
    // spostamenti locali d'estremità
    const ui_x = c * ui.ux + s * ui.uy, vi = -s * ui.ux + c * ui.uy;
    const uj_x = c * uj.ux + s * uj.uy, vj = -s * uj.ux + c * uj.uy;
    // rotazioni d'estremità dell'asta dal solutore (D8): alla cerniera differiscono da quella del nodo.
    // Senza il dato (risultati di versioni precedenti) si usa la corda, approssimazione grafica.
    const r = rot.get(a.id), corda = (vj - vi) / L;
    const ti = a.svincoli?.rz_i ? (r ? r.phi_i : corda) : ui.rz, tj = a.svincoli?.rz_j ? (r ? r.phi_j : corda) : uj.rz;
    const approssimata = (a.svincoli?.rz_i || a.svincoli?.rz_j) && !r;
    const m = modello.materiali.find((x) => x.id === a.materiale), se = modello.sezioni.find((x) => x.id === a.sezione);
    const car = approssimata ? { wy: 0, P: [] } : carichiTrasversali(modello, caso, a, c, s);
    const pts = [];
    for (let i = 0; i <= 20; i++) {
      const x = i / 20, X = x * L;
      // funzioni di forma di Hermite (interpolazione dai soli spostamenti nodali)
      const N1 = 1 - 3 * x * x + 2 * x ** 3, N2 = L * (x - 2 * x * x + x ** 3), N3 = 3 * x * x - 2 * x ** 3, N4 = L * (-x * x + x ** 3);
      const v = N1 * vi + N2 * ti + N3 * vj + N4 * tj + inflessioneIncastrata(X, L, m.E * se.I, car);
      const u = (1 - x) * ui_x + x * uj_x;
      pts.push(ni.x + c * (X + k * u) - s * k * v, ni.y + s * (X + k * u) + c * k * v, 0);
    }
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(pts, 3));
    const l = new THREE.Line(g, mat);
    l.computeLineDistances();
    gruppo.add(l);
  }
  return k;
}

const fmt = (v, d = 2) => (Math.abs(v) < 5e-13 ? 0 : v).toLocaleString('it-IT', { minimumFractionDigits: d, maximumFractionDigits: d });

export function tabellaRisultati(modello, ris) {
  if (!ris) return '<p class="vuoto">Premi «Calcola».</p>';
  let h = '<table><thead><tr><th>Nodo</th><th class="num">Rx [kN]</th><th class="num">Ry [kN]</th><th class="num">Mz [kNm]</th></tr></thead><tbody>';
  for (const r of ris.reazioni) h += `<tr><td>${r.nodo}</td><td class="num">${fmt(r.Rx)}</td><td class="num">${fmt(r.Ry)}</td><td class="num">${fmt(r.Mz)}</td></tr>`;
  h += '</tbody></table><p></p><table><thead><tr><th>Asta</th><th class="num">|M| max</th><th class="num">|V| max</th><th class="num">|N| max</th></tr></thead><tbody>';
  for (const s of ris.sollecitazioni) {
    const mx = (k) => Math.max(...s[k].map(Math.abs));
    h += `<tr><td>${s.asta}</td><td class="num">${fmt(mx('M'))}</td><td class="num">${fmt(mx('V'))}</td><td class="num">${fmt(mx('N'))}</td></tr>`;
  }
  const umax = ris.spostamenti.reduce((m, u) => (Math.hypot(u.ux, u.uy) > Math.hypot(m.ux, m.uy) ? u : m));
  h += `</tbody></table><p class="nota">Spostamento massimo: nodo ${umax.nodo}, ux = ${fmt(umax.ux * 1000)} mm, uy = ${fmt(umax.uy * 1000)} mm. Unità: kN, kNm. Solutore: ${String(ris.solutore).replace(/[<>&]/g, '')}.</p>`;
  h += '<p class="nota">Deformata esatta lungo le aste: spostamenti e rotazioni d\'estremità, comprese quelle alle cerniere interne, più l\'inflessione dei carichi d\'asta.</p>';
  return h;
}
