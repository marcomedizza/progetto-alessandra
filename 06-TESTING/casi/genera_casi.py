"""Genera i casi di prova (modelli secondo DATA_SCHEMA.json v1.0; C11–C13 v1.1) e i valori attesi
calcolati con formule chiuse di scienza delle costruzioni.

Uso:  python3 genera_casi.py      (scrive i file C*.json e C*.atteso.json in questa cartella)
"""

import json
import os

QUI = os.path.dirname(os.path.abspath(__file__))

E_ACC = 2.10e8  # kN/m², acciaio
# Profili europei laminati (valori da sagomario, da ricontrollare sulla tabella del produttore)
IPE300 = {"id": "IPE300", "nome": "IPE 300", "A": 53.81e-4, "I": 8356e-8, "W": 557.1e-6, "fonte": "sagomario profili IPE, asse forte"}
HEA200 = {"id": "HEA200", "nome": "HE 200 A", "A": 53.83e-4, "I": 3692e-8, "W": 388.6e-6, "fonte": "sagomario profili HE A, asse forte"}
ACC = {"id": "S275", "nome": "Acciaio S275", "tipo": "acciaio", "E": E_ACC, "peso_specifico": 78.5}


def base(id_, nome, descr):
    return {
        "schema_version": "1.0",
        "progetto": {"id": id_, "nome": nome, "descrizione": descr, "autore": "Valentina (casi di prova)",
                     "data": "2026-10-26", "tipo_modello": "telaio_piano", "unita": {"lunghezza": "m", "forza": "kN"}},
        "materiali": [ACC],
    }


def scrivi(nome, dati):
    with open(os.path.join(QUI, nome), "w", encoding="utf-8") as fh:
        json.dump(dati, fh, indent=2, ensure_ascii=False)
        fh.write("\n")


def c1():
    L, q = 6.0, 10.0
    EI = E_ACC * IPE300["I"]
    m = base("C1", "Trave appoggiata, carico uniforme", "IPE 300, L = 6 m, q = 10 kN/m verso il basso. Nodo intermedio in mezzeria.")
    m.update({
        "nodi": [{"id": 1, "x": 0, "y": 0}, {"id": 2, "x": 3, "y": 0}, {"id": 3, "x": 6, "y": 0}],
        "sezioni": [IPE300],
        "aste": [{"id": 1, "nodo_i": 1, "nodo_j": 2, "materiale": "S275", "sezione": "IPE300"},
                 {"id": 2, "nodo_i": 2, "nodo_j": 3, "materiale": "S275", "sezione": "IPE300"}],
        "vincoli": [{"nodo": 1, "ux": True, "uy": True}, {"nodo": 3, "uy": True}],
        "casi_di_carico": [{"id": "Q", "nome": "Carico uniforme", "categoria": "Q", "carichi_aste": [
            {"asta": 1, "tipo": "distribuito_uniforme", "direzione": "globale_y", "q": -q},
            {"asta": 2, "tipo": "distribuito_uniforme", "direzione": "globale_y", "q": -q}]}],
    })
    atteso = {"caso": "Q", "formule": {
        "reazioni": "R = qL/2",
        "momento in mezzeria": "M = qL²/8",
        "freccia in mezzeria": "f = 5qL⁴/(384EI)",
        "rotazione agli appoggi": "θ = qL³/(24EI)"},
        "valori": [
            {"grandezza": "Ry nodo 1", "valore": q * L / 2, "unita": "kN"},
            {"grandezza": "Ry nodo 3", "valore": q * L / 2, "unita": "kN"},
            {"grandezza": "M asta 1 x=3 (mezzeria)", "valore": q * L ** 2 / 8, "unita": "kNm"},
            {"grandezza": "uy nodo 2", "valore": -5 * q * L ** 4 / (384 * EI), "unita": "m"},
            {"grandezza": "rz nodo 1", "valore": -q * L ** 3 / (24 * EI), "unita": "rad"},
            {"grandezza": "V asta 1 x=0", "valore": q * L / 2, "unita": "kN"}]}
    return m, atteso


def c2():
    L, P = 3.0, 10.0
    EI = E_ACC * HEA200["I"]
    m = base("C2", "Mensola, carico in punta", "HE 200 A, L = 3 m, P = 10 kN verso il basso all'estremo libero.")
    m.update({
        "nodi": [{"id": 1, "x": 0, "y": 0}, {"id": 2, "x": 3, "y": 0}],
        "sezioni": [HEA200],
        "aste": [{"id": 1, "nodo_i": 1, "nodo_j": 2, "materiale": "S275", "sezione": "HEA200"}],
        "vincoli": [{"nodo": 1, "ux": True, "uy": True, "rz": True}],
        "casi_di_carico": [{"id": "Q", "nome": "Forza in punta", "categoria": "Q", "carichi_nodali": [{"nodo": 2, "Fy": -P}]}],
    })
    atteso = {"caso": "Q", "formule": {
        "reazione verticale": "R = P", "momento d'incastro": "M = −PL (tende le fibre superiori)",
        "freccia": "f = PL³/(3EI)", "rotazione": "θ = PL²/(2EI)"},
        "valori": [
            {"grandezza": "Ry nodo 1", "valore": P, "unita": "kN"},
            {"grandezza": "Mz nodo 1 (reazione)", "valore": P * L, "unita": "kNm"},
            {"grandezza": "M asta 1 x=0", "valore": -P * L, "unita": "kNm"},
            {"grandezza": "uy nodo 2", "valore": -P * L ** 3 / (3 * EI), "unita": "m"},
            {"grandezza": "rz nodo 2", "valore": -P * L ** 2 / (2 * EI), "unita": "rad"}]}
    return m, atteso


def portale(id_, nome, descr, carichi):
    m = base(id_, nome, descr)
    m.update({
        "nodi": [{"id": 1, "nome": "base sinistra", "x": 0, "y": 0}, {"id": 2, "x": 0, "y": 4},
                 {"id": 3, "x": 6, "y": 4}, {"id": 4, "nome": "base destra", "x": 6, "y": 0}],
        "sezioni": [HEA200, IPE300],
        "aste": [{"id": 1, "nome": "colonna sinistra", "nodo_i": 1, "nodo_j": 2, "materiale": "S275", "sezione": "HEA200"},
                 {"id": 2, "nome": "traverso", "nodo_i": 2, "nodo_j": 3, "materiale": "S275", "sezione": "IPE300"},
                 {"id": 3, "nome": "colonna destra", "nodo_i": 4, "nodo_j": 3, "materiale": "S275", "sezione": "HEA200"}],
        "vincoli": [{"nodo": 1, "ux": True, "uy": True, "rz": True}, {"nodo": 4, "ux": True, "uy": True, "rz": True}],
        "casi_di_carico": [carichi],
        "analisi": {"tipo": "statica_lineare", "deformabilita_assiale": False, "punti_diagramma": 11},
    })
    return m


def k_portale():
    h, L = 4.0, 6.0
    return (IPE300["I"] / L) / (HEA200["I"] / h)


def c3():
    H, h = 20.0, 4.0
    k = k_portale()
    m = portale("C3", "Portale incastrato, forza orizzontale", "Colonne HE 200 A h = 4 m, traverso IPE 300 L = 6 m, H = 20 kN al nodo 2. Deformabilità assiale trascurata.",
                {"id": "H", "nome": "Forza orizzontale", "categoria": "vento", "carichi_nodali": [{"nodo": 2, "Fx": H}]})
    Mb = H * h / 2 * (3 * k + 1) / (6 * k + 1)
    Mt = H * h / 2 * 3 * k / (6 * k + 1)
    atteso = {"caso": "H", "formule": {
        "rapporto di rigidezza": "k = (Ib/L)/(Ic/h)",
        "momento al piede": "Mb = (Hh/2)(3k+1)/(6k+1)",
        "momento in testa": "Mt = (Hh/2)·3k/(6k+1)",
        "taglio per colonna": "V = H/2 (colonne uguali)",
        "nota": "formule con aste assialmente indeformabili; il modello imposta deformabilita_assiale = false"},
        "k": k,
        "valori": [
            {"grandezza": "Rx nodo 1", "valore": -H / 2, "unita": "kN"},
            {"grandezza": "Rx nodo 4", "valore": -H / 2, "unita": "kN"},
            {"grandezza": "Mz nodo 1 (reazione)", "valore": Mb, "unita": "kNm"},
            {"grandezza": "Mz nodo 4 (reazione)", "valore": Mb, "unita": "kNm"},
            {"grandezza": "|M| asta 1 x=0", "valore": Mb, "unita": "kNm"},
            {"grandezza": "|M| asta 1 x=h", "valore": Mt, "unita": "kNm"},
            {"grandezza": "Ry nodo 1 + Ry nodo 4", "valore": 0.0, "unita": "kN"}]}
    return m, atteso


def c4():
    q, L = 30.0, 6.0
    k = k_portale()
    m = portale("C4", "Portale incastrato, carico uniforme sul traverso", "Colonne HE 200 A h = 4 m, traverso IPE 300 L = 6 m, q = 30 kN/m verso il basso. Deformabilità assiale trascurata.",
                {"id": "G", "nome": "Carico uniforme", "categoria": "G2", "carichi_aste": [
                    {"asta": 2, "tipo": "distribuito_uniforme", "direzione": "globale_y", "q": -q}]})
    Mc = q * L ** 2 / 12 * 2 / (k + 2)
    Mb = Mc / 2
    Mm = q * L ** 2 / 8 - Mc
    Hs = (Mc + Mb) / 4.0
    atteso = {"caso": "G", "formule": {
        "momento d'angolo": "Mc = (qL²/12)·2/(k+2), k = (Ib/L)/(Ic/h)",
        "momento al piede": "Mb = Mc/2 (trasmissione 1/2, nodi senza traslazione per simmetria)",
        "momento in mezzeria del traverso": "Mm = qL²/8 − Mc",
        "spinta orizzontale al piede": "H = (Mc + Mb)/h",
        "nota": "metodo delle rotazioni, aste assialmente indeformabili"},
        "k": k,
        "valori": [
            {"grandezza": "Ry nodo 1", "valore": q * L / 2, "unita": "kN"},
            {"grandezza": "Ry nodo 4", "valore": q * L / 2, "unita": "kN"},
            {"grandezza": "|Rx| nodo 1", "valore": Hs, "unita": "kN"},
            {"grandezza": "|M| asta 2 x=0 (angolo)", "valore": Mc, "unita": "kNm"},
            {"grandezza": "M asta 2 x=L/2 (mezzeria)", "valore": Mm, "unita": "kNm"},
            {"grandezza": "|Mz| nodo 1 (reazione)", "valore": Mb, "unita": "kNm"}]}
    return m, atteso


def c5():
    m = base("C5", "Telaio a due piani", "Una campata L = 6 m, due piani h = 3.5 m. Colonne HE 200 A, travi IPE 300. q = 25 kN/m sulle travi, H = 10 kN al primo piano e 15 kN al secondo.")
    m.update({
        "nodi": [{"id": 1, "x": 0, "y": 0}, {"id": 2, "x": 6, "y": 0},
                 {"id": 3, "x": 0, "y": 3.5}, {"id": 4, "x": 6, "y": 3.5},
                 {"id": 5, "x": 0, "y": 7}, {"id": 6, "x": 6, "y": 7}],
        "sezioni": [HEA200, IPE300],
        "aste": [{"id": 1, "nodo_i": 1, "nodo_j": 3, "materiale": "S275", "sezione": "HEA200"},
                 {"id": 2, "nodo_i": 2, "nodo_j": 4, "materiale": "S275", "sezione": "HEA200"},
                 {"id": 3, "nodo_i": 3, "nodo_j": 5, "materiale": "S275", "sezione": "HEA200"},
                 {"id": 4, "nodo_i": 4, "nodo_j": 6, "materiale": "S275", "sezione": "HEA200"},
                 {"id": 5, "nodo_i": 3, "nodo_j": 4, "materiale": "S275", "sezione": "IPE300"},
                 {"id": 6, "nodo_i": 5, "nodo_j": 6, "materiale": "S275", "sezione": "IPE300"}],
        "vincoli": [{"nodo": 1, "ux": True, "uy": True, "rz": True}, {"nodo": 2, "ux": True, "uy": True, "rz": True}],
        "casi_di_carico": [{"id": "C", "nome": "Verticali + orizzontali", "categoria": "altro",
                            "carichi_nodali": [{"nodo": 3, "Fx": 10}, {"nodo": 5, "Fx": 15}],
                            "carichi_aste": [{"asta": 5, "tipo": "distribuito_uniforme", "direzione": "globale_y", "q": -25},
                                             {"asta": 6, "tipo": "distribuito_uniforme", "direzione": "globale_y", "q": -25}]}],
        "analisi": {"tipo": "statica_lineare", "deformabilita_assiale": True, "punti_diagramma": 11},
    })
    atteso = {"caso": "C", "formule": {
        "equilibrio verticale": "Ry1 + Ry2 = 2·q·L",
        "equilibrio orizzontale": "Rx1 + Rx2 = −(H1 + H2)",
        "equilibrio alla rotazione attorno al nodo 1": "Mz1 + Mz2 + Ry2·L − H1·3.5 − H2·7 − 2·qL·L/2 = 0",
        "nota": "per la ripartizione interna non esiste formula chiusa semplice: valori numerici dal risolutore di riferimento, da confermare con un programma commerciale"},
        "valori": [
            {"grandezza": "Ry nodo 1 + Ry nodo 2", "valore": 2 * 25 * 6, "unita": "kN"},
            {"grandezza": "Rx nodo 1 + Rx nodo 2", "valore": -25.0, "unita": "kN"},
            {"grandezza": "momento risultante attorno al nodo 1", "valore": 0.0, "unita": "kNm"}]}
    return m, atteso


def trave(id_, nome, descr, nodi, aste, vincoli, caso, punti):
    m = base(id_, nome, descr)
    m.update({"nodi": nodi, "sezioni": [IPE300], "aste": aste, "vincoli": vincoli, "casi_di_carico": [caso],
              "analisi": {"tipo": "statica_lineare", "deformabilita_assiale": True, "punti_diagramma": punti}})
    return m


def c6():
    q = 10.0
    m = trave("C6", "Trave Gerber, carico uniforme",
              "IPE 300: incastro in x = 0, cerniera interna in x = 4 m, appoggio scorrevole in x = 6 m; q = 10 kN/m su tutta la lunghezza.",
              [{"id": 1, "x": 0, "y": 0}, {"id": 2, "x": 4, "y": 0}, {"id": 3, "x": 6, "y": 0}],
              [{"id": 1, "nodo_i": 1, "nodo_j": 2, "materiale": "S275", "sezione": "IPE300", "svincoli": {"rz_j": True}},
               {"id": 2, "nodo_i": 2, "nodo_j": 3, "materiale": "S275", "sezione": "IPE300"}],
              [{"nodo": 1, "ux": True, "uy": True, "rz": True}, {"nodo": 3, "uy": True}],
              {"id": "Q", "nome": "Carico uniforme", "categoria": "Q", "carichi_aste": [
                  {"asta": 1, "tipo": "distribuito_uniforme", "direzione": "globale_y", "q": -q},
                  {"asta": 2, "tipo": "distribuito_uniforme", "direzione": "globale_y", "q": -q}]}, 5)
    Rs = q * 2 / 2               # tratto appoggiato 4–6: reazione e forza trasmessa alla cerniera
    EI = E_ACC * IPE300["I"]
    v2 = (q * 4 ** 4 / 8 + Rs * 4 ** 3 / 3) / EI      # abbassamento della punta della mensola
    th1 = -(q * 4 ** 3 / 6 + Rs * 4 ** 2 / 2) / EI    # rotazione della mensola alla cerniera (oraria)
    th2 = v2 / 2 - q * 2 ** 3 / (24 * EI)             # tratto appoggiato: corda + rotazione d'appoggio
    atteso = {"caso": "Q", "formule": {
        "tratto appoggiato (2 m)": "R3 = q·2/2; forza in cerniera = q·2/2; M max = q·2²/8 in x = 5",
        "mensola (4 m) con carico in punta dalla cerniera": "R1 = q·4 + Rs; M1 = −(q·4²/2 + Rs·4)",
        "cerniera": "M = 0 in x = 4",
        "spostamenti (D8)": "v2 = q·4⁴/(8EI) + Rs·4³/(3EI); φ mensola = −(q·4³/(6EI) + Rs·4²/(2EI)); φ tratto appoggiato = v2/2 − q·2³/(24EI)"},
        "valori": [
            {"grandezza": "Ry nodo 3", "valore": Rs, "unita": "kN"},
            {"grandezza": "Ry nodo 1", "valore": q * 4 + Rs, "unita": "kN"},
            {"grandezza": "Mz nodo 1 (reazione)", "valore": q * 4 ** 2 / 2 + Rs * 4, "unita": "kNm"},
            {"grandezza": "M asta 1 x=0", "valore": -(q * 4 ** 2 / 2 + Rs * 4), "unita": "kNm"},
            {"grandezza": "M asta 1 x=4 (cerniera)", "valore": 0.0, "unita": "kNm"},
            {"grandezza": "M asta 2 x=1 (mezzeria tratto appoggiato)", "valore": q * 2 ** 2 / 8, "unita": "kNm"},
            {"grandezza": "uy nodo 2 (cerniera)", "valore": -v2, "unita": "m"},
            {"grandezza": "φj asta 1 (mensola alla cerniera)", "valore": th1, "unita": "rad"},
            {"grandezza": "rz nodo 2 (tratto appoggiato alla cerniera)", "valore": th2, "unita": "rad"}]}
    return m, atteso


def c7():
    P, L, a = 20.0, 6.0, 2.0
    b = L - a
    EI = E_ACC * IPE300["I"]
    m = trave("C7", "Trave appoggiata, carico concentrato fuori mezzeria",
              "IPE 300, L = 6 m, P = 20 kN verso il basso a 2 m dall'appoggio sinistro, applicato sull'asta.",
              [{"id": 1, "x": 0, "y": 0}, {"id": 2, "x": 6, "y": 0}],
              [{"id": 1, "nodo_i": 1, "nodo_j": 2, "materiale": "S275", "sezione": "IPE300"}],
              [{"nodo": 1, "ux": True, "uy": True}, {"nodo": 2, "uy": True}],
              {"id": "P", "nome": "Forza concentrata", "categoria": "Q", "carichi_aste": [
                  {"asta": 1, "tipo": "concentrato", "direzione": "globale_y", "P": -P, "a": a}]}, 4)
    atteso = {"caso": "P", "formule": {
        "reazioni": "R1 = P·b/L, R2 = P·a/L", "momento sotto il carico": "M = P·a·b/L",
        "rotazioni agli appoggi": "θ1 = P·a·b·(L+b)/(6EIL), θ2 = P·a·b·(L+a)/(6EIL)"},
        "valori": [
            {"grandezza": "Ry nodo 1", "valore": P * b / L, "unita": "kN"},
            {"grandezza": "Ry nodo 2", "valore": P * a / L, "unita": "kN"},
            {"grandezza": "M asta 1 x=2 (sotto il carico)", "valore": P * a * b / L, "unita": "kNm"},
            {"grandezza": "rz nodo 1", "valore": -P * a * b * (L + b) / (6 * EI * L), "unita": "rad"},
            {"grandezza": "rz nodo 2", "valore": P * a * b * (L + a) / (6 * EI * L), "unita": "rad"}]}
    return m, atteso


def c8():
    q, L, k = 10.0, 6.0, 1000.0
    EI = E_ACC * IPE300["I"]
    m = trave("C8", "Trave appoggiata con molla in mezzeria",
              "IPE 300, L = 6 m, q = 10 kN/m; in mezzeria molla verticale ky = 1000 kN/m.",
              [{"id": 1, "x": 0, "y": 0}, {"id": 2, "x": 3, "y": 0}, {"id": 3, "x": 6, "y": 0}],
              [{"id": 1, "nodo_i": 1, "nodo_j": 2, "materiale": "S275", "sezione": "IPE300"},
               {"id": 2, "nodo_i": 2, "nodo_j": 3, "materiale": "S275", "sezione": "IPE300"}],
              [{"nodo": 1, "ux": True, "uy": True}, {"nodo": 2, "molle": {"ky": k}}, {"nodo": 3, "uy": True}],
              {"id": "Q", "nome": "Carico uniforme", "categoria": "Q", "carichi_aste": [
                  {"asta": 1, "tipo": "distribuito_uniforme", "direzione": "globale_y", "q": -q},
                  {"asta": 2, "tipo": "distribuito_uniforme", "direzione": "globale_y", "q": -q}]}, 3)
    d0 = 5 * q * L ** 4 / (384 * EI)                   # freccia senza molla
    Rs = d0 / (1 / k + L ** 3 / (48 * EI))             # congruenza in mezzeria
    atteso = {"caso": "Q", "formule": {
        "freccia senza molla": "δ0 = 5qL⁴/(384EI)",
        "forza nella molla": "Rs = δ0 / (1/k + L³/(48EI))",
        "freccia in mezzeria": "δ = Rs/k",
        "reazioni agli appoggi": "R = (qL − Rs)/2",
        "momento in mezzeria": "M = qL²/8 − Rs·L/4"},
        "valori": [
            {"grandezza": "Ry nodo 2 (molla)", "valore": Rs, "unita": "kN"},
            {"grandezza": "uy nodo 2", "valore": -Rs / k, "unita": "m"},
            {"grandezza": "Ry nodo 1", "valore": (q * L - Rs) / 2, "unita": "kN"},
            {"grandezza": "M asta 1 x=3 (mezzeria)", "valore": q * L ** 2 / 8 - Rs * L / 4, "unita": "kNm"}]}
    return m, atteso


def c9():
    H, h, L, k = 20.0, 4.0, 6.0, 5000.0
    m = base("C9", "Portale a tre cerniere con molla al piede",
             "Colonne HE 200 A h = 4 m, traverso IPE 300 L = 6 m con cerniera interna in mezzeria. Piede sinistro a cerniera, "
             "piede destro con ux impedito e molla verticale ky = 5000 kN/m. H = 20 kN al nodo 2. Struttura isostatica.")
    m.update({
        "nodi": [{"id": 1, "x": 0, "y": 0}, {"id": 2, "x": 0, "y": h}, {"id": 5, "nome": "cerniera", "x": L / 2, "y": h},
                 {"id": 3, "x": L, "y": h}, {"id": 4, "x": L, "y": 0}],
        "sezioni": [HEA200, IPE300],
        "aste": [{"id": 1, "nodo_i": 1, "nodo_j": 2, "materiale": "S275", "sezione": "HEA200"},
                 {"id": 2, "nodo_i": 2, "nodo_j": 5, "materiale": "S275", "sezione": "IPE300", "svincoli": {"rz_j": True}},
                 {"id": 4, "nodo_i": 5, "nodo_j": 3, "materiale": "S275", "sezione": "IPE300"},
                 {"id": 3, "nodo_i": 4, "nodo_j": 3, "materiale": "S275", "sezione": "HEA200"}],
        "vincoli": [{"nodo": 1, "ux": True, "uy": True}, {"nodo": 4, "ux": True, "molle": {"ky": k}}],
        "casi_di_carico": [{"id": "H", "nome": "Forza orizzontale", "categoria": "vento", "carichi_nodali": [{"nodo": 2, "Fx": H}]}],
        "analisi": {"tipo": "statica_lineare", "deformabilita_assiale": True, "punti_diagramma": 5},
    })
    Rby = H * h / L
    Rbx = -L * Rby / (2 * h)
    atteso = {"caso": "H", "formule": {
        "rotazione attorno al nodo 1": "Ry4·L − H·h = 0 → Ry4 = H·h/L",
        "equilibrio verticale": "Ry1 = −Ry4",
        "momento nullo in cerniera (parte destra)": "(L/2)·Ry4 + h·Rx4 = 0 → Rx4 = −L·Ry4/(2h) = −H/2",
        "equilibrio orizzontale": "Rx1 = −H − Rx4",
        "momento in testa alla colonna destra": "|M| = |Rx4|·h",
        "molla": "uy4 = −Ry4/k (la struttura è isostatica: la molla non cambia le reazioni)"},
        "valori": [
            {"grandezza": "Ry nodo 4 (molla)", "valore": Rby, "unita": "kN"},
            {"grandezza": "Ry nodo 1", "valore": -Rby, "unita": "kN"},
            {"grandezza": "Rx nodo 4", "valore": Rbx, "unita": "kN"},
            {"grandezza": "Rx nodo 1", "valore": -H - Rbx, "unita": "kN"},
            {"grandezza": "uy nodo 4", "valore": -Rby / k, "unita": "m"},
            {"grandezza": "|M| asta 3 x=h (testa colonna destra)", "valore": abs(Rbx) * h, "unita": "kNm"},
            {"grandezza": "M asta 2 x=L/2 (cerniera)", "valore": 0.0, "unita": "kNm"}]}
    return m, atteso


def c10():
    q, P, L, a = 10.0, 20.0, 6.0, 2.0
    b = L - a
    gG, gQ = 1.3, 1.5
    m = trave("C10", "Trave appoggiata, combinazione SLU di due casi",
              "IPE 300, L = 6 m. Caso G2: q = 10 kN/m; caso Q: P = 20 kN a 2 m dall'appoggio sinistro. Combinazione SLU 1,3·G2 + 1,5·Q (NTC 2018 §2.5.3).",
              [{"id": 1, "x": 0, "y": 0}, {"id": 2, "x": 6, "y": 0}],
              [{"id": 1, "nodo_i": 1, "nodo_j": 2, "materiale": "S275", "sezione": "IPE300"}],
              [{"nodo": 1, "ux": True, "uy": True}, {"nodo": 2, "uy": True}],
              {"id": "G2", "nome": "Permanenti portati", "categoria": "G2", "carichi_aste": [
                  {"asta": 1, "tipo": "distribuito_uniforme", "direzione": "globale_y", "q": -q}]}, 4)
    m["casi_di_carico"].append({"id": "Q", "nome": "Variabile concentrato", "categoria": "Q", "carichi_aste": [
        {"asta": 1, "tipo": "concentrato", "direzione": "globale_y", "P": -P, "a": a}]})
    m["combinazioni"] = [{"id": "SLU1", "nome": "SLU 1,3·G2 + 1,5·Q", "tipo": "SLU", "coefficienti": {"G2": gG, "Q": gQ}}]
    MG = q * a * b / 2                  # momento del carico uniforme nella sezione x = a
    MQ = P * a * b / L
    atteso = {"caso": "SLU1", "formule": {
        "reazione sinistra": "R1 = 1,3·qL/2 + 1,5·P·b/L",
        "reazione destra": "R2 = 1,3·qL/2 + 1,5·P·a/L",
        "momento sotto il carico": "M(a) = 1,3·q·a·b/2 + 1,5·P·a·b/L",
        "nota": "verifica della sovrapposizione lineare dei casi nelle combinazioni"},
        "valori": [
            {"grandezza": "Ry nodo 1", "valore": gG * q * L / 2 + gQ * P * b / L, "unita": "kN"},
            {"grandezza": "Ry nodo 2", "valore": gG * q * L / 2 + gQ * P * a / L, "unita": "kN"},
            {"grandezza": "M asta 1 x=2 (sotto il carico)", "valore": gG * MG + gQ * MQ, "unita": "kNm"}]}
    return m, atteso


def v11(m):
    m["schema_version"] = "1.1"
    m["progetto"]["data"] = "2026-10-31"
    return m


def c11():
    L, d = 6.0, 0.010
    EI = E_ACC * IPE300["I"]
    m = v11(trave("C11", "Trave continua, cedimento dell'appoggio centrale",
                  "IPE 300, due campate da 6 m su tre appoggi, nessun carico; l'appoggio centrale cede di 10 mm verso il basso (schema v1.1, Carla).",
                  [{"id": 1, "x": 0, "y": 0}, {"id": 2, "x": 6, "y": 0}, {"id": 3, "x": 12, "y": 0}],
                  [{"id": 1, "nodo_i": 1, "nodo_j": 2, "materiale": "S275", "sezione": "IPE300"},
                   {"id": 2, "nodo_i": 2, "nodo_j": 3, "materiale": "S275", "sezione": "IPE300"}],
                  [{"nodo": 1, "ux": True, "uy": True}, {"nodo": 2, "uy": True}, {"nodo": 3, "uy": True}],
                  {"id": "CED", "nome": "Cedimento appoggio centrale", "categoria": "altro",
                   "cedimenti": [{"nodo": 2, "uy": -d}]}, 7))
    F = 48 * EI * d / (2 * L) ** 3   # forza in mezzeria di una trave appoggiata di luce 2L che dà la freccia d
    atteso = {"caso": "CED", "formule": {
        "reazione dell'appoggio centrale": "F = 48·EI·δ/(2L)³, diretta verso il basso",
        "appoggi di estremità": "RA = RC = F/2",
        "momento sull'appoggio centrale": "MB = F·2L/4, fibre tese in basso",
        "rotazione in A": "φA = −F·(2L)²/(16EI)"},
        "valori": [
            {"grandezza": "Ry nodo 2", "valore": -F, "unita": "kN"},
            {"grandezza": "Ry nodo 1", "valore": F / 2, "unita": "kN"},
            {"grandezza": "Ry nodo 3", "valore": F / 2, "unita": "kN"},
            {"grandezza": "M asta 1 x=6 (appoggio centrale)", "valore": F * 2 * L / 4, "unita": "kNm"},
            {"grandezza": "uy nodo 2 (cedimento impresso)", "valore": -d, "unita": "m"},
            {"grandezza": "rz nodo 1", "valore": -F * (2 * L) ** 2 / (16 * EI), "unita": "rad"}]}
    return m, atteso


def c12():
    L, a, b, q1, q2 = 6.0, 1.0, 4.0, 10.0, 20.0
    m = v11(trave("C12", "Trave appoggiata, carico trapezoidale parziale",
                  "IPE 300, L = 6 m; carico verso il basso da 10 kN/m in x = 1 m a 20 kN/m in x = 4 m (schema v1.1, Daniela).",
                  [{"id": 1, "x": 0, "y": 0}, {"id": 2, "x": 6, "y": 0}],
                  [{"id": 1, "nodo_i": 1, "nodo_j": 2, "materiale": "S275", "sezione": "IPE300"}],
                  [{"nodo": 1, "ux": True, "uy": True}, {"nodo": 2, "uy": True}],
                  {"id": "Q", "nome": "Carico trapezoidale", "categoria": "Q", "carichi_aste": [
                      {"asta": 1, "tipo": "distribuito_trapezio", "direzione": "globale_y", "q_i": -q1, "q_j": -q2, "a": a, "b": b}]}, 7))
    c = b - a
    W = c * (q1 + q2) / 2
    xg = a + c * (q1 + 2 * q2) / (3 * (q1 + q2))          # baricentro del trapezio
    R2 = W * xg / L
    R1 = W - R2
    t = 3 - a                                             # sezione x = 3 m, a 2 m dall'inizio del carico
    M3 = R1 * 3 - (q1 * t ** 2 / 2 + (q2 - q1) / c * t ** 3 / 6)
    atteso = {"caso": "Q", "formule": {
        "risultante": "W = (b − a)·(q1 + q2)/2",
        "baricentro": "xg = a + (b − a)·(q1 + 2q2)/(3(q1 + q2))",
        "reazioni": "R2 = W·xg/L; R1 = W − R2",
        "momento in x = 3": "M = R1·3 − [q1·t²/2 + (q2 − q1)/(b − a)·t³/6], t = 3 − a",
        "momento in x = 4": "M = R2·(L − 4)"},
        "valori": [
            {"grandezza": "Ry nodo 1", "valore": R1, "unita": "kN"},
            {"grandezza": "Ry nodo 2", "valore": R2, "unita": "kN"},
            {"grandezza": "M asta 1 x=1 (inizio del carico)", "valore": R1 * a, "unita": "kNm"},
            {"grandezza": "M asta 1 x=3", "valore": M3, "unita": "kNm"},
            {"grandezza": "M asta 1 x=4 (fine del carico)", "valore": R2 * (L - b), "unita": "kNm"}]}
    return m, atteso


def c13():
    L, q = 6.0, 20.0
    m = v11(trave("C13", "Trave incastrata, carico triangolare",
                  "IPE 300, L = 6 m, incastri alle estremità; carico verso il basso crescente da 0 in x = 0 a 20 kN/m in x = 6 m (schema v1.1, Daniela).",
                  [{"id": 1, "x": 0, "y": 0}, {"id": 2, "x": 6, "y": 0}],
                  [{"id": 1, "nodo_i": 1, "nodo_j": 2, "materiale": "S275", "sezione": "IPE300"}],
                  [{"nodo": 1, "ux": True, "uy": True, "rz": True}, {"nodo": 2, "ux": True, "uy": True, "rz": True}],
                  {"id": "Q", "nome": "Carico triangolare", "categoria": "Q", "carichi_aste": [
                      {"asta": 1, "tipo": "distribuito_trapezio", "direzione": "globale_y", "q_i": 0.0, "q_j": -q, "a": 0.0, "b": L}]}, 7))
    atteso = {"caso": "Q", "formule": {
        "momenti d'incastro": "MA = qL²/30 (lato scarico), MB = qL²/20 (lato carico), fibre tese in alto",
        "reazioni": "RA = 3qL/20, RB = 7qL/20"},
        "valori": [
            {"grandezza": "Ry nodo 1", "valore": 3 * q * L / 20, "unita": "kN"},
            {"grandezza": "Ry nodo 2", "valore": 7 * q * L / 20, "unita": "kN"},
            {"grandezza": "M asta 1 x=0", "valore": -q * L ** 2 / 30, "unita": "kNm"},
            {"grandezza": "M asta 1 x=6", "valore": -q * L ** 2 / 20, "unita": "kNm"}]}
    return m, atteso


if __name__ == "__main__":
    for nome, f in (("C1_trave_appoggiata", c1), ("C2_mensola", c2), ("C3_portale_forza_orizzontale", c3),
                    ("C4_portale_carico_uniforme", c4), ("C5_telaio_due_piani", c5),
                    ("C6_trave_gerber", c6), ("C7_carico_concentrato", c7), ("C8_molla_in_mezzeria", c8),
                    ("C9_portale_tre_cerniere_molla", c9),
                    ("C10_combinazione_slu", c10), ("C11_cedimento_appoggio", c11),
                    ("C12_trapezio_parziale", c12), ("C13_triangolare_incastrata", c13)):
        m, a = f()
        scrivi(nome + ".json", m)
        scrivi(nome + ".atteso.json", a)
        print("scritto", nome)
