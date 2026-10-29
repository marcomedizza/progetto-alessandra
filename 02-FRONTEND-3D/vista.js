// Vista 3D del telaio (Irene): scena, telecamere, aste, nodi, vincoli, carichi, selezione.
import * as THREE from 'three';
import { OrbitControls } from './vendor/OrbitControls.js';

const COL = {
  asta: 0x3b4654, astaSel: 0xd9822b, nodo: 0x1d232b, vincolo: 0x6b7480,
  carico: 0xb23a2a, deformata: 0x2f5fa7, griglia: 0xd5d9df,
};

export class Vista {
  constructor(contenitore, onSeleziona) {
    this.box = contenitore;
    this.onSeleziona = onSeleziona;
    this.renderer = new THREE.WebGLRenderer({ antialias: true });
    this.renderer.setPixelRatio(window.devicePixelRatio);
    this.renderer.setClearColor(0xf7f8fa);
    contenitore.appendChild(this.renderer.domElement);
    this.scene = new THREE.Scene();
    this.camera = new THREE.OrthographicCamera(-1, 1, 1, -1, -1000, 1000);
    this.controlli = new OrbitControls(this.camera, this.renderer.domElement);
    this.controlli.enableDamping = false;
    this.gruppoModello = new THREE.Group();
    this.gruppoRisultati = new THREE.Group();
    this.scene.add(this.gruppoModello, this.gruppoRisultati);
    this.scene.add(new THREE.AmbientLight(0xffffff, 1.0));
    this.raycaster = new THREE.Raycaster();
    this.selezionabili = [];
    this.vistaCorrente = 'frontale';
    this.S = 1;
    this.etichette = [];
    this.strato = document.createElement('div');
    this.strato.className = 'strato-etichette';
    contenitore.appendChild(this.strato);
    this.centro = new THREE.Vector3();
    new ResizeObserver(() => this.ridimensiona()).observe(contenitore);
    this.renderer.domElement.addEventListener('pointerdown', (e) => { this._giu = [e.clientX, e.clientY]; });
    this.renderer.domElement.addEventListener('pointerup', (e) => {
      if (this._giu && Math.hypot(e.clientX - this._giu[0], e.clientY - this._giu[1]) < 4) this.clic(e);
    });
    const ciclo = () => {
      this.controlli.update();
      this.renderer.render(this.scene, this.camera);
      this.posizionaEtichette();
      requestAnimationFrame(ciclo);
    };
    ciclo();
  }

  // Etichette numeriche dei diagrammi (Mariana, D3): elementi HTML posizionati sul punto 3D a ogni fotogramma.
  impostaEtichette(lista) {
    this.strato.replaceChildren();
    this.etichette = lista.map(({ x, y, testo }) => {
      const el = document.createElement('span');
      el.className = 'etichetta';
      el.textContent = testo;
      this.strato.appendChild(el);
      return { pos: new THREE.Vector3(x, y, 0), el };
    });
  }

  posizionaEtichette() {
    if (!this.etichette.length) return;
    const w = this.renderer.domElement.clientWidth, h = this.renderer.domElement.clientHeight;
    const v = new THREE.Vector3();
    for (const e of this.etichette) {
      v.copy(e.pos).project(this.camera);
      e.el.style.transform = `translate(${((v.x + 1) / 2) * w}px, ${((1 - v.y) / 2) * h}px) translate(-50%, -50%)`;
    }
  }

  ridimensiona() {
    const w = this.box.clientWidth, h = this.box.clientHeight;
    if (!w || !h) return;
    this.renderer.setSize(w, h);
    const a = w / h, m = this.S * 0.85;
    this.camera.left = -m * a; this.camera.right = m * a; this.camera.top = m; this.camera.bottom = -m;
    this.camera.updateProjectionMatrix();
  }

  svuota(g) {
    while (g.children.length) {
      const o = g.children.pop();
      o.traverse?.((x) => { x.geometry?.dispose(); x.material?.dispose?.(); });
    }
  }

  disegna(modello, caso, selezione) {
    this.svuota(this.gruppoModello);
    this.selezionabili = [];
    const nodi = new Map(modello.nodi.map((n) => [n.id, n]));
    const xs = modello.nodi.map((n) => n.x), ys = modello.nodi.map((n) => n.y);
    const minx = Math.min(...xs), maxx = Math.max(...xs), miny = Math.min(...ys), maxy = Math.max(...ys);
    this.S = Math.max(maxx - minx, maxy - miny, 1);
    this.centro.set((minx + maxx) / 2, (miny + maxy) / 2, 0);
    const S = this.S;

    // aste
    for (const a of modello.aste) {
      const ni = nodi.get(a.nodo_i), nj = nodi.get(a.nodo_j);
      const p1 = new THREE.Vector3(ni.x, ni.y, 0), p2 = new THREE.Vector3(nj.x, nj.y, 0);
      const L = p1.distanceTo(p2);
      const sel = selezione?.tipo === 'asta' && selezione.id === a.id;
      const m = new THREE.Mesh(new THREE.CylinderGeometry(S * 0.006, S * 0.006, L, 8),
        new THREE.MeshBasicMaterial({ color: sel ? COL.astaSel : COL.asta }));
      m.position.copy(p1).add(p2).multiplyScalar(0.5);
      m.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), p2.clone().sub(p1).normalize());
      this.gruppoModello.add(m);
      // cilindro invisibile più largo per la selezione col mouse, ruotato di 30° perché nessuno spigolo cada sul piano del telaio
      const presa = new THREE.Mesh(new THREE.CylinderGeometry(S * 0.025, S * 0.025, L, 6, 1, false, Math.PI / 6), new THREE.MeshBasicMaterial({ visible: false }));
      presa.position.copy(m.position); presa.quaternion.copy(m.quaternion);
      presa.userData = { tipo: 'asta', id: a.id };
      this.gruppoModello.add(presa);
      this.selezionabili.push(presa);
      for (const [lato, rel] of [['i', a.svincoli?.rz_i], ['j', a.svincoli?.rz_j]]) {
        if (!rel) continue;
        const p = lato === 'i' ? p1.clone().lerp(p2, 0.04) : p2.clone().lerp(p1, 0.04);
        const c = new THREE.Mesh(new THREE.RingGeometry(S * 0.008, S * 0.013, 20), new THREE.MeshBasicMaterial({ color: COL.asta }));
        c.position.copy(p);
        this.gruppoModello.add(c);
      }
    }
    // nodi
    for (const n of modello.nodi) {
      const sel = selezione?.tipo === 'nodo' && selezione.id === n.id;
      const m = new THREE.Mesh(new THREE.SphereGeometry(S * (sel ? 0.018 : 0.012), 16, 12),
        new THREE.MeshBasicMaterial({ color: sel ? COL.astaSel : COL.nodo }));
      m.position.set(n.x, n.y, 0);
      this.gruppoModello.add(m);
      // sfera invisibile più grande per facilitare la selezione col mouse
      const presa = new THREE.Mesh(new THREE.SphereGeometry(S * 0.035, 8, 6), new THREE.MeshBasicMaterial({ visible: false }));
      presa.position.set(n.x, n.y, 0);
      presa.userData = { tipo: 'nodo', id: n.id };
      this.gruppoModello.add(presa);
      this.selezionabili.push(presa);
    }
    // vincoli
    for (const v of modello.vincoli) this.gruppoModello.add(this.simboloVincolo(nodi.get(v.nodo), v));
    // carichi del caso
    if (caso) this.disegnaCarichi(modello, caso, nodi);
    // griglia di riferimento a terra
    const g = new THREE.GridHelper(S * 2, 20, COL.griglia, COL.griglia);
    g.position.set(this.centro.x, miny - S * 0.08, 0);
    this.gruppoModello.add(g);
    this.ridimensiona();
  }

  simboloVincolo(n, v) {
    const S = this.S, g = new THREE.Group(), mat = new THREE.MeshBasicMaterial({ color: COL.vincolo, side: THREE.DoubleSide });
    const d = S * 0.035;
    if (v.ux && v.uy && v.rz) {                    // incastro
      const r = new THREE.Mesh(new THREE.PlaneGeometry(d * 2.4, d * 0.5), mat);
      r.position.set(n.x, n.y - d * 0.25, 0);
      g.add(r);
    } else if (v.uy || v.ux) {                     // cerniera o carrello
      const sh = new THREE.Shape([new THREE.Vector2(0, 0), new THREE.Vector2(-d, -d * 1.4), new THREE.Vector2(d, -d * 1.4)]);
      const t = new THREE.Mesh(new THREE.ShapeGeometry(sh), mat);
      t.position.set(n.x, n.y, 0);
      if (!v.uy) t.rotation.z = -Math.PI / 2;      // vincolo solo orizzontale
      g.add(t);
      if (!(v.ux && v.uy)) {                        // carrello: linea sotto
        const l = new THREE.Mesh(new THREE.PlaneGeometry(d * 2.4, d * 0.15), mat);
        l.position.set(n.x, n.y - d * 1.7, 0);
        if (!v.uy) { l.rotation.z = -Math.PI / 2; l.position.set(n.x + d * 1.7, n.y, 0); }
        g.add(l);
      }
    }
    if (v.molle && (v.molle.kx || v.molle.ky || v.molle.kr)) {
      const m = new THREE.Mesh(new THREE.TorusGeometry(d * 0.6, d * 0.12, 6, 16), mat);
      m.position.set(n.x + d * 1.2, n.y - d * 0.6, 0);
      g.add(m);
    }
    return g;
  }

  freccia(da, dir, lung) {
    return new THREE.ArrowHelper(dir.clone().normalize(), da, lung, COL.carico, lung * 0.3, lung * 0.18);
  }

  disegnaCarichi(modello, caso, nodi) {
    const S = this.S, Lf = S * 0.1;
    for (const q of caso.carichi_nodali || []) {
      const n = nodi.get(q.nodo), p = new THREE.Vector3(n.x, n.y, 0);
      if (q.Fx) { const d = new THREE.Vector3(Math.sign(q.Fx), 0, 0); this.gruppoModello.add(this.freccia(p.clone().sub(d.clone().multiplyScalar(Lf)), d, Lf)); }
      if (q.Fy) { const d = new THREE.Vector3(0, Math.sign(q.Fy), 0); this.gruppoModello.add(this.freccia(p.clone().sub(d.clone().multiplyScalar(Lf)), d, Lf)); }
      if (q.Mz) {
        const t = new THREE.Mesh(new THREE.TorusGeometry(S * 0.04, S * 0.004, 6, 24, Math.PI * 1.5),
          new THREE.MeshBasicMaterial({ color: COL.carico }));
        t.position.copy(p);
        this.gruppoModello.add(t);
      }
    }
    const aste = new Map(modello.aste.map((a) => [a.id, a]));
    for (const q of caso.carichi_aste || []) {
      const a = aste.get(q.asta), ni = nodi.get(a.nodo_i), nj = nodi.get(a.nodo_j);
      const p1 = new THREE.Vector3(ni.x, ni.y, 0), p2 = new THREE.Vector3(nj.x, nj.y, 0);
      const ax = p2.clone().sub(p1).normalize(), ny = new THREE.Vector3(-ax.y, ax.x, 0);
      const val = q.tipo === 'distribuito_uniforme' ? q.q : q.P;
      const dirBase = q.direzione === 'globale_y' ? new THREE.Vector3(0, 1, 0)
        : q.direzione === 'globale_x' ? new THREE.Vector3(1, 0, 0) : ny;
      const d = dirBase.clone().multiplyScalar(Math.sign(val));
      const posizioni = q.tipo === 'distribuito_uniforme' ? [...Array(9).keys()].map((k) => k / 8) : [q.a / p1.distanceTo(p2)];
      const l = q.tipo === 'distribuito_uniforme' ? Lf * 0.6 : Lf;
      for (const t of posizioni) {
        const p = p1.clone().lerp(p2, t);
        this.gruppoModello.add(this.freccia(p.clone().sub(d.clone().multiplyScalar(l)), d, l));
      }
    }
  }

  vista(nome) {
    this.vistaCorrente = nome;
    const c = this.centro, D = this.S * 5;
    this.camera.up.set(0, 1, 0);
    if (nome === 'frontale') this.camera.position.set(c.x, c.y, D);
    else if (nome === 'alto') { this.camera.position.set(c.x, c.y + D, 0.0001); this.camera.up.set(0, 0, -1); }
    else this.camera.position.set(c.x + D * 0.6, c.y + D * 0.5, D * 0.8);
    this.controlli.target.copy(c);
    this.controlli.enableRotate = nome === 'asso';
    this.camera.zoom = 1;
    this.camera.updateProjectionMatrix();
    this.controlli.update();
  }

  clic(e) {
    const r = this.renderer.domElement.getBoundingClientRect();
    const v = new THREE.Vector2(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1);
    this.raycaster.setFromCamera(v, this.camera);
    const hit = this.raycaster.intersectObjects(this.selezionabili, false);
    // i nodi hanno la precedenza sulle aste quando sono entrambi colpiti
    const scelto = hit.find((h) => h.object.userData.tipo === 'nodo') || hit[0];
    this.onSeleziona(scelto ? scelto.object.userData : null);
  }
}
