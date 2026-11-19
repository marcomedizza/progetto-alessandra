# Scenari utente automatici (Renata, Vittoria, Lucia)

Script Playwright (Chromium) che usano l'interfaccia 3D come un utente. Dal 19/11/2026 stanno nel repository (punto 91). Prima erano solo nella cartella di lavoro della sessione e si sarebbero persi a un riavvio.

**Esecuzione di tutti gli scenari**, dalla radice del repository, con il solutore compilato:

    python3 06-TESTING/scenari/esegui_scenari.py [cartella_uscite]

L'esecutore:
- avvia il servizio sulla porta 8765 e genera il modello grande (4681 nodi, 9150 aste);
- esegue gli script nell'ordine giusto: `s35` scrive il file che `s36` riapre, e lo script generale spegne il servizio (S13), quindi va per ultimo;
- controlla per ciascuno codice d'uscita, errori di console ed esiti `false`;
- salva le uscite (`*.txt`) e le schermate nella cartella indicata.

Durata circa 3 minuti.

| Script | Scenari | Controlli numerici nello script |
|---|---|---|
| `s01_s33_generale.js` | S1–S33 in sequenza, combinazione, S13 servizio spento | sì (S10 è un'eccezione nota: il clic non seleziona il nodo, vedi `s10_struttura_labile.js`) |
| `s10_struttura_labile.js` | S10, struttura labile dopo aver tolto un vincolo | messaggio |
| `s17_disegno.js` | S17, disegno di aste col mouse | messaggi |
| `s20_s22_pannello.js` | S20–S22, cedimenti e trapezi dal pannello | sì, valori risolti a mano |
| `s23_s26_trapezi.js` | S23–S26, trapezi, deformata | messaggi |
| `s27_s30_termiche.js` | S27–S30, distorsioni termiche | sì |
| `s31_s33_farfalla.js` | S31–S33, ΔT a farfalla, h della sezione | messaggi e freccia |
| `s34_combinazioni.js` | S34, combinazioni di C23, C24, C26, C27, C30 | valori stampati, controllo a vista |
| `s35_avvisi.js` | S35, avviso di plausibilità (punto 76) | classe e testo dell'avviso |
| `s36_menu.js` | S36, menu dopo file e «Nuovo» (D26) | voci del menu |
| `s37_pannello.js` | S37, trapezio, ΔT, cedimento, Ctrl+Z su C2 | sì, 8 controlli |
| `d3_d4_etichette.js` | D3/D4, etichette e nodo duplicato | valori stampati |
| `molle.js`, `viste.js`, `termiche_etichette.js` | schermate per il controllo a vista | — |
| `modello_grande.js` | modello da 9150 aste: tempi e memoria | errori di console |

I controlli automatici non sostituiscono il controllo a vista delle schermate, obbligatorio dal 07/11 (difetto D20).
