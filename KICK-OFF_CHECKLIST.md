# 🚀 KICK-OFF CHECKLIST — Progetto Alessandra

**Data Kick-Off**: 2026-08-16 (domani)  
**Orario**: 09:00  
**Attendees**: Alessandra + 7 Team Leads + Marco (Product Owner/User)  
**Durata**: 90 min

---

## 📋 AGENDA KICK-OFF MEETING

### 1️⃣ WELCOME & PROJECT OVERVIEW (10 min)
**Owner**: Alessandra

- [ ] Saluto team
- [ ] Ricorda obiettivo: CAD 3D tipo AutoCAD con solver Fortran
- [ ] Timeline: ~8 weeks to β release
- [ ] Highlight: parallelo frontend/backend/fortran

**Talking points**:
- "Questo è un progetto ambizioso ma fattibile"
- "Ogni team lead è responsabile della sua area"
- "Comunicazione frequente è critica"

---

### 2️⃣ TEAM INTRODUCTIONS (15 min)
**Owner**: Alessandra

Ogni team lead presenta il suo team (1 min each):

- [ ] **Benedetta (BeneD)** - ARCHITETTURA
  - "Mio team disegna come funziona tutto. Schema dati è il fondamento."
  
- [ ] **Irene (Ire)** - FRONTEND 3D
  - "Faremo interfaccia 3D che sembra AutoCAD. Viewport, viste multiple, toolbar."
  
- [ ] **Natalia (Nat)** - BACKEND
  - "Gestirò orchestrazione: FastAPI, file I/O, lancio Fortran, coordinamento."
  
- [ ] **Elisa (Eli)** - FORTRAN SOLVER
  - "Estenderò solver da lineare a nonlineare (P-Delta) e dinamica (modale)."
  
- [ ] **Francesca (Fra)** - RICERCA
  - "Cercherò integrazioni: ModeSt, OpenFOAM, FEM standards."
  
- [ ] **Valentina (Vale)** - TESTING/QA
  - "Assicurerò qualità: test, regressione, quality gates."

---

### 3️⃣ ARCHITETTURA ALTO LIVELLO (20 min)
**Owner**: Benedetta

- [ ] Mostra diagram flussi (CAD → JSON → Fortran → risultati → visualizzazione)
- [ ] Spiega 3 livelli:
  1. **Geometria Input** (CAD 3D draw)
  2. **Calcoli** (Fortran solver)
  3. **Risultati** (3D visualization)

- [ ] Mostra cartelle principali (01-ARCHITETTURA, 02-FRONTEND-3D, etc.)
- [ ] Sottolinea: **JSON è il ponte universale** tra componenti

**Q&A**: Chiedi se tutti capiscono flussi dati

---

### 4️⃣ TIMELINE & MILESTONES (15 min)
**Owner**: Alessandra

Mostra Gantt (approssimativo):

```
Week 1:   [ARCH]  [SCHEMA DATI] ← Critico: Benedetta
Week 2:   [ARCH]  [BACKEND]     [FRONTEND proto]  [FORTRAN P-Delta]
Week 3:   [BACKEND]  [FRONTEND proto]  [FORTRAN P-Delta]
Week 4:   [BACKEND]  [FRONTEND proto]  [FORTRAN P-Delta]  [QA α]
Week 5:   [QA α release]  ← PROTOTIPO ALPHA
Week 6:   [FORTRAN modale]  [UI completa]  [Post-processor]
Week 7:   [ModeSt bridge]  [QA β]
Week 8:   [QA β release]  ← VERSIONE BETA
```

- [ ] Evidenzia: **Week 1 è CRITICO — Benedetta deve finire schema dati**
- [ ] Nota: Sviluppo parallelo (frontend/backend/fortran simultanei Week 2+)

---

### 5️⃣ DECISIONI GIÀ PRESE (5 min)
**Owner**: Alessandra

- [ ] **Q1**: Input Fortran = binario (veloce) + ASCII (debug)
- [ ] **Q2**: Nonlinearità = tutti, start P-Delta
- [ ] **Q3**: Dinamica = tutti, start modale
- [ ] **Q4**: UI = semi-automatico + template libreria
- [ ] **Q5**: ModeSt = export unidirezionale (per ora)

Chiedi conferme: "Qualcuno ha dubbi su queste scelte?"

---

### 6️⃣ PRIMO STEP (Week 1) (10 min)
**Owner**: Benedetta

**Benedetta ha compiti chiari**:
- [ ] Lunedì: disegna schema dati JSON (formato CAD input)
- [ ] Lunedì-Mercoledì: definisce struttura Fortran input (binario + ASCII)
- [ ] Mercoledì: **API spec** (quali endpoint BackendNat usera)
- [ ] Giovedì: Review con Alessandra + Natalia
- [ ] Venerdì: finalize, pronto per developer

**Aspetto**: Schema dati per martedì → gli altri team iniziano su Foundation solida

---

### 7️⃣ COMUNICAZIONE & WORKFLOW (10 min)
**Owner**: Alessandra

- [ ] Daily sync: Slack #progetto-alessandra ore 15:00 (10 min max)
- [ ] Weekly standup: Lunedì 09:00 (60 min, team leads)
- [ ] Code review: Ogni PR reviewed da tech lead
- [ ] Merge gate: Benedetta (architettura check) + Alessandra (approva)

**Strumenti**:
- [ ] Git repo: D:\progetto-alessandra
- [ ] Slack: #progetto-alessandra
- [ ] Tracking: PROGRESS_DAILY.md (update ogni giorno)

---

### 8️⃣ Q&A APERTE (5 min)
**Owner**: Alessandra

- [ ] Marco (utente): "Avete domande prima di iniziare?"
- [ ] Team: "Chiarimenti su feature, scope, timeline?"

---

## 🎯 DELIVERABLES DOPO KICK-OFF

**Entro domani sera (2026-08-16 EOD)**:
- [ ] BeneD ha **Schema dati JSON draft** pronto per review
- [ ] Natalia sa esattamente quale API deve buildare
- [ ] Irene ha **UI mockup** per viewport 3D
- [ ] Elisa conosce esattamente quale Fortran modifications serve

**Entro fine Week 1 (2026-08-19)**:
- [ ] Schema dati **FINALIZZATO** e approvato
- [ ] API spec **PRONTO**
- [ ] Ogni team lead ha suo piano dettagliato (task, timeline, owner)

---

## 📋 PRE-MEETING CHECKLIST (Today 2026-08-15)

**Alessandra**:
- [ ] Manda calendar invite al team (riunione 2026-08-16 09:00)
- [ ] Allega: README.md, ORGANIGRAMMA_TEAM.md, questa checklist
- [ ] Crea Slack channel #progetto-alessandra
- [ ] Crea Git repo (se non già fatto)

**BeneD** (Benedetta):
- [ ] Prepara presentazione architettura (10 slide max)
- [ ] Prepara template schema dati (vuoto, pronto per riempire)
- [ ] Prepara lista question per FRA/Carla su ModeSt

**Ire** (Irene):
- [ ] Prepara mockup UI 3D (Figma o sketch)
- [ ] Lista tool/library valutate (Three.js vs Babylon vs Other)
- [ ] Prepara setup Electron + React

**Nat** (Natalia):
- [ ] Prepara FastAPI project template
- [ ] Lista dipendenze Python che serviranno
- [ ] Prepara Fortran launcher script (skeleton)

**Eli** (Elisa):
- [ ] Prepara lista paper/reference P-Delta
- [ ] Prepara skeleton Fortran per P-Delta
- [ ] Valuta se serve LAPACK linking

**Fra** (Francesca):
- [ ] Prepara lista ricerca: ModeSt API, OpenFOAM integration points
- [ ] Contatti Tecnisoft (email draft?)
- [ ] Ricerca formato IFC + SAF

**Vale** (Valentina):
- [ ] Prepara test framework choice (pytest + unittest)
- [ ] Prepara Fortran regression suite template
- [ ] Prepara QA checklist per alpha

---

## ✅ POST-MEETING CHECKLIST (2026-08-16 dopo meeting)

**IMMEDIATELY AFTER (14:00)**:
- [ ] ALE scrive riepilogo su Slack #progetto-alessandra
- [ ] ALE crea Issue backlog iniziale (se usi Jira/GitHub)
- [ ] BeneD iniza schema dati nel 01-ARCHITETTURA/

**ENTRO 17:00 (same day)**:
- [ ] Ogni team lead ha suo task tracking file:
  - 02-FRONTEND-3D/TASKS_Irene.md
  - 03-BACKEND/TASKS_Natalia.md
  - 04-FORTRAN-SOLVER/TASKS_Elisa.md
  - 05-RICERCA/TASKS_Francesca.md
  - 06-TESTING/TASKS_Valentina.md

**DAY 2 (2026-08-17)**:
- [ ] BeneD ha schema dati draft → review con ALE + Nat
- [ ] Irene ha UI mockup → review con ALE
- [ ] Natalia ha FastAPI setup → pronto per dev

---

## 🔴 CRITICAL PATH

```
Benedetta disegna schema dati (Week 1)
        ↓
Natalia buildare API (Week 2)
        ↓
Irene buildare UI basato su API (Week 2-3)
        ↓
Elisa estende Fortran (Week 2-3)
        ↓
Paola connette tutto con converter (Week 3)
        ↓
Valentina testa integrazioni (Week 4)
        ↓
ALPHA release (Week 5)
```

**Collo di bottiglia**: Schema dati (se BeneD non finisce entro giovedì, tutto slida)

---

## 📌 NOTE FINALI

- **Non è permesso iniziare dev senza schema dati finalizzato** (BeneD approval required)
- **Parallelo è OK**: Irene/Natalia/Elisa possono iniziare Week 2 mentre BeneD finisce spec
- **Comunicazione è tutto**: Se qualcosa non è chiaro, chiedi subito (non aspettare settimane)
- **Alessandra è arbitro**: Se litigio tra team, ALE decide

---

**Preparato da**: Alessandra  
**Data**: 2026-08-15  
**Stato**: 🟢 READY FOR KICK-OFF
