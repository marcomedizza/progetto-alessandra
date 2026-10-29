# Collegamento con ModeSt — stato al 29/10/2026

**Autrici**: Carla (collegamento ModeSt), Daniela (ricerca ModeSt)
**Consegna prevista**: 30/10/2026 · **Stato**: bloccata in parte, per mancanza della documentazione del formato

## Cosa serve e non è disponibile

Per definire l'esportazione verso ModeSt servono almeno uno di questi materiali, che oggi non sono nel progetto:

1. **Documentazione dei formati di importazione** di ModeSt (Tecnisoft): quali formati accetta (DXF, IFC, file di testo propri) e con quali regole (livelli DXF, unità, convenzioni dei segni).
2. **File di esempio esportati da ModeSt**: un telaio semplice, per esempio il portale C4, salvato nei formati di scambio che ModeSt offre.

Non sono state fatte ipotesi sul formato: un'esportazione basata su supposizioni produrrebbe file che ModeSt potrebbe leggere in modo errato senza segnalarlo. Anche l'analisi a ritroso del formato proprietario è esclusa senza autorizzazione di Tecnisoft (vedi `licenze_componenti.md`).

## Richiesta a Marco

Lei usa ModeSt nello studio: se può esportare il portale C4 (colonne HE 200 A h = 4 m, traverso IPE 300 L = 6 m, q = 30 kN/m) nei formati di scambio disponibili e caricare i file in `RIFERIMENTI/MODEST/`, Carla e Daniela completano la corrispondenza in un giorno.

## Corrispondenza prevista (lato nostro schema)

Le grandezze del nostro schema v1.0 che l'esportazione deve trasferire. La colonna ModeSt va riempita con la documentazione o con i file di esempio.

| Schema v1.0 | Contenuto | Unità | ModeSt |
|---|---|---|---|
| `nodi[].x`, `nodi[].y` | coordinate dei nodi | m | da documentazione |
| `aste[].nodo_i`, `nodo_j` | connettività | — | da documentazione |
| `aste[].svincoli.rz_i/rz_j` | cerniere interne | — | da documentazione |
| `materiali[].E`, `peso_specifico` | modulo elastico, peso | kN/m², kN/m³ | da documentazione |
| `sezioni[].A`, `I` | area, inerzia nel piano | m², m⁴ | da documentazione (ModeSt usa in genere il nome del profilo da sagomario) |
| `vincoli[].ux/uy/rz`, `molle` | vincoli e molle | —, kN/m, kNm/rad | da documentazione |
| `casi_di_carico[]` | casi con categoria NTC | — | da documentazione |
| `carichi_nodali[]` | Fx, Fy, Mz | kN, kNm | da documentazione |
| `carichi_aste[]` | uniformi e concentrati, direzione | kN/m, kN | da documentazione |
| `combinazioni[]` | coefficienti | — | ModeSt genera le combinazioni da sé: probabilmente si esportano solo i casi |

## Ripiego possibile subito

Esportare la sola geometria (nodi e aste) in DXF, su livelli separati per colonne e travi. È un formato pubblico e ModeSt, come la maggior parte dei programmi di calcolo, importa geometrie da DXF; sezioni, vincoli e carichi andrebbero però reinseriti a mano. Da decidere con Marco se vale la pena.
