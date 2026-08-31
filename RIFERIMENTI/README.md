# 📚 RIFERIMENTI — Automazione Testo → JSON

**Sistema:** Monitoraggio daily folder input, conversione automatica a JSON, catalogazione per distribuzione

---

## 📁 Struttura Cartelle

```
RIFERIMENTI/
├── input/              ← 📥 AGGIUNGI NUOVI TESTI QUI
├── output/             ← 📤 JSON CONVERTITI (prodotto)
├── processed/          ← ✅ File originali dopo processamento
└── catalogo/           ← 📋 Metadata, catalogo, report per Agata
```

---

## 🔄 Workflow Rapido

1. **Aggiungi file** → `RIFERIMENTI/input/documento.md`
2. **Esegui automazione** → `python3 RIFERIMENTI_AUTOMAZIONE_DAILY.py`
3. **Risultati** → `RIFERIMENTI/output/documento.json`
4. **Agata riceve** → `RIFERIMENTI/catalogo/AGATA_REPORT_*.json`

---

## 📝 Come Aggiungere Nuovo Testo

```bash
# Opzione 1: Copia file
cp NUOVO_DOCUMENTO.md RIFERIMENTI/input/

# Opzione 2: Crea direttamente in folder
echo "# Nuovo Documento" > RIFERIMENTI/input/NUOVO_DOCUMENTO.md

# Opzione 3: Upload via Drive, poi copia
cp ~/Downloads/DOCUMENTO.md RIFERIMENTI/input/
```

---

## ⚙️ Esecuzione Automazione

### **Manuale (immediate):**
```bash
python3 RIFERIMENTI_AUTOMAZIONE_DAILY.py
```

### **Automatica (daily 08:00):**
```bash
crontab -e
# Aggiungi: 0 8 * * * cd /home/user/progetto-alessandra && python3 RIFERIMENTI_AUTOMAZIONE_DAILY.py
```

---

## 📊 Monitorare Progresso

```bash
# Ultimi file processati
ls -ltr catalogo/processed_files.json

# Catalogo master
cat catalogo/AGATA_CATALOGO_MASTER.json | jq

# Report giornalieri
ls -ltr catalogo/AGATA_REPORT_*.json

# Log automazione
tail -f catalogo/automazione.log
```

---

## 🚀 Prossimi Step

1. [ ] Aggiungi primo documento in `input/`
2. [ ] Esegui `RIFERIMENTI_AUTOMAZIONE_DAILY.py`
3. [ ] Verifica JSON in `output/`
4. [ ] Agata legge report in `catalogo/AGATA_REPORT_*.json`
5. [ ] Agata distribuisce a soggetti riferimento

---

## 📞 Supporto

- **Automazione issue:** Contatta Alessandra
- **Distribuzione issue:** Contatta Agata
- **Contenuto JSON:** Contatta Beatrice

---

**Documentazione correlata:**
- `AUTOMAZIONE_RIFERIMENTI_GUIDA.md` — Guida completa
- `AUTOMAZIONE_RIFERIMENTI_AGATA_WORKFLOW.md` — Workflow Agata
- `GUIDA_TRASFORMAZIONE_TESTO_TO_JSON.md` — Principi trasformazione

