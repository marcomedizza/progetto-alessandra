# Rapporto di Alessandra — 30/10/2026, per la revisione di Marco

**Catena verificata alle 08:10**: 
- solutore v0.2 compilato;
- C1–C10 superati nei tre percorsi (riferimento, Fortran, servizio), con zero scostamenti anche sulle rotazioni d'estremità;
- 16 prove del servizio superate;
- scenari S1–S19 superati in Chromium.

**Difetti e punti aperti di ieri**

| Punto | Esito del 30/10 |
|---|---|
| D8 deformata con cerniere | chiuso: rotazioni alla cerniera di C6 uguali alle formule chiuse (−10,64 e +15,01 mrad); deformata esatta |
| D10 disegno col mouse | chiuso in versione minima: spezzata con aggancio alla griglia; aperti D12 (reinquadratura) e D13 (annulla) |
| Rev. 14 materiali e sezioni | chiuso: E, A, I modificabili, copia per una sola asta |
| Rev. 6 matrice piena | chiuso: Cholesky a banda. 14 043 gdl in 0,26 s. Riordino di Cuthill-McKee contro le bande larghe dei modelli disegnati a mano |

**Da chiedere a Marco**:
1. controllare i valori attesi di C6–C10: i passaggi a mano sono in `06-TESTING/casi/README.md`;
2. provare l'interfaccia in Firefox, scenari S1–S19 di `06-TESTING/flusso.md`;
3. esportare da ModeSt il portale C4 (`05-RICERCA/modest.md`).

**Non svolto dal team tech**: nessuna consegna mancante. C11 (cedimento) è pronto a mano, ma il solutore non calcola ancora i cedimenti.
