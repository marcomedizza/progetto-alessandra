# Prova del flusso utente — prototipo del 09/11/2026

**Autrice**: Renata (validazione flussi) · **Data**: 27/10/2026
**Oggetto**: percorso completo dell'utente: apertura del modello, modifica, calcolo, lettura dei risultati.

## Avvio

    04-FORTRAN-SOLVER/build.sh
    python3 -m pip install fastapi uvicorn jsonschema
    python3 -m uvicorn --app-dir 03-BACKEND/servizio app:app --port 8000

Aprire http://127.0.0.1:8000/ in un navigatore recente (Chrome, Edge, Firefox).

## Scenari

| # | Scenario | Passi | Risultato atteso |
|---|---|---|---|
| S1 | Apertura | Aprire la pagina | Si carica il portale C4 in vista frontale, con vincoli e carichi visibili |
| S2 | Calcolo | Premere «Calcola» | Messaggio «Calcolo completato»; diagramma M; reazioni Ry = 90 kN per appoggio; M traverso = 83,70 kNm |
| S3 | Diagrammi | Scegliere V, poi N, poi «nessuno» | Il diagramma cambia senza ricalcolo; M dal lato delle fibre tese |
| S4 | Deformata | Togliere e rimettere la spunta | La deformata tratteggiata compare e scompare |
| S5 | Viste | Frontale, dall'alto, assonometrica | La telecamera cambia; nell'assonometrica il trascinamento ruota |
| S6 | Selezione asta | Clic sul traverso | Pannello con lunghezza 6 m, IPE 300, carico −30 kN/m e sollecitazioni massime |
| S7 | Modifica sezione | Cambiare la sezione del traverso in HE 200 A | Messaggio «Modello modificato»; risultati azzerati; ricalcolo con M angolo diverso |
| S8 | Modifica carico | Portare q a −40 kN/m e ricalcolare | Reazioni verticali 120 kN |
| S9 | Selezione nodo | Clic sul nodo 2 | Coordinate, vincolo, carichi nodali e spostamenti |
| S10 | Vincolo insufficiente | Togliere ux al nodo 1 in C1 e calcolare | Errore leggibile: struttura labile o vincoli insufficienti |
| S11 | Altro modello | Scegliere C5 e calcolare | Telaio a due piani con diagrammi su tutte le aste |
| S12 | File locale | Aprire un modello JSON dal computer | Il modello si carica; se non è valido, il calcolo restituisce l'elenco degli errori |
| S13 | Servizio spento | Fermare uvicorn e premere «Calcola» | Messaggio «Servizio di calcolo non raggiungibile» |
| S14 | Nuovo modello (D4) | «Nuovo», selezionare la trave, aggiungere q = −10 kN/m, calcolare | Trave appoggiata 6 m: M max = 45 kNm |
| S15 | Aggiunta nodo e asta (D4) | Aggiungere il nodo (0; 3) e l'asta 1 → 3, calcolare; ripetere lo stesso nodo | Calcolo completato; il nodo doppio è rifiutato con messaggio |
| S16 | Valori sui diagrammi (D3) | C4, calcolare, diagramma M | Etichette 25,6 · 51,3 · 83,7 kNm sui punti significativi |
| S17 | Disegno col mouse (D10) | «Nuovo», «Disegna aste», clic sul nodo 1, poi vicino a (0; 3), (6; 3) e sul nodo 2; Esc; Fx = 10 kN nel nodo 3; calcolare | Nodi agganciati alla griglia di passo 0,5 m (il clic a (0,1; 3,12) dà il nodo (0; 3)); tre aste aggiunte; Rx1 = −10 kN, Ry1 = −5 kN, Ry2 = +5 kN |
| S18 | Materiali e sezioni (rev. 14) | C1, selezionare un'asta, I = 16 712 cm⁴ (doppio), calcolare; poi «+» sezione e «+» materiale con E = 70 000 MPa sulla sola asta 1 | Freccia 4,808 mm, metà di 9,617; con l'asta 1 a E·I = 2/3 dell'originale e l'asta 2 al doppio la freccia torna 9,617 mm (contributi delle due metà); E = −5 rifiutato |
| S20 | Cedimento (v1.1) | C11, calcolare; clic sul nodo centrale | Ry = −4,87 · 2,44 kN; M = 14,62 kNm; nel pannello «Cedimento impresso: uy = −10 mm» |
| S21 | Trapezio parziale (v1.1) | C12, calcolare | Frecce di lunghezza crescente da 1 a 4 m; R = 25 · 20 kN; M max del diagramma 50,6 kNm |
| S22 | Triangolare su trave incastrata (v1.1) | C13, calcolare | R = 18 · 42 kN; momenti d'incastro 24 e 36 kNm |
| S23 | Trapezio dal pannello (D15) | «Nuovo», selezionare la trave, «+ trapezio» con i valori proposti (−10 → −20 kN/m su tutta la luce), calcolare; poi b = 7 m | R1 = 40 kN, R2 = 50 kN; con b oltre l'asta il messaggio «Il tratto deve stare dentro l'asta» |
| S24 | Cedimento dal pannello (D15) | C1, nodo 3, uy = −10 mm, «imposta», calcolare | Compare solo il campo uy (l'unica componente vincolata); reazioni invariate 30 · 30 kN (trave isostatica); uy del nodo 3 = −10 mm |
| S25 | Annulla (D13) | Dopo S23 premere «Annulla» due volte | Il trapezio sparisce e il ricalcolo non dà più 40 kN; al secondo clic «Niente da annullare» |
| S26 | Spostamento massimo (D14) | Dopo S23 leggere la nota sotto le tabelle | «asta 1, x = 3,00 m, uy = −14,43 mm», uguale a 5qL⁴/(384EI) con q = 15 kN/m (il triangolo antisimmetrico non dà freccia in mezzeria) |
| S27 | Direzione del trapezio (punto 32) | «Nuovo», trave, direzione «orizzontale (X)», q = −10 kN/m su tutta la luce, calcolare | Rx1 = +60 kN, nessuna reazione verticale |
| S28 | Carico normale all'asta inclinata | C17, calcolare | Rx1 = −18,00 kN; Ry = 5,25 · 18,75 kN |
| S29 | ΔT su trave incastrata (v1.2) | C14, calcolare | Reazione orizzontale 271,20 kN |
| S30 | ΔT a farfalla su trave appoggiata (v1.2) | C18, calcolare, selezionare un'asta | Spostamento massimo −1,80 mm in mezzeria; nel pannello «Distorsione termica: … 10 °C»; sollecitazioni 0 |
| S31 | Distorsione termica dal pannello (D17) | «Nuovo», selezionare la trave, ΔT a farfalla 10 °C, «+ ΔT», calcolare; poi «+ trapezio» e ricalcolo | Nota «qui: lato inferiore meno superiore»; spostamento massimo −1,80 mm in mezzeria; dopo il trapezio il modello resta in versione 1.2 e il calcolo riesce |
| S32 | Altezza della sezione | Copia della sezione, h = −1 | Valore rifiutato, resta 300 mm |
| S33 | ΔT uniforme su trave appoggiata | ΔT uniforme 20 °C, calcolare | Nessuna reazione orizzontale aggiuntiva: il carrello lascia libero l'allungamento |
| S19 | Deformata con cerniera (D8) | C6, calcolare | Deformata con angolo alla cerniera: mensola curva fino a 4 m, tratto appoggiato quasi rettilineo; nota «comprese quelle alle cerniere interne» |

## Esiti

| Scenario | 27/10 | 28/10 (Renata, Vittoria; Chromium automatico) |
|---|---|---|
| S1 Apertura | superato | superato |
| S2 Calcolo | superato | superato (Ry = 90,00 kN, M traverso = 83,70 kNm) |
| S3 Diagrammi | superato | superato |
| S4 Deformata | — | superato |
| S5 Viste | superato | superato |
| S6 Selezione asta | superato | superato |
| S7 Modifica sezione | — | superato (risultati azzerati, nuovo calcolo diverso) |
| S8 Modifica carico | — | superato (Ry = 120,00 kN con q = −40 kN/m) |
| S9 Selezione nodo | — | superato |
| S10 Vincolo insufficiente | — | superato: «matrice singolare: struttura labile o vincoli insufficienti» |
| S11 Altro modello (C5) | superato | superato |
| S12 File locale (C2) | — | superato (M incastro 30,00 kNm) |
| S13 Servizio spento | — | superato: «Servizio di calcolo non raggiungibile» |
| Combinazione SLU1 dell'esempio | — | superato: ΣRy = 241,69 kN = 1,3 × (180 + peso proprio 5,92) kN; ΣRx = −30,00 kN = −1,5 × 20 kN |

| Scenario | 29/10 (Renata, Vittoria; Chromium automatico) |
|---|---|
| S1–S9, S11–S13, combinazione | superati di nuovo dopo le modifiche del giorno |
| S10 | superato («matrice singolare: struttura labile o vincoli insufficienti») |
| S14 | superato: M max 45 kNm |
| S15 | superato: asta aggiunta e calcolata; nodo doppio rifiutato («Esiste già un nodo in quella posizione») |
| S16 | superato: 25,6 · 51,3 · 83,7 kNm |

| Scenario | 30/10 (Renata, Vittoria; Chromium automatico) |
|---|---|
| S1–S9, S11–S16, combinazione | superati di nuovo dopo le modifiche del giorno |
| S10 | superato con la prova dedicata (errore «matrice singolare: struttura labile o vincoli insufficienti»); nella prova generale lo script stima male la posizione del nodo, difetto dello script e non del programma |
| S17 | superato: nodi (0; 3) e (6; 3) agganciati, aste 2, 3 e 4, reazioni −10 · −5 · +5 kN |
| S18 | superato: 4,808 mm, poi 9,617 mm; E negativo rifiutato; copie IPE300_2 e S275_2 create |
| S19 | superato: scarto tra deformata disegnata e soluzione esatta 3·10⁻¹⁷ m su entrambe le aste |

| Scenario | 31/10 (Renata, Vittoria; Chromium automatico) |
|---|---|
| S1–S19, combinazione | superati di nuovo dopo le modifiche del giorno (S10 con la prova dedicata) |
| S20 | superato: −4,87 · 2,44 kN, 14,62 kNm, cedimento −10 mm nel pannello |
| S21 | superato: 25,00 · 20,00 kN, etichetta 50,6 kNm |
| S22 | superato: 18,00 · 42,00 kN, etichette 24 e 36 kNm |

| Scenario | 02/11 (Renata, Vittoria; Chromium automatico) |
|---|---|
| S1–S22, combinazione | superati di nuovo dopo le modifiche del giorno (S10 con la prova dedicata) |
| S23 | superato: 40,00 · 50,00 kN; b = 7 m rifiutato |
| S24 | superato: solo il campo uy; 30,00 · 30,00 kN; uy = −10 mm |
| S25 | superato |
| S26 | superato: −14,43 mm in x = 3,00 m |

| Scenario | 03/11 (Renata, Vittoria; Chromium automatico) |
|---|---|
| S1–S26, combinazione | superati di nuovo dopo le modifiche del giorno (S10 con la prova dedicata) |
| S27 | superato: Rx1 = 60,00 kN |
| S28 | superato |
| S29 | superato: 271,20 kN |
| S30 | superato: −1,80 mm; residui numerici mostrati come 0 dopo la correzione di D16 |

| Scenario | 04/11 (Renata, Vittoria; Chromium automatico) |
|---|---|
| S1–S30, combinazione | superati di nuovo dopo le modifiche del giorno (S10 con la prova dedicata) |
| S31 | superato: −1,80 mm; trapezio successivo calcolato |
| S32 | superato |
| S33 | superato: reazioni 0 · 40 · 50 kN, dovute solo al trapezio |

| Scenario | 06/11 (Renata, Vittoria, Mariana; Chromium automatico) |
|---|---|
| S1–S33, combinazione | superati di nuovo dopo le modifiche del giorno (S10 con la prova dedicata) |
| C14, C18, C19 (leggibilità, Mariana) | deformata corretta: su C19 mensola incurvata verso l'alto fino alla cerniera e tratto appoggiato rettilineo. Su C19 il diagramma M nullo mostrava due etichette «0» da rumore numerico (D18), corretto |

| Scenario | 07/11 (Renata, Vittoria, Mariana; Chromium automatico) |
|---|---|
| S1–S33, combinazione | superati di nuovo dopo le modifiche del giorno (S10 con la prova dedicata) |
| C20 | etichette 30 e 6,1 kNm, spostamento massimo −9,12 mm alla cerniera |
| Modello grande (4681 nodi, 9150 aste) da file | prima delle correzioni di D19: apertura 1,5 s, calcolo e disegno 12,7 s, 1,2 GB di memoria. Dopo: apertura 1,0 s, calcolo e disegno 4,7 s, 0,79 GB; modifica 1,7 s e «Annulla» 1,7 s |
| Controllo a vista (C5, C7, C12) | trovato D20 (frecce dei carichi 25 volte troppo lunghe su C5), corretto e ricontrollato |

**Lezione del 07/11**: le prove automatiche controllano i valori, non l'aspetto. D20 era presente dal 31/10 e nessuno scenario l'aveva rilevato. Da oggi ogni consegna dell'interfaccia include il controllo a vista delle schermate di C4, C5, C7 e C12.

| Scenario | 08/11 (Renata, Vittoria, Mariana; Chromium automatico) |
|---|---|
| S1–S33, combinazione | superati di nuovo (S10 con la prova dedicata) |
| Modello grande | calcolo e disegno 3,5 s (4,7 il 07/11, grazie alla validazione rapida), apertura 0,9 s, Annulla 1,5 s, 0,84 GB |
| Controllo a vista | C4, C5, C7, C12, C21: frecce proporzionate, diagrammi dal lato teso, deformate coerenti |

| Scenario | 09/11 (Renata, Vittoria, Mariana, Lucia; Chromium automatico) |
|---|---|
| S1–S33, combinazione | superati di nuovo (S10 con la prova dedicata) |
| Soglia dei diagrammi nulli (Lucia) | C19 senza etichette, C20 con 30 e 6,1 kNm, C21 con 31,5 kNm: la soglia non nasconde valori reali |
| Controllo a vista | C4, C5, C7, C12, C21, C22 corretti; su C22 la molla è disegnata come un anello, poco riconoscibile (D21) |

Nessun errore nella console. Firefox non provato (non disponibile nell'ambiente automatico): da fare a mano.

| Scenario | 10/11 (Renata, Vittoria, Mariana; Chromium automatico) |
|---|---|
| S1–S33, combinazione | superati; S10 con la prova dedicata, perché il clic sul nodo 1 di C1 nello script complessivo non seleziona il nodo. Il comportamento è lo stesso con il codice del 09/11, quindi il problema è nello script e non nell'interfaccia |
| Modello grande (4681 nodi, 9150 aste) | caricamento 0,9 s, calcolo e disegno 3,1 s, modifica 1,6 s, annulla 1,6 s, 792 MB, nessun errore |
| Controllo a vista | C13 e C23 con deformata visibile (D22); C14 senza deformata, corretto perché gli spostamenti sono nulli; molle a zig-zag su C8, C9, C22 (D21) |

| Scenario | 11/11 (Renata, Vittoria, Mariana; Chromium automatico) |
|---|---|
| S1–S33, combinazione | superati; S10 con la prova dedicata, come il 10/11 |
| S34, combinazioni di C23 e C24 nell'interfaccia | superato: C23 Ry 23,40 e 54,60 kN, M −37,52 e −53,12 kNm, N −244,08 kN; C24 Rx −18,75, Ry 195,00 kN, Mz 105,00 kNm, N travi 7,50 e 11,25 kN |
| Modello grande | 1,2–1,6 s per il caricamento, 4,2–5,4 s per calcolo e disegno, 782 MB, nessun errore. I tempi sono più alti del 10/11 (3,1 s) anche con il codice del 10/11, quindi dipendono dalla macchina, riavviata il giorno stesso, e non dalle modifiche |
| Controllo a vista | C24 caso G: momenti delle travi 112,5 kNm, colonne senza flessione, cerniere visibili; C24 combinazione: deformata e diagrammi coerenti; molle invariate dopo il punto 65 |

| Scenario | 12/11 (Renata, Vittoria, Mariana; Chromium automatico) |
|---|---|
| S1–S34, combinazione | superati; S10 con la prova dedicata |
| Modello grande | 1,3–1,8 s per il caricamento, 4,2–4,8 s per calcolo e disegno, nessun errore; il controllo delle sovrapposizioni delle etichette (al più 150) non cambia i tempi |
| Controllo a vista | C25: momenti 37,5 kNm agli angoli, zero alla cerniera, piccolo tratto positivo sotto il trapezio, coerente con M(1,5) = −1,875 kNm; C24 combinazione: freccia del primo piano libera; C5: etichette del nodo 3 separate. Con lo scorrimento l'etichetta d'estremità del traverso di C5 («31,7») si trova a circa 0,7 m dal nodo: il valore resta quello dell'estremità |

## Difetti

| N. | Data | Scenario | Descrizione | Gravità | Stato | Assegnata a |
|---|---|---|---|---|---|---|
| D1 | 27/10 | S4 | Deformata interpolata solo dagli spostamenti nodali | bassa | **chiuso 28/10**: aggiunta l'inflessione dei carichi d'asta, esatta per aste senza cerniere (verificata su C1 e C7) | Mariana |
| D2 | 27/10 | S2 | Combinazioni di carico non calcolate | media | **chiuso 28/10**: sovrapposizione lineare nel servizio e scelta della combinazione nell'interfaccia | Natalia, Benedetta |
| D3 | 27/10 | S1 | Nessun valore numerico sui diagrammi | bassa | **chiuso 29/10**: valori alle estremità e massimo interno; M in valore assoluto (il lato del diagramma indica le fibre tese) | Mariana |
| D4 | 27/10 | — | Non si possono disegnare nodi e aste nuovi | alta per la versione alfa | **chiuso 29/10** in versione minima: nuovo modello, aggiunta ed eliminazione di nodi e aste per coordinate, carichi uniformi sulle aste. Resta da fare il disegno col mouse | Lucia, Irene |
| D5 | 28/10 | S9 | Nodi difficili da selezionare col mouse | bassa | **chiuso 28/10** | Irene |
| D6 | 28/10 | S10 | Il messaggio d'errore conteneva «STOP 2» | bassa | **chiuso 28/10** | Ottavia |
| D7 | 28/10 | S12 | Un modello aperto da file poteva inserire codice HTML nella pagina | alta | **chiuso 28/10** | Irene |
| D8 | 28/10 | S4 | Deformata approssimata sulle aste con cerniere interne | bassa | **chiuso 30/10**: il solutore restituisce le rotazioni d'estremità delle aste (`rotazioni_aste`), verificate su C6 con le formule chiuse; la deformata le usa ed è esatta | Mariana, Elisa |
| D9 | 29/10 | S15 | Il clic esattamente sull'asse di un'asta non la selezionava (spigolo del prisma di selezione sul piano del telaio) | bassa | **chiuso 29/10** | Irene |
| D10 | 29/10 | — | Disegno di nodi e aste direttamente col mouse | media | **chiuso 30/10** in versione minima: spezzata di aste con aggancio alla griglia e ai nodi esistenti; sezione dell'ultima asta | Irene, Lucia |
| D11 | 30/10 | S18 | Materiali e sezioni non inseribili dall'interfaccia (revisione 14) | media | **chiuso 30/10**: E, A, I modificabili; copia di materiale e sezione per una sola asta | Lucia |
| D12 | 30/10 | S17 | Durante il disegno la vista non si adatta ai nodi aggiunti fuori dall'inquadratura (va usata la rotella o ricaricata la vista) | bassa | **chiuso 02/11**: se il nodo cade fuori dal 95 % dell'inquadratura la vista si adatta al modello; non provato in automatico, da controllare a mano | Irene |
| D14 | 31/10 | S21 | «Spostamento massimo» nel pannello dei risultati considera solo i nodi: su una trave con due soli nodi vincolati indica 0 mm, mentre la freccia in campata è 10 mm | bassa | **chiuso 02/11**: massimo sui 21 punti per asta della deformata esatta (S26) | Mariana |
| D15 | 31/10 | S21 | I carichi trapezoidali si vedono nel pannello ma non si possono inserire dall'interfaccia (solo da file) | media | **chiuso 02/11**: «+ trapezio» sull'asta selezionata e «imposta» cedimento sul nodo, solo sulle componenti vincolate; il modello passa allo schema 1.1 | Lucia, Irene, Daniela |
| D16 | 03/11 | S30 | Nel pannello proprietà i residui numerici comparivano come 0,000000000000003887 kNm | bassa | **chiuso 03/11**: valori sotto 10⁻⁹ mostrati come 0 | Lucia |
| D17 | 03/11 | — | Le distorsioni termiche si vedono nel pannello ma si inseriscono solo da file | bassa | **chiuso 04/11**: «+ ΔT» sull'asta selezionata, α e h modificabili, avviso sul lato del ΔT a farfalla | Lucia, Irene |
| D18 | 06/11 | C19 | Diagramma di grandezze nulle disegnato con etichette «0» dovute a residui di arrotondamento (10⁻¹⁴) | bassa | **chiuso 06/11**: sotto 10⁻⁶ kN o kNm il diagramma non si disegna | Mariana |
| D19 | 07/11 | modello grande | Calcolo e disegno di 4681 nodi e 9150 aste in 12,7 s con 1,2 GB di memoria | media | **ridotto il 07/11** a 4,7 s e 0,79 GB: mappa dei nodi costruita una volta, geometrie e materiali condivisi, diagrammi e deformata in un'unica geometria, al massimo 150 etichette. Restano 1,3 s di validazione dello schema nel servizio e la tabella di 9150 righe | Irene, Mariana |
| D20 | 07/11 | C5 | Frecce dei carichi uniformi e concentrati lunghe |q| volte il dovuto (introdotto il 31/10 con i trapezi) | alta (leggibilità) | **chiuso 07/11**, ricontrollato a vista | Irene |
| D21 | 09/11 | C22 | Le molle sono disegnate come un anello, simbolo poco riconoscibile; quello consueto è una molla a zig-zag | bassa | **chiuso 10/11**: zig-zag con tratto di terra per ky (sotto il nodo) e kx (a sinistra), spirale per kr; ricontrollato a vista su C8, C9 e C22 | Irene |
| D22 | 10/11 | C13, C23 | Sulle travi doppiamente incastrate la deformata non compariva: la scala usava i soli spostamenti dei nodi, che sono nulli | media | **chiuso 10/11**: la scala considera i 21 punti per asta; sotto 10⁻⁹ m la deformata non si disegna (C14, spostamenti nulli). I massimi su elenchi lunghi sono calcolati con cicli, perché `Math.max(...elenco)` falliva sul modello da 9150 aste | Mariana |
| D23 | 11/11 | S34 | Su C24 l'etichetta del momento al nodo 3 («39,4») copre la freccia della forza orizzontale del primo piano | bassa | **chiuso 12/11**: le etichette d'estremità si spostano verso l'interno dell'asta e, se cadono su un'altra etichetta, scorrono lungo la propria asta; ricontrollato a vista su C5, C24, C25 | Irene |
| D13 | 30/10 | S17 | Nel disegno non si possono annullare l'ultimo nodo o l'ultima asta (solo «Elimina» dal pannello) | bassa | **chiuso 02/11**: pulsante «Annulla» e Ctrl+Z per ogni modifica (fino a 50) | Lucia |
