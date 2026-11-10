# Rapporto di confronto del solutore — 09/11/2026

**Autrice**: Silvia (laboratorio di regressione) · sostituisce il rapporto dell'08/11

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

**Novità del 09/11**
- **C22**, trave Gerber su molla con trapezio parziale: reazioni come in C20, molla abbassata di R3/ky = 7,5 mm, cerniera −9,12 mm.
- **Identificativi non consecutivi** (prova del servizio): estesa a C20 e C21, con carichi d'asta e cedimenti rinumerati.

**Altre prove**: `test_app.py` 30 superate (nuova: validatori discordi, punto 58); `prove_modifica.mjs` 5 superate.
