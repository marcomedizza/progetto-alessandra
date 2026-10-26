"""Convertitore tra modello JSON (schema v1.0) e solutore Fortran telaio2d (Paola).

- `scrivi_input(modello, caso)`  → testo del file di ingresso ASCII del solutore
- `leggi_output(testo)`          → spostamenti, reazioni, forze d'estremità
- `risultati(modello, caso)`     → esegue il solutore e restituisce il blocco
                                   «risultati» dello schema, con N-V-M lungo le aste

Uso da riga di comando:
    python3 converti.py modello.json [caso]     → stampa i risultati JSON

Il solutore deve essere compilato con 04-FORTRAN-SOLVER/build.sh.
"""

import json
import math
import os
import subprocess
import sys
import tempfile

RADICE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SOLUTORE = os.environ.get("TELAIO2D_BIN", os.path.join(RADICE, "04-FORTRAN-SOLVER", "bin", "telaio2d"))


def _geometria(modello):
    nodi = {n["id"]: n for n in modello["nodi"]}
    geo = {}
    for el in modello["aste"]:
        ni, nj = nodi[el["nodo_i"]], nodi[el["nodo_j"]]
        dx, dy = nj["x"] - ni["x"], nj["y"] - ni["y"]
        L = math.hypot(dx, dy)
        geo[el["id"]] = (L, dx / L, dy / L)
    return geo


def carichi_locali(modello, caso):
    """Carichi d'asta in componenti locali: {asta: [(tipo, wx, wy, a)]}, tipo 1 uniforme, 2 concentrato."""
    geo = _geometria(modello)
    mat = {m["id"]: m for m in modello["materiali"]}
    sez = {s["id"]: s for s in modello["sezioni"]}
    out = {el["id"]: [] for el in modello["aste"]}

    def locale(direzione, v, c, s):
        if direzione == "globale_y":
            return v * s, v * c
        if direzione == "globale_x":
            return v * c, -v * s
        return 0.0, v

    for q in caso.get("carichi_aste", []):
        L, c, s = geo[q["asta"]]
        if q["tipo"] == "distribuito_uniforme":
            wx, wy = locale(q["direzione"], q["q"], c, s)
            out[q["asta"]].append((1, wx, wy, 0.0))
        else:
            wx, wy = locale(q["direzione"], q["P"], c, s)
            out[q["asta"]].append((2, wx, wy, q["a"]))
    if caso.get("peso_proprio"):
        for el in modello["aste"]:
            g = mat[el["materiale"]].get("peso_specifico")
            if g:
                L, c, s = geo[el["id"]]
                wx, wy = locale("globale_y", -g * sez[el["sezione"]]["A"], c, s)
                out[el["id"]].append((1, wx, wy, 0.0))
    return out


def scrivi_input(modello, caso_id):
    caso = next(c for c in modello["casi_di_carico"] if c["id"] == caso_id)
    mat = {m["id"]: m for m in modello["materiali"]}
    sez = {s["id"]: s for s in modello["sezioni"]}
    rigida = not modello.get("analisi", {}).get("deformabilita_assiale", True)
    righe = ["TELAIO2D 1", f"NODI {len(modello['nodi'])}"]
    righe += [f"{n['id']} {n['x']!r} {n['y']!r}" for n in modello["nodi"]]
    righe.append(f"ASTE {len(modello['aste'])}")
    for el in modello["aste"]:
        A = sez[el["sezione"]]["A"] * (1e6 if rigida else 1.0)
        sv = el.get("svincoli", {})
        righe.append(f"{el['id']} {el['nodo_i']} {el['nodo_j']} {mat[el['materiale']]['E']!r} {A!r} "
                     f"{sez[el['sezione']]['I']!r} {int(bool(sv.get('rz_i')))} {int(bool(sv.get('rz_j')))}")
    righe.append(f"VINCOLI {len(modello['vincoli'])}")
    for v in modello["vincoli"]:
        m = v.get("molle", {})
        righe.append(f"{v['nodo']} {int(bool(v.get('ux')))} {int(bool(v.get('uy')))} {int(bool(v.get('rz')))} "
                     f"{float(m.get('kx', 0))!r} {float(m.get('ky', 0))!r} {float(m.get('kr', 0))!r}")
    cn = caso.get("carichi_nodali", [])
    righe.append(f"CARICHI_NODALI {len(cn)}")
    righe += [f"{q['nodo']} {float(q.get('Fx', 0))!r} {float(q.get('Fy', 0))!r} {float(q.get('Mz', 0))!r}" for q in cn]
    cl = carichi_locali(modello, caso)
    tutte = [(a, *q) for a, lst in cl.items() for q in lst]
    righe.append(f"CARICHI_ASTE {len(tutte)}")
    righe += [f"{a} {t} {wx!r} {wy!r} {pa!r}" for a, t, wx, wy, pa in tutte]
    righe.append("FINE")
    return "\n".join(righe) + "\n"


def leggi_output(testo):
    out = {"spostamenti": [], "reazioni": [], "estremita": {}}
    righe = iter(testo.split("\n"))
    for r in righe:
        p = r.split()
        if not p:
            continue
        if p[0] == "SPOSTAMENTI":
            for _ in range(int(p[1])):
                v = next(righe).split()
                out["spostamenti"].append({"nodo": int(v[0]), "ux": float(v[1]), "uy": float(v[2]), "rz": float(v[3])})
        elif p[0] == "REAZIONI":
            for _ in range(int(p[1])):
                v = next(righe).split()
                out["reazioni"].append({"nodo": int(v[0]), "Rx": float(v[1]), "Ry": float(v[2]), "Mz": float(v[3])})
        elif p[0] == "ESTREMITA":
            for _ in range(int(p[1])):
                v = next(righe).split()
                out["estremita"][int(v[0])] = [float(x) for x in v[1:7]]
    return out


def diagrammi(f, carichi, L, npt):
    """N, V, M lungo l'asta dalle forze d'estremità locali e dai carichi locali (convenzioni dello schema)."""
    xs = [L * k / (npt - 1) for k in range(npt)]
    N, V, M = [], [], []
    for x in xs:
        n, v, m = -f[0], f[1], -f[2] + x * f[1]
        for t, wx, wy, a in carichi:
            if t == 1:
                n -= wx * x
                v += wy * x
                m += wy * x * x / 2
            elif a < x - 1e-9:
                n -= wx
                v += wy
                m += wy * (x - a)
        N.append(n)
        V.append(v)
        M.append(m)
    return xs, N, V, M


def risultati(modello, caso_id):
    if not os.path.exists(SOLUTORE):
        raise FileNotFoundError(f"solutore non compilato: {SOLUTORE} (eseguire 04-FORTRAN-SOLVER/build.sh)")
    with tempfile.TemporaryDirectory() as d:
        fin, fout = os.path.join(d, "input.txt"), os.path.join(d, "output.txt")
        with open(fin, "w") as fh:
            fh.write(scrivi_input(modello, caso_id))
        esito = subprocess.run([SOLUTORE, fin, fout], capture_output=True, text=True)
        if esito.returncode != 0:
            raise RuntimeError(esito.stderr.strip() or "errore del solutore")
        with open(fout) as fh:
            grezzo = leggi_output(fh.read())
    caso = next(c for c in modello["casi_di_carico"] if c["id"] == caso_id)
    cl = carichi_locali(modello, caso)
    geo = _geometria(modello)
    npt = modello.get("analisi", {}).get("punti_diagramma", 11)
    soll = []
    for el in modello["aste"]:
        xs, N, V, M = diagrammi(grezzo["estremita"][el["id"]], cl[el["id"]], geo[el["id"]][0], npt)
        soll.append({"asta": el["id"], "x": xs, "N": N, "V": V, "M": M})
    return {"caso": caso_id, "solutore": "telaio2d Fortran v0.1", "spostamenti": grezzo["spostamenti"],
            "reazioni": grezzo["reazioni"], "sollecitazioni": soll}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as fh:
        mod = json.load(fh)
    casi = [sys.argv[2]] if len(sys.argv) > 2 else [c["id"] for c in mod["casi_di_carico"]]
    print(json.dumps([risultati(mod, c) for c in casi], indent=2, ensure_ascii=False))
