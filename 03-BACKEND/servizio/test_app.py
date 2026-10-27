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
