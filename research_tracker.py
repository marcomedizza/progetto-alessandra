#!/usr/bin/env python3
"""
📱 Research Tracker — Team Alessandra & Giorgia
Gestisce ricerche online, raccoglie report, genera summary
Basato su schema telaio per validazione dati
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# ============================================================================
# SCHEMA TELAIO PER VALIDAZIONE REPORT
# ============================================================================

REPORT_SCHEMA = {
    "agent_name": str,
    "team": str,  # "alessandra" or "giorgia"
    "date": str,  # "2026-08-18"
    "theme": str,  # Area di ricerca
    "duration_hours": float,
    "sources": list,  # URL consultati
    "discoveries": list,  # Scoperte chiave
    "recommendations": list,  # Azioni raccomandate
    "status": str,  # "completed" or "in_progress"
}

AGENT_DATABASE = {
    "alessandra_team": [
        {"name": "Benedetta", "specialty": "Architettura", "date": "2026-08-18"},
        {"name": "Irene", "specialty": "Frontend 3D", "date": "2026-08-19"},
        {"name": "Natalia", "specialty": "Backend", "date": "2026-08-20"},
        {"name": "Elisa", "specialty": "Fortran Solver", "date": "2026-08-21"},
        {"name": "Francesca", "specialty": "Ricerca CFD", "date": "2026-08-22"},
        {"name": "Valentina", "specialty": "QA Testing", "date": "2026-08-23"},
        {"name": "Carla", "specialty": "ModeSt Bridge", "date": "2026-08-24"},
        {"name": "Daniela", "specialty": "ModeSt Research", "date": "2026-08-25"},
        {"name": "Lucia", "specialty": "UI Editor", "date": "2026-08-26"},
        {"name": "Mariana", "specialty": "Results Viz", "date": "2026-08-27"},
        {"name": "Ottavia", "specialty": "Build Wrapper", "date": "2026-08-28"},
        {"name": "Paola", "specialty": "Data Converter", "date": "2026-08-29"},
    ],
    "giorgia_team": [
        {"name": "Aurora", "specialty": "Pricing & Fatturazione", "date": "2026-08-18"},
        {"name": "Livia", "specialty": "Email & Comunicazioni", "date": "2026-08-19"},
        {"name": "Veronica", "specialty": "Aggiornamenti Normativi", "date": "2026-08-20"},
        {"name": "Camilla", "specialty": "News & Intelligence", "date": "2026-08-21"},
        {"name": "Laura", "specialty": "Work Progress Monitor", "date": "2026-08-22"},
    ],
}


class ResearchTracker:
    """Gestisce tracking ricerche online con validazione schema"""

    def __init__(self, base_dir: Path = None):
        self.base_dir = base_dir or Path("/home/user/progetto-alessandra")
        self.research_dir = self.base_dir / "RICERCHE_ONLINE"
        self.research_dir.mkdir(exist_ok=True)
        self.reports = []

    def validate_report(self, report: Dict) -> tuple[bool, str]:
        """
        Valida report contro schema telaio

        Returns:
            (is_valid, error_message)
        """
        # Controlla campi obbligatori
        for field, field_type in REPORT_SCHEMA.items():
            if field not in report:
                return False, f"Campo obbligatorio mancante: {field}"

            if not isinstance(report[field], field_type):
                return False, f"Tipo errato per {field}: atteso {field_type.__name__}"

        # Controlla formato data
        try:
            datetime.strptime(report["date"], "%Y-%m-%d")
        except ValueError:
            return False, "Data deve essere formato YYYY-MM-DD"

        # Controlla team valido
        if report["team"] not in ["alessandra", "giorgia"]:
            return False, "Team deve essere 'alessandra' o 'giorgia'"

        # Controlla durata ragionevole
        if not 0.5 <= report["duration_hours"] <= 8:
            return False, "Durata deve essere tra 0.5 e 8 ore"

        # Controlla almeno 2 source + 2 scoperte
        if len(report["sources"]) < 2:
            return False, "Minimo 2 fonte richieste"

        if len(report["discoveries"]) < 2:
            return False, "Minimo 2 scoperte richieste"

        # Controlla status valido
        if report["status"] not in ["completed", "in_progress"]:
            return False, "Status deve essere 'completed' o 'in_progress'"

        return True, "✅ Valido"

    def save_report(self, report: Dict) -> bool:
        """Salva report singolo"""
        # Valida
        is_valid, msg = self.validate_report(report)
        if not is_valid:
            print(f"❌ Errore validazione: {msg}")
            return False

        # Crea cartella per data
        date_dir = self.research_dir / report["date"]
        date_dir.mkdir(exist_ok=True)

        # Salva JSON
        filename = f"{report['agent_name']}_{report['date']}.json"
        filepath = date_dir / filename

        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)

        print(f"✅ Report salvato: {filename}")
        self.reports.append(report)
        return True

    def load_report(self, filepath: Path) -> Optional[Dict]:
        """Carica report da file"""
        try:
            with open(filepath) as f:
                return json.load(f)
        except Exception as e:
            print(f"❌ Errore lettura {filepath}: {e}")
            return None

    def generate_daily_summary(self, date_str: str) -> Dict:
        """Genera summary giornaliero"""
        date_dir = self.research_dir / date_str

        if not date_dir.exists():
            print(f"⚠️  Nessun report per {date_str}")
            return {}

        reports = []
        for report_file in date_dir.glob("*.json"):
            if report_file.name != f"SUMMARY_{date_str}.json":
                report = self.load_report(report_file)
                if report:
                    reports.append(report)

        # Conta scoperte
        total_discoveries = sum(len(r.get("discoveries", [])) for r in reports)
        total_recommendations = sum(len(r.get("recommendations", [])) for r in reports)

        summary = {
            "date": date_str,
            "total_reports": len(reports),
            "total_discoveries": total_discoveries,
            "total_recommendations": total_recommendations,
            "agents": [
                {
                    "name": r.get("agent_name"),
                    "team": r.get("team"),
                    "theme": r.get("theme"),
                    "duration_hours": r.get("duration_hours"),
                    "discoveries_count": len(r.get("discoveries", [])),
                    "status": r.get("status")
                }
                for r in reports
            ],
            "highlights": self._extract_highlights(reports),
            "blockers": self._extract_blockers(reports),
        }

        return summary

    def _extract_highlights(self, reports: List[Dict]) -> List[str]:
        """Estrae highlights principali dai report"""
        highlights = []
        for report in reports:
            discoveries = report.get("discoveries", [])
            if discoveries:
                # Prendi prime 2 scoperte
                for disc in discoveries[:2]:
                    highlights.append(f"📌 {report['agent_name']}: {disc}")
        return highlights[:5]  # Max 5 highlights

    def _extract_blockers(self, reports: List[Dict]) -> List[str]:
        """Estrae blockers/issues dai report"""
        blockers = []
        for report in reports:
            if report.get("status") == "in_progress":
                theme = report.get("theme")
                blockers.append(f"⚠️  {report['agent_name']} ({theme}): Ricerca in corso")
        return blockers

    def save_daily_summary(self, date_str: str) -> bool:
        """Salva summary giornaliero come file markdown"""
        summary = self.generate_daily_summary(date_str)

        if not summary:
            return False

        # Genera markdown
        md_content = f"""# 📊 Summary Ricerche Online — {date_str}

**Data**: {date_str}
**Total Report**: {summary['total_reports']} agenti
**Total Scoperte**: {summary['total_discoveries']}
**Raccomandazioni**: {summary['total_recommendations']}

## 👥 Agenti Completati

"""

        for agent in summary.get("agents", []):
            status_icon = "✅" if agent["status"] == "completed" else "⏳"
            md_content += f"- {status_icon} **{agent['name']}** ({agent['team']}) - {agent['theme']}\n"
            md_content += f"  - Durata: {agent['duration_hours']}h | Scoperte: {agent['discoveries_count']}\n\n"

        # Highlights
        if summary.get("highlights"):
            md_content += "## 🌟 Highlights\n\n"
            for highlight in summary["highlights"]:
                md_content += f"{highlight}\n"
            md_content += "\n"

        # Blockers
        if summary.get("blockers"):
            md_content += "## 🔴 Blockers/In Progress\n\n"
            for blocker in summary["blockers"]:
                md_content += f"{blocker}\n"

        # Salva
        date_dir = self.research_dir / date_str
        summary_file = date_dir / f"SUMMARY_{date_str}.md"

        with open(summary_file, 'w') as f:
            f.write(md_content)

        print(f"✅ Summary salvato: {summary_file}")
        return True

    def get_expected_agents(self, date_str: str) -> List[str]:
        """Ritorna agenti che dovrebbero avere ricerca completata oggi"""
        expected = []

        for team_agents in [AGENT_DATABASE["alessandra_team"], AGENT_DATABASE["giorgia_team"]]:
            for agent in team_agents:
                if agent["date"] == date_str:
                    expected.append(agent["name"])

        return expected

    def check_daily_progress(self, date_str: str) -> Dict:
        """Verifica progresso giornaliero"""
        expected = self.get_expected_agents(date_str)

        date_dir = self.research_dir / date_str
        if not date_dir.exists():
            return {
                "date": date_str,
                "expected": expected,
                "completed": [],
                "missing": expected,
                "completion_rate": 0.0
            }

        completed = []
        for report_file in date_dir.glob("*_*.json"):
            report = self.load_report(report_file)
            if report:
                completed.append(report["agent_name"])

        missing = [a for a in expected if a not in completed]
        completion_rate = (len(completed) / len(expected) * 100) if expected else 0

        return {
            "date": date_str,
            "expected": expected,
            "completed": completed,
            "missing": missing,
            "completion_rate": completion_rate
        }


# ============================================================================
# ESEMPIO USO
# ============================================================================

def example_report_benedetta():
    """Crea report esempio per Benedetta"""
    return {
        "agent_name": "Benedetta",
        "team": "alessandra",
        "date": "2026-08-18",
        "theme": "Schema Dati, FEM Standards, JSON Patterns",
        "duration_hours": 2.0,
        "sources": [
            "https://json-schema.org/",
            "https://www.buildingsmart.org/standards/ifc/",
            "https://www.ansys.com/products/structures",
            "https://www.bentley.com/en/products/brands/plaxis"
        ],
        "discoveries": [
            "IFC 4.0+ supporta structural geometry e carichi",
            "JSON-schema.org offre validator open-source Python",
            "ModeSt usa binary format proprietario (.mst)",
            "ANSYS APDL supporta export in formato testuale"
        ],
        "recommendations": [
            "Integrare json-schema validator in backend Python",
            "Pianificare IFC import support per Week 3+",
            "Contattare Tecnisoft per documentazione ModeSt API"
        ],
        "status": "completed"
    }


def main():
    """Esegui esempio"""
    tracker = ResearchTracker()

    # Test: Salva report Benedetta
    print("=" * 70)
    print("🔍 Research Tracker — Example Usage")
    print("=" * 70)

    report = example_report_benedetta()
    print(f"\n1️⃣  Salvando report: {report['agent_name']}")
    tracker.save_report(report)

    # Genera summary
    print(f"\n2️⃣  Generando summary per {report['date']}")
    tracker.save_daily_summary(report['date'])

    # Verifica progresso
    print(f"\n3️⃣  Verifica progresso {report['date']}")
    progress = tracker.check_daily_progress(report['date'])
    print(f"   Expected: {len(progress['expected'])} agenti")
    print(f"   Completed: {len(progress['completed'])} agenti")
    print(f"   Missing: {', '.join(progress['missing'][:3])}...")
    print(f"   Completion: {progress['completion_rate']:.0f}%")

    print("\n✅ Done!")


if __name__ == "__main__":
    main()
