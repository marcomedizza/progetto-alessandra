# Collegamento con ModeSt — stato al 30/10/2026

**Autrici**: Carla (collegamento ModeSt), Daniela (ricerca ModeSt)
**Stato dal 30/10 sera**: SOSPESO su disposizione di Marco: ModeSt non blocca nessuna attività; Carla e Daniela passano a cedimenti e carichi parziali (v1.1). Si riprende se e quando arrivano i file di esempio. · **Stato al 30/10 mattina**: corrispondenza con ModeSt non completabile senza documentazione; pronti la tabella lato schema, i formati pubblici e una bozza di esportazione DXF della sola geometria

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
| `nodi[].x`, `nodi[].y` | coordinate dei nodi | m | da verificare |
| `aste[].nodo_i`, `nodo_j` | connettività | — | da verificare |
| `aste[].svincoli.rz_i/rz_j` | cerniere interne | — | da verificare |
| `materiali[].E`, `peso_specifico` | modulo elastico, peso | kN/m², kN/m³ | da verificare |
| `sezioni[].A`, `I` | area, inerzia nel piano | m², m⁴ | da verificare (ipotesi: ModeSt usa il nome del profilo da sagomario) |
| `vincoli[].ux/uy/rz`, `molle` | vincoli e molle | —, kN/m, kNm/rad | da verificare |
| `casi_di_carico[]` | casi con categoria NTC | — | da verificare |
| `carichi_nodali[]` | Fx, Fy, Mz | kN, kNm | da verificare |
| `carichi_aste[]` | uniformi e concentrati, direzione | kN/m, kN | da verificare |
| `combinazioni[]` | coefficienti | — | da verificare (ipotesi: ModeSt genera le combinazioni da sé e si esportano solo i casi) |

## Ripiego possibile subito

Esportare la sola geometria (nodi e aste) in DXF, su livelli separati per colonne e travi. È un formato pubblico. Molti programmi di calcolo importano geometrie da DXF, ma per ModeSt non è confermato (vedi aggiornamento del 30/10). Sezioni, vincoli e carichi andrebbero però reinseriti a mano. Da decidere con Marco se vale la pena.

## Aggiornamento del 30/10 (Carla, Daniela)

### Cosa dicono le fonti pubbliche su ModeSt

Una ricerca sul sito del produttore e su fonti pubbliche non ha trovato documentazione dei formati che ModeSt **importa**. Le fonti trovate parlano solo dei disegni esecutivi che ModeSt **produce** in DXF. Non risulta né confermato né escluso che ModeSt importi IFC. Tutte le righe della tabella sopra restano quindi «da verificare». Contatto del produttore: Tecnisoft, Prato.

**Richiesta a Marco, ribadita**: esportare da ModeSt il portale C4 nei formati di scambio disponibili, caricarlo in `RIFERIMENTI/MODEST/` e indicare quali formati ModeSt accetta in importazione (menu «Importa» o simile).

### Formati pubblici utilizzabili

| Formato | Specifica | Cosa può trasferire | Limiti |
|---|---|---|---|
| DXF | Autodesk, «DXF Reference», pubblica e gratuita | geometria: linee e punti su livelli | nessuna informazione strutturale: sezioni, vincoli e carichi vanno reinseriti |
| IFC 4 | buildingSMART, norma ISO 16739 | modello di calcolo completo: `IfcStructuralAnalysisModel`, aste `IfcStructuralCurveMember`, nodi `IfcStructuralPointConnection` con `IfcBoundaryNodeCondition` (vincoli e molle), casi `IfcStructuralLoadCase`, carichi `IfcStructuralPointAction` e `IfcStructuralCurveAction` | utile solo se ModeSt importa la parte di calcolo dell'IFC, cosa da verificare; molti programmi importano solo la parte architettonica |
| Testo proprio di ModeSt | non pubblico | tutto | serve documentazione o autorizzazione di Tecnisoft |

I nomi delle entità IFC vengono dalla specifica IFC 4 di buildingSMART (standards.buildingsmart.org). Prima di scrivere un esportatore vanno ricontrollati sulla versione esatta che ModeSt dichiara di leggere.

### Bozza di esportazione: `05-RICERCA/esporta_dxf.py`

- **Cosa esporta**: dallo schema v1.0 la sola geometria, in un DXF R12 minimo:
  - un punto per nodo sul livello `NODI`;
  - una linea per asta, su un livello per sezione (`ASTE_IPE300`, `ASTE_HEA200`);
  - coordinate in metri.
- **Prova sul portale C4**: 4 nodi e 3 aste. Il file è stato riletto senza errori da una libreria DXF indipendente (ezdxf), che lo riconosce come versione AC1009 (R12).
- **Non ancora provato in ModeSt.**

    python3 05-RICERCA/esporta_dxf.py 06-TESTING/casi/C4_portale_carico_uniforme.json c4.dxf
