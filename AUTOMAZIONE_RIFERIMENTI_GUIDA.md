# 🔄 Automazione RIFERIMENTI → JSON → Agata

**Data:** 31 agosto 2026  
**Responsabile:** Sistema Automazione Daily  
**Destinatari:** Alessandra, Agata, Team Lead  
**Scopo:** Automatizzare conversione testi da RIFERIMENTI in JSON strutturato per distribuzione

---

## 🎯 Processo Automatico

### **OGNI GIORNO:**

1. **Check RIFERIMENTI/input** → Verifica nuovi file `.md` o `.txt`
2. **Converti a JSON** → Usa Claude API per strutturazione automatica
3. **Cataloga** → Crea entry in RIFERIMENTI/catalogo
4. **Prepara per Agata** → Genera report di distribuzione

---

## 📁 Struttura RIFERIMENTI

```
RIFERIMENTI/
├── input/              ← Nuovi testi aggiunti qui (fonte)
├── output/             ← JSON convertiti (prodotto)
├── processed/          ← File originali dopo processamento
└── catalogo/           ← Metadata e catalogo per Agata
    ├── processed_files.json        ← Tracking file processati
    ├── AGATA_CATALOGO_MASTER.json  ← Catalogo master
    └── AGATA_REPORT_*.json         ← Report giornalieri
```

---

## 🚀 Come Usare

### **Step 1: Aggiungi nuovo testo**

Copia file `.md` o `.txt` in `RIFERIMENTI/input/`:

```bash
cp DOCUMENTO_NUOVO.md RIFERIMENTI/input/
```

### **Step 2: Esegui automazione**

```bash
python3 RIFERIMENTI_AUTOMAZIONE_DAILY.py
```

**Output:**
```
============================================================
RIFERIMENTI AUTOMAZIONE DAILY
Data/Ora: 2026-08-31T14:00:00.000000
============================================================

Processing: DOCUMENTO_NUOVO.md
✅ DOCUMENTO_NUOVO.md → DOCUMENTO_NUOVO.json
📋 Catalogo master generato: CATALOGO_MASTER.json
📧 Report per Agata: {...}

============================================================
```

### **Step 3: Verifica output**

```bash
# JSON convertito
cat RIFERIMENTI/output/DOCUMENTO_NUOVO.json

# Catalog entry
cat RIFERIMENTI/catalogo/DOCUMENTO_NUOVO_catalog.json

# Report per Agata
cat RIFERIMENTI/catalogo/AGATA_REPORT_*.json
```

### **Step 4: Agata procede a distribuzione**

Vedi: **AUTOMAZIONE_RIFERIMENTI_AGATA_WORKFLOW.md**

---

## ⏰ Automazione Giornaliera (Cron)

### **Setup (eseguire una volta):**

```bash
# Aggiungi a crontab
crontab -e
```

### **Cron schedule (runs daily at 08:00 UTC):**

```cron
0 8 * * * cd /home/user/progetto-alessandra && python3 RIFERIMENTI_AUTOMAZIONE_DAILY.py >> RIFERIMENTI/catalogo/automazione.log 2>&1
```

### **Verificare che cron sia attivo:**

```bash
# List active crons
crontab -l

# Tail log di automazione
tail -f RIFERIMENTI/catalogo/automazione.log
```

---

## 🔍 Cosa Fa L'Automazione

### **1. Legge testi da RIFERIMENTI/input**

Identifica:
- File `.md` (Markdown)
- File `.txt` (Plain text)
- Ignora file già processati

### **2. Converte a JSON usando Claude**

Applica principi da **GUIDA_TRASFORMAZIONE_TESTO_TO_JSON.md**:
- ✅ Identifica struttura gerarchica
- ✅ Converte elenchi in array
- ✅ Normalizza date (ISO 8601)
- ✅ Normalizza durate (value/unit)
- ✅ Aggiungi ID univoci
- ✅ Includi metadata

### **3. Salva output**

- **JSON file:** `RIFERIMENTI/output/{nome}.json`
- **Catalog entry:** `RIFERIMENTI/catalogo/{nome}_catalog.json`
- **Master catalog:** `RIFERIMENTI/catalogo/AGATA_CATALOGO_MASTER.json`

### **4. Traccia processamento**

Aggiorna `RIFERIMENTI/catalogo/processed_files.json`:
```json
{
  "processed": {
    "DOCUMENTO_NUOVO.md": {
      "date": "2026-08-31T14:00:00",
      "json_file": "DOCUMENTO_NUOVO.json",
      "status": "completed"
    }
  }
}
```

---

## 📊 Catalogo Master per Agata

**File:** `RIFERIMENTI/catalogo/AGATA_CATALOGO_MASTER.json`

```json
{
  "metadata": {
    "generated_date": "2026-08-31T14:00:00",
    "source": "RIFERIMENTI Automation System",
    "destination": "Agata (Infrastructure Orchestrator)"
  },
  "conversions": [
    {
      "source_file": "DOCUMENTO_NUOVO.md",
      "json_file": "DOCUMENTO_NUOVO.json",
      "conversion_date": "2026-08-31T14:00:00",
      "status": "ready_for_distribution",
      "processing_time": "auto"
    }
  ]
}
```

---

## 🎯 Report Giornaliero per Agata

**File:** `RIFERIMENTI/catalogo/AGATA_REPORT_20260831_140000.json`

```json
{
  "date": "2026-08-31T14:00:00",
  "title": "Nuove Conversioni Testo → JSON Pronte per Distribuzione",
  "count": 1,
  "conversions": [
    {
      "source": "DOCUMENTO_NUOVO.md",
      "json": "DOCUMENTO_NUOVO.json",
      "catalog": "DOCUMENTO_NUOVO_catalog.json"
    }
  ],
  "action_required": "Cataloga e fornisci ai soggetti di riferimento",
  "instructions": {
    "step1": "Leggi CATALOGO_MASTER.json per dettagli conversioni",
    "step2": "Per ogni conversion, accedi a OUTPUT/{json_file}",
    "step3": "Verifica struttura JSON è corretta",
    "step4": "Cataloga nel sistema di tracking risorse",
    "step5": "Comunica ai soggetti di riferimento"
  }
}
```

---

## 📋 Checklist Implementazione

- [ ] Cartella RIFERIMENTI creata con struttura
- [ ] Script `RIFERIMENTI_AUTOMAZIONE_DAILY.py` funzionante
- [ ] Cron setup completato (daily 08:00)
- [ ] Agata briefed su nuovo workflow
- [ ] Test: carica file di prova in RIFERIMENTI/input
- [ ] Verifica: JSON generato in RIFERIMENTI/output
- [ ] Verifica: Catalogo e report generati
- [ ] Agata: conferma ricezione primo report

---

## 🚨 Troubleshooting

| Problema | Causa | Soluzione |
|----------|-------|----------|
| Script errore "ModuleNotFoundError: anthropic" | SDK non installato | `pip install anthropic` |
| JSON parsing error | Conversione Claude non è JSON valido | Controlla RIFERIMENTI/output/{nome}_raw.txt |
| File non processato | Già in processed_files.json | Cancella entry in processed_files.json per re-processare |
| Cron non esegue | Percorso non corretto | Usa absolute path in crontab |
| Agata non riceve report | Check log file automazione | `tail RIFERIMENTI/catalogo/automazione.log` |

---

## 🔗 Documenti Correlati

- **GUIDA_TRASFORMAZIONE_TESTO_TO_JSON.md** — Principi di trasformazione
- **AUTOMAZIONE_RIFERIMENTI_AGATA_WORKFLOW.md** — Workflow distribuzione
- **AGATA_RESPONSABILITA_OWNERSHIP.md** — Ruolo Agata

---

## 📞 Supporto

**Se automazione non funziona:**
1. Controlla che Anthropic SDK è installato
2. Verifica che API key è configurata
3. Controlla log file: `RIFERIMENTI/catalogo/automazione.log`
4. Contatta Alessandra con details dell'errore

**Se hai nuovo testo da convertire:**
1. Metti in `RIFERIMENTI/input/`
2. Aspetta prossima esecuzione daily (08:00 default)
3. O esegui manualmente: `python3 RIFERIMENTI_AUTOMAZIONE_DAILY.py`

---

**Status:** ✅ AUTOMAZIONE SETUP COMPLETATA  
**Data:** 31 agosto 2026  
**Prossima iterazione:** 1 settembre 2026 (08:00 UTC)

