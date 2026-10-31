"""Risolutore di riferimento per telai piani, statica lineare (metodo degli spostamenti).

Serve a calcolare e controllare i risultati attesi dei casi di prova e a
confrontarli con il solutore Fortran. Non è il solutore del programma.

Ipotesi: travi di Eulero-Bernoulli, piccoli spostamenti, materiale elastico
lineare. Unità coerenti dello schema dati v1.0: m, kN, kN/m², kNm.

Convenzioni (identiche a 01-ARCHITETTURA/DATA_SCHEMA.json):
- riferimento globale X verso destra, Y verso l'alto, rotazioni antiorarie positive;
- asse locale x dal nodo_i al nodo_j, y locale ruotato di +90°;
- N positivo di trazione; M positivo se tende le fibre dal lato −y locale
  (fibre inferiori di un'asta orizzontale con nodo_i a sinistra); V = dM/dx.

Uso:  python3 telaio2d.py modello.json [caso]
Senza dipendenze esterne.
"""

import json
import math
import sys


# ---------------------------------------------------------------- algebra

def risolvi(A, b):
    """Eliminazione di Gauss con pivot parziale. A n×n, b vettore."""
    n = len(b)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c]))
        if abs(M[p][c]) < 1e-12 * max(1.0, max(abs(M[r][c]) for r in range(n))):
            raise ValueError("Matrice di rigidezza singolare: struttura labile o vincoli insufficienti")
        M[c], M[p] = M[p], M[c]
        for r in range(c + 1, n):
            f = M[r][c] / M[c][c]
            if f:
                for k in range(c, n + 1):
                    M[r][k] -= f * M[c][k]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        x[r] = (M[r][n] - sum(M[r][k] * x[k] for k in range(r + 1, n))) / M[r][r]
    return x


def matvec(A, x):
    return [sum(a * b for a, b in zip(row, x)) for row in A]


# ---------------------------------------------------------------- elemento

def rigidezza_locale(E, A, I, L):
    a = E * A / L
    b = 12 * E * I / L ** 3
    c = 6 * E * I / L ** 2
    d = 4 * E * I / L
    e = 2 * E * I / L
    return [
        [a, 0, 0, -a, 0, 0],
        [0, b, c, 0, -b, c],
        [0, c, d, 0, -c, e],
        [-a, 0, 0, a, 0, 0],
        [0, -b, -c, 0, b, -c],
        [0, c, e, 0, -c, d],
    ]


def rotazione(c, s):
    return [
        [c, s, 0, 0, 0, 0],
        [-s, c, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, c, s, 0],
        [0, 0, 0, -s, c, 0],
        [0, 0, 0, 0, 0, 1],
    ]


def trasposta(T):
    return [list(r) for r in zip(*T)]


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def carichi_locali(carichi, c, s):
    """Converte i carichi d'asta in componenti locali.
    Restituisce lista di ('u', wx, wy) per uniformi, ('p', Px, Py, a) per concentrati e
    ('t', wxi, wyi, a, wxj, wyj, b) per i trapezoidali (v1.1)."""
    def locale(direzione, v):
        if direzione == "globale_y":
            return v * s, v * c
        if direzione == "globale_x":
            return v * c, -v * s
        return 0.0, v

    out = []
    for q in carichi:
        if q["tipo"] == "distribuito_trapezio":
            out.append(("t", *locale(q["direzione"], q["q_i"]), q["a"], *locale(q["direzione"], q["q_j"]), q["b"]))
        elif q["tipo"] == "distribuito_uniforme":
            v = q["q"]
            if q["direzione"] == "globale_y":
                out.append(("u", v * s, v * c))
            elif q["direzione"] == "globale_x":
                out.append(("u", v * c, -v * s))
            else:
                out.append(("u", 0.0, v))
        else:
            v = q["P"]
            if q["direzione"] == "globale_y":
                out.append(("p", v * s, v * c, q["a"]))
            elif q["direzione"] == "globale_x":
                out.append(("p", v * c, -v * s, q["a"]))
            else:
                out.append(("p", 0.0, v, q["a"]))
    return out


def forze_incastro(cl, L):
    """Forze d'estremità (agenti sull'asta) con estremi incastrati, riferimento locale."""
    f = [0.0] * 6
    for q in cl:
        if q[0] == "t":
            # f = −∫ N(x)·w(x) dx sul tratto [a, b], con le funzioni di forma della trave;
            # Gauss a 3 punti, esatto per N cubica × w lineare
            wxi, wyi, a, wxj, wyj, b = q[1:]
            if not 0 <= a < b <= L + 1e-9:
                raise ValueError("Carico trapezoidale fuori dall'asta")
            m, h = (a + b) / 2, (b - a) / 2
            for t, p in ((-math.sqrt(0.6), 5 / 9), (0.0, 8 / 9), (math.sqrt(0.6), 5 / 9)):
                x = m + h * t
                r = (x - a) / (b - a)
                wx, wy = wxi + (wxj - wxi) * r, wyi + (wyj - wyi) * r
                xi = x / L
                N = (1 - 3 * xi ** 2 + 2 * xi ** 3, L * (xi - 2 * xi ** 2 + xi ** 3), 3 * xi ** 2 - 2 * xi ** 3, L * (-xi ** 2 + xi ** 3))
                f[0] -= p * h * wx * (1 - xi)
                f[3] -= p * h * wx * xi
                f[1] -= p * h * wy * N[0]
                f[2] -= p * h * wy * N[1]
                f[4] -= p * h * wy * N[2]
                f[5] -= p * h * wy * N[3]
        elif q[0] == "u":
            wx, wy = q[1], q[2]
            f[0] += -wx * L / 2
            f[3] += -wx * L / 2
            f[1] += -wy * L / 2
            f[4] += -wy * L / 2
            f[2] += -wy * L ** 2 / 12
            f[5] += wy * L ** 2 / 12
        else:
            Px, Py, a = q[1], q[2], q[3]
            if not 0 <= a <= L:
                raise ValueError("Carico concentrato fuori dall'asta")
            b = L - a
            f[0] += -Px * b / L
            f[3] += -Px * a / L
            f[1] += -Py * b ** 2 * (3 * a + b) / L ** 3
            f[4] += -Py * a ** 2 * (a + 3 * b) / L ** 3
            f[2] += -Py * a * b ** 2 / L ** 2
            f[5] += Py * a ** 2 * b / L ** 2
    return f


def condensa(k, f, rilasciati):
    """Condensazione statica dei gradi di libertà rilasciati (cerniere interne).
    Restituisce k e f modificati sui gdl trattenuti (righe e colonne rilasciate a zero)."""
    if not rilasciati:
        return k, f
    R = rilasciati
    C = [i for i in range(6) if i not in R]
    KRR = [[k[i][j] for j in R] for i in R]
    k2 = [[0.0] * 6 for _ in range(6)]
    f2 = [0.0] * 6
    # KRR^-1 colonna per colonna
    inv = [risolvi(KRR, [1.0 if r == j else 0.0 for r in range(len(R))]) for j in range(len(R))]
    inv = trasposta(inv)
    for a in C:
        for b in C:
            corr = sum(k[a][R[p]] * inv[p][q] * k[R[q]][b] for p in range(len(R)) for q in range(len(R)))
            k2[a][b] = k[a][b] - corr
        f2[a] = f[a] - sum(k[a][R[p]] * inv[p][q] * f[R[q]] for p in range(len(R)) for q in range(len(R)))
    return k2, f2


# ---------------------------------------------------------------- analisi

def analizza(modello, caso_id, punti=None):
    nodi = {n["id"]: n for n in modello["nodi"]}
    mat = {m["id"]: m for m in modello["materiali"]}
    sez = {s["id"]: s for s in modello["sezioni"]}
    ids = sorted(nodi)
    idx = {nid: i for i, nid in enumerate(ids)}
    ndof = 3 * len(ids)
    analisi = modello.get("analisi", {})
    rigida = not analisi.get("deformabilita_assiale", True)
    npt = punti or analisi.get("punti_diagramma", 11)

    caso = next(c for c in modello["casi_di_carico"] if c["id"] == caso_id)
    carichi_per_asta = {}
    for q in caso.get("carichi_aste", []):
        carichi_per_asta.setdefault(q["asta"], []).append(q)

    K = [[0.0] * ndof for _ in range(ndof)]
    F = [0.0] * ndof
    dati = []
    for el in modello["aste"]:
        ni, nj = nodi[el["nodo_i"]], nodi[el["nodo_j"]]
        dx, dy = nj["x"] - ni["x"], nj["y"] - ni["y"]
        L = math.hypot(dx, dy)
        if L <= 0:
            raise ValueError(f"Asta {el['id']} di lunghezza nulla")
        c, s = dx / L, dy / L
        m, se = mat[el["materiale"]], sez[el["sezione"]]
        A = se["A"] * (1e6 if rigida else 1.0)
        kl = rigidezza_locale(m["E"], A, se["I"], L)
        carichi = list(carichi_per_asta.get(el["id"], []))
        if caso.get("peso_proprio") and m.get("peso_specifico"):
            carichi.append({"tipo": "distribuito_uniforme", "direzione": "globale_y", "q": -m["peso_specifico"] * se["A"]})
        cl = carichi_locali(carichi, c, s)
        ff = forze_incastro(cl, L)
        sv = el.get("svincoli", {})
        ril = ([2] if sv.get("rz_i") else []) + ([5] if sv.get("rz_j") else [])
        kc, fc = condensa(kl, ff, ril)
        T = rotazione(c, s)
        Tt = trasposta(T)
        kg = matmul(matmul(Tt, kc), T)
        fg = matvec(Tt, fc)
        dofs = [3 * idx[el["nodo_i"]] + r for r in range(3)] + [3 * idx[el["nodo_j"]] + r for r in range(3)]
        for a in range(6):
            F[dofs[a]] -= fg[a]
            for b in range(6):
                K[dofs[a]][dofs[b]] += kg[a][b]
        dati.append(dict(el=el, L=L, T=T, kl=kl, kc=kc, ff=ff, fc=fc, ril=ril, cl=cl, dofs=dofs))

    for q in caso.get("carichi_nodali", []):
        i = 3 * idx[q["nodo"]]
        F[i] += q.get("Fx", 0.0)
        F[i + 1] += q.get("Fy", 0.0)
        F[i + 2] += q.get("Mz", 0.0)

    vincolati = set()
    molle = {}
    for v in modello["vincoli"]:
        i = 3 * idx[v["nodo"]]
        for r, nome in enumerate(("ux", "uy", "rz")):
            if v.get(nome):
                vincolati.add(i + r)
        for r, nome in enumerate(("kx", "ky", "kr")):
            kv = v.get("molle", {}).get(nome)
            if kv:
                molle[i + r] = kv
    Ks = [row[:] for row in K]
    for d, kv in molle.items():
        Ks[d][d] += kv

    # cedimenti impressi (v1.1): spostamenti noti sui gdl vincolati, portati a secondo membro
    u = [0.0] * ndof
    for d in caso.get("cedimenti", []):
        i = 3 * idx[d["nodo"]]
        for r, nome in enumerate(("ux", "uy", "rz")):
            if d.get(nome):
                if i + r not in vincolati:
                    raise ValueError(f"cedimento {nome} sul nodo {d['nodo']} non vincolato")
                u[i + r] = d[nome]
    liberi = [d for d in range(ndof) if d not in vincolati]
    Kff = [[Ks[a][b] for b in liberi] for a in liberi]
    uf = risolvi(Kff, [F[a] - sum(Ks[a][c] * u[c] for c in vincolati) for a in liberi])
    for a, val in zip(liberi, uf):
        u[a] = val

    Ku = matvec(K, u)
    reaz = {}
    for d in sorted(vincolati | set(molle)):
        reaz[d] = Ku[d] - F[d]

    out = {"caso": caso_id, "solutore": "telaio2d.py (riferimento)", "spostamenti": [], "reazioni": [], "sollecitazioni": []}
    for nid in ids:
        i = 3 * idx[nid]
        out["spostamenti"].append({"nodo": nid, "ux": u[i], "uy": u[i + 1], "rz": u[i + 2]})
        if any(i + r in reaz for r in range(3)):
            out["reazioni"].append({"nodo": nid, "Rx": reaz.get(i, 0.0), "Ry": reaz.get(i + 1, 0.0), "Mz": reaz.get(i + 2, 0.0)})

    out["rotazioni_aste"] = []
    for d in dati:
        ul = matvec(d["T"], [u[k] for k in d["dofs"]])
        # rotazioni svincolate (D8): momenti d'estremità nulli sull'asta non condensata
        R = d["ril"]
        if R:
            for r in R:
                ul[r] = 0.0
            b = [-(sum(d["kl"][r][c] * ul[c] for c in range(6)) + d["ff"][r]) for r in R]
            th = risolvi([[d["kl"][r][c] for c in R] for r in R], b)
            for r, t in zip(R, th):
                ul[r] = t
        out["rotazioni_aste"].append({"asta": d["el"]["id"], "phi_i": ul[2], "phi_j": ul[5]})

    for d in dati:
        ug = [u[k] for k in d["dofs"]]
        ul = matvec(d["T"], ug)
        f = [a + b for a, b in zip(matvec(d["kc"], ul), d["fc"])]
        L = d["L"]
        xs = [L * k / (npt - 1) for k in range(npt)]
        Ns, Vs, Ms = [], [], []
        for x in xs:
            N = -f[0]
            V = f[1]
            M = -f[2] + x * f[1]
            for q in d["cl"]:
                if q[0] == "t":
                    wxi, wyi, a, wxj, wyj, b = q[1:]
                    if x > a:
                        cc = min(x, b)
                        w = lambda y, wi, wj: wi + (wj - wi) * (y - a) / (b - a)  # noqa: E731
                        # Simpson sul tratto [a, cc]: esatto per integrandi quadratici
                        for wi, wj, comp in ((wxi, wxj, "x"), (wyi, wyj, "y")):
                            W = (cc - a) * (w(a, wi, wj) + w(cc, wi, wj)) / 2
                            if comp == "x":
                                N -= W
                            else:
                                V += W
                                ym = (a + cc) / 2
                                M += (cc - a) / 6 * (w(a, wi, wj) * (x - a) + 4 * w(ym, wi, wj) * (x - ym) + w(cc, wi, wj) * (x - cc))
                elif q[0] == "u":
                    N -= q[1] * x
                    V += q[2] * x
                    M += q[2] * x * x / 2
                elif q[3] < x - 1e-9:  # carico concentrato a sinistra della sezione (valore a sinistra del punto di applicazione)
                    N -= q[1]
                    V += q[2]
                    M += q[2] * (x - q[3])
            Ns.append(N)
            Vs.append(V)
            Ms.append(M)
        out["sollecitazioni"].append({"asta": d["el"]["id"], "x": xs, "N": Ns, "V": Vs, "M": Ms})
    return out


def principale(argv):
    if len(argv) < 2:
        print(__doc__)
        return 1
    with open(argv[1], encoding="utf-8") as fh:
        modello = json.load(fh)
    casi = [argv[2]] if len(argv) > 2 else [c["id"] for c in modello["casi_di_carico"]]
    print(json.dumps([analizza(modello, c) for c in casi], indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(principale(sys.argv))
