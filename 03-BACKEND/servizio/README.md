# Servizio di calcolo (Natalia)

FastAPI. Valida il modello con `01-ARCHITETTURA/DATA_SCHEMA.json`, controlla la coerenza dei riferimenti (nodi, aste, materiali, sezioni), chiama il solutore Fortran tramite il convertitore e restituisce i risultati. Pubblica anche l'interfaccia 3D.

    04-FORTRAN-SOLVER/build.sh
    python3 -m pip install fastapi uvicorn jsonschema httpx
    python3 -m uvicorn --app-dir 03-BACKEND/servizio app:app --port 8000

| Metodo | Percorso | Funzione |
|---|---|---|
| GET | `/api/salute` | stato del servizio, del solutore e dello schema |
| GET | `/api/casi`, `/api/casi/{nome}` | elenco e contenuto dei casi di prova |
| POST | `/api/valida` | errori di schema e di coerenza |
| POST | `/api/calcola?caso=ID` | risultati (422 con l'elenco degli errori se il modello non è valido o la struttura è labile) |

Prove: `python3 03-BACKEND/servizio/test_app.py` (8 prove, comprese C1 e C3 attraverso il Fortran).
