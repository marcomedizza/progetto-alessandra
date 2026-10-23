# Disposizione di studio — 23/10/2026

**Disposto da**: Marco
**Regola**: chi ha materiale di studio disponibile in `progetto-alessandra/RIFERIMENTI` procede con quello. Fonte disponibilità: `RIFERIMENTI_INVENTARIO_2026-10-23.md`.

## Procedono con lo studio

| Agente | Disciplina | Materiale disponibile | Note |
|---|---|---|---|
| Roberta | Calcestruzzo armato | `CALCESTRUZZO/Leonhardt vol I, II, III.pdf` | Corrisponde all'assegnazione |
| Martina | Acciaio | `ACCIAIO/STRUTTURE DI ACCIAIO.pdf`, `Collegamenti.pdf` | L'assegnazione era Timoshenko, non presente |
| Alessia | Geotecnica | `GEOTECNICA/bowles-foundation-analysis-and-design.pdf`; `_05libro.pdf`, `_08libro.pdf` | Prima identificare se uno dei due è il Lancellotta |
| Elisa | Solutore Fortran | Bowles, capitoli sull'interazione terreno-struttura; `CALCOLO AUTOMATICO/_09libro.pdf` | `_09libro` da identificare (Monegato?) |
| Francesca | Idraulica e CFD | `IDRAULICA/Finite element techniques for fluid flow.pdf`, quaderni 1–5, `acqua.pdf`, `aria.pdf` | Manca «Computational Hydraulics» |
| Ilaria | **Prefabbricati** (nuovo incarico) | `STRUTTURE/PREFABBRICATI/Di Prisco Marco/` (dispense), `PREFABBRICATE 2/` (solai alveolari, elementi di copertura, travi), `TECNICA/` | Vedi sotto |
| Gabriella | **Energetica** (nuovo incarico) | `ENERGETICA/` Olgyay, «Design with Climate»; manuali EnergyPlus da scaricare | Vedi sotto |

## Restano senza materiale di studio

**Team strutturale**
- Sofia (alluminio): nessuna cartella
- Giulia (legno e fibre): nessuna cartella
- Chiara (muratura): nessuna cartella
- Beatrice (scienza delle costruzioni): Belluzzi assegnato ma non presente

**Team Alessandra (tech)**
- Benedetta, Irene, Natalia, Valentina, Carla, Daniela, Lucia, Mariana, Ottavia, Paola: nessun testo assegnato in RIFERIMENTI
- Renata, Silvia: mai attivate

**Team Giorgia (business)**
- Giorgia, Katia, Aurora, Livia, Veronica, Camilla, Laura: nessun testo assegnato in RIFERIMENTI

## Con compiti diversi dallo studio

- Agata: riordino di RIFERIMENTI (file senza titolo, file senza estensione, duplicati), vedi inventario
- Sole, Ginevra, Raffaella, Marisa, Vittoria: controllo qualità

## Nuovi incarichi del 23/10/2026

### Ilaria — prefabbricati
- **Scelta**: è nel team strutturale e la sua disciplina (muratura armata) non ha testi; passa a Chiara, che segue la muratura.
- **Ordine di studio**:
  1. Di Prisco: `introduzione1-2`, `concetti generali`, `tipologie1-2`, `materiali1-2`
  2. Di Prisco: `compressione`, `pressoflessione`, `verifica resistenza`, `resistenza di progetto`, `inserti1-4`, `problemi e tolleranze`
  3. `PREFABBRICATE 2`: `alveolari.th`, `alveolari.exp`, `elementi di copertura`, `trave.design`, `Calcolo sezione Giangreco`
  4. Di Prisco: `durabilità`, `resistenza al fuoco`, `fibrorinforzati`, `ottimizzazione1-11`
- **Prerequisito (Agata)**: riordinare la cartella `PREFABBRICATI` (file `it1`–`it50` senza estensione, serie `9_*.pdf` cumulative, `dwl*`): capire di quale volume fanno parte e unirli in un solo PDF.
- **Collegamenti**: Roberta (calcestruzzo armato) per i fondamenti del c.a. e del c.a.p.

### Gabriella — energetica
- **Scelta**: mai attivata (era «Norme FEM»); la sua competenza su IFC e interoperabilità è utile per lo scambio dati dei modelli energetici.
- **Studio**: Olgyay, «Design with Climate. Bioclimatic Approach to Architectural Regionalism» (1963, nuova ed. 2015). Punti chiave: diagramma bioclimatico, controllo solare e ombreggiamento, orientamento, forma dell'edificio in funzione del clima.
- **Copia del testo**: il PDF in cartella proviene da un sito di distribuzione non autorizzata (z-library). Per l'uso nel progetto va procurata una copia regolare.
- **Materiale da riordinare**: gli script `test1`–`test4` e i documenti `CHECKLIST_AVVIO_WEEK1.md` e `PROCEDURA_TEST_VALIDATION.md` in `ENERGETICA` sono prove di accoppiamento termico/OpenFOAM, non testi: Gabriella ne verifica l'origine con Francesca.
- **Ruolo di Olgyay**: concetti di base (clima, comfort, strategie bioclimatiche). Non è un testo di calcolo.
- **EnergyPlus — manuali da assimilare** (documentazione ufficiale gratuita, da scaricare dal sito energyplus.net nella sezione documentazione, nella versione corrispondente al programma installato; Agata li salva in `RIFERIMENTI/ENERGETICA/EnergyPlus/`):
  1. *EnergyPlus Essentials* e *Getting Started*: struttura del programma, flusso input → simulazione → output
  2. *Engineering Reference*: metodo del bilancio termico, conduzione con funzioni di trasferimento, radiazione solare, ventilazione e infiltrazioni. È il collegamento tra i concetti di Olgyay e il calcolo
  3. *Input Output Reference*: da usare come riferimento, partendo da parametri di simulazione, località e file climatici, materiali e costruzioni, zone termiche, carichi interni, impianti ideali
  4. *Output Details and Examples*, *Auxiliary Programs* (convertitore dei dati climatici, ExpandObjects), *Tips and Tricks*
  5. Manuali da sviluppatore:
     - *Interface Developer's Guide*: formati di input IDF ed epJSON. Priorità alta: è la via con cui il nostro programma genera i modelli energetici, e epJSON va confrontato con lo schema dati di Benedetta
     - API Python di EnergyPlus e *External Interfaces Application Guide* (co-simulazione FMI): base per gli script di accoppiamento in `ENERGETICA` (`test4_weak_coupling.py`)
     - *Module Developer's Guide*: struttura del codice sorgente C++, solo se si dovranno sviluppare moduli
  6. Guide applicative (*Application Guide for EMS*, *Plant Application Guide*): dopo i punti precedenti, se servono controlli o impianti dettagliati
- **Mancano** testi sulla normativa energetica italiana (UNI/TS 11300, D.M. 26/06/2015 requisiti minimi): da procurare se la parte energetica deve arrivare al calcolo di legge.
