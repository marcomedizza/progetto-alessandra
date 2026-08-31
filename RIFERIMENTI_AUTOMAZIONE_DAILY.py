#!/usr/bin/env python3
"""
Automazione Daily: Monitoraggio RIFERIMENTI → JSON Conversion → Agata Catalog
Script che verifica daily nuovi testi in RIFERIMENTI/input, converte a JSON,
e prepara catalogo per distribuzione ad Agata.
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
from anthropic import Anthropic

# Configurazione
RIFERIMENTI_DIR = Path("RIFERIMENTI")
INPUT_DIR = RIFERIMENTI_DIR / "input"
OUTPUT_DIR = RIFERIMENTI_DIR / "output"
PROCESSED_DIR = RIFERIMENTI_DIR / "processed"
CATALOG_DIR = RIFERIMENTI_DIR / "catalogo"

# Assicura che tutte le directory esistono
for dir_path in [INPUT_DIR, OUTPUT_DIR, PROCESSED_DIR, CATALOG_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)


def load_processed_files():
    """Carica lista di file già processati"""
    processed_file = CATALOG_DIR / "processed_files.json"
    if processed_file.exists():
        with open(processed_file, "r") as f:
            return json.load(f)
    return {"processed": {}}


def save_processed_files(data):
    """Salva lista di file processati"""
    processed_file = CATALOG_DIR / "processed_files.json"
    with open(processed_file, "w") as f:
        json.dump(data, f, indent=2)


def convert_text_to_json(text_content, filename):
    """Usa Claude API per convertire testo a JSON strutturato"""
    try:
        client = Anthropic()
    except Exception as e:
        print(f"\n⚠️  ERRORE: Anthropic API non configurata")
        print(f"   Setup: export ANTHROPIC_API_KEY='your-api-key'")
        raise

    # Prompt per trasformazione
    prompt = f"""Converti il seguente documento testo in JSON strutturato.

Segui questi principi:
1. Identifica la struttura gerarchica (titoli, sezioni, sottosezioni)
2. Converti elenchi puntati in array JSON
3. Normalizza date a formato ISO 8601 (YYYY-MM-DD)
4. Normalizza durate a {{value, unit}} objects
5. Aggiungi ID univoci a ogni oggetto
6. Includi metadata (versione, data, fonte)

Documento da convertire:
---
{text_content}
---

Rispondi SOLO con il JSON valido, niente altro."""

    response = client.messages.create(
        model="claude-opus-5",
        max_tokens=4096,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    # Estrai JSON dalla risposta
    json_text = response.content[0].text

    # Pulisci JSON se necessario (rimuovi markdown code blocks)
    json_text = re.sub(r'^```json\s*', '', json_text)
    json_text = re.sub(r'\s*```$', '', json_text)

    return json_text


def process_new_files():
    """Processa tutti i nuovi file in RIFERIMENTI/input"""
    processed = load_processed_files()
    new_conversions = []

    # Verifica file in input
    if not INPUT_DIR.exists():
        print(f"[{datetime.now().isoformat()}] INPUT_DIR non esiste ancora")
        return new_conversions

    for file_path in INPUT_DIR.glob("*.md"):
        filename = file_path.name

        # Salta se già processato
        if filename in processed["processed"]:
            continue

        print(f"[{datetime.now().isoformat()}] Processing: {filename}")

        try:
            # Leggi contenuto
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Converti a JSON
            json_content = convert_text_to_json(content, filename)

            # Valida JSON
            json_data = json.loads(json_content)

            # Salva JSON
            json_filename = file_path.stem + ".json"
            json_path = OUTPUT_DIR / json_filename
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)

            # Crea entry catalogo
            catalog_entry = {
                "source_file": filename,
                "json_file": json_filename,
                "conversion_date": datetime.now().isoformat(),
                "status": "ready_for_distribution",
                "processing_time": "auto"
            }

            catalog_path = CATALOG_DIR / (file_path.stem + "_catalog.json")
            with open(catalog_path, "w", encoding="utf-8") as f:
                json.dump(catalog_entry, f, indent=2, ensure_ascii=False)

            # Sposta file in processed
            processed_path = PROCESSED_DIR / filename
            file_path.rename(processed_path)

            # Registra processamento
            processed["processed"][filename] = {
                "date": datetime.now().isoformat(),
                "json_file": json_filename,
                "status": "completed"
            }
            save_processed_files(processed)

            new_conversions.append({
                "source": filename,
                "json": json_filename,
                "catalog": catalog_path.name
            })

            print(f"✅ {filename} → {json_filename}")

        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error in {filename}: {e}")
            # Salva testo grezzo se JSON parsing fallisce
            raw_path = OUTPUT_DIR / (file_path.stem + "_raw.txt")
            with open(raw_path, "w") as f:
                f.write(json_content)
        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")

    return new_conversions


def generate_agata_catalog():
    """Genera catalogo finale per Agata"""
    catalog_data = {
        "metadata": {
            "generated_date": datetime.now().isoformat(),
            "source": "RIFERIMENTI Automation System",
            "destination": "Agata (Infrastructure Orchestrator)"
        },
        "conversions": []
    }

    # Raccoglie tutti i file di catalogo
    for catalog_file in CATALOG_DIR.glob("*_catalog.json"):
        with open(catalog_file, "r") as f:
            entry = json.load(f)
            catalog_data["conversions"].append(entry)

    # Salva catalogo master per Agata
    master_catalog = CATALOG_DIR / "AGATA_CATALOGO_MASTER.json"
    with open(master_catalog, "w", encoding="utf-8") as f:
        json.dump(catalog_data, f, indent=2, ensure_ascii=False)

    return catalog_data


def create_agata_report(new_conversions):
    """Crea report per Agata"""
    if not new_conversions:
        return None

    report = {
        "date": datetime.now().isoformat(),
        "title": "Nuove Conversioni Testo → JSON Pronte per Distribuzione",
        "count": len(new_conversions),
        "conversions": new_conversions,
        "action_required": "Cataloga e fornisci ai soggetti di riferimento",
        "instructions": {
            "step1": "Leggi CATALOGO_MASTER.json per dettagli conversioni",
            "step2": "Per ogni conversion, accedi a OUTPUT/{json_file}",
            "step3": "Verifica struttura JSON è corretta",
            "step4": "Cataloga nel sistema di tracking risorse",
            "step5": "Comunica ai soggetti di riferimento"
        }
    }

    # Salva report
    report_path = CATALOG_DIR / f"AGATA_REPORT_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    return report


def main():
    """Main automation loop"""
    print(f"\n{'='*60}")
    print(f"RIFERIMENTI AUTOMAZIONE DAILY")
    print(f"Data/Ora: {datetime.now().isoformat()}")
    print(f"{'='*60}\n")

    # Processa nuovi file
    new_conversions = process_new_files()

    if new_conversions:
        print(f"\n✅ {len(new_conversions)} nuove conversioni completate")

        # Genera catalogo master
        catalog = generate_agata_catalog()
        print(f"📋 Catalogo master generato: CATALOGO_MASTER.json")

        # Crea report per Agata
        report = create_agata_report(new_conversions)
        if report:
            print(f"📧 Report per Agata: {report}")
    else:
        print("ℹ️  Nessun nuovo file da processare")

    print(f"\n{'='*60}\n")


if __name__ == "__main__":
    main()
