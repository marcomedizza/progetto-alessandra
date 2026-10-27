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

## Prossime estensioni (v2)

P-Delta, analisi modale, telai spaziali, formato binario per il Fortran.
