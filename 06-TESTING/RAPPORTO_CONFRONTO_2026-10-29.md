# Rapporto di confronto del solutore — 29/10/2026

**Autrice**: Silvia (laboratorio di regressione) · sostituisce il rapporto del 28/10

**Comandi**: `verifica_casi.py --fortran` e `verifica_casi.py --api`. Dal 29/10 entrambi gestiscono anche le combinazioni (C10).

**Tolleranze**: valori attesi 0,5 % relativa (minimo 1·10⁻⁶ assoluto); confronto completo con il riferimento 1·10⁻⁶ relativa, per identificativo di nodo e asta.

| Caso | Controlli sui valori attesi (servizio) | Scostamenti servizio / riferimento |
|---|---|---|
| C1 Trave appoggiata, carico uniforme | 6 superati, 0 non superati | 0 |
| C2 Mensola, carico in punta | 5 superati, 0 non superati | 0 |
| C3 Portale incastrato, forza orizzontale | 7 superati, 0 non superati | 0 |
| C4 Portale incastrato, carico uniforme sul traverso | 6 superati, 0 non superati | 0 |
| C5 Telaio a due piani | 3 superati, 0 non superati | 0 |
| C6 Trave Gerber, carico uniforme | 6 superati, 0 non superati | 0 |
| C7 Trave appoggiata, carico concentrato fuori mezzeria | 5 superati, 0 non superati | 0 |
| C8 Trave appoggiata con molla in mezzeria | 4 superati, 0 non superati | 0 |
| C9 Portale a tre cerniere con molla al piede | 7 superati, 0 non superati | 0 |
| C10 Trave appoggiata, combinazione SLU di due casi | 3 superati, 0 non superati | 0 |

**Altre prove**: `03-BACKEND/servizio/test_app.py` 12 prove superate, tra cui struttura labile (errore leggibile), modello modificato come dall'interfaccia (nodo e asta aggiunti con identificativi non consecutivi), limite di dimensione.

**Limiti**: solo statica lineare di telai piani. C5 resta da confrontare con un programma commerciale.
