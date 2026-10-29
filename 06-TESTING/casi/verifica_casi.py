"""Verifica dei casi di prova.

1. Valida ogni modello C*.json con 01-ARCHITETTURA/DATA_SCHEMA.json (serve il pacchetto jsonschema).
2. Risolve ogni modello con il risolutore di riferimento 06-TESTING/riferimento/telaio2d.py.
3. Confronta i risultati con i valori attesi di C*.atteso.json (tolleranza relativa 0,5 %).

Uso:  python3 verifica_casi.py              → risolutore di riferimento Python
      python3 verifica_casi.py --fortran    → solutore Fortran tramite il convertitore (03-BACKEND/converter)
      python3 verifica_casi.py --api        → percorso completo del prototipo: POST al servizio FastAPI → Fortran
      python3 verifica_casi.py --scrivi     → salva anche i risultati del riferimento in C*.riferimento.json

Con --fortran confronta anche, nodo per nodo e asta per asta, i risultati
completi del Fortran con quelli del riferimento (tolleranza 1e-6 relativa).
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
    "C6": {
        "Ry nodo 3": R(3, "Ry"), "Ry nodo 1": R(1, "Ry"), "Mz nodo 1 (reazione)": R(1, "Mz"),
        "M asta 1 x=0": S(1, "M", 0.0), "M asta 1 x=4 (cerniera)": S(1, "M", 4.0),
        "M asta 2 x=1 (mezzeria tratto appoggiato)": S(2, "M", 1.0)},
    "C7": {
        "Ry nodo 1": R(1, "Ry"), "Ry nodo 2": R(2, "Ry"), "M asta 1 x=2 (sotto il carico)": S(1, "M", 2.0),
        "rz nodo 1": U(1, "rz"), "rz nodo 2": U(2, "rz")},
    "C8": {
        "Ry nodo 2 (molla)": R(2, "Ry"), "uy nodo 2": U(2, "uy"), "Ry nodo 1": R(1, "Ry"),
        "M asta 1 x=3 (mezzeria)": S(1, "M", 3.0)},
    "C9": {
        "Ry nodo 4 (molla)": R(4, "Ry"), "Ry nodo 1": R(1, "Ry"), "Rx nodo 4": R(4, "Rx"), "Rx nodo 1": R(1, "Rx"),
        "uy nodo 4": U(4, "uy"), "|M| asta 3 x=h (testa colonna destra)": ABS(S(3, "M", 4.0)),
        "M asta 2 x=L/2 (cerniera)": S(2, "M", 3.0)},
    "C10": {
        "Ry nodo 1": R(1, "Ry"), "Ry nodo 2": R(2, "Ry"), "M asta 1 x=2 (sotto il carico)": S(1, "M", 2.0)},
}


API = "--api" in sys.argv
FORTRAN = "--fortran" in sys.argv or API
if FORTRAN:
    sys.path.insert(0, os.path.join(RADICE, "03-BACKEND", "converter"))
    import converti  # noqa: E402
if API:
    sys.path.insert(0, os.path.join(RADICE, "03-BACKEND", "servizio"))
    from fastapi.testclient import TestClient  # noqa: E402
    import app as servizio  # noqa: E402
    CLIENT = TestClient(servizio.app)


def combinazione_riferimento(modello, comb_id):
    """Sovrapposizione lineare dei casi con il risolutore di riferimento."""
    comb = next(c for c in modello["combinazioni"] if c["id"] == comb_id)
    parti = [(telaio2d.analizza(modello, cid), f) for cid, f in comb["coefficienti"].items()]
    out = json.loads(json.dumps(parti[0][0]))
    out["caso"] = comb_id
    for blocco, campi in (("spostamenti", ("ux", "uy", "rz")), ("reazioni", ("Rx", "Ry", "Mz")), ("sollecitazioni", ("N", "V", "M"))):
        for i, el in enumerate(out[blocco]):
            for k in campi:
                if isinstance(el[k], list):
                    el[k] = [sum(f * p[blocco][i][k][j] for p, f in parti) for j in range(len(el[k]))]
                else:
                    el[k] = sum(f * p[blocco][i][k] for p, f in parti)
    return out


def e_combinazione(modello, caso):
    return any(c["id"] == caso for c in modello.get("combinazioni", []))


def risultati(modello, caso):
    comb = e_combinazione(modello, caso)
    if API:
        r = CLIENT.post(f"/api/calcola?{'combinazione' if comb else 'caso'}={caso}", json=modello)
        if r.status_code != 200:
            raise RuntimeError(f"servizio: {r.status_code} {r.text}")
        return r.json()["risultati"][0]
    if FORTRAN:
        return converti.combina(modello, caso) if comb else converti.risultati(modello, caso)
    return combinazione_riferimento(modello, caso) if comb else telaio2d.analizza(modello, caso)


def confronto_completo(a, b):
    """Differenze tra due blocchi risultati (Fortran e riferimento). Restituisce il numero di scostamenti."""
    n = 0
    def vicino(p, q):
        return abs(p - q) <= 1e-6 * max(1.0, abs(p), abs(q))
    # confronto per identificativo, non per posizione: l'ordine dei nodi può differire
    def per_id(lista, chiave):
        return {x[chiave]: x for x in lista}
    for blocco, chiave, campi in (("spostamenti", "nodo", ("ux", "uy", "rz")), ("reazioni", "nodo", ("Rx", "Ry", "Mz"))):
        A, B = per_id(a[blocco], chiave), per_id(b[blocco], chiave)
        n += len(set(A) ^ set(B))
        for i in set(A) & set(B):
            n += sum(not vicino(A[i][k], B[i][k]) for k in campi)
    A, B = per_id(a["sollecitazioni"], "asta"), per_id(b["sollecitazioni"], "asta")
    n += len(set(A) ^ set(B))
    for x, y in ((A[i], B[i]) for i in set(A) & set(B)):
        for k in ("N", "V", "M"):
            n += sum(not vicino(p, q) for p, q in zip(x[k], y[k]))
    return n


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
        print(f"\n== {cid}: {modello['progetto']['nome']}" + (" [servizio FastAPI → Fortran]" if API else " [Fortran]" if FORTRAN else ""))
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
        if FORTRAN:
            rif = (combinazione_riferimento(modello, atteso["caso"]) if e_combinazione(modello, atteso["caso"])
                   else telaio2d.analizza(modello, atteso["caso"]))
            diff = confronto_completo(r, rif)
            errori += diff
            print(f"  {'✓' if diff == 0 else '✗'} confronto completo {'servizio' if API else 'Fortran'} / riferimento: {diff} scostamenti")
        if scrivi and not FORTRAN:
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
