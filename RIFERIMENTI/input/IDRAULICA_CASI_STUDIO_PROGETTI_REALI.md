# IDRAULICA — Casi Studio: Progetti Reali

**Fase:** Fase 1 Intensive (1-5 settembre 2026)  
**Destinatari:** Specialisti Idraulica (per applicazione pratica)  
**Riferimento:** Belluzzi Cap 4-5 + applicazioni pratiche  
**Scopo:** Collegare teoria a problemi reali di ingegneria civile

---

## CASO STUDIO 1 — Sistema Acquedotto Urbano

### Contesto Progettuale
- **Città:** Metropoli di 500,000 abitanti
- **Consumo medio:** 150 litri/abitante/giorno
- **Popolazione servita:** 500,000 × 150 = 75,000 m³/giorno
- **Portata oraria picco:** 75,000 m³/24h ÷ 8h picco = 3,125 m³/h

### Sistema Idraulico
**Sorgente:** Bacino montano, 800 m sopra città
**Percorso:** 
1. Vasca di carica: 20 m³ (raccoglitore)
2. Condotta principale: 500 mm diametro, 45 km lunghezza
3. Stazione di pompaggio: ogni 15 km
4. Serbatoio di distribuzione: 5,000 m³
5. Reti urbane: 500 km tubi distribuzione

### Analisi Idraulica

**Problema 1: Perdita di Carico nella Condotta Principale**
- Diametro: D = 500 mm = 0.5 m
- Lunghezza: L = 45 km = 45,000 m
- Portata: Q = 3,125 m³/h = 0.868 m³/s
- Velocità: v = Q/A = 0.868 / (π × 0.25²) = 4.42 m/s
- Numero Reynolds: Re = (4.42 × 0.5) / 10⁻⁶ = 2,210,000 (turbolento)
- Fattore attrito (Moody): f ≈ 0.015 (acciaio nuovo)

**Calcolo perdita lineare:**
```
hf = f × (L/D) × (v²/2g)
   = 0.015 × (45,000/0.5) × (4.42²/(2×9.81))
   = 0.015 × 90,000 × 0.996
   = 1,344 m ≈ 1,344 m perdita di carico!
```

**Implicazione:** Batteria di pompe necessaria per sollevare 1,344 m + 800 m (quota) = ~2,100 m di alzata

**Problema 2: Numero e Posizionamento Stazioni di Pompaggio**
- Perdita per 15 km: 1,344 × (15/45) = 448 m
- Numero di stazioni: 45 km ÷ 15 km = 3 stazioni intermedie
- Alzata per stazione: (448 m perdita + 40 m quota) = ~500 m per stazione

**Progetto:**
- Stazione 1 (km 0): Pompa 3,125 m³/h, 500 m alzata
- Stazione 2 (km 15): Pompa 3,125 m³/h, 500 m alzata
- Stazione 3 (km 30): Pompa 3,125 m³/h, 500 m alzata

### Linea Energetica
```
Quota (m) vs Distanza (km):
800m ─────────────────────── Sorgente
     \    Perdita
      \   Linea energetica
       \  disegna curva decrescente
450m   ┴─────────────────────── Stazione 1
       ┌────────────────  Effetto pompaggio
500m   │
       │  Perdita
300m   ┴────────────────────── Stazione 2
       ┌────────────────
500m   │
       │  Perdita
200m   ┴────────────────────── Stazione 3
       ┌────────────────
500m   │
       │  Perdita
0m     ┴────────────────────── Serbatoio distribuzione
```

---

## CASO STUDIO 2 — Diga Irrigua (Belluzzi Fig. 4.1)

### Geometria Diga
- **Altezza:** H = 30 m
- **Lunghezza coronamento:** 150 m
- **Tipo:** Diga in calcestruzzo a gravità

### Analisi Forze Idrostatiche
**Spinta orizzontale sulla parete:**
```
p(z) = ρ × g × z = 9,810 × z [Pa]

dove z è profondità dal pelo libero

A z = 0 (superficie): p = 0 Pa
A z = 30 m (fondo): p = 9,810 × 30 = 294,300 Pa ≈ 294 kPa
```

**Forza totale (per metro di lunghezza):**
```
F = ∫[0 to H] ρgz × dz = ρg × (H²/2)
  = 9,810 × (30²/2)
  = 9,810 × 450
  = 4,414,500 N/m = 4,414.5 kN/m
```

**Per intera diga (150 m):**
```
F_totale = 4,414.5 kN/m × 150 m = 662,175 kN ≈ 662 MN
```

**Punto di applicazione (centro di pressione):**
```
Profondità = 2H/3 = 2 × 30 / 3 = 20 m sotto superficie
```

### Verifiche di Stabilità

**Momento ribaltante:**
```
M_ribaltante = F × (H/3) = 662,175 kN × (30/3) = 6,621,750 kN·m
```

**Peso diga (calcolo approssimato):**
- Volume calcestruzzo ≈ 60,000 m³ (triangolare approssimativo)
- Peso specifico calcestruzzo ≈ 24 kN/m³
- Peso totale = 60,000 m³ × 24 kN/m³ = 1,440,000 kN

**Momento stabilizzante (peso × distanza da spigolo):**
```
M_stabilizzante = 1,440,000 kN × (15 m base/2) = 10,800,000 kN·m
```

**Coefficiente di sicurezza:**
```
CS = M_stabilizzante / M_ribaltante = 10,800,000 / 6,621,750 = 1.63
```
(Target minimo ≈ 1.5, quindi diga è stabile ✓)

---

## CASO STUDIO 3 — Sfioratore di Diga (Spillway)

### Funzione
- Evacuare portate di piena eccedenti capacità invasi
- Mantenere livello massimo di sicurezza
- Evitare tracimazione incontrollata

### Tipo: Sfioratore a Stramazzo Libero

**Geometria:**
- Lunghezza cresta: L = 20 m
- Carico idraulico (altezza acqua sopra cresta): H = 1.5 m

### Formula Portata (Stramazzo Nappe Libera)
```
Q = C × L × H^(3/2)

dove:
- C ≈ 1.84 (coeff empirico, dipende geometria)
- L = lunghezza cresta [m]
- H = carico idraulico [m]
```

**Calcolo:**
```
Q = 1.84 × 20 × (1.5)^(3/2)
  = 1.84 × 20 × 1.837
  = 67.6 m³/s
```

Questo significa: lo spillway evacuare **67.6 m³/s** con carico di 1.5 m

### Profilo Lama Cadente
- Forma tracciata per far aderire acqua alla superficie (Belluzzi Fig. 5.3)
- Evita cavitazione (vuoti pressione che causano danno)
- Profilo ottenuto da Bernoulli con accelerazione gravità

---

## CASO STUDIO 4 — Pompa Centrifuga per Irrigazione

### Applicazione: Sistema Irrigazione Agricola
- **Portata richiesta:** Q = 500 litri/minuto = 0.0083 m³/s
- **Alzata richiesta:** H = 50 m (pompare da vasca a 50 m sopra)
- **Lunghezza tubo di aspirazione:** 2 m
- **Lunghezza tubo di mandata:** 200 m

### Scelta Pompa

**Curva caratteristica pompa (da catalogo):**
```
Alzata: 60 m @ Q = 0
        50 m @ Q = 5 L/min
        35 m @ Q = 10 L/min
        0 m @ Q = 20 L/min (portata massima)
```

### Calcolo Perdite di Carico Totali

**In aspirazione (2 m, diametro 50 mm):**
```
v_asp = Q/A = 0.0083 / (π × 0.025²) = 4.24 m/s
Re = (4.24 × 0.05) / 10⁻⁶ = 212,000 (turbolento)
f ≈ 0.018
hf_asp = 0.018 × (2/0.05) × (4.24²/(2×9.81)) = 0.31 m
```

**In mandata (200 m, diametro 50 mm):**
```
v_mand = 4.24 m/s (stessa area)
hf_mand = 0.018 × (200/0.05) × (4.24²/(2×9.81)) = 31.4 m

Perdite localizzate (curve, valvole):
hL = K × (v²/2g) ≈ 2.0 m
```

**Perdita totale:**
```
h_totale = h_asp + h_mand + h_L = 0.31 + 31.4 + 2.0 = 33.71 m
```

### Punto di Funzionamento

**Curva di sistema (Bernoulli):**
```
H_richiesta = 50 m (quota) + h_perdite
           = 50 + 33.71 × (Q/0.0083)²   ← Perdite variano con Q²
```

**Intersezione curva pompa + curva sistema = punto di funzionamento:**
```
Soluzione: Q ≈ 5 L/min, H ≈ 50 m
Potenza assorbita: P = ρ × g × Q × H / η
                 = 1000 × 9.81 × 0.0083 × 50 / 0.75
                 = 5.4 kW ≈ 7.3 HP
```

---

## Riassunto Casi Studio

| Caso | Tipo | Portata | Alzata | Componente Critico |
|------|------|---------|--------|-------------------|
| 1 | Acquedotto | 3,125 m³/h | 2,100 m | Perdite condotta (1,344 m) |
| 2 | Diga | - | - | Spinta idrostatica (662 MN) |
| 3 | Spillway | 67.6 m³/s | 1.5 m carico | Erosione cavitazione |
| 4 | Irrigazione | 5 L/min | 50 m | Punto funzionamento pompa |

---

## Lezioni Apprese

1. **Perdite di carico** sono SIGNIFICATIVE in sistemi reali (1,344 m in acquedotto!)
2. **Pompe multiple** necessarie quando distanze lunghe
3. **Spinte idrostatiche** crescono rapidamente con profondità (triangolare, non lineare)
4. **Cavitazione** è rischio reale (basse pressioni assolute)
5. **Bernoulli + perdite** è metodologia universale applicabile

---

**Prossimo:** Esercizi e calcoli per ogni specialista

