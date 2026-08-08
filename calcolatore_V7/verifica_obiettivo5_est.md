# Verifica finale - Obiettivo 5 Area Est

## Fonti e conferma

- Quattro accordi comunali distinti, con hash PDF bloccati in `tools/comuni_obiettivo5.json`.
- Zone e corrispondenze OMI: art. 4.1.a, pagine PDF 3 o 4.
- Tabelle dei canoni: pagine PDF 15 o 17.
- Conferma umana: `VERIFICA_obiettivo5_est_COMPILATA.md`, SHA-256 originale `80ae0a26e022b3e48419bcb4c9b33c7e9fe4e9859946f8dc1ca431dfb450781a`.
- Superfici: Annuario statistico 2026 della Città metropolitana di Milano.

## Corrispondenze zona - OMI

| Comune | Zona 1 | Zona 2 | Zona 3 |
|---|---|---|---|
| Peschiera Borromeo | D1 | B1 | D2 |
| Pioltello | B1, D1 | R1, R2, **D4** | — |
| Segrate | E1, E2 | B1, C1, **R1** | D1 |
| Vimodrone | B1 | D1 | — |

Peschiera e Segrate sono casi discriminanti: B1 non è zona 1. Il numero viene dalla cartografia e dall'accordo, mai dal codice OMI.

## Canoni confermati

Valori in €/mq al mese; ogni cella è sub-fascia 1 / 2 / 3.

| Comune | Zona | Canoni |
|---|---:|---|
| Peschiera Borromeo | 1 | `6,00-7,99 / 8,00-9,99 / 10,00-12,00` |
| Peschiera Borromeo | 2 | `5,00-5,99 / 6,00-7,99 / 8,00-9,50` |
| Peschiera Borromeo | 3 | `4,00-4,99 / 5,00-6,99 / 7,00-8,00` |
| Pioltello | 1 | `6,00-7,99 / 8,00-9,99 / 10,00-12,50` |
| Pioltello | 2 | `4,00-6,49 / 6,50-7,99 / 8,00-10,00` |
| Segrate | 1 | `7,00-11,99 / 12,00-13,99 / 14,00-16,00` |
| Segrate | 2 | `5,00-8,99 / 9,00-10,99 / 11,00-13,00` |
| Segrate | 3 | `3,00-5,99 / 6,00-7,99 / 8,00-10,00` |
| Vimodrone | 1 | `7,00-8,99 / 9,00-11,99 / 12,00-14,00` |
| Vimodrone | 2 | `6,00-7,99 / 8,00-9,99 / 10,00-12,00` |

## D4 di Pioltello e R1 di Segrate

L'accordo non nomina D4 e R1, ma la legenda della cartografia ufficiale assegna i gruppi colore alle zone. Il manifesto registra:

- Pioltello: `[B1,D1]` zona 1; `[D4,R1,R2]` zona 2.
- Segrate: `[E1,E2]` zona 1; `[B1,C1,R1]` zona 2; `[D1]` zona 3.

Il generatore verifica che ogni gruppo condivida lo stesso colore, che gruppi distinti abbiano colori distinti e che ogni codice sia coperto. Qualunque variazione strutturale fa fallire la build.

## Geometrie e confini

Le geometrie bloccate coprono 23,454 km² a Peschiera (+1,0%), 13,185 km² a Pioltello (+0,7%), 17,427 km² a Segrate (-0,4%) e 4,782 km² a Vimodrone (+0,9%).

Nessuno dei quattro accordi contiene una clausola locale sui confini. Le eventuali sovrapposizioni seguono solo la regola generale del §5 del brief, registrata come fonte nei manifesti.

## Esito

I quattro JSON hanno `canoni_confirmed: true`, nessuna zona senza canoni e registrazione completa nel selettore.
