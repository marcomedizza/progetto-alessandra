# 📅 AGENDA RIUNIONE URGENTE

**Partecipanti:** Alessandra (Tech Lead), Giorgia (Business Lead), Sole (QA Director)  
**Data:** 2026-08-21  
**Ora:** 16:00 (URGENTE - ORA)  
**Durata:** 30-40 minuti  
**Formato:** Video call (preferibilmente)  
**Redatto da:** Sistema di Controllo

---

## 🎯 OBIETTIVI RIUNIONE

1. ✅ Identificare e risolvere blocco GitHub authentication
2. ✅ Verificare status dashboard mobile
3. ✅ Confermare operatività Team Controllo
4. ✅ Allineare su prossimi passi

---

## 📋 ORDINE DEL GIORNO DETTAGLIATO

### ⏱️ PARTE 1: BLOCCO CRITICO GITHUB (15 minuti)

**Responsabile:** Alessandra  

#### Situation Report:
- ❌ 16 commit pendenti da pushare
- ❌ Errore 403 Forbidden su tutti i tentativi
- ❌ Non è risolto con retry di rete
- ⚠️ Causa probabile: OAuth scope o App non abilitata

#### Domande da discutere:
1. Alessandra: È la Claude GitHub App installata per questo repo?
2. Alessandra: Quali sono gli OAuth scopes configurati?
3. Alessandra: Il repo è nel whitelist dell'app?
4. Chi ha admin access per risolvere questo?

#### Decisioni richieste:
- [ ] Chi si occupa della risoluzione?
- [ ] Timeline (oggi, domani, inizio settimana prossima)?
- [ ] Workaround nel frattempo (push via web interface)?
- [ ] Contingency plan se problema persiste?

#### Deliverables da pushare (bloccati):
```
✅ Dashboard mobile fix (CORRETTO)
✅ .gitignore (PRONTO)
✅ Team Controllo documentation (PRONTO)
✅ 13 altri commit vari (TUTTI PRONTI)
```

---

### ⏱️ PARTE 2: DASHBOARD MOBILE VERIFICATION (10 minuti)

**Responsabile:** Sole (QA), Giorgia (test)  

#### Situation Report:
- ✅ Fix implementato (data-tab attribute)
- ✅ File su Google Drive aggiornato
- ⚠️ **NON TESTATO SU DISPOSITIVI REALI**

#### Domande da discutere:
1. Sole: Hai avuto modo di testare su mobile?
2. Giorgia: Riesco ad accedere al file Drive e verificare?
3. Serve test su iOS e Android?
4. Quali device dovremmo usare per testing?

#### Test checklist (da assegnare):
- [ ] iPhone (iOS 15+)
- [ ] Android phone (Android 12+)
- [ ] iPad (tablet)
- [ ] Test navigation: Dashboard → Ricerche → Team → Timeline
- [ ] Test touch interaction (no click)
- [ ] Test on slow network

#### Responsabilità:
- Sole: Coordina test plan
- Giorgia: Esegui test su device personale
- Alessandra: Supporta con device Tech team se necessario

#### Acceptance Criteria:
- ✅ Tutti i 4 tab si aprono correttamente
- ✅ Bottoni cambiano colore quando attivi
- ✅ Nessun Javascript error (check console)
- ✅ Responsive su viewport 320px-1024px

---

### ⏱️ PARTE 3: TEAM CONTROLLO OPERATIVITÀ (10 minuti)

**Responsabile:** Sole  

#### Situazione:
- ✅ Team Controllo costituito (7 specialiste)
- ✅ Ruoli e responsabilità definiti
- ✅ Checklist quotidiana preparata
- 🟡 **NON ANCORA OPERATIVO** (github push bloccato, ma documentazione locale è OK)

#### Announcement:
```
TEAM CONTROLLO & VERIFICA — Guidato da Sole

Sole (QA Director)
├─ Marisa (QA Tech Lead)
├─ Ginevra (Structural Verification)
├─ Raffaella (Business Compliance)
├─ Vittoria (Test & Validation)
├─ Serena (Documentation & Audit)
├─ Isotta (Performance Monitor)
└─ Margherita (Integration Verifier)
```

#### Discussione:
1. Sole: Confermi la struttura del team?
2. Alessandra: OK per Marisa che monitora Tech team?
3. Giorgia: OK per Raffaella che monitora Business team?
4. Timeline start: Lunedì 25 agosto (Week 2)?
5. First monitoring task: Week 1 ricerche quality check?

#### Decision:
- [ ] Team Controllo APPROVED per operatività
- [ ] Start date confermata
- [ ] First report scheduled

---

### ⏱️ PARTE 4: PROSSIMI PASSI & ALIGNMENT (5 minuti)

**Responsabile:** Tutti  

#### Quick Status Check:

| Area | Status | Owner |
|------|--------|-------|
| GitHub Auth | 🔴 BLOCCO | Alessandra |
| Dashboard Test | ⏳ IN PROGRESS | Sole + Giorgia |
| Team Controllo | ✅ READY | Sole |
| Ricerche Online | ✅ ON TRACK | Alessandra + Giorgia |
| Compliance System | ✅ ACTIVE | Sistema |

#### Próximas acciones:
1. **Alessandra:** Risolvere GitHub auth entro 24 ore
2. **Sole:** Coordina mobile testing entro 24 ore
3. **Giorgia:** Partecipa test dashboard
4. **Tutti:** Riunione follow-up domani 16:00 se problemi non risolti

#### Communication:
- [ ] Update team via Slack/Email dopo riunione
- [ ] Shared drive con report
- [ ] Daily standup se blocchi critici

---

## 📄 ALLEGATI

**File di riferimento per riunione:**
- ✅ `REPORT_PROBLEMI_21_AGOSTO.md` — Dettagli tutti i problemi
- ✅ `TEAM_CONTROLLO_SOLE.md` — Team structure
- ✅ `TEAM_CONTROLLO_SOLE.json` — Team data
- ✅ `DASHBOARD_ALESSANDRA_MOBILE.html` — Dashboard (su Drive + locale)

---

## 🎤 TALKING POINTS

### Per Alessandra:
> "Abbiamo 16 commit pronti, tutti i file funzionano su Drive, ma il push a GitHub è bloccato da un 403 Forbidden. Sembra un problema OAuth con la Claude GitHub App. Riusciamo a risolvere oggi?"

### Per Giorgia:
> "Il dashboard mobile ha avuto problemi di navigazione, li abbiamo corretti. Serve testare su dispositivi reali (mobile/tablet) entro domani per confermare che tutto funziona."

### Per Sole:
> "Il nuovo Team Controllo è pronto (7 specialiste, structure completa, checklist preparate). Possiamo iniziare a monitorare il lavoro di Alessandra e Giorgia da lunedì. Nel frattempo, coordiniarno il test del dashboard."

---

## ✅ POST-RIUNIONE

**Azioni immediate dopo riunione:**

1. **Email di recap** a tutti i partecipanti con:
   - Decisioni prese
   - Task assegnati
   - Timeline
   - Owners

2. **Update Google Drive** con:
   - Report riunione
   - Action items list
   - Assigned owners + deadline

3. **Setup** per follow-up:
   - Riunione domani 16:00 se blocchi non risolti?
   - Or just async updates?

---

## 🔔 NOTE IMPORTANTI

- ⏰ **URGENZA:** Tutti i blocchi devono essere risolti entro Week 1 end (22 agosto)
- 📊 **VISIBILITY:** Tutti gli agenti aspettano che sistema sia completo
- 🚀 **TIMELINE:** Week 2 deve iniziare con tutto operativo

---

**Riunione preparata:** 2026-08-21 15:30  
**Convocazione:** URGENTE - Si richiede partecipazione IMMEDIATE  
**Moderatore suggerito:** Alessandra (Tech Lead)

---

*Se Alessandra ha impegni, Sole può moderare. Se Giorgia non può, Alessandra rappresenta anche Business concerns.*
