# Rapporto di confronto del solutore Fortran — 27/10/2026

**Autrice**: Silvia (laboratorio di regressione) · **Comando**: `python3 06-TESTING/casi/verifica_casi.py --fortran`

**Tolleranze**: valori attesi da formule chiuse 0,5 % relativa (minimo 1·10⁻⁶ assoluto); confronto completo Fortran / risolutore di riferimento Python 1·10⁻⁶ relativa su ogni spostamento, reazione e valore di N, V, M.

| Caso | Controlli sui valori attesi | Scostamenti Fortran / riferimento |
|---|---|---|
| C1 Trave appoggiata, carico uniforme | 6 superati, 0 non superati | 0 |
| C2 Mensola, carico in punta | 5 superati, 0 non superati | 0 |
| C3 Portale incastrato, forza orizzontale | 7 superati, 0 non superati | 0 |
| C4 Portale incastrato, carico uniforme sul traverso | 6 superati, 0 non superati | 0 |
| C5 Telaio a due piani | 3 superati, 0 non superati | 0 |
| C6 Trave Gerber, carico uniforme | 6 superati, 0 non superati | 0 |
| C7 Trave appoggiata, carico concentrato fuori mezzeria | 5 superati, 0 non superati | 0 |
| C8 Trave appoggiata con molla in mezzeria | 4 superati, 0 non superati | 0 |

**Esito**: tutti i controlli superati su C1–C8. Il percorso modello JSON → convertitore → Fortran → risultati è verificato anche attraverso il servizio FastAPI (`03-BACKEND/servizio/test_app.py`, 8 prove superate).

**Limiti noti**: la verifica copre solo statica lineare di telai piani. C5 è confrontato solo su equilibrio globale e con il riferimento Python: serve il confronto con un programma commerciale.
