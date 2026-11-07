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

**Banda contro matrice piena con cedimenti e distorsioni** (Carla, Ottavia, 04/11): `prova_prestazioni.py --v04` aggiunge ai telai regolari un cedimento di 10 mm di un piede e ΔT = +20 °C uniforme e +10 °C a farfalla sulle travi.

| Telaio | gdl | Banda | Piena | Scarto |
|---|---|---|---|---|
| 10 × 40 | 1353 | 0,026 s | 0,088 s | 5·10⁻¹⁴ |
| 12 × 50 | 1989 | 0,027 s | 0,200 s | 2·10⁻¹² |
| 20 × 100 | 6363 | 0,232 s | — | — |
| 30 × 150 | 14 043 | 0,598 s | — | — |

Le reazioni verticali equilibrano sempre il carico: cedimento e distorsioni producono reazioni autoequilibrate. I tempi sono dello stesso ordine della prova senza cedimenti; le differenze rientrano nella variabilità della macchina.

**Tutti i casi di prova con banda e con matrice piena** (Elisa, 04/11, `prova_prestazioni.py --casi`): scarto massimo sugli spostamenti ≤ 1,2·10⁻¹⁶ m in tutti i casi tranne due.
- C3: scarto 1,2·10⁻¹⁰ m. È l'unico caso con deformabilità assiale trascurata (A × 10⁶): la matrice è mal condizionata e i due metodi differiscono di circa 10⁻⁸ in termini relativi, sotto la tolleranza delle verifiche.
- C9: scarto 9·10⁻¹⁵ m.

In particolare C6 (cerniera) dà 1,2·10⁻¹⁶ m e C8 (molla) 5·10⁻¹⁸ m.

**Deformabilità assiale trascurata (punto 46, Carla ed Elisa, 06/11)**: oggi si ottiene moltiplicando l'area per 10⁶. Ho studiato il fattore su C3 confrontando il momento al piede con la soluzione chiusa ad assiale rigida (21,9894 kNm) e i due metodi di soluzione tra loro.

| Fattore su A | Errore sul momento | Banda contro piena (relativo) |
|---|---|---|
| 1 (assiale deformabile) | 3·10⁻³ | 4·10⁻¹⁹ |
| 10² | 3·10⁻⁵ | 2·10⁻¹² |
| 10⁴ | 3·10⁻⁷ | 1·10⁻¹⁰ |
| 10⁶ (in uso) | 6·10⁻⁹ | 1·10⁻⁸ |
| 10⁸ | 3·10⁻⁶ | 2·10⁻⁶ |
| 10¹⁰ | — | matrice dichiarata singolare |

L'errore di modello scende come 1/fattore; l'arrotondamento cresce con il fattore e oltre 10⁸ prevale. Il fattore 10⁶ è vicino all'ottimo per la doppia precisione, con errore 10⁻⁸: sei ordini sotto qualunque tolleranza di progetto.

**Proposta**: mantenere la penalità e non introdurre ora vincoli esatti di inestensibilità. Questi richiederebbero l'eliminazione di gradi di libertà dipendenti con il riconoscimento dei vincoli ridondanti nei telai a più campate: lavoro e rischio non giustificati da un guadagno di precisione di 10⁻⁸. Per robustezza conviene invece rendere il fattore relativo all'asta, cioè EA/L pari a circa 10⁶ volte la rigidezza flessionale 12EI/L³, così il condizionamento non dipende dalle dimensioni. Da fare nella v0.5, con nuova verifica di C3, C4 e del telaio di prova; la versione sperimentale senza A × 10⁶ non è stata scritta, per i motivi detti.

**v0.5 (07/11, Carla, Elisa, Paola): fattore relativo all'asta.** Con deformabilità assiale trascurata l'area di calcolo è ora max(A, 10⁸·12I/L²): la rigidezza assiale di ogni asta vale 10⁸ volte quella flessionale. La regola è nel convertitore (`area_di_calcolo`) e nel risolutore di riferimento; il solutore Fortran non cambia.

Verifica su C3 al variare delle luci, con la forza orizzontale fissa. Errore relativo sul momento al piede rispetto alla soluzione chiusa ad assiale rigida:

| Luci × | A × 10⁶ (fino al 06/11) | Fattore relativo (v0.5) |
|---|---|---|
| 0,05 | 1,2·10⁻⁶ | 1,0·10⁻⁸ |
| 0,25 | 4,9·10⁻⁸ | 2,4·10⁻⁹ |
| 1 | 6,2·10⁻⁹ | 2,4·10⁻⁹ |
| 5 | 3,0·10⁻⁷ | 7,2·10⁻⁹ |
| 25 | 8,9·10⁻⁶ | 6,9·10⁻⁹ |

Con il fattore fisso l'errore dipende dalle dimensioni: per aste corte prevale l'errore di modello, per aste lunghe l'arrotondamento. Con il fattore relativo resta tra 2·10⁻⁹ e 1·10⁻⁸. C1–C20 restano superati nei tre percorsi; banda contro piena su C3 6,8·10⁻⁹ e su C4 2,8·10⁻⁹. Il punto 46 è chiuso.

**Build dopo la v0.5** (Ottavia, 07/11): la v0.5 cambia solo il convertitore. `build.sh` ricompila il solutore v0.4 senza avvisi nuovi, e C1–C20 e le prestazioni restano invariati.

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
