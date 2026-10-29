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

import glob
import json
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
        VALIDATORE = jsonschema.Draft202012Validator(json.load(fh))
except ImportError:  # validazione disattivata solo se manca la libreria
    VALIDATORE = None

CASI = os.path.join(RADICE, "06-TESTING", "casi")

# Limiti di dimensione (Natalia, 29/10): il solutore v0.1 usa una matrice piena (3 gdl per nodo, tre copie
# in memoria). Con 1000 nodi: circa 216 MB e meno di 1 s (misure in 04-FORTRAN-SOLVER/prova_prestazioni.py).
MAX_NODI = 1000
MAX_ASTE = 3000
FRONTEND = os.path.join(RADICE, "02-FRONTEND-3D")

app = FastAPI(title="Progetto Alessandra — servizio di calcolo", version="0.1")


def errori_schema(modello):
    if VALIDATORE is None:
        return []
    return [{"percorso": "/".join(str(p) for p in e.path) or "(radice)", "messaggio": e.message}
            for e in sorted(VALIDATORE.iter_errors(modello), key=str)]


def errori_coerenza(modello):
    """Controlli che lo schema non può fare: riferimenti tra nodi, aste, materiali e sezioni."""
    err = []
    if len(modello.get("nodi", [])) > MAX_NODI or len(modello.get("aste", [])) > MAX_ASTE:
        return [f"modello troppo grande per il solutore v0.1: al massimo {MAX_NODI} nodi e {MAX_ASTE} aste"]
    nodi = {n["id"] for n in modello.get("nodi", [])}
    mat = {m["id"] for m in modello.get("materiali", [])}
    sez = {s["id"] for s in modello.get("sezioni", [])}
    aste = {a["id"] for a in modello.get("aste", [])}
    if len(nodi) != len(modello.get("nodi", [])):
        err.append("identificativi dei nodi duplicati")
    for a in modello.get("aste", []):
        for k in ("nodo_i", "nodo_j"):
            if a[k] not in nodi:
                err.append(f"asta {a['id']}: {k} {a[k]} non esiste")
        if a["nodo_i"] == a["nodo_j"]:
            err.append(f"asta {a['id']}: nodi coincidenti")
        if a["materiale"] not in mat:
            err.append(f"asta {a['id']}: materiale {a['materiale']} non definito")
        if a["sezione"] not in sez:
            err.append(f"asta {a['id']}: sezione {a['sezione']} non definita")
    for v in modello.get("vincoli", []):
        if v["nodo"] not in nodi:
            err.append(f"vincolo sul nodo {v['nodo']} inesistente")
    for c in modello.get("casi_di_carico", []):
        for q in c.get("carichi_nodali", []):
            if q["nodo"] not in nodi:
                err.append(f"caso {c['id']}: carico sul nodo {q['nodo']} inesistente")
        for q in c.get("carichi_aste", []):
            if q["asta"] not in aste:
                err.append(f"caso {c['id']}: carico sull'asta {q['asta']} inesistente")
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
            return {"risultati": [converti.combina(modello, combinazione)]}
        scelti = [caso] if caso else casi
        for s in scelti:
            if s not in casi:
                raise HTTPException(422, f"caso di carico {s} non definito")
        return {"risultati": [converti.risultati(modello, s) for s in scelti]}
    except FileNotFoundError as ex:
        raise HTTPException(503, str(ex))
    except (RuntimeError, TimeoutError) as ex:
        raise HTTPException(422, f"solutore: {ex}")


@app.get("/")
def radice():
    return RedirectResponse("/app/")


if os.path.isdir(FRONTEND):
    app.mount("/app", StaticFiles(directory=FRONTEND, html=True), name="app")
