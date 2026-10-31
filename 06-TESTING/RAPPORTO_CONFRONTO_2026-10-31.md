# Rapporto di confronto del solutore — 31/10/2026

**Autrice**: Silvia (laboratorio di regressione) · sostituisce il rapporto del 30/10

**Solutore**: telaio2d v0.3. Aggiunge i carichi trapezoidali e parziali (Daniela) e i cedimenti vincolari (Carla). Schema v1.1.

**Comandi**: `verifica_casi.py --fortran` e `verifica_casi.py --api`.

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

**Novità del 31/10**: C11, C12 e C13 superano i valori calcolati a mano nei tre percorsi.

**Controllo indipendente dei trapezi**: C12 e C13 sono stati ricalcolati con un modello di controllo di 60 aste, con il carico ripartito sui singoli tratti.
- Gli spostamenti nodali di questo modello sono esatti per la trave di Eulero-Bernoulli.
- La deformata disegnata dall'interfaccia coincide con essi entro 4·10⁻¹³ m, su frecce di 10,2 mm (C12) e 1,9 mm (C13).

**Altre prove**: `03-BACKEND/servizio/test_app.py`, 18 prove superate. Le 2 nuove sono:
- C11–C13 contro le formule chiuse;
- regole di coerenza della v1.1: versione dichiarata, cedimento su componente non vincolata, trapezio oltre l'asta.

**Limiti**: solo statica lineare di telai piani; distorsioni termiche non ancora gestite (v1.2). C5 resta da confrontare con un programma commerciale.
