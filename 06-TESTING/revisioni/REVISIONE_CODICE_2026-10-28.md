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
