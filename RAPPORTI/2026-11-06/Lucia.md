# Rapporto di Lucia — 06/11/2026

**Punto 34, memoria dell'Annulla**: un modello da 4681 nodi occupa 1,37 milioni di caratteri per copia; 50 copie sarebbero circa 140 MB in memoria. Ho introdotto un limite di 20 milioni di caratteri in tutto, circa 40 MB: su quel modello restano circa 14 annullamenti, sui modelli piccoli 50. Si conservano sempre le ultime due copie.

**Alternativa valutata**: memorizzare solo le differenze. Non adottata ora: è più complessa e soggetta a errori, e il limite basta ai modelli attuali.
