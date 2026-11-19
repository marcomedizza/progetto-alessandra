"""Esecuzione automatica degli scenari utente nel navigatore (Renata, Vittoria; 19/11/2026, punto 91).

Avvia il servizio sulla porta 8765, genera il modello grande, esegue gli script di questa cartella con Playwright
(Chromium) e controlla per ciascuno:
- che termini senza errori;
- che non ci siano errori di console (chiavi «errori» o «errori_console» vuote);
- che l'esito non contenga «false», salvo le eccezioni note in ECCEZIONI.

I valori numerici sono controllati dentro gli script che li confrontano con la soluzione a mano (S20–S22, S28–S30,
S37). Per gli altri il confronto con i valori attesi di 06-TESTING/flusso.md resta a vista, sulle schermate e
sulle uscite salvate nella cartella indicata.

Uso, dalla radice del repository:
    python3 06-TESTING/scenari/esegui_scenari.py [cartella_uscite]
Richiede node con playwright e il solutore compilato (04-FORTRAN-SOLVER/build.sh).
"""

import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.request

QUI = os.path.dirname(os.path.abspath(__file__))
RADICE = os.path.abspath(os.path.join(QUI, "..", ".."))
PORTA = 8765

# ordine: s35 scrive il file che s36 riapre; lo script generale spegne il servizio (S13) e va per ultimo
SCRIPT = ["s10_struttura_labile.js", "s17_disegno.js", "s20_s22_pannello.js", "s23_s26_trapezi.js",
          "s27_s30_termiche.js", "s31_s33_farfalla.js", "s34_combinazioni.js", "s35_avvisi.js", "s36_menu.js",
          "s37_pannello.js", "d3_d4_etichette.js", "molle.js", "termiche_etichette.js", "viste.js",
          "modello_grande.js", "s01_s33_generale.js"]

# S10 nello script generale: il clic sul nodo 1 di C1 non lo seleziona (problema dello script, non
# dell'interfaccia, vedi flusso.md 10/11); il comportamento è provato da s10_struttura_labile.js
ECCEZIONI = {"s01_s33_generale.js": ['"S10": false']}


def avvia_servizio():
    p = subprocess.Popen([sys.executable, "-m", "uvicorn", "--app-dir", "03-BACKEND/servizio", "app:app",
                          "--port", str(PORTA)], cwd=RADICE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for _ in range(50):
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{PORTA}/api/salute", timeout=1)
            return p
        except OSError:
            time.sleep(0.2)
    p.kill()
    raise RuntimeError(f"il servizio non risponde sulla porta {PORTA}")


def modello_grande(out):
    sys.path.insert(0, os.path.join(RADICE, "04-FORTRAN-SOLVER"))
    import prova_prestazioni
    m = prova_prestazioni.telaio(30, 150)
    m["progetto"] = {"id": "prova", "nome": "Telaio 30 x 150", "tipo_modello": "telaio_piano",
                     "unita": {"lunghezza": "m", "forza": "kN"}}
    with open(os.path.join(out, "grande.json"), "w", encoding="utf-8") as fh:
        json.dump(m, fh)


def errori_console(testo):
    """Contenuti non vuoti delle liste di errori stampate dagli script."""
    trovati = re.findall(r'"?errori(?:_console)?"?\s*:?\s*\[([^\]]*)\]', testo)
    return [t.strip() for t in trovati if t.strip()]


def controlla(nome, ris):
    problemi = []
    if ris.returncode != 0:
        problemi.append(f"codice d'uscita {ris.returncode}: {ris.stderr.strip()[-200:]}")
    problemi += [f"errori di console: {e[:120]}" for e in errori_console(ris.stdout)]
    falsi = re.findall(r'"[^"]+":\s*false', ris.stdout)
    falsi = [f for f in falsi if f not in ECCEZIONI.get(nome, [])]
    problemi += [f"esito negativo {f}" for f in falsi]
    return problemi


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else tempfile.mkdtemp(prefix="scenari_")
    os.makedirs(out, exist_ok=True)
    modello_grande(out)
    servizio = avvia_servizio()
    esiti = []
    try:
        for nome in SCRIPT:
            if servizio.poll() is not None:  # spento dallo scenario S13
                servizio = avvia_servizio()
            argomenti = ["node", os.path.join(QUI, nome), out]
            if nome == "s01_s33_generale.js":
                argomenti.append(str(servizio.pid))
            t0 = time.time()
            ris = subprocess.run(argomenti, cwd=RADICE, capture_output=True, text=True, timeout=600)
            with open(os.path.join(out, nome.replace(".js", ".txt")), "w", encoding="utf-8") as fh:
                fh.write(ris.stdout + ris.stderr)
            esiti.append((nome, time.time() - t0, controlla(nome, ris)))
            print(f"{'✓' if not esiti[-1][2] else '✗'} {nome:28} {esiti[-1][1]:5.1f} s", *esiti[-1][2], sep="\n    " if esiti[-1][2] else " ")
    finally:
        if servizio.poll() is None:
            servizio.terminate()
    falliti = [e for e in esiti if e[2]]
    print(f"\n{len(esiti) - len(falliti)} script superati su {len(esiti)}; uscite e schermate in {out}")
    return 1 if falliti else 0


if __name__ == "__main__":
    sys.exit(main())
