# Assegnazione compiti — dal 23/10/2026, ore 12:00

**Disposto da**: Marco
**Validità**: dal 23/10/2026 al 13/11/2026 (tre settimane), con revisione ogni venerdì
**Sostituisce**: il programma di formazione 26/08–24/10, che si chiude con questa assegnazione. La valutazione finale del 24/10 diventa la prima revisione del 30/10.

## Regole comuni

1. Tutti iniziano da subito. Nessun agente resta senza compito.
2. **Rapporto settimanale obbligatorio**, ogni venerdì entro le 17:00, nel file `RAPPORTI/AAAA-MM-GG/<Nome>.md` con: cosa è stato fatto, cosa è stato letto (capitoli e pagine), problemi, cosa si fa la settimana dopo. Un rapporto mancante è un compito non svolto.
3. Chi studia consegna anche una **sintesi tecnica** di ogni capitolo letto: formule principali, ipotesi, campo di validità, un esempio numerico.
4. I testi si chiedono ad Agata. Se un testo manca, lo si segnala nel rapporto e si passa al successivo dell'elenco.
5. Il codice va nel repository GitHub, nelle cartelle previste dal README (`01-ARCHITETTURA/` … `06-TESTING/`).

## Scadenze comuni

| Data | Traguardo | Responsabile della verifica |
|---|---|---|
| mar 27/10 | RIFERIMENTI riordinata; NTC 2018, Circolare 2019 e manuali EnergyPlus scaricati | Agata → Raffaella |
| ven 30/10 | Primo rapporto di tutti; schema dati v1.0; casi di prova con soluzione nota | Sole |
| ven 06/11 | Prototipo minimo: portale 2D in JSON → solutore Fortran → risultati → vista 3D | Alessandra, Valentina |
| ven 13/11 | Revisione: prototipo funzionante sui casi di prova; sintesi di studio consegnate | Marco |

## Team strutturale (resp. Roberta) — studio

| Agente | Compito | Materiale |
|---|---|---|
| Roberta | Studio Leonhardt vol. I–III. Coordina il team e raccoglie i rapporti del venerdì | `RIFERIMENTI/CALCESTRUZZO` |
| Martina | Studio acciaio: «Strutture di acciaio», poi «Collegamenti» | `RIFERIMENTI/ACCIAIO` |
| Alessia | Identificare `_05libro` e `_08libro` (Lancellotta?). Studio Bowles completo, poi Lancellotta cap. 8–11 | `RIFERIMENTI/GEOTECNICA` |
| Ilaria | Studio prefabbricati, nell'ordine indicato in `DISPOSIZIONE_STUDIO_2026-10-23.md` | `RIFERIMENTI/STRUTTURE/PREFABBRICATI` |
| Beatrice | Studio Zienkiewicz (metodo degli elementi finiti) in attesa del Belluzzi. Supporto teorico a tutti, risposte entro 2 ore | `RIFERIMENTI/TEORIA` |
| Chiara | Muratura ordinaria e armata: NTC 2018 §4.5 e §7.8 con la Circolare 2019. Elenco dei testi di muratura da procurare | NTC 2018 (da Agata) |
| Giulia | Legno: NTC 2018 §4.4 e §7.7 con la Circolare 2019. Elenco dei testi di legno e rinforzi FRP da procurare | NTC 2018 (da Agata) |
| Sofia | Alluminio: le NTC 2018 non hanno un capitolo dedicato e rimandano agli Eurocodici. Raccogliere i riferimenti normativi (UNI EN 1999-1-1) e l'elenco dei testi da procurare. Nel frattempo studia «Collegamenti» con Martina | `RIFERIMENTI/ACCIAIO` |

## Team Alessandra (resp. Alessandra, tecnico Elisa) — ripresa dello sviluppo

Obiettivo: il prototipo minimo del 06/11, sul portale 2D di `ESEMPIO_PORTALE_2D.json`.

| Agente | Compito | Consegna |
|---|---|---|
| Benedetta | Completare lo schema dati da «DRAFT_v1» a v1.0: nodi, aste, sezioni, materiali, vincoli, carichi, risultati. Confronto con epJSON di EnergyPlus insieme a Gabriella | 30/10 `01-ARCHITETTURA/DATA_SCHEMA.json` |
| Elisa | Solutore Fortran per telaio piano, statica lineare (matrice di rigidezza, assemblaggio, vincoli, soluzione con LAPACK). In parallelo: Bowles, capitoli sull'interazione terreno-struttura | 06/11 `04-FORTRAN-SOLVER/` |
| Ottavia | Compilazione gfortran del solutore e chiamata da Python | 06/11 `04-FORTRAN-SOLVER/build` |
| Paola | Convertitore JSON (schema v1.0) → file di input del solutore, e risultati del solutore → JSON | 06/11 `03-BACKEND/converter` |
| Natalia | Servizio FastAPI minimo: carica il modello, lo valida con lo schema, avvia il calcolo, restituisce i risultati | 06/11 `03-BACKEND/` |
| Irene | Vista 3D con Three.js: disegna nodi e aste dal JSON, viste dall'alto, frontale, laterale e assonometrica | 06/11 `02-FRONTEND-3D/` |
| Lucia | Pannello proprietà: mostra e modifica sezione, materiale, vincoli e carichi dell'elemento selezionato | 06/11 `02-FRONTEND-3D/` |
| Mariana | Visualizzazione risultati: deformata e diagrammi di momento e taglio sulla vista di Irene | 06/11 `02-FRONTEND-3D/` |
| Valentina | Casi di prova con soluzione nota: trave appoggiata, mensola, portale incastrato, telaio a due piani, con risultati calcolati a mano | 30/10 `06-TESTING/casi/` |
| Silvia | Confronto automatico dei risultati del solutore con i casi di Valentina (tolleranze, rapporto) | 06/11 `06-TESTING/` |
| Renata | Prova del flusso completo dal punto di vista dell'utente: disegno, calcolo, lettura dei risultati. Lista dei difetti | 06/11 `06-TESTING/flusso.md` |
| Francesca | Studio idraulica (Connor-Brebbia, quaderni 1–5). Verifica con Gabriella degli script OpenFOAM in `ENERGETICA` | 30/10 sintesi |
| Gabriella | Energetica: Olgyay per i concetti di base, poi i manuali EnergyPlus nell'ordine della disposizione; priorità all'Interface Developer's Guide (IDF/epJSON) | 30/10 sintesi Olgyay; 13/11 sintesi Engineering Reference |
| Carla | ModeSt: formati di importazione accettati (DXF, IFC, testo). Proposta del formato di esportazione dal nostro schema | 06/11 `05-RICERCA/modest.md` |
| Daniela | Con Carla: analisi dei file di esempio ModeSt, corrispondenza delle grandezze con lo schema v1.0 | 06/11 `05-RICERCA/modest.md` |

## Team Giorgia (resp. Giorgia) — attività di supporto al progetto

| Agente | Compito | Consegna |
|---|---|---|
| Giorgia | Coordina il team business e prepara il resoconto settimanale per Marco | ogni venerdì |
| Katia | Analisi dei programmi concorrenti per piccoli studi (calcolo strutturale ed energetico): funzioni, prezzi, punti deboli | 06/11 |
| Aurora | Ipotesi di modello di prezzo e costi di sviluppo (ore per agente, licenze software) | 13/11 |
| Livia | Comunicazione interna: raccoglie i rapporti del venerdì e li pubblica nella bacheca del cruscotto | ogni venerdì |
| Veronica | Licenze dei componenti: EnergyPlus (BSD), OpenFOAM (GPL), LAPACK (BSD), Three.js (MIT); compatibilità con la distribuzione del nostro programma | 30/10 |
| Camilla | Rassegna settimanale su aggiornamenti normativi (NTC, Eurocodici di seconda generazione, requisiti energetici) | ogni venerdì |
| Laura | Controllo avanzamento: aggiorna il cruscotto con i rapporti del venerdì e segnala i ritardi entro il lunedì | ogni lunedì |

## Biblioteca e controllo qualità

| Agente | Compito | Consegna |
|---|---|---|
| Agata | Riordinare RIFERIMENTI (vedi inventario): titoli dei file `_0Xlibro`, cartella PREFABBRICATI, duplicati. Scaricare NTC 2018, Circolare 2019 e manuali EnergyPlus. Consegnare i testi su richiesta | 27/10 |
| Sole | Verifica dei rapporti del venerdì e delle consegne; segnala a Marco chi non consegna | ogni venerdì |
| Ginevra | Verifica del team strutturale: qualità delle sintesi tecniche | ogni venerdì |
| Raffaella | Verifica del team business e del lavoro di Agata | ogni venerdì |
| Marisa | Revisione del codice del team tech prima dell'inserimento nel repository | continua |
| Vittoria | Esecuzione delle prove di Valentina e Silvia sul prototipo | dal 06/11 |
