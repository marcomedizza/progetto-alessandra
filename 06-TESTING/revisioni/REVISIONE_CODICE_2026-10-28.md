# Revisione del codice — 28/10/2026

**Revisora**: Marisa (qualità tech) · **Oggetto**: codice del prototipo (commit fino a cd45432 più le correzioni di oggi)

| # | File | Problema | Gravità | Esito |
|---|---|---|---|---|
| 1 | `06-TESTING/casi/verifica_casi.py` | Il confronto completo Fortran/riferimento abbinava i risultati per posizione: con nodi non numerati in ordine (C9) segnalava 9 scostamenti inesistenti | media | **corretto oggi**: confronto per identificativo |
| 2 | `04-FORTRAN-SOLVER/src/telaio2d.f90` | Un carico riferito a un'asta inesistente veniva ignorato senza avviso; nessun controllo su identificativi duplicati | media | **corretto oggi**: errore esplicito |
| 3 | `04-FORTRAN-SOLVER/esegui.py` | Il messaggio d'errore mostrato all'utente conteneva «STOP 2» e il prefisso interno | bassa | **corretto oggi** |
| 4 | `02-FRONTEND-3D/app.js` | Nomi di casi e modelli inseriti nella pagina senza protezione: un modello aperto da file poteva iniettare codice HTML | alta | **corretto oggi**: testi protetti |
| 5 | `02-FRONTEND-3D/vista.js` | Nodi difficili da selezionare col mouse (sfera di pochi pixel) | bassa | **corretto oggi**: area di selezione più ampia |
| 6 | `04-FORTRAN-SOLVER/src/telaio2d.f90` | Matrice piena ed eliminazione di Gauss: memoria e tempo crescono con il cubo dei gradi di libertà. Adeguato per il prototipo, non per modelli reali (oltre qualche centinaio di nodi) | media | aperto: matrice a banda o LAPACK (Elisa) |
| 7 | `04-FORTRAN-SOLVER/src/telaio2d.f90` | L'uscita segue l'ordine di ingresso dei nodi; il riferimento Python li ordina per identificativo. Chi legge i risultati deve usare gli identificativi | bassa | aperto, documentato |
| 8 | `03-BACKEND/converter/converti.py` | La deformabilità assiale trascurata si ottiene moltiplicando l'area per 10⁶: funziona ma peggiora il condizionamento (scarti dell'ordine di 10⁻⁹ kN sulle somme delle reazioni) | bassa | aperto: vincolo cinematico esatto nella versione successiva |
| 9 | `04-FORTRAN-SOLVER/build.sh` | Compilazione unica con controllo dei limiti degli array: utile in prova, rallenta l'uso reale | bassa | aperto: due configurazioni (prova e rilascio) |
| 10 | `03-BACKEND/servizio/app.py` | Nessun limite alla dimensione del modello ricevuto | media | aperto: limite di nodi e aste prima della messa in rete |
| 11 | `02-FRONTEND-3D/risultati.js` | Deformata lungo le aste con cerniere interne ancora approssimata (rotazione di estremità non restituita dal solutore) | bassa | aperto (Mariana, Elisa) |

**Verifiche eseguite dopo le correzioni**: `verifica_casi.py` (riferimento, `--fortran`, `--api`) su C1–C9 superati; `test_app.py` 9 prove superate; scenari S1–S13 superati nel navigatore.


## Aggiornamento del 29/10/2026 (Marisa)

**Stato dei punti aperti del 28/10**

| # | Stato al 29/10 |
|---|---|
| 6 | aperto, ma misurato: 1989 gdl in 0,23 s (`04-FORTRAN-SOLVER/prova_prestazioni.py`). Il servizio ora rifiuta modelli oltre 1000 nodi o 3000 aste |
| 7 | aperto, documentato: verifiche, servizio e interfaccia leggono i risultati per identificativo |
| 8 | aperto |
| 9 | aperto |
| 10 | **chiuso**: limite di dimensione nel servizio, con prova |
| 11 | aperto (D8) |

**Revisione del codice nuovo del 29/10**

| # | File | Osservazione | Gravità | Esito |
|---|---|---|---|---|
| 12 | `02-FRONTEND-3D/vista.js` | Il prisma di selezione delle aste aveva uno spigolo sul piano del telaio: il clic esattamente sull'asse non selezionava l'asta | bassa | corretto (rotazione di 30°) |
| 13 | `02-FRONTEND-3D/modifica.js` | L'eliminazione di un nodo elimina anche aste, vincoli e carichi collegati: corretto, ma non c'è annullamento | bassa | aperto: aggiungere «Annulla» |
| 14 | `02-FRONTEND-3D/modifica.js` | Il nuovo modello usa un solo materiale (S275) e due profili: per modelli reali serve l'inserimento di materiali e sezioni | media | aperto |
| 15 | `02-FRONTEND-3D/risultati.js` | Etichette di M in valore assoluto e di N, V con segno: scelta coerente con la pratica (diagramma dal lato teso) | — | nessun intervento |
| 16 | `06-TESTING/casi/verifica_casi.py` | Gestisce ora anche le combinazioni (C10) in tutti e tre i percorsi | — | nessun intervento |
| 17 | `03-BACKEND/servizio/app.py` | Il limite di dimensione è nel controllo di coerenza: il messaggio arriva sia da /api/valida sia da /api/calcola | — | nessun intervento |


## Aggiornamento del 30/10/2026 (Marisa)

**Stato dei punti aperti**

| # | Stato al 30/10 |
|---|---|
| 6 | **chiuso**: Cholesky a banda (solutore v0.2), confrontato con la matrice piena fino a 1989 gdl (scarto ≤ 2,4·10⁻¹²); limite del servizio portato a 5000 nodi e 10 000 aste |
| 7 | aperto, documentato |
| 8 | aperto |
| 9 | aperto |
| 11 | **chiuso** (D8): rotazioni d'estremità restituite dal solutore e usate nella deformata |
| 13 | aperto: nessun «Annulla», ora anche per il disegno col mouse (D13) |
| 14 | **chiuso** (D11): E, A, I modificabili e copia di materiale e sezione |

**Revisione del codice nuovo del 30/10**

| # | File | Osservazione | Gravità | Esito |
|---|---|---|---|---|
| 18 | `04-FORTRAN-SOLVER/src/telaio2d.f90` | La semibanda dipende dall'ordine dei nodi. Un modello disegnato a mano, con nodi aggiunti in coda e collegati ai primi, porta la banda vicino al numero totale di gdl: con 5000 nodi sarebbero circa 1,8 GB | alta | corretto lo stesso giorno: riordino di Cuthill-McKee inverso nel convertitore (semibanda da 6203 a 71 sul telaio di prova) e limite di 5·10⁷ termini nel solutore, con messaggio leggibile; due prove nuove |
| 19 | `04-FORTRAN-SOLVER/src/telaio2d.f90` | Soglia di labilità relativa al massimo termine diagonale (10⁻¹²). Con molle molto cedevoli accanto ad aste con deformabilità assiale trascurata (A × 10⁶) il rapporto tra i termini può avvicinarsi alla soglia e dare un falso «labile» | bassa | aperto: aggiungere un caso di prova con molla di 1 kN/m e aste assialmente rigide |
| 20 | `04-FORTRAN-SOLVER/src/telaio2d.f90` | Rotazioni alle cerniere ricavate dall'asta non condensata con momento d'estremità nullo; con due cerniere sulla stessa asta si risolve un sistema 2 × 2 (biella) | — | verificato su C6 con le formule chiuse e su C9 con il riferimento |
| 21 | `02-FRONTEND-3D/app.js` | Il disegno assegna alla nuova asta la sezione dell'ultima asta e il primo materiale del modello, senza dirlo | bassa | aperto: mostrare sezione e materiale nel messaggio di disegno |
| 22 | `02-FRONTEND-3D/vista.js` | La vista si reinquadra solo cambiando vista; durante il disegno i nodi fuori dall'inquadratura restano invisibili (D12) | bassa | aperto |
| 23 | `02-FRONTEND-3D/proprieta.js` | Cambiare A o I di una sezione da sagomario toglie W e la fonte: corretto, perché W non sarebbe più coerente. Il pannello indica quante aste usano la sezione | — | nessun intervento |
| 24 | `01-ARCHITETTURA/DATA_SCHEMA.json` | Campo facoltativo `rotazioni_aste` aggiunto ai risultati senza cambiare versione: compatibile, perché è un'uscita facoltativa | — | nessun intervento, motivato in SCHEMA_DATI_v1.0.md |

**Verifiche eseguite**:
- `verifica_casi.py` nei tre percorsi su C1–C10: superati;
- `test_app.py`: 16 prove superate;
- scenari S1–S19 nel navigatore: superati.


## Aggiornamento del 31/10/2026 (Marisa)

**Revisione del codice nuovo del 31/10** (solutore v0.3, schema v1.1)

| # | File | Osservazione | Gravità | Esito |
|---|---|---|---|---|
| 25 | `04-FORTRAN-SOLVER/src/telaio2d.f90` | Forze d'incastro del trapezio con Gauss a 3 punti: l'integrando è di quarto grado (funzione di forma cubica per carico lineare) e la regola è esatta fino al quinto | — | verificato su C13 (formule tabellate) e con il modello di controllo a 60 aste |
| 26 | `04-FORTRAN-SOLVER/src/telaio2d.f90` | Cedimenti portati a secondo membro asta per asta (kg·u impresso), senza conservare la matrice completa; le reazioni includono l'effetto del cedimento | — | verificato su C11 |
| 27 | `04-FORTRAN-SOLVER/src/telaio2d.f90` | Una riga dei carichi d'asta è letta in un buffer di 1024 caratteri: sufficiente per 8 numeri in notazione esponenziale | — | nessun intervento |
| 28 | `04-FORTRAN-SOLVER/src/telaio2d.f90` | Cedimento su una molla rifiutato («grado di libertà non vincolato»): corretto, perché la molla ha già uno spostamento incognito; da spiegare nel manuale | bassa | aperto: documentazione |
| 29 | `03-BACKEND/servizio/app.py` | Le regole della v1.1 sono nel controllo di coerenza: versione, componenti vincolate, trapezio dentro l'asta. Un modello v1.0 con questi campi è rifiutato con un messaggio chiaro | — | nessun intervento |
| 30 | `02-FRONTEND-3D/risultati.js` | Deformata dei trapezi: integrale della funzione di Green diviso nel punto angoloso | — | verificato: scarto ≤ 4·10⁻¹³ m |
| 31 | `02-FRONTEND-3D/risultati.js` | «Spostamento massimo» calcolato sui soli nodi (D14) | bassa | aperto |

**Verifiche eseguite**:
- `verifica_casi.py` nei tre percorsi su C1–C13: superati;
- `test_app.py`: 18 prove superate;
- scenari S1–S22 nel navigatore: superati.
