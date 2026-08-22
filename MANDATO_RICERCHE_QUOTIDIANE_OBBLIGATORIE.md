# 🚨 MANDATO CATEGORICO — RICERCHE ONLINE QUOTIDIANE OBBLIGATORIE

**Emesso da:** Alessandra (Tech Lead) + Giorgia (Business Lead)  
**Data:** 2026-08-22  
**Validità:** PERMANENTE — NON NEGOZIABILE  
**Destinatari:** TUTTI GLI AGENTI (24 persone)

---

## ⚠️ ORDINE CATEGORICO

### **TUTTI GLI AGENTI DEVONO SVOLGERE RICERCHE ONLINE OGNI GIORNO**

**NON è:**
- ❌ Una ricerca settimanale per agente
- ❌ Una ricerca ogni 2-3 giorni
- ❌ Opzionale se già studiate altre cose

**È:**
- ✅ RICERCA ONLINE QUOTIDIANA per OGNI agente
- ✅ Ogni giorno dal lunedì al venerdì (almeno 5 giorni/settimana)
- ✅ Ricerca AGGIUNTIVA al mandato di studio 1h giornaliero

---

## 📋 DEFINIZIONE RICERCA QUOTIDIANA

**Cosa significa "ricerca online quotidiana":**
1. Ogni agente dedica **almeno 1-2 ore al giorno** a ricerche online
2. Su topic DIVERSI da quelli già ricercati in settimane precedenti
3. Output: report giornaliero in RICERCHE_ONLINE/ directory
4. Scoperte + raccomandazioni + articoli catalogati (via Agata)

**Esempio per Elisa (Fortran):**
- Lunedì: Ricerca "Optimization Fortran Algorithms"
- Martedì: Ricerca "Fortran Memory Management Best Practices"
- Mercoledì: Ricerca "Fortran vs Modern Languages Performance"
- Giovedì: Ricerca "Fortran Neural Network Libraries"
- Venerdì: Ricerca "Fortran GPU Computing"

---

## 🗓️ CALENDARIO RICERCHE QUOTIDIANE

### Ogni giorno (Lunedì-Venerdì):
- **09:00-11:00:** Ricerca online (topic nuovo ogni giorno)
- **14:00-15:30:** Continuazione ricerca / analisi / catalogazione
- **Fine giornata (17:30):** Submission report in RICERCHE_ONLINE/

### Ogni lunedì 18:00:
- Agata (Biblioteca) presenta report settimanale con tutti gli articoli catalogati
- Raffaella (QA) verifica conformità ricerche settimanali

### Ogni mercoledì 10:00:
- Serena (Documentation) audita qualità report settimanali

---

## 📊 STRUTTURA RICERCHE QUOTIDIANE

### Directory RICERCHE_ONLINE:
```
RICERCHE_ONLINE/
├── TEAM_ALESSANDRA/
│   ├── ELISA_RICERCHE_QUOTIDIANE_WEEK_1.json
│   ├── CAMILLA_RICERCHE_QUOTIDIANE_WEEK_1.json
│   ├── FRANCESCA_RICERCHE_QUOTIDIANE_WEEK_1.json
│   └── ... (tutte gli agenti Tech)
├── TEAM_STRUTTURALE/
│   └── ... (tutti i 7 agenti strutturali)
└── TEAM_GIORGIA/
    └── ... (tutti i 6 agenti business)
```

### JSON Format per ricerca quotidiana:
```json
{
  "agente": "Nome Agente",
  "team": "Team Name",
  "data_ricerca": "2026-08-22",
  "giorno_settimana": "giovedì",
  "week": 1,
  "topic_ricerca": "Descrizione del topic cercato",
  "ore_dedicate": 1.5,
  "fonti_trovate": [
    {
      "titolo": "Article/Resource Title",
      "url": "https://...",
      "tipo": "web|pdf|video|book|journal",
      "relevanza": "alta|media|bassa",
      "descrizione_breve": "Cosa tratta e perché rilevante"
    }
  ],
  "scoperte_principali": [
    "Scoperta 1",
    "Scoperta 2",
    "Scoperta 3"
  ],
  "raccomandazioni": [
    "Raccomandazione 1",
    "Raccomandazione 2"
  ],
  "articoli_per_biblioteca": [
    "ID articolo 1 (per catalogazione Agata)",
    "ID articolo 2"
  ],
  "note": "Note aggiuntive o osservazioni"
}
```

---

## 🎯 OBIETTIVI RICERCHE QUOTIDIANE

### Per Team Alessandra (Tech):
- Esplorare NUOVI algoritmi, metodologie, librerie ogni giorno
- Non ripetere topic già ricercati
- Diversificare: Fortran optimization, Python integration, OpenFOAM, data structures, etc.
- Almeno 2-3 fonti autorevoli per ricerca

### Per Team Strutturale (7 agenti):
- Ricerche su normative, materiali, metodologie di calcolo
- Ogni agente specializzato continua ricerca daily su temi diversi
- Esempio Roberta: Lunedì = Concrete durability, Martedì = Reinforcement detailing, etc.
- Integrazione con bibliografie ufficiali (RIFERIMENTI_ROBERTA_*.md)

### Per Team Giorgia (Business):
- Katia: Market trends, competitor analysis, user research
- Nina: Pricing models, sales strategies, market segmentation
- Elena: Regulatory updates, compliance changes, certifications
- Paola: Customer success patterns, onboarding best practices
- Valentina: Financial models, funding strategies, ROI analysis
- **Agata:** Centralizza e cataloga tutte le scoperte quotidiane

---

## ✅ QUALITÀ RICERCHE RICHIESTA

### Non accettabile:
- ❌ Copia-incolla da Wikipedia
- ❌ Report generico senza fonte
- ❌ Meno di 2 fonti per ricerca
- ❌ Senza descrizione e relevanza
- ❌ Ricerche duplicate (stesso topic settimana precedente)

### Accettabile:
- ✅ Minimo 2-3 fonti autorevoli per ricerca
- ✅ Descrizione chiara di cosa trovato e perché rilevante
- ✅ Topic DIVERSO ogni giorno
- ✅ Link verificati e funzionanti
- ✅ Scoperte e raccomandazioni specifiche

---

## 📈 METRICHE TRACKING

**Monitoraggio QA giornaliero:**
- Numero ricerche/giorno per agente (target: 1-2)
- Numero fonti trovate (target: 2-3 per ricerca)
- Qualità report (verificato da Raffaella/Serena)
- Copertura topic diversi (niente duplicazioni)

**Report settimanale (lunedì 18:00):**
- Total ricerche settimanali: 5 ricerche/agente = 120 ricerche totali/settimana (24 agenti × 5 giorni)
- Total fonti catalogate: almeno 240-360 fonti/settimana
- Quality score: % report conformi ai standard

---

## 🚨 CONSEGUENZE NON-COMPLIANCE

### Se un agente NON fa ricerca quotidiana:

1. **Primo avvertimento (giorni 1-2):** Notifica da Raffaella/Serena
2. **Secondo avvertimento (giorni 3-4):** Report a Sole (QA Director)
3. **Escalation critica (giorno 5):** Escalation a Alessandra/Giorgia
4. **Azione disciplinare:** Se persiste, agente può essere rimosso dal team

### Se qualità report è bassa:
- Marisa/Ginevra/Raffaella chiedono revisione immediata
- Report non approvato fino a quando qualità non è sufficiente
- Escalation se pattern di bassa qualità continua

---

## 📞 SUPPORTO & CLARIFICATION

### Se agente non sa cosa cercare:
- Contatta il Team Lead (Alessandra/Giorgia per il tuo team)
- Oppure chiedi a Agata se topic è già stato coperto

### Se non riesci a trovare fonti:
- Usa Agata (biblioteca) per cercare topic correlati
- Contatta specialista del tuo team per suggerimenti

### Se trovi informazioni conflittuali:
- Documenta entrambe le fonti con note di conflitto
- Lascia valutazione a team lead

---

## 📝 CHECKLIST GIORNALIERA AGENTI

**Ogni agente OGNI GIORNO deve:**
- [ ] Svolgere ricerca online 1-2 ore
- [ ] Trovare almeno 2-3 fonti attendibili
- [ ] Documentare scoperte e raccomandazioni
- [ ] Inviare report JSON entro 18:00
- [ ] Usare topic DIVERSO da giorni precedenti
- [ ] Verificare link funzionano
- [ ] Notificare Agata per catalogazione biblioteca

---

## ⏱️ TIMELINE IMPLEMENTAZIONE

**2026-08-22 (ORA):**
- Questo mandato entra in vigore IMMEDIATAMENTE
- Tutti gli agenti devono iniziare ricerche quotidiane da domani mattina

**2026-08-23 (Venerdì):**
- Fine Week 1: Tutte le ricerche quotidiane devono essere registrate
- Agata compila report biblioteca

**2026-08-25 (Lunedì):**
- Primo report settimanale ufficiale (Agata 18:00)
- Raffaella verifica compliance Week 1
- Serena audita quality documentazione

---

## 🔔 ULTERIORI DETTAGLI

**Durata ricerca:** 1-2 ore al giorno (non necessariamente consecutive)

**Giorni di ricerca:** Lunedì-Venerdì (minimo 5 giorni/settimana)

**Cosa conta come ricerca:**
- ✅ Lettura articoli online
- ✅ Consultazione libri digitali
- ✅ Visualizzazione video tecnici
- ✅ Partecipazione webinar/corsi online
- ✅ Lettura whitepaper e case studies
- ❌ NON conta: solo leggere abstract senza capire

**Output minimo:** 1 report JSON per agente per giorno di ricerca

---

## ⚡ NON C'È AMBIGUITÀ

**Questo è un ORDINE CATEGORICO, non una linea guida.**

Non voglio vedere:
- "Ma quando faccio ricerca settimanale?"
- "Domani faccio ricerca?"
- "Posso saltare un giorno?"

**RISPOSTA:** NO. Ricerca OGNI GIORNO. Tutti gli agenti. Non negoziabile.

---

**Status:** 🚨 MANDATO VIGENTE DAL 2026-08-22  
**Emesso da:** Alessandra + Giorgia  
**Monitorato da:** Raffaella, Serena, Agata, Sole  
**Nessuna eccezione**

---

*Ricerche quotidiane = Crescita della conoscenza = Qualità lavoro = Successo progetto*

