# Rapporto di Natalia — 13/11/2026

Prove con dati errati inviati a `/api/calcola`:

| Dato | Prima | Dopo |
|---|---|---|
| JSON malformato, corpo vuoto, lista | 422 | 422 |
| campo mancante, E negativo, A nulla, testo al posto di numero, nessun caso, punti_diagramma fuori intervallo | 422 dallo schema | 422 |
| caso inesistente | 422 | 422 |
| coordinata NaN o infinita | **500** | 422 «valore non finito» |
| nodi distinti con le stesse coordinate | **500** (divisione per zero) | 422 «lunghezza nulla» |
| carico 10³⁰⁰ kN/m | **500** (uscita Fortran illeggibile) | 200, risultati finiti |
| coordinata 10³⁰⁸ m | 422 con un avviso interno di gfortran nel testo | 422 «struttura labile», messaggio poco chiaro (punto 76) |

Prove nuove: `test_dati_errati`, `test_esponente_a_tre_cifre`. Le prove del servizio sono ora 35, tutte superate.
