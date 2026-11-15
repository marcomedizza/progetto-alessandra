# Rapporto di confronto del solutore — 15/11/2026

**Autrice**: Silvia (laboratorio di regressione) · sostituisce il rapporto del 14/11

**Calcolo**: telaio2d v0.4 con il convertitore v0.5; schema v1.2.

**Tolleranze**:
- valori attesi: 0,5 % relativa, minimo 1·10⁻⁶ assoluto;
- confronto completo con il riferimento: 1·10⁻⁶ relativa, per identificativo.

| Caso | Valori attesi (servizio) | Scostamenti Fortran / riferimento | Scostamenti servizio / riferimento |
|---|---|---|---|
| C1 Trave appoggiata, carico uniforme | 6 superati, 0 non superati | 0 | 0 |
| C2 Mensola, carico in punta | 5 superati, 0 non superati | 0 | 0 |
| C3 Portale incastrato, forza orizzontale | 7 superati, 0 non superati | 0 | 0 |
| C4 Portale incastrato, carico uniforme sul traverso | 6 superati, 0 non superati | 0 | 0 |
| C5 Telaio a due piani | 3 superati, 0 non superati | 0 | 0 |
| C6 Trave Gerber, carico uniforme | 9 superati, 0 non superati | 0 | 0 |
| C7 Trave appoggiata, carico concentrato fuori mezzeria | 5 superati, 0 non superati | 0 | 0 |
| C8 Trave appoggiata con molla in mezzeria | 4 superati, 0 non superati | 0 | 0 |
| C9 Portale a tre cerniere con molla al piede | 7 superati, 0 non superati | 0 | 0 |
| C10 Trave appoggiata, combinazione SLU di due casi | 3 superati, 0 non superati | 0 | 0 |
| C11 Trave continua, cedimento dell'appoggio centrale | 6 superati, 0 non superati | 0 | 0 |
| C12 Trave appoggiata, carico trapezoidale parziale | 5 superati, 0 non superati | 0 | 0 |
| C13 Trave incastrata, carico triangolare | 4 superati, 0 non superati | 0 | 0 |
| C14 Trave incastrata, distorsioni termiche | 6 superati, 0 non superati | 0 | 0 |
| C15 Asta inclinata, carico verticale parziale | 6 superati, 0 non superati | 0 | 0 |
| C16 Trave Gerber, cedimento dell'appoggio | 6 superati, 0 non superati | 0 | 0 |
| C17 Asta inclinata, carico parziale normale all'asta | 6 superati, 0 non superati | 0 | 0 |
| C18 Trave appoggiata, ΔT a farfalla | 5 superati, 0 non superati | 0 | 0 |
| C19 Trave Gerber, ΔT a farfalla sulla mensola | 6 superati, 0 non superati | 0 | 0 |
| C20 Trave Gerber, trapezio parziale sul tratto appoggiato | 6 superati, 0 non superati | 0 | 0 |
| C21 Asta inclinata, trapezio verticale e cedimento | 5 superati, 0 non superati | 0 | 0 |
| C22 Trave Gerber su molla, trapezio parziale | 5 superati, 0 non superati | 0 | 0 |
| C23 Trave incastrata, combinazione di carico triangolare e distorsione termica | 5 superati, 0 non superati | 0 | 0 |
| C24 Telaio a due piani a travi incernierate, combinazione di carichi verticali e vento | 8 superati, 0 non superati | 0 | 0 |
| C25 Portale a tre cerniere, trapezio parziale e cedimento | 8 superati, 0 non superati | 0 | 0 |
| C26 Trave continua, combinazione di carico uniforme e cedimento | 5 superati, 0 non superati | 0 | 0 |
| C27 Telaio a due piani a travi incernierate, combinazione di carichi verticali e ΔT a farfalla | 6 superati, 0 non superati | 0 | 0 |

**Novità del 15/11**
- Nessun caso nuovo: C1–C27 superati nei tre percorsi.
- **Punto 79 chiuso**: `04-FORTRAN-SOLVER/studio_area_fittizia.py` mostra che l'errore dell'area fittizia arriva a 10⁻⁵ relativo con aste incernierate agli estremi. Il limite nel README del solutore è corretto. La catena è superata anche con R = 10⁷: la scelta di R non cambia l'esito delle prove.

**Altre prove**: `test_app.py` 37 superate; `prove_modifica.mjs` 5 superate.
