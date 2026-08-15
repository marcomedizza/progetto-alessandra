# 🏗️ PROGETTO ALESSANDRA — Visualizzatore CAD Strutturale 3D

**Lead**: Alessandra (ALE)  
**Inizio**: 2026-08-15  
**Team**: 16 donne ingegnere specializzate  
**Status**: 🟢 FASE DI PLANNING & KICK-OFF

---

## 📌 OBIETTIVO PROGETTO

Sviluppare un **visualizzatore CAD 3D tipo AutoCAD 2015** con:
- ✅ Interfaccia 3D (viste Top, Front, Right, ISO)
- ✅ Pre-processore grafico (input geometria, proprietà, carichi)
- ✅ Risolutore strutturale Fortran (telai 2D: statica, P-Delta, dinamica, nonlinearità)
- ✅ Post-processore (risultati visualizzazione 3D)
- ✅ Export/Import ModeSt (ponte bidirezionale futura)
- ✅ Template libreria (strutture ripetitive: travi, solai, travetti)

**Target**: Ingegneria civile strutturale (calcoli strutturali + termici + idraulici futuri)

---

## 📂 STRUTTURA CARTELLE

```
D:\progetto-alessandra\
├── 01-ARCHITETTURA/          ← Schema dati, API, architecture docs (Benedetta)
├── 02-FRONTEND-3D/           ← React + Three.js + Electron UI 3D (Irene)
├── 03-BACKEND/               ← FastAPI + Python orchestration (Natalia)
├── 04-FORTRAN-SOLVER/        ← Estensioni Fortran solver (Elisa)
├── 05-RICERCA/               ← Ricerca ModeSt, OpenFOAM, FEM standards (Francesca)
├── 06-TESTING/               ← Test suite, regression, QA (Valentina)
├── 07-DOCUMENTAZIONE/        ← User manual, technical docs
├── 08-CONFIG/                ← Build scripts, CI/CD, setup
├── 09-ASSETS/                ← Icone, modelli, template dati
├── ORGANIGRAMMA_TEAM.md      ← Struttura team e responsabilità
└── README.md                 ← Questo file
```

---

## 👩‍💼 TEAM LEADS

| Specialità | Lead | Cartella |
|-----------|------|----------|
| **Architettura** | Benedetta (BeneD) | 01-ARCHITETTURA |
| **Frontend 3D** | Irene (Ire) | 02-FRONTEND-3D |
| **Backend** | Natalia (Nat) | 03-BACKEND |
| **Fortran Solver** | Elisa (Eli) | 04-FORTRAN-SOLVER |
| **Ricerca** | Francesca (Fra) | 05-RICERCA |
| **Testing/QA** | Valentina (Vale) | 06-TESTING |

---

## 🚀 ROADMAP ALTO LIVELLO

### **Fase 1 (Weeks 1-2): Planning & Spec**
- ✅ Architettura completa (BeneD)
- ✅ Schema dati JSON/Fortran (BeneD)
- ✅ API contracts (BeneD)
- ✅ Ricerca ModeSt, OpenFOAM (Fra, Gabriella)

**Deliverable**: Architecture document, data schema, API spec

### **Fase 2 (Weeks 2-4): Core Development**
- Backend FastAPI base (Nat, Ottavia, Paola)
- Frontend CAD 3D prototipo (Ire, Lucia)
- Fortran P-Delta extension (Eli)
- Data converter pipeline (Paola)

**Deliverable**: Prototipo funzionante (draw → calculate → results)

### **Fase 3 (Weeks 4-6): Integrazione & Feature**
- Integrazione componenti (Vale - QA)
- Fortran dinamica modale (Eli)
- UI geometry editor completo (Lucia)
- Post-processor 3D (Mariana)

**Deliverable**: Versione α con calcoli lineari + dinamica modale

### **Fase 4 (Weeks 6-8): Bridge ModeSt & Refine**
- ModeSt export (Carla, Daniela)
- Nonlinearità aggiuntive (Eli)
- Template libreria (Lucia)
- Performance optimization

**Deliverable**: Versione β con ModeSt bridge

### **Fase 5+ (Weeks 9+): Estensioni**
- OpenFOAM integration (Francesca)
- CFD workflow
- Analisi termiche (Edilclima bridge)
- Idraulica (EPANET workflow)

---

## 🛠️ STACK TECNOLOGICO

### Frontend
- **React** 18+ (UI framework)
- **Three.js** (3D visualization, WebGL)
- **Electron** (Desktop app)
- **TypeScript** (type safety)

### Backend
- **Python** 3.11+
- **FastAPI** (REST API framework)
- **Pydantic** (data validation)
- **SQLAlchemy** (ORM, if needed)

### Solver
- **Fortran 2008+** (gfortran 16.1.0)
- **LAPACK** (linear algebra)
- **Binary I/O** (performance)

### Testing
- **pytest** (Python tests)
- **unittest** (Fortran wrapper tests)
- **Performance benchmark tools**

### DevOps
- **Docker** (containerization)
- **GitHub Actions** (CI/CD)
- **Git** (version control)

---

## 📋 DECISIONI ARCHITETTURALI CONFERMATE

| Tema | Decisione | Rationale |
|------|-----------|-----------|
| **Input Fortran** | Binario (fast) + ASCII (debug) | Performance + Debuggability |
| **Nonlinearità** | Tutti (P-Delta, Plasticità, G.Spostamenti, Contatti) | Start P-Delta |
| **Dinamica** | Tutti (Modale, Spettrale, Time-hist, Armonica) | Start Modale |
| **UI Input** | Semi-automatico + Template libreria | Velocità + UX moderna |
| **ModeSt** | Export unidirezionale (per ora) | No reverse-engineering complesso |
| **Visualizzazione** | 3D tipo AutoCAD (viste multiple) | Professional UX |

---

## 📞 COMUNICAZIONE

### Daily Sync
- **Channel**: Slack #progetto-alessandra
- **Ora**: 15:00 (sync brief 10 min)
- **Owner**: Alessandra

### Weekly Status
- **Giorno**: Lunedì 09:00
- **Attendees**: Alessandra + 7 Team Leads
- **Durata**: 60 min
- **Owner**: Alessandra

### Code Review
- **Standard**: Ogni PR reviewed da tech lead del team
- **Merge gate**: BeneD (architettura) + ALE (approva)

---

## 🎯 SUCCESS CRITERIA

✅ **Prototipo α** (Week 5):
- [ ] Disegni geometria in CAD 3D
- [ ] Calcoli eseguiti (statica lineare + P-Delta)
- [ ] Risultati visualizzati (deformate, diagrammi M/T)
- [ ] Esporta DXF

✅ **Versione β** (Week 8):
- [ ] Dinamica modale funzionante
- [ ] ModeSt export working
- [ ] Template libreria (5+ tipi)
- [ ] Test suite completa

✅ **Release 1.0**:
- [ ] Tutte le features
- [ ] Performance acceptabile
- [ ] User manual + API docs
- [ ] Deploy Windows/Mac/Linux

---

## 📊 METRICHE

- **Code coverage**: Target 80%+ (strutturale Fortran 90%+)
- **Performance**: P-Delta solve < 500ms per 100 elementi
- **UI responsiveness**: < 16ms per frame (60 FPS)
- **API latency**: < 100ms (p95)

---

## 🔗 LINK IMPORTANTI

- **Architettura**: vedi `01-ARCHITETTURA/ARCHITECTURE.md` (in sviluppo)
- **Schema dati**: vedi `01-ARCHITETTURA/DATA_SCHEMA.json` (in sviluppo)
- **API docs**: vedi `03-BACKEND/API_SPEC.md` (in sviluppo)
- **Organigramma**: vedi `ORGANIGRAMMA_TEAM.md`

---

## 📌 GET STARTED

**Se sei nuovo al progetto**:
1. Leggi questo README
2. Leggi `ORGANIGRAMMA_TEAM.md` → trovi il tuo team lead
3. Contatta il tuo team lead per onboarding
4. Segui setup istruzioni in `08-CONFIG/SETUP.md`
5. Inizia con il tuo primo task

---

## ❓ FAQ / SUPPORT

**Q: Come inicio un task nuovo?**  
A: Coordinati con il tuo team lead, crea issue in Git, commenta con estimativa tempo.

**Q: Come do feedback architettura?**  
A: Post in Slack #progetto-alessandra o crea PR comment su PR architettura (BeneD).

**Q: Chi approva merge?**  
A: Tech lead del tuo team + Benedetta (architettura) + Alessandra (finale).

---

## 📅 PROSSIMI PASSI

- [ ] **Oggi**: Kick-off call con team leads
- [ ] **Domani**: BeneD inizia schema dati + API spec
- [ ] **Week 1**: Tutti team leads hanno piano dettagliato
- [ ] **Week 2**: Inizio development vero

---

_Documento creato: 2026-08-15 · Alessandra (ALE) Project Lead_
