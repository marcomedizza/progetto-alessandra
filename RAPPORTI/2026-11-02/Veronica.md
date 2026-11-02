# Rapporto di Veronica — 02/11/2026

Licenze di FastAPI, Uvicorn, jsonschema e Three.js verificate sui testi originali distribuiti con i pacchetti, nelle versioni dell'ambiente di prova. Il dettaglio è in `05-RICERCA/licenze_componenti.md`.

| Componente | Licenza |
|---|---|
| FastAPI | MIT |
| jsonschema | MIT |
| Three.js | MIT |
| Uvicorn | BSD 3 clausole |

Ho aggiunto due dipendenze indirette che mancavano: Starlette (BSD 3 clausole) e Pydantic (MIT). Sono tutte compatibili con la distribuzione, anche commerciale, se si riportano avvisi e testi di licenza. Da fare: fissare le versioni in un file dei requisiti.
