# 📊 GUIDA DASHBOARD INTERATTIVO

**File**: `DASHBOARD_PROGETTO.html`  
**Apertura**: Doppio click su file (apre in browser)  
**Memorizzazione**: Dati salvati localmente (localStorage del browser)

---

## 🎯 FUNZIONALITÀ PRINCIPALI

### 1️⃣ **DASHBOARD** (Tab Principale)
Visualizza snapshot rapido del progetto:
- 📊 Statistiche: Agenti totali, task attivi, % completamento
- 📅 Prossime milestone
- 🔔 Notifiche recenti

---

### 2️⃣ **AGENTI** (👩‍💼 Team)
Elenco completo dei 21 agenti diviso in:
- **Team Alessandra** (16) — Sviluppo tecnico
  - Project Lead + 6 Tech Lead + Junior team
- **Team Giorgia** (5) — Business operations
  - Business Lead + 4 specialisti

Stato visualizzato:
- 🟢 **Attivo** — Pronto a lavorare
- 🟡 **In Attesa** — Prossimamente

---

### 3️⃣ **NOTIFICHE** (🔔)
Gestione notifiche complete:
- ➕ **Aggiungi Notifica** — Crea nuova notifica
- **Priorità**: Low, Medium, High
- 🗑️ **Rimuovi** — Cancella notifica
- **Automazione**: Visualizza in dashboard

**Esempio notifiche**:
```
🔔 Schema Dati Completato (MEDIUM)
   Benedetta ha terminato lo schema dati JSON
```

---

### 4️⃣ **BACHECHE** (📌)
Due bacheche separate:

#### **Bacheca Pubblica** (Visibile a tutti)
- Posta da te (Marco) visibile a team
- Annunci, comunicati, aggiornamenti

#### **Bacheca Privata** (Solo tu)
- Appunti personali
- Note private
- Traccia privata

**Come usare**:
1. Scrivi nel textarea
2. Clicca "Pubblica"
3. Post appare in elenco (più recente in alto)
4. Rimuovi quando finito

---

### 5️⃣ **AVANZAMENTO** (📈)
Tracking visuale progetto:
- Fase 1: Planning & Spec (Week 1)
- Fase 2: Core Development (Week 2-4)
- Fase 3: Integration (Week 4-6)

**Milestone**:
- ✓ Schema Dati Finalizzato — 19/08/2026
- ✓ Alpha Release — 02/09/2026
- ✓ Beta Release — 16/09/2026

**Interazione**:
- Clicca "Segna Completato" per finire milestone
- Clicca "Riporta In Progress" per riaprire
- ➕ Aggiungi nuove milestone

---

### 6️⃣ **RICHIESTE** (📝)
Due sezioni:

#### **Richieste Agenti**
Richieste dirette ai singoli agenti:
1. Seleziona agente (dropdown)
2. Descrivi richiesta
3. Clicca "Invia Richiesta"

**Esempio**:
```
→ A: Benedetta
"Puoi aggiornare schema dati con sezioni precompresse?"
```

#### **Le Tue Richieste**
Richieste tue agli agenti:
1. Seleziona priorità (Normale/Alta/Urgente)
2. Scrivi richiesta
3. Clicca "Invia"

---

### 7️⃣ **MEETING** (🤝)
Resoconti riunioni (max 300 battute per resoconto):

**Come compilare**:
1. Seleziona **data** (auto-popolato con oggi)
2. Seleziona **partecipanti**:
   - Team Alessandra
   - Team Giorgia
   - Tutti
   - Alessandra & Giorgia
3. Scrivi **resoconto** (contatore live: 0/300)
4. Clicca "Salva Resoconto"

**Formato resoconto** (esempio):
```
📅 2026-08-16 - Alessandra & Giorgia
Discusso: architettura, timeline, rischi.
Decisioni: Schema dati entro giovedì, API spec entro venerdì.
Next: Review architettore, feedback Natalia.
```

---

## 🎮 COME USARE

### Apertura File
1. Vai in `D:\progetto-alessandra\`
2. Doppio click su `DASHBOARD_PROGETTO.html`
3. Apre automaticamente in browser

### Navigation
- Clicca i **tab in alto** per cambiare sezione
- I dati si salvano **automaticamente** (localStorage)
- Aggiorna browser: **i dati rimangono** 💾

### Data Persistence
- Tutti i dati salvati localmente nel browser
- Non vanno persi se chiudi il tab
- Se svuoti cache del browser → dati cancellati

---

## 💡 BEST PRACTICE

### Dashboard Quotidiano
1. **Mattina (09:00)**: Apri dashboard, leggi notifiche, milestone
2. **Pomeriggio (15:00)**: Aggiungi notifiche per team leads
3. **Sera (17:00)**: Compila resoconti meeting, richieste

### Per Agenti
1. Controlla **tab Richieste** → nuove richieste a loro indirizzo
2. Rispondono scrivendo su **Bacheca Pubblica**
3. Tu puoi tracciare in **Dashboard**

### Coordinamento Ale ↔ Gio
1. **16:00 quotidiano** (Week 3+):
   - Leggi **Progress Monitor** (Laura)
   - Clicca tab **Avanzamento** per stato
   - Aggiungi **Notifiche** se blocchi
   - Compila **Richieste** se serve supporto

---

## 📋 STATISTICHE

**Dashboard mostra**:
- 📊 **21 Agenti Totali** (16 Ale + 5 Giorgia)
- 📈 **% Completamento** — Aggiornato con milestone
- 📅 **Prossime 3 Milestone**

---

## 🔒 PRIVACY

- **Bacheca Pubblica**: Visibile a tutti i team
- **Bacheca Privata**: Solo tu (Marco)
- Notifiche: Visualizzate in dashboard (tutte)
- Meeting: Salvati con date e partecipanti

---

## ⚡ SCORCIATOIE

| Azione | Dove |
|--------|------|
| Vedi stato progetto | Tab **Dashboard** |
| Traccio agenti | Tab **Agenti** |
| Ricordo importa | Tab **Bacheche** (privata) |
| Richieste urgenti | Tab **Richieste** → Priorità Alta |
| Milestone scadenze | Tab **Avanzamento** |
| Resoconto riunione | Tab **Meeting** |

---

## 🐛 TROUBLESHOOTING

**Q: Dati non si salvano?**  
A: Controlla se localStorage è abilitato nel browser. Prova altro browser.

**Q: Voglio cancellare tutto?**  
A: Apri Console (F12) e digita: `localStorage.clear()`

**Q: Come esporto dati?**  
A: Seleziona tutto (Ctrl+A) dalla Console, salva come testo. Futura versione avrà export CSV.

---

## 🎯 PROSSIME FEATURE (Futura)

- 📊 Grafici avanzati (Gantt, burn-down)
- 📥 Import/Export CSV
- 👥 Assegnazione task agli agenti
- 🔔 Notifiche push
- 📧 Integrazione email
- 🌍 Versione cloud (futura)

---

**Creato**: 2026-08-15  
**Ultimo aggiornamento**: 2026-08-15  
**Versione**: 1.0 (MVP)

_Buon lavoro! 🚀_
