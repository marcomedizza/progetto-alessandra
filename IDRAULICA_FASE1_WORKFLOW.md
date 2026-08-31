# 🌊 IDRAULICA Fase 1 — Workflow Intensive (31 AGO - 5 SET)

**Fase:** Fase 1 Intensive  
**Periodo:** 30 agosto - 5 settembre 2026 (7 giorni, sabato no intensive)  
**Destinatari:** 3-4 specialisti Idraulica  
**Intensità:** 4-5 ore/giorno (8:30-12:30 + 14:00-17:00)  
**Responsabili:** Roberta (coord), Beatrice (supporto teorico), Agata (risorse)  
**Status:** PRONTO PER LAUNCH

---

## 🎯 Obiettivo Fase 1

**Trasformare specialisti da ramp-up generico → ESPERTI OPERATIVI Idraulica**

Entro Venerdì 5 settembre, ogni specialista deve:
- ✅ Padronanza concetti Belluzzi Cap 1-5 (proprietà fluidi, statica, cinematica, Bernoulli, perdite)
- ✅ Capacità applicare teoria a problemi reali (4 case study completati)
- ✅ Competenza risolvere esercizi pratici (25 esercizi svolti + 5 aggiuntivi)
- ✅ Readiness per FASE 2 (Idraulica applicata a progetto Alessandra)

---

## 📥 MATERIALI STUDIO (JSON-TO-BE)

**3 documenti in RIFERIMENTI/input/ pronti per conversione JSON:**

### **1. IDRAULICA_FASE1_CONCETTI_FONDAMENTALI.md**
- **Capitoli Belluzzi:** 1-5 (proprietà fluidi, statica, cinematica, Bernoulli, perdite)
- **Lunghezza:** ~3,000 parole
- **Formato JSON sarà:**
  ```json
  {
    "metadata": { "phase": 1, "type": "conceptual_foundations", "days": "1-5" },
    "chapters": [
      { "id": 1, "title": "Proprietà Fluidi", "topics": [...], "exercises": [...] },
      ...
    ]
  }
  ```
- **Per chi:** Tutti e 3-4 specialisti
- **Quando:** Distribuito lunedì 31 agosto mattina

### **2. IDRAULICA_CASI_STUDIO_PROGETTI_REALI.md**
- **4 case study:** Acquedotto urbano, diga irrigua, spillway, pompa centrifuga
- **Lunghezza:** ~2,500 parole
- **Formato JSON sarà:**
  ```json
  {
    "metadata": { "type": "real_world_applications", "cases": 4 },
    "cases": [
      { "id": 1, "name": "Urban Aqueduct", "problem": {...}, "solution": {...} },
      ...
    ]
  }
  ```
- **Per chi:** Tutti e 3-4 specialisti (assegnazione case per specialità)
- **Quando:** Distribuito martedì 1 settembre

### **3. IDRAULICA_ESERCIZI_INTENSIVO.md**
- **25 esercizi totali:** 5/giorno × 5 giorni (lunedì-venerdì)
- **Lunghezza:** ~2,000 parole + solutions
- **Formato JSON sarà:**
  ```json
  {
    "metadata": { "type": "daily_exercises", "days": 5, "total_exercises": 25 },
    "days": [
      { "day": 1, "date": "2026-08-31", "topic": "Properties & Statics", "exercises": [...] },
      ...
    ]
  }
  ```
- **Per chi:** Tutti e 3-4 specialisti (stessi esercizi per omogeneità)
- **Quando:** Distribuito OGGI (31 agosto), con schedule daily

---

## 🔄 TIMELINE CONVERSIONE & DISTRIBUZIONE

### **OGGI (31 AGOSTO) — Automazione & Distribution Start**

**08:00** — Sistema automazione avvia conversione
```
RIFERIMENTI_AUTOMAZIONE_DAILY.py esegue:
- Legge 3 file IDRAULICA da RIFERIMENTI/input/
- Converte a JSON via Claude API
- Cataloga in RIFERIMENTI/catalogo/
- Genera AGATA_REPORT_20260831.json
```

**10:00** — Agata riceve report
```
AGATA_REPORT_20260831.json contiene:
[
  {
    "source": "IDRAULICA_FASE1_CONCETTI_FONDAMENTALI.md",
    "json": "IDRAULICA_FASE1_CONCETTI_FONDAMENTALI.json",
    "status": "ready_for_distribution"
  },
  ... (altri 2 file)
]
```

**10:30** — Agata verifica & cataloga
- Controlla JSON è valido (syntax, structure)
- Identifica soggetti: Specialisti Idraulica (3-4 agenti)
- Aggiorna DISTRIBUZIONE_LOG.json
- Prepara 3 email (una per documento)

**11:00** — Agata distribuisce ai specialisti
```
Email 1 (subito):
  Subject: [Intensive Idraulica] Concetti Fondamentali (JSON)
  Body: Attachment: IDRAULICA_FASE1_CONCETTI_FONDAMENTALI.json
  To: agente_hydro_001, agente_hydro_002, agente_hydro_003, (agente_hydro_004 if available)

Email 2 (domani mattina, 1 settembre):
  Subject: [Intensive Idraulica] Casi Studio Progetti Reali (JSON)
  Body: Attachment: IDRAULICA_CASI_STUDIO_PROGETTI_REALI.json

Email 3 (domani mattina, 1 settembre):
  Subject: [Intensive Idraulica] Esercizi Daily (JSON)
  Body: Attachment: IDRAULICA_ESERCIZI_INTENSIVO.json
```

**11:30** — Roberta (Team Lead Strutturale) invia briefing

```
Specialisti Idraulica,

Fase 1 Intensive inizia LUNEDÌ 30 AGOSTO alle 08:30 (OGGI!)

Avete ricevuto 3 file JSON con tutto materiale studio:
1. Concetti Fondamentali (5 capitoli Belluzzi)
2. Casi Studio (4 progetti reali)
3. Esercizi (25 problema-solution + explanation)

SCHEDULE:
- Lunedì 31 ago: Cap 1-2 (Proprietà, Statica) + 5 esercizi
- Martedì 1 set: Cap 3-4 (Cinematica, Bernoulli) + 5 esercizi
- Mercoledì 2 set: Cap 5 (Perdite) + casi studio 1-2 + 5 esercizi
- Giovedì 3 set: Casi studio 3-4, approfondimento specialistica + 5 esercizi
- Venerdì 4 set: Integrazione totale, mini-progetto + 5 esercizi aggiuntivi

SUPPORTO:
- Beatrice: Domande teoriche su Belluzzi (Slack @beatrice, email, 2h max response)
- Agata: Problemi tecnici accesso file (Slack #resources)
- Roberta: Coordinamento daily, check-in mattina e sera

BELLUZZI + JSON:
- Physical book è ancora riferimento principale
- JSON files aggiungono: struttura, formule, esempi, esercizi
- Leggi entrambi in parallelo

Siete brillanti. Intensive sarà intenso ma doable. 4-5 ore/giorno, supporto totale.

Iniziamo con confidence! 💪

—Roberta (Team Lead, Strutturale)
```

**14:00** — Daily check-in Roberta con specialisti (Slack)
```
Roberta: Come state? Belluzzi arrivatə? JSON file accessibility OK?
Agente_hydro_001: Tutto ricevuto, inizio stasera concetti fondamentali
Agente_hydro_002: JSON aperto, è structured bene, capisco formato
Agente_hydro_003: Belluzzi in mano fisico, JSON su drive. Pronto.
[Agente_hydro_004]: [Se entra nel team]
```

**18:00** — Agata final check
- Tutti e 3-4 specialisti confermato ricezione? ✓
- Accesso JSON OK per tutti? ✓
- Belluzzi fisico è arrivato per intensive? ✓
- Supporto 24/7 setup pronto? ✓

**Serata (19:00-21:00)** — Specialisti iniziano LETTURA PREPARATORIA
- Leggere Introduzione IDRAULICA_FASE1_CONCETTI_FONDAMENTALI.json
- Aprire Belluzzi Cap 1 (fisico)
- Check comprensione terminologia base
- Domande teoriche → Beatrice (Slack message, response domani mattina)

---

## 📅 SCHEDULE GIORNALIERO (1-5 SETTEMBRE)

### **Lunedì 31 Agosto (OGGI)** — Ramp-up & Setup

**08:30 — Lancio Ufficiale**
```
Roberta in Slack #idraulica-intensive:
"Buongiorno specialisti. Fase 1 Intensive inizia ORA.
Contenuti JSON sono pronti. Belluzzi è in mano.
Obiettivo: padronanza Cap 1-5 + 4 case study + 25 esercizi entro venerdì.
Iniziamo con Cap 1 (Proprietà fluidi).
Domande? → Beatrice
Accesso problemi? → Agata
Coordinamento? → Roberta
Siete brillanti!"
```

**09:00-12:30 — Studio Cap 1 (Proprietà Fluidi)**
- Lettura Belluzzi Cap 1 (fisico)
- Parallelo: IDRAULICA_FASE1_CONCETTI_FONDAMENTALI.json → Sezione 1
- Focus: Densità, viscosità, pressione
- Domande: Beatrice disponibile per chiarificazioni

**14:00-17:00 — Esercizi Day 1**
- Svolgere 5 esercizi Day 1 (IDRAULICA_ESERCIZI_INTENSIVO.json)
- Verificare soluzioni (provided in JSON)
- Compare metodologia tra specialisti (Slack thread sharing)

**17:30 — Check-in Sera Roberta**
```
Roberta: Come è andata giornata 1?
Agente_hydro_001: Bene, Cap 1 è chiaro. Esercizi 4/5 risolti, 1 dubbio su viscosità
Roberta: Beatrice ha risposto? Se no, escalate.
[Beatrice si attiva se domanda è rimasta in sospeso]
```

**18:00 — Report Automatico Agata**
- Tracked: Tutti specialisti hanno accesso JSON? ✓
- Tracked: Belluzzi fisico? ✓
- Supporto necessario? [Log any issues]

---

### **Martedì 1 Settembre — Cap 2-3, Casi 1-2**

**08:30 — Standup mattina**
```
Roberta: Check domande dalla ieri?
Specialisti: [Brief update]
Roberta: Oggi: Cap 2-3 (Statica, Cinematica) + Casi Studio 1-2
```

**09:00-12:30 — Cap 2-3 + Casi Studio 1-2**
- Belluzzi Cap 2: Statica fluidi (Pascal, spinta idrostatica)
- JSON Cap 2 (Idrostatica)
- Caso Studio 1: Acquedotto urbano (apply statica, continuità)
- Caso Studio 2: Diga irrigua (spinta idrostatica calculations)

**14:00-17:00 — Esercizi Day 2**
- 5 esercizi Day 2 (Esercizi_Intensivo.json)
- Topic: Reynolds, continuità, Bernoulli basics

**17:30-18:00 — Check-in sera + Report**

---

### **Mercoledì 2 Settembre — Cap 4-5, Casi 3-4**

**09:00-12:30 — Cap 4-5**
- Belluzzi Cap 4: Bernoulli equation (energy equation)
- JSON Cap 4 (Dinamica dei Fluidi)
- Belluzzi Cap 5: Perdite di carico (Darcy-Weisbach)
- JSON Cap 5 (Perdite)

**14:00-15:00 — Casi Studio 3-4**
- Caso 3: Spillway (sfioratore) - energia, cavitazione
- Caso 4: Pompa centrifuga - Bernoulli + perdite

**15:00-17:00 — Esercizi Day 3**
- 5 esercizi Day 3 (Perdite, Bernoulli applications)

---

### **Giovedì 3 Settembre — Approfondimento Specialistico**

**Ogni specialista approfondisce sua sub-specialità:**

Se specialista focus **Idraulica Urbana** (acquedotti):
- Rilegge Caso 1 (Acquedotto) in dettaglio
- Applica formule a varianti (diametri diversi, portate diverse)
- Sviluppa mini-calcolo per rete locale (se esiste dati reali)

Se specialista focus **Idraulica Strutturale** (dighe, spillway):
- Rilegge Casi 2-3 (Dighe, spillway)
- Calcoli stabilità per geometrie diverse
- Analisi cavitazione

Se specialista focus **Impianti Idraulici** (pompe, distribuzione):
- Approfondisce Caso 4 (Pompe)
- Curve caratteristiche pompe (consultare cataloghi reali)
- Punto di funzionamento per sistemi diversi

**14:00-17:00 — Esercizi Day 4 + Case-Specific Problems**
- 5 esercizi standard
- 3-5 esercizi aggiuntivi per specialità (customizzati)

---

### **Venerdì 4 Settembre — Integrazione & Assessment**

**08:30-12:30 — Mini-Progetto Integrativo**
- Scenario: Progettare mini-acquedotto completo
- Inputs: quota sorgente, quota distribuzione, portata, distanza
- Outputs: diametro tubo, perdite, pressione, eventuale pompa, costi energetici
- Methodo: applica Bernoulli + Darcy-Weisbach + continuità
- Tempo: 3-4 ore

**14:00-16:00 — Group Review**
- Specialisti presentano soluzioni mini-progetto
- Compare approaches, metodologie
- Beatrice fornisce feedback su correttezza fisica
- Identifica "best practices" per phase 2

**16:00-17:00 — Debrief Roberta + Ginevra (QA)**
```
Roberta: Come è andata settimana intensiva?
Specialisti: [Reflection on learning, confidence level]
Ginevra: Sono pronti per Fase 2 operativa (applicazione al progetto)?
Beatrice: Hanno capito concetti? Gaps da colmare?

Assessment criteria:
- ✓ Capiscono Belluzzi Cap 1-5
- ✓ Sanno applicare theory a problemi reali
- ✓ Risolvono esercizi senza errori concettuali
- ✓ Pronti per applicazione a progetto Alessandra (next week)
```

**17:30 — Report Finale Fase 1**
```
FASE 1 INTENSIVE — ASSESSMENT FINALE
Data: 4 settembre 2026, ore 17:00
Specialisti: [Nomi] × 3-4
Risultato: ✅ PRONTO PER FASE 2 / ⚠️ CAUTION / ❌ RETRAINING NEEDED

- Concetti Belluzzi: Masterizzati ✓
- Case Study: Applicati correttamente ✓
- Esercizi: 24/25 svolti correttamente ✓
- Confidence: 8/10 (da rampup assoluto a competenza operativa)

Prossimo step: Fase 2 applicazione (6 settembre in poi)
Supporto continuo: Beatrice + Agata + Roberta (daily)
```

---

## 🔗 Integrazione Belluzzi + JSON

**Belluzzi Fisico è FONTE DI VERITÀ**
- Letture primarie dal libro
- Diagrammi, figure, tabelle da Belluzzi
- Numero di pagina = reference unico

**JSON è SUPPLEMENT STRUTTURATO**
- Rinforza concetti chiave con riassunto
- Aggiunge formule in formato computabile
- Fornisce esercizi + soluzioni (non in Belluzzi)
- Struttura gerarchica (facile navigazione)

**Strategia Studio:**
```
Belluzzi Cap X → Leggi 20-30 min (physical book)
           ↓
JSON Cap X → Riasunto, rinforzo (10-15 min su JSON)
           ↓
Esercizi → Applica concetti (30-45 min, solve problems)
           ↓
Case Study → Integra tutto (60-90 min, real-world application)
```

---

## 👥 Supporto & Coordinamento

### **Roberta (Team Lead Strutturale)**
- **Ruolo:** Coordinamento, motivazione, check-in giornaliero
- **Responsabilità:** Standup 08:30, briefing, evening debrief
- **Disponibilità:** Business hours + su-demand emergencies
- **Canale:** Slack #idraulica-intensive, @roberta

### **Beatrice (Supporto Teorico)**
- **Ruolo:** Q&A supporto, chiarificazioni concetti Belluzzi
- **Responsabilità:** Rispondere domande teoriche in 2h max
- **Disponibilità:** 08:00-18:00 business hours (eventuali escalation)
- **Canale:** Slack @beatrice, email beatrice@...

### **Agata (Risorse Infrastruttura)**
- **Ruolo:** Accesso file, backup, support tecnico
- **Responsabilità:** JSON accessible 100%, backup se link breaks
- **Disponibilità:** 24/7 for critical issues
- **Canale:** Slack #resources

### **Ginevra (QA Strutturale)**
- **Ruolo:** Assessment, verification correttezza soluzioni
- **Responsabilità:** Friday debrief, assessment finale
- **Disponibilità:** Daily check (se needed), Friday full-day
- **Canale:** Slack #idraulica-intensive

---

## 📊 Metriche Successo Fase 1

**Giornaliera:**
- ✅ 100% specialisti presenti (4-5 ore/giorno)
- ✅ 100% capiscono lezione del giorno
- ✅ 80%+ esercizi risolti correttamente
- ✅ Zero escalation critiche (accesso problemi, mancanza risorse)

**Settimanale:**
- ✅ Tutti Cap 1-5 completati
- ✅ 4 case study applicati
- ✅ 25 esercizi risolti (90%+ accuracy)
- ✅ Mini-progetto integrativo svolto da ogni specialista
- ✅ Confidence level 7-8 / 10

**Fine Fase 1:**
- ✅ Specialisti sono ESPERTI (non ramp-up) in Idraulica teoria
- ✅ Pronti per Fase 2 (applicazione a progetto Alessandra)
- ✅ Zero skill gap da ricuperare

---

## 🚀 Fase 2 Prossima (6 settembre+)

**Idraulica Applicata al Progetto Alessandra:**
- Input: Progetto strutturale (CAD, carichi, geometria)
- Output: Analisi idraulica integrata (pressioni, flussi, dimensionamenti)
- Strumenti: Formulazioni Belluzzi + tools computazionali
- Timeline: 4 settimane (6 set - 3 ott)

**Supporto Fase 2:**
- Beatrice: Continuous availability
- Roberta: Daily coordination
- Agata: Risorse supplementari (cataloghi pompe, curve caratteristiche, etc)
- Ginevra: Weekly reviews + sign-off

---

## 📋 Checklist Pre-Launch (Oggi 31 Agosto)

- [ ] 3 file IDRAULICA in RIFERIMENTI/input/ (done)
- [ ] Automazione JSON conversion scheduled (cron setup)
- [ ] Agata riceve report & distribuisce (10:30-11:30)
- [ ] Belluzzi fisico consegnato a specialisti (done: verified)
- [ ] Roberta briefing inviato (11:00)
- [ ] Specialisti confermato ricezione (11:30-12:00)
- [ ] First day (lunedì) materials da studiare (Cap 1 + 5 esercizi)
- [ ] Beatrice availability confirmed per Q&A
- [ ] Ginevra calendar blocked per daily check-in
- [ ] Slack channel #idraulica-intensive attivo

---

**Status:** ✅ FASE 1 INTENSIVE PRONTA PER LAUNCH  
**Data:** 31 agosto 2026  
**Soggetto:** 3-4 Specialisti Idraulica  
**Responsabile:** Roberta (Coordinamento)  
**Inizio:** Lunedì 31 agosto 2026, 08:30

**Siamo pronti. Iniziamo con confidence.** 💪

