# Rapporto di confronto del solutore — 30/10/2026

**Autrice**: Silvia (laboratorio di regressione) · sostituisce il rapporto del 29/10

**Solutore**: telaio2d v0.2, con Cholesky a matrice a banda e rotazioni d'estremità delle aste (D8).

**Comandi**: `verifica_casi.py --fortran` e `verifica_casi.py --api`.

**Tolleranze**:
- valori attesi: 0,5 % relativa, minimo 1·10⁻⁶ assoluto;
- confronto completo con il riferimento: 1·10⁻⁶ relativa, per identificativo di nodo e asta, sugli spostamenti, sulle reazioni, sulle rotazioni d'estremità (nuove) e su N, V, M.

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

**Novità del 30/10**
- **C6, tre controlli nuovi sulla struttura con cerniera (D8)**: abbassamento della cerniera, rotazione della mensola alla cerniera e rotazione del tratto appoggiato. Coincidono con le formule chiuse: −30,39 mm, −10,64 mrad, +15,01 mrad.
- **C9**: anche la seconda struttura con cerniera è confrontata sulle rotazioni d'estremità.
- **Matrice a banda**: `04-FORTRAN-SOLVER/prova_prestazioni.py` confronta banda e matrice piena fino a 1989 gradi di libertà. Lo scarto relativo massimo sugli spostamenti è 2,4·10⁻¹², cioè arrotondamento numerico. Telai fino a 14 043 gradi di libertà sono stati risolti con la sola banda, con equilibrio verticale esatto.

**Altre prove**: `03-BACKEND/servizio/test_app.py`, 16 prove superate. Le 4 nuove sono:
- rotazioni alla cerniera di C6 contro la formula chiusa;
- sezione e materiale inseriti dall'interfaccia, con la freccia di C1 confrontata con la formula e il rifiuto di I = 0;
- modello grande (2121 nodi, 4100 aste) con equilibrio verticale;
- nodi in ordine casuale (4681 nodi): con il riordino di Cuthill-McKee il calcolo riesce e i risultati tornano nell'ordine del modello; senza riordino il solutore segnala «semibanda troppo grande».

**Limiti**: solo statica lineare di telai piani. C5 resta da confrontare con un programma commerciale. C11 (cedimento vincolare) è preparato a mano ma non è calcolabile finché il solutore non gestisce i cedimenti.
