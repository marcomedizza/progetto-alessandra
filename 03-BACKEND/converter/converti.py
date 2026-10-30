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
import sys

RADICE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "04-FORTRAN-SOLVER"))
from esegui import SOLUTORE, esegui  # noqa: E402  (modulo di Ottavia)


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


def ordine_nodi(modello):
    """Ordine dei nodi di Cuthill-McKee inverso (Paola, 30/10): riduce la semibanda della matrice del
    solutore, che numera le equazioni nell'ordine dei nodi del file d'ingresso. Senza riordino un modello
    disegnato a mano (nodi aggiunti in coda e collegati ai primi) può avere semibanda vicina al totale."""
    vicini = {n["id"]: set() for n in modello["nodi"]}
    for a in modello["aste"]:
        vicini[a["nodo_i"]].add(a["nodo_j"])
        vicini[a["nodo_j"]].add(a["nodo_i"])
    visti, ordine = set(), []
    for inizio in sorted(vicini, key=lambda n: len(vicini[n])):   # una ricerca per parte connessa
        if inizio in visti:
            continue
        visti.add(inizio)
        coda = [inizio]
        for n in coda:
            ordine.append(n)
            for v in sorted(vicini[n] - visti, key=lambda x: len(vicini[x])):
                visti.add(v)
                coda.append(v)
    return ordine[::-1]


def semibanda(modello, ordine=None):
    """Semibanda in gradi di libertà per un dato ordine dei nodi (per le prove)."""
    pos = {n: i for i, n in enumerate(ordine or [n["id"] for n in modello["nodi"]])}
    return max((3 * abs(pos[a["nodo_i"]] - pos[a["nodo_j"]]) + 2 for a in modello["aste"]), default=0)


def scrivi_input(modello, caso_id):
    caso = next(c for c in modello["casi_di_carico"] if c["id"] == caso_id)
    mat = {m["id"]: m for m in modello["materiali"]}
    sez = {s["id"]: s for s in modello["sezioni"]}
    rigida = not modello.get("analisi", {}).get("deformabilita_assiale", True)
    righe = ["TELAIO2D 1", f"NODI {len(modello['nodi'])}"]
    nodi = {n["id"]: n for n in modello["nodi"]}
    righe += [f"{i} {nodi[i]['x']!r} {nodi[i]['y']!r}" for i in ordine_nodi(modello)]
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
    out = {"spostamenti": [], "reazioni": [], "estremita": {}, "rotazioni_aste": []}
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
        elif p[0] == "ROTAZIONI_ASTE":
            for _ in range(int(p[1])):
                v = next(righe).split()
                out["rotazioni_aste"].append({"asta": int(v[0]), "phi_i": float(v[1]), "phi_j": float(v[2])})
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
    grezzo = leggi_output(esegui(scrivi_input(modello, caso_id)))
    # il solutore scrive i nodi nell'ordine di calcolo: si torna all'ordine del modello
    pos = {n["id"]: i for i, n in enumerate(modello["nodi"])}
    for blocco in ("spostamenti", "reazioni"):
        grezzo[blocco].sort(key=lambda x: pos[x["nodo"]])
    caso = next(c for c in modello["casi_di_carico"] if c["id"] == caso_id)
    cl = carichi_locali(modello, caso)
    geo = _geometria(modello)
    npt = modello.get("analisi", {}).get("punti_diagramma", 11)
    soll = []
    for el in modello["aste"]:
        xs, N, V, M = diagrammi(grezzo["estremita"][el["id"]], cl[el["id"]], geo[el["id"]][0], npt)
        soll.append({"asta": el["id"], "x": xs, "N": N, "V": V, "M": M})
    return {"caso": caso_id, "solutore": "telaio2d Fortran v0.2", "spostamenti": grezzo["spostamenti"],
            "reazioni": grezzo["reazioni"], "rotazioni_aste": grezzo["rotazioni_aste"], "sollecitazioni": soll}


def combina(modello, comb_id):
    """Risultati di una combinazione per sovrapposizione lineare dei casi (schema v1.1, Benedetta/Natalia).
    Valida solo per analisi statica lineare."""
    comb = next(c for c in modello.get("combinazioni", []) if c["id"] == comb_id)
    parti = [(risultati(modello, cid), f) for cid, f in comb["coefficienti"].items()]
    base = parti[0][0]

    def somma(chiave, campi, ident):
        out = []
        for i, el in enumerate(base[chiave]):
            r = {ident: el[ident]}
            for k in campi:
                if isinstance(el[k], list):
                    r[k] = [sum(f * p[chiave][i][k][j] for p, f in parti) for j in range(len(el[k]))]
                else:
                    r[k] = sum(f * p[chiave][i][k] for p, f in parti)
            out.append(r)
        return out

    sol = somma("sollecitazioni", ("N", "V", "M"), "asta")
    for s, b in zip(sol, base["sollecitazioni"]):
        s["x"] = b["x"]
    return {"caso": comb_id, "solutore": base["solutore"] + " (combinazione lineare)",
            "spostamenti": somma("spostamenti", ("ux", "uy", "rz"), "nodo"),
            "reazioni": somma("reazioni", ("Rx", "Ry", "Mz"), "nodo"),
            "rotazioni_aste": somma("rotazioni_aste", ("phi_i", "phi_j"), "asta"),
            "sollecitazioni": [{"asta": s["asta"], "x": s["x"], "N": s["N"], "V": s["V"], "M": s["M"]} for s in sol]}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as fh:
        mod = json.load(fh)
    casi = [sys.argv[2]] if len(sys.argv) > 2 else [c["id"] for c in mod["casi_di_carico"]]
    print(json.dumps([risultati(mod, c) for c in casi], indent=2, ensure_ascii=False))

