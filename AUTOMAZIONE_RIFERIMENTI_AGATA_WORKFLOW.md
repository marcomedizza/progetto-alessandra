# 📦 Agata Workflow — JSON Catalogo & Distribuzione

**Data:** 31 agosto 2026  
**Destinatario:** Agata (Infrastructure Orchestrator)  
**Origine:** RIFERIMENTI Automazione System  
**Scopo:** Ricevi JSON convertiti, cataloga, distribuisci ai soggetti di riferimento

---

## 🔄 Workflow Completo

```
AUTOMAZIONE (Daily 08:00)
    ↓
Genera JSON + Catalogo + Report
    ↓
AGATA riceve notifica di report pronto
    ↓
[1] Leggi AGATA_CATALOGO_MASTER.json
[2] Verifica struttura JSON output
[3] Determina soggetto di riferimento per ogni file
[4] Cataloga nel sistema di tracking
[5] Comunica distribuzione ai soggetti
[6] Traccia ricezione e conferma lettura
    ↓
SOGGETTI DI RIFERIMENTO
Ricevono JSON strutturato per lettura/studio
```

---

## 📥 STEP 1: Ricevi Report

**Quando riceverai:** Daily, dopo automazione (default 08:00)  
**Dove trovarla:** `RIFERIMENTI/catalogo/AGATA_REPORT_*.json`  
**Come verificare:** Check email o Slack #resources

**Report conterrà:**
```json
{
  "date": "2026-08-31T14:00:00",
  "title": "Nuove Conversioni Testo → JSON Pronte per Distribuzione",
  "count": 2,
  "conversions": [
    {
      "source": "DOCUMENTO_A.md",
      "json": "DOCUMENTO_A.json",
      "catalog": "DOCUMENTO_A_catalog.json"
    },
    {
      "source": "DOCUMENTO_B.md",
      "json": "DOCUMENTO_B.json",
      "catalog": "DOCUMENTO_B_catalog.json"
    }
  ]
}
```

---

## 🔍 STEP 2: Leggi Catalogo Master

**File:** `RIFERIMENTI/catalogo/AGATA_CATALOGO_MASTER.json`

Per ogni conversione, leggi:
- `source_file` — Documento originale (per context)
- `json_file` — File JSON convertito (in RIFERIMENTI/output/)
- `conversion_date` — Quando è stato convertito
- `status` — Dovrebbe essere "ready_for_distribution"

---

## ✅ STEP 3: Verifica Struttura JSON

**Per ogni JSON file:**

```bash
# Leggi JSON
cat RIFERIMENTI/output/{json_file}

# Verifica è valido
python3 -m json.tool RIFERIMENTI/output/{json_file} > /dev/null && echo "✅ JSON valido" || echo "❌ JSON non valido"
```

**Checklist verifica:**
- [ ] JSON è syntatticamente valido
- [ ] Ha campo `metadata` con versione, data, source
- [ ] Ha campo `data` o equivalente con contenuto strutturato
- [ ] Tutte stringhe, numeri, date, array sono corretti
- [ ] Nessun campo `null` o vuoto non atteso

**Se problema trovato:**
- Contatta Alessandra con dettagli
- Non distribuire se struttura è dubbia

---

## 🎯 STEP 4: Determina Soggetto di Riferimento

**Per ogni JSON, identifica chi deve leggerlo:**

### **Matrice Assegnazione**

| Tipo Documento | Soggetto Riferimento | Disciplina |
|---|---|---|
| **Belluzzi** (Idraulica) | Specialisti Idraulica (3-4 agenti) | Idraulica |
| **Leonhardt** (Strutturale) | Agenti Strutturale (8) | Strutturale |
| **Timoshenko** (Elasticità) | Agenti Strutturale avanzato (4-5) | Strutturale |
| **Terzaghi** (Geotecnica) | Agenti Strutturale geotecnica (2-3) | Strutturale |
| **Articoli Tech** | Agenti Tech (12) | Tech/Architettura |
| **Documenti Business** | Agenti Business (6) | Business/Economia |
| **Case Studies** | Team specifico (varia) | Varia |
| **Altro** | Contatta Alessandra | TBD |

### **Come Determinare:**

1. **Leggi filename JSON** — di solito include disciplina o soggetto
2. **Controlla metadata.description** — specifica cui è destinato
3. **Se non chiaro** — contatta Alessandra prima di distribuire

---

## 📋 STEP 5: Cataloga nel Sistema

**Crea entry di tracking per ogni distribuzione:**

### **Template:** `RIFERIMENTI/catalogo/DISTRIBUZIONE_LOG.json`

```json
{
  "data": "2026-08-31T14:30:00",
  "catalog_entries": [
    {
      "id": "distr_20260831_001",
      "source_file": "DOCUMENTO_A.md",
      "json_file": "DOCUMENTO_A.json",
      "soggetto_riferimento": "Specialisti Idraulica",
      "destinatari": ["agente_001", "agente_002", "agente_003"],
      "status": "ready_to_send",
      "data_distribuzione_prevista": "2026-08-31T15:00:00",
      "metodo_distribuzione": "email",
      "note": "Parte di Fase 1 intensive"
    },
    {
      "id": "distr_20260831_002",
      "source_file": "DOCUMENTO_B.md",
      "json_file": "DOCUMENTO_B.json",
      "soggetto_riferimento": "Agenti Tech",
      "destinatari": ["tech_001", "tech_002", "tech_003", "tech_004", "tech_005", "tech_006", "tech_007", "tech_008", "tech_009", "tech_010", "tech_011", "tech_012"],
      "status": "ready_to_send",
      "data_distribuzione_prevista": "2026-08-31T16:00:00",
      "metodo_distribuzione": "drive_link",
      "note": "Per studio settimanale"
    }
  ]
}
```

**Aggiorna questo file per ogni nuovo batch di conversioni.**

---

## 📧 STEP 6: Comunica Distribuzione

### **Email Template a Soggetti Riferimento:**

**Subject:** `[Risorse Learning] Nuovo Material JSON — {Tipo Documento}`

```
Caro/a [SOGGETTO/AGENTE],

Da parte della Automazione Risorse (Agata), hai nuovo materiale disponibile per 
studio/lettura nella forma JSON strutturata:

DOCUMENTO: {source_file}
FORMATO: JSON (machine-readable + human-readable)
COME ACCEDERE:
- Opzione A: Email allegato (se file piccolo)
- Opzione B: Drive link (se file grande)
- Opzione C: Repo clone (se in git)

ISTRUZIONI DI LETTURA:
1. Apri file JSON con editor (VS Code, Sublime, etc)
2. O parse con Python/Node per uso programmatico
3. Structura è conforme a SCHEMA_DATI_ALESSANDRA

SUPPORTO:
Se hai problemi accesso o domande su contenuto:
→ Contatta Agata (Slack #resources)
→ Contatta Beatrice per supporto teorico

Buona lettura! 💪

—Agata (Infrastructure Orchestrator)
```

### **Metodi Distribuzione:**

| Metodo | Quando usare | Pros | Cons |
|---|---|---|---|
| **Email allegato** | File < 5MB | Immediato, semplice | Limite size |
| **Drive link** | File 5-100MB | No size limit, versioning | Accesso richiesto |
| **Repo (Git)** | Documentazione tecnica | Integration, history | Setup necessario |
| **Slack file upload** | File piccoli | Team visibility | Size limit 20MB |

---

## ✔️ STEP 7: Traccia Ricezione & Conferma

### **Tracking Checklist:**

**Per ogni soggetto di riferimento:**
- [ ] Email/notifica inviata?
- [ ] Agente ha confermato ricezione?
- [ ] Agente ha apertο file?
- [ ] Agente ha iniziato lettura/studio?
- [ ] Date completion prevista annotata

### **Follow-up se no ricezione:**

1. **Dopo 2 ore:** Check Slack — agente ha domande?
2. **Dopo 24 ore:** Se silenzio, invia reminder gentle
3. **Dopo 48 ore:** Escalate a Alessandra se agente non responsive
4. **Nota:** Se agente dice "non trovo file" → Agata risolve accesso issue

---

## 📊 Esempio Completo — Distribuzione Idraulica

**Scenario:** 31 agosto, Automazione converte "BELLUZZI_CAP1_5_SUMMARY.md" a JSON

### **1. Agata riceve report**
```json
{
  "conversions": [
    {
      "source": "BELLUZZI_CAP1_5_SUMMARY.md",
      "json": "BELLUZZI_CAP1_5_SUMMARY.json"
    }
  ]
}
```

### **2. Agata verifica JSON**
```bash
cat RIFERIMENTI/output/BELLUZZI_CAP1_5_SUMMARY.json
# ✅ Struttura OK
```

### **3. Agata identifica soggetti**
- Documento: Belluzzi (Idraulica)
- Soggetti: 3-4 specialisti Idraulica
- Destinatari: agente_hydro_001, agente_hydro_002, agente_hydro_003

### **4. Agata cataloga**
```json
{
  "id": "distr_20260831_hydro",
  "source_file": "BELLUZZI_CAP1_5_SUMMARY.md",
  "json_file": "BELLUZZI_CAP1_5_SUMMARY.json",
  "soggetto_riferimento": "Specialisti Idraulica",
  "destinatari": ["agente_hydro_001", "agente_hydro_002", "agente_hydro_003"],
  "status": "ready_to_send"
}
```

### **5. Agata distribuisce**
```
Email a 3 specialisti:
Subject: [Risorse Learning] Belluzzi Caps 1-5 (JSON)
Body: Vedi template sopra
Allegato: BELLUZZI_CAP1_5_SUMMARY.json (o Drive link)
```

### **6. Agata traccia**
```
- 14:45 — Email inviata a 3 agenti
- 14:50 — agente_hydro_001 conferma ricezione ✅
- 15:00 — agente_hydro_002 conferma ricezione ✅
- 15:15 — agente_hydro_003 silenzio (reminder inviato)
- 15:45 — agente_hydro_003 conferma ricezione ✅
- 16:00 — Tutti hanno file, studio iniziato
```

---

## 🎯 Metriche di Successo

**Per ogni conversione/distribuzione, verifica:**

| Metrica | Target | Tracking |
|---|---|---|
| Tempo verification dopo report | < 1h | Timestamp in DISTRIBUZIONE_LOG.json |
| Tempo distribuzione dopo verification | < 2h | Email sent timestamp |
| % agenti che confermano ricezione | 100% | Note in tracking log |
| Tempo conferma dopo notifica | < 24h | Response timestamp |
| % agenti che iniziano lettura | 80%+ | Monitora Slack engagement |
| Escalation per access issues | 0 | Se sorge, Agata resolve |

---

## 📞 Escalation Path

**Se problema sorge durante workflow:**

| Problema | Azione |
|---|---|
| JSON non è valido | Contatta Alessandra + screenshot error |
| Agente non riceve file | Agata verifica indirizzo email / accesso Drive |
| Agente non accede file | Agata fornisce backup link alternativo |
| Agente ha domande su contenuto | Escalate a Beatrice (supporto teorico) |
| Agente rimane silenzioso 48h+ | Escalate a team lead (Roberta/Elisa/Katia) |

---

## 🗂️ File Organization per Agata

**Locations to monitor:**

```
RIFERIMENTI/
├── catalogo/
│   ├── AGATA_CATALOGO_MASTER.json          ← Leggi ogni mattina
│   ├── AGATA_REPORT_*.json                 ← Report daily
│   └── DISTRIBUZIONE_LOG.json              ← Tu aggiorni qui
└── output/
    └── {json_file}                         ← I file da distribuire
```

---

## 📋 Checklist Implementazione Agata

- [ ] Capisco il workflow completo (7 step)
- [ ] So dove trovare report (AGATA_REPORT_*.json)
- [ ] So dove trovare JSON output (RIFERIMENTI/output/)
- [ ] Conosco matrice assegnazione soggetti
- [ ] Ho template email per distribuzione
- [ ] Mantengo DISTRIBUZIONE_LOG.json aggiornato
- [ ] So come tracciare ricezione/conferma
- [ ] So path escalation per ogni tipo di problema
- [ ] Ho accesso a email, Drive, Slack per distribuzione
- [ ] Confermo: pronto a ricevere primo batch conversioni

---

## 🚀 Prossimi Step

**Per Alessandra:**
1. Verifica Agata capisce workflow
2. Confermato cron è setup per daily execution
3. Pronto primo test: carica documento in RIFERIMENTI/input

**Per Agata:**
1. Leggi documento complete (no skipping!)
2. Conferma capisce 7 step workflow
3. Pronto a ricevere primo report: ___________ (firma)

---

**Status:** ✅ WORKFLOW DOCUMENTED  
**Data:** 31 agosto 2026  
**Responsabile:** Agata  
**Frequenza:** Daily (a partire da 1 settembre)

