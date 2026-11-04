# Rapporto di Veronica — 04/11/2026

Ho letto le licenze delle 14 dipendenze indirette del servizio nei testi distribuiti con i pacchetti. Il dettaglio è in `05-RICERCA/licenze_componenti.md`.

| Licenza | Pacchetti |
|---|---|
| MIT | 10 |
| BSD 3 clausole | click, idna |
| Apache 2.0 | opentelemetry-api |
| PSF 2.0 | typing-extensions |

Sono tutte compatibili con la distribuzione commerciale. L'interfaccia dipende solo da Three.js (MIT).

**Dubbi**: non ho verificato le librerie Rust compilate dentro rpds-py e pydantic-core, e non so ancora quale pacchetto richieda opentelemetry-api.
