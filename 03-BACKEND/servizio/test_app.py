"""Prove del servizio (Natalia, Silvia). Avvio: python3 -m pytest 03-BACKEND/servizio -q
oppure python3 03-BACKEND/servizio/test_app.py"""

import copy
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fastapi.testclient import TestClient  # noqa: E402
import app as servizio  # noqa: E402

client = TestClient(servizio.app)


def modello(nome):
    return client.get(f"/api/casi/{nome}").json()


def test_salute():
    r = client.get("/api/salute").json()
    assert r["servizio"] == "ok" and r["solutore"] and r["schema"]


def test_elenco():
    nomi = [c["nome"] for c in client.get("/api/casi").json()]
    assert "C1_trave_appoggiata" in nomi and "C3_portale_forza_orizzontale" in nomi


def test_calcola_c1():
    r = client.post("/api/calcola", json=modello("C1_trave_appoggiata"))
    assert r.status_code == 200
    ris = r.json()["risultati"][0]
    m = next(s for s in ris["sollecitazioni"] if s["asta"] == 1)
    assert abs(m["M"][-1] - 45.0) < 1e-6          # momento in mezzeria qL²/8
    uy = next(s for s in ris["spostamenti"] if s["nodo"] == 2)["uy"]
    assert abs(uy - (-0.0096167)) < 1e-6


def test_calcola_c3():
    r = client.post("/api/calcola?caso=H", json=modello("C3_portale_forza_orizzontale"))
    assert r.status_code == 200
    reaz = r.json()["risultati"][0]["reazioni"]
    assert abs(sum(x["Rx"] for x in reaz) + 20.0) < 1e-6
    assert abs(reaz[0]["Mz"] - 21.9894) < 1e-3


def test_modello_non_valido():
    m = modello("C1_trave_appoggiata")
    del m["aste"]
    r = client.post("/api/calcola", json=m)
    assert r.status_code == 422


def test_riferimento_errato():
    m = copy.deepcopy(modello("C1_trave_appoggiata"))
    m["aste"][0]["nodo_j"] = 99
    v = client.post("/api/valida", json=m).json()
    assert not v["valido"] and any("99" in e for e in v["coerenza"])


def test_struttura_labile():
    m = modello("C1_trave_appoggiata")
    m["vincoli"] = [{"nodo": 1, "uy": True}, {"nodo": 3, "uy": True}]   # manca il vincolo orizzontale
    r = client.post("/api/calcola", json=m)
    assert r.status_code == 422 and "singolare" in json.dumps(r.json())


def test_combinazione_lineare():
    import json, os
    with open(os.path.join(servizio.RADICE, "01-ARCHITETTURA", "ESEMPIO_PORTALE_2D.json"), encoding="utf-8") as fh:
        m = json.load(fh)
    g = client.post("/api/calcola?caso=G2", json=m).json()["risultati"][0]
    w = client.post("/api/calcola?caso=W", json=m).json()["risultati"][0]
    c = client.post("/api/calcola?combinazione=SLU1", json=m).json()["risultati"][0]
    for rg, rw, rc in zip(g["reazioni"], w["reazioni"], c["reazioni"]):
        for k in ("Rx", "Ry", "Mz"):
            assert abs(rc[k] - (1.3 * rg[k] + 1.5 * rw[k])) < 1e-9
    assert client.post("/api/calcola?combinazione=XX", json=m).status_code == 422


def test_c9_cerniera_e_molla():
    r = client.post("/api/calcola", json=modello("C9_portale_tre_cerniere_molla"))
    assert r.status_code == 200
    reaz = {x["nodo"]: x for x in r.json()["risultati"][0]["reazioni"]}
    assert abs(reaz[4]["Ry"] - 20 * 4 / 6) < 1e-6 and abs(reaz[4]["Rx"] + 10) < 1e-6


def test_modello_modificato():
    # come dall'interfaccia (D4): si aggiunge un nodo e un'asta con identificativi non consecutivi
    m = modello("C1_trave_appoggiata")
    m["nodi"].append({"id": 10, "x": 0, "y": 3})
    m["aste"].append({"id": 7, "nodo_i": 1, "nodo_j": 10, "materiale": "S275", "sezione": "IPE300"})
    m["casi_di_carico"][0]["carichi_nodali"] = [{"nodo": 10, "Fx": 5}]
    r = client.post("/api/calcola", json=m)
    assert r.status_code == 200
    ris = r.json()["risultati"][0]
    assert abs(sum(x["Rx"] for x in ris["reazioni"]) + 5) < 1e-9
    assert {s["asta"] for s in ris["sollecitazioni"]} == {1, 2, 7}


def test_limite_dimensione():
    m = modello("C1_trave_appoggiata")
    m["nodi"] = [{"id": i, "x": float(i), "y": 0.0} for i in range(1, servizio.MAX_NODI + 2)]
    v = client.post("/api/valida", json=m).json()
    assert not v["valido"] and "troppo grande" in v["coerenza"][0]


def test_frontend():
    assert client.get("/app/").status_code == 200


if __name__ == "__main__":
    n = 0
    for nome, f in list(globals().items()):
        if nome.startswith("test_"):
            f()
            n += 1
            print("✓", nome)
    print(f"{n} prove superate")
