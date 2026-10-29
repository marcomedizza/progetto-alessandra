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

## Prestazioni (Ottavia, 29/10/2026)

`python3 04-FORTRAN-SOLVER/prova_prestazioni.py` — telai regolari, campate da 6 m, piani da 3,5 m, matrice piena:

| Telaio | Nodi | Aste | Gradi di libertà | Tempo |
|---|---|---|---|---|
| 1 × 10 | 22 | 30 | 66 | 0,005 s |
| 5 × 20 | 126 | 220 | 378 | 0,012 s |
| 10 × 40 | 451 | 840 | 1353 | 0,11 s |
| 12 × 50 | 663 | 1250 | 1989 | 0,23 s |

In tutti i casi la somma delle reazioni verticali coincide con il carico applicato. Il tempo cresce circa con il cubo dei gradi di libertà e la memoria con il quadrato (tre matrici piene). Il servizio accetta quindi al massimo 1000 nodi (circa 216 MB, meno di 1 s); il limite si alzerà con la matrice a banda.
