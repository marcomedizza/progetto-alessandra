# 📝 GUIDA — Trasformazione TESTO → JSON

**Autore:** Claude  
**Data:** 29 agosto 2026  
**Scopo:** Spiegazione pratica su come convertire documenti testuali in JSON strutturato

---

## 🎯 CONCETTO BASE

**Testo → JSON** significa prendere informazioni **non strutturate** (paragrafi, elenchi, tabelle) e convertirle in **struttura JSON rigida** (campi, tipi di dati, validazione).

### Perché?

| Testo | JSON |
|-------|------|
| Leggibile umano | Leggibile macchina |
| Unstructured | Structured |
| Facile da scrivere | Facile da validare |
| Difficile da parsare | Facile da parsare (API) |

---

## 📚 ESEMPIO PRATICO #1 — ORGANIGRAMMA

### **PRIMA: Testo (ORGANIGRAMMA_TEAM.md)**

```markdown
# ORGANIGRAMMA PROGETTO ALESSANDRA

## TEAM ALESSANDRA (19 agenti)

### Tech Core (12 agenti)
- Benedetta — Architettura, Schema JSON
- Irene — Frontend 3D, Three.js
- Natalia — Backend, FastAPI
- Elisa — Fortran Solver, P-Delta

### Strutturale (7 agenti)
- Roberta — Calcestruzzo Armato
- Martina — Acciaio Strutturale
```

### **DOPO: JSON Strutturato**

```json
{
  "project": {
    "name": "Progetto Alessandra",
    "totalAgents": 24,
    "teams": [
      {
        "id": "team_alessandra",
        "name": "Team Alessandra",
        "type": "primary",
        "totalAgents": 19,
        "subteams": [
          {
            "id": "tech_core",
            "name": "Tech Core",
            "description": "Team tecnico principale",
            "agents": [
              {
                "id": "benedetta_001",
                "name": "Benedetta",
                "role": "Architettura",
                "skills": ["Architettura", "Schema JSON"],
                "team": "tech_core"
              },
              {
                "id": "irene_001",
                "name": "Irene",
                "role": "Frontend 3D",
                "skills": ["Frontend 3D", "Three.js"],
                "team": "tech_core"
              },
              {
                "id": "natalia_001",
                "name": "Natalia",
                "role": "Backend",
                "skills": ["Backend", "FastAPI"],
                "team": "tech_core"
              },
              {
                "id": "elisa_001",
                "name": "Elisa",
                "role": "Fortran Solver",
                "skills": ["Fortran", "P-Delta"],
                "team": "tech_core"
              }
            ],
            "totalAgents": 4
          },
          {
            "id": "strutturale",
            "name": "Strutturale",
            "description": "Team strutturale specializzato",
            "agents": [
              {
                "id": "roberta_001",
                "name": "Roberta",
                "role": "Calcestruzzo Armato",
                "skills": ["Calcestruzzo Armato", "Analisi Strutturale"],
                "team": "strutturale"
              },
              {
                "id": "martina_001",
                "name": "Martina",
                "role": "Acciaio Strutturale",
                "skills": ["Acciaio", "Dimensionamento"],
                "team": "strutturale"
              }
            ],
            "totalAgents": 2
          }
        ]
      }
    ]
  }
}
```

### **CHE È ACCADUTO?**

1. ✅ **Titoli** → `"name"`, `"id"` (campi JSON)
2. ✅ **Elenchi puntati** → `[array]` (liste JSON)
3. ✅ **Testo descrittivo** → `"description"`, `"role"` (string values)
4. ✅ **Struttura gerarchica** → `nested objects` (relazioni parent-child)
5. ✅ **Aggiunti IDs** → `"id"` unique identifiers (per database)

---

## 📚 ESEMPIO PRATICO #2 — MANDATO RICERCHE

### **PRIMA: Testo Non Strutturato**

```markdown
# MANDATO RICERCHE ONLINE

Periodo: 18 agosto - 5 settembre 2026 (19 giorni)
Status: OBBLIGATORIO

COSA SIGNIFICA "ANDARE ONLINE"

1. Minimo 2 ore di ricerca CONTINUATIVA
   - Accedi a computer/internet
   - Apri browser
   - Consulta 3-5 siti autorevoli su TUO tema

2. Compila report markdown (30 min max)
   - Sintetizza scoperte in report
   - Includi minimo 3 fonti

CALENDARIO OBBLIGATORIO

SETTIMANA 1 (18-22 agosto)
- 18 (LUN) → Benedetta + Aurora
- 19 (MAR) → Irene + Livia
```

### **DOPO: JSON Strutturato**

```json
{
  "mandate": {
    "id": "ricerche_online_2026",
    "title": "Mandato Ricerche Online",
    "status": "obbligatorio",
    "period": {
      "start": "2026-08-18",
      "end": "2026-09-05",
      "totalDays": 19
    },
    "requirements": [
      {
        "step": 1,
        "title": "Ricerca Continuativa",
        "duration": {
          "value": 2,
          "unit": "hours"
        },
        "description": "Minimo 2 ore di ricerca",
        "tasks": [
          "Accedi a computer/internet",
          "Apri browser",
          "Consulta 3-5 siti autorevoli su TUO tema"
        ]
      },
      {
        "step": 2,
        "title": "Compilazione Report",
        "duration": {
          "value": 30,
          "unit": "minutes"
        },
        "description": "Compila report markdown",
        "minimumRequirements": {
          "sources": 3,
          "keyDiscoveries": 3,
          "recommendations": 2
        }
      }
    ],
    "schedule": [
      {
        "week": 1,
        "period": "18-22 agosto",
        "days": [
          {
            "date": "2026-08-18",
            "dayOfWeek": "lunedì",
            "agents": ["Benedetta", "Aurora"]
          },
          {
            "date": "2026-08-19",
            "dayOfWeek": "martedì",
            "agents": ["Irene", "Livia"]
          }
        ]
      }
    ]
  }
}
```

### **TRASFORMAZIONI APPLICATE:**

1. ✅ **Date testuali** ("18 agosto 2026") → **Date ISO** (`"2026-08-18"`)
2. ✅ **Durate** ("2 ore") → **Oggetti strutturati** (`{"value": 2, "unit": "hours"}`)
3. ✅ **Liste non numerate** → **Array numerato** (`"tasks": [...]`)
4. ✅ **Requisiti impliciti** → **Campi espliciti** (`"minimumRequirements"`)
5. ✅ **Testo libero** → **Campi categorizzati** (`"week"`, `"dayOfWeek"`, `"agents"`)

---

## 🔑 PRINCIPI DI TRASFORMAZIONE

### **1. IDENTIFICARE LA STRUTTURA**

Guardare il testo e identificare:
- **Gerarchie** (parent-child)
- **Ripetizioni** (liste, array)
- **Categorie** (raggruppamenti)
- **Attributi** (proprietà di un oggetto)

### **2. DEFINIRE SCHEMA JSON**

```json
{
  "object_type": {
    "id": "unique_identifier",
    "name": "string",
    "property1": "value_type",
    "property2": {
      "subproperty": "value_type"
    },
    "array_property": [
      {
        "item": "value"
      }
    ]
  }
}
```

### **3. NORMALIZZARE DATI**

Convertire formati:
- Testo date → ISO 8601 (`YYYY-MM-DD`)
- Numeri con unità → `{value, unit}`
- Booleani testuali → `true/false`
- Enumerazioni → select from predefined list

### **4. AGGIUNGERE METADATA**

```json
{
  "metadata": {
    "version": "1.0",
    "createdDate": "2026-08-29",
    "updatedDate": "2026-08-29",
    "author": "Alessandra",
    "description": "Schema per..."
  },
  "data": {
    ...
  }
}
```

---

## 💾 SCHEMA DATI ALESSANDRA — ANALISI

### **COSA È (ATTUALMENTE)?**

Il file `SCHEMA_DATI_ALESSANDRA.json` è un **Template Schema** (type definitions), non dati effettivi:

```json
{
  "geometry": {
    "nodes": [
      {
        "id": "integer",      ← Tipo, non valore
        "x": "float",         ← Tipo, non valore
        "y": "float"          ← Tipo, non valore
      }
    ]
  }
}
```

### **COME TRASFORMARLO IN DATI REALI?**

Popolare con valori effettivi:

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
          "dz": "fixed"
        }
      },
      {
        "id": 2,
        "x": 5.0,
        "y": 0.0,
        "z": 0.0,
        "restraints": {
          "dx": "free",
          "dy": "free",
          "dz": "free"
        }
      }
    ]
  }
}
```

---

## 🛠️ STRUMENTI PER LA TRASFORMAZIONE

### **1. Manuale (Python/JavaScript)**

```python
import json
import yaml

# Leggere YAML/testo
with open("mandato.md", "r") as f:
    content = f.read()

# Parsare (manuale o regex)
data = {
    "title": extract_title(content),
    "period": extract_period(content),
    "requirements": extract_requirements(content)
}

# Scrivere JSON
with open("mandato.json", "w") as f:
    json.dump(data, f, indent=2)
```

### **2. AI (Claude API)**

```python
from anthropic import Anthropic

client = Anthropic()
conversation_history = []

# Passo 1: Carica documento
document = open("mandato.md").read()
conversation_history.append({
    "role": "user",
    "content": f"Converti questo documento in JSON strutturato:\n\n{document}"
})

response = client.messages.create(
    model="claude-opus-5",
    max_tokens=2000,
    messages=conversation_history
)

json_output = response.content[0].text
conversation_history.append({
    "role": "assistant",
    "content": json_output
})

# Passo 2: Refina schema
conversation_history.append({
    "role": "user",
    "content": "Aggiungi campo 'id' a ogni oggetto e valida il JSON"
})

refined = client.messages.create(
    model="claude-opus-5",
    max_tokens=2000,
    messages=conversation_history
)

print(refined.content[0].text)
```

### **3. Tools Online**

- JSON Schema Validator: https://www.jsonschemavalidator.net/
- YAML to JSON: https://www.convertjson.com/yaml-to-json.html
- JSON Formatter: https://jsonformatter.org/

---

## ✅ CHECKLIST TRASFORMAZIONE

Quando converti testo in JSON, verifica:

- [ ] **Structure**: Nessun livello di nesting confuso
- [ ] **IDs**: Ogni oggetto ha `"id"` unico
- [ ] **Types**: Tipi di dati coerenti (string, number, boolean, array, object)
- [ ] **Dates**: Formato ISO 8601 (`YYYY-MM-DD`)
- [ ] **Validation**: Schema JSON valido (testa con validator)
- [ ] **Metadata**: Versione, autore, data creazione
- [ ] **Completeness**: Nessun dato perso dalla conversione
- [ ] **Readability**: Indentazione corretta (2-4 spazi)

---

## 📊 ESEMPIO COMPLETO — Da Testo a JSON Strutturato

### **INPUT: Documento Testo (RIEPILOGO_WEEK1_SETUP.md)**

```
# RIEPILOGO WEEK 1 SETUP

Status: PRONTO PER TEAM
Agenti: 24 totali (Tech 12, Strutturale 7, Business 5)

## DELIVERABLE COMPLETATI

### Schema JSON
✅ SCHEMA_DATI_ALESSANDRA.json (completo)
✅ GUIDA_SCHEMA_JSON_BENEDETTA.md (step-by-step)

### Ricerche Online
✅ 24 AGENTI IN TOTALE
Periodo: 18 agosto - 5 settembre 2026
Deadline: 18:00 (NON NEGOZIABILE)
```

### **PROCESSO DI TRASFORMAZIONE**

**Passo 1: Identifica sezioni**
```
Livello 1: Title → metadata.title
Livello 2: Status → metadata.status
Livello 2: Agenti → project.agents
Livello 3: Deliverable → deliverables array
Livello 4: Schema JSON → deliverable item
```

**Passo 2: Normalizza dati**
```
"24 agenti" → agents: {total: 24, breakdown: {...}}
"18 agosto - 5 settembre" → period: {start: "2026-08-18", end: "2026-09-05"}
"18:00 NON NEGOZIABILE" → deadline: {time: "18:00", negotiable: false}
```

**Passo 3: Crea schema**

### **OUTPUT: JSON Strutturato**

```json
{
  "metadata": {
    "version": "1.0",
    "title": "Riepilogo Week 1 Setup",
    "status": "pronto_per_team",
    "createdDate": "2026-08-21",
    "totalAgents": 24,
    "breakdown": {
      "tech": 12,
      "strutturale": 7,
      "business": 5
    }
  },
  "deliverables": [
    {
      "id": "schema_json",
      "name": "Schema JSON",
      "category": "Architettura",
      "items": [
        {
          "file": "SCHEMA_DATI_ALESSANDRA.json",
          "status": "completo",
          "description": "Schema dati universale"
        },
        {
          "file": "GUIDA_SCHEMA_JSON_BENEDETTA.md",
          "status": "completo",
          "description": "Guida step-by-step"
        }
      ]
    },
    {
      "id": "ricerche_online",
      "name": "Ricerche Online",
      "category": "Research",
      "agents": 24,
      "period": {
        "start": "2026-08-18",
        "end": "2026-09-05",
        "totalDays": 19
      },
      "requirements": {
        "dailyDeadline": "18:00",
        "negotiable": false,
        "minimumHours": 2
      }
    }
  ]
}
```

---

## 🎯 RIASSUNTO

| Aspetto | Testo | JSON |
|---------|-------|------|
| **Formato** | Paragraft, elenchi | Campi, array, nesting |
| **Parsing** | Visivo (umano) | Programmato (macchina) |
| **Validazione** | Difficile | Schema validator |
| **API Ready** | No | Sì |
| **Database Ready** | No | Sì |
| **Queryable** | No | Sì (JQ, SQL, ecc) |

**La trasformazione testo → JSON rende i dati:**
- ✅ Machina-readable
- ✅ Validabili
- ✅ Queryabili
- ✅ API-ready
- ✅ Database-ready

---

**Fatto!** Questa è la guida completa sulla trasformazione testo → JSON con esempi dai tuoi file del Drive. 📋
