# Rapporto di Alessandra — 28/11/2026

**Perché il 26 e il 27/11 non ci sono commit**: il 26/11 il lavoro era pronto e provato, ma è andato perso quando il contenitore è stato sostituito, prima dell'invio al remoto. Il 27/11 l'esecuzione non è partita per lo stesso motivo. Il nuovo contenitore non aveva né gfortran né le dipendenze del servizio, che sono state reinstallate. Dal 28/11 ogni prodotto viene inviato subito (punto 114).

**Fatto oggi** (ogni voce ha un commit):
- archivio del cruscotto: assegnazioni del 26, 27 e 28/11, verifiche del 25, 26 e 27/11;
- Natalia: nuova prova del servizio su C34–C38, 23 valori a mano letti da `/api/calcola`; 43 prove;
- Ottavia: compilazione in 1,0 s; due avvisi `-Wcompare-reals`, non uno, entrambi voluti e spiegati nel README; scarto banda/piena massimo 1,5·10⁻⁸ m (C32);
- Irene, Mariana: C34 e C35 aggiunti allo scenario delle viste, controllati a vista con la soluzione a mano;
- Benedetta: `SimulationControl` (7 campi), `Timestep` (1) e `RunPeriod` (13) nel confronto epJSON. Building e Zone erano già presenti dal 23/11;
- Silvia: rapporto di confronto al 28/11, identico al 25/11 (nessuna regressione);
- Renata, Vittoria: 16 scenari su 16;
- Marisa: revisione, punti 111–114.

**Carla, cedimenti vincolari**: sono nel solutore dal 31/10 (`telaio2d.f90`, righe 160–170) e nello schema (`cedimenti`). Oggi sono stati verificati sui casi assegnati, dal servizio fino al Fortran:
- C11: cedimento di 10 mm, Ry centrale −4,874 kN;
- C16: rz = −0,005 rad;
- C29: uy = −10 mm;
- C30: uy = −13 mm;
- C35: rz = 0,001 rad, M d'incastro 11,70 e 5,85 kNm.

Tutti coincidono con la soluzione a mano. Non serve altro codice: l'assegnazione «commit in 04-FORTRAN-SOLVER» chiede un lavoro già fatto.

**Daniela, Valentina**: la suite resta completa (32 su 32). Un caso nuovo serve solo se lo schema cresce, e `copertura.py` lo segnala da sé.

**Paola**: `converti.py` passa C34–C38 senza modifiche. Lo schema v1.2 non prevede altri tipi di carico, quindi oggi non c'è nulla da aggiornare.

**Catena**: C1–C38 nei tre percorsi, 217 valori, 0 scostamenti; 43 prove del servizio, 9 dell'interfaccia, 16 scenari.

**Bloccati**:
- studio dei PDF (team strutturale, Elisa, Francesca, Gabriella): il 26 e il 28/11 il collegatore Google Drive non ha restituito nessun PDF (`mimeType = 'application/pdf'`: 0 risultati). Vede solo la cartella GEOTECNICA e i documenti creati dal collegatore stesso. `GOOGLE_SA_KEY_B64` è assente. Lo studio non viene simulato;
- Lucia, pannello delle proprietà su C34–C38: nessun ostacolo tecnico, oggi non c'è stato tempo;
- D12 e Firefox: solo a mano;
- documenti business: mancano fonti verificabili.

**Per Marco**: punto 76 (avvisi o rifiuto), proposte epJSON e termiche; accesso ai PDF (vedi sopra).
