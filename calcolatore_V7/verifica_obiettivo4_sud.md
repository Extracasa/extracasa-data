# Verifica finale - Obiettivo 4 Area Sud

## Fonti e conferma

- Sei accordi comunali distinti, con hash PDF bloccati in `tools/comuni_obiettivo4.json`.
- Zone e corrispondenze OMI: art. 4.1.a, pagina PDF 3.
- Tabelle dei canoni: pagine PDF 15 o 17, secondo il Comune.
- Conferma umana: `VERIFICA_obiettivo4_sud_COMPILATA.md`, SHA-256 dei byte versionati `8adaec3d6f5799396293d34a06a156b663c956460295b1dae0801ff41387ab41`, identico all'originale fornito.
- Superfici: Annuario statistico 2026 della Città metropolitana di Milano.

## Corrispondenze zona - OMI

| Comune | Zona 1 | Zona 2 | Zona 3 |
|---|---|---|---|
| Buccinasco | B1 | D1 | R1 |
| Opera | B1 | D1, R1 | — |
| Rozzano | B1 | D1 | R1, R2 |
| San Donato Milanese | B1 | D2 | R1, R2 |
| San Giuliano Milanese | B1 | E1 | R1 |
| Trezzano sul Naviglio | **D1** | **B1** | R1 |

Trezzano è l'eccezione discriminante: il numero di zona viene dal KML e dall'accordo, mai dedotto dal codice OMI.

## Canoni confermati

Valori in €/mq al mese; ogni cella è sub-fascia 1 / 2 / 3.

| Comune | Zona | Canoni |
|---|---:|---|
| Buccinasco | 1 | `7,00-8,99 / 9,00-10,99 / 11,00-13,00` |
| Buccinasco | 2 | `5,00-6,99 / 7,00-8,99 / 9,00-11,00` |
| Buccinasco | 3 | `4,00-4,99 / 5,00-6,99 / 7,00-9,00` |
| Opera | 1 | `5,00-7,99 / 8,00-10,99 / 11,00-13,50` |
| Opera | 2 | `4,00-5,29 / 5,30-7,99 / 8,00-11,00` |
| Rozzano, San Giuliano Milanese | 1 | `7,00-9,99 / 10,00-11,99 / 12,00-14,00` |
| Rozzano, San Giuliano Milanese | 2 | `5,00-6,99 / 7,00-8,99 / 9,00-11,00` |
| Rozzano, San Giuliano Milanese | 3 | `3,00-4,99 / 5,00-6,99 / 7,00-8,50` |
| San Donato Milanese | 1 | `7,00-8,99 / 9,00-11,99 / 12,00-14,00` |
| San Donato Milanese | 2 | `6,00-7,99 / 8,00-9,99 / 10,00-12,00` |
| San Donato Milanese | 3 | `4,00-5,99 / 6,00-7,99 / 8,00-10,00` |
| Trezzano sul Naviglio | 1 | `6,00-7,99 / 8,00-10,99 / 11,00-13,00` |
| Trezzano sul Naviglio | 2 | `5,00-6,99 / 7,00-8,99 / 9,00-11,00` |
| Trezzano sul Naviglio | 3 | `3,50-4,99 / 5,00-6,99 / 7,00-9,00` |

Rozzano e San Giuliano hanno valori identici ma fonti PDF distinte. Le zone rurali elencate sopra hanno canoni propri e restano calcolabili.

## Confini e geometrie

Nessuno dei sei accordi contiene una clausola locale sui confini. Le sovrapposizioni geometriche seguono esclusivamente la regola generale del §5 del brief, registrata come fonte nei manifesti; non viene attribuita agli accordi.

Le geometrie bloccate restano entro l'1,3% delle superfici ufficiali. I placemark ripetuti di Opera e San Donato sono aggregati nella stessa zona contrattuale, non scartati.

## Esito

I sei JSON hanno `canoni_confirmed: true`, nessuna zona senza canoni e registrazione completa nel selettore.
