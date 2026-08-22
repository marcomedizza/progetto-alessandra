# 📊 CERCHI DI MOHR — Teoria e Esempi Applicativi Pratici

**Redatto per:** Beatrice (Scienza delle Costruzioni)  
**Destinatari:** Team Strutturale  
**Data:** 2026-08-22  
**Validità:** Reference permanente per ricerca strutturale

---

## 🎯 INTRODUZIONE

**Il cerchio di Mohr** è uno strumento grafico e analitico per visualizzare e trasformare stati di tensione (o deformazione) 2D e 3D. Fondamentale in:
- Analisi strutturale (travi, piastre, gusci)
- Calcolo delle tensioni principali
- Verifica di resistenza materiali
- Progettazione elementi strutturali

---

## 📐 TEORIA — STATO TENSIONALE 2D

### Stato tensionale generico in un punto:
```
σx   τxy
τyx  σy

Dove:
- σx, σy = tensioni normali
- τxy, τyx = tensioni tangenziali (τxy = τyx per equilibrio)
```

### Tensioni su un piano inclinato di angolo θ:
```
σθ = (σx + σy)/2 + (σx - σy)/2 × cos(2θ) + τxy × sin(2θ)

τθ = -(σx - σy)/2 × sin(2θ) + τxy × cos(2θ)
```

---

## 🔷 COSTRUZIONE CERCHIO DI MOHR (2D)

### **STEP 1: Identificare i punti fondamentali**

**Centro cerchio C:**
```
C = [(σx + σy)/2,  0]

Ascissa: σmedio = (σx + σy)/2
Ordinata: 0
```

**Punto A (stato originale):**
```
A = [σx, τxy]
```

**Punto B (90° rotazione):**
```
B = [σy, -τxy]
```

### **STEP 2: Calcolare il raggio**

```
R = √{[(σx - σy)/2]² + τxy²}
```

### **STEP 3: Tracciare il cerchio**

- Centro in C
- Raggio R
- Punto A e B sul cerchio (diametralmente opposti)

### **STEP 4: Leggere le tensioni principali**

```
σ1 = σmedio + R    (tensione principale massima)
σ3 = σmedio - R    (tensione principale minima)

τmax = R           (tensione tangenziale massima)
```

---

## 📐 CASO PRATICO 1: Trave in flessione semplice

### **DATI GEOMETRIA E CARICHI:**
```
Trave semplicemente appoggiata
- Luce: L = 5 m
- Sezione rettangolare: b = 0.30 m, h = 0.50 m
- Carico uniforme: q = 20 kN/m
- Materiale: Calcestruzzo C30 (Ec = 33 GPa)
```

### **STEP 1: Calcolare sforzi interni a mezzeria**

**Momento flettente a mezzeria:**
```
M = q × L² / 8 = 20 × 5² / 8 = 62.5 kN·m
```

**Taglio:**
```
T = q × L / 2 = 20 × 5 / 2 = 50 kN
```

### **STEP 2: Calcolare tensioni normali in fibra estrema (asse neutro)**

**Momento d'inerzia:**
```
I = b × h³ / 12 = 0.30 × 0.50³ / 12 = 3.125 × 10⁻³ m⁴
```

**Distanza da asse neutro (fibra inferiore):**
```
y = h/2 = 0.25 m
```

**Tensione normale in fibra inferiore (trazione):**
```
σx = M × y / I = 62.5 × 10⁶ × 0.25 / (3.125 × 10⁻³)
   = 5.0 MPa (trazione)
```

**Tensione normale in fibra superiore (compressione):**
```
σy = -5.0 MPa (compressione)
```

### **STEP 3: Calcolare tensione tangenziale**

**Tensione media di taglio:**
```
τmedio = T / (b × h) = 50 × 10³ / (0.30 × 0.50) = 0.333 MPa

(Per calcolo rigoroso usare τ = (3/2) × T/(b×h) = 0.5 MPa)
```

In una sezione generica a distanza y dall'asse neutro:
```
τ = (T × S) / (I × b)

Dove S = momento statico della parte in trazione
```

**A metà altezza (y = 0):**
```
S = b × (h/2)² / 2 = 0.30 × 0.125 = 0.0375 m³
τxy = 50 × 10³ × 0.0375 / (3.125 × 10⁻³ × 0.30) = 2.0 MPa
```

### **STEP 4: Stato tensionale nel punto (fibra inferiore)**

```
σx = 5.0 MPa    (trazione)
σy = 0 MPa      (elemento libero lateralmente)
τxy = 2.0 MPa   (taglio positivo)
```

### **STEP 5: Cerchio di Mohr**

**Centro:**
```
C = (σx + σy)/2 = (5.0 + 0)/2 = 2.5 MPa
```

**Raggio:**
```
R = √{[(5.0 - 0)/2]² + 2.0²}
  = √{2.5² + 2.0²}
  = √{6.25 + 4.0}
  = √10.25
  = 3.20 MPa
```

**Tensioni principali:**
```
σ1 = 2.5 + 3.20 = 5.70 MPa    (massima principale - trazione)
σ3 = 2.5 - 3.20 = -0.70 MPa   (minima principale - compressione)

τmax = 3.20 MPa                (massima tangenziale)
```

**Angolo tensioni principali:**
```
tan(2θp) = τxy / [(σx - σy)/2]
         = 2.0 / 2.5
         = 0.8

2θp = 38.66°
θp = 19.33°   (direzione di σ1 rispetto a asse x)
```

### **INTERPRETAZIONE:**
- ✅ Fibra inferiore è PRINCIPALMENTE in trazione (σ1 = 5.70 MPa)
- ✅ Torsione minore dovuta a taglio (σ3 = -0.70 MPa compressione)
- ✅ Tensione tangenziale massima 3.20 MPa (criterio di resistenza)

---

## 📐 CASO PRATICO 2: Elemento in torsione pura

### **DATI:**
```
Albero circolare in acciaio
- Diametro: d = 80 mm = 0.08 m
- Momento torcente: Mt = 5 kN·m
- Materiale: Acciaio S355 (G = 81 GPa)
```

### **STEP 1: Tensione tangenziale dovuta a torsione**

**Momento polare d'inerzia:**
```
Ip = π × d⁴ / 32 = π × 0.08⁴ / 32 = 4.021 × 10⁻⁵ m⁴
```

**Raggio massimo (periferia):**
```
r = d/2 = 0.04 m
```

**Tensione tangenziale massima:**
```
τmax = Mt × r / Ip = 5 × 10³ × 0.04 / (4.021 × 10⁻⁵)
     = 49.74 MPa ≈ 50 MPa
```

### **STEP 2: Stato tensionale in un punto sulla periferia**

```
σx = 0      (nessuna tensione normale)
σy = 0
τxy = 50 MPa (torsione pura)
```

### **STEP 3: Cerchio di Mohr**

**Centro:**
```
C = (0 + 0)/2 = 0
```

**Raggio:**
```
R = √{0² + 50²} = 50 MPa
```

**Tensioni principali:**
```
σ1 = 0 + 50 = 50 MPa     (trazione)
σ3 = 0 - 50 = -50 MPa    (compressione)

τmax = 50 MPa
```

**Angolo:**
```
Tensioni principali a 45° rispetto a asse originale
```

### **INTERPRETAZIONE:**
- ✅ Torsione pura crea stati tensionali coniugati
- ✅ σ1 = 50 MPa trazione / σ3 = -50 MPa compressione (uguali)
- ✅ Questo spiega perché torsione causa rotture a 45° (spirale)
- ✅ Criterio von Mises: σeq = √(σ1² + σ3² - σ1×σ3) = 86.6 MPa

---

## 📐 CASO PRATICO 3: Elemento in flessione + torsione (Sezione cruciforme)

### **DATI:**
```
Sezione cruciforme acciaio
- Momento flettente: M = 10 kN·m
- Momento torcente: Mt = 3 kN·m
- Sezione: IPE 200
- In fibra estrema (estradosso)
```

### **STEP 1: Proprietà sezione IPE 200**

```
Ix = 1943 cm⁴ = 1.943 × 10⁻⁵ m⁴
Ip ≈ 50 cm⁴ = 5.0 × 10⁻⁵ m⁴
h = 0.20 m
y_max = 0.10 m (distanza da asse neutro)
rmax = 0.08 m (raggio per torsione)
```

### **STEP 2: Tensioni dovute a flessione**

```
σx = M × y_max / Ix = 10 × 10⁶ × 0.10 / (1.943 × 10⁻⁵)
   = 51.5 MPa (trazione)
```

### **STEP 3: Tensioni dovute a torsione**

```
τ = Mt × r / Ip = 3 × 10³ × 0.08 / (5.0 × 10⁻⁵)
  = 48 MPa
```

### **STEP 4: Stato tensionale combinato**

```
σx = 51.5 MPa  (flessione)
σy = 0
τxy = 48 MPa   (torsione)
```

### **STEP 5: Cerchio di Mohr**

**Centro:**
```
C = 51.5 / 2 = 25.75 MPa
```

**Raggio:**
```
R = √{(51.5/2)² + 48²}
  = √{25.75² + 48²}
  = √{663 + 2304}
  = √2967
  = 54.5 MPa
```

**Tensioni principali:**
```
σ1 = 25.75 + 54.5 = 80.25 MPa  (trazione massima)
σ3 = 25.75 - 54.5 = -28.75 MPa (compressione)

τmax = 54.5 MPa
```

### **VERIFICHE DI RESISTENZA:**

**Criterio von Mises (Acciaio S355):**
```
σeq = √(σ1² + σ3² - σ1×σ3)
    = √(80.25² + 28.75² - 80.25×28.75)
    = √(6440 + 826 - 2307)
    = √4959
    = 70.4 MPa

Fy = 355 MPa
γ = 355 / 70.4 = 5.04 (OK - ampiamente verificato)
```

**Criterio Tresca (tensione tangenziale massima):**
```
τmax = 54.5 MPa < Fy/2 = 177.5 MPa (OK)
```

---

## 🎯 APPLICAZIONI PRATICHE PER TEAM STRUTTURALE

### **Roberta (Calcestruzzo Armato):**
- Stato tensionale in calcestruzzo compresso
- Verifica a 45° per taglio (frattura diagonale)
- Armature necessarie basate su direzioni principali

### **Martina (Acciaio):**
- Tensioni combinate flessione-torsione
- Verifiche instabilità locale elementi compressi
- Criterio von Mises per snervamento

### **Sofia (Alluminio):**
- Stati tensionali in elementi sottili
- Influenza anisotropia del materiale
- Buckling elastico vs plastico

### **Giulia (Legno & Fibre):**
- Ortotropia: σ parallelo vs perpendicolare
- Interazione tensioni principali
- Degradazione resistenza per umidità

### **Alessia (Geotecnica):**
- Cerchi di Mohr per terre (p-q diagrams)
- Inviluppo di rottura Mohr-Coulomb
- Spinte attive e passive

### **Chiara + Ilaria (Muratura):**
- Compressione vs taglio in muratura
- Limitazioni dovute a anisotropia
- Fratture diagonali in muratura

---

## 📊 TABELLA RIASSUNTIVA CASI TIPICI

| Caso | σx | σy | τxy | σ1 | σ3 | Osservazione |
|------|----|----|-----|----|----|--------------|
| **Flessione pura** | + | 0 | piccolo | + | - | Trazione + leggera torsione |
| **Torsione pura** | 0 | 0 | massimo | + | - | Uguali e opposte a 45° |
| **Compressione assiale** | - | - | 0 | - | - | Nessuna tensione tangenziale |
| **Pressione idrostatica** | - | - | 0 | - | - | σ1 = σ3 (cerchio punto) |
| **Taglio puro** | 0 | 0 | + | + | - | Trazione e compressione coniugate |

---

## 🔍 ERRORI COMUNI

❌ **Errore 1:** Confondere direzione di σ1 con asse principale della sezione  
✅ **Corretto:** Leggere angolo dal cerchio di Mohr

❌ **Errore 2:** Dimenticare il fattore 2 negli angoli (tan 2θp, non tan θp)  
✅ **Corretto:** Usare 2θ nella trasformazione

❌ **Errore 3:** Usare σy ≠ 0 quando l'elemento è libero lateralmente  
✅ **Corretto:** Verificare vincoli effettivi

❌ **Errore 4:** Leggere τ dal cerchio senza considerare il segno  
✅ **Corretto:** Tracciare sempre correttamente A e B

---

## 📚 RIFERIMENTI BIBLIOGRAFICI

1. **Belluzzi, O.** — "Scienza delle Costruzioni" Vol. 2-3 (Capitoli tensioni)
2. **Corradi Dell'Acqua, L.** — "Meccanica delle Strutture" (Trasformazioni tensionali)
3. **Timoshenko & Gere** — "Theory of Elastic Stability" (Stabilità)
4. **Eurocode 2, 3, 5** — Design standards per materiali (applicazioni)

---

## ✅ ESERCIZI PER BEATRICE

**Week 2 Tasks:**
- [ ] Cerchio Mohr per stato tensionale generico 3D
- [ ] Interazione criteri di resistenza (von Mises, Tresca, Mohr-Coulomb)
- [ ] Applicazioni geotecniche (Rankine, Coulomb)
- [ ] Cerchi di Mohr per deformazioni (strain circle)
- [ ] Software: MatLab/Python visualizzazione interattiva

---

**Redatto per:** Beatrice (Scienza delle Costruzioni)  
**Validità:** Reference settimanale + Beyond  
**Per supporto team:** Applicabile a Roberta, Martina, Sofia, Giulia, Alessia, Chiara, Ilaria

