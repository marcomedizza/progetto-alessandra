# IDRAULICA — Esercizi Intensivo (Belluzzi Cap 1-5)

**Fase:** Fase 1 Intensive (1-5 settembre 2026)  
**Destinatari:** Specialisti Idraulica (esercitazione giornaliera)  
**Formato:** 5 esercizi/giorno × 5 giorni = 25 esercizi totali  
**Scopo:** Padronanza concetti attraverso problem-solving pratico

---

## GIORNO 1 (LUN 31 AGO) — Proprietà Fluidi & Statica

### Esercizio 1.1 — Densità e Peso Specifico
**Problema:**
Un serbatoio contiene olio con densità ρ = 850 kg/m³.
Calcolare:
a) Peso specifico dell'olio
b) Massa di olio in serbatoio di 50 m³
c) Pressione sul fondo a profondità 4 m

**Dati:**
- ρ = 850 kg/m³
- g = 9.81 m/s²
- V = 50 m³
- h = 4 m

**Soluzione:**
```
a) γ = ρ × g = 850 × 9.81 = 8,338.5 N/m³ ≈ 8.34 kN/m³

b) m = ρ × V = 850 kg/m³ × 50 m³ = 42,500 kg

c) p = γ × h = 8,338.5 N/m³ × 4 m = 33,354 Pa ≈ 33.4 kPa
   Nota: pressione relativa (gauge). 
   Assoluta = 33.4 + 101.3 = 134.7 kPa
```

---

### Esercizio 1.2 — Viscosità e Numero Reynolds
**Problema:**
Nel tubo orizzontale di diametro 25 mm scorre olio (da Esercizio 1.1) a velocità media 2 m/s.
Viscosità cinematica olio: ν = 15 × 10⁻⁶ m²/s

Calcolare:
a) Numero Reynolds
b) Regime di flusso (laminare/turbolento)
c) Fattore di attrito (assume tubo liscio)

**Soluzione:**
```
a) Re = (v × D) / ν
      = (2 m/s × 0.025 m) / (15 × 10⁻⁶ m²/s)
      = 0.05 / (15 × 10⁻⁶)
      = 3,333

b) Re = 3,333 → FLUSSO TRANSITORIO (500 < Re < 2000... no, Re > 2000)
   Re = 3,333 → FLUSSO TURBOLENTO (Re > 2000)
   Nota: confine a Re ≈ 2000-2300 per tubi lisci

c) Per flusso turbolento in tubo liscio (Blasius):
   f = 0.316 / Re^0.25
     = 0.316 / (3333)^0.25
     = 0.316 / 7.58
     = 0.0417 ≈ 0.042
```

---

### Esercizio 1.3 — Spinta Idrostatica su Parete
**Problema:**
Serbatoio rettangolare con parete verticale di larghezza 6 m, profondità acqua 3 m.
Calcolare:
a) Forza totale su parete
b) Profondità del centro di pressione
c) Momento ribaltante rispetto alla base

**Dati:**
- Larghezza parete: B = 6 m
- Profondità: H = 3 m
- ρ = 1000 kg/m³, g = 9.81 m/s²

**Soluzione:**
```
a) F = (1/2) × γ × H² × B
     = (1/2) × 9810 × 3² × 6
     = (1/2) × 9810 × 9 × 6
     = 264,870 N ≈ 265 kN

b) Profondità centro pressione (da superficie):
   zcp = H / 3 = 3 / 3 = 1 m
   
   (Per parete rettangolare: center di pressione è a 1/3 della profondità
    dal fondo, o 2/3 dal top)

c) Momento ribaltante (rispetto a base della parete):
   M = F × (H/3) = 264,870 N × (3/3) = 264,870 N·m
   
   Nota: braccio è H/3 perché forza agisce a H/3 da fondo
```

---

### Esercizio 1.4 — Principio di Pascal e Moltiplicatore Idraulico
**Problema:**
Pressa idraulica con cilindro piccolo (d₁ = 20 mm) e cilindro grande (d₂ = 100 mm).
Forza applicata su cilindro piccolo: F₁ = 500 N

Calcolare:
a) Pressione nel sistema
b) Forza su cilindro grande
c) Vantaggio meccanico

**Soluzione:**
```
a) Pressione (Pascal):
   p = F₁ / A₁ = F₁ / (π × r₁²)
     = 500 / (π × 0.01²)
     = 500 / (π × 0.0001)
     = 500 / 0.0003142
     = 1,591,549 Pa ≈ 1.59 MPa

b) Forza su cilindro grande:
   F₂ = p × A₂ = p × (π × r₂²)
      = 1,591,549 × (π × 0.05²)
      = 1,591,549 × (π × 0.0025)
      = 1,591,549 × 0.007854
      = 12,500 N

c) Vantaggio meccanico:
   VM = F₂ / F₁ = 12,500 / 500 = 25
   
   Equivalente:
   VM = A₂ / A₁ = (d₂/d₁)²
      = (100/20)²
      = (5)²
      = 25
```

---

### Esercizio 1.5 — Barometro ad Acqua
**Problema:**
Barometro ad acqua (non a mercurio). Pressione atmosferica standard = 101,325 Pa.
Calcolare altezza colonna d'acqua in equilibrio.

**Soluzione:**
```
p_atm = ρ_acqua × g × h
h = p_atm / (ρ × g)
  = 101,325 Pa / (1000 kg/m³ × 9.81 m/s²)
  = 101,325 / 9,810
  = 10.33 m

Nota: Questo è perché barometri ad acqua sono impraticabili (~10 m di altezza!)
      Mercurio è usato: h = 0.76 m (760 mm) per pressione atmosferica standard
      Densità mercurio ≈ 13,600 kg/m³
      Verifica: 101,325 / (13,600 × 9.81) = 0.76 m ✓
```

---

## GIORNO 2 (MAR 1 SET) — Cinematica & Bernoulli

### Esercizio 2.1 — Equazione di Continuità
**Problema:**
Condotta che cambia diametro: d₁ = 100 mm, d₂ = 50 mm
Velocità in sezione 1: v₁ = 2 m/s

Calcolare:
a) Velocità in sezione 2
b) Portata
c) Rapporto velocità

**Soluzione:**
```
a) Per continuità: Q = A₁ × v₁ = A₂ × v₂ = cost
   A₁ × v₁ = A₂ × v₂
   
   (π × 0.05²) × 2 = (π × 0.025²) × v₂
   0.005 × 2 = 0.00196 × v₂
   0.01 = 0.00196 × v₂
   v₂ = 0.01 / 0.00196 = 5.1 m/s

b) Portata:
   Q = A₁ × v₁ = π × 0.05² × 2 = 0.0157 m³/s ≈ 15.7 L/s

c) Rapporto velocità:
   v₂/v₁ = (d₁/d₂)² = (100/50)² = 4
   
   v₂ = 4 × v₁ = 4 × 2 = 8 m/s (teorico, ma abbiamo 5.1... ricontro)
   
   Nota: errore nel conto precedente:
   (π × 0.05²) × 2 = (π × 0.025²) × v₂
   (0.025)² × 2 = (0.025)² ÷ 4 × v₂
   
   Correzione usando rapporto aree:
   A₁/A₂ = (d₁/d₂)² = (100/50)² = 4
   v₂ = (A₁/A₂) × v₁ = 4 × 2 = 8 m/s ✓
```

---

### Esercizio 2.2 — Equazione di Bernoulli (Tubo Inclinato)
**Problema:**
Tubo inclinato con acqua, nessun attrito (ideale).
Punto 1: z₁ = 0 m, v₁ = 1 m/s, p₁ = 0 Pa (gauge/relativa)
Punto 2: z₂ = 5 m, v₂ = ?

Calcolare pressione in punto 2 (assume continuità Q = cost).

**Soluzione:**
```
Bernoulli: (p₁/γ) + (v₁²/2g) + z₁ = (p₂/γ) + (v₂²/2g) + z₂

Per sezione costante (nessun cambiamento diametro):
v₁ = v₂ = 1 m/s (per continuità)

(0/9810) + (1²/(2×9.81)) + 0 = (p₂/9810) + (1²/(2×9.81)) + 5

0 + 0.051 + 0 = (p₂/9810) + 0.051 + 5

0 = (p₂/9810) + 5

p₂/9810 = -5

p₂ = -49,050 Pa

Nota: Pressione NEGATIVA (relativa)!
      Assoluta = -49,050 + 101,325 = 52,275 Pa ≈ 0.52 atm
      
      Questo è fisicamente possibile, ma se scende sotto ~-91 kPa (valore di
      cavitazione per acqua a 20°C), si formano bolle di vapore (cavitazione).
```

---

### Esercizio 2.3 — Teorema di Torricelli
**Problema:**
Serbatoio con buco sul fondo a profondità h = 2 m sotto superficie.
Calcolare velocità di uscita acqua (ignore friction).

**Soluzione:**
```
Bernoulli tra superficie (punto 1) e uscita (punto 2):
(p₁/γ) + (v₁²/2g) + z₁ = (p₂/γ) + (v₂²/2g) + z₂

Condizioni:
- p₁ = p₂ = pressione atmosferica (0 gauge)
- v₁ ≈ 0 (superficie è grande, velocità è minuscola)
- z₁ = h = 2 m, z₂ = 0 m
- Differenza quota = h

Semplificazione:
0 + 0 + 2 = 0 + (v₂²/(2×9.81)) + 0

v₂² = 2 × 9.81 × 2 = 39.24

v₂ = √39.24 = 6.26 m/s

Formula generale: v = √(2gh)
```

---

### Esercizio 2.4 — Portata da Orifizio
**Problema:**
Orifizio circolare su parete serbatoio: d = 10 mm
Profondità centro orifizio: h = 3 m
Coefficiente di contrazione: Cc = 0.62

Calcolare portata

**Soluzione:**
```
Velocità teorica (Torricelli):
v = √(2gh) = √(2 × 9.81 × 3) = √58.86 = 7.67 m/s

Area nominale orifizio:
A_nom = π × (0.005)² = 7.85 × 10⁻⁵ m²

Area di vena (area contratta):
A_vena = Cc × A_nom = 0.62 × 7.85 × 10⁻⁵ = 4.87 × 10⁻⁵ m²

Portata:
Q = A_vena × v = 4.87 × 10⁻⁵ × 7.67 = 3.74 × 10⁻⁴ m³/s
  = 0.374 L/s ≈ 22.4 L/min
```

---

## GIORNO 3 (MER 2 SET) — Perdite di Carico

### Esercizio 3.1-3.5
[Omessi per brevità, ma seguono pattern simile di calcolo Darcy-Weisbach, Moody diagram, perdite localizzate]

---

## GIORNO 4 (GIO 3 SET) — Dinamica Avanzata

### Esercizio 4.1-4.5
[Diagrammi energetici, linee piezometriche, casi combinati]

---

## GIORNO 5 (VEN 4 SET) — Integrazione e Sintesi

### Esercizio 5.1 — Progetto Completo Mini-Acquedotto
**Problema Integrativo:**
Progettare mini-acquedotto che:
- Prende acqua da sorgente a quota 150 m
- Serve villaggio a quota 100 m
- Distanza = 5 km
- Portata richiesta = 100 L/min
- Calcolare: diametro tubo, perdite, pressione finale, eventuale pompa?

[Soluzione richiede: calcolo velocità ottimale, perdita Darcy-Weisbach, verifiche cavitazione, selezione pompa...]

---

## Chiavi di Lettura per Esercizi

### Pattern Risolutivo Standard
1. **Identifica tipo problema** (statica, cinematica, energia, etc)
2. **Scrivi equazioni pertinenti** (Bernoulli, continuità, Darcy-Weisbach)
3. **Raccogli dati** e **converti unità** se necessario
4. **Applica formula** sostituendo valori
5. **Verifica ragionevolezza risultato** (pressioni negative? Velocità unreasonable? Portate fisiche?)
6. **Commenta interpretazione** (cosa significa il risultato?)

### Errori Comuni
- ❌ Dimenticare fattore 2 in Bernoulli (v²/2g non v²/g)
- ❌ Mescolare pressioni gauge vs assolute
- ❌ Invertire formule (Re =?, non v × D / ν backwards)
- ❌ Unità inconsistenti (m/s con diametro in mm?)
- ❌ Ignorare perdite localizzate (valvole, curve)

---

## Risorse Supporto

**Fogli di Calcolo Utili:**
- Diagramma Moody (riprodotto in Belluzzi Fig. 5.2)
- Tabelle fattori attrito per vari materiali tubi
- Coefficienti perdite localizzate (curve 0.3-1.0, valvole 0.5-5.0)

**Tools Online:**
- Online Moody diagram calculator
- Darcy-Weisbach solver
- Unit converter (m/s, cm/s, ft/s)

**Contatti:**
- Beatrice: Domande teoriche (supporto concetti)
- Specialisti: Scambio soluzioni esercizi, group review venerdì
- Roberta: Coordinamento, debrief settimanale

---

**Completare 5 esercizi/giorno → Master concetti Belluzzi Cap 1-5**

**Venerdì 4 settembre: Sintesi e assessment finale Fase 1 Intensive**

