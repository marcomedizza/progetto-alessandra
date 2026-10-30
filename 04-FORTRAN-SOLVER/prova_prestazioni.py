"""Prova di prestazioni del solutore (Ottavia, Elisa).

Genera telai regolari (campate × piani), li risolve con il Fortran e misura il tempo del solo
solutore, con la matrice a banda (predefinita) e con la matrice piena (opzione «piena»).
Controlla che i due metodi diano gli stessi spostamenti. Serve a fissare il limite di dimensione
del modello accettato dal servizio.

Uso:  python3 04-FORTRAN-SOLVER/prova_prestazioni.py
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from esegui import esegui  # noqa: E402

RADICE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, os.path.join(RADICE, "03-BACKEND", "converter"))
import converti  # noqa: E402


def telaio(campate, piani, L=6.0, h=3.5, q=-25.0, H=10.0):
    nodi, aste, vincoli = [], [], []
    nid = lambda c, p: p * (campate + 1) + c + 1  # noqa: E731
    for p in range(piani + 1):
        for c in range(campate + 1):
            nodi.append({"id": nid(c, p), "x": c * L, "y": p * h})
    k = 1
    for p in range(piani):
        for c in range(campate + 1):
            aste.append({"id": k, "nodo_i": nid(c, p), "nodo_j": nid(c, p + 1), "materiale": "S275", "sezione": "HEA200"}); k += 1
    travi = []
    for p in range(1, piani + 1):
        for c in range(campate):
            aste.append({"id": k, "nodo_i": nid(c, p), "nodo_j": nid(c + 1, p), "materiale": "S275", "sezione": "IPE300"})
            travi.append(k); k += 1
    for c in range(campate + 1):
        vincoli.append({"nodo": nid(c, 0), "ux": True, "uy": True, "rz": True})
    return {
        "schema_version": "1.0",
        "progetto": {"id": "prova", "nome": f"telaio {campate}x{piani}", "tipo_modello": "telaio_piano", "unita": {"lunghezza": "m", "forza": "kN"}},
        "nodi": nodi, "aste": aste, "vincoli": vincoli,
        "materiali": [{"id": "S275", "nome": "S275", "E": 2.1e8}],
        "sezioni": [{"id": "HEA200", "nome": "HE 200 A", "A": 53.83e-4, "I": 3692e-8}, {"id": "IPE300", "nome": "IPE 300", "A": 53.81e-4, "I": 8356e-8}],
        "casi_di_carico": [{"id": "C", "nome": "verticali e orizzontali",
                            "carichi_aste": [{"asta": t, "tipo": "distribuito_uniforme", "direzione": "globale_y", "q": q} for t in travi],
                            "carichi_nodali": [{"nodo": nid(0, p), "Fx": H} for p in range(1, piani + 1)]}],
        "analisi": {"punti_diagramma": 3},
    }


def cronometra(testo, opzioni=()):
    t0 = time.perf_counter()
    out = esegui(testo, opzioni=opzioni, tempo_massimo=600)
    return time.perf_counter() - t0, converti.leggi_output(out)


if __name__ == "__main__":
    PIENA_FINO_A = 2000  # oltre questi gdl la matrice piena richiede troppa memoria e tempo
    print(f"{'telaio':>10} {'nodi':>6} {'aste':>6} {'gdl':>6} {'banda [s]':>10} {'piena [s]':>10} {'scarto':>9} {'ΣRy/carico':>12}")
    for campate, piani in ((1, 10), (3, 10), (5, 20), (8, 25), (10, 40), (12, 50), (20, 100), (30, 150)):
        m = telaio(campate, piani)
        testo = converti.scrivi_input(m, "C")
        gdl = 3 * len(m["nodi"])
        tb, rb = cronometra(testo)
        tp, scarto = "—", "—"
        if gdl <= PIENA_FINO_A:
            t, rp = cronometra(testo, ("piena",))
            tp = f"{t:.3f}"
            umax = max(abs(u["ux"]) for u in rp["spostamenti"])
            scarto = f"{max(abs(a['ux'] - b['ux']) for a, b in zip(rb['spostamenti'], rp['spostamenti'])) / umax:.1e}"
        carico = 25.0 * 6.0 * campate * piani
        sry = sum(x["Ry"] for x in rb["reazioni"])
        print(f"{campate:>4}x{piani:<5} {len(m['nodi']):>6} {len(m['aste']):>6} {gdl:>6} {tb:>10.3f} {tp:>10} {scarto:>9} {sry / carico:>12.9f}")
