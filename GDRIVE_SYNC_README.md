# ☁️ Google Drive Sync - Dashboard Alessandra

Sincronizzazione automatica del Dashboard tra locale e Google Drive.

---

## 🚀 **SETUP RAPIDO (5 minuti)**

### **Step 1: Installa dipendenze**
```bash
pip install watchdog google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### **Step 2: Setup Google Cloud (OPZIONALE - solo per auto-sync)**

Se vuoi sincronizzazione **automatica**, segui questi passi:

1. Vai a: https://console.cloud.google.com/
2. Crea un nuovo progetto: **"Progetto Alessandra"**
3. Abilita **Google Drive API**
4. Crea credenziali: **"Desktop application" (OAuth 2.0)**
5. Scarica il JSON e salvalo qui:
   ```
   D:\progetto-alessandra\credentials.json
   ```

### **Step 3: Avvia il sync**
```bash
python C:\Users\User\AppData\Local\Temp\claude\...\scratchpad\gdrive_sync.py
```

Il script:
- ✅ Monitora `DASHBOARD_ALESSANDRA_v2.html` in locale
- ✅ Carica automaticamente su Google Drive quando lo modifichi
- ✅ Crea backup locali in `D:\progetto-alessandra\backups\`
- ✅ Sincronizzazione bidirezionale

---

## 📁 **STRUTTURA**

```
D:\progetto-alessandra\
├── DASHBOARD_ALESSANDRA_v2.html ← File monitorato
├── credentials.json ← (caricato da Google Cloud)
├── token.json ← (generato automaticamente)
├── sync_state.json ← (stato sync)
├── backups/
│   ├── DASHBOARD_20260815_150230.html
│   ├── DASHBOARD_20260815_151045.html
│   └── ...
└── GDRIVE_SYNC_README.md (questo file)

Google Drive: progetto-alessandra/
├── DASHBOARD_ALESSANDRA_v2.html (sincronizzato)
└── (altri file progetto)
```

---

## 🔄 **COME FUNZIONA**

### **Sync Automatico**
1. Modifichi il file HTML locale
2. Lo salvi
3. Lo script rileva il cambiamento
4. Carica su Google Drive entro 2 secondi
5. Crea backup locale

### **Accesso su Google Drive**
- Apri: https://drive.google.com/
- Cartella: `progetto-alessandra`
- File: `DASHBOARD_ALESSANDRA_v2.html`
- Condividi il link con il team

---

## 💾 **BACKUP LOCALI**

Ogni sincronizzazione crea backup automatici:
```
D:\progetto-alessandra\backups\DASHBOARD_YYYYMMDD_HHMMSS.html
```

Recupera una versione precedente se necessario.

---

## ⚙️ **OPZIONI**

### **Sync Manuale (senza Google Cloud Setup)**
Se non vuoi configurare Google Cloud:

1. Carica il file **UNA VOLTA** manualmente su Google Drive
2. Condividi il link con il team
3. Questo script crea backup locali automaticamente
4. Scarica le modifiche manualmente da GDrive quando serve

### **Sync con Rclone (Alternativa)**
Se preferisci usare Rclone invece di Python:

```bash
pip install rclone
# Configurazione: https://rclone.org/drive/
rclone sync D:\progetto-alessandra\DASHBOARD_ALESSANDRA_v2.html remote:progetto-alessandra/
```

---

## 📊 **STATUS**

Quando il sync è attivo, vedrai:

```
✅ Autenticato con Google Drive

🚀 Sincronizzazione attiva!
💡 Modifica il file HTML e sarà sincronizzato automaticamente
⏸️  Premi CTRL+C per fermare

📝 File modificato: D:\progetto-alessandra\DASHBOARD_ALESSANDRA_v2.html
☁️  Sincronizzando con Google Drive...
✅ File aggiornato su GDrive (ID: 1a2b3c4d...)
💾 Backup locale: D:\progetto-alessandra\backups\DASHBOARD_20260815_150230.html
```

---

## 🔧 **TROUBLESHOOTING**

### **"Credentials not found"**
→ Scarica credentials.json da Google Cloud Console

### **"Permission denied"**
→ Controlla che Google Drive API sia abilitato nel progetto

### **Sync non funziona**
→ Controlla che `watchdog` sia installato: `pip install watchdog`

### **File troppo grande**
→ Il file HTML dovrebbe essere < 1MB, dovrebbe essere ok

---

## 👥 **TEAM SHARING**

Una volta su GDrive, condividi con il team:

1. Apri GDrive → progetto-alessandra
2. Clicca su `DASHBOARD_ALESSANDRA_v2.html` → **Condividi**
3. Aggiungi email agenti
4. Imposta: **Visualizzatore** (non editore, per evitare conflitti)
5. Link condivisibile: Copia e invia su Slack

---

## 📝 **NOTE**

- ⚠️ Il file HTML si auto-salva in **localStorage** (browser storage)
- 📱 Ogni browser ha il suo localStorage
- 💡 Suggerimento: Apri il file HTML in Google Drive direttamente (se abiliti)
- 🔄 Per sincronizzare modifiche dal team, scarica il file aggiornato da GDrive

---

## 🎯 **WORKFLOW CONSIGLIATO**

1. **Avvia il sync** (mattina):
   ```bash
   python gdrive_sync.py
   ```

2. **Modifica il dashboard** (durante la giornata):
   - Edita `DASHBOARD_ALESSANDRA_v2.html`
   - Il sync carica automaticamente

3. **Condividi con team** (una volta all'inizio):
   - Condividi il link GDrive
   - Gli agenti possono accedere/modificare

4. **Monitora backup** (settimanale):
   - Controlla `backups/` se serve ripristinare

---

**Pronto! 🚀**

Avvia il sync e il dashboard sarà sempre sincronizzato tra locale e Google Drive.

Domande? Controlla i log nella console dove gira lo script.
