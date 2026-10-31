# Schema dati v1.0 — telaio piano

**File**: `01-ARCHITETTURA/DATA_SCHEMA.json` (JSON Schema 2020-12)
**Data**: 26/10/2026 · **Stato**: v1.0, sostituisce la bozza `SCHEMA_DATI_ALESSANDRA.json` «DRAFT_v1» del 18/08
**Ambito**: telai piani, analisi statica lineare. È il formato comune a interfaccia 3D, servizi, convertitore e solutore Fortran per il prototipo del 28/10.

## Convenzioni

| Tema | Scelta |
|---|---|
| Unità | Fisse e coerenti: m, kN, kN/m² (moduli elastici), kNm. Nessuna conversione dentro il modello |
| Riferimento globale | X verso destra, Y verso l'alto, rotazioni positive antiorarie |
| Riferimento locale | x dal nodo_i al nodo_j, y ruotato di +90° |
| Sforzo normale N | positivo di trazione |
| Momento M | positivo se tende le fibre dal lato −y locale (fibre inferiori di un'asta orizzontale con nodo_i a sinistra) |
| Taglio V | V = dM/dx |
| Vincoli | `ux`, `uy`, `rz` = true se il movimento è impedito; molle con `kx`, `ky`, `kr` |
| Cerniere interne | `svincoli.rz_i`, `svincoli.rz_j` sull'asta |
| Carichi d'asta | uniforme o concentrato, direzione `globale_x`, `globale_y` o `locale_y`; valori per unità di lunghezza dell'asta |
| Categorie dei carichi | G1, G2, Q, vento, neve, sisma, temperatura (NTC 2018 §2.5) |
| Risultati | spostamenti nodali, reazioni, N-V-M in `punti_diagramma` punti per asta |

## Differenze dalla bozza di agosto

- **Ambito ridotto**: solo telaio piano statico. Le parti 3D, la dinamica, il P-Delta e l'interfaccia binaria Fortran tornano nelle versioni successive. La bozza le descriveva, ma senza definirle in modo verificabile.
- **Formato validabile**: la bozza descriveva i campi a parole («float (Pa)») e non poteva validare un modello. La v1.0 è un JSON Schema: ogni modello si controlla automaticamente.
- **Unità**: la bozza mescolava kN e MPa nel progetto con moduli in Pa nei materiali. La v1.0 fissa un solo sistema coerente.
- **Nomi dei campi in italiano**, coerenti con la documentazione del progetto.

## Errori trovati nella bozza

- **HEA 200**: nell'esempio `ESEMPIO_PORTALE_2D.json` aveva Iy = 1,25·10⁻⁵ m⁴ e Iz = 3,69·10⁻⁶ m⁴. Il valore corretto sull'asse forte è Iy ≈ 3692 cm⁴ = 3,692·10⁻⁵ m⁴ (Iz ≈ 1336 cm⁴). Anche gli spessori indicati non corrispondono al profilo.
- **Risultati attesi dell'esempio**: indicati come intervalli («~50-100 kNm»), non utilizzabili come prova. Sostituiti dai casi di `06-TESTING/casi/`.

## Esempi

I cinque modelli in `06-TESTING/casi/` sono validi secondo questo schema. Il portale del prototipo è `C4_portale_carico_uniforme.json`.

## Esempio di riferimento

`ESEMPIO_PORTALE_2D.json` (27/10/2026): portale incastrato con due casi di carico (G2 sul traverso con peso proprio, vento) e una combinazione SLU 1,3·G2 + 1,5·W. Sostituisce l'esempio della bozza di agosto ed è valido secondo lo schema.

## Bozza v1.1 (Benedetta, 27/10/2026)

Cerniere interne, carichi concentrati sulle aste e molle sono già nella v1.0 e sono coperti dai casi C6, C7 e C8. La v1.1 riguarda quindi:

1. **Combinazioni**: già descritte nello schema ma non ancora calcolate dal solutore. Proposta: il servizio sovrappone i risultati dei casi con i coefficienti della combinazione (analisi lineare), senza modificare il Fortran.
2. **Carichi distribuiti parziali e trapezi**: `q_i`, `q_j`, `a`, `b` sul tratto.
3. **Distorsioni termiche**: ΔT uniforme e a farfalla sull'asta, coerenti con la categoria «temperatura».
4. **Cedimenti vincolari** impressi.

## Decisione sulla v1.1 (Benedetta, 29/10/2026)

La bozza v1.1 **non viene promossa** a schema in vigore. Il motivo è che le sue voci 2–4 (carichi parziali e trapezi, distorsioni termiche, cedimenti) non sono ancora calcolate dal solutore: uno schema che le accettasse produrrebbe risultati sbagliati senza avviso.

La voce 1 (combinazioni) è già nella v1.0 e dal 28/10 viene calcolata dal servizio per sovrapposizione lineare (caso C10). Lo schema in vigore resta quindi la **v1.0**, che copre per intero ciò che il programma calcola. La v1.1 sarà promossa insieme alle modifiche del solutore che la rendono calcolabile, con un caso di prova per ogni voce.

**Tabella schema ↔ epJSON di EnergyPlus**: rinviata. Serve l'Interface Developer's Guide, che non è ancora in RIFERIMENTI (vedi compito di Agata). Va detto anche che lo schema è strutturale (nodi, aste, sezioni) mentre epJSON descrive zone termiche, superfici e impianti: i campi in comune sono pochi (geometria e materiali) e il confronto riguarda la futura parte energetica, non la v1.x.

## Aggiunta compatibile del 30/10/2026 (Benedetta)

Nel blocco `risultati` è stato aggiunto il campo facoltativo `rotazioni_aste` (asta, phi_i, phi_j [rad]), scritto dal solutore v0.2 per il difetto D8: alla cerniera interna la rotazione dell'estremità dell'asta è diversa da quella del nodo. È un campo di uscita e facoltativo, quindi i modelli esistenti restano validi e `schema_version` resta «1.0». Senza il campo, un blocco risultati con le rotazioni sarebbe stato rifiutato da `additionalProperties: false`.

**Tabella schema ↔ epJSON**: ancora rinviata per lo stesso motivo del 29/10. L'Interface Developer's Guide di EnergyPlus non è in RIFERIMENTI e non può essere scaricata dagli agenti, perché il collegatore Drive non vede i file caricati. Proposta dei campi v1.1 da validare con un caso ciascuno: carichi parziali e trapezi (caso da preparare a mano su trave appoggiata), cedimenti vincolari (C11 di Valentina, quando il solutore li calcolerà), distorsioni termiche (caso da preparare).

## Schema v1.1 in vigore dal 31/10/2026 (Benedetta, Carla, Daniela)

La v1.1 è promossa insieme alle modifiche del solutore (v0.3) che la rendono calcolabile, con un caso di prova per voce, come deciso il 29/10. `DATA_SCHEMA.json` accetta `schema_version` «1.0» o «1.1».

| Voce | Campo | Calcolo | Caso di prova |
|---|---|---|---|
| Carichi parziali e trapezi | `carichi_aste[]` con `tipo: "distribuito_trapezio"`, `q_i`, `q_j`, `a`, `b` (0 ≤ a < b ≤ L) | forze d'incastro con le funzioni di forma (Gauss a 3 punti, esatto); diagrammi con Simpson (esatto) | C12 (trapezio parziale), C13 (triangolare, trave incastrata) |
| Cedimenti vincolari | `casi_di_carico[].cedimenti[]`: `nodo`, `ux`, `uy`, `rz` [m, rad] | spostamenti impressi ai gdl vincolati, portati a secondo membro | C11 |
| Distorsioni termiche | — | non ancora | rinviate alla v1.2 |

**Regole di coerenza** controllate dal servizio:
- un modello che usa trapezi o cedimenti deve dichiarare «1.1»;
- un cedimento è ammesso solo su una componente vincolata, non su una molla;
- il trapezio deve stare dentro l'asta.

I modelli v1.0 restano validi senza modifiche.

## Prossime estensioni (v2)

P-Delta, analisi modale, telai spaziali, formato binario per il Fortran.
