# Assegnazione compiti — dal 23/10/2026, ore 12:00

**Disposto da**: Marco
**Validità**: dal 23/10/2026 al 30/10/2026, sette giorni su sette (gli agenti virtuali non hanno fine settimana), con rapporto ogni giorno
**Calendario compresso il 23/10 ore 12:00**: le scadenze iniziali seguivano il calendario lavorativo umano; restano sui giorni feriali solo le verifiche di Marco
**Sostituisce**: il programma di formazione 26/08–24/10, che si chiude con questa assegnazione. La valutazione finale del 24/10 diventa la prima verifica delle consegne di sabato 24/10.

## Regole comuni

1. Tutti iniziano da subito. Nessun agente resta senza compito.
2. **Rapporto giornaliero obbligatorio**, ogni giorno entro le 18:00, sabato e domenica compresi, nel file `RAPPORTI/AAAA-MM-GG/<Nome>.md` con: cosa è stato fatto, cosa è stato letto (capitoli e pagine), problemi, cosa si fa la settimana dopo. Un rapporto mancante è un compito non svolto.
3. Chi studia consegna anche una **sintesi tecnica** di ogni capitolo letto: formule principali, ipotesi, campo di validità, un esempio numerico.
4. I testi si chiedono ad Agata. Se un testo manca, lo si segnala nel rapporto e si passa al successivo dell'elenco.
5. Il codice va nel repository GitHub, nelle cartelle previste dal README (`01-ARCHITETTURA/` … `06-TESTING/`).

## Scadenze comuni

| Data | Traguardo | Responsabile della verifica |
|---|---|---|
| ven 23/10, 18:00 | RIFERIMENTI riordinata; NTC 2018, Circolare 2019 e manuali EnergyPlus scaricati; primo rapporto di tutti | Agata → Raffaella; Sole |
| sab 24/10, 18:00 | Schema dati v1.0; casi di prova con soluzione nota; prime sintesi di studio | Sole |
| mer 28/10, 18:00 | Prototipo minimo: portale 2D in JSON → solutore Fortran → risultati → vista 3D | Alessandra, Valentina |
| ven 30/10 | Revisione: prototipo funzionante sui casi di prova; sintesi di studio consegnate | Marco |

## Team strutturale (resp. Roberta) — studio

| Agente | Compito | Materiale |
|---|---|---|
| Roberta | Studio Leonhardt vol. I–III. Coordina il team e raccoglie i rapporti giornalieri | `RIFERIMENTI/CALCESTRUZZO` |
| Martina | Studio acciaio: «Strutture di acciaio», poi «Collegamenti» | `RIFERIMENTI/ACCIAIO` |
| Alessia | Identificare `_05libro` e `_08libro` (Lancellotta?). Studio Bowles completo, poi Lancellotta cap. 8–11 | `RIFERIMENTI/GEOTECNICA` |
| Ilaria | Studio prefabbricati, nell'ordine indicato in `DISPOSIZIONE_STUDIO_2026-10-23.md` | `RIFERIMENTI/STRUTTURE/PREFABBRICATI` |
| Beatrice | Studio Zienkiewicz (metodo degli elementi finiti) in attesa del Belluzzi. Supporto teorico a tutti, risposte entro 2 ore | `RIFERIMENTI/TEORIA` |
| Chiara | Muratura ordinaria e armata: NTC 2018 §4.5 e §7.8 con la Circolare 2019. Elenco dei testi di muratura da procurare | NTC 2018 (da Agata) |
| Giulia | Legno: NTC 2018 §4.4 e §7.7 con la Circolare 2019. Elenco dei testi di legno e rinforzi FRP da procurare | NTC 2018 (da Agata) |
| Sofia | Alluminio: le NTC 2018 non hanno un capitolo dedicato e rimandano agli Eurocodici. Raccogliere i riferimenti normativi (UNI EN 1999-1-1) e l'elenco dei testi da procurare. Nel frattempo studia «Collegamenti» con Martina | `RIFERIMENTI/ACCIAIO` |

## Team Alessandra (resp. Alessandra, tecnico Elisa) — ripresa dello sviluppo

Obiettivo: il prototipo minimo di mercoledì 28/10, sul portale 2D di `ESEMPIO_PORTALE_2D.json`.

| Agente | Compito | Consegna |
|---|---|---|
| Benedetta | Completare lo schema dati da «DRAFT_v1» a v1.0: nodi, aste, sezioni, materiali, vincoli, carichi, risultati. Confronto con epJSON di EnergyPlus insieme a Gabriella | 24/10 `01-ARCHITETTURA/DATA_SCHEMA.json` |
| Elisa | Solutore Fortran per telaio piano, statica lineare (matrice di rigidezza, assemblaggio, vincoli, soluzione con LAPACK). In parallelo: Bowles, capitoli sull'interazione terreno-struttura | 28/10 `04-FORTRAN-SOLVER/` |
| Ottavia | Compilazione gfortran del solutore e chiamata da Python | 28/10 `04-FORTRAN-SOLVER/build` |
| Paola | Convertitore JSON (schema v1.0) → file di input del solutore, e risultati del solutore → JSON | 28/10 `03-BACKEND/converter` |
| Natalia | Servizio FastAPI minimo: carica il modello, lo valida con lo schema, avvia il calcolo, restituisce i risultati | 28/10 `03-BACKEND/` |
| Irene | Vista 3D con Three.js: disegna nodi e aste dal JSON, viste dall'alto, frontale, laterale e assonometrica | 28/10 `02-FRONTEND-3D/` |
| Lucia | Pannello proprietà: mostra e modifica sezione, materiale, vincoli e carichi dell'elemento selezionato | 28/10 `02-FRONTEND-3D/` |
| Mariana | Visualizzazione risultati: deformata e diagrammi di momento e taglio sulla vista di Irene | 28/10 `02-FRONTEND-3D/` |
| Valentina | Casi di prova con soluzione nota: trave appoggiata, mensola, portale incastrato, telaio a due piani, con risultati calcolati a mano | 24/10 `06-TESTING/casi/` |
| Silvia | Confronto automatico dei risultati del solutore con i casi di Valentina (tolleranze, rapporto) | 28/10 `06-TESTING/` |
| Renata | Prova del flusso completo dal punto di vista dell'utente: disegno, calcolo, lettura dei risultati. Lista dei difetti | 28/10 `06-TESTING/flusso.md` |
| Francesca | Studio idraulica (Connor-Brebbia, quaderni 1–5). Verifica con Gabriella degli script OpenFOAM in `ENERGETICA` | 24/10 sintesi |
| Gabriella | Energetica: Olgyay per i concetti di base, poi i manuali EnergyPlus nell'ordine della disposizione; priorità all'Interface Developer's Guide (IDF/epJSON) | 24/10 sintesi Olgyay; 30/10 sintesi Engineering Reference |
| Carla | ModeSt: formati di importazione accettati (DXF, IFC, testo). Proposta del formato di esportazione dal nostro schema | 30/10 `05-RICERCA/modest.md` |
| Daniela | Con Carla: analisi dei file di esempio ModeSt, corrispondenza delle grandezze con lo schema v1.0 | 30/10 `05-RICERCA/modest.md` |

## Team Giorgia (resp. Giorgia) — attività di supporto al progetto

| Agente | Compito | Consegna |
|---|---|---|
| Giorgia | Coordina il team business e prepara il resoconto giornaliero per Marco | ogni giorno, 18:30 |
| Katia | Analisi dei programmi concorrenti per piccoli studi (calcolo strutturale ed energetico): funzioni, prezzi, punti deboli | 30/10 |
| Aurora | Ipotesi di modello di prezzo e costi di sviluppo (ore per agente, licenze software) | 30/10 |
| Livia | Comunicazione interna: raccoglie i rapporti giornalieri e li pubblica nella bacheca del cruscotto | ogni giorno, 18:30 |
| Veronica | Licenze dei componenti: EnergyPlus (BSD), OpenFOAM (GPL), LAPACK (BSD), Three.js (MIT); compatibilità con la distribuzione del nostro programma | 24/10 |
| Camilla | Rassegna su aggiornamenti normativi (NTC, Eurocodici di seconda generazione, requisiti energetici) | 25/10, poi ogni domenica |
| Laura | Controllo avanzamento: aggiorna il cruscotto con i rapporti del giorno e segnala i ritardi | ogni giorno, 19:00 |

## Biblioteca e controllo qualità

| Agente | Compito | Consegna |
|---|---|---|
| Agata | Riordinare RIFERIMENTI (vedi inventario): titoli dei file `_0Xlibro`, cartella PREFABBRICATI, duplicati. Scaricare NTC 2018, Circolare 2019 e manuali EnergyPlus. Consegnare i testi su richiesta | 23/10, 18:00 |
| Sole | Verifica dei rapporti e delle consegne; segnala a Marco chi non consegna | ogni giorno, 19:00 |
| Ginevra | Verifica del team strutturale: qualità delle sintesi tecniche | ogni giorno |
| Raffaella | Verifica del team business e del lavoro di Agata | ogni giorno |
| Marisa | Revisione del codice del team tech prima dell'inserimento nel repository | continua |
| Vittoria | Esecuzione delle prove di Valentina e Silvia sul prototipo | dal 28/10 |
