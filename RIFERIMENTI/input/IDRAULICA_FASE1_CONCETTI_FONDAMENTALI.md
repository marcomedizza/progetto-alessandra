# IDRAULICA — Fase 1 Intensive: Concetti Fondamentali

**Fase:** Fase 1 (30 agosto - 5 settembre 2026)  
**Destinatari:** Specialisti Idraulica (3-4 agenti)  
**Riferimento:** Belluzzi "Fondamenti di Idraulica" Cap 1-5  
**Durata intensive:** 4-5 ore/giorno  
**Obiettivo:** Ramp-up specialisti su principi fondamentali idraulici

---

## CAPITOLO 1 — Proprietà dei Fluidi

### Fluidi Incomprimibili vs Comprimibili
- Acqua è incomprimibile (densità costante)
- Gas sono comprimibili (densità varia con pressione)
- Nell'idraulica civile: focus su liquidi incomprimibili

### Densità e Peso Specifico
- **Densità (ρ):** massa per unità volume [kg/m³]
  - Acqua a 4°C: 1000 kg/m³
- **Peso specifico (γ):** peso per unità volume [N/m³]
  - Acqua: γ = ρ × g = 1000 × 9.81 = 9810 N/m³

### Viscosità
- **Viscosità dinamica (μ):** resistenza a flusso [Pa·s]
- **Viscosità cinematica (ν):** ν = μ/ρ [m²/s]
- Per acqua a 20°C: ν ≈ 1.0 × 10⁻⁶ m²/s

### Pressione
- **Pressione assoluta:** pressione rispetto a vuoto perfetto [Pa]
- **Pressione relativa (gauge):** pressione rispetto atmosfera [Pa]
- **Pressione atmosferica standard:** 101,325 Pa ≈ 101.3 kPa

---

## CAPITOLO 2 — Statica dei Fluidi (Idrostatica)

### Equazione Fondamentale
- **dp/dz = -ρg** (dove z è altitudine)
- Pressione aumenta linearmente con profondità
- **p = p₀ + ρgh** (h è profondità sotto superficie)

### Principio di Pascal
- Pressione in un punto si trasmette uniformemente in tutte direzioni
- Applicazione: moltiplicatori idraulici, presse idrauliche

### Forze su Superfici Immerse
**Superficie orizzontale (fondo bacino):**
- Forza totale: F = p × A = ρgh × A
- Punto di applicazione: al centro della superficie

**Superficie verticale (parete):**
- Forza totale: F = ρg × (h/2) × A
- Punto di applicazione: a 2/3 profondità (non al centro!)

### Spinta Idrostatica su Dighe
- Carico aumenta con profondità (triangolare)
- Risultante agisce a 1/3 da superficie, 2/3 da fondo
- Momento ribaltante deve essere equilibrato

---

## CAPITOLO 3 — Cinematica dei Fluidi

### Tipi di Flusso
**Flusso laminare:**
- Strati paralleli che non si mescolano
- Numero di Reynolds Re < 500
- Perdite per attrito maggiori

**Flusso turbolento:**
- Moto caotico, mescolamento
- Re > 2000 (in tubi)
- Perdite per attrito minori ma resistenza varia

**Flusso transitorio:**
- 500 < Re < 2000
- Instabile, difficile da analizzare

### Numero di Reynolds
- **Re = (v × D) / ν**
  - v = velocità media [m/s]
  - D = diametro [m]
  - ν = viscosità cinematica [m²/s]

### Equazione di Continuità
- **Q = A × v = costante** (lungo un condotto)
  - Q = portata [m³/s]
  - A = sezione trasversale [m²]
  - v = velocità media [m/s]

---

## CAPITOLO 4 — Dinamica dei Fluidi (Equazione di Bernoulli)

### Equazione di Bernoulli (forma energetica)
```
(p/γ) + (v²/2g) + z = costante
                         (per flusso ideale)
```

Tre componenti:
1. **p/γ** = quota di pressione [m]
2. **(v²/2g)** = quota di velocità [m]
3. **z** = quota geometrica [m]

### Interpretazione Fisica
- Somma di tre "quote" rimane costante lungo linea di corrente
- Se velocità aumenta → pressione diminuisce
- Se quota aumenta → pressione diminuisce

### Applicazioni Pratiche
- Tubi di Pitot (misura velocità)
- Venturimetri (misura portata)
- Sifoni (flusso a pressione atmosferica)
- Effetto Coanda (aderenza a superficie)

---

## CAPITOLO 5 — Perdite di Carico in Condotti

### Perdite Lineari (Darcy-Weisbach)
```
hf = f × (L/D) × (v²/2g)
```
Dove:
- **hf** = perdita di carico [m]
- **f** = fattore di attrito (Moody diagram)
- **L** = lunghezza condotto [m]
- **D** = diametro [m]
- **v** = velocità media [m/s]

### Fattore di Attrito
- **Flusso laminare:** f = 64/Re (indipendente da rugosità)
- **Flusso turbolento:** f dipende da Re e rugosità relativa (ε/D)

### Perdite Localizzate
Perdite dovute a:
- Curve e gomiti: **K ≈ 0.3-1.0**
- Allargamenti/restringimenti
- Valvole e raccordi
- Entrate/uscite

**Formula:** hL = K × (v²/2g)

### Linea Piezometrica e Linea Energetica
- **Linea energetica:** rappresenta (p/γ) + (v²/2g) + z
- **Linea piezometrica:** rappresenta (p/γ) + z
- Distanza tra le due = (v²/2g)

---

## Tabella Riassuntiva — Concetti Chiave

| Concetto | Formula | Unità | Note |
|----------|---------|-------|------|
| Peso specifico acqua | γ = 9810 N/m³ | N/m³ | A 4°C, standard |
| Pressione idrostatica | p = ρgh | Pa | h è profondità |
| Numero Reynolds | Re = vD/ν | - | Determine regime flusso |
| Portata | Q = A × v | m³/s | Costante per continuità |
| Bernoulli | p/γ + v²/2g + z = cost | m | Tre quote energetiche |
| Perdita lineale | hf = f(L/D)(v²/2g) | m | Dipende da Reynolds |

---

## Esercizi Applicativi

### Esercizio 1: Pressione a Profondità
Una piscina profonda 2 m contiene acqua.
- Calcolare pressione assoluta a fondo
- Calcolare pressione relativa a fondo
- **Soluzione:** p_rel = ρgh = 1000 × 9.81 × 2 = 19,620 Pa ≈ 19.6 kPa

### Esercizio 2: Numero Reynolds
In un tubo di diametro 50 mm scorre acqua a 2 m/s.
- Calcolare Reynolds
- Determinare regime flusso
- **Soluzione:** Re = (2 × 0.05) / 10⁻⁶ = 100,000 → Flusso turbolento

### Esercizio 3: Perdita di Carico
Tubo lungo 100 m, diametro 100 mm, velocità 1 m/s, f = 0.02
- Calcolare perdita di carico lineare
- **Soluzione:** hf = 0.02 × (100/0.1) × (1²/2×9.81) = 0.102 m ≈ 10 cm

---

## Prossimo Studio (giorni 2-5)

- Lunedì 31 ago (oggi): Capitoli 1-3 (Proprietà, Statica, Cinematica)
- Martedì 1 set: Capitoli 4-5 (Bernoulli, Perdite)
- Mercoledì 2 set: Esercizi applicativi + casi studio
- Giovedì 3 set: Approfondimento specialistico per ogni agente
- Venerdì 4 set: Debrief e preparazione operativo

---

## Supporto Disponibile

- **Teoria:** Contatta Beatrice (Slack @beatrice)
- **Risorse:** Contatta Agata (Slack #resources)
- **Coordinamento:** Roberta (Team lead Strutturale)

**Siete brillanti. Procediamo con confidence. 💪**

