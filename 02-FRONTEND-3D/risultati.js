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

export function disegnaRisultati(gruppo, modello, ris, opzioni, S) {
  while (gruppo.children.length) { const o = gruppo.children.pop(); o.geometry?.dispose(); o.material?.dispose(); }
  if (!ris) return;
  if (opzioni.diagramma) disegnaDiagramma(gruppo, modello, ris, opzioni.diagramma, S);
  if (opzioni.deformata) disegnaDeformata(gruppo, modello, ris, S);
}

function disegnaDiagramma(gruppo, modello, ris, comp, S) {
  const max = Math.max(1e-12, ...ris.sollecitazioni.flatMap((s) => s[comp].map(Math.abs)));
  const k = (S * 0.15) / max;
  const segno = comp === 'M' ? -1 : 1;
  const matRiemp = new THREE.MeshBasicMaterial({ color: COLORI[comp], transparent: true, opacity: 0.28, side: THREE.DoubleSide, depthWrite: false });
  const matLinea = new THREE.LineBasicMaterial({ color: COLORI[comp] });
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
  }
}

function disegnaDeformata(gruppo, modello, ris, S) {
  const sp = new Map(ris.spostamenti.map((u) => [u.nodo, u]));
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
    // rotazioni d'estremità: con cerniera interna si usa la corda (approssimazione grafica)
    const corda = (vj - vi) / L;
    const ti = a.svincoli?.rz_i ? corda : ui.rz, tj = a.svincoli?.rz_j ? corda : uj.rz;
    const pts = [];
    for (let i = 0; i <= 20; i++) {
      const x = i / 20, X = x * L;
      // funzioni di forma di Hermite (interpolazione dai soli spostamenti nodali)
      const N1 = 1 - 3 * x * x + 2 * x ** 3, N2 = L * (x - 2 * x * x + x ** 3), N3 = 3 * x * x - 2 * x ** 3, N4 = L * (-x * x + x ** 3);
      const v = N1 * vi + N2 * ti + N3 * vj + N4 * tj;
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
  h += `</tbody></table><p class="nota">Spostamento massimo: nodo ${umax.nodo}, ux = ${fmt(umax.ux * 1000)} mm, uy = ${fmt(umax.uy * 1000)} mm. Unità: kN, kNm. Solutore: ${ris.solutore}.</p>`;
  h += '<p class="nota">La deformata tra i nodi è interpolata con le funzioni di Hermite: è esatta ai nodi, approssimata lungo le aste caricate.</p>';
  return h;
}
