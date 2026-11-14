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


def test_modello_grande_con_cedimenti():
    # Carla (02/11): telaio 20 × 100 (6363 gdl, matrice a banda), solo cedimento di 10 mm di un piede.
    # Senza carichi le reazioni sono autoequilibrate: somme di forze e momento risultante nulli
    sys.path.insert(0, os.path.join(servizio.RADICE, "04-FORTRAN-SOLVER"))
    from prova_prestazioni import telaio
    m = telaio(20, 100)
    m["schema_version"] = "1.1"
    m["casi_di_carico"][0].update(carichi_aste=[], carichi_nodali=[], cedimenti=[{"nodo": 11, "uy": -0.01}])
    ris = client.post("/api/calcola", json=m).json()["risultati"][0]
    x = {n["id"]: n["x"] for n in m["nodi"]}
    assert abs(sum(r["Ry"] for r in ris["reazioni"])) < 1e-6 and abs(sum(r["Rx"] for r in ris["reazioni"])) < 1e-6
    assert abs(sum(r["Mz"] + r["Ry"] * x[r["nodo"]] for r in ris["reazioni"])) < 1e-5
    assert abs(next(u["uy"] for u in ris["spostamenti"] if u["nodo"] == 11) + 0.01) < 1e-15
    assert max(abs(r["Ry"]) for r in ris["reazioni"]) > 1.0     # il cedimento produce davvero reazioni


def test_cedimento_su_molla_rifiutato():
    # punto 28 della revisione: la molla ha già uno spostamento incognito, un cedimento lì non ha senso
    m = modello("C8_molla_in_mezzeria")
    m["schema_version"] = "1.1"
    m["casi_di_carico"][0]["cedimenti"] = [{"nodo": 2, "uy": -0.005}]
    v = client.post("/api/valida", json=m).json()
    assert not v["valido"] and "non ha uy vincolato" in " ".join(v["coerenza"])


def test_trapezio_normale_asta_inclinata():
    # punto 32 (03/11): carico normale all'asta (locale_y) su asta inclinata, C17 contro la statica
    r = client.post("/api/calcola", json=modello("C17_inclinata_normale")).json()["risultati"][0]
    reaz = {x["nodo"]: x for x in r["reazioni"]}
    assert abs(reaz[1]["Rx"] + 18) < 1e-9 and abs(reaz[2]["Ry"] - 18.75) < 1e-9
    assert max(abs(n - 11.25) for n in r["sollecitazioni"][0]["N"]) < 1e-9


def test_v12_distorsioni_termiche():
    # v1.2 (03/11): C14 incastrata (N = −EAαΔT, M = −EIαΔTg/h) e C18 appoggiata (freccia −κL²/8)
    r14 = client.post("/api/calcola", json=modello("C14_termica_incastrata")).json()["risultati"][0]
    assert abs(r14["sollecitazioni"][0]["N"][0] + 2.1e8 * 53.81e-4 * 1.2e-5 * 20) < 1e-6
    r18 = client.post("/api/calcola", json=modello("C18_termica_appoggiata")).json()["risultati"][0]
    assert abs(next(u["uy"] for u in r18["spostamenti"] if u["nodo"] == 2) + 1.2e-5 * 10 / 0.3 * 36 / 8) < 1e-12
    # regole di coerenza
    m = modello("C14_termica_incastrata")
    m["schema_version"] = "1.1"
    assert "schema_version 1.2" in " ".join(client.post("/api/valida", json=m).json()["coerenza"])
    m = modello("C14_termica_incastrata")
    del m["sezioni"][0]["h"]
    assert "richiede h" in " ".join(client.post("/api/valida", json=m).json()["coerenza"])
    m = modello("C14_termica_incastrata")
    m["analisi"]["deformabilita_assiale"] = False
    assert "deformabilità assiale" in " ".join(client.post("/api/valida", json=m).json()["coerenza"])


def test_cerniera_e_termica():
    # punto 41 (04/11): condensazione della cerniera con forze termiche, C19 contro la cinematica
    r = client.post("/api/calcola", json=modello("C19_gerber_termica")).json()["risultati"][0]
    k = 1.2e-5 * 10 / 0.3
    assert abs(next(u["uy"] for u in r["spostamenti"] if u["nodo"] == 2) - k * 8) < 1e-12
    assert abs(next(x["phi_j"] for x in r["rotazioni_aste"] if x["asta"] == 1) - 4 * k) < 1e-12
    assert max(abs(v) for s in r["sollecitazioni"] for v in s["M"]) < 1e-9


def test_termica_dal_pannello():
    # D17 (04/11): modello come lo produce «Nuovo» + «+ ΔT»: alfa_t e h presenti, schema 1.2
    m = modello("C1_trave_appoggiata")
    m["schema_version"] = "1.2"
    m["materiali"][0]["alfa_t"] = 1.2e-5
    m["sezioni"][0]["h"] = 0.300
    m["casi_di_carico"][0]["carichi_aste"] = []
    m["casi_di_carico"][0]["carichi_termici"] = [{"asta": 1, "dT_u": 0, "dT_g": 10}, {"asta": 2, "dT_u": 0, "dT_g": 10}]
    r = client.post("/api/calcola", json=m)
    assert r.status_code == 200
    assert abs(next(u["uy"] for u in r.json()["risultati"][0]["spostamenti"] if u["nodo"] == 2) + 1.8e-3) < 1e-12
    m["materiali"][0].pop("alfa_t")
    assert "manca alfa_t" in " ".join(client.post("/api/valida", json=m).json()["coerenza"])


def test_trapezio_con_cerniera():
    # C20 (05/11): trapezio parziale sul tratto oltre la cerniera; forza trasmessa e momento contro la statica
    r = client.post("/api/calcola", json=modello("C20_gerber_trapezio")).json()["risultati"][0]
    reaz = {x["nodo"]: x for x in r["reazioni"]}
    assert abs(reaz[3]["Ry"] - 15) < 1e-9 and abs(reaz[1]["Ry"] - 7.5) < 1e-9 and abs(reaz[1]["Mz"] - 30) < 1e-9


def test_identificativi_non_consecutivi_v12():
    # Paola (06/11, esteso il 09/11 a C20 e C21): nodi e aste rinumerati e in ordine inverso danno gli stessi risultati
    for nome in ("C14_termica_incastrata", "C18_termica_appoggiata", "C19_gerber_termica",
                 "C20_gerber_trapezio", "C21_inclinata_trapezio_cedimento"):
        m = modello(nome)
        base = client.post("/api/calcola", json=m).json()["risultati"][0]
        n2 = {n["id"]: 10 * n["id"] + 7 for n in m["nodi"]}
        a2 = {a["id"]: a["id"] + 40 for a in m["aste"]}
        r = copy.deepcopy(m)
        r["nodi"] = [dict(n, id=n2[n["id"]]) for n in reversed(m["nodi"])]
        r["aste"] = [dict(a, id=a2[a["id"]], nodo_i=n2[a["nodo_i"]], nodo_j=n2[a["nodo_j"]]) for a in reversed(m["aste"])]
        r["vincoli"] = [dict(v, nodo=n2[v["nodo"]]) for v in m["vincoli"]]
        for c in r["casi_di_carico"]:
            for t in c.get("carichi_termici", []) + c.get("carichi_aste", []):
                t["asta"] = a2[t["asta"]]
            for d in c.get("cedimenti", []):
                d["nodo"] = n2[d["nodo"]]
        ris = client.post("/api/calcola", json=r).json()["risultati"][0]
        sp = {u["nodo"]: u for u in ris["spostamenti"]}
        for u in base["spostamenti"]:
            assert all(abs(u[k] - sp[n2[u["nodo"]]][k]) < 1e-12 for k in ("ux", "uy", "rz")), nome
        rot = {x["asta"]: x for x in ris["rotazioni_aste"]}
        for x in base["rotazioni_aste"]:
            assert abs(x["phi_j"] - rot[a2[x["asta"]]]["phi_j"]) < 1e-12, nome


def test_assiale_rigida_indipendente_dalla_scala():
    # punto 46, v0.5 (07/11): con deformabilità assiale trascurata il momento al piede di C3 resta esatto
    # anche con luci 25 volte maggiori (con A × 10⁶ l'errore saliva a 9·10⁻⁶)
    m = modello("C3_portale_forza_orizzontale")
    Mp = 21.98943851708158 * 25
    for n in m["nodi"]:
        n["x"] *= 25
        n["y"] *= 25
    r = client.post("/api/calcola", json=m).json()["risultati"][0]
    assert abs(next(x["Mz"] for x in r["reazioni"] if x["nodo"] == 1) - Mp) / Mp < 1e-7


def test_validatore_rapido_concorde():
    # punto 56 (08/11): la via rapida e jsonschema danno lo stesso esito; un modello non valido ha i messaggi completi
    if servizio.VALIDATORE_RAPIDO is None:
        return
    for nome in ("C1_trave_appoggiata", "C14_termica_incastrata", "C20_gerber_trapezio"):
        m = modello(nome)
        assert servizio.VALIDATORE_RAPIDO.is_valid(m) and servizio.VALIDATORE.is_valid(m)
        m["sezioni"][0]["A"] = -1
        assert not servizio.VALIDATORE_RAPIDO.is_valid(m) and not servizio.VALIDATORE.is_valid(m)
        v = client.post("/api/valida", json=m).json()
        assert not v["valido"] and any("sezioni" in e["percorso"] for e in v["schema"])


def test_validatori_discordi():
    # punto 58 (09/11): se la via rapida rifiutasse un modello valido per jsonschema, il modello è accettato
    # e la discordanza registrata. Si simula con una via rapida che rifiuta tutto
    class Rifiuta:
        def is_valid(self, m):
            return False
    originale, servizio.VALIDATORE_RAPIDO = servizio.VALIDATORE_RAPIDO, Rifiuta()
    try:
        n = len(servizio.ANOMALIE_VALIDAZIONE)
        r = client.post("/api/calcola", json=modello("C1_trave_appoggiata"))
        assert r.status_code == 200 and len(servizio.ANOMALIE_VALIDAZIONE) == min(n + 1, 100)
        # punto 60 (10/11): l'elenco non supera le 100 voci
        for _ in range(105):
            servizio.errori_schema(modello("C1_trave_appoggiata"))
        assert len(servizio.ANOMALIE_VALIDAZIONE) == 100
    finally:
        servizio.VALIDATORE_RAPIDO = originale


def test_combinazione_carico_e_termica():
    # Natalia, 11/11: C23 dal servizio. La combinazione è la somma pesata dei casi G e T, punto per punto,
    # e un caso T con dT_u ma deformabilità assiale trascurata resta rifiutato anche dentro una combinazione
    m = modello("C23_combinazione_termica")
    g, t = client.post("/api/calcola", json=m).json()["risultati"]
    c = client.post("/api/calcola?combinazione=SLU1", json=m).json()["risultati"][0]
    for k in ("N", "V", "M"):
        for sg, st, sc in zip(g["sollecitazioni"], t["sollecitazioni"], c["sollecitazioni"]):
            assert all(abs(1.3 * a + 0.9 * b - x) < 1e-6 for a, b, x in zip(sg[k], st[k], sc[k]))
    m["analisi"]["deformabilita_assiale"] = False
    r = client.post("/api/calcola?combinazione=SLU1", json=m)
    assert r.status_code == 422 and any("ΔT uniforme" in e for e in r.json()["detail"]["coerenza"])


def test_combinazione_due_piani():
    # C24: le colonne uguali collegate da travi incernierate rigide si dividono a metà il vento
    c = client.post("/api/calcola?combinazione=SLU1", json=modello("C24_due_piani_combinazione")).json()["risultati"][0]
    rz = {x["nodo"]: x for x in c["reazioni"]}
    assert abs(rz[1]["Rx"] + 18.75) < 1e-6 and abs(rz[2]["Rx"] + 18.75) < 1e-6
    assert abs(rz[1]["Ry"] - 195) < 1e-6 and abs(rz[2]["Ry"] - 195) < 1e-6


def test_tre_cerniere_cedimento_isostatico():
    # Natalia, 12/11: su C25, isostatico, il cedimento non cambia reazioni né momenti, sposta solo il piede
    m = modello("C25_tre_cerniere_trapezio_cedimento")
    con = client.post("/api/calcola", json=m).json()["risultati"][0]
    m["casi_di_carico"][0]["cedimenti"] = []
    senza = client.post("/api/calcola", json=m).json()["risultati"][0]
    for a, b in zip(con["reazioni"], senza["reazioni"]):
        assert all(abs(a[k] - b[k]) < 1e-6 for k in ("Rx", "Ry"))
    for a, b in zip(con["sollecitazioni"], senza["sollecitazioni"]):
        assert all(abs(x - y) < 1e-6 for x, y in zip(a["M"], b["M"]))
    uy = {u["nodo"]: u["uy"] for u in con["spostamenti"]}
    assert abs(uy[5] + 0.010) < 1e-12
    # cedimento su una rotazione non vincolata (piede incernierato): rifiutato
    m["casi_di_carico"][0]["cedimenti"] = [{"nodo": 5, "rz": 0.001}]
    r = client.post("/api/valida", json=m).json()
    assert not r["valido"] and any("rz" in e for e in r["coerenza"])


def test_dati_errati():
    # Natalia, 13/11: nessun dato errato deve dare un errore interno (500)
    r = client.post("/api/calcola", content=b'{"nodi": [', headers={"content-type": "application/json"})
    assert r.status_code == 422
    for campo, valore in (("x", float("nan")), ("x", float("inf"))):
        m = modello("C1_trave_appoggiata")
        m["nodi"][1][campo] = valore
        r = client.post("/api/calcola", content=json.dumps(m).encode(), headers={"content-type": "application/json"})
        assert r.status_code == 422 and "non finito" in r.json()["detail"]["schema"][0]["messaggio"]
    m = modello("C1_trave_appoggiata")
    m["nodi"][1]["x"] = 0
    r = client.post("/api/calcola", json=m)
    assert r.status_code == 422 and "lunghezza nulla" in r.json()["detail"]["coerenza"][0]


def test_esponente_a_tre_cifre():
    # 13/11: il Fortran scriveva -2.24+296 senza la E per esponenti oltre 99; ora sempre E+ddd
    m = modello("C1_trave_appoggiata")
    m["casi_di_carico"][0]["carichi_aste"][0]["q"] = 1e300
    r = client.post("/api/calcola", json=m)
    assert r.status_code == 200
    uy = max(abs(u["uy"]) for u in r.json()["risultati"][0]["spostamenti"])
    assert 1e290 < uy < 1e300


def test_avvisi_di_plausibilita():
    # punto 76 (14/11): oltre le soglie il calcolo procede ma la risposta porta un avviso; sotto, nessun avviso
    m = modello("C1_trave_appoggiata")
    assert "avvisi" not in client.post("/api/calcola", json=m).json()
    m["casi_di_carico"][0]["carichi_aste"][0]["q"] = -1e9
    r = client.post("/api/calcola", json=m)
    assert r.status_code == 200 and "unità sbagliate" in r.json()["avvisi"][0]
    m = modello("C1_trave_appoggiata")
    for n in m["nodi"]:
        n["x"] *= 1e4
    v = client.post("/api/valida", json=m).json()
    assert v["valido"] and "coordinate" in v["avvisi"][0]


def test_c27_termica_su_travi_isostatiche():
    # 14/11: il ΔT a farfalla sulle travi incernierate di C27 non dà reazioni né momenti, solo la freccia
    m = modello("C27_due_piani_termica")
    t = client.post("/api/calcola?caso=T", json=m).json()["risultati"][0]
    assert all(abs(x[k]) < 1e-6 for x in t["reazioni"] for k in ("Rx", "Ry", "Mz"))
    assert all(abs(v) < 1e-6 for s in t["sollecitazioni"] for v in s["M"])
    uy = {u["nodo"]: u["uy"] for u in t["spostamenti"]}
    assert abs(uy[7] + 1.2e-5 * 20 / 0.3 * 36 / 8) < 1e-9


def test_limite_nodi_accettato():
    # Natalia (08/11): esattamente MAX_NODI nodi è ancora ammesso, uno in più no (geometria di C20 ripetuta)
    m = modello("C20_gerber_trapezio")
    m["nodi"] = [{"id": i, "x": float(i), "y": 0.0} for i in range(1, servizio.MAX_NODI + 1)]
    m["aste"] = [{"id": i, "nodo_i": i, "nodo_j": i + 1, "materiale": "S275", "sezione": "IPE300"} for i in range(1, 4)]
    assert not any("troppo grande" in e for e in servizio.errori_coerenza(m))
    m["nodi"].append({"id": servizio.MAX_NODI + 1, "x": -1.0, "y": 0.0})
    assert any("troppo grande" in e for e in servizio.errori_coerenza(m))


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
