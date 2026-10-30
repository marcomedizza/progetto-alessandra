# Rapporto di Vittoria — 30/10/2026

**Procedura ed esiti** (dopo le consegne del mattino)
1. `04-FORTRAN-SOLVER/build.sh` → solutore v0.2 compilato.
2. `verifica_casi.py` (riferimento), `--fortran`, `--api` → C1–C10 superati, zero scostamenti dal riferimento su spostamenti, reazioni, rotazioni d'estremità e N, V, M.
3. `03-BACKEND/servizio/test_app.py` → 16 prove superate.
4. `04-FORTRAN-SOLVER/prova_prestazioni.py` → banda e matrice piena coincidono (scarto ≤ 2,4·10⁻¹²); equilibrio verticale esatto fino a 14 043 gdl.
5. Scenari S1–S19 in Chromium → superati, nessun errore nella console. S10 superato con la prova dedicata.

**Non provato**: Firefox, non disponibile nell'ambiente automatico. Da fare a mano.
