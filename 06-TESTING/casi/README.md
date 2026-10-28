# Casi di prova con soluzione nota

**Data**: 26/10/2026 (C1–C5), 27/10/2026 (C6–C8), 28/10/2026 (C9) · **Schema**: `01-ARCHITETTURA/DATA_SCHEMA.json` v1.0
**Da controllare**: Marco (i valori attesi sono la base di verifica del solutore Fortran)

| Caso | Modello | Verifica | Valori attesi principali |
|---|---|---|---|
| C1 | Trave appoggiata IPE 300, L = 6 m, q = 10 kN/m | formule chiuse | R = 30 kN; M = qL²/8 = 45,00 kNm; f = 5qL⁴/384EI = 9,617 mm |
| C2 | Mensola HE 200 A, L = 3 m, P = 10 kN in punta | formule chiuse | M incastro = −30,00 kNm; f = PL³/3EI = 11,608 mm |
| C3 | Portale incastrato, h = 4 m, L = 6 m, H = 20 kN | formule chiuse, k = (Ib/L)/(Ic/h) = 1,509 | M piede = 21,99 kNm; M testa = 18,01 kNm; Rx = −10 kN per colonna |
| C4 | Stesso portale, q = 30 kN/m sul traverso | metodo delle rotazioni | M angolo = 51,30 kNm; M mezzeria = 83,70 kNm; M piede = 25,65 kNm; spinta = 19,24 kN |
| C5 | Telaio a due piani, una campata, q = 25 kN/m, H = 10 + 15 kN | equilibrio globale + valori numerici | ΣRy = 300 kN; ΣRx = −25 kN; momento risultante nullo |
| C6 | Trave Gerber IPE 300: incastro, cerniera interna a 4 m, appoggio a 6 m, q = 10 kN/m | statica (isostatica) | R1 = 50 kN; M incastro = −120,0 kNm; M cerniera = 0; M tratto appoggiato = 5,00 kNm; R3 = 10 kN |
| C7 | Trave appoggiata IPE 300, L = 6 m, P = 20 kN a 2 m | formule chiuse | R1 = 13,33 kN; R2 = 6,67 kN; M = Pab/L = 26,67 kNm |
| C8 | Trave appoggiata IPE 300, L = 6 m, q = 10 kN/m, molla ky = 1000 kN/m in mezzeria | congruenza | forza nella molla = 7,654 kN; freccia = 7,65 mm; M mezzeria = 33,52 kNm |
| C9 | Portale a tre cerniere (cerniera in mezzeria del traverso), piede destro su molla verticale ky = 5000 kN/m, H = 20 kN | statica (isostatica) + molla | Ry4 = 13,33 kN; Rx1 = Rx4 = −10 kN; M testa colonna = 40,00 kNm; abbassamento della molla = 2,67 mm |

Materiale: acciaio, E = 210 000 MPa = 2,10·10⁸ kN/m². Profili: IPE 300 (A = 53,81 cm², I = 8356 cm⁴), HE 200 A (A = 53,83 cm², I = 3692 cm⁴), valori da sagomario da ricontrollare sulla tabella del produttore.

C3 e C4 trascurano la deformabilità assiale (`deformabilita_assiale: false`), come le formule usate. Con aste assialmente deformabili il momento al piede di C3 diventa 22,06 e 21,95 kNm, con differenze dello 0,3 % e asimmetria dovuta all'accorciamento delle colonne.

C5 non ha una soluzione chiusa semplice per la ripartizione interna. I valori in `C5_telaio_due_piani.riferimento.json` sono del risolutore di riferimento e vanno confermati con un programma commerciale (ModeSt).

## File

- `C*.json`: modelli di input
- `C*.atteso.json`: valori attesi con le formule usate
- `C*.riferimento.json`: risultati completi del risolutore di riferimento (spostamenti, reazioni, N-V-M)
- `genera_casi.py`: rigenera modelli e valori attesi
- `verifica_casi.py`: valida i modelli con lo schema, li risolve e confronta con gli attesi (tolleranza 0,5 %); `--fortran` usa il solutore Fortran, `--api` il percorso completo attraverso il servizio FastAPI
- `../riferimento/telaio2d.py`: risolutore di riferimento in Python, senza dipendenze

## Come si usa per il solutore Fortran

Silvia sostituisce in `verifica_casi.py` la funzione `risultati(modello, caso)` con la chiamata al solutore Fortran tramite il convertitore di Paola. Il solutore è accettato quando tutti i controlli passano.
