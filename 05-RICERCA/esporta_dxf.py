"""Bozza di esportazione della geometria in DXF (Carla, Daniela — 30/10/2026).

Ripiego in attesa della documentazione ModeSt: esporta solo nodi e aste di un modello conforme allo
schema v1.0 in un DXF ASCII minimo (formato R12: sezione ENTITIES con LINE e POINT), coordinate in metri.
Un livello per sezione (es. «ASTE_IPE300»), più il livello «NODI». Sezioni, vincoli e carichi NON sono
trasferiti: in ModeSt andrebbero reinseriti a mano. Da provare su ModeSt prima di qualunque uso.

Uso:  python3 05-RICERCA/esporta_dxf.py modello.json uscita.dxf
"""

import json
import re
import sys


def livello(nome):
    # nomi dei livelli DXF: lettere, cifre, trattino e sottolineatura
    return re.sub(r"[^A-Za-z0-9_-]", "_", nome).upper()[:31]


def dxf(modello):
    nodi = {n["id"]: n for n in modello["nodi"]}
    r = ["0", "SECTION", "2", "ENTITIES"]
    for n in modello["nodi"]:
        r += ["0", "POINT", "8", "NODI", "10", repr(float(n["x"])), "20", repr(float(n["y"])), "30", "0.0"]
    for a in modello["aste"]:
        i, j = nodi[a["nodo_i"]], nodi[a["nodo_j"]]
        r += ["0", "LINE", "8", livello("ASTE_" + a["sezione"]),
              "10", repr(float(i["x"])), "20", repr(float(i["y"])), "30", "0.0",
              "11", repr(float(j["x"])), "21", repr(float(j["y"])), "31", "0.0"]
    r += ["0", "ENDSEC", "0", "EOF"]
    return "\n".join(r) + "\n"


def rileggi(testo):
    """Rilettura minima per la prova: restituisce le LINE come (livello, x1, y1, x2, y2)."""
    v = testo.split("\n")
    coppie = list(zip(v[0::2], v[1::2]))
    linee, cur = [], None
    for cod, val in coppie:
        if cod == "0":
            if cur:
                linee.append((cur["8"], float(cur["10"]), float(cur["20"]), float(cur["11"]), float(cur["21"])))
            cur = {} if val == "LINE" else None
        elif cur is not None:
            cur[cod] = val
    return linee


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    with open(sys.argv[1], encoding="utf-8") as fh:
        m = json.load(fh)
    testo = dxf(m)
    with open(sys.argv[2], "w") as fh:
        fh.write(testo)
    print(f"scritto {sys.argv[2]}: {len(m['nodi'])} nodi, {len(rileggi(testo))} aste")
