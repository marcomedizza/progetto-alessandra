#!/usr/bin/env python3
"""
🔴 COMPLIANCE CHECKER — Ricerche Online Obbligatorie
Verifica che OGNI agente faccia ricerca nella sua data
Non negoziabile - Mandato Alessandra + Giorgia
"""

import json
import sys
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Dict, List, Tuple

# Database agenti con date obbligatorie
AGENTS_CALENDAR = {
    "alessandra_team": [
        # Tech Core
        {"name": "Benedetta", "specialty": "Architettura", "required_date": "2026-08-18"},
        {"name": "Irene", "specialty": "Frontend 3D", "required_date": "2026-08-19"},
        {"name": "Natalia", "specialty": "Backend", "required_date": "2026-08-20"},
        {"name": "Elisa", "specialty": "Fortran Solver", "required_date": "2026-08-21"},
        {"name": "Francesca", "specialty": "Ricerca CFD", "required_date": "2026-08-22"},
        {"name": "Valentina", "specialty": "QA Testing", "required_date": "2026-08-23"},
        {"name": "Carla", "specialty": "ModeSt Bridge", "required_date": "2026-08-24"},
        {"name": "Daniela", "specialty": "ModeSt Research", "required_date": "2026-08-25"},
        {"name": "Lucia", "specialty": "UI Editor", "required_date": "2026-08-26"},
        {"name": "Mariana", "specialty": "Results Viz", "required_date": "2026-08-27"},
        {"name": "Ottavia", "specialty": "Build Wrapper", "required_date": "2026-08-28"},
        {"name": "Paola", "specialty": "Data Converter", "required_date": "2026-08-29"},
        # Team Strutturale
        {"name": "Roberta", "specialty": "Calcestruzzo Armato", "required_date": "2026-08-30"},
        {"name": "Martina", "specialty": "Acciaio", "required_date": "2026-08-31"},
        {"name": "Sofia", "specialty": "Alluminio", "required_date": "2026-09-01"},
        {"name": "Giulia", "specialty": "Legno e Rinforzi Fibre", "required_date": "2026-09-02"},
        {"name": "Alessia", "specialty": "Geotecnica", "required_date": "2026-09-03"},
        {"name": "Chiara", "specialty": "Muratura Normale", "required_date": "2026-09-04"},
        {"name": "Ilaria", "specialty": "Muratura Armata", "required_date": "2026-09-05"},
    ],
    "giorgia_team": [
        {"name": "Aurora", "specialty": "Pricing", "required_date": "2026-08-18"},
        {"name": "Livia", "specialty": "Email", "required_date": "2026-08-19"},
        {"name": "Veronica", "specialty": "Normative", "required_date": "2026-08-20"},
        {"name": "Camilla", "specialty": "News", "required_date": "2026-08-21"},
        {"name": "Laura", "specialty": "Progress", "required_date": "2026-08-22"},
    ],
}

RESEARCH_DIR = Path("/home/user/progetto-alessandra/RICERCHE_ONLINE")


class ComplianceChecker:
    """Verifica compliance ricerche obbligatorie"""

    def __init__(self):
        self.today = date.today()
        self.deadline_time = "18:00"
        self.reports = []

    def get_today_expected_agents(self) -> List[Dict]:
        """Ritorna agenti che devono completare ricerca OGGI"""
        today_str = self.today.strftime("%Y-%m-%d")
        expected = []

        for team_agents in [AGENTS_CALENDAR["alessandra_team"], AGENTS_CALENDAR["giorgia_team"]]:
            for agent in team_agents:
                if agent["required_date"] == today_str:
                    expected.append(agent)

        return expected

    def get_agent_report(self, agent_name: str, date_str: str) -> Tuple[bool, Path]:
        """Controlla se agente ha completato report nella data"""
        report_dir = RESEARCH_DIR / date_str
        report_file = report_dir / f"{agent_name}_{date_str}.json"
        report_file_md = report_dir / f"{agent_name}_{date_str}.md"

        if report_file.exists():
            return True, report_file
        elif report_file_md.exists():
            return True, report_file_md
        return False, None

    def validate_report(self, report_path: Path) -> Tuple[bool, str]:
        """Valida qualità report"""
        try:
            if report_path.suffix == ".json":
                with open(report_path) as f:
                    data = json.load(f)

                # Controlli obbligatori
                checks = [
                    ("agent_name" in data, "Agent name missing"),
                    ("sources" in data and len(data.get("sources", [])) >= 3, "Min 3 sources required"),
                    (
                        "discoveries" in data and len(data.get("discoveries", [])) >= 3,
                        "Min 3 discoveries required",
                    ),
                    (
                        "recommendations" in data and len(data.get("recommendations", [])) >= 2,
                        "Min 2 recommendations required",
                    ),
                    ("duration_hours" in data and 0.5 <= data.get("duration_hours", 0) <= 8, "Invalid duration"),
                ]

                for check, msg in checks:
                    if not check:
                        return False, msg

                return True, "✅ Report valido"

            elif report_path.suffix == ".md":
                # Validazione base markdown
                with open(report_path) as f:
                    content = f.read()

                checks = [
                    ("Scoperte" in content or "scoperte" in content, "No discoveries section"),
                    ("Raccomandazioni" in content or "raccomandazioni" in content, "No recommendations"),
                    ("http" in content, "No sources/links"),
                ]

                for check, msg in checks:
                    if not check:
                        return False, msg

                return True, "✅ Report valido (markdown)"

        except Exception as e:
            return False, f"Errore validazione: {str(e)}"

        return False, "Unknown error"

    def check_today_compliance(self) -> Dict:
        """Verifica compliance per OGGI"""
        today_str = self.today.strftime("%Y-%m-%d")
        expected = self.get_today_expected_agents()

        compliance = {
            "date": today_str,
            "expected_agents": len(expected),
            "completed": [],
            "missing": [],
            "invalid": [],
            "completion_rate": 0.0,
        }

        if not expected:
            return {
                **compliance,
                "message": "Nessun agente ha ricerca obbligatoria oggi",
            }

        for agent in expected:
            has_report, report_path = self.get_agent_report(agent["name"], today_str)

            if not has_report:
                compliance["missing"].append(
                    {
                        "name": agent["name"],
                        "specialty": agent["specialty"],
                        "status": "🔴 MISSING — Deadline 18:00",
                    }
                )
            else:
                is_valid, msg = self.validate_report(report_path)
                if is_valid:
                    compliance["completed"].append(
                        {
                            "name": agent["name"],
                            "specialty": agent["specialty"],
                            "status": "✅ COMPLETATO",
                            "file": report_path.name,
                        }
                    )
                else:
                    compliance["invalid"].append(
                        {
                            "name": agent["name"],
                            "specialty": agent["specialty"],
                            "status": f"⚠️  INVALIDO — {msg}",
                            "file": report_path.name,
                        }
                    )

        total_ok = len(compliance["completed"])
        total = len(expected)
        compliance["completion_rate"] = (total_ok / total * 100) if total > 0 else 0

        return compliance

    def generate_compliance_report(self) -> str:
        """Genera report compliance giornaliero"""
        compliance = self.check_today_compliance()

        report = f"""
╔════════════════════════════════════════════════════════════════════╗
║           🔴 COMPLIANCE CHECK — Ricerche Online                    ║
║                  {compliance['date']}                              ║
╚════════════════════════════════════════════════════════════════════╝

📊 STATUS ODIERNO
─────────────────────────────────────────────────────────────────────
Expected Agents:      {compliance['expected_agents']}
Completed:            {len(compliance['completed'])}  ✅
Missing:              {len(compliance['missing'])}  🔴
Invalid Quality:      {len(compliance['invalid'])}  ⚠️
Completion Rate:      {compliance['completion_rate']:.0f}%
Deadline:             18:00 (NON NEGOZIABILE)

"""

        if compliance["completed"]:
            report += "✅ COMPLETATI:\n"
            for agent in compliance["completed"]:
                report += f"   • {agent['name']} ({agent['specialty']}) — {agent['status']}\n"
            report += "\n"

        if compliance["missing"]:
            report += "🔴 MANCANTI (ESCALATE):\n"
            for agent in compliance["missing"]:
                report += f"   • {agent['name']} ({agent['specialty']}) — {agent['status']}\n"
            report += "\n"

        if compliance["invalid"]:
            report += "⚠️  QUALITÀ INSUFFICIENTE (FIX REQUIRED):\n"
            for agent in compliance["invalid"]:
                report += f"   • {agent['name']} ({agent['specialty']}) — {agent['status']}\n"
            report += "\n"

        # Raccomandazioni
        if compliance["completion_rate"] < 100:
            report += """
🚨 AZIONE RICHIESTA (ENTRO 18:00):
───────────────────────────────────────────────────────────────────
1. Contatta agenti mancanti via Slack IMMEDIATAMENTE
2. Fornisci supporto se hanno dubbi su tema ricerca
3. Se problemi tecnici → fornisci alternativa (mobile, tablet, etc.)
4. Report invalidi → chiedi revisione entro 1 ora

⚠️  Se deadline passa senza compliance → ESCALATE a Alessandra/Giorgia
"""

        report += "\n✍️  SLACK UPDATE (post in #progetto-alessandra):\n"
        report += f"```\n📊 Ricerche Online — {compliance['date']}\n"
        for agent in compliance["completed"]:
            report += f"✅ {agent['name']}\n"
        for agent in compliance["missing"]:
            report += f"🔴 {agent['name']}\n"
        report += f"\nCompletion: {compliance['completion_rate']:.0f}% ({len(compliance['completed'])}/{compliance['expected_agents']})\n```\n"

        return report

    def generate_weekly_report(self, start_date: str = None) -> str:
        """Genera report settimanale compliance"""
        if not start_date:
            # Ultima settimana
            start = self.today - timedelta(days=7)
            start_date = start.strftime("%Y-%m-%d")

        all_agents = list(AGENTS_CALENDAR["alessandra_team"]) + list(
            AGENTS_CALENDAR["giorgia_team"]
        )

        stats = {
            "total_agents": len(all_agents),
            "completed_count": 0,
            "missing_count": 0,
            "on_time_pct": 0.0,
        }

        report = f"""
╔════════════════════════════════════════════════════════════════════╗
║     📈 WEEKLY COMPLIANCE REPORT — Ricerche Online                   ║
║                  Starting: {start_date}                             ║
╚════════════════════════════════════════════════════════════════════╝

SUMMARY:
────────────────────────────────────────────────────────────────────
Total Agents:         {stats['total_agents']}
Completed:            [Data would be calculated]
Missing:              [Data would be calculated]
On-Time Delivery:     [Data would be calculated]%

✅ TREND: [Would show week-over-week improvement/decline]

"""

        return report

    def print_today_status(self):
        """Stampa status odierno"""
        print(self.generate_compliance_report())

    def save_compliance_log(self):
        """Salva log compliance"""
        today_str = self.today.strftime("%Y-%m-%d")
        log_file = RESEARCH_DIR / f"COMPLIANCE_{today_str}.txt"

        with open(log_file, 'w') as f:
            f.write(self.generate_compliance_report())

        print(f"✅ Compliance log salvato: {log_file}")


def main():
    """Esegui compliance check"""
    checker = ComplianceChecker()

    # Stampa status odierno
    print("\n" + "=" * 70)
    print("🔴 COMPLIANCE CHECKER — Ricerche Online Obbligatorie")
    print("=" * 70)

    checker.print_today_status()

    # Salva log
    checker.save_compliance_log()


if __name__ == "__main__":
    main()
