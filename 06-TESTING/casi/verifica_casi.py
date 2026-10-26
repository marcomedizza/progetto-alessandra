"""Verifica dei casi di prova.

1. Valida ogni modello C*.json con 01-ARCHITETTURA/DATA_SCHEMA.json (serve il pacchetto jsonschema).
2. Risolve ogni modello con il risolutore di riferimento 06-TESTING/riferimento/telaio2d.py.
3. Confronta i risultati con i valori attesi di C*.atteso.json (tolleranza relativa 0,5 %).

Uso:  python3 verifica_casi.py            → esito su terminale, codice di uscita 0 se tutto passa
      python3 verifica_casi.py --scrivi   → salva anche i risultati del riferimento in C*.riferimento.json

Lo stesso confronto si usa per il solutore Fortran: basta sostituire la funzione `risultati`.
"""

import glob
import json
import os
import sys

QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "06-TESTING", "riferimento"))
import telaio2d  # noqa: E402

TOLL_REL = 0.005
TOLL_ASS = 1e-6

# Lettura delle grandezze: etichetta dell'atteso → come estrarla dai risultati
def R(nodo, comp):
    return lambda r: next(x[comp] for x in r["reazioni"] if x["nodo"] == nodo)


def U(nodo, comp):
    return lambda r: next(x[comp] for x in r["spostamenti"] if x["nodo"] == nodo)


def S(asta, comp, x):
    def f(r):
        s = next(v for v in r["sollecitazioni"] if v["asta"] == asta)
        i = min(range(len(s["x"])), key=lambda k: abs(s["x"][k] - x))
        if abs(s["x"][i] - x) > 1e-9:
            raise ValueError(f"ascissa {x} non presente sull'asta {asta}")
        return s[comp][i]
    return f


def ABS(g):
    return lambda r: abs(g(r))


def SOMMA(*gs):
    return lambda r: sum(g(r) for g in gs)


def momento_c5(r):
    rz = {x["nodo"]: x for x in r["reazioni"]}
    # momento delle reazioni + carichi attorno al nodo 1 (0,0); positivo antiorario
    m = rz[1]["Mz"] + rz[2]["Mz"] + rz[2]["Ry"] * 6.0
    m += -10 * 3.5 - 15 * 7.0          # forze orizzontali verso +X alle quote 3.5 e 7
    m += 2 * (-25 * 6.0) * 3.0         # risultanti dei carichi uniformi a x = 3
    return m


LETTURE = {
    "C1": {
        "Ry nodo 1": R(1, "Ry"), "Ry nodo 3": R(3, "Ry"),
        "M asta 1 x=3 (mezzeria)": S(1, "M", 3.0), "uy nodo 2": U(2, "uy"),
        "rz nodo 1": U(1, "rz"), "V asta 1 x=0": S(1, "V", 0.0)},
    "C2": {
        "Ry nodo 1": R(1, "Ry"), "Mz nodo 1 (reazione)": R(1, "Mz"), "M asta 1 x=0": S(1, "M", 0.0),
        "uy nodo 2": U(2, "uy"), "rz nodo 2": U(2, "rz")},
    "C3": {
        "Rx nodo 1": R(1, "Rx"), "Rx nodo 4": R(4, "Rx"),
        "Mz nodo 1 (reazione)": R(1, "Mz"), "Mz nodo 4 (reazione)": R(4, "Mz"),
        "|M| asta 1 x=0": ABS(S(1, "M", 0.0)), "|M| asta 1 x=h": ABS(S(1, "M", 4.0)),
        "Ry nodo 1 + Ry nodo 4": SOMMA(R(1, "Ry"), R(4, "Ry"))},
    "C4": {
        "Ry nodo 1": R(1, "Ry"), "Ry nodo 4": R(4, "Ry"), "|Rx| nodo 1": ABS(R(1, "Rx")),
        "|M| asta 2 x=0 (angolo)": ABS(S(2, "M", 0.0)), "M asta 2 x=L/2 (mezzeria)": S(2, "M", 3.0),
        "|Mz| nodo 1 (reazione)": ABS(R(1, "Mz"))},
    "C5": {
        "Ry nodo 1 + Ry nodo 2": SOMMA(R(1, "Ry"), R(2, "Ry")),
        "Rx nodo 1 + Rx nodo 2": SOMMA(R(1, "Rx"), R(2, "Rx")),
        "momento risultante attorno al nodo 1": momento_c5},
}


def risultati(modello, caso):
    return telaio2d.analizza(modello, caso)


def main():
    scrivi = "--scrivi" in sys.argv
    try:
        import jsonschema
        with open(os.path.join(RADICE, "01-ARCHITETTURA", "DATA_SCHEMA.json"), encoding="utf-8") as fh:
            schema = json.load(fh)
        validatore = jsonschema.Draft202012Validator(schema)
    except ImportError:
        validatore = None
        print("ATTENZIONE: pacchetto jsonschema assente, validazione dello schema saltata")

    errori = 0
    for f in sorted(glob.glob(os.path.join(QUI, "C*.json"))):
        if f.endswith(".atteso.json") or f.endswith(".riferimento.json"):
            continue
        with open(f, encoding="utf-8") as fh:
            modello = json.load(fh)
        cid = modello["progetto"]["id"]
        print(f"\n== {cid}: {modello['progetto']['nome']}")
        if validatore:
            errs = sorted(validatore.iter_errors(modello), key=str)
            for e in errs:
                print("  SCHEMA ✗", list(e.path), e.message)
            errori += len(errs)
            if not errs:
                print("  schema ✓")
        with open(f.replace(".json", ".atteso.json"), encoding="utf-8") as fh:
            atteso = json.load(fh)
        r = risultati(modello, atteso["caso"])
        if scrivi:
            with open(f.replace(".json", ".riferimento.json"), "w", encoding="utf-8") as fh:
                json.dump(r, fh, indent=2, ensure_ascii=False)
                fh.write("\n")
        for v in atteso["valori"]:
            calc = LETTURE[cid][v["grandezza"]](r)
            att = v["valore"]
            ok = abs(calc - att) <= max(TOLL_ASS, TOLL_REL * abs(att))
            errori += 0 if ok else 1
            print(f"  {'✓' if ok else '✗'} {v['grandezza']:<42} atteso {att:>14.6g}  calcolato {calc:>14.6g} {v['unita']}")
    print("\nESITO:", "tutti i controlli superati" if errori == 0 else f"{errori} controlli non superati")
    return 0 if errori == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
