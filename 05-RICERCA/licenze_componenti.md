# Licenze dei componenti — 27/10/2026, aggiornato il 30/10/2026

**Autrice**: Veronica (normativa e conformità)
**Scopo**: verificare che i componenti usati o previsti permettano di distribuire il programma, anche a pagamento.
**Avvertenza**: sintesi tecnica, non parere legale. Prima di una distribuzione commerciale va confermata da un consulente.

## Componenti già usati nel prototipo

| Componente | Uso | Licenza | Obblighi principali | Esito |
|---|---|---|---|---|
| Three.js 0.160.0 | vista 3D | MIT | conservare l'avviso di copyright (`02-FRONTEND-3D/vendor/LICENSE-three.txt`) | compatibile |
| FastAPI | servizio | MIT | avviso di copyright | compatibile |
| Uvicorn | server del servizio | BSD 3 clausole | avviso di copyright, nessun uso del nome per promozione | compatibile |
| jsonschema | validazione del modello | MIT | avviso di copyright | compatibile |
| gfortran (GCC) | compilazione del solutore | GPL v3 con eccezione per la libreria di esecuzione | nessuno sul programma compilato, grazie all'eccezione | compatibile |

## Componenti previsti

| Componente | Uso previsto | Licenza | Nota | Esito |
|---|---|---|---|---|
| LAPACK | solutore, prossima versione | BSD modificata | avviso di copyright | compatibile |
| EnergyPlus | parte energetica | BSD 3 clausole con clausole aggiuntive (testo letto il 30/10 in `LICENSE.txt` del repository NREL/EnergyPlus) | conservare avviso e clausola di esclusione di responsabilità; il governo statunitense conserva una licenza d'uso gratuita e irrevocabile; il nome «EnergyPlus» non va usato nel nome della società o del prodotto né in pubblicità, e il programma va citato come «EnergyPlus version X» | compatibile, a condizione di chiamarlo come programma esterno e di non usarne il nome nel prodotto |
| OpenFOAM | CFD | GPL v3 | collegarlo come libreria impone la GPL a tutto il programma; usarlo come **processo separato** (file di input e output) di norma no | compatibile solo come processo separato |
| ParaView | post-elaborazione CFD | BSD 3 clausole | avviso di copyright | compatibile |
| ModeSt | esportazione | proprietaria (Tecnisoft) | serve la documentazione del formato o un accordo; nessuna analisi a ritroso del formato senza autorizzazione | da chiarire con Tecnisoft |

## Indicazioni

1. **Struttura del programma**: tenere OpenFOAM ed EnergyPlus come programmi esterni chiamati con file, come già avviene per il solutore Fortran. Così il programma resta distribuibile con licenza propria.
2. **Avvisi di copyright**: raccogliere tutti gli avvisi in un file `LICENZE_TERZE_PARTI.md` da distribuire con il programma.
3. **Testi in RIFERIMENTI**: il PDF di Olgyay proviene da un sito di distribuzione non autorizzata. Non va incluso in nessuna distribuzione né nel repository pubblico; serve una copia regolare.
4. **Repository pubblico**: il repository GitHub è pubblico. Il codice e i documenti caricati sono leggibili da chiunque; scegliere ora la licenza del progetto o rendere il repository privato.
