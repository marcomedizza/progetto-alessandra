# Rapporto di Irene — 12/11/2026

1. D23: in `risultati.js` le etichette d'estremità si spostano verso l'interno dell'asta di min(12 % di L; 4 % del modello).
2. Se un'etichetta cade su un'altra già posta, scorre lungo la propria asta, al più 4 passi.
3. Controllo a vista:
   - C24: freccia del primo piano libera;
   - C5: le tre etichette del nodo 3 sono separate;
   - C25: corretto.
4. Modello grande: tempi invariati, nessun errore.
5. Limiti, revisione 70–71: le dimensioni delle etichette sono stimate e non misurate; un'etichetta spostata può essere letta come valore del punto in cui si trova.

**Non fatto**: D12 e Firefox, che si provano solo a mano.
