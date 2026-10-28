# Solutore Fortran telaio2d — v0.1

Telai piani, statica lineare, metodo degli spostamenti (Elisa, compilazione Ottavia).

- Sorgente: `src/telaio2d.f90` (Fortran 2008, nessuna libreria esterna)
- Compilazione: `./build.sh` (richiede gfortran) → `bin/telaio2d`
- Uso: `bin/telaio2d input.txt output.txt`; il formato dei file è descritto in testa al sorgente
- Chiamata da Python: `esegui.py` (Ottavia), con tempo massimo di calcolo e messaggi d'errore puliti
- Ingresso e uscita sono gestiti dal convertitore `03-BACKEND/converter/converti.py`
- Controlli in lettura (28/10): carichi su aste inesistenti, identificativi duplicati di nodi e aste

Gestisce: aste inclinate, cerniere interne, vincoli e molle, carichi nodali, carichi d'asta uniformi e concentrati, peso proprio (tramite convertitore), deformabilità assiale escludibile.

**Verifica (26/10/2026)**: `python3 06-TESTING/casi/verifica_casi.py --fortran` supera tutti i controlli sui casi C1–C5. Il confronto completo con il risolutore di riferimento Python dà zero scostamenti, anche su un caso misto con cerniera, molla, asta inclinata e peso proprio.

**Prossimi passi**: matrice a banda e LAPACK (prestazioni), combinazioni di carico, P-Delta.
