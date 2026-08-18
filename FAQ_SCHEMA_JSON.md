# ❓ FAQ & TROUBLESHOOTING — Schema JSON Alessandra

**Data**: 2026-08-18  
**Audience**: Benedetta + Team Architettura  
**Scopo**: Risolvere dubbi comuni su schema JSON

---

## ❓ DOMANDE FREQUENTI

### **Q1: Coordinate e Sistema di Riferimento**

**D**: Che sistema di coordinate usiamo?  
**R**: **Globale XYZ destrorso (right-handed)**
- X = sinistra-destra (>>)
- Y = basso-alto (↑)
- Z = verso-indietro (⊙)

```
      Y (up)
      ↑
      |     Z (out)
      |    /
      |   /
   ---|--→ X (right)
```

**Convenzioni:**
- **Positive Y** = verso l'alto
- **Negative carichi** = verso il basso (gravità)
- **Angoli** = senso antiorario (right-hand rule)

---

### **Q2: Formato Coordinate — Metri vs Millimetri?**

**D**: Devo usare metri o mm?  
**R**: **Dipende dal `units.length` nel JSON**

```json
{
  "units": {
    "length": "m"  // Usa sempre METRI nel JSON
  }
}
```

✅ **Sempre** convertire a **metri** nel JSON (coerenza).  
Se user disegna in mm, UI converte a m prima di salvare JSON.

---

### **Q3: Ordine Nodi Elemento**

**D**: Elemento `[1, 2]` significa 1→2 o 2→1?  
**R**: **Sempre da inizio a fine: node[0] = inizio, node[1] = fine**

```json
{
  "id": 1,
  "nodes": [1, 2],  // 1 = inizio, 2 = fine
  "type": "frame_2d"
}
```

**Implicazioni:**
- **Locale x-axis** = direzione 1→2
- **Elementi 2D**: xy-plane (z=0)
- **Orientamento**: right-hand rule

---

### **Q4: Dove Vanno I Rilasci?**

**D**: Elemento con rilascio su Mz — dove lo specifico?  
**R**: In `properties.releases` (start/end)

```json
{
  "properties": {
    "releases": {
      "start": {"Mz": "fixed"},    // Nodo 1 = incastrato
      "end": {"Mz": "free"}        // Nodo 2 = libero
    }
  }
}
```

**Cosa significa:**
- `"fixed"` = blocca il momento (incastro)
- `"free"` = libero di ruotare (cerniera)

---

### **Q5: Carichi Distribuiti — Come Specificare?**

**D**: Come specifichicare carico distribuito su trave?  
**R**: In `element_loads` con `type: distributed`

```json
{
  "element_id": 2,
  "type": "distributed",
  "direction": "global_y",  // verso l'alto o basso
  "value": -30.0,            // -30 kN/m = verso il basso
  "position": 0.5            // al centro (opzionale)
}
```

**Interpretazione:**
- `value`: Carico per unità lunghezza (kN/m)
- **Negativo** = verso il basso (gravità)
- Se vuoi **triangolare**, usa 2 load_cases (inizio e fine)

---

### **Q6: P-Delta — Quando Attivarlo?**

**D**: Devo sempre usare P-Delta?  
**R**: **No. Dipende da elementi snelli**

```json
{
  "solver_parameters": {
    "static": {
      "nonlinear_p_delta": {
        "enabled": true,        // ✅ Sì per colonne snelle
        "load_steps": 5         // 5 step carico
      }
    }
  }
}
```

**Attiva P-Delta quando:**
- ✅ Colonne snelle (h/b > 20)
- ✅ Effetti 2° ordine significativi
- ✅ Necessario per NTC 2018

**Non necessario:**
- ❌ Travi molto rigide
- ❌ Piccoli spostamenti (<< 1% luce)

---

### **Q7: Materiali — Dove Hardcoded i Valori?**

**D**: Inserisco E, fy, ρ ogni volta? O sono in database?  
**R**: **Misto:**

```json
{
  "material_id": "steel_S235"  // ID → lookup database
}
```

**Database hardcoded** (Natalia popola):
```python
MATERIALS = {
  "steel_S235": {
    "E": 210e9,
    "fy": 235e6,
    "rho": 7850
  },
  "concrete_C30": {
    "E": 33e9,
    "fc": 30e6,
    "rho": 2400
  }
}
```

**Se material_id non in database:**
- ❌ Errore di validazione
- Suggerimento: Usa ID standard (S235, C30, etc.)

---

### **Q8: Sezioni — Computed vs Hardcoded?**

**D**: Se uso HEA200 standard, calcolo area o uso tabella?  
**R**: **Usa tabella! Imposta `computed: false`**

```json
{
  "section_id": "HEA200",
  "computed": false,  // ✅ Usa valori tabulati
  "properties": {
    "area": 0.005380,
    "inertia_y": 1.25e-5
  }
}
```

**Se `computed: true`:**
```json
{
  "section_id": "custom_rect",
  "computed": true,  // Calcola da geometria
  "geometry": {
    "b": 0.2,
    "h": 0.3
  }
}
```

---

### **Q9: Load Combinations — Fattori SLU vs SLS**

**D**: Quali fattori uso per SLU?  
**R**: **Codice italiano NTC 2018:**

```json
{
  "id": "comb_slu",
  "name": "SLU (Stato Limite Ultimo)",
  "cases": [
    {"case_id": "dead", "factor": 1.35},      // Peso proprio
    {"case_id": "live", "factor": 1.5},       // Carico utile
    {"case_id": "wind", "factor": 1.5}        // Vento
  ]
}
```

**SLS (Stato Limite di Servizio):**
```json
{
  "id": "comb_sls",
  "cases": [
    {"case_id": "dead", "factor": 1.0},
    {"case_id": "live", "factor": 1.0}
  ]
}
```

---

### **Q10: Fortran I/O — Binary vs ASCII?**

**D**: Quando usare binary vs ASCII?  
**R**: **Binary per produzione, ASCII per debug**

```json
{
  "fortran_interface": {
    "input_format": "binary",    // Fast (Week 2+)
    "file_paths": {
      "input_binary": "/tmp/model.bin",
      "input_ascii": "/tmp/model.txt"   // Debug only
    }
  }
}
```

**Binary:**
- ✅ Veloce (no parsing)
- ✅ Compresso
- ❌ Non human-readable

**ASCII:**
- ✅ Human-readable
- ❌ Lento (parsing)
- ✅ Debugging

---

### **Q11: Output Results — Chi Li Riempie?**

**D**: Io specifico output_requests. Chi compila results?  
**R**: **Fortran + Natalia (Backend)**

**Tu scrivi:**
```json
{
  "output_requests": {
    "node_results": {
      "displacements": true,
      "reactions": true
    }
  }
}
```

**Fortran scrive:**
```json
{
  "results": {
    "nodes_results": [
      {
        "node_id": 1,
        "displacements": {"dx": 0.001, "dy": -0.05}
      }
    ]
  }
}
```

---

### **Q12: Validazione — Cosa Controllare?**

**D**: Quando valido il JSON, cosa checko?  
**R**: **Checklist validazione:**

```json
{
  "validation": {
    "error_checks": {
      "duplicate_nodes": false,        // ✅ OK
      "disconnected_elements": false,  // ✅ OK
      "zero_length_elements": false,   // ✅ OK
      "negative_areas": false,         // ✅ OK
      "high_aspect_ratio_elements": false  // ✅ OK
    }
  }
}
```

**Tool Python per validare:**
```python
import json

with open('modello.json') as f:
    data = json.load(f)

# Controlla nodi
assert len(data['geometry']['nodes']) > 0, "No nodes!"

# Controlla elementi
assert len(data['geometry']['elements']) > 0, "No elements!"

# Controlla references
node_ids = {n['id'] for n in data['geometry']['nodes']}
for elem in data['geometry']['elements']:
    for nid in elem['nodes']:
        assert nid in node_ids, f"Element {elem['id']}: node {nid} not found!"

print("✅ JSON valido!")
```

---

### **Q13: Template Library — Quando Usarla?**

**D**: A cosa serve template_library?  
**R**: **Strutture ripetitive pre-fatte**

Esempio: Portale standard 5m × 4m

```json
{
  "template_library": {
    "templates": [
      {
        "id": "portale_5x4",
        "name": "Portale 5×4",
        "type": "frame",
        "parameters": [
          {"name": "span", "default_value": 5.0},
          {"name": "height", "default_value": 4.0}
        ]
      }
    ]
  }
}
```

**Uso in UI (Lucia):**
- User clicca "Portale 5×4"
- UI popola span, height
- User modifica se serve
- ✅ Veloce!

---

### **Q14: Export ModeSt — Come Funziona?**

**D**: Come esportare a ModeSt?  
**R**: **Week 4 (Carla/Daniela)**. Per ora specifica supporto:

```json
{
  "export_import": {
    "supported_formats": [
      {
        "format": "modeest",
        "description": "ModeSt format (bidirectional)",
        "version": "2.x",
        "status": "planned_week4"
      }
    ]
  }
}
```

**Implementazione Week 4:**
- Mapping nodi → ID ModeSt
- Mapping elementi → tipo ModeSt
- Export sezioni, materiali
- Bridge dati unidirezionale (per ora)

---

### **Q15: Damping (Smorzamento) — Come Specifico?**

**D**: Smorzamento per analisi modale?  
**R**: **In modal analysis parameters**

```json
{
  "modal": {
    "enabled": true,
    "damping": {
      "type": "rayleigh",
      "values": [0.02, 0.02]   // α, β Rayleigh
    }
  }
}
```

**Opzioni:**
- `rayleigh`: C = α*M + β*K (più accurato)
- `modal_ratios`: ξ per ogni modo
- `mass_proportional`: Solo α*M
- `stiffness_proportional`: Solo β*K

**Valori tipici:** ξ = 2-5% (0.02-0.05)

---

## ⚠️ COMMON MISTAKES

### **Errore 1: Unità Inconsistenti**

❌ **SBAGLIATO:**
```json
{
  "units": {"length": "m"},
  "nodes": [{"id": 1, "x": 5000, "y": 4000}]  // Millimetri!
}
```

✅ **GIUSTO:**
```json
{
  "units": {"length": "m"},
  "nodes": [{"id": 1, "x": 5.0, "y": 4.0}]  // Metri
}
```

---

### **Errore 2: Elementi Senza Nodi**

❌ **SBAGLIATO:**
```json
{
  "elements": [{"id": 1, "nodes": [1, 99]}]  // Nodo 99 non esiste!
}
```

✅ **GIUSTO:**
```json
{
  "elements": [{"id": 1, "nodes": [1, 2]}]  // Nodi 1,2 definiti
}
```

---

### **Errore 3: P-Delta senza Load Steps**

❌ **SBAGLIATO:**
```json
{
  "nonlinear_p_delta": {
    "enabled": true,
    "load_steps": 1  // Troppo pochi!
  }
}
```

✅ **GIUSTO:**
```json
{
  "nonlinear_p_delta": {
    "enabled": true,
    "load_steps": 5  // Almeno 5 step
  }
}
```

---

### **Errore 4: Carichi Opposti**

❌ **SBAGLIATO:**
```json
{
  "element_loads": [
    {"element_id": 1, "direction": "global_y", "value": 30.0}  // Verso l'alto!
  ]
}
```

✅ **GIUSTO:**
```json
{
  "element_loads": [
    {"element_id": 1, "direction": "global_y", "value": -30.0}  // Verso il basso
  ]
}
```

---

### **Errore 5: Material/Section Non Referenziati**

❌ **SBAGLIATO:**
```json
{
  "materials": [{"id": "steel_S235", ...}],
  "elements": [{"material_id": "STEEL_S235"}]  // Case-sensitive!
}
```

✅ **GIUSTO:**
```json
{
  "materials": [{"id": "steel_S235", ...}],
  "elements": [{"material_id": "steel_S235"}]  // Esatto match
}
```

---

## 📞 ESCALATION FLOWCHART

```
Domanda su schema JSON?
    ↓
1. Leggi questo FAQ
    ↓
2. Guarda ESEMPIO_PORTALE_2D.json
    ↓
3. Leggi GUIDA_SCHEMA_JSON_BENEDETTA.md
    ↓
   Risolto?
    ├─ SÌ → ✅ Procedi
    └─ NO → Chiedi:
        ├─ Tech question → Contatta Natalia (Backend)
        ├─ Fortran format → Contatta Elisa
        ├─ UI rendering → Contatta Irene
        └─ Urgente → Escalate a Alessandra
```

---

## 📋 VALIDATION CHECKLIST

Prima di sottomettere schema:

- [ ] JSON è valido (no syntax errors)
- [ ] Tutti gli elementi referenziano nodi esistenti
- [ ] Tutti gli elementi hanno section_id + material_id validi
- [ ] Load cases hanno senso (gravità verso il basso)
- [ ] Combinazioni hanno fattori NTC 2018
- [ ] Output_requests è coerente con analysis_type
- [ ] Fortran interface paths sono corretti
- [ ] Almeno 1 esempio concreto (portale semplice)

---

## 🎯 DELIVERABLE FINALE

**Venerdì, fine giornata:**

✅ **SCHEMA_DATI_ALESSANDRA.json** (completo, approvato)  
✅ **ESEMPIO_PORTALE_2D.json** (test case)  
✅ **GUIDA_SCHEMA_JSON_BENEDETTA.md** (documentazione)  
✅ **FAQ_SCHEMA_JSON.md** (questo file)  
✅ **API_SPEC_NATALIA.md** (endpoints che Natalia deve buildare)  
✅ **FORTRAN_INPUT_FORMAT.md** (formato binary Elisa)

---

**Benedetta, sei una rock star! 🚀**  
Se hai domande → Slack #progetto-alessandra o chiama direttamente.

_Preparato: 2026-08-18 · Team Architettura_
