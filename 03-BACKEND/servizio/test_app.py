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


def test_rotazioni_alle_cerniere():
    # D8 (30/10): rotazione della mensola alla cerniera di C6, soluzione chiusa −(q·4³/6 + Rs·4²/2)/EI
    r = client.post("/api/calcola", json=modello("C6_trave_gerber"))
    ris = r.json()["risultati"][0]
    rot = {x["asta"]: x for x in ris["rotazioni_aste"]}
    EI = 2.1e8 * 8356e-8
    assert abs(rot[1]["phi_j"] + (10 * 4 ** 3 / 6 + 10 * 4 ** 2 / 2) / EI) < 1e-9
    rz2 = next(u["rz"] for u in ris["spostamenti"] if u["nodo"] == 2)
    assert abs(rot[2]["phi_i"] - rz2) < 1e-15 and abs(rot[1]["phi_j"] - rz2) > 1e-3


def test_sezione_e_materiale_inseriti():
    # revisione 14 (30/10): come dall'interfaccia, sezione e materiale copiati e modificati su un'asta di C1.
    # Freccia in mezzeria = somma dei contributi delle due metà: δ = δ0·(EI0/EI1 + EI0/EI2)/2
    m = modello("C1_trave_appoggiata")
    m["sezioni"].append({"id": "IPE300_2", "nome": "IPE 300 (2)", "A": 53.81e-4, "I": 2 * 8356e-8, "fonte": "valori inseriti dall'utente"})
    m["materiali"].append({"id": "S275_2", "nome": "Alluminio", "E": 7.0e7})
    m["aste"][0].update(sezione="IPE300_2", materiale="S275_2")
    uy = next(u["uy"] for u in client.post("/api/calcola", json=m).json()["risultati"][0]["spostamenti"] if u["nodo"] == 2)
    d0 = 5 * 10 * 6 ** 4 / (384 * 2.1e8 * 8356e-8)
    assert abs(-uy - d0 * (2.1e8 / (7.0e7 * 2) + 1) / 2) < 1e-9
    m["sezioni"][-1]["I"] = 0
    assert client.post("/api/calcola", json=m).status_code == 422


def test_modello_grande():
    # matrice a banda (30/10): telaio 20 campate × 100 piani, 2121 nodi e 4100 aste, equilibrio verticale
    sys.path.insert(0, os.path.join(servizio.RADICE, "04-FORTRAN-SOLVER"))
    from prova_prestazioni import telaio
    m = telaio(20, 100)
    ris = client.post("/api/calcola", json=m).json()["risultati"][0]
    assert abs(sum(x["Ry"] for x in ris["reazioni"]) - 25 * 6 * 20 * 100) < 1e-6


def test_nodi_in_ordine_qualsiasi():
    # riordino di Cuthill-McKee (30/10): nodi mescolati come in un modello disegnato a mano
    import random
    sys.path.insert(0, os.path.join(servizio.RADICE, "04-FORTRAN-SOLVER"))
    from prova_prestazioni import telaio
    import converti
    m = telaio(30, 150)
    random.Random(1).shuffle(m["nodi"])
    assert converti.semibanda(m, converti.ordine_nodi(m)) < 120 < converti.semibanda(m)
    ris = client.post("/api/calcola", json=m).json()["risultati"][0]
    assert [u["nodo"] for u in ris["spostamenti"]] == [n["id"] for n in m["nodi"]]
    # senza riordino la semibanda supera il limite di memoria e il solutore lo dice
    originale = converti.ordine_nodi
    converti.ordine_nodi = lambda mod: [n["id"] for n in mod["nodi"]]
    try:
        r = client.post("/api/calcola", json=m)
        assert r.status_code != 200 and "semibanda" in r.text
    finally:
        converti.ordine_nodi = originale


def test_v11_trapezi_e_cedimenti():
    # schema v1.1 (31/10): C11 cedimento, C12 trapezio parziale, C13 triangolare, contro le formule chiuse
    r11 = client.post("/api/calcola", json=modello("C11_cedimento_appoggio")).json()["risultati"][0]
    F = 48 * 2.1e8 * 8356e-8 * 0.01 / 12 ** 3
    assert abs(next(x["Ry"] for x in r11["reazioni"] if x["nodo"] == 2) + F) < 1e-9
    r12 = client.post("/api/calcola", json=modello("C12_trapezio_parziale")).json()["risultati"][0]
    assert abs(next(x["Ry"] for x in r12["reazioni"] if x["nodo"] == 1) - 25) < 1e-9
    r13 = client.post("/api/calcola", json=modello("C13_triangolare_incastrata")).json()["risultati"][0]
    assert abs(r13["sollecitazioni"][0]["M"][-1] + 36) < 1e-9


def test_v11_controlli():
    m = modello("C11_cedimento_appoggio")
    m["schema_version"] = "1.0"
    assert "schema_version 1.1" in " ".join(client.post("/api/valida", json=m).json()["coerenza"])
    m = modello("C11_cedimento_appoggio")
    m["casi_di_carico"][0]["cedimenti"] = [{"nodo": 2, "ux": 0.01}]   # ux non vincolato nel nodo 2
    assert "non ha ux vincolato" in " ".join(client.post("/api/valida", json=m).json()["coerenza"])
    m = modello("C12_trapezio_parziale")
    m["casi_di_carico"][0]["carichi_aste"][0]["b"] = 7.0               # oltre la lunghezza dell'asta
    assert client.post("/api/calcola", json=m).status_code == 422


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
