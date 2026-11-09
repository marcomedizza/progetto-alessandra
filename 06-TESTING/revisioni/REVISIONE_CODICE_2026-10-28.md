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


## Aggiornamento del 02/11/2026 (Marisa)

**Punti aperti precedenti**: 13 **chiuso** (Annulla, D13); 28 **chiuso** (cedimento su molla spiegato nel README del solutore e coperto da una prova); 31 **chiuso** (D14).

**Revisione del codice nuovo del 02/11**

| # | File | Osservazione | Gravità | Esito |
|---|---|---|---|---|
| 32 | `02-FRONTEND-3D/modifica.js` | Il trapezio dal pannello è sempre verticale (`globale_y`). Per carichi normali all'asta inclinata, come vento o pressione, serve `locale_y`, che oggi si inserisce solo da file | bassa | aperto: aggiungere la scelta della direzione |
| 33 | `02-FRONTEND-3D/modifica.js` | Aggiungere un trapezio o un cedimento porta il modello a `schema_version` 1.1; togliendolo non torna a 1.0. È corretto: la 1.1 accetta anche i modelli 1.0 | — | nessun intervento |
| 34 | `02-FRONTEND-3D/app.js` | «Annulla» conserva copie complete del modello in JSON, fino a 50. Per 5000 nodi sono qualche decina di MB: accettabile, da rivedere se il limite sale | bassa | aperto, da tenere d'occhio |
| 35 | `02-FRONTEND-3D/app.js` | Ctrl+Z è ignorato quando il cursore è in un campo di testo, dove il navigatore annulla la digitazione: comportamento atteso | — | nessun intervento |
| 36 | `02-FRONTEND-3D/risultati.js` | La deformata è calcolata una volta per il disegno e una per la tabella: costo doppio trascurabile fino a migliaia di aste | — | nessun intervento |
| 37 | `02-FRONTEND-3D/vista.js` | La reinquadratura del disegno (D12) non è coperta dalle prove automatiche, perché la posizione dei clic dipende dall'inquadratura | bassa | aperto: prova a mano |

**Verifiche eseguite**:
- `verifica_casi.py` nei tre percorsi su C1–C16: superati;
- `test_app.py`: 20 prove superate;
- scenari S1–S26 nel navigatore: superati.


## Aggiornamento del 03/11/2026 (Marisa)

**Punti aperti precedenti**: 32 **chiuso**: direzione del trapezio scelta nel pannello, coperta da C17 e S27. 34 e 37 restano aperti.

**Revisione del codice nuovo del 03/11** (solutore v0.4, schema v1.2)

| # | File | Osservazione | Gravità | Esito |
|---|---|---|---|---|
| 38 | `03-BACKEND/converter/converti.py` | NT e MT sono calcolati nel convertitore, non nel solutore: il file del solutore resta senza α e h. Scelta corretta, ma il formato di tipo 4 è valido solo con quei valori precalcolati: va scritto nel README del solutore | — | fatto (README v0.4) |
| 39 | `03-BACKEND/servizio/app.py` | Il ΔT uniforme è rifiutato con deformabilità assiale trascurata (A × 10⁶ darebbe una forza fittizia enorme): il messaggio è chiaro e coperto da una prova | — | nessun intervento |
| 40 | `01-ARCHITETTURA/DATA_SCHEMA.json` | La convenzione di `dT_g` (lato −y meno lato +y) dipende dal verso dell'asta: invertendo nodo_i e nodo_j cambia il lato. Va spiegato all'utente, perché è facile sbagliare il segno | media | aperto: nota nell'interfaccia quando le distorsioni saranno inseribili (D17) |
| 41 | `04-FORTRAN-SOLVER/src/telaio2d.f90` | Con una cerniera interna la condensazione tratta correttamente anche le forze termiche, che passano dallo stesso vettore delle forze d'incastro | bassa | aperto: manca un caso di prova con cerniera e ΔT a farfalla |
| 42 | `02-FRONTEND-3D/proprieta.js` | I residui numerici erano mostrati con 16 cifre (D16) | bassa | corretto |

**Verifiche eseguite**:
- `verifica_casi.py` nei tre percorsi su C1–C18: superati;
- `test_app.py`: 22 prove superate;
- scenari S1–S30 nel navigatore: superati.


## Aggiornamento del 04/11/2026 (Marisa)

**Punti aperti precedenti**
- 40 **chiuso**: convenzione documentata in SCHEMA_DATI; il pannello indica il lato per l'asta selezionata.
- 41 **chiuso**: caso C19, condensazione delle forze termiche alla cerniera verificata.
- 34 e 37 restano aperti.

**Revisione del codice nuovo del 04/11**

| # | File | Osservazione | Gravità | Esito |
|---|---|---|---|---|
| 43 | `02-FRONTEND-3D/modifica.js` | L'aggiunta di trapezi o cedimenti portava sempre lo schema a 1.1, anche da 1.2: un modello con distorsioni termiche sarebbe stato poi rifiutato | media | corretto prima della consegna: la versione sale soltanto, da 1.0 a 1.1 |
| 44 | `02-FRONTEND-3D/modifica.js` | «Nuovo» assegna ora α = 1,2·10⁻⁵ all'acciaio e h ai due profili da sagomario (IPE 300 = 300 mm, HE 200 A = 190 mm) | — | nessun intervento |
| 45 | `02-FRONTEND-3D/proprieta.js` | Cambiare h non cancella W né la fonte del sagomario, a differenza di A e I: corretto, perché h non entra in W del sagomario | — | nessun intervento |
| 46 | `04-FORTRAN-SOLVER/prova_prestazioni.py` | Su C3 banda e piena differiscono di 1,2·10⁻¹⁰ m per il cattivo condizionamento della deformabilità assiale trascurata (A × 10⁶). Resta sotto la tolleranza, ma è un limite del metodo | bassa | aperto: valutare vincoli di inestensibilità al posto di A × 10⁶ |
| 47 | `05-RICERCA/licenze_componenti.md` | Due dubbi dichiarati: licenze delle librerie Rust incluse in rpds-py e pydantic-core; origine di opentelemetry-api | bassa | aperto |

**Verifiche eseguite**:
- `verifica_casi.py` nei tre percorsi su C1–C19: superati;
- `test_app.py`: 24 prove superate;
- scenari S1–S33 nel navigatore: superati.


## Aggiornamento del 06/11/2026 (Marisa)

Il 05/11 l'esecuzione si è interrotta per un riavvio della macchina di lavoro dopo la generazione di C20, che è stato completato e salvato oggi.

**Punti aperti precedenti**
- 34 **chiuso**: «Annulla» limitato a 50 copie e 20 milioni di caratteri, circa 14 annullamenti su un modello da 4681 nodi; restano sempre le ultime due copie.
- 46 **chiuso come studio**: il fattore 10⁶ è vicino all'ottimo, errore 6·10⁻⁹. Proposta per la v0.5: fattore relativo all'asta.
- 47 **chiuso**: licenze Rust da SBOM, opentelemetry-api richiesto da FastAPI.
- 37 resta aperto: D12 da provare a mano.

**Revisione del codice nuovo**

| # | File | Osservazione | Gravità | Esito |
|---|---|---|---|---|
| 48 | `02-FRONTEND-3D/prove_modifica.mjs` | Prima prova automatica dell'interfaccia eseguibile con node, senza navigatore: copre il punto 43 e le regole dei pannelli | — | nessun intervento |
| 49 | `02-FRONTEND-3D/risultati.js` | La soglia di 10⁻⁶ per i diagrammi nulli è assoluta (kN, kNm): adatta alle unità del progetto; con unità diverse andrebbe resa relativa | bassa | aperto, da ricordare se cambiano le unità |
| 50 | `02-FRONTEND-3D/app.js` | Il limite dell'«Annulla» conta i caratteri della stringa JSON, non i byte: in JavaScript ogni carattere occupa 2 byte, quindi 20 milioni di caratteri sono circa 40 MB | — | nessun intervento, scritto nel commento |
| 51 | `03-BACKEND/servizio/test_app.py` | La prova sugli identificativi non consecutivi copre ora anche distorsioni termiche e rotazioni alle cerniere (C14, C18, C19) | — | nessun intervento |

**Verifiche eseguite**:
- `verifica_casi.py` nei tre percorsi su C1–C20: superati;
- `test_app.py`: 26 prove superate;
- `prove_modifica.mjs`: 5 prove superate;
- scenari S1–S33 nel navigatore: superati.


## Aggiornamento del 07/11/2026 (Marisa)

**Punti aperti precedenti**
- 46 **chiuso con modifica**: fattore relativo all'asta (v0.5 del convertitore), verificato sulla scala delle luci.
- 49 **chiuso senza modifica**: le unità sono fissate dallo schema (m, kN), quindi la soglia assoluta di 10⁻⁶ kN o kNm è coerente. Una soglia relativa ai risultati fallirebbe proprio sui casi da distorsione su struttura isostatica come C19, dove tutte le grandezze sono residui di arrotondamento.
- 41: già chiuso con C19; il compito ripetuto oggi era un doppione.
- 37 resta aperto (D12 a mano).

**Revisione del codice nuovo del 07/11**

| # | File | Osservazione | Gravità | Esito |
|---|---|---|---|---|
| 52 | `03-BACKEND/converter/converti.py` | `area_di_calcolo` prende il massimo tra A e 10⁸·12I/L²: non riduce mai l'area reale, quindi un'asta tozza resta con la sua EA | — | nessun intervento |
| 53 | `02-FRONTEND-3D/vista.js` | Frecce dei carichi con lunghezza divisa per un riferimento pari a 1 (D20, dal 31/10): errore di presentazione grave, non rilevato dalle prove automatiche | alta | corretto; aggiunto il controllo a vista alla procedura di consegna |
| 54 | `02-FRONTEND-3D/risultati.js` | `geometriaAsta` ricostruiva la mappa dei nodi a ogni chiamata: costo n_aste × n_nodi (D19) | media | corretto |
| 55 | `02-FRONTEND-3D/vista.js` | Geometrie condivise e scalate: la selezione col mouse usa la geometria scalata ed è stata riprovata negli scenari S6, S9 e S17 | — | nessun intervento |
| 56 | `03-BACKEND/servizio/app.py` | La validazione con jsonschema costa 1,3 s sul modello da 9150 aste: è la parte più lenta del servizio | bassa | aperto: valutare un validatore compilato o la validazione per parti |

**Verifiche eseguite**:
- `verifica_casi.py` nei tre percorsi su C1–C20: superati;
- `test_app.py`: 27 prove superate; `prove_modifica.mjs`: 5 superate;
- scenari S1–S33 nel navigatore: superati;
- controllo a vista di C5, C7, C12, C19 e C20.


## Aggiornamento dell'08/11/2026 (Marisa)

**Punti aperti precedenti**: 56 **chiuso** con la validazione rapida; 37 resta aperto (D12 a mano).

**Revisione del codice nuovo dell'08/11**

| # | File | Osservazione | Gravità | Esito |
|---|---|---|---|---|
| 57 | `03-BACKEND/servizio/app.py` | La via rapida decide solo se il modello è valido. Se non lo è, si torna a jsonschema per i messaggi, quindi l'utente vede gli stessi errori di prima. Concordanza provata su 120 modelli e in una prova del servizio | — | nessun intervento |
| 58 | `03-BACKEND/servizio/app.py` | Se due validatori discordassero su un modello valido per jsonschema e non per la via rapida, la risposta conterrebbe un elenco di errori vuoto ma non validato. Va escluso con un controllo | bassa | aperto: se la via rapida dice «non valido» e jsonschema non trova errori, accettare il modello e registrare l'anomalia |
| 59 | `03-BACKEND/servizio/requirements.txt` | Primo file dei requisiti con versioni fissate: risolve l'indicazione di Veronica del 02/11 | — | nessun intervento |

**Verifiche eseguite**:
- `verifica_casi.py` nei tre percorsi su C1–C21: superati;
- `test_app.py`: 29 superate; `prove_modifica.mjs`: 5 superate;
- scenari S1–S33 e controllo a vista di 5 casi.


## Aggiornamento del 09/11/2026 (Marisa)

**Punti aperti precedenti**: 58 **chiuso**. Se la via rapida rifiuta e jsonschema non trova errori, fa fede jsonschema: il modello è accettato e la discordanza è registrata nel log e in `ANOMALIE_VALIDAZIONE`; c'è una prova con una via rapida simulata. Il punto 37 resta aperto (D12 a mano).

**Revisione del codice nuovo del 09/11**

| # | File | Osservazione | Gravità | Esito |
|---|---|---|---|---|
| 60 | `03-BACKEND/servizio/app.py` | `ANOMALIE_VALIDAZIONE` è una lista in memoria: si azzera al riavvio e cresce senza limite in un servizio sempre acceso | bassa | aperto: tenere solo le ultime 100 voci o affidarsi al solo log |
| 61 | `03-BACKEND/servizio/test_app.py` | La prova degli identificativi non consecutivi rinumera ora anche carichi d'asta e cedimenti: copre C20 e C21 | — | nessun intervento |

**Verifiche eseguite**:
- `verifica_casi.py` nei tre percorsi su C1–C22: superati;
- `test_app.py`: 30 prove; `prove_modifica.mjs`: 5;
- scenari S1–S33 e controllo a vista di 6 casi.
