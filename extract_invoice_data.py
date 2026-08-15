#!/usr/bin/env python3
"""
Extract invoice data from XML files for HTML interface
"""

import xml.etree.ElementTree as ET
from pathlib import Path
import json

def extract_invoice_from_xml(xml_file):
    """Extract invoice data from FatturaPA XML"""
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        ns = {
            'p': 'http://ivaservizi.agenziaentrate.gov.it/docs/xsd/fatture/v1.2',
            'ds': 'http://www.w3.org/2000/09/xmldsig#'
        }

        data = {'id': xml_file.stem}

        body = root.find('.//p:FatturaElettronicaBody', ns) or root.find('.//FatturaElettronicaBody')

        if body is not None:
            doc_header = body.find('.//p:DatiGenerali/p:DatiGeneraliDocumento', ns) or \
                        body.find('.//DatiGenerali/DatiGeneraliDocumento')
            if doc_header is not None:
                data['numero'] = doc_header.findtext('p:Numero', default='', namespaces=ns) or \
                               doc_header.findtext('Numero', default='')
                data['data'] = doc_header.findtext('p:Data', default='', namespaces=ns) or \
                             doc_header.findtext('Data', default='')
                importo_elem = doc_header.find('p:ImportoTotaleDocumento', ns) or doc_header.find('ImportoTotaleDocumento')
                data['importo'] = float(importo_elem.text) if importo_elem is not None else 0

            fornitore_elem = body.find('.//p:DatiCessionario/p:DatiAnagrafici/p:Anagrafica/p:Denominazione', ns) or \
                            body.find('.//DatiCessionario/DatiAnagrafici/Anagrafica/Denominazione')
            data['fornitore'] = fornitore_elem.text if fornitore_elem is not None else 'N/A'

            riga = body.find('.//p:DatiBeniServizi/p:DettaglioLinee', ns) or body.find('.//DatiBeniServizi/DettaglioLinee')
            if riga is not None:
                desc = riga.findtext('p:Descrizione', default='', namespaces=ns) or riga.findtext('Descrizione', default='')
                data['oggetto'] = desc[:100]

            riepilogo = body.find('.//p:DatiBeniServizi/p:DatiRiepilogo', ns) or body.find('.//DatiBeniServizi/DatiRiepilogo')
            if riepilogo is not None:
                iva_elem = riepilogo.find('p:Imposta', ns) or riepilogo.find('Imposta')
                data['iva'] = float(iva_elem.text) if iva_elem is not None else 0

            # Default category
            data['categoria'] = categorize_invoice(data)

        return data
    except Exception as e:
        print(f"Error: {e}")
        return None

def categorize_invoice(invoice):
    """Categorize invoice"""
    desc = (invoice.get('oggetto', '') + invoice.get('fornitore', '')).lower()
    keywords = {
        'Spese ufficio': ['ufficio', 'materiale', 'amazon', 'click'],
        'Canoni ufficio': ['affitto', 'locazione', 'canone'],
        'Software': ['software', 'licenza'],
        'Gasolio': ['gasolio', 'diesel'],
        'Telefono': ['telefono', 'telecom'],
        'ENEL': ['enel', 'energia', 'luce'],
    }
    for cat, kws in keywords.items():
        if any(k in desc for k in kws):
            return cat
    return 'Spese ufficio'

if __name__ == "__main__":
    xml_folder = Path(r"D:\progetto-alessandra\10-OFFERTE E FATTURAZIONE\FATTURE RICEVUTE\2026\PRIMO TRIMETRE")
    xml_files = [f for f in xml_folder.glob("*.xml") if not f.name.endswith('_metaDato.xml')]

    invoices = []
    for xml_file in xml_files:
        inv = extract_invoice_from_xml(xml_file)
        if inv:
            invoices.append(inv)

    # Save as JSON
    output_json = r"D:\progetto-alessandra\10-OFFERTE E FATTURAZIONE\fatture ricevute\2026\PRIMO TRIMETRE\invoices_data.json"
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(invoices, f, ensure_ascii=False, indent=2)

    print(f"✅ {len(invoices)} fatture estratte in invoices_data.json")
