# Rapporto di confronto del solutore — 04/11/2026

**Autrice**: Silvia (laboratorio di regressione) · sostituisce il rapporto del 03/11

**Solutore**: telaio2d v0.4, schema v1.2. **Comandi**: `verifica_casi.py --fortran` e `verifica_casi.py --api`.

**Tolleranze**:
- valori attesi: 0,5 % relativa, minimo 1·10⁻⁶ assoluto;
- confronto completo con il riferimento: 1·10⁻⁶ relativa, per identificativo, su spostamenti, reazioni, rotazioni d'estremità e N, V, M.

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

**Novità del 04/11**
- **C19, cerniera interna e ΔT a farfalla (punto 41)**: la condensazione della cerniera tratta le forze d'incastro termiche. Cerniera +3,20 mm, rotazioni +1,60 e −1,60 mrad, nessuna sollecitazione.
- **Banda contro matrice piena su tutti i casi** (`prova_prestazioni.py --casi`): scarto ≤ 1,2·10⁻¹⁶ m, tranne C3 (deformabilità assiale trascurata, 1,2·10⁻¹⁰ m) e C9 (9·10⁻¹⁵ m).

**Altre prove**: `03-BACKEND/servizio/test_app.py`, 24 prove superate. Le 2 nuove sono C19 e le distorsioni termiche come le crea il pannello, con il rifiuto quando manca α.
