# Interfaccia 3D — prototipo

Pagina web con Three.js (versione 0.160.0, inclusa in `vendor/`, licenza MIT). Si usa attraverso il servizio di `03-BACKEND/servizio`, che la pubblica su http://127.0.0.1:8000/.

| File | Autrice | Contenuto |
|---|---|---|
| `vista.js` | Irene | Scena, telecamere (frontale, dall'alto, assonometrica), aste, nodi, vincoli, carichi, selezione col mouse |
| `proprieta.js` | Lucia | Pannello proprietà: mostra e modifica sezione, cerniere, vincoli e carichi dell'elemento selezionato |
| `risultati.js` | Mariana | Deformata e diagrammi N, V, M; tabella delle reazioni e dei massimi |
| `app.js` | — | Collegamento tra le parti e chiamate al servizio |

Convenzioni dei segni: quelle di `01-ARCHITETTURA/DATA_SCHEMA.json`. Il diagramma del momento è disegnato dal lato delle fibre tese.

Limiti del prototipo: vedi l'elenco dei difetti in `06-TESTING/flusso.md`.
