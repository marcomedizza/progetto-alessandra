# Rapporto di confronto del solutore — 28/10/2026

**Autrice**: Silvia (laboratorio di regressione) · sostituisce il rapporto del 27/10

**Comandi**: `verifica_casi.py --fortran` (convertitore → Fortran) e `verifica_casi.py --api` (POST al servizio FastAPI → convertitore → Fortran).

**Tolleranze**: valori attesi da formule chiuse 0,5 % relativa (minimo 1·10⁻⁶ assoluto); confronto completo con il risolutore di riferimento Python 1·10⁻⁶ relativa su ogni spostamento, reazione e valore di N, V, M, abbinati per identificativo di nodo e asta.

| Caso | Controlli sui valori attesi (servizio) | Scostamenti servizio / riferimento |
|---|---|---|
| C1 Trave appoggiata, carico uniforme | 6 superati, 0 non superati | 0 |
| C2 Mensola, carico in punta | 5 superati, 0 non superati | 0 |
| C3 Portale incastrato, forza orizzontale | 7 superati, 0 non superati | 0 |
| C4 Portale incastrato, carico uniforme sul traverso | 6 superati, 0 non superati | 0 |
| C5 Telaio a due piani | 3 superati, 0 non superati | 0 |
| C6 Trave Gerber, carico uniforme | 6 superati, 0 non superati | 0 |
| C7 Trave appoggiata, carico concentrato fuori mezzeria | 5 superati, 0 non superati | 0 |
| C8 Trave appoggiata con molla in mezzeria | 4 superati, 0 non superati | 0 |
| C9 Portale a tre cerniere con molla al piede | 7 superati, 0 non superati | 0 |

**Esito**: C1–C9 superati in entrambi i percorsi. Le combinazioni sono verificate in `03-BACKEND/servizio/test_app.py` (sovrapposizione esatta, scarto < 1·10⁻⁹).

**Correzione del 28/10**: il confronto completo abbinava i risultati per posizione e segnalava falsi scostamenti su C9, dove i nodi non sono numerati in ordine. Ora l'abbinamento è per identificativo.

**Limiti**: solo statica lineare di telai piani. C5 resta da confrontare con un programma commerciale.
