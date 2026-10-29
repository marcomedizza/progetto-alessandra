# Rapporto di Alessandra — 29/10/2026

**Oggetto**: stato della catena del prototipo per la revisione di Marco del 30/10.

**Catena verificata**: compilazione del solutore, servizio FastAPI, verifica dei casi C1–C10 per i tre percorsi (riferimento, Fortran, servizio), 12 prove del servizio, 16 scenari utente. Tutto superato.

**Difetti del team tech**

| Difetto | Stato | Correttivo assegnato |
|---|---|---|
| D3 valori sui diagrammi | chiuso 29/10 | — |
| D4 disegno di nodi e aste | chiuso in versione minima (inserimento per coordinate) | D10: disegno col mouse — Irene, Lucia |
| D8 deformata sulle aste con cerniere | aperto | Elisa: restituire dal solutore la rotazione dell'estremità svincolata; Mariana: usarla nella deformata |
| Revisione 14: materiali e sezioni non inseribili dall'interfaccia | aperto | Lucia |
| Revisione 6: matrice piena (limite 1000 nodi) | aperto | Elisa, Ottavia: matrice a banda |

**Bloccati, fuori dal team tech**
- Studio dei testi: il collegatore Google Drive non vede i PDF di RIFERIMENTI.
- ModeSt (Carla, Daniela): manca la documentazione del formato; richiesta a Marco in `05-RICERCA/modest.md`.

**Per la revisione del 30/10**: chiedo a Marco di controllare i valori attesi dei casi C6–C10 (`06-TESTING/casi/README.md`) e di provare l'interfaccia in Firefox.
