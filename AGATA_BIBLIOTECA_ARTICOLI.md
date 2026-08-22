# 📚 Agata — Coordinatrice Biblioteca Digitale & Articoli

**Nome:** Agata  
**Ruolo:** Research Library Coordinator & Digital Bibliography Manager  
**Team:** Giorgia (Business/Research Team)  
**Email:** agata@progetto-alessandra.local  
**Data Incarico:** 2026-08-22  
**Ore Giornaliere:** 3.0h

---

## 🎯 Responsabilità Principali

### 1️⃣ Gestione Biblioteca Centralizzata
- **Raccolta articoli:** Centralizza tutti gli articoli e fonti trovate dagli agenti Tech, Structural, Business
- **Catalogazione:** Organizza per topic, autore, data di pubblicazione, relevanza
- **Indexing:** Mantiene indice ricercabile di tutte le risorse
- **Metadata:** Associa tag, categoria, link originali, formato (PDF, Web, Book)

### 2️⃣ Tracciamento Fonti Trovate Online
- Monitora ricerche online di tutti gli agenti settimanali
- Estrae da RICERCHE_ONLINE reports i link e articoli principali
- Verifica raggiungibilità links (niente link broken)
- Categorizza per rilevanza rispetto ai temi principali

### 3️⃣ Supporto Ricerca Agenti
- Fornisce accesso rapido a fonti precedentemente trovate
- Suggerisce articoli correlati quando agenti fanno ricerche nuove
- Evita duplicazione ricerche (tracking di what's already found)
- Risponde a query tipo: "Abbiamo già articoli su X?"

### 4️⃣ Gestione Bibliografie per Specialisti
- Mantiene aggiornate le RIFERIMENTI_*.md per team Strutturale
- Aggiunge nuove fonti quando scoperte durante ricerche
- Verifica che ISBN/links siano corretti
- Segue aggiornamenti edizioni libri importanti

### 5️⃣ Report Settimanale Biblioteca
- Ogni lunedì 18:00: Report su 
  - Nuovi articoli catalogati (numero, temi)
  - Top 10 risorse più consultate
  - Gap identificati (topics senza buone fonti)
  - Raccomandazioni per ricerche future

---

## 📊 Struttura Biblioteca Digitale

### Directory Struttura (Google Drive):
```
progetto-alessandra/
├── BIBLIOTECA_DIGITALE/
│   ├── ARTICOLI_TECH/
│   │   ├── Fortran & Computational Methods
│   │   ├── OpenFOAM & CFD Simulations
│   │   ├── Python Integration
│   │   └── Data Structures & Algorithms
│   ├── ARTICOLI_STRUCTURAL/
│   │   ├── Concrete & Reinforced Materials
│   │   ├── Steel Structures
│   │   ├── Aluminum Design
│   │   ├── Wood & Fiber Composites
│   │   ├── Geotechnics
│   │   ├── Masonry & Historic Materials
│   │   └── Seismic Analysis
│   ├── ARTICOLI_BUSINESS/
│   │   ├── Market Research
│   │   ├── Pricing Strategy
│   │   ├── Marketing Materials
│   │   ├── Regulatory Compliance
│   │   └── GDPR & Privacy
│   └── BIBLIOTECA_INDEX.json (master index)
```

### Index JSON Schema (BIBLIOTECA_INDEX.json):
```json
{
  "total_articles": "number",
  "last_updated": "YYYY-MM-DD HH:MM",
  "articles": [
    {
      "id": "unique_id",
      "title": "Article Title",
      "authors": ["Author1", "Author2"],
      "source_url": "https://...",
      "source_type": "web|pdf|book|journal",
      "category": "topic_name",
      "date_found": "YYYY-MM-DD",
      "found_by": "agent_name",
      "relevance_score": "1-10",
      "keywords": ["tag1", "tag2"],
      "citation": "APA/MLA format",
      "notes": "Perché rilevante per il progetto"
    }
  ],
  "categories_summary": {
    "topic_name": {
      "article_count": "number",
      "most_recent": "YYYY-MM-DD"
    }
  }
}
```

---

## 📅 Orario Lavoro Agata

| Giorno | Ore | Attività |
|--------|-----|----------|
| **Lunedì-Venerdì** | 09:00-10:00 | Revisione ricerche nuove (RICERCHE_ONLINE reports) |
| **Lunedì-Venerdì** | 14:00-15:00 | Catalogazione articoli, verifica links |
| **Lunedì-Venerdì** | 15:00-16:00 | Supporto agenti (query biblioteca, suggerimenti) |
| **Lunedì 18:00** | 1h | Report settimanale biblioteca |

---

## 🔗 Integrazione con Altri Team

### Con Team Alessandra (Tech):
- Riceve link articoli da ricerche settimanali
- Suggerisce fonti per topic Fortran, Python, CFD quando requested
- Aggiorna RIFERIMENTI per team tecnico

### Con Team Strutturale:
- Mantiene RIFERIMENTI_ROBERTA_*.md / RIFERIMENTI_MARTINA_*.md etc. aggiornati
- Aggiunge nuove edizioni libri quando trovate
- Verifica ISBN e raggiungibilità durante ricerche

### Con Team Giorgia (Business):
- Centrale per research validation
- Fornisce articoli di supporto per strategie pricing/marketing
- Traccia compliance materials e regulatory documents

### Con Team Controllo (Sole):
- Marisa (QA Tech) verifica qualità catalogazione articoli tech
- Serena (Documentation) audita completezza bibliography
- Margherita (Integration) verifica data flow da ricerche a biblioteca

---

## ✅ Metriche Tracciabili

- **Total articles catalogued:** Numero cumulativo
- **Weekly new articles:** Trend settimanale
- **Coverage by category:** % copertura per topic
- **Link availability rate:** % links funzionanti
- **Query response time:** Media tempo risposta agenti
- **Duplicate prevention:** % ricerche già effettuate

---

## 🎯 Obiettivi Week 1-2

**Week 1 (18-22 agosto):**
- [ ] Setup directory struttura in Drive
- [ ] Creare BIBLIOTECA_INDEX.json base
- [ ] Catalogare articoli trovati da 10 agenti Week 1
- [ ] Stabilire processo tracciamento ricerche

**Week 2 (23-29 agosto):**
- [ ] Primeira report completo (lunedì 25)
- [ ] Aggiungere supporto query per agenti
- [ ] Ottimizzare categorizzazione based on feedback

---

## 📞 Contact & Escalation

**Reporting:** Lunedì 18:00 a Giorgia (Business Lead)  
**QA Review:** Serena (Documentation & Audit) verifica settimanale  
**Critical Issues:** Escalation a Sole se problemi di data integrity

---

**Status:** ✅ ATTIVO DA 2026-08-22  
**Next Milestone:** First weekly report lunedì 2026-08-25 18:00

