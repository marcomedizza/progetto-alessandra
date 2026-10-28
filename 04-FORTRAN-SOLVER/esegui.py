"""Esecuzione del solutore Fortran telaio2d da Python (Ottavia).

    from esegui import esegui, SOLUTORE
    testo_output = esegui(testo_input)          # stringhe nel formato ASCII del solutore

Il percorso dell'eseguibile si può cambiare con la variabile d'ambiente TELAIO2D_BIN.
Errori:
- FileNotFoundError se il solutore non è compilato (eseguire build.sh);
- RuntimeError con il messaggio del solutore (es. struttura labile);
- TimeoutError se il calcolo supera il tempo massimo.
"""

import os
import subprocess
import tempfile

QUI = os.path.dirname(os.path.abspath(__file__))
SOLUTORE = os.environ.get("TELAIO2D_BIN", os.path.join(QUI, "bin", "telaio2d"))
TEMPO_MASSIMO = 60  # secondi


def esegui(testo_input, solutore=None, tempo_massimo=TEMPO_MASSIMO):
    exe = solutore or SOLUTORE
    if not os.path.exists(exe):
        raise FileNotFoundError(f"solutore non compilato: {exe} (eseguire 04-FORTRAN-SOLVER/build.sh)")
    with tempfile.TemporaryDirectory() as d:
        fin, fout = os.path.join(d, "input.txt"), os.path.join(d, "output.txt")
        with open(fin, "w") as fh:
            fh.write(testo_input)
        try:
            r = subprocess.run([exe, fin, fout], capture_output=True, text=True, timeout=tempo_massimo)
        except subprocess.TimeoutExpired as ex:
            raise TimeoutError(f"il solutore ha superato {tempo_massimo} s") from ex
        if r.returncode != 0:
            # il Fortran aggiunge «STOP 2» all'uscita d'errore: si tiene solo il messaggio
            righe = [x.strip() for x in r.stderr.splitlines() if x.strip() and not x.strip().startswith("STOP")]
            msg = " ".join(x.replace("ERRORE telaio2d: ", "") for x in righe)
            raise RuntimeError(msg or f"errore del solutore (codice {r.returncode})")
        with open(fout) as fh:
            return fh.read()


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Uso: python3 esegui.py input.txt  (stampa l'output del solutore)")
        sys.exit(1)
    with open(sys.argv[1]) as fh:
        print(esegui(fh.read()), end="")
