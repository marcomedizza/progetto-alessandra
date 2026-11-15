"""Studio dell'errore del metodo dell'area fittizia (punto 79; Elisa e Ottavia, 15/11/2026).

Con la deformabilità assiale trascurata ogni asta riceve A = max(A, R·12I/L²), cioè una rigidezza assiale
R volte quella flessionale della stessa asta. L'errore rispetto alla soluzione rigida ha due parti:
- errore di modello, che cala come 1/R, perché l'asta resta un po' deformabile;
- arrotondamento, che cresce con R, perché la matrice diventa malcondizionata.

Il telaio di C24 sotto il solo vento ha soluzione rigida esatta: ciascuna colonna porta metà delle forze di piano.
- Rx = −12,5 kN per piede;
- momento al piede 70 kNm;
- travi compresse di 5 e 7,5 kN;
- reazioni verticali nulle.

La variante «divisa» spezza ogni trave in due aste con le cerniere agli estremi, come C27.

Uso:  python3 04-FORTRAN-SOLVER/studio_area_fittizia.py
"""

import copy
import json
import os
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(QUI, ".."))
sys.path.insert(0, os.path.join(RADICE, "03-BACKEND", "converter"))
sys.path.insert(0, os.path.join(RADICE, "06-TESTING", "riferimento"))
import converti  # noqa: E402
import telaio2d  # noqa: E402

ESATTI = {"Rx": -12.5, "M_piede": 70.0, "N_trave_1": -5.0, "N_trave_2": -7.5, "Ry": 0.0}


def c24():
    with open(os.path.join(RADICE, "06-TESTING", "casi", "C24_due_piani_combinazione.json"), encoding="utf-8") as fh:
        return json.load(fh)


def divisa(m):
    """Travi divise in mezzeria (nodi 7 e 8), cerniere agli estremi, come in C27."""
    m = copy.deepcopy(m)
    m["nodi"] += [{"id": 7, "x": 3.0, "y": 3.5}, {"id": 8, "x": 3.0, "y": 7.0}]
    m["aste"] = m["aste"][:4] + [
        {"id": 5, "nodo_i": 3, "nodo_j": 7, "materiale": "S275", "sezione": "IPE300", "svincoli": {"rz_i": True}},
        {"id": 6, "nodo_i": 7, "nodo_j": 4, "materiale": "S275", "sezione": "IPE300", "svincoli": {"rz_j": True}},
        {"id": 7, "nodo_i": 5, "nodo_j": 8, "materiale": "S275", "sezione": "IPE300", "svincoli": {"rz_i": True}},
        {"id": 8, "nodo_i": 8, "nodo_j": 6, "materiale": "S275", "sezione": "IPE300", "svincoli": {"rz_j": True}}]
    m["casi_di_carico"] = [c for c in m["casi_di_carico"] if c["id"] == "W"]
    return m


def errore(r, travi):
    """Massimo scarto assoluto [kN, kNm] sulle grandezze con soluzione rigida esatta."""
    rz = {x["nodo"]: x for x in r["reazioni"]}
    s = {x["asta"]: x for x in r["sollecitazioni"]}
    valori = [(rz[1]["Rx"], ESATTI["Rx"]), (rz[2]["Rx"], ESATTI["Rx"]),
              (abs(s[1]["M"][0]), ESATTI["M_piede"]), (abs(s[2]["M"][0]), ESATTI["M_piede"]),
              (s[travi[0]]["N"][0], ESATTI["N_trave_1"]), (s[travi[1]]["N"][0], ESATTI["N_trave_2"]),
              (rz[1]["Ry"], ESATTI["Ry"]), (rz[2]["Ry"], ESATTI["Ry"])]
    return max(abs(a - b) for a, b in valori)


def errore_c3(r):
    """C3, portale a nodi rigidi: scarto sul momento al piede rispetto alla soluzione chiusa (21,9894 kNm)."""
    with open(os.path.join(RADICE, "06-TESTING", "casi", "C3_portale_forza_orizzontale.atteso.json"), encoding="utf-8") as fh:
        esatto = next(v["valore"] for v in json.load(fh)["valori"] if v["grandezza"] == "Mz nodo 1 (reazione)")
    return abs({x["nodo"]: x for x in r["reazioni"]}[1]["Mz"] - esatto)


def c3():
    with open(os.path.join(RADICE, "06-TESTING", "casi", "C3_portale_forza_orizzontale.json"), encoding="utf-8") as fh:
        return json.load(fh)


def studio(rapporti=(1e4, 1e5, 1e6, 1e7, 1e8, 1e9, 1e10, 1e11)):
    righe = []
    for nome, m, travi in (("C24, travi intere", c24(), (5, 6)), ("travi divise (C27)", divisa(c24()), (5, 7))):
        for R in rapporti:
            converti.RAPPORTO_ASSIALE = R
            telaio2d.RAPPORTO_ASSIALE = R
            try:
                ef = errore(converti.risultati(m, "W"), travi)
            except RuntimeError as ex:  # il Fortran può dichiarare labile la struttura se il condizionamento crolla
                ef = f"errore: {ex}"[:40]
            try:
                er = errore(telaio2d.analizza(m, "W"), travi)
            except ValueError:  # soglia di labilità del riferimento superata
                er = "labile"
            righe.append((nome, R, er, ef))
    m = c3()
    for R in rapporti:
        converti.RAPPORTO_ASSIALE = telaio2d.RAPPORTO_ASSIALE = R
        caso = m["casi_di_carico"][0]["id"]
        try:
            ef = errore_c3(converti.risultati(m, caso))
        except RuntimeError as ex:
            ef = f"errore: {ex}"[:40]
        try:
            er = errore_c3(telaio2d.analizza(m, caso))
        except ValueError:
            er = "labile"
        righe.append(("C3, nodi rigidi", R, er, ef))
    converti.RAPPORTO_ASSIALE = telaio2d.RAPPORTO_ASSIALE = 1e8
    return righe


if __name__ == "__main__":
    print(f"{'modello':22} {'R':>8} {'riferimento [kN]':>18} {'Fortran [kN]':>18}")
    for nome, R, er, ef in studio():
        fmt = lambda x: f"{x:>18}" if isinstance(x, str) else f"{x:18.2e}"  # noqa: E731
        print(f"{nome:22} {R:8.0e} {fmt(er)} {fmt(ef)}")
