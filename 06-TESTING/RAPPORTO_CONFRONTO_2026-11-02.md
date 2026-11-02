# Rapporto di confronto del solutore — 02/11/2026

**Autrice**: Silvia (laboratorio di regressione) · sostituisce il rapporto del 31/10

**Solutore**: telaio2d v0.3, schema v1.1. **Comandi**: `verifica_casi.py --fortran` e `verifica_casi.py --api`.

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
| C15 Asta inclinata, carico verticale parziale | 6 superati, 0 non superati | 0 | 0 |
| C16 Trave Gerber, cedimento dell'appoggio | 6 superati, 0 non superati | 0 | 0 |

**Novità del 02/11**
- **C15, carico parziale su asta inclinata**: controlla le componenti locali del carico verticale, cioè la trasversale nel momento e l'assiale nello sforzo normale.
- **C16, struttura con cerniera e cedimento**: controlla che un cedimento su struttura isostatica non produca sollecitazioni e che il tratto oltre la cerniera ruoti rigidamente.
- **Modello grande a banda con cedimenti**: telaio di 6363 gdl con reazioni autoequilibrate; prova del servizio `test_modello_grande_con_cedimenti`.

**Altre prove**: `03-BACKEND/servizio/test_app.py`, 20 prove superate. Le 2 nuove sono il modello grande con cedimenti e il rifiuto del cedimento su una molla.

**Numerazione**: C14 resta riservato alle distorsioni termiche (schema v1.2), non ancora iniziate.
