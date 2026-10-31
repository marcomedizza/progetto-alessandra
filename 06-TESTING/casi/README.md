# Casi di prova con soluzione nota

**Data**: 26/10/2026 (C1–C5), 27/10/2026 (C6–C8), 28/10/2026 (C9), 29/10/2026 (C10), 31/10/2026 (C11–C13) · **Schema**: `01-ARCHITETTURA/DATA_SCHEMA.json` v1.0; C11–C13 v1.1
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
| C10 | Trave appoggiata IPE 300, L = 6 m: G2 q = 10 kN/m, Q P = 20 kN a 2 m; combinazione SLU 1,3·G2 + 1,5·Q | formule chiuse + sovrapposizione | R1 = 59 kN; R2 = 49 kN; M sotto il carico = 92 kNm |
| C11 | Trave continua su tre appoggi (2 × 6 m), cedimento dell'appoggio centrale δ = 10 mm (v1.1) | formule chiuse | RB = −4,874 kN; RA = RC = 2,437 kN; MB = 14,62 kNm; φA = −2,50 mrad |
| C12 | Trave appoggiata L = 6 m, trapezio da 10 kN/m in x = 1 m a 20 kN/m in x = 4 m (v1.1) | statica | R1 = 25 kN; R2 = 20 kN; M(1) = 25,00; M(3) = 50,56; M(4) = 40,00 kNm |
| C13 | Trave incastrata L = 6 m, carico triangolare da 0 a 20 kN/m (v1.1) | formule chiuse | RA = 3qL/20 = 18 kN; RB = 7qL/20 = 42 kN; MA = −qL²/30 = −24; MB = −qL²/20 = −36 kNm |
| C9 | Portale a tre cerniere (cerniera in mezzeria del traverso), piede destro su molla verticale ky = 5000 kN/m, H = 20 kN | statica (isostatica) + molla | Ry4 = 13,33 kN; Rx1 = Rx4 = −10 kN; M testa colonna = 40,00 kNm; abbassamento della molla = 2,67 mm |

Materiale: acciaio, E = 210 000 MPa = 2,10·10⁸ kN/m². Profili: IPE 300 (A = 53,81 cm², I = 8356 cm⁴), HE 200 A (A = 53,83 cm², I = 3692 cm⁴), valori da sagomario da ricontrollare sulla tabella del produttore.

C3 e C4 trascurano la deformabilità assiale (`deformabilita_assiale: false`), come le formule usate. Con aste assialmente deformabili il momento al piede di C3 diventa 22,06 e 21,95 kNm, con differenze dello 0,3 % e asimmetria dovuta all'accorciamento delle colonne.

C5 non ha una soluzione chiusa semplice per la ripartizione interna. I valori in `C5_telaio_due_piani.riferimento.json` sono del risolutore di riferimento e vanno confermati con un programma commerciale (ModeSt).

## Valori da controllare per la revisione di Marco (Valentina, 30/10/2026)

Passaggi a mano dei casi C6–C10. EI dell'IPE 300 = 2,1·10⁸ × 8356·10⁻⁸ = 17 547,6 kNm².

**C6 · trave Gerber** (incastro in 0, cerniera interna in 4 m, appoggio in 6 m, q = 10 kN/m)
1. Tratto appoggiato 4–6, isostatico: R3 = q·2/2 = 10 kN; forza trasmessa alla cerniera Rs = 10 kN; M in x = 5 = q·2²/8 = 5,00 kNm.
2. Mensola 0–4 con q e Rs in punta: R1 = 10·4 + 10 = 50 kN; M incastro = −(10·4²/2 + 10·4) = −120,0 kNm.
3. Spostamenti (aggiunti il 30/10 per D8):
   - abbassamento della cerniera v2 = q·4⁴/(8EI) + Rs·4³/(3EI) = 533,33/EI = 30,39 mm;
   - rotazione della mensola alla cerniera = −(q·4³/(6EI) + Rs·4²/(2EI)) = −186,67/EI = −10,64 mrad;
   - rotazione del tratto appoggiato alla cerniera = v2/2 − q·2³/(24EI) = 15,01 mrad.

**C7 · trave appoggiata, P = 20 kN a 2 m** (L = 6 m)
R1 = P·b/L = 20·4/6 = 13,33 kN; R2 = 20·2/6 = 6,67 kN; M sotto il carico = P·a·b/L = 20·2·4/6 = 26,67 kNm.

**C8 · trave appoggiata con molla in mezzeria** (q = 10 kN/m, ky = 1000 kN/m)
1. Freccia senza molla: δ0 = 5qL⁴/(384EI) = 9,617 mm.
2. Cedevolezza della trave in mezzeria: f = L³/(48EI) = 0,2565 mm/kN.
3. Congruenza: X·(f + 1/ky) = δ0, quindi X = 9,617/(0,2565 + 1,000) = 7,654 kN; freccia = X/ky = 7,65 mm.
4. M in mezzeria = qL²/8 − X·L/4 = 45,00 − 11,48 = 33,52 kNm.

**C9 · portale a tre cerniere, molla verticale al piede destro** (h = 4 m, L = 6 m, H = 20 kN in testa)
1. Equilibrio alla rotazione attorno al piede sinistro: Ry4 = H·h/L = 20·4/6 = 13,33 kN; Ry1 = −13,33 kN.
2. Cerniera in mezzeria del traverso: il momento delle forze di destra attorno a essa è nullo, quindi Rx4·h = −Ry4·L/2, cioè Rx4 = −10 kN; Rx1 = −20 + 10 = −10 kN.
3. M in testa alla colonna = |Rx|·h = 40,00 kNm; abbassamento della molla = 13,33/5000 = 2,67 mm.

La molla non cambia le reazioni, perché la struttura resta isostatica.

**C10 · combinazione SLU su trave appoggiata** (G2: q = 10 kN/m; Q: P = 20 kN a 2 m; 1,3·G2 + 1,5·Q)
- G2: R1 = R2 = 30 kN; M in x = 2 = q·x·(L − x)/2 = 40 kNm.
- Q: R1 = 13,33 kN; R2 = 6,67 kN; M in x = 2 = 26,67 kNm.
- Combinazione:
  - R1 = 1,3·30 + 1,5·13,33 = 59,0 kN;
  - R2 = 1,3·30 + 1,5·6,67 = 49,0 kN;
  - M = 1,3·40 + 1,5·26,67 = 92,0 kNm.

## C11 · cedimento vincolare (preparato il 30/10, calcolato dal 31/10)

Trave continua su tre appoggi, IPE 300, due campate da 6 m, nessun carico, cedimento dell'appoggio centrale δ = 10 mm verso il basso.

Soluzione a mano: la reazione dell'appoggio centrale equivale alla forza che, in mezzeria di una trave appoggiata lunga 2L = 12 m, produce la freccia δ.
1. F = 48·EI·δ/(2L)³ = 48 × 17 547,6 × 0,010/1728 = 4,874 kN, diretta verso il basso: è l'appoggio che trattiene la trave.
2. Reazioni: RB = −4,874 kN; RA = RC = +2,437 kN.
3. Momento sull'appoggio centrale: |MB| = F·2L/4 = 14,62 kNm, con fibre tese in basso.

Dal 31/10 il caso è nei file JSON (schema v1.1, solutore v0.3). Si aggiunge anche la rotazione in A: φA = −F·(2L)²/(16EI) = −2,50 mrad.

## C12 · trapezio parziale (Daniela, 31/10)

Trave appoggiata, L = 6 m; carico verso il basso da q1 = 10 kN/m in a = 1 m a q2 = 20 kN/m in b = 4 m.
1. Risultante W = (b − a)·(q1 + q2)/2 = 3 × 30/2 = 45 kN.
2. Baricentro xg = a + (b − a)·(q1 + 2q2)/(3(q1 + q2)) = 1 + 3 × 50/90 = 2,667 m.
3. Reazioni: R2 = W·xg/L = 20,00 kN; R1 = 25,00 kN.
4. Momenti:
   - M(1) = R1·1 = 25,00 kNm;
   - M(4) = R2·2 = 40,00 kNm;
   - M(3), con t = 2: M = R1·3 − (q1·t²/2 + (q2 − q1)/3·t³/6) = 75 − (20 + 4,444) = 50,56 kNm.

Il massimo cade in x = 2,899 m e vale 50,64 kNm: non è un punto del diagramma a 7 punti.

## C13 · carico triangolare su trave incastrata (Daniela, 31/10)

Trave incastrata alle due estremità, L = 6 m, carico da 0 in x = 0 a q = 20 kN/m in x = 6 m. Formule tabellate:
- MA = qL²/30 = 24 kNm e MB = qL²/20 = 36 kNm, con fibre tese in alto (M = −24 e −36);
- RA = 3qL/20 = 18 kN e RB = 7qL/20 = 42 kN.

Verifica di equilibrio: RA + RB = qL/2 = 60 kN.

## File

- `C*.json`: modelli di input
- `C*.atteso.json`: valori attesi con le formule usate
- `C*.riferimento.json`: risultati completi del risolutore di riferimento (spostamenti, reazioni, N-V-M)
- `genera_casi.py`: rigenera modelli e valori attesi
- `verifica_casi.py`: valida i modelli con lo schema, li risolve e confronta con gli attesi (tolleranza 0,5 %); `--fortran` usa il solutore Fortran, `--api` il percorso completo attraverso il servizio FastAPI
- `../riferimento/telaio2d.py`: risolutore di riferimento in Python, senza dipendenze

## Come si usa per il solutore Fortran

Silvia sostituisce in `verifica_casi.py` la funzione `risultati(modello, caso)` con la chiamata al solutore Fortran tramite il convertitore di Paola. Il solutore è accettato quando tutti i controlli passano.
