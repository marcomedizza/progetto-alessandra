# 🚀 KICK-OFF PROGETTO ALESSANDRA — 15 Agosto 2026

**Orario**: Ora (15:00 - 17:00)  
**Location**: Online/In-person  
**Lead**: Alessandra (ALE) + Giorgia (GIO)  
**Attendees**: 21 agenti + Marco (Product Owner)

---

## ⏰ AGENDA (90 min)

### **1️⃣ WELCOME & PROJECT VISION** (10 min)
**Chi**: Alessandra + Giorgia + Marco  
**Cosa**:
- Benvenuto al team
- Visione progetto: CAD 3D tipo AutoCAD con solver Fortran
- Timeline: ~8 weeks → Beta release
- Highlights: Parallelo frontend/backend/fortran

### **2️⃣ TEAM INTRODUCTIONS** (15 min)
**Chi**: Alessandra, Benedetta, Irene, Natalia, Elisa, Francesca, Valentina (Tech Leads) + Giorgia  
**Formato**: 1 min per team lead
- Cosa fa il mio team
- Collaborazioni critiche
- Dipendenze Week 1

### **3️⃣ ARCHITETTURA ALTO LIVELLO** (15 min)
**Chi**: Benedetta (BeneD)  
**Cosa**:
- Diagram flussi: CAD → JSON → Fortran → Risultati → Visualizzazione
- 3 livelli: Input / Calcoli / Output
- **CRITICO**: Schema dati è il fondamento

### **4️⃣ TIMELINE & MILESTONES** (10 min)
**Chi**: Alessandra  
**Highlight**:
```
Week 1:   [ARCH + SCHEMA DATI]      ← CRITICO
Week 2-4: [BACKEND + FRONTEND + FORTRAN] ← Parallelo
Week 5:   [ALPHA RELEASE]
Week 8:   [BETA RELEASE]
```

### **5️⃣ DECISIONI GIÀ PRESE** (5 min)
**Chi**: Alessandra  
- ✅ Input Fortran: Binario (veloce) + ASCII (debug)
- ✅ Nonlinearità: Tutti, start P-Delta
- ✅ Dinamica: Tutti, start Modale
- ✅ UI: Semi-automatico + Template
- ✅ ModeSt: Export unidirezionale

### **6️⃣ PRIMO STEP — WEEK 1** (10 min)
**Chi**: Benedetta (BeneD) + Alessandra  
**Compiti Benedetta**:
- [ ] Lunedì: Schema dati JSON (draft)
- [ ] Martedì-Mercoledì: Fortran input format
- [ ] Mercoledì: API spec
- [ ] Giovedì: Review Alessandra + Natalia
- [ ] Venerdì: FINALE → pronto dev

**Aspetto**: Schema dati per martedì → gli altri team possono iniziare

### **7️⃣ RICERCHE ONLINE — OGGI (After Kick-off)** (5 min)
**Chi**: Giorgia + tutti agenti  
**Timeline**: 15:10 - 17:30 (ricerca) → 17:30 upload → 18:00 DONE  
**Criteri**: Fonti autorevoli, internazionali, max 300 battute riassunto  
**Tab**: Dashboard → "📚 Ricerche Online"

### **8️⃣ COMUNICAZIONE & WORKFLOW** (5 min)
**Chi**: Alessandra + Giorgia  
- 📱 Daily sync: Slack #progetto-alessandra 15:00 (10 min)
- 📅 Weekly standup: Lunedì 09:00 (60 min)
- 📝 Code review: Tech lead → Benedetta → Alessandra
- ☑️ Tracking: PROGRESS_DAILY.md aggiornato ogni giorno

### **9️⃣ Q&A APERTE** (5 min)
**Chi**: Tutti  
- Marco: "Domande?"
- Agenti: "Chiarimenti su feature, scope, timeline?"

---

## 📊 COSA È PRONTO PER OGGI

✅ **Dashboard interattivo**:
- `DASHBOARD_PROGETTO.html` — 8 tab funzionali
- Agenti, Notifiche, Bacheche, Avanzamento, Richieste, Meeting, **Ricerche Online** (NUOVO)
- Tutti i 21 agenti pre-caricati
- Auto-save in localStorage

✅ **Documentazione completa**:
- `README.md` — Overview progetto
- `ORGANIGRAMMA_TEAM.md` — Struttura team + responsabilità
- `TEAM_GIORGIA.md` — Dettagli team business
- `KICK-OFF_CHECKLIST.md` — Preparazione incontro
- `RESEARCH_PLAN_GIORGIA_TEAM.md` — Piano ricerche (scadenza 18:00)
- `GUIDA_RICERCHE_ONLINE.md` — Come salvare ricerche
- `GUIDA_DASHBOARD.md` — Tutorial dashboard

✅ **Team Structure**:
- 16 agenti Team Alessandra (6 Tech Leads + 10 junior)
- 5 agenti Team Giorgia
- Descrizioni complete per ogni agente
- Skill per ogni agente

---

## 🎯 DURANTE IL KICK-OFF

### **Alessandra (ALE)**:
- Presenta visione + timeline
- Introduce Team Leads
- Sottolinea: Schema dati (Benedetta) è CRITICO Week 1
- Confirm: Tutti capiscono flussi dati

### **Benedetta (BeneD)**:
- Mostra architettura (15 min talk)
- Sottolinea: JSON è ponte universale
- Specifica: "Voi iniziate DOPO schema dati finito"

### **Tech Leads**:
- Brevemente presentano team e ruolo
- Ascoltano dipendenze da altri team

### **Giorgia (GIO)**:
- Presenta Team Giorgia (5 agenti)
- Spiega ricerche online (scadenza 18:00)
- Specifica: Dashboard → tab "Ricerche Online"

### **Tutti gli Agenti**:
- Capiscono il loro ruolo
- Sanno cosa fare Week 1
- Hanno link a documentazione

---

## 🔴 BLOCCHI CRITICI WEEK 1

**Benedetta DEVE finire schema dati entro giovedì**:
- Se no → tutti gli altri team bloccati
- Team Natalia, Irene, Elisa aspettano schema dati

**Action**: Se Benedetta ha dubbi → escalate immediatamente a Alessandra

---

## 📋 POST-KICK-OFF (Subito dopo)

### **14:30-15:10 (Setup)**:
- [ ] Alessandra apre link dashboard per team
- [ ] Giorgia apre link dashboard per team
- [ ] Tutti agenti possono accedere

### **15:10-17:30 (Ricerche Online)**:
- [ ] Ogni agente va in tab "📚 Ricerche Online"
- [ ] Seleziona il suo nome
- [ ] Salva ricerche (1-2 fonti autorevoli ciascuno)
- [ ] Riassunto max 300 battute

### **17:30-17:45**:
- [ ] Ultimo agente upload ricerca
- [ ] Giorgia/Alessandra review veloce

### **18:00**:
- [ ] ✅ RICERCHE COMPLETE
- [ ] Dashboard aggiornato con tutte ricerche
- [ ] Pronto per domani

---

## 📱 LINK ESSENZIALI

**Dashboard**:
```
D:\progetto-alessandra\DASHBOARD_PROGETTO.html
→ Doppio click per aprire
```

**Documentazione**:
- `README.md` — Leggi per overview
- `ORGANIGRAMMA_TEAM.md` — Chi è chi
- `GUIDA_DASHBOARD.md` — Come usare dashboard
- `GUIDA_RICERCHE_ONLINE.md` — Ricerche online (leggi prima di iniziare)

**Cartelle Progetto**:
```
D:\progetto-alessandra\
├── 01-ARCHITETTURA/
├── 02-FRONTEND-3D/
├── 03-BACKEND/
├── 04-FORTRAN-SOLVER/
├── 05-RICERCA/
├── 06-TESTING/
├── 07-DOCUMENTAZIONE/
├── 08-CONFIG/
└── 09-ASSETS/
```

---

## 🎓 QUICK REFERENCE

| Ruolo | Primo Task | Scadenza |
|-------|-----------|----------|
| **Benedetta** | Schema dati JSON | Giovedì |
| **Natalia** | FastAPI setup | Venerdì |
| **Irene** | UI 3D mockup | Venerdì |
| **Elisa** | Fortran P-Delta planning | Venerdì |
| **Francesca** | Ricerca ModeSt/OpenFOAM | Mercoledì |
| **Valentina** | Test framework setup | Venerdì |
| **Aurora** | Pricing model | Mercoledì |
| **Livia** | Email templates | Martedì |
| **Veronica** | Compliance checklist | Mercoledì |
| **Camilla** | News digest weekly | Martedì |
| **Laura** | Dashboard monitoring setup | Mercoledì |

---

## ✨ FINAL NOTES

- **Non è permesso** iniziare dev senza schema dati approvato
- **Parallelo è OK**: Irene/Natalia/Elisa possono prep mentre BeneD finisce schema
- **Comunicazione è tutto**: Se qualcosa non è chiaro, chiedi SUBITO
- **Alessandra è arbitro**: Litigio tra team → ALE decide

---

**GOOD LUCK! 🚀**

_Kick-off document prepared: 2026-08-15_
