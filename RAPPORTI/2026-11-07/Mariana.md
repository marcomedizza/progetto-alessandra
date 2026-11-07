# Rapporto di Mariana — 07/11/2026

- **C20**: leggibile; etichette 30 e 6,1 kNm, freccia della cerniera −9,12 mm.
- **Modello grande (4681 nodi, 9150 aste)** caricato da file nel navigatore. La prima misura era di 12,7 s per calcolo e disegno, con 1,2 GB di memoria. Ho trovato tre cause, con Irene:
  1. la mappa dei nodi ricostruita per ogni asta (43 milioni di inserimenti);
  2. una geometria e un materiale per ogni asta e ogni nodo;
  3. circa 25 000 etichette riposizionate a ogni fotogramma.

  Dopo le correzioni: 4,7 s e 0,79 GB.
- **Controllo a vista**: su C5 le frecce dei carichi erano 25 volte troppo lunghe (D20). Corretto e ricontrollato.
