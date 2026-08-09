# Verifica finale - Obiettivo 3 Area Rhodense

## Fonti bloccate

- Accordo: **Accordo locale ambito Rhodense 2024**, Google Drive `1HZLf8y6fjs17ak_Yqm-RUInwLn3nSsqZ`, SHA-256 `cc25031db50587e366672ee61332ee22f4be1ae9f64682b3a73d0639ce32d7be`.
- Zone e corrispondenze OMI: pagina PDF 4.
- Tabelle dei canoni: pagine PDF 33, 35 e 37.
- Conferma umana: `VERIFICA_obiettivo3_rhodense_COMPILATA.md`, SHA-256 dei byte versionati `cbdac25ab0d4c70c8cef98ec196fce5fc7718c654c53d4e8819e6f234c23758e`; SHA-256 dell'originale fornito `167fe15a8e82f48ac1b9e5c73e458ffe70c68fd4e7b34e1357301fb5a9e72ea2`.
- Superfici: Annuario statistico 2026 della Città metropolitana di Milano.

## Canoni confermati

Valori in €/mq al mese. Ogni cella è riportata come sub-fascia 1 / 2 / 3.

| Comuni | Zona | Canoni |
|---|---:|---|
| Arese, Cornaredo, Lainate, Pero, Settimo Milanese | 1 | `5,75-7,19 / 7,20-8,10 / 8,11-9,00` |
| Arese, Cornaredo, Lainate, Pero, Settimo Milanese | 2 | `4,80-5,99 / 6,00-6,79 / 6,80-8,00` |
| Rho | 1 | `6,00-6,99 / 7,00-7,99 / 8,00-10,00` |
| Rho | 2 | `5,50-6,49 / 6,50-7,19 / 7,20-8,20` |
| Pogliano Milanese, Pregnana Milanese, Vanzago | unica | `4,00-4,99 / 5,00-5,99 / 6,00-7,20` |

Le ripetizioni sono intenzionali: l'accordo contiene una tabella distinta per ciascun Comune.

## Geometrie e anomalie

| Comune | Area KML | Scarto ufficiale | Esito |
|---|---:|---:|---|
| Arese | 6,130 km² | -6,5% | avvertenza, R1 mancante |
| Cornaredo | 10,953 km² | -1,1% | valido |
| Lainate | 12,760 km² | -1,3% | valido |
| Pero | 4,991 km² | +0,2% | valido |
| Pogliano Milanese | 4,697 km² | -1,7% | valido |
| Pregnana Milanese | 4,894 km² | -3,5% | valido |
| Rho | 22,333 km² | +0,4% | valido |
| Settimo Milanese | 10,760 km² | +0,4% | valido |
| Vanzago | 6,150 km² | +1,7% | valido |

Arese è deliberatamente fail-closed: pagina 4 associa R1 alla zona 2, ma il KML espone solo B1 e D2. Il simulatore non ricostruisce né estende il perimetro mancante; un indirizzo esterno ai poligoni ufficiali resta non coperto.

La pagina 4 assegna gli edifici attraversati dal confine alla zona di maggior valore. Il generatore conserva l'ordine contrattuale crescente e lo valida contro i canoni confermati.

## Esito

I nove JSON hanno `canoni_confirmed: true`, sono rigenerabili dalle fonti bloccate e sono registrati nel selettore.
