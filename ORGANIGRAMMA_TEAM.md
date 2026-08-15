# 👩‍💼 ORGANIGRAMMA PROGETTO ALESSANDRA

**Inizio progetto**: 2026-08-15  
**Team Lead**: Alessandra (ALE)  
**Status**: 🟢 KICK-OFF

---

## 📊 STRUTTURA GERARCHICA COMPLESSIVA

```
                        ┌────────────────────────┐
                        │  MARCO (Product Owner) │
                        └────────────┬───────────┘
                                     │
                ┌────────────────────┼────────────────────┐
                │                    │                    │
         ┌──────▼──────────┐  ┌──────▼──────────┐
         │  ALESSANDRA     │  │    GIORGIA      │
         │  (Tech Lead)    │  │  (Business Lead)│
         └──────┬──────────┘  └──────┬──────────┘
                │                    │
    ┌───────────┼───────────┐   ┌────┴────────────┐
    │           │           │   │                 │
┌───▼───┐  ┌───▼───┐  ┌───▼───┐│ ┌──────────────┐
│ARCHITETTURA   │FRONTEND 3D  │BACKEND    │ OFFERTE & FAT.│
│Benedetta(TL)  │ Irene(TL)   │Natalia(TL)│ Aurora        │
└───┬───┘  └───┬───┘  └───┬───┘│ └──────────────┘
    │          │          │    │ ┌──────────────┐
┌───┴──┐  ┌───┴──┐  ┌────┴─┐ │ │EMAIL & COMM.  │
│Carla │  │Lucia │  │Ottavia   │ Livia          │
│Daniel   │Mariana  │Paola  │ └──────────────┘
└───┬──┘  └───┬──┘  └────┬─┘  ┌──────────────┐
    │         │         │    │NORMATIVE     │
┌───▼─────┐   │    ┌────▼─┐  │Veronica      │
│FORTRAN  │   │    │      │  └──────────────┘
│Elisa(TL)│   │    │      │  ┌──────────────┐
│         │   │    │      │  │NEWS & INTEL. │
└───┬─────┘   │    │      │  │Camilla       │
    │    ┌────▼──┐ │      │  └──────────────┘
    │    │RICERCA   │      │  ┌──────────────┐
    │    │Francesca(TL) │  │PROGRESS MON. │
    │    │Gabriella     │  │Laura         │
    │    └────┬──┘      │  └──────────────┘
    │         │         │
    │    ┌────▼────┐ ┌──▼──┐
    │    │TESTING/QA│
    │    │Valentina(TL)
    │    │Renata, Silvia
    │    └────┬────┘
    │         │
```

**Struttura gerarchica**:
- MARCO (User/Product Owner) — autorità suprema
  - ALESSANDRA — Tech Lead (16 agenti, team sviluppo)
  - GIORGIA — Business Lead (5 agenti, operations/business)

**Coordinamento**:
- Daily: Alessandra coordina team tecnico
- Daily: Giorgia coordina team business
- Giornaliero (Week 3+): Alessandra ↔ Giorgia sync (15 min, 16:00)
- Settimanale: Marco + Alessandra + Giorgia (Monday 14:00, 60 min)

---

## 👩‍💼 TEAM LEADERS PER SPECIALITÀ

### 🏛️ **ARCHITETTURA** — Benedetta (BeneD)
**Cartella**: `01-ARCHITETTURA`  
**Responsabilità**: 
- Disegno architettura complessiva
- Schema dati JSON/Fortran
- API contracts
- Dipendenze tra componenti
- Milestone planning

**Team**:
- **Benedetta** (Lead) - Schema dati, disegno architettura
- **Carla** - Bridge ModeSt, interfacce esterne
- **Daniela** - Ricerca formati, doc technical

**Output**: Documenti architetturali, API specs, data schemas

---

### 🎨 **FRONTEND 3D** — Irene (Ire)
**Cartella**: `02-FRONTEND-3D`  
**Responsabilità**:
- Visualizzazione 3D (Three.js/WebGL)
- Viste multiple (Top, Front, Right, ISO)
- Toolbar stile AutoCAD
- Interazione (pan, zoom, rotate, gizmo)
- Rendering risultati (deformate, diagrammi)

**Team**:
- **Irene** (Lead) - CAD 3D core, viewport
- **Lucia** - UI geometry editor, property panel, template library
- **Mariana** - Post-processing, risultati visualizzazione

**Stack**: React, Three.js, Electron, GLSL shaders

**Output**: App Electron con UI 3D funzionale

---

### ⚙️ **BACKEND** — Natalia (Nat)
**Cartella**: `03-BACKEND`  
**Responsabilità**:
- FastAPI server
- File I/O management
- Launcher processi Fortran
- Data conversion pipeline
- API endpoints

**Team**:
- **Natalia** (Lead) - FastAPI engine, orchestrazione
- **Ottavia** - Fortran compilation, packaging
- **Paola** - Data converter, DXF↔JSON↔Fortran

**Stack**: Python 3.11+, FastAPI, Pydantic, gfortran

**Output**: Backend API + Fortran wrapper executable

---

### 🧮 **FORTRAN SOLVER** — Elisa (Eli)
**Cartella**: `04-FORTRAN-SOLVER`  
**Responsabilità**:
- Estensione solver (P-Delta, nonlinearità, dinamica)
- Analisi modale (frequenze, modi)
- Implementazione algoritmi
- Testing regressione calcoli

**Team**:
- **Elisa** (Lead) - Fortran evolution, algoritmi strutturali
- (Junior engineers: sviluppatori specifici algoritmi)

**Stack**: Fortran 2008+, gfortran 16.1.0, LAPACK (linear algebra)

**Output**: Eseguibile Fortran compilato con tutte le estensioni

---

### 🔍 **RICERCA** — Francesca (Fra)
**Cartella**: `05-RICERCA`  
**Responsabilità**:
- Ricerca integrazioni esterne (ModeSt, OpenFOAM)
- Analisi standard FEM (SAF, IFC, XML)
- Documentazione tecniche
- Reverse-engineering formati proprietari

**Team**:
- **Francesca** (Lead) - OpenFOAM, CFD research
- **Gabriella** - FEM standards (SAF, IFC)
- **Daniela** - ModeSt integration research

**Output**: Technical documentation, format specifications, integration guides

---

### 🧪 **TESTING & QA** — Valentina (Vale)
**Cartella**: `06-TESTING`  
**Responsabilità**:
- Test suite calcoli Fortran
- Test integrazione componenti
- Performance benchmark
- Validazione workflow end-to-end
- Quality gates

**Team**:
- **Valentina** (Lead) - QA integration, gates
- **Renata** - Workflow validator
- **Silvia** - Fortran regression lab

**Stack**: pytest, unittest, benchmark tools

**Output**: Test reports, regression suite, QA checklist

---

### 📚 **DOCUMENTAZIONE** — Documentatrice (TBD)
**Cartella**: `07-DOCUMENTAZIONE`  
**Responsabilità**:
- User manual
- API documentation
- Architecture docs
- Installation guide
- Troubleshooting guide

---

### ⚙️ **CONFIGURAZIONE** — DevOps (TBD)
**Cartella**: `08-CONFIG`  
**Responsabilità**:
- Setup environment
- Build scripts
- CI/CD pipelines
- Docker/packaging
- Deployment

---

### 🎨 **ASSETS**
**Cartella**: `09-ASSETS`  
**Contenuti**:
- Icone, texture, modelli 3D
- Dati test
- Template libreria strutture

---

## 📋 ASSEGNAZIONI DETTAGLIATE

| Nome | Specialità | Team | Ruolo | Cartella Owner |
|------|-----------|------|-------|--------|
| **Alessandra** | Project Management | Governance | Project Lead (ALE) | 01-ARCHITETTURA |
| **Benedetta** | Architecture | 01 | Tech Lead Architettura | 01-ARCHITETTURA |
| **Carla** | ModeSt Bridge | 01 | Integration Specialist | 01-ARCHITETTURA |
| **Daniela** | ModeSt Research | 05 | Research Engineer | 05-RICERCA |
| **Elisa** | Fortran Evolution | 04 | Tech Lead Solver | 04-FORTRAN-SOLVER |
| **Francesca** | CFD/OpenFOAM | 05 | Tech Lead Ricerca | 05-RICERCA |
| **Gabriella** | FEM Standards | 05 | Standards Analyst | 05-RICERCA |
| **Irene** | CAD 3D Core | 02 | Tech Lead Frontend | 02-FRONTEND-3D |
| **Lucia** | UI/Geometry Editor | 02 | UI Engineer | 02-FRONTEND-3D |
| **Mariana** | Results Visualizer | 02 | Visualization Engineer | 02-FRONTEND-3D |
| **Natalia** | Backend API | 03 | Tech Lead Backend | 03-BACKEND |
| **Ottavia** | Fortran Wrapper | 03 | Build/DevOps | 03-BACKEND |
| **Paola** | Data Converter | 03 | Data Pipeline | 03-BACKEND |
| **Renata** | Workflow Testing | 06 | QA Engineer | 06-TESTING |
| **Silvia** | Regression Lab | 06 | Test Engineer | 06-TESTING |
| **Valentina** | Quality Assurance | 06 | Tech Lead QA | 06-TESTING |

---

## 📞 CONTATTI TEAM LEADS

```
┌─────────────────────────────────────────────────────────┐
│                    TEAM LEADS RIUNIONE                  │
├─────────────────────────────────────────────────────────┤
│ Alessandra (ALE)      - Project Lead (Governance)       │
│ Benedetta (BeneD)     - Architettura                    │
│ Irene (Ire)           - Frontend 3D                     │
│ Natalia (Nat)         - Backend                         │
│ Elisa (Eli)           - Fortran Solver                  │
│ Francesca (Fra)       - Ricerca                         │
│ Valentina (Vale)      - Testing/QA                      │
└─────────────────────────────────────────────────────────┘
```

**Riunione coordinamento**: Lunedì/Mercoledì/Venerdì 09:00  
**Owner**: Alessandra

---

## 🚀 WORKFLOW DECISIONALE

```
1. ARCHITETTURA (BeneD) disegna → Approva ALE
                          ↓
2. TEAM LEADS ricevono specifiche dettagliate
                          ↓
3. Ciascun team sviluppa in parallelo (FRONTEND, BACKEND, FORTRAN, etc.)
                          ↓
4. TESTING (Vale) valida integrazioni
                          ↓
5. ALE approva milestone, go/no-go release
```

---

## 📅 MILESTONE PLANNING

| Fase | Owner | Timeline | Status |
|------|-------|----------|--------|
| Architettura & Design | BeneD | Week 1 | 🔴 NOT STARTED |
| Schema dati JSON | BeneD | Week 1-2 | 🔴 NOT STARTED |
| Backend base (FastAPI) | Nat | Week 2-3 | 🔴 NOT STARTED |
| Frontend CAD 3D prototipo | Ire | Week 2-4 | 🔴 NOT STARTED |
| Fortran P-Delta extension | Eli | Week 3-5 | 🔴 NOT STARTED |
| Integrazione α | Vale | Week 5 | 🔴 NOT STARTED |
| Fortran Dinamica modale | Eli | Week 6-7 | 🔴 NOT STARTED |
| ModeSt bridge | Carla | Week 7-8 | 🔴 NOT STARTED |
| Release β | ALE | Week 8 | 🔴 NOT STARTED |

---

## 📌 NOTE IMPORTANTI

✅ **Ogni team lead è responsabile di**:
- Piano di lavoro dettagliato per la sua area
- Daily sync con team
- Reporting settimanale a Alessandra
- Quality gate prima di merge

✅ **Alessandra coordina**:
- Riunioni team leads
- Approvazione architettura
- Release decisions
- Escalation

✅ **Comunicazione**:
- Slack/Discord per daily
- Weekly status report (lunedì)
- Code review prima di merge

---

_Documento creato: 2026-08-15_  
_Last update: 2026-08-15_
