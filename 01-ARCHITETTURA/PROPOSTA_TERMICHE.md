# Proposta: proprietà termiche dei materiali (Benedetta, 24/11/2026)

**Stato: proposta, non adottata.** Va decisa insieme alla proposta del 23/11 in `CONFRONTO_SCHEMA_EPJSON.md`, che resta in attesa di Marco. Lo schema in vigore resta la v1.2.

## Motivo

Dal confronto con il dizionario dei dati di EnergyPlus (23/11) risulta che le proprietà termiche dei materiali sono il punto d'incontro naturale tra modello strutturale e modello energetico. Per un oggetto `Material` EnergyPlus richiede:
- Thickness [m];
- Conductivity [W/m-K];
- Density [kg/m3];
- Specific Heat [J/kg-K].

Lo schema ha soltanto il peso specifico.

## Proposta

1. **Nessun campo nuovo nel telaio.** Il 29/10 è stato deciso di non accettare nello schema voci che il programma non usa, perché un dato accettato e ignorato dà risultati sbagliati senza avviso. Conducibilità e calore specifico non servono al calcolo statico.
2. **Catalogo dei materiali comune**, in un file separato (per esempio `01-ARCHITETTURA/CATALOGO_MATERIALI.json`). Per ogni materiale:
   - `id`, uguale a quello dello schema del telaio;
   - `E` [kN/m²], `peso_specifico` [kN/m³], `alfa_t` [1/°C], letti dallo schema strutturale;
   - `conducibilita` [W/(m·K)] e `calore_specifico` [J/(kg·K)], letti dal futuro modello energetico.
3. **Spessore**: non appartiene al materiale ma allo strato della stratigrafia, come `Construction` / `Material` Thickness in EnergyPlus. Va nel modello energetico, non nel catalogo.
4. **Densità**: si ricava dal peso specifico, ρ = γ·1000/g. Non va scritta due volte, per evitare valori incoerenti.

## Valori

Il catalogo non contiene ancora valori. Conducibilità e calori specifici vanno presi da fonti normative, per esempio le tabelle di UNI EN ISO 10456 o UNI 10351. Quei testi non sono disponibili agli agenti e non vanno scritti a memoria.

## Da decidere con Marco

- Se la parte energetica rientra nel programma e quando.
- Se il catalogo comune è la strada giusta o se il modello energetico resta del tutto separato.
