"""Servizio del prototipo (Natalia) — FastAPI.

Avvio dalla radice del repository:
    04-FORTRAN-SOLVER/build.sh
    python3 -m uvicorn --app-dir 03-BACKEND/servizio app:app --port 8000
poi aprire http://127.0.0.1:8000/ (vista 3D di 02-FRONTEND-3D).

Interfaccia:
    GET  /api/salute              → stato del servizio e del solutore
    GET  /api/casi                → elenco dei casi di prova disponibili
    GET  /api/casi/{nome}         → modello del caso (JSON, schema v1.0)
    GET  /api/esempio             → esempio di riferimento 01-ARCHITETTURA/ESEMPIO_PORTALE_2D.json
    POST /api/valida              → controllo del modello con lo schema
    POST /api/calcola?caso=ID     → valida, calcola con il solutore Fortran, restituisce i risultati
    POST /api/calcola?combinazione=ID → risultati della combinazione (sovrapposizione lineare dei casi)
"""

import collections
import glob
import json
import logging
import math
import os
import sys

from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(QUI, "..", ".."))
sys.path.insert(0, os.path.join(RADICE, "03-BACKEND", "converter"))
import converti  # noqa: E402

try:
    import jsonschema
    with open(os.path.join(RADICE, "01-ARCHITETTURA", "DATA_SCHEMA.json"), encoding="utf-8") as fh:
        SCHEMA = json.load(fh)
    VALIDATORE = jsonschema.Draft202012Validator(SCHEMA)
except ImportError:  # validazione disattivata solo se manca la libreria
    VALIDATORE = None

# Via rapida (punto 56, Natalia e Ottavia, 08/11): jsonschema-rs, compilato, dice solo se il modello è valido;
# sul modello da 9150 aste impiega 3 ms invece di 1,0 s. Se non è valido, i messaggi d'errore restano quelli
# di jsonschema. Concordanza verificata su 120 modelli validi e volutamente errati. Facoltativo: senza la
# libreria si usa solo jsonschema.
try:
    import jsonschema_rs
    VALIDATORE_RAPIDO = jsonschema_rs.validator_for(SCHEMA) if VALIDATORE is not None else None
except ImportError:
    VALIDATORE_RAPIDO = None
# modelli su cui i due validatori non concordano (punto 58); solo gli ultimi 100 (punto 60), il resto è nel log
ANOMALIE_VALIDAZIONE = collections.deque(maxlen=100)

CASI = os.path.join(RADICE, "06-TESTING", "casi")

# Limiti di dimensione (Natalia, 29/10; alzati il 30/10 con la matrice a banda del solutore v0.2:
# 4681 nodi e 9150 aste in 0,5 s, risultati 3,4 MB; misure in 04-FORTRAN-SOLVER/prova_prestazioni.py).
MAX_NODI = 5000
MAX_ASTE = 10000
FRONTEND = os.path.join(RADICE, "02-FRONTEND-3D")

app = FastAPI(title="Progetto Alessandra — servizio di calcolo", version="0.1")


def numeri_non_finiti(x, percorso="(radice)"):
    """Percorsi dei numeri NaN o infiniti: il JSON di Python li accetta, lo schema no (Natalia, 13/11)."""
    if isinstance(x, float) and not math.isfinite(x):
        return [percorso]
    if isinstance(x, dict):
        return [p for k, v in x.items() for p in numeri_non_finiti(v, f"{percorso}/{k}".removeprefix("(radice)/"))]
    if isinstance(x, list):
        return [p for i, v in enumerate(x) for p in numeri_non_finiti(v, f"{percorso}/{i}".removeprefix("(radice)/"))]
    return []


def errori_schema(modello):
    # prima dei validatori: jsonschema-rs rifiuta NaN e infinito, jsonschema li accetta (sarebbe una falsa
    # discordanza, punto 58) e il calcolo fallirebbe con un errore interno
    non_finiti = numeri_non_finiti(modello)
    if non_finiti:
        return [{"percorso": p, "messaggio": "valore non finito (NaN o infinito)"} for p in non_finiti]
    if VALIDATORE is None:
        return []
    if VALIDATORE_RAPIDO is not None and VALIDATORE_RAPIDO.is_valid(modello):
        return []
    errori = [{"percorso": "/".join(str(p) for p in e.path) or "(radice)", "messaggio": e.message}
              for e in sorted(VALIDATORE.iter_errors(modello), key=str)]
    if not errori and VALIDATORE_RAPIDO is not None:
        # punto 58 (Natalia, 09/11): la via rapida rifiuta ma jsonschema non trova errori. Fa fede jsonschema, che
        # dà i messaggi all'utente: il modello è accettato e la discordanza resta registrata per l'analisi
        ANOMALIE_VALIDAZIONE.append(modello.get("progetto", {}).get("id", "?"))
        logging.getLogger("servizio").warning("validatori discordi sul modello %s", ANOMALIE_VALIDAZIONE[-1])
    return errori


def lunghezza_nulla(coord, asta):
    i, j = coord.get(asta["nodo_i"]), coord.get(asta["nodo_j"])
    return i is not None and j is not None and math.dist(i, j) < 1e-9


def risultati_finiti(r):
    """Vero se tutti i numeri dei risultati sono finiti: carichi o dimensioni fuori scala danno infiniti."""
    return not numeri_non_finiti(r)


def errori_coerenza(modello):
    """Controlli che lo schema non può fare: riferimenti tra nodi, aste, materiali e sezioni."""
    err = []
    if len(modello.get("nodi", [])) > MAX_NODI or len(modello.get("aste", [])) > MAX_ASTE:
        return [f"modello troppo grande per il solutore v0.3: al massimo {MAX_NODI} nodi e {MAX_ASTE} aste"]
    nodi = {n["id"] for n in modello.get("nodi", [])}
    mat = {m["id"] for m in modello.get("materiali", [])}
    sez = {s["id"] for s in modello.get("sezioni", [])}
    aste = {a["id"] for a in modello.get("aste", [])}
    coord = {n["id"]: (n["x"], n["y"]) for n in modello.get("nodi", [])}
    if len(nodi) != len(modello.get("nodi", [])):
        err.append("identificativi dei nodi duplicati")
    for a in modello.get("aste", []):
        for k in ("nodo_i", "nodo_j"):
            if a[k] not in nodi:
                err.append(f"asta {a['id']}: {k} {a[k]} non esiste")
        if a["nodo_i"] == a["nodo_j"]:
            err.append(f"asta {a['id']}: nodi coincidenti")
        elif lunghezza_nulla(coord, a):
            err.append(f"asta {a['id']}: lunghezza nulla (i nodi {a['nodo_i']} e {a['nodo_j']} hanno le stesse coordinate)")
        if a["materiale"] not in mat:
            err.append(f"asta {a['id']}: materiale {a['materiale']} non definito")
        if a["sezione"] not in sez:
            err.append(f"asta {a['id']}: sezione {a['sezione']} non definita")
    for v in modello.get("vincoli", []):
        if v["nodo"] not in nodi:
            err.append(f"vincolo sul nodo {v['nodo']} inesistente")
    vincoli = {v["nodo"]: v for v in modello.get("vincoli", [])}
    aste_per_id = {a["id"]: a for a in modello.get("aste", [])}
    materiali = {m["id"]: m for m in modello.get("materiali", [])}
    sezioni = {x["id"]: x for x in modello.get("sezioni", [])}
    lunghezze = {a["id"]: math.dist(coord[a["nodo_i"]], coord[a["nodo_j"]]) for a in modello.get("aste", [])
                 if a["nodo_i"] in coord and a["nodo_j"] in coord}
    for c in modello.get("casi_di_carico", []):
        for q in c.get("carichi_nodali", []):
            if q["nodo"] not in nodi:
                err.append(f"caso {c['id']}: carico sul nodo {q['nodo']} inesistente")
        for q in c.get("carichi_aste", []):
            if q["asta"] not in aste:
                err.append(f"caso {c['id']}: carico sull'asta {q['asta']} inesistente")
            elif q["tipo"] == "distribuito_trapezio" and not 0 <= q["a"] < q["b"] <= lunghezze.get(q["asta"], 0) + 1e-9:
                err.append(f"caso {c['id']}: carico trapezoidale sull'asta {q['asta']} fuori dall'asta (serve 0 ≤ a < b ≤ L)")
        # cedimenti (v1.1, Carla): solo su componenti vincolate
        for d in c.get("cedimenti", []):
            v = vincoli.get(d["nodo"], {})
            for k in ("ux", "uy", "rz"):
                if d.get(k) and not v.get(k):
                    err.append(f"caso {c['id']}: cedimento {k} sul nodo {d['nodo']}, che non ha {k} vincolato")
        usa_v11 = c.get("cedimenti") or any(q["tipo"] == "distribuito_trapezio" for q in c.get("carichi_aste", []))
        if usa_v11 and modello.get("schema_version") not in ("1.1", "1.2"):
            err.append(f"caso {c['id']}: carichi trapezoidali e cedimenti richiedono schema_version 1.1 o successiva")
        # distorsioni termiche (v1.2, Benedetta): servono alfa_t del materiale e, per la farfalla, h della sezione
        if c.get("carichi_termici") and modello.get("schema_version") != "1.2":
            err.append(f"caso {c['id']}: le distorsioni termiche richiedono schema_version 1.2")
        rigida = not modello.get("analisi", {}).get("deformabilita_assiale", True)
        for t in c.get("carichi_termici", []):
            el = aste_per_id.get(t["asta"])
            if el is None:
                err.append(f"caso {c['id']}: distorsione termica sull'asta {t['asta']} inesistente")
                continue
            if not materiali.get(el["materiale"], {}).get("alfa_t"):
                err.append(f"caso {c['id']}: asta {t['asta']}: manca alfa_t del materiale {el['materiale']}")
            if t.get("dT_g") and not sezioni.get(el["sezione"], {}).get("h"):
                err.append(f"caso {c['id']}: asta {t['asta']}: il ΔT a farfalla richiede h della sezione {el['sezione']}")
            if t.get("dT_u") and rigida:
                err.append(f"caso {c['id']}: asta {t['asta']}: il ΔT uniforme non è calcolabile con deformabilità assiale trascurata")
    return err


@app.get("/api/salute")
def salute():
    return {"servizio": "ok", "solutore": os.path.exists(converti.SOLUTORE), "schema": VALIDATORE is not None}


@app.get("/api/casi")
def elenco_casi():
    out = []
    for f in sorted(glob.glob(os.path.join(CASI, "C*.json"))):
        if f.endswith((".atteso.json", ".riferimento.json")):
            continue
        with open(f, encoding="utf-8") as fh:
            m = json.load(fh)
        out.append({"nome": os.path.basename(f)[:-5], "titolo": m["progetto"]["nome"]})
    return out


@app.get("/api/casi/{nome}")
def caso(nome: str):
    if "/" in nome or ".." in nome:
        raise HTTPException(400, "nome non valido")
    f = os.path.join(CASI, nome + ".json")
    if not os.path.exists(f):
        raise HTTPException(404, "caso non trovato")
    with open(f, encoding="utf-8") as fh:
        return json.load(fh)


@app.get("/api/esempio")
def esempio():
    with open(os.path.join(RADICE, "01-ARCHITETTURA", "ESEMPIO_PORTALE_2D.json"), encoding="utf-8") as fh:
        return json.load(fh)


@app.post("/api/valida")
def valida(modello: dict):
    e = errori_schema(modello)
    c = [] if e else errori_coerenza(modello)
    return {"valido": not e and not c, "schema": e, "coerenza": c}


@app.post("/api/calcola")
def calcola(modello: dict, caso: str | None = None, combinazione: str | None = None):
    e = errori_schema(modello)
    c = [] if e else errori_coerenza(modello)
    if e or c:
        raise HTTPException(422, {"schema": e, "coerenza": c})
    casi = [x["id"] for x in modello["casi_di_carico"]]
    try:
        if combinazione:
            comb = next((x for x in modello.get("combinazioni", []) if x["id"] == combinazione), None)
            if comb is None:
                raise HTTPException(422, f"combinazione {combinazione} non definita")
            mancanti = [k for k in comb["coefficienti"] if k not in casi]
            if mancanti:
                raise HTTPException(422, f"la combinazione cita casi inesistenti: {', '.join(mancanti)}")
            out = [converti.combina(modello, combinazione)]
        else:
            scelti = [caso] if caso else casi
            for s in scelti:
                if s not in casi:
                    raise HTTPException(422, f"caso di carico {s} non definito")
            out = [converti.risultati(modello, s) for s in scelti]
        if not risultati_finiti(out):
            raise HTTPException(422, "risultati non finiti: carichi, rigidezze o dimensioni fuori scala")
        return {"risultati": out}
    except FileNotFoundError as ex:
        raise HTTPException(503, str(ex))
    except (RuntimeError, TimeoutError) as ex:
        raise HTTPException(422, f"solutore: {ex}")


@app.get("/")
def radice():
    return RedirectResponse("/app/")


if os.path.isdir(FRONTEND):
    app.mount("/app", StaticFiles(directory=FRONTEND, html=True), name="app")
