# Confronto schema v1.2 ↔ EnergyPlus epJSON (Benedetta, Gabriella; 23/11/2026)

**Fonte**: dizionario dei dati di EnergyPlus (`idd/Energy+.idd.in`), letto il 23/11/2026 dal repository pubblico NREL/EnergyPlus su GitHub (ramo `develop`, quindi non una versione rilasciata). Licenza BSD a tre clausole. Il dizionario non è copiato nel repository: qui ci sono solo i nomi dei campi.

L'epJSON è la forma JSON degli stessi oggetti dell'IDF. Nel testo i campi sono indicati con il nome del dizionario («Specific Heat»). Il nome nello schema epJSON dovrebbe essere lo stesso in minuscolo con i trattini bassi («specific_heat»). Questa corrispondenza non è stata verificata sullo schema epJSON generato (`Energy+.schema.epJSON`) e va confermata prima di scrivere un esportatore.

**Perché la tabella è rimasta bloccata 26 giorni**: era legata alla Interface Developer's Guide in RIFERIMENTI, che gli agenti non leggono. Il dizionario dei dati è la fonte primaria degli oggetti ed è raggiungibile in rete. energyplus.net e bigladdersoftware.com restano invece bloccati dalla rete dell'ambiente.

## Oggetti esaminati

| Oggetto | Campi | Campi rilevanti per il confronto |
|---|---|---|
| `Building` | 9 | Name, North Axis [deg] |
| `GlobalGeometryRules` | 5 | Starting Vertex Position, Vertex Entry Direction, Coordinate System |
| `Site:Location` | 6 | Latitude, Longitude [deg], Time Zone [hr], Elevation [m] |
| `Zone` | 13 | Name, X/Y/Z Origin [m], Ceiling Height [m], Volume [m3], Floor Area [m2] |
| `Material` | 12 | Name, Thickness [m], Conductivity [W/m-K], Density [kg/m3], Specific Heat [J/kg-K], assorbimenti |
| `Material:NoMass` | 9 | Name, Thermal Resistance [m2-K/W] |
| `Construction` | 11 | Name, Outside Layer, Layer 2 … Layer 10 (nomi di materiali) |
| `BuildingSurface:Detailed` | 371 | Name, Surface Type, Construction Name, Zone Name, Outside Boundary Condition, Number of Vertices, Vertex n X/Y/Z-coordinate [m] |

## Aggiunta del 25/11: `HeatBalanceAlgorithm` (Benedetta)

Oggetto con 4 campi, letti dallo stesso dizionario:
- `Algorithm`, a scelta tra ConductionTransferFunction (predefinito), MoisturePenetrationDepthConductionTransferFunction, ConductionFiniteDifference e CombinedHeatAndMoistureFiniteElement;
- `Surface Temperature Upper Limit` [C], predefinito 200;
- `Minimum Surface Convection Heat Transfer Coefficient Value` [W/m2-K], predefinito 0,1;
- `Maximum Surface Convection Heat Transfer Coefficient Value` [W/m2-K], predefinito 1000.

È un'impostazione del metodo di calcolo termico, l'equivalente di `analisi` nel nostro schema, che vale `statica_lineare`. Non ha campi in comune con lo schema strutturale. In un modello energetico separato basterebbe il valore predefinito, salvo esigenze di umidità, che richiederebbero i metodi a differenze o elementi finiti.

`Building` e `Zone`, citati nell'assegnazione del 25/11, erano già nella tabella del 23/11.

## Aggiunta del 28/11: `SimulationControl`, `Timestep`, `RunPeriod` (Benedetta)

Campi letti il 28/11 dallo stesso dizionario (ramo `develop`). Sono oggetti di controllo della simulazione nel tempo:

| Oggetto | Campi | Contenuto | Predefiniti |
|---|---|---|---|
| `SimulationControl` | 7 | Sì/No per il dimensionamento di zone, sistemi e impianti; Sì/No per la simulazione sui periodi di dimensionamento e sui periodi del file climatico; Sì/No e numero massimo di passate (≥ 1) per la simulazione di dimensionamento HVAC | No, No, No, Yes, Yes, No, 1 |
| `Timestep` | 1 | Number of Timesteps per Hour, da 1 a 60 | 6 (passo di 10 min) |
| `RunPeriod` | 13 | Name, mese e giorno di inizio e di fine (obbligatori), anno di inizio e di fine, giorno della settimana iniziale, uso di festività, ora legale, pioggia e neve del file climatico, regola del fine settimana, «Treat Weather as Actual», interpolazione della prima ora (Hour1/Hour24) | festività, ora legale, pioggia e neve: Yes; regola del fine settimana e Treat Weather as Actual: No; Hour24 |

Nessuno dei tre ha un corrispondente nello schema. Lo schema descrive un'analisi statica lineare senza tempo (`analisi.tipo` = `statica_lineare`), mentre questi oggetti definiscono il periodo e il passo di una simulazione dinamica oraria o suboraria. In un modello energetico separato (punto 2 della proposta) servirebbero tutti e tre:
- `RunPeriod` dal 1/1 al 31/12 per il fabbisogno annuo;
- `Timestep` predefinito a 6;
- `SimulationControl` con il dimensionamento disattivato, se non si progettano impianti.

**Nota**: il «Building» e la «Zone» richiesti nell'assegnazione del 27 e del 28/11 erano già nella tabella del 23/11 (righe `Building` e `Zone` qui sotto), come annotato il 25/11. Non c'è altro da aggiungere senza un modello d'involucro da confrontare.

## Corrispondenza con lo schema dati v1.2

| Schema v1.2 | Unità | epJSON | Unità | Relazione |
|---|---|---|---|---|
| `progetto.nome` | — | `Building` Name | — | diretta |
| `unita.lunghezza` = m | m | tutte le lunghezze | m | stessa unità |
| `nodi[].x`, `nodi[].y` (telaio piano) | m | `BuildingSurface:Detailed` Vertex n X/Y/Z | m | **nessuna diretta**: i nodi sono punti di un telaio piano, i vertici delimitano superfici 3D; servirebbe la geometria dell'involucro, che lo schema non descrive |
| `aste[]` | — | — | — | nessuna: EnergyPlus non descrive elementi strutturali |
| `materiali[].nome` | — | `Material` Name | — | stessa identità, proprietà diverse |
| `materiali[].peso_specifico` γ | kN/m³ | `Material` Density ρ | kg/m³ | ρ = γ·1000/g, con g = 9,81 m/s² (78,5 kN/m³ → 8002 kg/m³; la densità dell'acciaio usata di solito nei calcoli termici è circa 7850 kg/m³, perché 78,5 kN/m³ è un valore arrotondato per eccesso per i pesi propri) |
| `materiali[].E`, `alfa_t` | kN/m², 1/°C | — | — | nessuna: EnergyPlus non usa proprietà meccaniche né dilatazione termica |
| — | — | `Material` Conductivity, Specific Heat, Thickness | W/m-K, J/kg-K, m | mancano nello schema |
| `sezioni[].h` | m | `Material` Thickness | m | **solo apparente**: h è l'altezza della sezione di un'asta, Thickness lo spessore di uno strato di parete |
| `vincoli`, `casi_di_carico`, `combinazioni` | — | — | — | nessuna |
| — | — | `Zone`, `Construction`, `Site:Location` | — | mancano nello schema |

## Conclusione

I due modelli hanno in comune soltanto il nome del progetto, l'unità di lunghezza e l'identità dei materiali con la densità. Lo schema descrive un telaio piano per il calcolo statico. epJSON descrive zone termiche, superfici d'involucro e stratigrafie. Nessuno dei due contiene le informazioni principali dell'altro.

Proposta, da decidere con Marco:
1. nessun convertitore diretto schema → epJSON;
2. se la parte energetica partirà, un modello d'edificio separato, con zone, superfici e stratigrafie, collegato al modello strutturale per nome di progetto e di materiale;
3. le proprietà termiche dei materiali (Conductivity, Specific Heat) vanno in un catalogo dei materiali comune, non nello schema del telaio.

**Da verificare** prima di un esportatore:
- i nomi dei campi nello schema epJSON generato;
- la versione rilasciata di EnergyPlus da usare, invece del ramo `develop`.
