"""Matrice di copertura dei casi di prova (Valentina, Silvia; 24/11/2026).

Legge i modelli C*.json e indica, per ogni funzione dello schema, quali casi la usano. Le funzioni senza casi
sono elencate in fondo: sono le lacune della suite.

Uso:  python3 06-TESTING/casi/copertura.py            stampa la tabella in Markdown
"""

import glob
import json
import math
import os

QUI = os.path.dirname(os.path.abspath(__file__))


def funzioni(m):
    """Insieme delle funzioni dello schema usate dal modello m."""
    f = set()
    nodi = {n["id"]: n for n in m["nodi"]}
    f.add(f"schema {m.get('schema_version', '1.0')}")
    for v in m.get("vincoli", []):
        tipo = "".join(k for k in ("ux", "uy", "rz") if v.get(k))
        f.add({"uxuyrz": "vincolo: incastro", "uxuy": "vincolo: cerniera", "uy": "vincolo: carrello verticale",
               "ux": "vincolo: carrello orizzontale"}.get(tipo, f"vincolo: {tipo or 'solo molle'}"))
        if "rz" in tipo and tipo != "uxuyrz":
            f.add("vincolo: rotazione impedita senza incastro (pattino)")
        for k in ("kx", "ky", "kr"):
            if (v.get("molle") or {}).get(k):
                f.add(f"molla {k}")
    for a in m["aste"]:
        sv = a.get("svincoli", {})
        if sv.get("rz_i") and sv.get("rz_j"):
            f.add("asta incernierata ai due estremi")
        elif sv.get("rz_i") or sv.get("rz_j"):
            f.add("asta incernierata a un estremo")
        ni, nj = nodi[a["nodo_i"]], nodi[a["nodo_j"]]
        dx, dy = nj["x"] - ni["x"], nj["y"] - ni["y"]
        if abs(dx) > 1e-9 and abs(dy) > 1e-9:
            f.add("asta inclinata")
        if abs(dx) < 1e-9:
            f.add("asta verticale")
    if not m.get("analisi", {}).get("deformabilita_assiale", True):
        f.add("deformabilità assiale trascurata")
    for c in m["casi_di_carico"]:
        if c.get("peso_proprio"):
            f.add("peso proprio")
        for q in c.get("carichi_nodali", []):
            for k in ("Fx", "Fy", "Mz"):
                if q.get(k):
                    f.add(f"carico nodale {k}")
        for q in c.get("carichi_aste", []):
            nome = {"distribuito_uniforme": "uniforme", "concentrato": "concentrato",
                    "distribuito_trapezio": "trapezio"}.get(q["tipo"], q["tipo"])
            f.add(f"carico d'asta {nome} {q['direzione']}")
            if q["tipo"] == "distribuito_trapezio":
                a = next(x for x in m["aste"] if x["id"] == q["asta"])
                L = math.dist((nodi[a["nodo_i"]]["x"], nodi[a["nodo_i"]]["y"]), (nodi[a["nodo_j"]]["x"], nodi[a["nodo_j"]]["y"]))
                if q["a"] > 1e-9 or q["b"] < L - 1e-9:
                    f.add("trapezio parziale")
        for d in c.get("cedimenti", []):
            for k in ("ux", "uy", "rz"):
                if d.get(k):
                    f.add(f"cedimento {k}")
        for t in c.get("carichi_termici", []):
            if t.get("dT_u"):
                f.add("ΔT uniforme")
            if t.get("dT_g"):
                f.add("ΔT a farfalla")
    if m.get("combinazioni"):
        f.add("combinazione di casi")
    return f


# funzioni che lo schema consente e che ci si aspetta di trovare nella suite
ATTESE = ["vincolo: incastro", "vincolo: cerniera", "vincolo: carrello verticale", "vincolo: carrello orizzontale",
          "vincolo: rotazione impedita senza incastro (pattino)", "molla kx", "molla ky", "molla kr",
          "asta incernierata a un estremo", "asta incernierata ai due estremi", "asta inclinata",
          "deformabilità assiale trascurata", "peso proprio", "carico nodale Fx", "carico nodale Fy", "carico nodale Mz"] + [
          f"carico d'asta {t} {d}" for t in ("uniforme", "concentrato", "trapezio")
          for d in ("globale_x", "globale_y", "locale_y")] + [
          "trapezio parziale", "cedimento ux", "cedimento uy", "cedimento rz", "ΔT uniforme", "ΔT a farfalla",
          "combinazione di casi"]


def attese_dallo_schema():
    """Funzioni ricavate dallo schema (punto 105, 25/11): tipi e direzioni dei carichi d'asta, componenti dei
    carichi nodali, dei cedimenti, delle distorsioni termiche e delle molle. Ogni voce deve stare in ATTESE."""
    with open(os.path.join(QUI, "..", "..", "01-ARCHITETTURA", "DATA_SCHEMA.json"), encoding="utf-8") as fh:
        sc = json.load(fh)
    caso = sc["properties"]["casi_di_carico"]["items"]["properties"]
    nomi = {"distribuito_uniforme": "uniforme", "concentrato": "concentrato", "distribuito_trapezio": "trapezio"}
    out = []
    for o in caso["carichi_aste"]["items"]["oneOf"]:
        for d in o["properties"]["direzione"]["enum"]:
            out.append(f"carico d'asta {nomi[o['properties']['tipo']['const']]} {d}")
    out += [f"carico nodale {k}" for k in caso["carichi_nodali"]["items"]["properties"] if k != "nodo"]
    out += [f"cedimento {k}" for k in caso["cedimenti"]["items"]["properties"] if k != "nodo"]
    out += [{"dT_u": "ΔT uniforme", "dT_g": "ΔT a farfalla"}[k] for k in caso["carichi_termici"]["items"]["properties"] if k != "asta"]
    out += [f"molla {k}" for k in sc["properties"]["vincoli"]["items"]["properties"]["molle"]["properties"]]
    if "peso_proprio" in caso:
        out.append("peso proprio")
    return out


def main():
    casi = {}
    for p in sorted(glob.glob(os.path.join(QUI, "C*.json")), key=lambda p: int(os.path.basename(p)[1:].split("_")[0])):
        if p.endswith((".atteso.json", ".riferimento.json")):
            continue
        with open(p, encoding="utf-8") as fh:
            m = json.load(fh)
        casi[m["progetto"]["id"]] = funzioni(m)
    print("| Funzione | Casi |\n|---|---|")
    for f in ATTESE:
        print(f"| {f} | {', '.join(c for c, s in casi.items() if f in s) or '**nessuno**'} |")
    fuori = [f for f in attese_dallo_schema() if f not in ATTESE]
    if fuori:
        print("Funzioni dello schema non elencate in ATTESE:", "; ".join(fuori))
    mancanti = [f for f in ATTESE if not any(f in s for s in casi.values())]
    print(f"\n{len(casi)} casi; {len(ATTESE) - len(mancanti)} funzioni coperte su {len(ATTESE)}.")
    if mancanti:
        print("Senza casi:", "; ".join(mancanti))


if __name__ == "__main__":
    main()
