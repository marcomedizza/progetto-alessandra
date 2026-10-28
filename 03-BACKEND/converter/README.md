# Convertitore JSON ↔ solutore Fortran (Paola)

`converti.py` legge un modello conforme a `01-ARCHITETTURA/DATA_SCHEMA.json`, scrive il file di ingresso del solutore, lo esegue e restituisce il blocco `risultati` dello schema (spostamenti, reazioni, N-V-M lungo le aste).

    python3 converti.py ../../06-TESTING/casi/C4_portale_carico_uniforme.json

Il solutore si compila con `04-FORTRAN-SOLVER/build.sh`; il percorso si può cambiare con la variabile `TELAIO2D_BIN`.

## Interfaccia con il servizio (concordata con Natalia, 28/10/2026)

- `risultati(modello, caso)` → blocco `risultati` dello schema per un caso di carico
- `combina(modello, combinazione)` → risultati di una combinazione per sovrapposizione lineare
- La chiamata al solutore è nel modulo di Ottavia `04-FORTRAN-SOLVER/esegui.py`

## Campi in dubbio

- **Ordine dei risultati**: spostamenti e reazioni escono nell'ordine dei nodi del modello. Vanno letti per identificativo, non per posizione.
- **Peso proprio**: è convertito in carico uniforme verticale γ·A per unità di lunghezza dell'asta; sulle aste inclinate agisce sulla lunghezza reale, non sulla proiezione orizzontale.
- **Carico concentrato all'estremità di un'asta**: è accettato (a = 0 o a = L) ma è preferibile applicarlo come carico nodale.
- **Deformabilità assiale trascurata**: ottenuta moltiplicando l'area per 10⁶ (vedi revisione di Marisa, punto 8).
