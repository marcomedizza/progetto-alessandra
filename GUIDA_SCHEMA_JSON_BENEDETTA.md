# 📋 GUIDA SCHEMA JSON ALESSANDRA — Per Benedetta

**Documento**: SCHEMA_DATI_ALESSANDRA.json  
**Data**: 2026-08-18  
**Autore**: Benedetta (Architettura Team)  
**Status**: DRAFT v1 — Pronto per Review Giovedì  
**Scadenza Finalizzazione**: Venerdì 2026-08-20

---

## 📌 QUICK START — COSA DEVI FARE OGGI

### **OGGI (Mercoledì 18 agosto)**
1. ✅ **Leggi lo schema** (30 min) — capire la struttura
2. ✅ **Riempi esempio pratico** (1 ora) — un semplice portale 2D
3. ✅ **Valida con team**:
   - **Natalia** (Backend): API endpoints da schema
   - **Elisa** (Fortran): Fortran input/output format

### **GIOVEDÌ 19 agosto**
- Raccogli feedback
- Finalizza schema
- Approva con Alessandra

### **VENERDÌ 20 agosto**
- Pronto per developer!

---

## 🏗️ STRUTTURA SCHEMA — OVERVIEW

```
metadata              ← Info progetto
project               ← Units, analysis type, nonlinearità
geometry              ← Nodi + elementi
materials             ← Proprietà materiali
sections              ← Sezioni trasversali (I, rettangolare, etc.)
loads                 ← Carichi + combinazioni
solver_parameters     ← Statica, modale, P-Delta, etc.
output_requests       ← Cosa vuoi in output
results               ← Risultati da Fortran
visualization         ← Deformate, diagrammi, animazioni
fortran_interface     ← Come comunica con Fortran
validation            ← Controlli su modello
template_library      ← Template ripetitivi
export_import         ← DXF, IFC, ModeSt, etc.
```

---

## 📖 SEZIONE PER SEZIONE

### **1. METADATA**
```json
{
  "metadata": {
    "schema_version": "2.0",
    "created_date": "2026-08-18",
    "author": "Benedetta",
    "status": "DRAFT_v1"
  }
}
```
💡 **Uso**: Versionamento schema. Se cambiamo struttura, incremen ta version.

---

### **2. PROJECT**

```json
{
  "project": {
    "id": "prj_202608_portale_semplice",
    "name": "Portale 2D Semplice",
    "units": {
      "length": "m",
      "force": "kN",
      "stress": "MPa"
    },
    "analysis_type": "static",
    "nonlinearity_options": {
      "p_delta": true,
      "plasticity": false
    }
  }
}
```

**Cosa inserire:**
- `units`: Sempre specificare (fondamentale!)
- `analysis_type`: `static` (Week 2), `modal` (Week 3)
- `nonlinearity_options`: Cosa attiva (P-Delta sì, plasticity no per Week 1)

💡 **Per Team**: Questo dice a Natalia quale API configurare, a Elisa quale Fortran compilare.

---

### **3. GEOMETRY (Nodi + Elementi)**

**NODI:**
```json
{
  "geometry": {
    "nodes": [
      {
        "id": 1,
        "x": 0.0,
        "y": 0.0,
        "z": 0.0,
        "restraints": {
          "dx": "fixed",
          "dy": "fixed",
          "rz": "fixed"
        }
      },
      {
        "id": 2,
        "x": 5.0,
        "y": 0.0,
        "z": 0.0,
        "restraints": {
          "dx": "free",
          "dy": "fixed",
          "rz": "free"
        }
      }
    ]
  }
}
```

**ELEMENTI:**
```json
{
  "elements": [
    {
      "id": 1,
      "type": "frame_2d",
      "nodes": [1, 2],
      "section_id": "HEA200",
      "material_id": "steel_S235",
      "orientation": {
        "angle_z": 0.0
      },
      "properties": {
        "releases": {
          "start": {"Mz": "fixed"},
          "end": {"Mz": "free"}
        }
      }
    }
  ]
}
```

💡 **Cosa significa:**
- `type`: `beam_2d`, `frame_2d`, `truss_2d` (Week 1-2)
- `restraints`: Vincoli ai nodi (fissi, liberi, molle)
- `releases`: Rilasci alle estremità (per incastri parziali)
- `orientation`: Angoli locali per sezioni (importante!)

---

### **4. MATERIALS (Proprietà Materiali)**

```json
{
  "materials": [
    {
      "id": "steel_S235",
      "name": "Acciaio S235",
      "type": "steel",
      "properties": {
        "elastic_modulus": 210000e6,
        "shear_modulus": 81000e6,
        "density": 7850,
        "poisson_ratio": 0.3,
        "yield_stress": 235e6
      },
      "nonlinear": {
        "plasticity_model": "perfect_plastic"
      }
    }
  ]
}
```

💡 **Valori standard (hardcoded in database):**
- **Steel S235**: E=210 GPa, fy=235 MPa
- **Concrete C30**: E=33 GPa, fc=30 MPa
- **Aluminio**: E=70 GPa

---

### **5. SECTIONS (Sezioni Trasversali)**

```json
{
  "sections": [
    {
      "id": "HEA200",
      "name": "HEA 200 mm",
      "type": "i_beam",
      "geometry": {
        "b": 0.20,
        "h": 0.19,
        "t": 0.008
      },
      "properties": {
        "area": 0.005380,
        "inertia_y": 0.0000000000000,
        "inertia_z": 0.0000000000000
      },
      "computed": false
    }
  ]
}
```

💡 **Opzioni:**
- `computed: true` → Auto-calcola area/inerzie da geometria
- `computed: false` → Usa valori specificati (database HEA/HEB/IPE)

---

### **6. LOADS (Carichi)**

```json
{
  "loads": {
    "load_cases": [
      {
        "id": "dead",
        "name": "Peso Proprio",
        "type": "dead",
        "self_weight": true
      },
      {
        "id": "live",
        "name": "Carico Utile Solaio",
        "type": "live",
        "node_loads": [
          {
            "node_id": 2,
            "fx": 0.0,
            "fy": -50.0,
            "fz": 0.0
          }
        ]
      },
      {
        "id": "snow",
        "name": "Neve",
        "type": "live",
        "element_loads": [
          {
            "element_id": 1,
            "type": "distributed",
            "direction": "global_y",
            "value": -5.0
          }
        ]
      }
    ],
    "load_combinations": [
      {
        "id": "comb_SLU",
        "name": "Combinazione SLU",
        "cases": [
          {"case_id": "dead", "factor": 1.35},
          {"case_id": "live", "factor": 1.5}
        ]
      }
    ]
  }
}
```

💡 **Tipi di carico:**
- `node_loads`: Forze puntuali ai nodi
- `element_loads`: Distributed, concentrato, temperatura
- `self_weight`: Auto-calcola da massa + gravità

---

### **7. SOLVER_PARAMETERS (Opzioni Solver)**

**Per Static:**
```json
{
  "solver_parameters": {
    "static": {
      "method": "nonlinear",
      "nonlinear_p_delta": {
        "enabled": true,
        "max_iterations": 20,
        "tolerance": 1e-6,
        "load_steps": 5
      }
    }
  }
}
```

**Per Modal:**
```json
{
  "modal": {
    "enabled": true,
    "method": "lanczos",
    "num_modes": 10,
    "damping": {
      "type": "rayleigh",
      "values": [0.02, 0.02]
    }
  }
}
```

💡 **Week 2 vs Week 3:**
- **Week 2**: Static + P-Delta
- **Week 3**: Aggiungi Modal (num_modes=10-20)

---

### **8. OUTPUT_REQUESTS (Cosa Vogliamo In Output)**

```json
{
  "output_requests": {
    "node_results": {
      "displacements": true,
      "reactions": true
    },
    "element_results": {
      "internal_forces": true,
      "stresses": true,
      "stress_resultants": ["Nx", "Vy", "Mz"]
    },
    "modal_results": {
      "frequencies": true,
      "mode_shapes": true
    }
  }
}
```

💡 **Output format**: JSON (per API), binary (per performance Fortran)

---

### **9. RESULTS (Output da Fortran)**

Questa sezione **VIENE RIEMPITA DA FORTRAN**, non dall'utente.

```json
{
  "results": {
    "status": "completed",
    "nodes_results": [
      {
        "node_id": 2,
        "displacements": {"dx": 0.0, "dy": -0.05, "dz": 0.0},
        "reactions": {"fx": 0.0, "fy": 50.0, "fz": 0.0}
      }
    ],
    "element_results": [
      {
        "element_id": 1,
        "internal_forces": {"N": 0.0, "Vy": 50.0, "Mz": 125.0}
      }
    ]
  }
}
```

---

### **10. VISUALIZATION (Deformate, Diagrammi, Animazioni)**

```json
{
  "visualization": {
    "deformed_shape": {
      "scale_factor": 50,
      "show_undeformed": true,
      "show_reactions": true
    },
    "diagrams": {
      "axial_force": true,
      "shear_force_y": true,
      "bending_moment_z": true
    },
    "animation": {
      "mode_animation": true,
      "num_frames": 30
    }
  }
}
```

💡 **Per Irene (Frontend)**: Dice quali diagrammi disegnare in 3D

---

### **11. FORTRAN_INTERFACE (Come Parla con Fortran)**

```json
{
  "fortran_interface": {
    "input_format": "binary",
    "binary_precision": "double",
    "file_paths": {
      "input_binary": "/tmp/model.bin",
      "output_binary": "/tmp/results.bin"
    },
    "solver_command": "./solver --input /tmp/model.bin --output /tmp/results.bin"
  }
}
```

💡 **Per Natalia (Backend)**: Come lanciare Fortran e passare dati

---

### **12. TEMPLATE_LIBRARY (Strutture Ripetitive)**

```json
{
  "template_library": {
    "templates": [
      {
        "id": "simple_frame_2d",
        "name": "Portale Semplice 2D",
        "type": "frame",
        "parameters": [
          {"name": "span", "type": "length", "default_value": 5.0},
          {"name": "height", "type": "length", "default_value": 3.0},
          {"name": "num_bays", "type": "count", "default_value": 1}
        ]
      }
    ]
  }
}
```

💡 **Per Lucia (UI Editor)**: Template da cui partire (velocizza disegno)

---

### **13. EXPORT_IMPORT (Interoperabilità)**

```json
{
  "export_import": {
    "supported_formats": [
      "dxf",    // AutoCAD
      "ifc",    // BIM
      "modeest" // Bidirectional
    ]
  }
}
```

💡 **Week 4**: ModeSt export (Carla + Daniela)

---

## 🔄 FLUSSO DATI TIPICO

```
[UI 3D Irene]
      ↓
   JSON
      ↓
[Backend Natalia] → Converte JSON → Binary Fortran
      ↓
[Fortran Elisa] → Risolve → Output binary
      ↓
[Backend Natalia] → Converte binary → JSON
      ↓
[Risultati UI Irene] → Disegna deformate, diagrammi
```

---

## ✅ CHECKLIST FINALIZZAZIONE SCHEMA

**Entro Giovedì mattina (2026-08-19):**

- [ ] **Leggi e comprendi** lo schema JSON
- [ ] **Riempi esempio:** Portale 2D semplice (3 nodi, 2 elementi)
- [ ] **Valida con Natalia**:
  - [ ] API endpoints necessari
  - [ ] Come Natalia legge input JSON
  - [ ] Come Natalia scrive output JSON
- [ ] **Valida con Elisa**:
  - [ ] Come Elisa riceve dati (binary format)
  - [ ] Quali campi sono obbligatori
  - [ ] Fortran output structure
- [ ] **Risolvi ambiguità**:
  - [ ] Coordinate sistema? (globale per tutto)
  - [ ] Segno carichi? (positivo = verso alto)
  - [ ] Ordine nodi elemento? (Inizio → Fine)

**Giovedì review:**
- [ ] Alessandra approva architettura
- [ ] Natalia approva API contracts
- [ ] Elisa approva Fortran I/O

**Venerdì:**
- [ ] Schema finalizzato
- [ ] Developers possono iniziare!

---

## 🛠️ STRUMENTI PER VALIDARE JSON

**Online validator:**
```
https://jsonlint.com/
```

**Python (locale):**
```python
import json
with open('SCHEMA_DATI_ALESSANDRA.json') as f:
    data = json.load(f)
print("✅ JSON valido!")
```

---

## 📞 CHECKLIST REVIEW GIOVEDÌ

**Con ALESSANDRA:**
- [ ] "Questo schema copre tutti i nostri requisiti?"
- [ ] "Ho dimenticato qualcosa?"

**Con NATALIA (Backend):**
- [ ] "Puoi leggere questo JSON facilmente?"
- [ ] "API dovranno supportare X/Y/Z?"

**Con ELISA (Fortran):**
- [ ] "Formato input binary va bene?"
- [ ] "Output results structure è chiaro?"

---

## 🎯 RISULTATO ATTESO VENERDÌ

✅ **Schema JSON FINALIZZATO** con:
- Tutti i campi necessari documentati
- Esempi reali (portale 2D)
- Approvazione Alessandra + Natalia + Elisa
- Pronto per developer Week 2

---

## 📚 RIFERIMENTI

- `README.md` — Roadmap progetto
- `KICK-OFF_CHECKLIST.md` — Timeline Week 1
- `SCHEMA_DATI_ALESSANDRA.json` — Schema completo
- `ORGANIGRAMMA_TEAM.md` — Chi contattare

---

**Benedetta, sei tu la regina di questa settimana!** 👑  
Se hai domande → chiedi subito → non aspettare.

_Preparato: 2026-08-18 · Team Architettura_
