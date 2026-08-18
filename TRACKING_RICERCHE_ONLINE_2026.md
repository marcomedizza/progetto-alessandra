# 📱 TRACKING RICERCHE ONLINE — Team Alessandra & Giorgia

**Periodo**: 18 agosto - 29 agosto 2026 (12 giorni)  
**Status**: 🟢 ATTIVO  
**Owner**: Alessandra (Project Lead) + Giorgia (Business Lead)  
**Deadline Giornaliera**: 18:00 ogni giorno

---

## 🎯 OBIETTIVO

Ogni agente documenta **1-2 ore di ricerca online** su tematiche specifiche:
- **Tema tecnico** (architecture, solver, UI/UX, integration)
- **Tema business** (pricing, market, licensing, communication)

Ogni giorno → **1 agente raccoglie report** → **Summary giornaliero**

---

## 📋 TEAM ALESSANDRA (Tech — 12 agenti)

| # | Agente | Specialità | Tema Ricerca | Deadline |
|----|--------|-----------|-------------|----------|
| 1 | **Benedetta** | Architettura | Schema dati, design patterns, FEM standards | 18/08 |
| 2 | **Irene** | Frontend 3D | Three.js, WebGL, UI/UX CAD | 19/08 |
| 3 | **Natalia** | Backend | FastAPI, microservices, Fortran integration | 20/08 |
| 4 | **Elisa** | Fortran Solver | P-Delta, nonlinear analysis, LAPACK | 21/08 |
| 5 | **Francesca** | Ricerca | ModeSt API, OpenFOAM, CFD integration | 22/08 |
| 6 | **Valentina** | QA Testing | Testing frameworks, regression, performance | 23/08 |
| 7 | **Carla** | ModeSt Bridge | ModeSt format, export/import, compatibility | 24/08 |
| 8 | **Daniela** | ModeSt Research | ModeSt solver capabilities, documentation | 25/08 |
| 9 | **Lucia** | UI Editor | React components, property panels, geometry editor | 26/08 |
| 10 | **Mariana** | Results Viz | 3D visualization, diagram rendering, D3/Plotly | 27/08 |
| 11 | **Ottavia** | Build Wrapper | CMake, Fortran compilation, ctypes binding | 28/08 |
| 12 | **Paola** | Data Converter | JSON validation, schema mapping, data pipeline | 29/08 |

---

## 👥 TEAM GIORGIA (Business — 5 agenti)

| # | Agente | Specialità | Tema Ricerca | Deadline |
|----|--------|-----------|-------------|----------|
| 1 | **Aurora** | Offerte & Fatturazione | Pricing models, SaaS, payment tools | 18/08 |
| 2 | **Livia** | Email & Comunicazioni | Email management, customer support, newsletter | 19/08 |
| 3 | **Veronica** | Aggiornamenti Normativi | NTC 2018, licensing, GDPR compliance | 20/08 |
| 4 | **Camilla** | News & Intelligence | Market trends, competitors, tech news | 21/08 |
| 5 | **Laura** | Work Progress Monitor | Project management tools, KPI tracking | 22/08 |

---

## 📅 CALENDARIO RICERCHE

```
SETTIMANA 1 (18-22 agosto)
Mon 18   Tue 19   Wed 20   Thu 21   Fri 22
ALE+BeneD IRE     NAT      ELI      FRA
AUR      LIV      VER      CAM      LAU

SETTIMANA 2 (23-29 agosto)
Sat 23   Sun 24   Mon 25   Tue 26   Wed 27   Thu 28   Fri 29
VALE     CAR      DANI     LUCIA    MARIA    OTTA     PAOLA
```

---

## 📝 TEMPLATE REPORT GIORNALIERO

Ogni agente compila un report così:

```markdown
# 📊 Report Ricerca Online — [NOME AGENTE]

**Data**: 2026-08-18  
**Ricercatore**: Benedetta  
**Tema**: Schema Dati, FEM Standards  
**Durata**: 2 ore  
**Link**: https://claude.ai/code/session_xyz  

## 🔍 Fonti Consultate

1. **FEM Data Standards**
   - https://www.buildingsmart.org/ (IFC standard)
   - https://www.ansys.com/ (APDL format)
   - Wikipedia: Finite Element Method

2. **JSON Schema Patterns**
   - https://json-schema.org/
   - GitHub: json-schema-validator
   - JSON-LD context patterns

3. **Structural Analysis Data Exchange**
   - ModeSt documentation (Tecnisoft)
   - SAFE format (CSI)
   - OpenSees TCL format

## 🎯 Scoperte Principali

### Scoperta 1: IFC 4.0+ Support
- IFC (Industry Foundation Classes) è standard BIM internazionale
- IFC 4.0+ supporta structural geometry + carichi
- **Raccomandazione**: Pianificare IFC import (Week 3+)

### Scoperta 2: JSON Schema Validation
- json-schema.org offre validator open-source
- Puoi validare JSON contro schema TypeScript
- **Raccomandazione**: Integrare validazione in backend

### Scoperta 3: ModeSt Binary Format
- ModeSt usa binary format proprietario (.mst)
- API REST disponibile (non documentata pubblicamente)
- **Raccomandazione**: Contattare Tecnisoft per documentazione

## 💡 Raccomandazioni Azione

- [ ] Integrare json-schema validator in Python backend
- [ ] Pianificare IFC import (Week 3 post-alpha)
- [ ] Contattare Tecnisoft per ModeSt API documentation

## 🔗 Link & Bookmark

- https://json-schema.org/ → JSON schema validation
- https://www.buildingsmart.org/standards/ifc/ → IFC standard
- https://tecnisoft.it/ → ModeSt software

---

**Preparato**: Benedetta (2026-08-18 17:45)  
**Status**: ✅ Completo  
**Next**: Lucia ricerca UI (19 agosto)
```

---

## 📊 REPORT GIORNALIERO AGGREGATO

**Owner**: Alessandra (every 18:00)

```markdown
# 📈 Summary Ricerche Online — 18 agosto 2026

## Team Alessandra
- ✅ **Benedetta**: Schema dati + FEM standards (2h) → 3 scoperte
- ...

## Team Giorgia
- ✅ **Aurora**: Pricing models SaaS (2h) → 5 scoperte
- ...

## 📌 Highlights Today
1. JSON-schema validator disponibile (Benedetta)
2. IFC 4.0+ supporta structural (Benedetta)
3. SaaS pricing models: per-seat vs per-project (Aurora)

## 🔴 Blocchi/Escalate
- Nessuno

## ✅ Completato
- 12 agenti online completato
- 5 agenti business completato

---

**Compilato**: Alessandra (2026-08-18 18:00)
```

---

## 🛠️ PYTHON SCRIPT PER TRACKING

```python
#!/usr/bin/env python3
"""
Tracking sistema ricerche online — Team Alessandra & Giorgia
Raccogli report giornalieri, valida, genera summary
"""

import json
from datetime import datetime
from pathlib import Path

# Database agenti
AGENTS = {
    "alessandra_team": [
        {"name": "Benedetta", "specialty": "Architettura", "date": "2026-08-18"},
        {"name": "Irene", "specialty": "Frontend 3D", "date": "2026-08-19"},
        # ... altri 10
    ],
    "giorgia_team": [
        {"name": "Aurora", "specialty": "Pricing", "date": "2026-08-18"},
        # ... altri 4
    ]
}

class ResearchTracker:
    def __init__(self, base_dir="/home/user/progetto-alessandra"):
        self.base_dir = Path(base_dir)
        self.research_dir = self.base_dir / "RICERCHE_ONLINE"
        self.research_dir.mkdir(exist_ok=True)
        self.reports = []
    
    def validate_report(self, report_json):
        """Valida schema report"""
        required_fields = [
            "agent_name", "date", "theme", "duration_hours",
            "sources", "discoveries", "recommendations"
        ]
        return all(field in report_json for field in required_fields)
    
    def save_report(self, agent_name, report_data):
        """Salva report singolo"""
        date_str = report_data.get("date", datetime.now().strftime("%Y-%m-%d"))
        filename = f"{agent_name}_{date_str}.json"
        filepath = self.research_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"✅ Report salvato: {filename}")
        return filepath
    
    def generate_daily_summary(self, date_str):
        """Genera summary giornaliero"""
        daily_reports = list(self.research_dir.glob(f"*_{date_str}.json"))
        
        summary = {
            "date": date_str,
            "total_reports": len(daily_reports),
            "agents": [],
            "highlights": [],
            "blockers": []
        }
        
        for report_file in daily_reports:
            with open(report_file) as f:
                report = json.load(f)
            
            summary["agents"].append({
                "name": report.get("agent_name"),
                "sources_count": len(report.get("sources", [])),
                "discoveries_count": len(report.get("discoveries", []))
            })
        
        return summary
    
    def generate_master_report(self):
        """Genera report master (18-29 agosto)"""
        all_reports = list(self.research_dir.glob("*.json"))
        
        master = {
            "period": "2026-08-18 to 2026-08-29",
            "total_days": 12,
            "total_agents": 17,
            "reports_collected": len(all_reports),
            "completion_rate": f"{(len(all_reports)/17)*100:.1f}%",
            "summary_by_team": {
                "alessandra": {},
                "giorgia": {}
            }
        }
        
        return master

# Uso
if __name__ == "__main__":
    tracker = ResearchTracker()
    
    # Esempio: salva report Benedetta
    benedetta_report = {
        "agent_name": "Benedetta",
        "date": "2026-08-18",
        "theme": "Schema Dati, FEM Standards",
        "duration_hours": 2,
        "sources": [
            "https://json-schema.org/",
            "https://www.buildingsmart.org/",
            "https://www.ansys.com/"
        ],
        "discoveries": [
            "IFC 4.0+ supporta structural geometry",
            "JSON-schema validator disponibile",
            "ModeSt usa binary format proprietario"
        ],
        "recommendations": [
            "Integrare json-schema validator",
            "Pianificare IFC import Week 3+",
            "Contattare Tecnisoft per API docs"
        ]
    }
    
    tracker.save_report("Benedetta", benedetta_report)
    
    # Genera summary giornaliero
    daily = tracker.generate_daily_summary("2026-08-18")
    print(json.dumps(daily, indent=2))
```

---

## 📁 STRUTTURA CARTELLE

```
/home/user/progetto-alessandra/
├── RICERCHE_ONLINE/
│   ├── 2026-08-18/
│   │   ├── Benedetta_2026-08-18.md
│   │   ├── Aurora_2026-08-18.md
│   │   └── SUMMARY_2026-08-18.md
│   ├── 2026-08-19/
│   │   ├── Irene_2026-08-19.md
│   │   ├── Livia_2026-08-19.md
│   │   └── SUMMARY_2026-08-19.md
│   └── ...
│   └── MASTER_REPORT_2026-08-29.md
```

---

## ✅ CHECKLIST GIORNALIERO

**Ogni agente (entro 18:00):**
- [ ] Dedica 1-2 ore ricerca online
- [ ] Compila report template
- [ ] Carica in RICERCHE_ONLINE/[DATA]/
- [ ] Notifica Alessandra/Giorgia via Slack

**Alessandra (ore 18:00):**
- [ ] Raccoglie tutti report del giorno
- [ ] Genera summary
- [ ] Posta #progetto-alessandra
- [ ] Escalate blockers se ci sono

**Giorgia (ore 18:00 team business):**
- [ ] Raccogli report team business (Aurora, Livia, Veronica, Camilla, Laura)
- [ ] Aggrega in BUSINESS_SUMMARY

---

## 🎯 EXPECTED OUTPUT (29 agosto EOD)

✅ **17 report individuali** (1 per agente × 12 giorni)  
✅ **12 summary giornalieri** (uno per giorno)  
✅ **1 master report** (sintesi 12 giorni)  
✅ **Documentazione ricerca** (fonti, bookmark, guidelines)  
✅ **Raccomandazioni** (basate su scoperte online)

**Totale ore ricerca**: ~34 ore (2h × 17 agenti)

---

## 📞 ESCALATION

**Blocchi/Dubbi?**
- **Tech**: Contatta Alessandra
- **Business**: Contatta Giorgia
- **Tool issues**: Contatta Natalia (backend)

---

**Ricorda**: Ricerca online è **fondamentale** per Week 1 decisions.  
**Fai il tuo meglio** → domani partiamo forti! 💪

_Sistema tracking: 2026-08-18 · Alessandra (Project Lead)_
