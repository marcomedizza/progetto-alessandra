# Solutore Fortran telaio2d — v0.4 (03/11/2026)

Telai piani, statica lineare, metodo degli spostamenti (Elisa, compilazione Ottavia).

- Sorgente: `src/telaio2d.f90` (Fortran 2008, nessuna libreria esterna)
- Compilazione: `./build.sh` (richiede gfortran) → `bin/telaio2d`
- Uso: `bin/telaio2d input.txt output.txt [piena]`; il formato dei file è descritto in testa al sorgente. L'opzione `piena` usa la matrice piena della v0.1, per confronto
- Uscita `ROTAZIONI_ASTE` (30/10, difetto D8): rotazioni delle due estremità di ogni asta. Alla cerniera interna sono ricavate dall'asta non condensata, imponendo il momento d'estremità nullo
- Chiamata da Python: `esegui.py` (Ottavia), con tempo massimo di calcolo e messaggi d'errore puliti
- Ingresso e uscita sono gestiti dal convertitore `03-BACKEND/converter/converti.py`
- Controlli in lettura (28/10): carichi su aste inesistenti, identificativi duplicati di nodi e aste

Gestisce: aste inclinate, cerniere interne, vincoli e molle, carichi nodali, carichi d'asta uniformi e concentrati, peso proprio (tramite convertitore), deformabilità assiale escludibile.

**Verifica (26/10/2026)**: `python3 06-TESTING/casi/verifica_casi.py --fortran` supera tutti i controlli sui casi C1–C5. Il confronto completo con il risolutore di riferimento Python dà zero scostamenti, anche su un caso misto con cerniera, molla, asta inclinata e peso proprio.

**v0.3 (31/10)**:
- carichi distribuiti lineari su un tratto dell'asta (tipo 3: parziali, trapezoidali, triangolari; Daniela), con forze d'incastro integrate con Gauss a 3 punti, esatto;
- sezione facoltativa `CEDIMENTI` (Carla): spostamenti impressi ai gradi di libertà vincolati, portati a secondo membro per asta. Un cedimento su un grado di libertà non vincolato è un errore.

**Cedimento su una molla** (punto 28 della revisione): non è ammesso. Il grado di libertà con molla resta un'incognita del sistema, il cui spostamento dipende dalla rigidezza della molla. Imporne il valore annullerebbe il significato della molla. Un cedimento noto va dato su un vincolo rigido; un terreno cedevole si rappresenta con la molla e i carichi. Il servizio respinge il modello con il messaggio «il nodo non ha uy vincolato» e il solutore con «cedimento su un grado di libertà non vincolato».

**Modello grande con cedimenti** (Carla, 02/11): telaio 20 × 100 (6363 gdl), cedimento di 10 mm di un piede, nessun carico. Le reazioni risultano autoequilibrate: somme delle forze e momento risultante nulli entro 10⁻⁵. Prova `test_modello_grande_con_cedimenti`.

I file della v0.2 restano validi. Verifica sui casi C11–C13 con soluzione a mano.

**v0.4 (03/11, Elisa e Paola)**: distorsioni termiche, carico di tipo 4 `asta 4 NT MT 0`. Il convertitore calcola NT = E·A·α·ΔTu e MT = E·I·α·ΔTg/h; il solutore li applica come forze d'incastro: f1 = +NT, f4 = −NT, f3 = +MT, f6 = −MT. Verifica: C14 (trave incastrata) e C18 (trave appoggiata) contro le formule chiuse. Il costo della soluzione non cambia, perché agisce solo sul secondo membro.

**Prossimi passi** vincolari (C11), P-Delta. Le combinazioni sono calcolate dal servizio per sovrapposizione.

## Prestazioni (Ottavia, 29/10/2026)

`python3 04-FORTRAN-SOLVER/prova_prestazioni.py` — telai regolari, campate da 6 m, piani da 3,5 m, matrice piena:

| Telaio | Nodi | Aste | Gradi di libertà | Tempo |
|---|---|---|---|---|
| 1 × 10 | 22 | 30 | 66 | 0,005 s |
| 5 × 20 | 126 | 220 | 378 | 0,012 s |
| 10 × 40 | 451 | 840 | 1353 | 0,11 s |
| 12 × 50 | 663 | 1250 | 1989 | 0,23 s |

In tutti i casi la somma delle reazioni verticali coincide con il carico applicato. Il tempo cresce circa con il cubo dei gradi di libertà e la memoria con il quadrato (tre matrici piene). Il servizio accetta quindi al massimo 1000 nodi (circa 216 MB, meno di 1 s); il limite si alzerà con la matrice a banda.

## Matrice a banda (Elisa, Ottavia, 30/10/2026)

Il sistema K·u = F sui soli gradi di libertà liberi si risolve con la fattorizzazione di Cholesky in forma a banda: K = Uᵀ·U, con memoria n·(b+1) e tempo proporzionale a n·b², dove b è la semibanda. La semibanda dipende dalla numerazione dei nodi: con la numerazione per piani dei telai regolari vale circa 3·(campate + 2). Il convertitore scrive i nodi nell'ordine di Cuthill-McKee inverso, quindi la semibanda resta piccola anche per modelli disegnati a mano: su un telaio 20 × 100 con nodi mescolati passa da 6203 a 71. Se un file scritto a mano richiede più di 5·10⁷ termini di banda (400 MB), il solutore si ferma con il messaggio «semibanda troppo grande». Un pivot non positivo, o minore di 10⁻¹² volte il massimo termine diagonale, segnala una struttura labile con lo stesso messaggio della v0.1. Le reazioni si ricavano sommando ai nodi le forze d'estremità delle aste, così non serve conservare la matrice completa.

| Telaio | Nodi | Aste | Gradi di libertà | Banda | Matrice piena | Scarto relativo |
|---|---|---|---|---|---|---|
| 1 × 10 | 22 | 30 | 66 | 0,004 s | 0,004 s | 5·10⁻¹⁴ |
| 5 × 20 | 126 | 220 | 378 | 0,006 s | 0,007 s | 2·10⁻¹³ |
| 10 × 40 | 451 | 840 | 1353 | 0,012 s | 0,125 s | 2·10⁻¹² |
| 12 × 50 | 663 | 1250 | 1989 | 0,029 s | 0,350 s | 6·10⁻¹³ |
| 20 × 100 | 2121 | 4100 | 6363 | 0,106 s | — | — |
| 30 × 150 | 4681 | 9150 | 14 043 | 0,260 s | — | — |

**Ripetizione con la v0.3** (Elisa, Ottavia, 02/11), nell'ordine dei nodi di Cuthill-McKee:

| Telaio | gdl | Banda | Piena | Scarto |
|---|---|---|---|---|
| 10 × 40 | 1353 | 0,019 s | 0,080 s | 5·10⁻¹⁴ |
| 12 × 50 | 1989 | 0,020 s | 0,183 s | 2·10⁻¹² |
| 20 × 100 | 6363 | 0,103 s | — | — |
| 30 × 150 | 14 043 | 0,458 s | — | — |

L'equilibrio verticale è esatto in tutti i casi. I tempi variano di un fattore fino a 2 da un'esecuzione all'altra, per il carico della macchina di prova. La v0.3 non cambia il costo della soluzione: trapezi e cedimenti agiscono solo sul secondo membro.

Lo scarto relativo è quello tra gli spostamenti dei due metodi. In tutti i casi la somma delle reazioni verticali coincide con il carico. Il percorso completo del servizio (convertitore compreso) sul telaio 30 × 150 richiede 0,5 s e produce 3,4 MB di risultati. Il servizio accetta ora fino a 5000 nodi e 10 000 aste. Il limite pratico diventa la vista 3D del navigatore, non provata oltre qualche centinaio di aste.
