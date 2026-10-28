# Rapporto di Vittoria — 28/10/2026

**Compito**: compilazione, verifica del solutore e prova del prototipo attraverso il servizio.

**Procedura**
1. `04-FORTRAN-SOLVER/build.sh` → compilato con gfortran 13.3 senza errori (un avviso sul confronto tra reali, innocuo).
2. `python3 06-TESTING/casi/verifica_casi.py --fortran` → C1–C9 superati, zero scostamenti dal riferimento.
3. `python3 06-TESTING/casi/verifica_casi.py --api` → stesso esito passando dal servizio FastAPI.
4. `python3 03-BACKEND/servizio/test_app.py` → 9 prove superate, compresa la combinazione SLU (sovrapposizione esatta).
5. Servizio avviato con uvicorn, scenari S1–S13 di `06-TESTING/flusso.md` eseguiti nel navigatore Chromium: tutti superati, nessun errore nella console.

**Non provato**: Firefox (non disponibile nell'ambiente di prova). Da eseguire a mano.
