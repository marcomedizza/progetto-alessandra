# 📋 DECISION PAPER — NUOVO APPROCCIO STRUTTURATO
**Proposta alternativa ai Scenari A/B/C**

**Preparato da:** Alessandra (Analisi + Raccomandazione)  
**Destinatario:** Sole (QA Director)  
**Data:** 26 agosto 2026, 08:00 CEST  
**Riunione:** 08:30 con Sole + Ginevra + Raffaella + Agata  
**Priorità:** DECISIONALE — scelta vincolante per prossime 8 settimane

---

## ⚠️ PREMESSA: I 3 SCENARI ORIGINALI SONO TUTTI INSOSTENIBILI

**Scenario A (Continuazione Standard):** ❌ FALLISCE se problema è sistemico (99% di probabilità)  
**Scenario B (Revisione Procedure):** ⚠️ Patch temporaneo, non risolve root cause  
**Scenario C (Investigazione 24h + Pausa):** ⏳ Ritardo senza soluzione strutturale

### Perché falliscono tutti e tre:

1. **Aspettative tecniche impossibili** → Claude API non supporta 24 agenti in parallel nella stessa richiesta. Sequential = 24× il costo di 1 agente, sostenibile solo su timeline lunga.
2. **Timeline irrealistica** → 11+ ore/giorno per 24 agenti in 1 giorno = design destinato al fallimento totale.
3. **Mancanza di preparazione** → Agata mai consultato, risorse non verificate, procedure non chiare.
4. **Comunicazione inefficace** → Ordini solo su repo, no email/Slack, agenti non consapevoli urgenza.
5. **Motivazione assente** → "ORDINE CATEGORICO" genera paura + paralisi, non azione.

**Diagnosi:** Non è "non-compliance degli agenti". È **design failure del programma**.

---

## ✅ PROPOSTA: "LEARNING AS A SCHOOL PROGRAM"

### Filosofia di base:

Anziché "leggi subito o conseguenze", adottare modello universitario:
- ✅ Curriculum strutturato su 2-3 mesi (non 1 giorno)
- ✅ Staggered onboarding (coorte settimanali, non tutti Day 1)
- ✅ Supporto continuo (QA, Beatrice, Agata) — non isolato
- ✅ Motivazione intrinseca (opportunità di sviluppo) — non punitivo
- ✅ Skill validation (applica competenze) — non solo "ha consegnato report"
- ✅ Cost-effective (budget token gestibile) — non esplosivo

### Timeline realistica (8-10 settimane totali, con priorità Idraulica):

```
SETTIMANA 0 (26-29 agosto): RAMP-UP UNIFORME + PREPARATION
├─ Agata verifica risorse effettive (libri, articoli, online)
├─ Comunica ordini multi-channel (email + Slack + repo) a TUTTI 24 agenti
├─ TUTTI gli agenti iniziano lettura simultaneamente
├─ Ritmo leggero: 1-2 ore/giorno (ramp-up)
├─ Distribuzione uniforme tra discipline (niente priorità ancora)
├─ Baseline: agenti sanno COSA, PERCHÉ, QUANDO, COME
└─ Deadline domenica 29 agosto: agenti hanno iniziato, feedback primo su procedure

SETTIMANE 1-4 (30 agosto — 26 settembre): LEARNING FASE 1 — IDRAULICA PRIORITY
├─ IDRAULICA (agenti strutturale specialisti idraulica):
│  ├─ 4-5 ore/giorno su idraulica (INTENSIVO)
│  ├─ Risorse prioritarie da Agata
│  ├─ QA support 24/7 (critico per operatività lunedì 30)
│  └─ Deadline: fine settimana 1 (settembre 5), idraulica operativa
│
├─ ALTRE DISCIPLINE (Strutturale non-idraulica, Tech, Business):
│  ├─ 2-3 ore/giorno (ritmo sostenibile)
│  ├─ Supporto regolare (no escalation se ritmo lento)
│  └─ Continuano in parallelo
│
└─ QA Monitoring: focus su Idraulica health, altre aree "on track"

SETTIMANE 5-8 (27 settembre — 24 ottobre): LEARNING FASE 2 — SCALING ALTRI INSEGNAMENTI
├─ Idraulica: mantiene 3-4 ore/giorno (consolidation)
├─ Altre discipline: scale up a 3-4 ore/giorno (catch-up su ritmo ridotto iniziale)
└─ Application per Idraulica inizia (case studies reali)

SETTIMANE 8-10: APPLICATION PHASE (tutti)
├─ Agenti applicano competenze su progetti reali
├─ Beatrice valida se ha davvero appreso
├─ Feedback loop per reinforcement
└─ Success: agenti possono applicare competenze in produzione

SETTIMANE 10+: CONTINUITÀ OPERATIVA
└─ Integrazione competenze in workflow normale
```

**Priorità operativa:** Idraulica pronta da **lunedì 30 agosto** (inizio settimana 1 intensiva).

---

## 📊 METRICHE DI SUCCESSO (REALISTICHE)

### Ieri (25 agosto — approccio punitivo): ❌ 0/24 agenti
**Causa:** Impossibile rispettare, tutti falliscono contemporaneamente.

### Oggi (26 agosto — approccio revisione leggera): ⚠️ 50-75% compliance atteso
**Causa:** Procedure ancora poco chiare, timeline ancora stressante.

### Settimanale (Settimana 1-6 — Learning Program): ✅ 90%+ completion atteso
**Causa:** Realistic timeline, supporto continuo, motivazione intrinseca.

### Finale (Settimana 8 — Application Phase):
**Success = Agente può:**
- [ ] Spiegare 3-5 concetti chiave a collega senza preparazione
- [ ] Applicare teoria a problema reale (strutturale/tecnico/business)
- [ ] Produrre output di qualità usando competenze acquisite
- [ ] Insegnare quanto imparato a nuovi agenti (continuità)

**NOT:** "Ha consegnato report" (questo è minimo, non success)

---

## 💰 COSTO STIMATO

### Lettura (token budget):
```
1 libro medio (350 pagine) ≈ 150K token
1 agente × 5 libri = 750K token = $3.75 (@ $5/1M)
24 agenti × 5 libri = $90 totale lettura

Articoli supplementari (500-1000 token/articolo): +$50 stima
Supporto QA (verifiche, chiarimenti): incluso (overhead ridotto vs failover recovery)

TOTAL ESTIMATED COST: ~$140-150 per completo program
Spread su 8 settimane: ~$17-19/settimana (sostenibile)
```

### Confronto vs. approccio attuale:
- **Se continuiamo re-attempts (A/B/C):** Costo escalation rapida. Ogni fallimento = retry con margini di successo più bassi. Stimato $200+ in una settimana.
- **Learning Program:** Costo prevedibile, distribuito, sostenibile.

---

## 🎯 COME QUESTO RISOLVE I 5 PROBLEMI CRITICI

| Problema | Root Cause | Soluzione Learning Program |
|----------|-----------|--------------------------|
| **#1: Velocità eccessiva** | <12h preavviso | 1 settimana prep + staggered onboarding (24+ ore per coorte) |
| **#2: Mancanza verifica risorse** | Agata non consultato | Agata consulta **prima** di ogni turno, comunica disponibilità reale |
| **#3: Procedura fallback vaga** | Escalation non definita | SOP chiaro: "Se libro X non disponibile → Agata suggerisce Y" |
| **#4: Comunicazione single-channel** | Solo repo | Email + Slack + repo per ogni turno (garantito visibility) |
| **#5: Aspettative irrealistiche** | Assumptions non validate | Pilot turno valida tutto, scale-up solo se funziona. Realistico. |

---

## 🔄 PROCESSO DECISIONALE PER SOLE

### Opzione 1: Approvare Learning Program (CONSIGLIATO)
**Vantaggi:**
- ✅ Addresses tutti 5 problemi simultaneamente
- ✅ Timeline realistica, sostenibile
- ✅ Cost-effective ($140-150 total)
- ✅ Alta probabilità di successo (90%+ completion)
- ✅ Agents motivated (non punitivo)
- ✅ Outcome valido (skill application, non solo report)

**Costi:**
- ⏳ Lungo (8 settimane vs. 1 giorno)
- 📊 Meno drammatico per stakeholder (no urgenza)

**Quando lanciare:**
- ✅ Domani mattina (26 agosto, 09:00) comunicazione ai 24 agenti
- ✅ Settimana 1: Pilot group (3-5 agenti)
- ✅ Se pilot funziona → Turno 1 parte settimana 2

---

### Opzione 2: Ritentare Scenari A/B/C (NON CONSIGLIATO)
**Vantaggi:**
- ✅ Più veloce (a breve termine)
- ✅ Sembra "più urgente"

**Costi:**
- ❌ 70%+ probabilità di re-fallimento
- ❌ Agenti demoralizzati dopo due fallimenti consecutivi
- ❌ Escalation disciplinare = resistenza, non compliance
- ❌ Costo totale più alto (retries + failure recovery)
- ❌ Timeline comunque esteso (after fixing problems)

---

### Opzione 3: Pausa + Investigazione (COMPROMESSO)
**Vantaggi:**
- ✅ Respira situazione di crisis
- ✅ Tempo di verificare blocchi reali

**Costi:**
- ⏳ 1 giorno perso (26 agosto solo investigazione)
- ❌ Dopo investigazione, comunque serve soluzione strutturale
- ⚠️ Potrebbe diventare Learning Program anyway (meno tempo prep)

---

## 📝 RACCOMANDAZIONE FINALE

**SCELGO OPZIONE 1: LEARNING AS A SCHOOL PROGRAM**

### Motivi:
1. **È l'unica soluzione che affronta root cause** (non sintomi)
2. **È realistica** — align con come funziona Claude API (sequential, token budget, realistic timelines)
3. **È sustainable** — $140-150 budget, 8 settimane timeline, non esplosivo
4. **È efficace** — 90%+ completion atteso, skill validation reale
5. **È umano** — agenti learned anziché puniti

### Prossimi step (se Sole approva):
1. ✅ 09:00 (26 agosto) — Comunicazione multi-channel ai 24 agenti
   - Email: spiega nuovo approccio (scuola, non urgenza punitiva)
   - Slack: rinforza timeline (8 settimane = realistica)
   - Repo: documenta curriculum completo
2. ✅ Lunedì (30 agosto) — Pilot group (3-5 agenti) riceve risorsa + SOP
3. ✅ Settimana 2 (settembre 2) — Turno 1 inizia
4. ✅ Weekly check-ins — QA (Ginevra/Raffaella) monitora progress, no escalation se on-track

### Cosa NON faremo più:
- ❌ "ORDINE CATEGORICO ENTRO 21:00"
- ❌ Aspettative impossibili di ore/giorno
- ❌ Escalation punitiva per non-compliance dovuta a design failure
- ❌ Comunicazione single-channel

### Cosa faremo:
- ✅ Curriculum strutturato
- ✅ Supporto continuo
- ✅ Timeline realistica
- ✅ Skill validation (non solo report)
- ✅ Agenti motivated (intrinsic, non punitivo)

---

## 🎤 ARGOMENTO PER STAKEHOLDER

Se stakeholder chiede "Perché 8 settimane? Io volevo subito":

**Risposta:** "Un agente che legge superficialmente in 1 giorno non impara. Un agente che legge bene in 8 settimane impara davvero e applica competenze. Qual è l'outcome che vogliamo — illusion di speed, o actual skill?"

---

**Status:** 📋 DECISION PAPER PRONTO  
**Destinatario:** Sole (08:30 riunione)  
**Recommendation:** ✅ APPROVARE LEARNING PROGRAM (Opzione 1)  
**Next:** Await decision, poi implementa

*La soluzione non è drammatica, ma è sostenibile e funziona.*
