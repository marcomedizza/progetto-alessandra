# Rapporto di confronto del solutore — 21/11/2026

**Autrice**: Silvia (laboratorio di regressione) · sostituisce il rapporto del 20/11

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
| C28 Portale asimmetrico a tre cerniere, carichi misti | 8 superati, 0 non superati | 0 | 0 |
| C29 Telaio a due piani a travi incernierate, trapezio e cedimento | 7 superati, 0 non superati | 0 | 0 |
| C30 Telaio a tre piani a travi incernierate, carichi misti combinati | 8 superati, 0 non superati | 0 | 0 |
| C31 Telaio a tre piani a travi incernierate, carichi misti e ΔT | 5 superati, 0 non superati | 0 | 0 |
| C32 Telaio a tre piani a travi incernierate, carichi misti, ΔT e vento | 6 superati, 0 non superati | 0 | 0 |

**Novità del 21/11**
- **Punto 79, vento sbloccato**: R = 10⁶ per le aste incernierate. Fortran e riferimento concordano di nuovo sul telaio a travi incernierate con vento, con differenza massima da 6·10⁻⁵ a 3·10⁻⁷ kN. Il riferimento di C24 è rigenerato, con variazioni sotto 10⁻⁵ kN.
- **C32**: C31 con il vento, soluzione esatta, uguale nei tre percorsi.

**Altre prove**: `test_app.py` 40 superate (tolleranza di `test_combinazione_due_piani` motivata, punto 99); `esegui_scenari.py` 16 script.
