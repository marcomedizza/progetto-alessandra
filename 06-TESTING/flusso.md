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

## Esito della prima esecuzione (27/10/2026, navigatore Chromium automatico)

S1, S2, S3, S5, S6 e S11 eseguiti: superati, nessun errore nella console. Gli altri scenari vanno eseguiti a mano durante la prova del 28/10.

## Difetti

| N. | Data | Scenario | Descrizione | Gravità (alta / media / bassa) | Stato | Assegnata a |
|---|---|---|---|---|---|---|
| D1 | 27/10 | S4 | La deformata è interpolata con le funzioni di Hermite dai soli spostamenti nodali: lungo le aste caricate è approssimata | bassa | aperto | Mariana |
| D2 | 27/10 | S2 | Le combinazioni di carico descritte nello schema non sono ancora calcolate | media | aperto | Natalia, Benedetta |
| D3 | 27/10 | S1 | Nessun valore numerico sui diagrammi: si leggono solo nel pannello | bassa | aperto | Mariana |
| D4 | 27/10 | — | Non si possono ancora disegnare nodi e aste nuovi: si modificano solo modelli esistenti | alta per la versione alfa | aperto | Lucia, Irene |
