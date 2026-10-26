# Convertitore JSON ↔ solutore Fortran (Paola)

`converti.py` legge un modello conforme a `01-ARCHITETTURA/DATA_SCHEMA.json`, scrive il file di ingresso del solutore, lo esegue e restituisce il blocco `risultati` dello schema (spostamenti, reazioni, N-V-M lungo le aste).

    python3 converti.py ../../06-TESTING/casi/C4_portale_carico_uniforme.json

Il solutore si compila con `04-FORTRAN-SOLVER/build.sh`; il percorso si può cambiare con la variabile `TELAIO2D_BIN`.
