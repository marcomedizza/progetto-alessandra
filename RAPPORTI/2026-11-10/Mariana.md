# Rapporto di Mariana — 10/11/2026

1. Difetto nuovo D22: su C13 e C23, travi doppiamente incastrate, la deformata non compariva. La scala usava solo gli spostamenti dei nodi, che lì sono nulli.
2. Correzione in `risultati.js`: la scala considera i 21 punti per asta; sotto 10⁻⁹ m la deformata non si disegna (C14, spostamenti nulli ovunque).
3. La prima versione usava `Math.max(...elenco)` e si interrompeva sul modello da 9150 aste (punto 62). Ora si usano cicli, anche per la scala dei diagrammi.
4. Modello grande: calcolo e disegno 3,1 s, modifica e annulla 1,6 s, 792 MB, nessun errore. C21 e C22 leggibili.
