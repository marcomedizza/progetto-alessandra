# Prova del flusso utente — prototipo del 28/10/2026

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

Nessun errore nella console. Firefox non provato (non disponibile nell'ambiente automatico): da fare a mano.

## Difetti

| N. | Data | Scenario | Descrizione | Gravità | Stato | Assegnata a |
|---|---|---|---|---|---|---|
| D1 | 27/10 | S4 | Deformata interpolata solo dagli spostamenti nodali | bassa | **chiuso 28/10**: aggiunta l'inflessione dei carichi d'asta, esatta per aste senza cerniere (verificata su C1 e C7) | Mariana |
| D2 | 27/10 | S2 | Combinazioni di carico non calcolate | media | **chiuso 28/10**: sovrapposizione lineare nel servizio e scelta della combinazione nell'interfaccia | Natalia, Benedetta |
| D3 | 27/10 | S1 | Nessun valore numerico sui diagrammi | bassa | aperto | Mariana |
| D4 | 27/10 | — | Non si possono disegnare nodi e aste nuovi | alta per la versione alfa | aperto | Lucia, Irene |
| D5 | 28/10 | S9 | Nodi difficili da selezionare col mouse | bassa | **chiuso 28/10** | Irene |
| D6 | 28/10 | S10 | Il messaggio d'errore conteneva «STOP 2» | bassa | **chiuso 28/10** | Ottavia |
| D7 | 28/10 | S12 | Un modello aperto da file poteva inserire codice HTML nella pagina | alta | **chiuso 28/10** | Irene |
| D8 | 28/10 | S4 | Deformata approssimata sulle aste con cerniere interne | bassa | aperto | Mariana, Elisa |
