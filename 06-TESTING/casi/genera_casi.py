"""Genera i casi di prova (modelli secondo DATA_SCHEMA.json v1.0; C11–C13, C15–C17 v1.1; C14, C18 v1.2) e i valori attesi
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


def c15():
    q, a, b = 10.0, 1.0, 4.0
    m = v11(trave("C15", "Asta inclinata, carico verticale parziale",
                  "IPE 300 da (0; 0) a (4; 3), L = 5 m; cerniera al piede, carrello a scorrimento orizzontale in testa; "
                  "carico verticale di 10 kN/m di lunghezza dell'asta da 1 a 4 m lungo l'asta (schema v1.1, Daniela).",
                  [{"id": 1, "x": 0, "y": 0}, {"id": 2, "x": 4, "y": 3}],
                  [{"id": 1, "nodo_i": 1, "nodo_j": 2, "materiale": "S275", "sezione": "IPE300"}],
                  [{"nodo": 1, "ux": True, "uy": True}, {"nodo": 2, "uy": True}],
                  {"id": "Q", "nome": "Carico parziale", "categoria": "Q", "carichi_aste": [
                      {"asta": 1, "tipo": "distribuito_trapezio", "direzione": "globale_y", "q_i": -q, "q_j": -q, "a": a, "b": b}]}, 11))
    c, s = 0.8, 0.6                  # coseni direttori dell'asta
    W = q * (b - a)                  # risultante verticale
    xg = (a + b) / 2 * c             # ascissa orizzontale del baricentro
    R2 = W * xg / 4.0
    R1 = W - R2
    wy = q * c                       # componente trasversale locale del carico
    M = R1 * c * 2.5 - wy * (2.5 - a) ** 2 / 2
    atteso = {"caso": "Q", "formule": {
        "reazioni verticali": "R2 = W·xg/4 con W = q·(b − a), xg = (a + b)/2·cosα; R1 = W − R2; nessuna reazione orizzontale",
        "momento in s = 2,5 m": "M = R1·cosα·s − q·cosα·(s − a)²/2",
        "sforzo normale": "N(0) = −R1·sinα (compressione); N(L) = +R2·sinα; differenza = q·sinα·(b − a)"},
        "valori": [
            {"grandezza": "Ry nodo 1", "valore": R1, "unita": "kN"},
            {"grandezza": "Ry nodo 2", "valore": R2, "unita": "kN"},
            {"grandezza": "Rx nodo 1", "valore": 0.0, "unita": "kN"},
            {"grandezza": "M asta 1 x=2.5", "valore": M, "unita": "kNm"},
            {"grandezza": "N asta 1 x=0", "valore": -R1 * s, "unita": "kN"},
            {"grandezza": "N asta 1 x=5", "valore": R2 * s, "unita": "kN"}]}
    return m, atteso


def c16():
    d = 0.010
    m = v11(trave("C16", "Trave Gerber, cedimento dell'appoggio",
                  "Geometria di C6 (incastro, cerniera interna a 4 m, appoggio a 6 m), nessun carico; l'appoggio a 6 m cede di 10 mm (schema v1.1, Silvia e Carla).",
                  [{"id": 1, "x": 0, "y": 0}, {"id": 2, "x": 4, "y": 0}, {"id": 3, "x": 6, "y": 0}],
                  [{"id": 1, "nodo_i": 1, "nodo_j": 2, "materiale": "S275", "sezione": "IPE300", "svincoli": {"rz_j": True}},
                   {"id": 2, "nodo_i": 2, "nodo_j": 3, "materiale": "S275", "sezione": "IPE300"}],
                  [{"nodo": 1, "ux": True, "uy": True, "rz": True}, {"nodo": 3, "uy": True}],
                  {"id": "CED", "nome": "Cedimento dell'appoggio", "categoria": "altro", "cedimenti": [{"nodo": 3, "uy": -d}]}, 5))
    atteso = {"caso": "CED", "formule": {
        "struttura isostatica": "il cedimento non produce reazioni né sollecitazioni",
        "cinematica": "la mensola resta indeformata; il tratto 4–6 ruota rigidamente attorno alla cerniera: φ = −δ/2"},
        "valori": [
            {"grandezza": "Ry nodo 1", "valore": 0.0, "unita": "kN"},
            {"grandezza": "Mz nodo 1 (reazione)", "valore": 0.0, "unita": "kNm"},
            {"grandezza": "M asta 1 x=0", "valore": 0.0, "unita": "kNm"},
            {"grandezza": "uy nodo 2 (cerniera)", "valore": 0.0, "unita": "m"},
            {"grandezza": "φj asta 1 (mensola alla cerniera)", "valore": 0.0, "unita": "rad"},
            {"grandezza": "rz nodo 2 (tratto appoggiato)", "valore": -d / 2, "unita": "rad"}]}
    return m, atteso


def c17():
    q, a, b = 10.0, 1.0, 4.0
    m = v11(trave("C17", "Asta inclinata, carico parziale normale all'asta",
                  "Geometria e vincoli di C15; carico di 10 kN/m normale all'asta (direzione locale_y, verso −y locale) da 1 a 4 m lungo l'asta "
                  "(punto 32 della revisione, Daniela).",
                  [{"id": 1, "x": 0, "y": 0}, {"id": 2, "x": 4, "y": 3}],
                  [{"id": 1, "nodo_i": 1, "nodo_j": 2, "materiale": "S275", "sezione": "IPE300"}],
                  [{"nodo": 1, "ux": True, "uy": True}, {"nodo": 2, "uy": True}],
                  {"id": "Q", "nome": "Carico normale parziale", "categoria": "Q", "carichi_aste": [
                      {"asta": 1, "tipo": "distribuito_trapezio", "direzione": "locale_y", "q_i": -q, "q_j": -q, "a": a, "b": b}]}, 11))
    c, s = 0.8, 0.6
    W = q * (b - a)
    Fx, Fy = W * s, -W * c                        # risultante: verso −y locale = (sin α, −cos α)
    xg, yg = (a + b) / 2 * c, (a + b) / 2 * s     # punto di applicazione
    R2 = -(xg * Fy - yg * Fx) / 4.0               # momento nullo attorno al piede; il carrello in (4; 3) reagisce solo in Y
    R1y, R1x = -Fy - R2, -Fx
    T1 = -R1x * s + R1y * c                       # componente trasversale locale della reazione al piede
    M = T1 * 2.5 - q * (2.5 - a) ** 2 / 2
    N = -(R1x * c + R1y * s)
    atteso = {"caso": "Q", "formule": {
        "risultante": "W = q·(b − a) normale all'asta, applicata in s = (a + b)/2",
        "reazioni": "R2 da equilibrio alla rotazione attorno al piede (carrello verticale); R1x = −Wx; R1y = −Wy − R2",
        "momento in s = 2,5 m": "M = T1·s − q·(s − a)²/2, T1 = componente trasversale di R1",
        "sforzo normale": "costante (nessun carico assiale): N = −(R1x·cos α + R1y·sin α)"},
        "valori": [
            {"grandezza": "Rx nodo 1", "valore": R1x, "unita": "kN"},
            {"grandezza": "Ry nodo 1", "valore": R1y, "unita": "kN"},
            {"grandezza": "Ry nodo 2", "valore": R2, "unita": "kN"},
            {"grandezza": "M asta 1 x=2.5", "valore": M, "unita": "kNm"},
            {"grandezza": "N asta 1 x=0", "valore": N, "unita": "kN"},
            {"grandezza": "N asta 1 x=5", "valore": N, "unita": "kN"}]}
    return m, atteso


def v12(m):
    """Schema v1.2: acciaio con alfa_t, IPE 300 con altezza h (distorsioni termiche)."""
    m["schema_version"] = "1.2"
    m["progetto"]["data"] = "2026-11-03"
    m["materiali"] = [dict(ACC, alfa_t=ALFA)]
    m["sezioni"] = [dict(IPE300, h=0.300)]
    return m


ALFA = 1.2e-5   # 1/°C, acciaio


def c14():
    L, dTu, dTg = 6.0, 20.0, 10.0
    m = v12(trave("C14", "Trave incastrata, distorsioni termiche",
                  "IPE 300, L = 6 m, incastri alle estremità; ΔT uniforme +20 °C e ΔT a farfalla +10 °C (lato inferiore più caldo) (schema v1.2, Valentina).",
                  [{"id": 1, "x": 0, "y": 0}, {"id": 2, "x": 6, "y": 0}],
                  [{"id": 1, "nodo_i": 1, "nodo_j": 2, "materiale": "S275", "sezione": "IPE300"}],
                  [{"nodo": 1, "ux": True, "uy": True, "rz": True}, {"nodo": 2, "ux": True, "uy": True, "rz": True}],
                  {"id": "T", "nome": "Distorsioni termiche", "categoria": "temperatura",
                   "carichi_termici": [{"asta": 1, "dT_u": dTu, "dT_g": dTg}]}, 7))
    EA, EI = E_ACC * IPE300["A"], E_ACC * IPE300["I"]
    N = -EA * ALFA * dTu
    M = -EI * ALFA * dTg / 0.300
    atteso = {"caso": "T", "formule": {
        "ΔT uniforme impedito": "N = −E·A·α·ΔTu (compressione); Rx1 = +E·A·α·ΔTu, Rx2 = −Rx1",
        "ΔT a farfalla impedito": "curvatura libera κ = α·ΔTg/h; M = −E·I·κ costante (fibre tese in alto)",
        "nessuno spostamento": "estremi incastrati, nessun carico: reazioni verticali nulle"},
        "valori": [
            {"grandezza": "N asta 1 x=0", "valore": N, "unita": "kN"},
            {"grandezza": "N asta 1 x=6", "valore": N, "unita": "kN"},
            {"grandezza": "M asta 1 x=0", "valore": M, "unita": "kNm"},
            {"grandezza": "M asta 1 x=3", "valore": M, "unita": "kNm"},
            {"grandezza": "Rx nodo 1", "valore": -N, "unita": "kN"},
            {"grandezza": "Ry nodo 1", "valore": 0.0, "unita": "kN"}]}
    return m, atteso


def c18():
    L, dTg = 6.0, 10.0
    m = v12(trave("C18", "Trave appoggiata, ΔT a farfalla",
                  "IPE 300, L = 6 m con nodo in mezzeria, cerniera e carrello; ΔT a farfalla +10 °C (lato inferiore più caldo) su tutta la trave (schema v1.2, Valentina).",
                  [{"id": 1, "x": 0, "y": 0}, {"id": 2, "x": 3, "y": 0}, {"id": 3, "x": 6, "y": 0}],
                  [{"id": 1, "nodo_i": 1, "nodo_j": 2, "materiale": "S275", "sezione": "IPE300"},
                   {"id": 2, "nodo_i": 2, "nodo_j": 3, "materiale": "S275", "sezione": "IPE300"}],
                  [{"nodo": 1, "ux": True, "uy": True}, {"nodo": 3, "uy": True}],
                  {"id": "T", "nome": "Gradiente termico", "categoria": "temperatura",
                   "carichi_termici": [{"asta": 1, "dT_g": dTg}, {"asta": 2, "dT_g": dTg}]}, 4))
    k = ALFA * dTg / 0.300
    atteso = {"caso": "T", "formule": {
        "struttura isostatica": "nessuna reazione né sollecitazione",
        "curvatura libera": "κ = α·ΔTg/h; il lato inferiore si allunga e la trave si inflette verso il basso: v(x) = κ·x·(x − L)/2",
        "freccia in mezzeria": "v(L/2) = −κ·L²/8",
        "rotazioni agli appoggi": "φ(0) = −κ·L/2, φ(L) = +κ·L/2"},
        "valori": [
            {"grandezza": "uy nodo 2", "valore": -k * L ** 2 / 8, "unita": "m"},
            {"grandezza": "rz nodo 1", "valore": -k * L / 2, "unita": "rad"},
            {"grandezza": "rz nodo 3", "valore": k * L / 2, "unita": "rad"},
            {"grandezza": "Ry nodo 1", "valore": 0.0, "unita": "kN"},
            {"grandezza": "M asta 1 x=3", "valore": 0.0, "unita": "kNm"}]}
    return m, atteso


def c19():
    dTg = 10.0
    m = v12(trave("C19", "Trave Gerber, ΔT a farfalla sulla mensola",
                  "Geometria di C6 (incastro, cerniera interna a 4 m, appoggio a 6 m), nessun carico; ΔT a farfalla +10 °C "
                  "(lato inferiore più caldo) sulla sola mensola 0–4 m, che ha la cerniera all'estremità j (punto 41, Valentina e Daniela).",
                  [{"id": 1, "x": 0, "y": 0}, {"id": 2, "x": 4, "y": 0}, {"id": 3, "x": 6, "y": 0}],
                  [{"id": 1, "nodo_i": 1, "nodo_j": 2, "materiale": "S275", "sezione": "IPE300", "svincoli": {"rz_j": True}},
                   {"id": 2, "nodo_i": 2, "nodo_j": 3, "materiale": "S275", "sezione": "IPE300"}],
                  [{"nodo": 1, "ux": True, "uy": True, "rz": True}, {"nodo": 3, "uy": True}],
                  {"id": "T", "nome": "Gradiente sulla mensola", "categoria": "temperatura",
                   "carichi_termici": [{"asta": 1, "dT_g": dTg}]}, 5))
    k, a = ALFA * dTg / 0.300, 4.0
    atteso = {"caso": "T", "formule": {
        "struttura isostatica": "la distorsione non produce reazioni né sollecitazioni",
        "mensola con curvatura libera": "v(x) = κ·x²/2 verso l'alto (lato inferiore più lungo): v(4) = κ·a²/2; rotazione alla cerniera φ = κ·a",
        "tratto 4–6": "rotazione rigida attorno all'appoggio: φ = −v(4)/2"},
        "valori": [
            {"grandezza": "Ry nodo 1", "valore": 0.0, "unita": "kN"},
            {"grandezza": "Mz nodo 1 (reazione)", "valore": 0.0, "unita": "kNm"},
            {"grandezza": "M asta 1 x=0", "valore": 0.0, "unita": "kNm"},
            {"grandezza": "uy nodo 2 (cerniera)", "valore": k * a ** 2 / 2, "unita": "m"},
            {"grandezza": "φj asta 1 (mensola alla cerniera)", "valore": k * a, "unita": "rad"},
            {"grandezza": "rz nodo 2 (tratto appoggiato)", "valore": -k * a ** 2 / 2 / 2, "unita": "rad"}]}
    return m, atteso


def c20():
    a, b, q1, q2 = 0.5, 2.0, 10.0, 20.0
    m = v11(trave("C20", "Trave Gerber, trapezio parziale sul tratto appoggiato",
                  "Geometria di C6 (incastro, cerniera interna a 4 m, appoggio a 6 m); carico verso il basso da 10 kN/m a 20 kN/m "
                  "sul tratto appoggiato, da 0,5 a 2,0 m dal suo nodo iniziale (Daniela e Valentina).",
                  [{"id": 1, "x": 0, "y": 0}, {"id": 2, "x": 4, "y": 0}, {"id": 3, "x": 6, "y": 0}],
                  [{"id": 1, "nodo_i": 1, "nodo_j": 2, "materiale": "S275", "sezione": "IPE300", "svincoli": {"rz_j": True}},
                   {"id": 2, "nodo_i": 2, "nodo_j": 3, "materiale": "S275", "sezione": "IPE300"}],
                  [{"nodo": 1, "ux": True, "uy": True, "rz": True}, {"nodo": 3, "uy": True}],
                  {"id": "Q", "nome": "Trapezio parziale", "categoria": "Q", "carichi_aste": [
                      {"asta": 2, "tipo": "distribuito_trapezio", "direzione": "globale_y", "q_i": -q1, "q_j": -q2, "a": a, "b": b}]}, 5))
    c = b - a
    W = c * (q1 + q2) / 2
    xg = a + c * (q1 + 2 * q2) / (3 * (q1 + q2))   # baricentro sul tratto appoggiato (luce 2 m)
    R3 = W * xg / 2.0
    Rs = W - R3                                  # forza trasmessa dalla cerniera alla mensola
    t = 1.0 - a
    M1 = Rs * 1.0 - (q1 * t ** 2 / 2 + (q2 - q1) / c * t ** 3 / 6)
    EI = E_ACC * IPE300["I"]
    atteso = {"caso": "Q", "formule": {
        "tratto appoggiato (2 m)": "W = (b − a)(q1 + q2)/2; xg = a + (b − a)(q1 + 2q2)/(3(q1 + q2)); R3 = W·xg/2; Rs = W − R3",
        "mensola (4 m)": "carico Rs in punta: R1 = Rs; M1 = −Rs·4; abbassamento della cerniera Rs·4³/(3EI)",
        "momento a 1 m dalla cerniera": "M = Rs·1 − [q1·t²/2 + (q2 − q1)/(b − a)·t³/6], t = 1 − a"},
        "valori": [
            {"grandezza": "Ry nodo 3", "valore": R3, "unita": "kN"},
            {"grandezza": "Ry nodo 1", "valore": Rs, "unita": "kN"},
            {"grandezza": "Mz nodo 1 (reazione)", "valore": Rs * 4, "unita": "kNm"},
            {"grandezza": "M asta 1 x=4 (cerniera)", "valore": 0.0, "unita": "kNm"},
            {"grandezza": "M asta 2 x=1", "valore": M1, "unita": "kNm"},
            {"grandezza": "uy nodo 2 (cerniera)", "valore": -Rs * 4 ** 3 / (3 * EI), "unita": "m"}]}
    return m, atteso


def c21():
    a, b, q1, q2, d = 1.0, 4.0, 10.0, 20.0, 0.010
    m = v11(trave("C21", "Asta inclinata, trapezio verticale e cedimento",
                  "Geometria e vincoli di C15 (cerniera al piede, carrello verticale in testa); carico verticale da 10 a 20 kN/m "
                  "di lunghezza dell'asta tra 1 e 4 m lungo l'asta; il carrello cede di 10 mm (Daniela e Valentina).",
                  [{"id": 1, "x": 0, "y": 0}, {"id": 2, "x": 4, "y": 3}],
                  [{"id": 1, "nodo_i": 1, "nodo_j": 2, "materiale": "S275", "sezione": "IPE300"}],
                  [{"nodo": 1, "ux": True, "uy": True}, {"nodo": 2, "uy": True}],
                  {"id": "Q", "nome": "Trapezio e cedimento", "categoria": "Q",
                   "carichi_aste": [{"asta": 1, "tipo": "distribuito_trapezio", "direzione": "globale_y", "q_i": -q1, "q_j": -q2, "a": a, "b": b}],
                   "cedimenti": [{"nodo": 2, "uy": -d}]}, 11))
    c = 0.8
    W = (b - a) * (q1 + q2) / 2
    sg = a + (b - a) * (q1 + 2 * q2) / (3 * (q1 + q2))   # baricentro lungo l'asta
    R2 = W * sg * c / 4.0
    R1 = W - R2
    t = 2.5 - a
    M = R1 * c * 2.5 - c * (q1 * t ** 2 / 2 + (q2 - q1) / (b - a) * t ** 3 / 6)
    atteso = {"caso": "Q", "formule": {
        "struttura isostatica": "il cedimento non cambia reazioni né sollecitazioni: solo spostamenti",
        "reazioni": "W = (b − a)(q1 + q2)/2; baricentro sg = a + (b − a)(q1 + 2q2)/(3(q1 + q2)); R2 = W·sg·cosα/4; R1 = W − R2",
        "momento in s = 2,5 m": "M = R1·cosα·s − cosα·[q1·t²/2 + (q2 − q1)/(b − a)·t³/6], t = s − a",
        "cedimento": "uy del carrello = −δ"},
        "valori": [
            {"grandezza": "Ry nodo 1", "valore": R1, "unita": "kN"},
            {"grandezza": "Ry nodo 2", "valore": R2, "unita": "kN"},
            {"grandezza": "Rx nodo 1", "valore": 0.0, "unita": "kN"},
            {"grandezza": "M asta 1 x=2.5", "valore": M, "unita": "kNm"},
            {"grandezza": "uy nodo 2 (cedimento)", "valore": -d, "unita": "m"}]}
    return m, atteso


def c22():
    a, b, q1, q2, k = 0.5, 2.0, 10.0, 20.0, 2000.0
    m = v11(trave("C22", "Trave Gerber su molla, trapezio parziale",
                  "Geometria e carico di C20; l'appoggio a 6 m è sostituito da una molla verticale ky = 2000 kN/m (Daniela e Valentina).",
                  [{"id": 1, "x": 0, "y": 0}, {"id": 2, "x": 4, "y": 0}, {"id": 3, "x": 6, "y": 0}],
                  [{"id": 1, "nodo_i": 1, "nodo_j": 2, "materiale": "S275", "sezione": "IPE300", "svincoli": {"rz_j": True}},
                   {"id": 2, "nodo_i": 2, "nodo_j": 3, "materiale": "S275", "sezione": "IPE300"}],
                  [{"nodo": 1, "ux": True, "uy": True, "rz": True}, {"nodo": 3, "molle": {"ky": k}}],
                  {"id": "Q", "nome": "Trapezio parziale", "categoria": "Q", "carichi_aste": [
                      {"asta": 2, "tipo": "distribuito_trapezio", "direzione": "globale_y", "q_i": -q1, "q_j": -q2, "a": a, "b": b}]}, 5))
    c = b - a
    W = c * (q1 + q2) / 2
    xg = a + c * (q1 + 2 * q2) / (3 * (q1 + q2))
    R3 = W * xg / 2.0
    Rs = W - R3
    EI = E_ACC * IPE300["I"]
    v2 = -Rs * 4 ** 3 / (3 * EI)
    atteso = {"caso": "Q", "formule": {
        "struttura isostatica": "la molla sostituisce l'appoggio ma non aggiunge vincoli sovrabbondanti: reazioni come in C20",
        "abbassamento della molla": "v3 = −R3/ky",
        "cerniera": "abbassamento come in C20: v2 = −Rs·4³/(3EI)",
        "tratto 4–6": "rotazione rigida della corda più quella elastica: le sollecitazioni non cambiano"},
        "valori": [
            {"grandezza": "Ry nodo 3 (molla)", "valore": R3, "unita": "kN"},
            {"grandezza": "Ry nodo 1", "valore": Rs, "unita": "kN"},
            {"grandezza": "Mz nodo 1 (reazione)", "valore": Rs * 4, "unita": "kNm"},
            {"grandezza": "uy nodo 3 (molla)", "valore": -R3 / k, "unita": "m"},
            {"grandezza": "uy nodo 2 (cerniera)", "valore": v2, "unita": "m"}]}
    return m, atteso


def c23():
    L, q, dTu, dTg = 6.0, 20.0, 20.0, 10.0
    # 0,9 = 1,5 × ψ0, con ψ0 = 0,6 per le variazioni termiche (NTC 2018, tab. 2.5.I, da ricontrollare sul testo):
    # vale per T azione di accompagnamento. Qui T è l'unica azione variabile, quindi in una combinazione normativa
    # sarebbe la principale con 1,5; il caso prova la sovrapposizione con coefficienti diversi, non la norma
    gG, gT = 1.3, 0.9
    m = v12(trave("C23", "Trave incastrata, combinazione di carico triangolare e distorsione termica",
                  "IPE 300, L = 6 m, incastri; caso G: carico triangolare da 0 a 20 kN/m (come C13); caso T: ΔT uniforme +20 °C e a farfalla +10 °C "
                  "(come C14); combinazione 1,3·G + 0,9·T (Daniela e Valentina).",
                  [{"id": 1, "x": 0, "y": 0}, {"id": 2, "x": 6, "y": 0}],
                  [{"id": 1, "nodo_i": 1, "nodo_j": 2, "materiale": "S275", "sezione": "IPE300"}],
                  [{"nodo": 1, "ux": True, "uy": True, "rz": True}, {"nodo": 2, "ux": True, "uy": True, "rz": True}],
                  {"id": "G", "nome": "Carico triangolare", "categoria": "G2", "carichi_aste": [
                      {"asta": 1, "tipo": "distribuito_trapezio", "direzione": "globale_y", "q_i": 0.0, "q_j": -q, "a": 0.0, "b": L}]}, 7))
    m["progetto"]["data"] = "2026-11-10"
    m["casi_di_carico"].append({"id": "T", "nome": "Distorsioni termiche", "categoria": "temperatura",
                                "carichi_termici": [{"asta": 1, "dT_u": dTu, "dT_g": dTg}]})
    m["combinazioni"] = [{"id": "SLU1", "nome": "1,3·G + 0,9·T", "tipo": "SLU", "coefficienti": {"G": gG, "T": gT}}]
    EA, EI = E_ACC * IPE300["A"], E_ACC * IPE300["I"]
    NT, MT = -EA * ALFA * dTu, -EI * ALFA * dTg / 0.300
    atteso = {"caso": "SLU1", "formule": {
        "caso G (C13)": "MA = −qL²/30, MB = −qL²/20, RA = 3qL/20, RB = 7qL/20, N = 0",
        "caso T (C14)": "N = −EAαΔTu, M = −EIαΔTg/h costante, nessuna reazione verticale",
        "combinazione": "sovrapposizione lineare: 1,3·G + 0,9·T"},
        "valori": [
            {"grandezza": "Ry nodo 1", "valore": gG * 3 * q * L / 20, "unita": "kN"},
            {"grandezza": "Ry nodo 2", "valore": gG * 7 * q * L / 20, "unita": "kN"},
            {"grandezza": "M asta 1 x=0", "valore": gG * (-q * L ** 2 / 30) + gT * MT, "unita": "kNm"},
            {"grandezza": "M asta 1 x=6", "valore": gG * (-q * L ** 2 / 20) + gT * MT, "unita": "kNm"},
            {"grandezza": "N asta 1 x=3", "valore": gT * NT, "unita": "kN"}]}
    return m, atteso


def c24():
    """Telaio a due piani con travi incernierate e combinazione di due casi (Daniela e Valentina, 11/11).

    Le travi hanno cerniere a entrambe le estremità e la deformabilità assiale è trascurata: le travi sono
    bielle rigide che collegano due mensole uguali. Ne seguono valori esatti senza risolvere il telaio:
    - caso G: ogni trave è appoggiata, M in mezzeria qL²/8; ogni colonna porta qL/2 per piano, senza flessione;
    - caso W: le bielle impongono lo stesso spostamento alle due mensole uguali, che si dividono a metà ogni
      forza di piano; nessuna reazione verticale, perché le travi incernierate non trasmettono momento.
    """
    L, h, q, H1, H2 = 6.0, 3.5, 25.0, 10.0, 15.0
    gG, gW = 1.3, 1.5
    m = base("C24", "Telaio a due piani a travi incernierate, combinazione di carichi verticali e vento",
             "Una campata L = 6 m, due piani h = 3,5 m; colonne HE 200 A continue e incastrate al piede, travi IPE 300 "
             "incernierate alle estremità; deformabilità assiale trascurata. Caso G: q = 25 kN/m sulle travi; caso W: "
             "10 kN al primo piano e 15 kN al secondo; combinazione 1,3·G + 1,5·W (Daniela e Valentina).")
    m["progetto"]["data"] = "2026-11-11"
    cerniere = {"rz_i": True, "rz_j": True}
    m.update({
        "nodi": [{"id": 1, "x": 0, "y": 0}, {"id": 2, "x": L, "y": 0}, {"id": 3, "x": 0, "y": h},
                 {"id": 4, "x": L, "y": h}, {"id": 5, "x": 0, "y": 2 * h}, {"id": 6, "x": L, "y": 2 * h}],
        "sezioni": [HEA200, IPE300],
        "aste": [{"id": 1, "nodo_i": 1, "nodo_j": 3, "materiale": "S275", "sezione": "HEA200"},
                 {"id": 2, "nodo_i": 2, "nodo_j": 4, "materiale": "S275", "sezione": "HEA200"},
                 {"id": 3, "nodo_i": 3, "nodo_j": 5, "materiale": "S275", "sezione": "HEA200"},
                 {"id": 4, "nodo_i": 4, "nodo_j": 6, "materiale": "S275", "sezione": "HEA200"},
                 {"id": 5, "nodo_i": 3, "nodo_j": 4, "materiale": "S275", "sezione": "IPE300", "svincoli": dict(cerniere)},
                 {"id": 6, "nodo_i": 5, "nodo_j": 6, "materiale": "S275", "sezione": "IPE300", "svincoli": dict(cerniere)}],
        "vincoli": [{"nodo": 1, "ux": True, "uy": True, "rz": True}, {"nodo": 2, "ux": True, "uy": True, "rz": True}],
        "casi_di_carico": [
            {"id": "G", "nome": "Carichi verticali sulle travi", "categoria": "G2",
             "carichi_aste": [{"asta": 5, "tipo": "distribuito_uniforme", "direzione": "globale_y", "q": -q},
                              {"asta": 6, "tipo": "distribuito_uniforme", "direzione": "globale_y", "q": -q}]},
            {"id": "W", "nome": "Vento", "categoria": "vento",
             "carichi_nodali": [{"nodo": 3, "Fx": H1}, {"nodo": 5, "Fx": H2}]}],
        "combinazioni": [{"id": "SLU1", "nome": "1,3·G + 1,5·W", "tipo": "SLU", "coefficienti": {"G": gG, "W": gW}}],
        "analisi": {"tipo": "statica_lineare", "deformabilita_assiale": False, "punti_diagramma": 11},
    })
    atteso = {"caso": "SLU1", "formule": {
        "caso G": "travi appoggiate: M mezzeria = qL²/8; Ry = 2·qL/2 per colonna; colonne senza flessione",
        "caso W": "mensole uguali collegate da bielle rigide: ciascuna porta H1/2 e H2/2; Rx = −(H1 + H2)/2; "
                  "M al piede = H1/2·h + H2/2·2h; M in testa al primo piano = H2/2·h; Ry = 0",
        "combinazione": "sovrapposizione lineare 1,3·G + 1,5·W"},
        "valori": [
            {"grandezza": "Ry nodo 1", "valore": gG * q * L, "unita": "kN"},
            {"grandezza": "Ry nodo 2", "valore": gG * q * L, "unita": "kN"},
            {"grandezza": "Rx nodo 1", "valore": -gW * (H1 + H2) / 2, "unita": "kN"},
            {"grandezza": "Rx nodo 2", "valore": -gW * (H1 + H2) / 2, "unita": "kN"},
            {"grandezza": "|M| asta 1 x=0 (piede)", "valore": gW * (H1 / 2 * h + H2 / 2 * 2 * h), "unita": "kNm"},
            {"grandezza": "|M| asta 3 x=0 (primo piano)", "valore": gW * H2 / 2 * h, "unita": "kNm"},
            {"grandezza": "|M| asta 5 x=L/2 (mezzeria)", "valore": gG * q * L ** 2 / 8, "unita": "kNm"},
            {"grandezza": "N asta 2 x=0", "valore": -gG * q * L, "unita": "kN"}]}
    return m, atteso


def c25():
    """Portale a tre cerniere con trapezio parziale e cedimento (Daniela e Valentina, 12/11).

    Isostatico: reazioni e sollecitazioni dal solo equilibrio; il cedimento non le cambia.
    """
    h, L, qi, qj, a = 4.0, 6.0, 10.0, 20.0, 3.0           # trapezio sulla mezza trave sinistra, da 0 a 3 m
    F = (qi + qj) / 2 * a                                  # 45 kN
    xF = a * (qi + 2 * qj) / (3 * (qi + qj))               # 1,667 m dal nodo 2
    VB = F * xF / L                                        # equilibrio alla rotazione attorno ad A
    VA = F - VB
    HB = -(L / 2) * VB / h                                 # M = 0 alla cerniera C per la parte destra
    HA = -HB
    x = 1.5
    Mx = VA * x - HA * h - (qi * x ** 2 / 2 + (qj - qi) / a * x ** 3 / 6)
    m = v11(trave("C25", "Portale a tre cerniere, trapezio parziale e cedimento",
                  "Colonne h = 4 m e traverso L = 6 m in IPE 300, appoggi fissi ai piedi, cerniera in mezzeria del traverso; "
                  "trapezio verticale da 10 a 20 kN/m sulla metà sinistra del traverso; cedimento di 10 mm del piede destro "
                  "(Daniela e Valentina).",
                  [{"id": 1, "x": 0, "y": 0}, {"id": 2, "x": 0, "y": h}, {"id": 3, "x": L / 2, "y": h},
                   {"id": 4, "x": L, "y": h}, {"id": 5, "x": L, "y": 0}],
                  [{"id": 1, "nodo_i": 1, "nodo_j": 2, "materiale": "S275", "sezione": "IPE300"},
                   {"id": 2, "nodo_i": 2, "nodo_j": 3, "materiale": "S275", "sezione": "IPE300", "svincoli": {"rz_j": True}},
                   {"id": 3, "nodo_i": 3, "nodo_j": 4, "materiale": "S275", "sezione": "IPE300"},
                   {"id": 4, "nodo_i": 5, "nodo_j": 4, "materiale": "S275", "sezione": "IPE300"}],
                  [{"nodo": 1, "ux": True, "uy": True}, {"nodo": 5, "ux": True, "uy": True}],
                  {"id": "Q", "nome": "Trapezio e cedimento", "categoria": "Q",
                   "carichi_aste": [{"asta": 2, "tipo": "distribuito_trapezio", "direzione": "globale_y",
                                     "q_i": -qi, "q_j": -qj, "a": 0.0, "b": a}],
                   "cedimenti": [{"nodo": 5, "uy": -0.010}]}, 21))
    m["progetto"]["data"] = "2026-11-12"
    atteso = {"caso": "Q", "formule": {
        "risultante": "F = (qi + qj)/2·a = 45 kN a xF = a(qi + 2qj)/(3(qi + qj)) = 1,667 m dal nodo 2",
        "verticali": "VB = F·xF/L = 12,5 kN; VA = F − VB = 32,5 kN",
        "orizzontali": "M = 0 alla cerniera per la parte destra: HB = −(L/2)·VB/h = −9,375 kN; HA = −HB",
        "momento nel traverso": "M(x) = VA·x − HA·h − (qi·x²/2 + (qj − qi)/a·x³/6), x dal nodo 2",
        "cedimento": "struttura isostatica: il cedimento non cambia reazioni né sollecitazioni"},
        "valori": [
            {"grandezza": "Ry nodo 1", "valore": VA, "unita": "kN"},
            {"grandezza": "Ry nodo 5", "valore": VB, "unita": "kN"},
            {"grandezza": "Rx nodo 1", "valore": HA, "unita": "kN"},
            {"grandezza": "Rx nodo 5", "valore": HB, "unita": "kN"},
            {"grandezza": "|M| asta 1 x=h (nodo 2)", "valore": HA * h, "unita": "kNm"},
            {"grandezza": "|M| asta 2 x=1,5", "valore": abs(Mx), "unita": "kNm"},
            {"grandezza": "M asta 2 x=3 (cerniera)", "valore": 0.0, "unita": "kNm"},
            {"grandezza": "uy nodo 5 (cedimento)", "valore": -0.010, "unita": "m"}]}
    return m, atteso


def c26():
    """Trave continua su tre appoggi: carico uniforme e cedimento in due casi, poi combinati (Daniela e Valentina, 13/11).

    Prima combinazione che contiene un cedimento. Soluzioni chiuse:
    - caso G: M sull'appoggio centrale −qL²/8, reazioni 3qL/8 e 10qL/8;
    - caso D: il cedimento δ equivale a una forza P = 6EIδ/L³ in mezzeria della trave 2L appoggiata
      (δ = P(2L)³/48EI), verso il basso sulla trave: reazione centrale −P, estreme +P/2, M centrale +PL/2.
    """
    L, q, d = 6.0, 20.0, 0.010
    gG, gD = 1.3, 1.0
    EI = E_ACC * IPE300["I"]
    P = 6 * EI * d / L ** 3
    m = v11(trave("C26", "Trave continua, combinazione di carico uniforme e cedimento",
                  "IPE 300, due campate da 6 m su tre appoggi; caso G: q = 20 kN/m su entrambe le campate; caso D: "
                  "cedimento di 10 mm dell'appoggio centrale; combinazione 1,3·G + 1,0·D (Daniela e Valentina).",
                  [{"id": 1, "x": 0, "y": 0}, {"id": 2, "x": L, "y": 0}, {"id": 3, "x": 2 * L, "y": 0}],
                  [{"id": 1, "nodo_i": 1, "nodo_j": 2, "materiale": "S275", "sezione": "IPE300"},
                   {"id": 2, "nodo_i": 2, "nodo_j": 3, "materiale": "S275", "sezione": "IPE300"}],
                  [{"nodo": 1, "ux": True, "uy": True}, {"nodo": 2, "uy": True}, {"nodo": 3, "uy": True}],
                  {"id": "G", "nome": "Carico uniforme", "categoria": "G2",
                   "carichi_aste": [{"asta": 1, "tipo": "distribuito_uniforme", "direzione": "globale_y", "q": -q},
                                    {"asta": 2, "tipo": "distribuito_uniforme", "direzione": "globale_y", "q": -q}]}, 13))
    m["progetto"]["data"] = "2026-11-13"
    m["casi_di_carico"].append({"id": "D", "nome": "Cedimento dell'appoggio centrale", "categoria": "altro",
                                "cedimenti": [{"nodo": 2, "uy": -d}]})
    m["combinazioni"] = [{"id": "SLU1", "nome": "1,3·G + 1,0·D", "tipo": "SLU", "coefficienti": {"G": gG, "D": gD}}]
    atteso = {"caso": "SLU1", "formule": {
        "caso G": "R1 = R3 = 3qL/8, R2 = 10qL/8, M2 = −qL²/8",
        "caso D": "P = 6EIδ/L³; R2 = −P, R1 = R3 = P/2, M2 = +PL/2, uy2 = −δ",
        "combinazione": "1,3·G + 1,0·D"},
        "valori": [
            {"grandezza": "Ry nodo 1", "valore": gG * 3 * q * L / 8 + gD * P / 2, "unita": "kN"},
            {"grandezza": "Ry nodo 2", "valore": gG * 10 * q * L / 8 - gD * P, "unita": "kN"},
            {"grandezza": "Ry nodo 3", "valore": gG * 3 * q * L / 8 + gD * P / 2, "unita": "kN"},
            {"grandezza": "M asta 1 x=L (appoggio centrale)", "valore": gG * (-q * L ** 2 / 8) + gD * P * L / 2, "unita": "kNm"},
            {"grandezza": "uy nodo 2", "valore": -gD * d, "unita": "m"}]}
    return m, atteso


def c27():
    """Telaio di C24 con le travi divise in mezzeria: carichi verticali e ΔT a farfalla (Daniela e Valentina, 14/11).

    Il vento di C24, escluso il 14/11 per il punto 79, è reinserito il 22/11: dal 21/11 le aste incernierate usano
    R = 10⁶ e i due solutori concordano. Le colonne uguali portano ciascuna metà del vento, come in C24.

    Le travi sono incernierate agli estremi, quindi isostatiche: il ΔT a farfalla le incurva senza sollecitazioni
    né reazioni. Ogni trave è divisa in mezzeria per leggere la freccia, che si somma a quella dei carichi:
    - caso G: −5qL⁴/384EI (nodi d'estremità fermi, colonne assialmente rigide);
    - caso T: κ = α·ΔTg/h; il lato inferiore più caldo si allunga e la trave si incurva verso il basso: −κL²/8
      (stesso verso di C18);
    """
    m, _ = c24()
    L, h, q, dTg = 6.0, 3.5, 25.0, 20.0
    gG, gW, gT = 1.3, 1.5, 0.9
    m["progetto"].update({"id": "C27", "nome": "Telaio a due piani a travi incernierate, combinazione di carichi verticali, vento e ΔT a farfalla",
                          "descrizione": "Telaio di C24 (colonne HE 200 A incastrate, travi IPE 300 incernierate agli estremi e divise in mezzeria, deformabilità assiale trascurata). Caso G: q = 25 kN/m sulle travi; caso T: ΔT a farfalla +20 °C sulle travi; caso W: 10 e 15 kN ai piani; combinazione 1,3·G + 1,5·W + 0,9·T (Daniela e Valentina).",
                          "data": "2026-11-14"})
    m["schema_version"] = "1.2"
    m["materiali"] = [dict(ACC, alfa_t=ALFA)]
    m["sezioni"] = [HEA200, dict(IPE300, h=0.300)]
    m["nodi"] += [{"id": 7, "x": L / 2, "y": h}, {"id": 8, "x": L / 2, "y": 2 * h}]
    m["aste"] = m["aste"][:4] + [
        {"id": 5, "nodo_i": 3, "nodo_j": 7, "materiale": "S275", "sezione": "IPE300", "svincoli": {"rz_i": True}},
        {"id": 6, "nodo_i": 7, "nodo_j": 4, "materiale": "S275", "sezione": "IPE300", "svincoli": {"rz_j": True}},
        {"id": 7, "nodo_i": 5, "nodo_j": 8, "materiale": "S275", "sezione": "IPE300", "svincoli": {"rz_i": True}},
        {"id": 8, "nodo_i": 8, "nodo_j": 6, "materiale": "S275", "sezione": "IPE300", "svincoli": {"rz_j": True}}]
    m["casi_di_carico"][0]["carichi_aste"] = [
        {"asta": a, "tipo": "distribuito_uniforme", "direzione": "globale_y", "q": -q} for a in (5, 6, 7, 8)]
    m["casi_di_carico"].append({"id": "T", "nome": "ΔT a farfalla sulle travi", "categoria": "temperatura",
                                "carichi_termici": [{"asta": a, "dT_g": dTg} for a in (5, 6, 7, 8)]})
    m["combinazioni"] = [{"id": "SLU1", "nome": "1,3·G + 1,5·W + 0,9·T", "tipo": "SLU",
                          "coefficienti": {"G": gG, "W": gW, "T": gT}}]
    EI = E_ACC * IPE300["I"]
    fG = -5 * q * L ** 4 / (384 * EI)
    fT = -ALFA * dTg / 0.300 * L ** 2 / 8
    atteso = {"caso": "SLU1", "formule": {
        "reazioni e momenti": "travi appoggiate: Ry = qL per piede, colonne senza flessione; il ΔT a farfalla su travi isostatiche non dà sollecitazioni",
        "freccia in mezzeria": "1,3·(−5qL⁴/384EI) + 0,9·(−α·ΔTg/h·L²/8)",
        "vento": "come C24: Rx = −(H1 + H2)/2, M piede = H1/2·h + H2/2·2h",
        "combinazione": "1,3·G + 1,5·W + 0,9·T"},
        "valori": [
            {"grandezza": "Ry nodo 1", "valore": gG * q * L, "unita": "kN"},
            {"grandezza": "Rx nodo 1", "valore": -gW * 12.5, "unita": "kN"},
            {"grandezza": "|M| asta 1 x=0 (piede)", "valore": gW * 70.0, "unita": "kNm"},
            {"grandezza": "M asta 5 x=L/2 (mezzeria)", "valore": gG * q * L ** 2 / 8, "unita": "kNm"},
            {"grandezza": "uy nodo 7 (mezzeria primo piano)", "valore": gG * fG + gT * fT, "unita": "m"},
            {"grandezza": "uy nodo 8 (mezzeria secondo piano)", "valore": gG * fG + gT * fT, "unita": "m"}]}
    return m, atteso


def c28():
    """Portale asimmetrico a tre cerniere con carichi misti (Daniela e Valentina, 16/11).

    Piedi a quote diverse: A (0; 0) e B (8; 2); traverso a quota 5, cerniera C a 3 m da sinistra.
    Carichi: forza orizzontale H in testa alla colonna sinistra, vento q uniforme sulla colonna sinistra,
    forza verticale P sul traverso a 6 m. Isostatico: tre equazioni globali e M = 0 in C.
    """
    H, q, P, xP = 12.0, 4.0, 30.0, 6.0
    A, D, C, E, B = (0.0, 0.0), (0.0, 5.0), (3.0, 5.0), (8.0, 5.0), (8.0, 2.0)
    Fq, yq = q * (D[1] - A[1]), (D[1] + A[1]) / 2          # risultante del vento e sua quota
    # rotazione attorno ad A (antioraria positiva): xB·VB − yB·HB − yD·H − yq·Fq − xP·P = 0
    # M = 0 in C per la parte destra:               (xB − xC)·VB − (yB − yC)·HB − (xP − xC)·P = 0
    a11, a12, b1 = B[0], -B[1], D[1] * H + yq * Fq + xP * P
    a21, a22, b2 = B[0] - C[0], -(B[1] - C[1]), (xP - C[0]) * P
    det = a11 * a22 - a12 * a21
    VB = (b1 * a22 - a12 * b2) / det
    HB = (a11 * b2 - a21 * b1) / det
    HA = -(H + Fq) - HB
    VA = P - VB
    M_E = abs(-(B[1] - E[1]) * HB)                                   # testa della colonna destra
    M_P = abs((B[0] - xP) * VB - (B[1] - E[1]) * HB)                 # traverso sotto il carico
    M_D = abs(-(A[1] - D[1]) * HA - (yq - D[1]) * Fq)                # testa della colonna sinistra
    m = trave("C28", "Portale asimmetrico a tre cerniere, carichi misti",
              "Piedi incernierati a quote diverse, A (0; 0) e B (8; 2); traverso IPE 300 a quota 5 m con cerniera a 3 m "
              "da sinistra; forza orizzontale 12 kN in testa alla colonna sinistra, vento 4 kN/m sulla colonna sinistra, "
              "forza verticale 30 kN sul traverso a 6 m (Daniela e Valentina).",
              [{"id": 1, "x": A[0], "y": A[1]}, {"id": 2, "x": D[0], "y": D[1]}, {"id": 3, "x": C[0], "y": C[1]},
               {"id": 4, "x": E[0], "y": E[1]}, {"id": 5, "x": B[0], "y": B[1]}],
              [{"id": 1, "nodo_i": 1, "nodo_j": 2, "materiale": "S275", "sezione": "IPE300"},
               {"id": 2, "nodo_i": 2, "nodo_j": 3, "materiale": "S275", "sezione": "IPE300", "svincoli": {"rz_j": True}},
               {"id": 3, "nodo_i": 3, "nodo_j": 4, "materiale": "S275", "sezione": "IPE300"},
               {"id": 4, "nodo_i": 5, "nodo_j": 4, "materiale": "S275", "sezione": "IPE300"}],
              [{"nodo": 1, "ux": True, "uy": True}, {"nodo": 5, "ux": True, "uy": True}],
              {"id": "Q", "nome": "Carichi misti", "categoria": "Q",
               "carichi_nodali": [{"nodo": 2, "Fx": H}],
               "carichi_aste": [{"asta": 1, "tipo": "distribuito_uniforme", "direzione": "globale_x", "q": q},
                                {"asta": 3, "tipo": "concentrato", "direzione": "globale_y", "P": -P, "a": xP - C[0]}]}, 21)
    m["progetto"]["data"] = "2026-11-16"
    atteso = {"caso": "Q", "formule": {
        "rotazione attorno ad A": "8·VB − 2·HB − 5·H − 2,5·(q·5) − 6·P = 0",
        "cerniera C, parte destra": "5·VB + 3·HB − 3·P = 0",
        "equilibrio": "HA = −(H + 5q) − HB; VA = P − VB",
        "momenti": "colonna destra in testa |3·HB|; traverso sotto P |2·VB + 3·HB|; colonna sinistra in testa |5·HA + 2,5·5q|"},
        "valori": [
            {"grandezza": "Ry nodo 1", "valore": VA, "unita": "kN"},
            {"grandezza": "Ry nodo 5", "valore": VB, "unita": "kN"},
            {"grandezza": "Rx nodo 1", "valore": HA, "unita": "kN"},
            {"grandezza": "Rx nodo 5", "valore": HB, "unita": "kN"},
            {"grandezza": "|M| asta 4 x=L (testa colonna destra)", "valore": M_E, "unita": "kNm"},
            {"grandezza": "|M| asta 3 x=3 (sotto il carico)", "valore": M_P, "unita": "kNm"},
            {"grandezza": "|M| asta 1 x=L (testa colonna sinistra)", "valore": M_D, "unita": "kNm"},
            {"grandezza": "M asta 2 x=3 (cerniera)", "valore": 0.0, "unita": "kNm"}]}
    return m, atteso


def c29():
    """Telaio di C24 con trapezio sulla trave del primo piano e cedimento del piede destro (Daniela e Valentina, 17/11).

    Le travi sono incernierate agli estremi e le colonne assialmente rigide: il cedimento del piede destro abbassa
    rigidamente la colonna destra e fa ruotare le travi senza sollecitazioni. Il trapezio dà le reazioni della
    trave appoggiata, portate a terra dalle colonne senza flessione.
    """
    m, _ = c24()
    L, qi, qj, d = 6.0, 10.0, 30.0, 0.010
    m["progetto"].update({"id": "C29", "nome": "Telaio a due piani a travi incernierate, trapezio e cedimento",
                          "descrizione": "Telaio di C24 (colonne HE 200 A incastrate, travi IPE 300 incernierate agli "
                          "estremi, deformabilità assiale trascurata); trapezio verticale da 10 a 30 kN/m sulla trave del "
                          "primo piano; cedimento di 10 mm del piede destro (Daniela e Valentina).", "data": "2026-11-17"})
    m["schema_version"] = "1.1"
    m["casi_di_carico"] = [{"id": "Q", "nome": "Trapezio e cedimento", "categoria": "Q",
                            "carichi_aste": [{"asta": 5, "tipo": "distribuito_trapezio", "direzione": "globale_y",
                                              "q_i": -qi, "q_j": -qj, "a": 0.0, "b": L}],
                            "cedimenti": [{"nodo": 2, "uy": -d}]}]
    m.pop("combinazioni", None)
    Rs, Rd = L * (2 * qi + qj) / 6, L * (qi + 2 * qj) / 6
    x = 3.0
    Mx = Rs * x - qi * x ** 2 / 2 - (qj - qi) * x ** 3 / (6 * L)
    atteso = {"caso": "Q", "formule": {
        "trave appoggiata con trapezio": "Rs = L(2qi + qj)/6, Rd = L(qi + 2qj)/6; M(x) = Rs·x − qi·x²/2 − (qj − qi)·x³/(6L)",
        "cedimento": "moto rigido: colonna destra abbassata di 10 mm, travi ruotate, nessuna sollecitazione",
        "colonne": "nessuna flessione; N = −Rs e −Rd"},
        "valori": [
            {"grandezza": "Ry nodo 1", "valore": Rs, "unita": "kN"},
            {"grandezza": "Ry nodo 2", "valore": Rd, "unita": "kN"},
            {"grandezza": "Rx nodo 1", "valore": 0.0, "unita": "kN"},
            {"grandezza": "M asta 1 x=0 (piede)", "valore": 0.0, "unita": "kNm"},
            {"grandezza": "M asta 5 x=3 (mezzeria)", "valore": Mx, "unita": "kNm"},
            {"grandezza": "N asta 2 x=0", "valore": -Rd, "unita": "kN"},
            {"grandezza": "uy nodo 6 (testa colonna destra)", "valore": -d, "unita": "m"}]}
    return m, atteso


def c30():
    """Telaio a tre piani a travi incernierate, carichi misti combinati (Daniela e Valentina, 18/11).

    Colonne HE 200 A continue e incastrate, travi IPE 300 incernierate agli estremi, deformabilità assiale
    trascurata, come C24 con un piano in più. Caso G: forza concentrata sulla trave del primo piano, carico
    uniforme sul secondo, trapezio sul terzo, cedimento del piede destro. Caso Q: carico uniforme in copertura.
    Soluzione esatta: travi appoggiate, colonne senza flessione, cedimento come moto rigido.
    Il vento, escluso il 18/11 per il punto 79, è reinserito il 22/11 come azione di accompagnamento (0,9 = 1,5·ψ0).
    """
    L, h, P, aP, q, qi, qj, d = 6.0, 3.5, 40.0, 2.0, 20.0, 10.0, 30.0, 0.010
    q2 = 15.0
    H = (5.0, 10.0, 15.0)
    gG, gQ, gW = 1.3, 1.5, 0.9
    m = base("C30", "Telaio a tre piani a travi incernierate, carichi misti combinati con il vento",
             "Una campata L = 6 m, tre piani h = 3,5 m; colonne HE 200 A continue e incastrate al piede, travi IPE 300 "
             "incernierate alle estremità; deformabilità assiale trascurata. Caso G: 40 kN a 2 m sulla trave del primo "
             "piano, 20 kN/m sul secondo, trapezio 10→30 kN/m sul terzo, cedimento di 10 mm del piede destro; caso Q: "
             "15 kN/m sulla trave di copertura; caso W: 5, 10 e 15 kN ai piani; combinazione 1,3·G + 1,5·Q + 0,9·W "
             "(Daniela e Valentina).")
    m["schema_version"] = "1.1"
    m["progetto"]["data"] = "2026-11-18"
    nodi = [{"id": 1, "x": 0, "y": 0}, {"id": 2, "x": L, "y": 0}]
    for k in (1, 2, 3):
        nodi += [{"id": 2 * k + 1, "x": 0, "y": k * h}, {"id": 2 * k + 2, "x": L, "y": k * h}]
    aste = []
    for k in (0, 1, 2):          # colonne: sinistra 2k+1 → 2k+3, destra 2k+2 → 2k+4
        aste += [{"id": 2 * k + 1, "nodo_i": 2 * k + 1, "nodo_j": 2 * k + 3, "materiale": "S275", "sezione": "HEA200"},
                 {"id": 2 * k + 2, "nodo_i": 2 * k + 2, "nodo_j": 2 * k + 4, "materiale": "S275", "sezione": "HEA200"}]
    for k in (1, 2, 3):          # travi 7, 8, 9
        aste.append({"id": 6 + k, "nodo_i": 2 * k + 1, "nodo_j": 2 * k + 2, "materiale": "S275", "sezione": "IPE300",
                     "svincoli": {"rz_i": True, "rz_j": True}})
    m.update({
        "nodi": nodi, "sezioni": [HEA200, IPE300], "aste": aste,
        "vincoli": [{"nodo": 1, "ux": True, "uy": True, "rz": True}, {"nodo": 2, "ux": True, "uy": True, "rz": True}],
        "casi_di_carico": [
            {"id": "G", "nome": "Carichi verticali e cedimento", "categoria": "G2",
             "carichi_aste": [{"asta": 7, "tipo": "concentrato", "direzione": "globale_y", "P": -P, "a": aP},
                              {"asta": 8, "tipo": "distribuito_uniforme", "direzione": "globale_y", "q": -q},
                              {"asta": 9, "tipo": "distribuito_trapezio", "direzione": "globale_y", "q_i": -qi, "q_j": -qj,
                               "a": 0.0, "b": L}],
             "cedimenti": [{"nodo": 2, "uy": -d}]},
            {"id": "Q", "nome": "Carico in copertura", "categoria": "Q",
             "carichi_aste": [{"asta": 9, "tipo": "distribuito_uniforme", "direzione": "globale_y", "q": -q2}]},
            {"id": "W", "nome": "Vento", "categoria": "vento",
             "carichi_nodali": [{"nodo": 2 * k + 1, "Fx": H[k - 1]} for k in (1, 2, 3)]}],
        "combinazioni": [{"id": "SLU1", "nome": "1,3·G + 1,5·Q + 0,9·W", "tipo": "SLU",
                          "coefficienti": {"G": gG, "Q": gQ, "W": gW}}],
        "analisi": {"tipo": "statica_lineare", "deformabilita_assiale": False, "punti_diagramma": 13},
    })
    Rs = P * (L - aP) / L + q * L / 2 + L * (2 * qi + qj) / 6       # reazioni sinistre delle tre travi
    Rd = P * aP / L + q * L / 2 + L * (qi + 2 * qj) / 6
    atteso = {"caso": "SLU1", "formule": {
        "travi appoggiate": "P: P(L−a)/L e Pa/L; uniforme: qL/2; trapezio: L(2qi + qj)/6 e L(qi + 2qj)/6",
        "caso Q": "trave di copertura appoggiata: q2·L/2 per colonna, M mezzeria q2·L²/8",
        "trapezio in x = 3 m": "M = Rs·x − qi·x²/2 − (qj − qi)·x³/(6L) = 90 kNm",
        "cedimento": "moto rigido della colonna destra; con il coefficiente 1,3 il cedimento combinato vale 13 mm",
        "vento": "ciascuna colonna porta metà delle forze di piano: Rx = −ΣH/2, M piede = Σ(H/2)·z",
        "combinazione": "1,3·G + 1,5·Q + 0,9·W"},
        "valori": [
            {"grandezza": "Ry nodo 1", "valore": gG * Rs + gQ * q2 * L / 2, "unita": "kN"},
            {"grandezza": "Ry nodo 2", "valore": gG * Rd + gQ * q2 * L / 2, "unita": "kN"},
            {"grandezza": "Rx nodo 1", "valore": -gW * sum(H) / 2, "unita": "kN"},
            {"grandezza": "|M| asta 1 x=0 (piede)", "valore": gW * sum(Hk / 2 * k * h for k, Hk in enumerate(H, start=1)), "unita": "kNm"},
            {"grandezza": "M asta 9 x=3 (mezzeria copertura)", "valore": gG * 90.0 + gQ * q2 * L ** 2 / 8, "unita": "kNm"},
            {"grandezza": "M asta 7 x=2 (sotto P)", "valore": gG * P * (L - aP) / L * aP, "unita": "kNm"},
            {"grandezza": "M asta 8 x=3 (mezzeria)", "valore": gG * q * L ** 2 / 8, "unita": "kNm"},
            {"grandezza": "uy nodo 8 (testa colonna destra)", "valore": -gG * d, "unita": "m"}]}
    return m, atteso


def c31():
    """C30 con la trave del secondo piano divisa in mezzeria e ΔT a farfalla (Daniela e Valentina, 20/11).

    Cerniere interne agli estremi di tutte le travi; la trave del secondo piano è divisa nel nodo 9 per leggere la
    freccia. Terzo caso T: ΔT a farfalla +20 °C sulle due aste di quella trave. Freccia di mezzeria esatta:
    - G: −5qL⁴/384EI più metà del cedimento della colonna destra (moto rigido della trave);
    - T: −κL²/8 con κ = α·ΔTg/h (lato inferiore più caldo, come C18 e C27);
    - Q: nessuna (carico solo in copertura).
    """
    m, _ = c30()
    # C30 ha il vento dal 22/11: C31 resta senza (il vento è in C32), con la descrizione di prima
    m["casi_di_carico"] = [x for x in m["casi_di_carico"] if x["id"] != "W"]
    m["progetto"]["descrizione"] = m["progetto"]["descrizione"].replace(
        "; caso W: 5, 10 e 15 kN ai piani; combinazione 1,3·G + 1,5·Q + 0,9·W", "; combinazione 1,3·G + 1,5·Q")
    L, h, q, d, dTg = 6.0, 3.5, 20.0, 0.010, 20.0
    gG, gQ, gT = 1.3, 1.5, 0.9
    m["progetto"].update({"id": "C31", "nome": "Telaio a tre piani a travi incernierate, carichi misti e ΔT",
                          "descrizione": m["progetto"]["descrizione"].replace(
                              "combinazione 1,3·G + 1,5·Q", "trave del secondo piano divisa in mezzeria; caso T: ΔT a "
                              "farfalla +20 °C su quella trave; combinazione 1,3·G + 1,5·Q + 0,9·T"),
                          "data": "2026-11-20"})
    m["schema_version"] = "1.2"
    m["materiali"] = [dict(ACC, alfa_t=ALFA)]
    m["sezioni"] = [HEA200, dict(IPE300, h=0.300)]
    m["nodi"].append({"id": 9, "x": L / 2, "y": 2 * h})
    m["aste"] = [a for a in m["aste"] if a["id"] != 8] + [
        {"id": 8, "nodo_i": 5, "nodo_j": 9, "materiale": "S275", "sezione": "IPE300", "svincoli": {"rz_i": True}},
        {"id": 10, "nodo_i": 9, "nodo_j": 6, "materiale": "S275", "sezione": "IPE300", "svincoli": {"rz_j": True}}]
    g = m["casi_di_carico"][0]
    g["carichi_aste"] = [x for x in g["carichi_aste"] if x["asta"] != 8] + [
        {"asta": a, "tipo": "distribuito_uniforme", "direzione": "globale_y", "q": -q} for a in (8, 10)]
    m["casi_di_carico"].append({"id": "T", "nome": "ΔT a farfalla sulla trave del secondo piano", "categoria": "temperatura",
                                "carichi_termici": [{"asta": a, "dT_g": dTg} for a in (8, 10)]})
    m["combinazioni"] = [{"id": "SLU1", "nome": "1,3·G + 1,5·Q + 0,9·T", "tipo": "SLU",
                          "coefficienti": {"G": gG, "Q": gQ, "T": gT}}]
    EI = E_ACC * IPE300["I"]
    fG = -5 * q * L ** 4 / (384 * EI) - d / 2
    fT = -ALFA * dTg / 0.300 * L ** 2 / 8
    q2 = 15.0
    Rs = 40.0 * 4 / 6 + q * L / 2 + L * (2 * 10.0 + 30.0) / 6
    Rd = 40.0 * 2 / 6 + q * L / 2 + L * (10.0 + 2 * 30.0) / 6
    atteso = {"caso": "SLU1", "formule": {
        "reazioni": "come C30: il ΔT a farfalla su travi isostatiche non dà reazioni",
        "freccia in mezzeria del secondo piano": "1,3·(−5qL⁴/384EI − δ/2) + 0,9·(−α·ΔTg/h·L²/8)",
        "combinazione": "1,3·G + 1,5·Q + 0,9·T"},
        "valori": [
            {"grandezza": "Ry nodo 1", "valore": gG * Rs + gQ * q2 * L / 2, "unita": "kN"},
            {"grandezza": "Ry nodo 2", "valore": gG * Rd + gQ * q2 * L / 2, "unita": "kN"},
            {"grandezza": "M asta 1 x=0 (piede)", "valore": 0.0, "unita": "kNm"},
            {"grandezza": "M asta 8 x=3 (mezzeria secondo piano)", "valore": gG * q * L ** 2 / 8, "unita": "kNm"},
            {"grandezza": "uy nodo 9 (mezzeria secondo piano)", "valore": gG * fG + gT * fT, "unita": "m"}]}
    return m, atteso


def c32():
    """C31 con il vento: la variante rinviata il 18/11 e il 20/11 per il punto 79 (Daniela e Valentina, 21/11).

    Dal 21/11 le aste incernierate con deformabilità assiale trascurata usano R = 10⁶ (RAPPORTO_ASSIALE_CERNIERE)
    e i due solutori concordano entro 10⁻⁶. Caso W: 5, 10 e 15 kN ai piani; le colonne uguali, collegate da travi
    incernierate rigide, portano ciascuna metà del vento (come C24). Combinazione con il carico in copertura come
    azione principale: 1,3·G + 1,5·Q + 0,9·W + 0,9·T (0,9 = 1,5·ψ0 con ψ0 = 0,6, valori da ricontrollare sulle NTC).
    """
    m, _ = c31()
    L, h = 6.0, 3.5
    H = (5.0, 10.0, 15.0)
    gG, gQ, gW, gT = 1.3, 1.5, 0.9, 0.9
    m["progetto"].update({"id": "C32", "nome": "Telaio a tre piani a travi incernierate, carichi misti, ΔT e vento",
                          "descrizione": m["progetto"]["descrizione"].replace(
                              "combinazione 1,3·G + 1,5·Q + 0,9·T", "caso W: 5, 10 e 15 kN ai piani; combinazione "
                              "1,3·G + 1,5·Q + 0,9·W + 0,9·T"), "data": "2026-11-21"})
    m["casi_di_carico"].append({"id": "W", "nome": "Vento", "categoria": "vento",
                                "carichi_nodali": [{"nodo": 2 * k + 1, "Fx": H[k - 1]} for k in (1, 2, 3)]})
    m["combinazioni"] = [{"id": "SLU1", "nome": "1,3·G + 1,5·Q + 0,9·W + 0,9·T", "tipo": "SLU",
                          "coefficienti": {"G": gG, "Q": gQ, "W": gW, "T": gT}}]
    Rs = 40.0 * 4 / 6 + 20.0 * L / 2 + L * (2 * 10.0 + 30.0) / 6
    Rd = 40.0 * 2 / 6 + 20.0 * L / 2 + L * (10.0 + 2 * 30.0) / 6
    Mw = sum(Hk / 2 * k * h for k, Hk in enumerate(H, start=1))
    atteso = {"caso": "SLU1", "formule": {
        "verticali": "come C31: travi appoggiate, colonne senza flessione per G, Q e T",
        "vento": "ciascuna colonna porta metà delle forze di piano: Rx = −ΣH/2, M piede = Σ(H/2)·z, Ry = 0",
        "combinazione": "1,3·G + 1,5·Q + 0,9·W + 0,9·T"},
        "valori": [
            {"grandezza": "Ry nodo 1", "valore": gG * Rs + gQ * 15.0 * L / 2, "unita": "kN"},
            {"grandezza": "Ry nodo 2", "valore": gG * Rd + gQ * 15.0 * L / 2, "unita": "kN"},
            {"grandezza": "Rx nodo 1", "valore": -gW * sum(H) / 2, "unita": "kN"},
            {"grandezza": "Rx nodo 2", "valore": -gW * sum(H) / 2, "unita": "kN"},
            {"grandezza": "|M| asta 1 x=0 (piede)", "valore": gW * Mw, "unita": "kNm"},
            {"grandezza": "M asta 8 x=3 (mezzeria secondo piano)", "valore": gG * 20.0 * L ** 2 / 8, "unita": "kNm"}]}
    return m, atteso


def c33():
    """Portale con trave incernierata da un solo lato, deformabilità assiale trascurata (punto 98; Valentina, 22/11).

    Colonne HE 200 A incastrate al piede (h = 4 m), traverso IPE 300 (L = 6 m) incastrato alla colonna sinistra e
    incernierato su quella destra; forza orizzontale H in testa a sinistra. Metodo delle rotazioni, incognite la
    rotazione θ del nodo sinistro in alto e lo spostamento orizzontale Δ del traverso (assialmente rigido):
    - nodo: (4EIc/h + 3EIb/L)·θ = 6EIc·Δ/h²
    - traslazione: H = (12EIc/h³)·Δ − (6EIc/h²)·θ + (3EIc/h³)·Δ
    θ è positivo in senso orario (convenzione del metodo); nello schema rz è antiorario, quindi rz = −θ.
    Momenti: colonna sinistra in alto Mt = EIc/h·(4θ − 6Δ/h), al piede Mp = EIc/h·(2θ − 6Δ/h); trave all'estremo
    sinistro 3EIb/L·θ; colonna destra al piede 3EIc·Δ/h².
    """
    h, L, H = 4.0, 6.0, 20.0
    EIc, EIb = E_ACC * HEA200["I"], E_ACC * IPE300["I"]
    a11, a12 = 4 * EIc / h + 3 * EIb / L, -6 * EIc / h ** 2          # equazione del nodo: a11·θ + a12·Δ = 0
    a21, a22 = -6 * EIc / h ** 2, 15 * EIc / h ** 3                 # traslazione:       a21·θ + a22·Δ = H
    det = a11 * a22 - a12 * a21
    th, D = (-a12 * H) / det, (a11 * H) / det
    Mt = EIc / h * (4 * th - 6 * D / h)
    Mp = EIc / h * (2 * th - 6 * D / h)
    Mb = 3 * EIb / L * th
    Md = 3 * EIc * D / h ** 2
    m = trave("C33", "Portale con traverso incernierato da un solo lato, assiale rigida",
              "Colonne HE 200 A incastrate al piede, h = 4 m; traverso IPE 300, L = 6 m, incastrato alla colonna sinistra e "
              "incernierato su quella destra; deformabilità assiale trascurata; H = 20 kN in testa a sinistra "
              "(Valentina, punto 98).",
              [{"id": 1, "x": 0, "y": 0}, {"id": 2, "x": 0, "y": h}, {"id": 3, "x": L, "y": h}, {"id": 4, "x": L, "y": 0}],
              [{"id": 1, "nodo_i": 1, "nodo_j": 2, "materiale": "S275", "sezione": "HEA200"},
               {"id": 2, "nodo_i": 2, "nodo_j": 3, "materiale": "S275", "sezione": "IPE300", "svincoli": {"rz_j": True}},
               {"id": 3, "nodo_i": 4, "nodo_j": 3, "materiale": "S275", "sezione": "HEA200"}],
              [{"nodo": 1, "ux": True, "uy": True, "rz": True}, {"nodo": 4, "ux": True, "uy": True, "rz": True}],
              {"id": "H", "nome": "Forza orizzontale", "categoria": "vento", "carichi_nodali": [{"nodo": 2, "Fx": H}]}, 11)
    m["sezioni"] = [HEA200, IPE300]
    m["analisi"]["deformabilita_assiale"] = False
    m["progetto"]["data"] = "2026-11-22"
    atteso = {"caso": "H", "formule": {
        "nodo": "(4EIc/h + 3EIb/L)·θ = 6EIc·Δ/h² (θ orario; rz = −θ)",
        "equilibrio": "tagli delle colonne (Mt + Mp)/h + Md/h = H",
        "traslazione": "H = 15EIc·Δ/h³ − 6EIc·θ/h²",
        "momenti": "Mt = EIc/h·(4θ − 6Δ/h); Mp = EIc/h·(2θ − 6Δ/h); trave 3EIb·θ/L; colonna destra al piede 3EIc·Δ/h²"},
        "valori": [
            {"grandezza": "ux nodo 2", "valore": D, "unita": "m"},
            {"grandezza": "rz nodo 2", "valore": -th, "unita": "rad"},   # θ orario nel metodo, rz antiorario nello schema
            {"grandezza": "|M| asta 1 x=h (testa colonna sinistra)", "valore": abs(Mt), "unita": "kNm"},
            {"grandezza": "|M| asta 1 x=0 (piede sinistro)", "valore": abs(Mp), "unita": "kNm"},
            {"grandezza": "|M| asta 2 x=0 (traverso, nodo rigido)", "valore": abs(Mb), "unita": "kNm"},
            {"grandezza": "|M| asta 3 x=0 (piede destro)", "valore": abs(Md), "unita": "kNm"},
            {"grandezza": "M asta 2 x=L (cerniera)", "valore": 0.0, "unita": "kNm"}]}
    return m, atteso


# Casi C34–C38 (Valentina, Daniela, 24/11): coprono le funzioni dello schema senza casi trovate da copertura.py


def c34():
    """Mensola IPE 300, L = 4 m: peso proprio (G) e momento nodale in punta (M); 1,3·G + 1,5·M."""
    L, Mz = 4.0, 10.0
    q = ACC["peso_specifico"] * IPE300["A"]                     # kN/m
    EI = E_ACC * IPE300["I"]
    m = trave("C34", "Mensola, peso proprio e momento nodale",
              "Mensola IPE 300, L = 4 m, incastrata in 1; caso G: peso proprio (γ = 78,5 kN/m³); caso M: momento "
              "antiorario di 10 kNm in punta; combinazione 1,3·G + 1,5·M (Valentina).",
              [{"id": 1, "x": 0, "y": 0}, {"id": 2, "x": L, "y": 0}],
              [{"id": 1, "nodo_i": 1, "nodo_j": 2, "materiale": "S275", "sezione": "IPE300"}],
              [{"nodo": 1, "ux": True, "uy": True, "rz": True}],
              {"id": "G", "nome": "Peso proprio", "categoria": "G1", "peso_proprio": True}, 11)
    m["casi_di_carico"].append({"id": "M", "nome": "Momento in punta", "categoria": "Q",
                                "carichi_nodali": [{"nodo": 2, "Mz": Mz}]})
    m["combinazioni"] = [{"id": "SLU1", "nome": "1,3·G + 1,5·M", "tipo": "SLU", "coefficienti": {"G": 1.3, "M": 1.5}}]
    m["progetto"]["data"] = "2026-11-24"
    atteso = {"caso": "SLU1", "formule": {
        "G": "q = γA; Ry = qL; M(0) = −qL²/2; uy punta = −qL⁴/8EI",
        "M": "momento antiorario in punta: M = +Mz costante (fibre inferiori tese); uy punta = +MzL²/2EI; rz = MzL/EI"},
        "valori": [
            {"grandezza": "Ry nodo 1", "valore": 1.3 * q * L, "unita": "kN"},
            {"grandezza": "M asta 1 x=0", "valore": 1.3 * (-q * L ** 2 / 2) + 1.5 * Mz, "unita": "kNm"},
            {"grandezza": "uy nodo 2", "valore": 1.3 * (-q * L ** 4 / (8 * EI)) + 1.5 * Mz * L ** 2 / (2 * EI), "unita": "m"},
            {"grandezza": "rz nodo 2", "valore": 1.3 * (-q * L ** 3 / (6 * EI)) + 1.5 * Mz * L / EI, "unita": "rad"}]}
    return m, atteso


def c35():
    """Trave IPE 300 doppiamente incastrata, L = 6 m: rotazione impressa in 1 e spostamento assiale impresso in 2."""
    L, th, dx = 6.0, 0.001, 0.002
    EI, EA = E_ACC * IPE300["I"], E_ACC * IPE300["A"]
    m = v11(trave("C35", "Trave doppiamente incastrata, cedimenti rz e ux",
                  "IPE 300, L = 6 m, incastri in 1 e 2; cedimenti: rotazione 1 mrad del nodo 1, spostamento orizzontale "
                  "di 2 mm del nodo 2 (Valentina).",
                  [{"id": 1, "x": 0, "y": 0}, {"id": 2, "x": L, "y": 0}],
                  [{"id": 1, "nodo_i": 1, "nodo_j": 2, "materiale": "S275", "sezione": "IPE300"}],
                  [{"nodo": 1, "ux": True, "uy": True, "rz": True}, {"nodo": 2, "ux": True, "uy": True, "rz": True}],
                  {"id": "D", "nome": "Cedimenti", "categoria": "altro",
                   "cedimenti": [{"nodo": 1, "rz": th}, {"nodo": 2, "ux": dx}]}, 13))
    m["progetto"]["data"] = "2026-11-24"
    atteso = {"caso": "D", "formule": {
        "rotazione impressa": "momenti d'estremità 4EIθ/L e 2EIθ/L, di segno opposto nella convenzione della trave; taglio 6EIθ/L²",
        "allungamento impresso": "N = EA·δ/L, trazione"},
        "valori": [
            {"grandezza": "N asta 1 x=3", "valore": EA * dx / L, "unita": "kN"},
            {"grandezza": "|M| asta 1 x=0", "valore": 4 * EI * th / L, "unita": "kNm"},
            {"grandezza": "|M| asta 1 x=L", "valore": 2 * EI * th / L, "unita": "kNm"},
            {"grandezza": "|V| asta 1 x=3", "valore": 6 * EI * th / L ** 2, "unita": "kN"},
            {"grandezza": "rz nodo 1", "valore": th, "unita": "rad"}]}
    return m, atteso


def c36():
    """Mensola IPE 300, L = 3 m, con il piede su molla orizzontale kx e rotazionale kr (uy impedito)."""
    L, kx, kr, P, H = 3.0, 1.0e4, 5000.0, 10.0, 20.0
    EI, EA = E_ACC * IPE300["I"], E_ACC * IPE300["A"]
    m = trave("C36", "Mensola su molle orizzontale e rotazionale",
              "Mensola IPE 300, L = 3 m; nodo 1 con uy impedito, molla orizzontale kx = 10 000 kN/m e rotazionale "
              "kr = 5000 kNm/rad; in punta P = 10 kN verso il basso e H = 20 kN verso destra (Valentina).",
              [{"id": 1, "x": 0, "y": 0}, {"id": 2, "x": L, "y": 0}],
              [{"id": 1, "nodo_i": 1, "nodo_j": 2, "materiale": "S275", "sezione": "IPE300"}],
              [{"nodo": 1, "uy": True, "molle": {"kx": kx, "kr": kr}}],
              {"id": "Q", "nome": "Forze in punta", "categoria": "Q", "carichi_nodali": [{"nodo": 2, "Fx": H, "Fy": -P}]}, 11)
    m["progetto"]["data"] = "2026-11-24"
    rz1 = -P * L / kr
    atteso = {"caso": "Q", "formule": {
        "molla orizzontale": "ux1 = H/kx; Rx = −H",
        "molla rotazionale": "rz1 = −PL/kr (orario)",
        "punta": "uy2 = −PL³/3EI + rz1·L; ux2 = H/kx + HL/EA"},
        "valori": [
            {"grandezza": "Ry nodo 1", "valore": P, "unita": "kN"},
            {"grandezza": "Rx nodo 1", "valore": -H, "unita": "kN"},
            {"grandezza": "ux nodo 1", "valore": H / kx, "unita": "m"},
            {"grandezza": "rz nodo 1", "valore": rz1, "unita": "rad"},
            {"grandezza": "uy nodo 2", "valore": -P * L ** 3 / (3 * EI) + rz1 * L, "unita": "m"},
            {"grandezza": "ux nodo 2", "valore": H / kx + H * L / EA, "unita": "m"}]}
    return m, atteso


def c37():
    """Mensola inclinata 3-4-5 (L = 5 m) incastrata al piede, carichi in direzione locale e globale X.

    Asse da (0; 0) a (4; 3): c = 0,8, s = 0,6; y locale = (−0,6; 0,8). Valori per unità di lunghezza dell'asta.
    Isostatica: reazioni dalla somma delle risultanti e dei loro momenti attorno al piede.
    """
    c, s_, L = 0.8, 0.6, 5.0
    q, P, aP, H, aH, qx = -4.0, -10.0, 2.0, 6.0, 2.5, 4.0
    m = trave("C37", "Mensola inclinata, carichi locali e orizzontali",
              "Mensola IPE 300 da (0; 0) a (4; 3), L = 5 m, incastrata al piede; casi: A uniforme normale all'asta "
              "−4 kN/m (locale_y); B forza normale all'asta −10 kN a 2 m; C forza orizzontale 6 kN a 2,5 m; "
              "D trapezio orizzontale da 0 a 4 kN/m su tutta l'asta; combinazione A + B + C + D (Daniela).",
              [{"id": 1, "x": 0, "y": 0}, {"id": 2, "x": 4, "y": 3}],
              [{"id": 1, "nodo_i": 1, "nodo_j": 2, "materiale": "S275", "sezione": "IPE300"}],
              [{"nodo": 1, "ux": True, "uy": True, "rz": True}],
              {"id": "A", "nome": "Uniforme normale all'asta", "categoria": "Q",
               "carichi_aste": [{"asta": 1, "tipo": "distribuito_uniforme", "direzione": "locale_y", "q": q}]}, 11)
    m["schema_version"] = "1.1"
    m["casi_di_carico"] += [
        {"id": "B", "nome": "Forza normale all'asta", "categoria": "Q",
         "carichi_aste": [{"asta": 1, "tipo": "concentrato", "direzione": "locale_y", "P": P, "a": aP}]},
        {"id": "C", "nome": "Forza orizzontale", "categoria": "vento",
         "carichi_aste": [{"asta": 1, "tipo": "concentrato", "direzione": "globale_x", "P": H, "a": aH}]},
        {"id": "D", "nome": "Trapezio orizzontale", "categoria": "vento",
         "carichi_aste": [{"asta": 1, "tipo": "distribuito_trapezio", "direzione": "globale_x", "q_i": 0.0, "q_j": qx,
                           "a": 0.0, "b": L}]}]
    m["combinazioni"] = [{"id": "TOT", "nome": "A + B + C + D", "tipo": "SLE_rara", "coefficienti": {"A": 1, "B": 1, "C": 1, "D": 1}}]
    m["progetto"]["data"] = "2026-11-24"
    yl = (-s_, c)
    F = [(q * L * yl[0], q * L * yl[1]), (P * yl[0], P * yl[1]), (H, 0.0), (qx * L / 2, 0.0)]
    # momenti antiorari attorno al piede: forza normale all'asta a distanza r → valore·r; forze orizzontali → −y·Fx
    Mo = [q * L ** 2 / 2, P * aP, -(aH * s_) * H, -(2 / 3 * L * s_) * (qx * L / 2)]
    atteso = {"caso": "TOT", "formule": {
        "risultanti": "A: qL normale all'asta; B: P normale; C: H orizzontale; D: qx·L/2 orizzontale a 2L/3",
        "momenti attorno al piede": "qL²/2 + P·a − H·a·s − (qx·L/2)·(2L/3)·s",
        "reazioni": "opposte alla somma delle risultanti e dei loro momenti"},
        "valori": [
            {"grandezza": "Rx nodo 1", "valore": -sum(f[0] for f in F), "unita": "kN"},
            {"grandezza": "Ry nodo 1", "valore": -sum(f[1] for f in F), "unita": "kN"},
            {"grandezza": "Mz nodo 1 (reazione)", "valore": -sum(Mo), "unita": "kNm"},
            {"grandezza": "|M| asta 1 x=0", "valore": abs(sum(Mo)), "unita": "kNm"}]}
    return m, atteso


def c38():
    """Trave IPE 300, L = 6 m, incastrata in 1 e a pattino in 2 (ux e rz impediti, uy libero), carico uniforme.

    È metà di una trave doppiamente incastrata di luce 2L: M(0) = −qL²/3, M(L) = +qL²/6, freccia qL⁴/24EI.
    """
    L, q = 6.0, 10.0
    EI = E_ACC * IPE300["I"]
    m = trave("C38", "Trave incastrata e a pattino, carico uniforme",
              "IPE 300, L = 6 m, incastrata in 1, nodo 2 a pattino (ux e rz impediti, uy libero); q = 10 kN/m (Valentina).",
              [{"id": 1, "x": 0, "y": 0}, {"id": 2, "x": L, "y": 0}],
              [{"id": 1, "nodo_i": 1, "nodo_j": 2, "materiale": "S275", "sezione": "IPE300"}],
              [{"nodo": 1, "ux": True, "uy": True, "rz": True}, {"nodo": 2, "ux": True, "rz": True}],
              {"id": "Q", "nome": "Uniforme", "categoria": "Q",
               "carichi_aste": [{"asta": 1, "tipo": "distribuito_uniforme", "direzione": "globale_y", "q": -q}]}, 13)
    m["progetto"]["data"] = "2026-11-24"
    atteso = {"caso": "Q", "formule": {
        "simmetria": "metà di una trave doppiamente incastrata di luce 2L",
        "valori": "Ry1 = qL; M(0) = −q(2L)²/12 = −qL²/3; M(L) = q(2L)²/24 = qL²/6; uy2 = −q(2L)⁴/384EI = −qL⁴/24EI"},
        "valori": [
            {"grandezza": "Ry nodo 1", "valore": q * L, "unita": "kN"},
            {"grandezza": "M asta 1 x=0", "valore": -q * L ** 2 / 3, "unita": "kNm"},
            {"grandezza": "M asta 1 x=L", "valore": q * L ** 2 / 6, "unita": "kNm"},
            {"grandezza": "uy nodo 2", "valore": -q * L ** 4 / (24 * EI), "unita": "m"}]}
    return m, atteso


if __name__ == "__main__":
    for nome, f in (("C1_trave_appoggiata", c1), ("C2_mensola", c2), ("C3_portale_forza_orizzontale", c3),
                    ("C4_portale_carico_uniforme", c4), ("C5_telaio_due_piani", c5),
                    ("C6_trave_gerber", c6), ("C7_carico_concentrato", c7), ("C8_molla_in_mezzeria", c8),
                    ("C9_portale_tre_cerniere_molla", c9),
                    ("C10_combinazione_slu", c10), ("C11_cedimento_appoggio", c11),
                    ("C12_trapezio_parziale", c12), ("C13_triangolare_incastrata", c13),
                    ("C15_inclinata_parziale", c15), ("C16_gerber_cedimento", c16),
                    ("C17_inclinata_normale", c17), ("C14_termica_incastrata", c14),
                    ("C18_termica_appoggiata", c18), ("C19_gerber_termica", c19),
                    ("C20_gerber_trapezio", c20), ("C21_inclinata_trapezio_cedimento", c21),
                    ("C22_gerber_trapezio_molla", c22), ("C23_combinazione_termica", c23),
                    ("C24_due_piani_combinazione", c24),
                    ("C25_tre_cerniere_trapezio_cedimento", c25),
                    ("C26_continua_carico_cedimento", c26),
                    ("C27_due_piani_termica", c27),
                    ("C28_portale_asimmetrico", c28),
                    ("C29_due_piani_trapezio_cedimento", c29),
                    ("C30_tre_piani_misti", c30),
                    ("C31_tre_piani_termica", c31),
                    ("C32_tre_piani_vento", c32),
                    ("C33_portale_una_cerniera", c33),
                    ("C34_mensola_peso_momento", c34), ("C35_incastrata_cedimenti_rz_ux", c35),
                    ("C36_mensola_molle", c36), ("C37_inclinata_carichi_locali", c37),
                    ("C38_incastro_pattino", c38)):
        m, a = f()
        scrivi(nome + ".json", m)
        scrivi(nome + ".atteso.json", a)
        print("scritto", nome)
