# Licenze dei componenti — 27/10/2026, aggiornato il 02/11/2026

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

### Verifica sui testi originali (Veronica, 02/11/2026)

Testi letti nei file di licenza distribuiti con i pacchetti installati nell'ambiente di prova (`*.dist-info/licenses/`) e nella copia di Three.js in `02-FRONTEND-3D/vendor/`.

| Componente | Versione | File letto | Testo | Titolare del copyright |
|---|---|---|---|---|
| FastAPI | 0.162.0 | `LICENSE` | MIT | Sebastián Ramírez, 2018 |
| Starlette (usato da FastAPI) | 1.10.0 | `LICENSE.md` | BSD 3 clausole | Encode OSS Ltd, 2018 |
| Pydantic (usato da FastAPI) | 2.14.1 | `LICENSE` | MIT | Pydantic Services Inc. e collaboratori |
| Uvicorn | 0.54.0 | `LICENSE.md` | BSD 3 clausole | Encode OSS Ltd, 2017 |
| jsonschema | 4.26.0 | `COPYING` | MIT | Julian Berman, 2013 |
| Three.js | 0.160.0 | `vendor/LICENSE-three.txt` e intestazione del modulo | MIT | three.js authors, 2010–2023 |

**Esito**: confermate le licenze della tabella precedente. Due dipendenze indirette, Starlette e Pydantic, non erano elencate e vanno aggiunte agli avvisi. Obblighi per la distribuzione:
- tutte e sei richiedono di riportare l'avviso di copyright e il testo della licenza;
- le BSD 3 clausole vietano anche di usare il nome dei titolari per promuovere il prodotto.

Per il servizio installato in rete (uso come SaaS, senza distribuire il codice) non c'è nessun obbligo ulteriore. Le versioni sono quelle dell'ambiente di prova: per il rilascio vanno fissate in un file dei requisiti.

### Dipendenze indirette del servizio (Veronica, 04/11/2026)

Albero delle dipendenze di FastAPI, Uvicorn e jsonschema, ricavato dai metadati dei pacchetti installati. Ogni testo è stato letto nel file di licenza distribuito con il pacchetto.

| Pacchetto | Versione | Licenza (testo letto) | Titolare |
|---|---|---|---|
| annotated-doc | 0.0.5 | MIT | Sebastián Ramírez |
| annotated-types | 0.8.0 | MIT | i collaboratori |
| anyio | 4.15.1 | MIT | Alex Grönholm |
| attrs | 26.1.0 | MIT | Hynek Schlawack e collaboratori |
| click | 8.5.0 | BSD 3 clausole | Pallets |
| h11 | 0.16.0 | MIT | Nathaniel J. Smith e collaboratori |
| idna | 3.20 | BSD 3 clausole | Kim Davies e collaboratori |
| jsonschema-specifications | 2025.9.1 | MIT | Julian Berman |
| opentelemetry-api | 1.45.1 | Apache 2.0 | OpenTelemetry Authors |
| pydantic-core | 2.50.1 | MIT | Samuel Colvin |
| referencing | 0.37.0 | MIT | Julian Berman |
| rpds-py | 2026.9.1 | MIT | Julian Berman |
| typing-extensions | 4.16.0 | PSF 2.0 (licenza di Python) | Python Software Foundation |
| typing-inspection | 0.4.4 | MIT | Pydantic Services Inc. |

**Esito**: tutte compatibili con la distribuzione, anche commerciale.
- Apache 2.0 (opentelemetry-api) richiede in più di conservare il file NOTICE, se presente, e di indicare le modifiche ai sorgenti.
- PSF 2.0 richiede di conservare l'avviso di copyright.

**Dubbi dichiarati**:
- rpds-py e pydantic-core contengono codice Rust compilato: le licenze delle librerie Rust incluse nel binario non sono state verificate.
- Non ho accertato quale pacchetto richieda opentelemetry-api: risulta nei requisiti dichiarati dell'albero, ma va confermato con un ambiente pulito.

**Interfaccia (02-FRONTEND-3D)**: l'unica dipendenza è Three.js 0.160.0, `three.module.min.js` e `OrbitControls.js`, MIT, già verificata il 02/11. Playwright serve solo alle prove automatiche e non si distribuisce.

### Chiusura dei dubbi del 04/11 (punto 47, Veronica, 06/11)

- **opentelemetry-api** è un requisito diretto di FastAPI 0.162: `opentelemetry-api>=1.44.0`, secondo i metadati del pacchetto. Starlette lo richiede solo nella variante opzionale «full». Licenza Apache 2.0, già verificata.
- **Librerie Rust incluse**: lette negli elenchi dei materiali (SBOM CycloneDX) distribuiti dentro i pacchetti.

| Pacchetto | Componenti Rust | Licenze |
|---|---|---|
| rpds-py 2026.9.1 | 17 | 13 «MIT o Apache 2.0», 2 MIT, 1 Apache 2.0 con eccezione LLVM, 1 «(MIT o Apache 2.0) e Unicode 3.0» |
| pydantic-core 2.50.1 | 99 | 51 «MIT o Apache 2.0», 19 Unicode 3.0, 12 MIT, 7 «Apache 2.0 o MIT», e inoltre Unlicense/MIT, BSD 2 clausole/Apache/MIT, Zlib, Unicode-DFS-2016 |

Un componente di pydantic-core offre la scelta «MIT o Apache 2.0 o LGPL 2.1+»: si sceglie MIT e la LGPL non si applica.

**Esito**: tutte licenze permissive, compatibili con la distribuzione commerciale. Gli avvisi vanno riportati nel file `LICENZE_TERZE_PARTI.md`, che si può generare da questi SBOM. Il punto 47 è chiuso.

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
