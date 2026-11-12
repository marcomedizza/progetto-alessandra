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
| C15 | Asta inclinata (0; 0)–(4; 3), cerniera e carrello, q = 10 kN/m verticale da 1 a 4 m lungo l'asta (v1.1) | statica | R1 = R2 = 15 kN; Rx = 0; M(2,5) = 21,0 kNm; N(0) = −9 kN; N(5) = +9 kN |
| C16 | Geometria di C6, nessun carico, cedimento di 10 mm dell'appoggio (v1.1) | isostatica | reazioni e momenti nulli; cerniera ferma; tratto 4–6 ruota di −δ/2 = −5 mrad |
| C17 | Geometria di C15, q = 10 kN/m normale all'asta (locale_y) da 1 a 4 m (v1.1, punto 32) | statica | Rx1 = −18 kN; Ry1 = 5,25 kN; Ry2 = 18,75 kN; M(2,5) = 26,25 kNm; N = +11,25 kN costante |
| C14 | Trave incastrata L = 6 m, ΔT uniforme +20 °C e a farfalla +10 °C (v1.2) | formule chiuse | N = −EAαΔTu = −271,2 kN; M = −EIαΔTg/h = −7,02 kNm costante; Rx1 = +271,2 kN |
| C18 | Trave appoggiata L = 6 m, ΔT a farfalla +10 °C (v1.2) | formule chiuse | nessuna reazione; uy(3) = −κL²/8 = −1,80 mm; φ = ∓κL/2 = ∓1,20 mrad |
| C19 | Geometria di C6, ΔT a farfalla +10 °C sulla mensola con cerniera in j (v1.2, punto 41) | isostatica | nessuna sollecitazione; uy cerniera = κa²/2 = +3,20 mm; φ mensola = κa = +1,60 mrad; tratto 4–6 −1,60 mrad |
| C20 | Geometria di C6, trapezio da 10 a 20 kN/m tra 0,5 e 2,0 m del tratto appoggiato (v1.1) | statica | R3 = 15,0 kN; R1 = 7,5 kN; M incastro = −30,0 kNm; M a 1 m dalla cerniera = 6,11 kNm; cerniera −9,12 mm |
| C21 | Geometria di C15, trapezio verticale da 10 a 20 kN/m tra 1 e 4 m lungo l'asta, cedimento del carrello di 10 mm (v1.1) | statica | R1 = 21 kN; R2 = 24 kN; Rx = 0; M(2,5) = 31,5 kNm; uy carrello = −10 mm |
| C22 | C20 con molla ky = 2000 kN/m al posto dell'appoggio a 6 m (v1.1) | isostatica | R3 = 15,0 kN (molla); R1 = 7,5 kN; M incastro 30,0 kNm; molla −7,5 mm; cerniera −9,12 mm |
| C25 | portale a tre cerniere IPE 300, h = 4 m, L = 6 m, cerniera in mezzeria del traverso; trapezio 10→20 kN/m sulla metà sinistra; cedimento di 10 mm del piede destro (v1.1) | isostatica | VA = 32,5, VB = 12,5 kN; HA = −HB = 9,375 kN; M agli angoli 37,5 kNm; M a 1,5 m 1,875 kNm; reazioni invariate dal cedimento |
| C24 | telaio a due piani, colonne HE 200 A incastrate, travi IPE 300 incernierate agli estremi, deformabilità assiale trascurata; G: q = 25 kN/m, W: 10 e 15 kN; combinazione 1,3·G + 1,5·W | iperstatica (soluzione esatta per simmetria) | Ry = 195 kN e Rx = −18,75 kN per piede; M piede 105 kNm; M colonna al primo piano 39,375 kNm; M travi 146,25 kNm |
| C23 | trave incastrata IPE 300, L = 6 m: caso G triangolare 0–20 kN/m (C13), caso T con ΔTu 20 °C e ΔTg 10 °C (C14), combinazione 1,3·G + 0,9·T (v1.2) | iperstatica | Ry = 23,4 e 54,6 kN; M = −37,52 e −53,12 kNm; N = −244,08 kN |
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

## C15 · carico parziale su asta inclinata (Daniela, 02/11)

Asta da (0; 0) a (4; 3), quindi L = 5 m, cos α = 0,8 e sin α = 0,6. Cerniera al piede, carrello in testa (solo uy impedito). Carico verticale q = 10 kN/m per metro d'asta, da s = 1 a s = 4 m.
1. W = q·3 = 30 kN; baricentro in s = 2,5 m, cioè x = 2,0 m.
2. Reazioni: R2 = 30 × 2/4 = 15 kN; R1 = 15 kN; nessuna reazione orizzontale, perché carichi e carrello sono verticali.
3. Componenti locali del carico: trasversale q·cos α = 8 kN/m, assiale q·sin α = 6 kN/m verso il piede.
4. M(2,5) = R1·cos α·2,5 − 8 × 1,5²/2 = 30 − 9 = 21,0 kNm. Con la proiezione orizzontale si ottiene lo stesso valore: 15 × 2 − 12,5 × 1,2²/2 = 21,0.
5. Sforzo normale: N(0) = −R1·sin α = −9 kN (compressione); N(5) = +R2·sin α = +9 kN; la differenza vale 6 × 3 = 18 kN.

## C16 · cedimento su struttura con cerniera (Silvia e Carla, 02/11)

Stessa geometria di C6, senza carichi; l'appoggio a 6 m cede di δ = 10 mm.
- La struttura è isostatica, quindi il cedimento non produce reazioni né sollecitazioni.
- La mensola resta indeformata (cerniera ferma, rotazione della mensola nulla).
- Il tratto 4–6 ruota rigidamente attorno alla cerniera di −δ/2 = −5 mrad.

Il caso controlla insieme cerniera interna, rotazioni d'estremità e cedimenti.

## C17 · carico normale all'asta inclinata (Daniela, 03/11)

Geometria e vincoli di C15; carico q = 10 kN/m perpendicolare all'asta, verso −y locale, cioè (sin α; −cos α) = (0,6; −0,8), da s = 1 a s = 4 m.
1. Risultante W = 30 kN, con componenti (18; −24) kN, applicata in s = 2,5 m, cioè nel punto (2; 1,5).
2. Momento attorno al piede: 4·R2 + (2 × (−24) − 1,5 × 18) = 0, quindi R2 = 75/4 = 18,75 kN.
3. Reazioni al piede: R1y = 24 − 18,75 = 5,25 kN; R1x = −18 kN.
4. Componente trasversale di R1: T1 = 18 × 0,6 + 5,25 × 0,8 = 15 kN. M(2,5) = 15 × 2,5 − 10 × 1,5²/2 = 26,25 kNm.
5. Sforzo normale costante, perché il carico non ha componente assiale: N = −(R1x·cos α + R1y·sin α) = −(−14,4 + 3,15) = +11,25 kN (trazione).

## C14 e C18 · distorsioni termiche (Valentina, 03/11)

Acciaio α = 1,2·10⁻⁵ /°C, IPE 300 con h = 0,300 m, EA = 1,130·10⁶ kN, EI = 17 547,6 kNm².

**C14, trave incastrata, ΔTu = +20 °C, ΔTg = +10 °C**
- Dilatazione impedita: N = −EA·α·ΔTu = −1,130·10⁶ × 1,2·10⁻⁵ × 20 = −271,2 kN (compressione). Gli incastri spingono verso l'interno: Rx1 = +271,2 kN, Rx2 = −271,2 kN.
- Curvatura impedita: κ = α·ΔTg/h = 1,2·10⁻⁵ × 10/0,3 = 4,0·10⁻⁴ 1/m. M = −EI·κ = −7,02 kNm costante, fibre tese in alto.

**C18, trave appoggiata, ΔTg = +10 °C**
- Struttura isostatica: nessuna reazione e nessun momento.
- Il lato inferiore, più caldo, si allunga e diventa il lato convesso: la trave si inflette verso il basso con v(x) = κ·x·(x − L)/2.
- v(3) = −κL²/8 = −4·10⁻⁴ × 36/8 = −1,80 mm; φ(0) = −κL/2 = −1,20 mrad; φ(6) = +1,20 mrad.

## C19 · cerniera interna e ΔT a farfalla (Valentina e Daniela, 04/11)

Geometria di C6; ΔTg = +10 °C (lato inferiore più caldo) solo sulla mensola 0–4 m, che ha la cerniera all'estremità j. κ = α·ΔTg/h = 4,0·10⁻⁴ 1/m.
- La struttura è isostatica: la distorsione non produce reazioni né momenti.
- Mensola: curvatura libera senza momento, quindi v(x) = κx²/2. Il lato inferiore, più lungo, rende la mensola concava verso l'alto e la punta sale: v(4) = 4·10⁻⁴ × 16/2 = +3,20 mm. Rotazione alla cerniera φ = κ·4 = +1,60 mrad.
- Tratto 4–6: ruota rigidamente attorno all'appoggio, φ = −3,20/2000 = −1,60 mrad. La rotazione è discontinua alla cerniera: +1,60 sulla mensola, −1,60 sul tratto appoggiato.

Il caso controlla che la condensazione statica della cerniera tratti anche le forze d'incastro termiche (punto 41 della revisione).

## C20 · trapezio parziale con cerniera interna (Daniela e Valentina, 05/11)

Geometria di C6. Sul tratto appoggiato 4–6 m c'è un carico verso il basso da q1 = 10 kN/m a q2 = 20 kN/m, tra a = 0,5 e b = 2,0 m dal nodo 2, cioè dalla cerniera.
1. Risultante W = 1,5 × 15 = 22,5 kN.
2. Baricentro xg = 0,5 + 1,5 × (10 + 40)/(3 × 30) = 1,333 m dalla cerniera.
3. Tratto appoggiato: R3 = 22,5 × 1,333/2 = 15,0 kN; forza trasmessa dalla cerniera Rs = 7,5 kN.
4. Mensola caricata in punta da Rs:
   - R1 = 7,5 kN;
   - M incastro = −7,5 × 4 = −30,0 kNm;
   - abbassamento della cerniera = Rs·4³/(3EI) = 7,5 × 64/(3 × 17 547,6) = 9,12 mm.
5. Momento a 1 m dalla cerniera, con t = 0,5: M = 7,5 × 1 − (10 × 0,5²/2 + 10/1,5 × 0,5³/6) = 7,5 − 1,389 = 6,11 kNm.

## C21 · trapezio su asta inclinata con cedimento (Daniela e Valentina, 08/11)

Geometria e vincoli di C15: asta da (0; 0) a (4; 3), cos α = 0,8. Carico verticale da q1 = 10 a q2 = 20 kN/m per metro d'asta, tra s = 1 e s = 4 m; il carrello in testa cede di δ = 10 mm.
1. W = 3 × 15 = 45 kN.
2. Baricentro lungo l'asta: sg = 1 + 3 × 50/90 = 2,667 m, cioè x = 2,133 m.
3. Reazioni: R2 = 45 × 2,133/4 = 24,0 kN; R1 = 21,0 kN; nessuna reazione orizzontale.
4. Momento in s = 2,5, con t = 1,5:
   - componente trasversale di R1: 21 × 0,8 = 16,8 kN;
   - carico trasversale: 0,8 × (10 × 1,5²/2 + 10/3 × 1,5³/6) = 0,8 × 13,125 = 10,5 kNm;
   - M = 16,8 × 2,5 − 10,5 = 31,5 kNm.
5. La struttura è isostatica, quindi il cedimento non cambia reazioni né momenti: compare solo come spostamento imposto, uy del carrello = −10 mm.

Il caso unisce asta inclinata, trapezio e cedimento, già provati separatamente in C15, C12 e C16.

## C22 · trapezio, cerniera e molla (Daniela e Valentina, 09/11)

C20 con l'appoggio a 6 m sostituito da una molla verticale ky = 2000 kN/m. La struttura resta isostatica: la molla sostituisce un vincolo senza aggiungerne. Reazioni e sollecitazioni sono quindi quelle di C20: R3 = 15,0 kN, Rs = 7,5 kN, M incastro 30,0 kNm.
- La molla si abbassa di R3/ky = 15/2000 = 7,5 mm.
- La cerniera si abbassa come in C20, perché la mensola porta lo stesso carico in punta: −9,12 mm.
- Il tratto 4–6 ha la stessa curvatura di C20, più una rotazione rigida diversa.

## C23 · combinazione di carico triangolare e distorsione termica (Daniela e Valentina, 10/11)

Primo caso che combina un carico con una distorsione termica. Il servizio somma i risultati dei casi G e T con i coefficienti 1,3 e 0,9.
- Caso G (come C13): MA = −qL²/30 = −24 kNm, MB = −qL²/20 = −36 kNm, RA = 3qL/20 = 18 kN, RB = 7qL/20 = 42 kN.
- Caso T (come C14): N = −E·A·α·ΔTu = −271,2 kN; M = −E·I·α·ΔTg/h = −7,02 kNm costante; nessuna reazione verticale.
- Combinazione: Ry = 1,3·18 = 23,4 kN e 1,3·42 = 54,6 kN; M = 1,3·(−24) + 0,9·(−7,02) = −37,52 kNm e 1,3·(−36) + 0,9·(−7,02) = −53,12 kNm; N = 0,9·(−271,2) = −244,08 kN.

**Coefficienti**: 0,9 = 1,5·ψ0 con ψ0 = 0,6 per le variazioni termiche (NTC 2018, tab. 2.5.I; valore citato a memoria, da ricontrollare sul testo). Vale per la temperatura come azione di accompagnamento. In C23 la temperatura è l'unica azione variabile, quindi in una combinazione normativa sarebbe l'azione principale con γ = 1,5. Il caso prova la sovrapposizione con coefficienti diversi tra loro, non la scelta normativa dei coefficienti.

## C24 · telaio a due piani a travi incernierate, combinazione (Daniela e Valentina, 11/11)

Telaio con le travi incernierate a entrambe le estremità e deformabilità assiale trascurata. Le travi sono bielle rigide tra due mensole uguali, quindi la soluzione è esatta senza risolvere il telaio.
- **Caso G** (q = 25 kN/m sulle due travi): ogni trave è appoggiata, M = qL²/8 = 112,5 kNm. Ogni colonna riceve qL/2 = 75 kN per piano, senza flessione, perché le cerniere non trasmettono momento. Ry = 150 kN per piede.
- **Caso W** (10 kN al primo piano, 15 kN al secondo): le bielle rigide impongono lo stesso spostamento orizzontale alle due mensole. Essendo uguali, ciascuna porta metà di ogni forza: 5 e 7,5 kN.
  - Rx = −12,5 kN per piede.
  - M al piede = 5·3,5 + 7,5·7 = 70 kNm.
  - M della colonna al primo piano = 7,5·3,5 = 26,25 kNm.
  - Nessuna reazione verticale.
  - Le travi sono compresse, perché portano alla colonna destra metà della forza di piano: 5 kN al primo piano, 7,5 kN al secondo.
- **Combinazione 1,3·G + 1,5·W**:
  - Ry = 195 kN;
  - Rx = −18,75 kN;
  - M piede = 105 kNm;
  - M colonna al primo piano = 39,375 kNm;
  - M travi = 146,25 kNm;
  - N colonna destra al piede = −195 kN;
  - N travi = 7,5 e 11,25 kN.

**Coefficienti**: 1,3 per i permanenti non strutturali e 1,5 per il vento come azione principale. È lo stesso schema dell'esempio di riferimento `ESEMPIO_PORTALE_2D.json`. Con G2 non compiutamente definiti le NTC prevedono 1,5 (tab. 2.6.I, citata a memoria, da ricontrollare sul testo), quindi anche qui i coefficienti servono a provare la sovrapposizione e non sono una scelta di progetto.

**Controllo nell'interfaccia** (11/11): reazioni, |M|, |V| e |N| per asta coincidono con i valori sopra.

## C25 · portale a tre cerniere, trapezio parziale e cedimento (Daniela e Valentina, 12/11)

Unisce cerniera interna, trapezio e cedimento, provati finora a coppie (C16, C20, C21, C22). La struttura è isostatica: appoggi fissi ai piedi A (0; 0) e B (6; 0), cerniera C (3; 4) in mezzeria del traverso.
1. Risultante del trapezio sulla metà sinistra (qi = 10, qj = 20 kN/m, a = 3 m): F = (10 + 20)/2 · 3 = 45 kN, a xF = 3·(10 + 40)/(3·30) = 1,667 m dal nodo 2.
2. Rotazione attorno ad A: VB · 6 = 45 · 1,667, quindi VB = 12,5 kN e VA = 32,5 kN.
3. M = 0 in C per la parte destra (colonna e mezza trave scariche): 3 · VB + 4 · HB = 0, quindi HB = −9,375 kN e HA = +9,375 kN.
4. Momenti agli angoli: HA · h = 37,5 kNm su entrambe le colonne.
5. Nel traverso, con x dal nodo 2: M(x) = VA·x − HA·h − (qi·x²/2 + (qj − qi)/a · x³/6). In x = 1,5 m vale 48,75 − 37,5 − 13,125 = −1,875 kNm; in x = 3 m vale 97,5 − 37,5 − 60 = 0, come deve alla cerniera.
6. Il cedimento di 10 mm del piede destro non cambia reazioni né sollecitazioni, perché la struttura è isostatica: dà solo un moto rigido. La prova del servizio `test_tre_cerniere_cedimento_isostatico` lo controlla confrontando il calcolo con e senza cedimento.

## File

- `C*.json`: modelli di input
- `C*.atteso.json`: valori attesi con le formule usate
- `C*.riferimento.json`: risultati completi del risolutore di riferimento (spostamenti, reazioni, N-V-M)
- `genera_casi.py`: rigenera modelli e valori attesi
- `verifica_casi.py`: valida i modelli con lo schema, li risolve e confronta con gli attesi (tolleranza 0,5 %); `--fortran` usa il solutore Fortran, `--api` il percorso completo attraverso il servizio FastAPI
- `../riferimento/telaio2d.py`: risolutore di riferimento in Python, senza dipendenze

## Come si usa per il solutore Fortran

Silvia sostituisce in `verifica_casi.py` la funzione `risultati(modello, caso)` con la chiamata al solutore Fortran tramite il convertitore di Paola. Il solutore è accettato quando tutti i controlli passano.
