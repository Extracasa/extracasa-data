# Verifica finale - Obiettivo 6 completamento

## Perimetro e fonti

- Otto accordi comunali distinti, con hash PDF bloccati in `tools/comuni_obiettivo6.json`.
- Zone e corrispondenze OMI: pagina PDF 3.
- Tabelle dei canoni: pagine PDF 14, 15 o 17.
- Conferma umana: `VERIFICA_obiettivo6_completamento_COMPILATA.md`, SHA-256 dei byte versionati `6d9931cc9791d615a6b66623b959d304c96bb9757e33e84ee4b0951d6afba868`; SHA-256 dell'originale fornito `6ca36919396e1088f6bebcf5e770d03d725ddb6f7d9fd143551c9cea9050401d`, che contiene una riga vuota finale rimossa nella copia versionata.
- Superfici: Annuario statistico 2026 della Città metropolitana di Milano.
- Noviglio è escluso per decisione esplicita: non compare nel manifesto finale, nel selettore o nei dataset pubblicabili.

## Corrispondenze zona - OMI

| Comune | Zona 1 | Zona 2 | Zona 3 |
|---|---|---|---|
| Cassano d'Adda | B1 | D1 | R1 |
| Cernusco sul Naviglio | B1 | D1 | R1 |
| Gorgonzola | B1 | D1 | R1, R2 |
| Legnano | B1 | C1 | D1, D2 |
| Melzo | B1 | R1 | — |
| Nerviano | B1 | D1 | R1 |
| Parabiago | B1 | D1 | R1, D2 |
| Rescaldina | B1 | D1 | R1 |

Legnano non ha zone R; Melzo non ha una zona D. Tutte le zone R presenti negli altri accordi hanno canoni propri.

## Canoni confermati

Valori in €/mq al mese; ogni cella è sub-fascia 1 / 2 / 3.

| Comune | Zona | Canoni |
|---|---:|---|
| Cassano d'Adda | 1 | `5,00-6,49 / 6,50-7,99 / 8,00-10,00` |
| Cassano d'Adda | 2 | `4,00-5,49 / 5,50-6,99 / 7,00-8,50` |
| Cassano d'Adda | 3 | `3,00-4,49 / 4,50-5,99 / 6,00-7,50` |
| Cernusco sul Naviglio, Gorgonzola | 1 | `7,00-9,99 / 10,00-12,99 / 13,00-15,00` |
| Cernusco sul Naviglio, Gorgonzola | 2 | `6,00-8,49 / 8,50-10,99 / 11,00-13,00` |
| Cernusco sul Naviglio, Gorgonzola | 3 | `3,00-5,99 / 6,00-7,49 / 7,50-9,00` |
| Legnano | 1 | `6,00-7,99 / 8,00-9,99 / 10,00-12,00` |
| Legnano | 2 | `4,00-6,49 / 6,50-7,99 / 8,00-10,00` |
| Legnano | 3 | `3,00-5,99 / 6,00-7,49 / 7,50-9,00` |
| Melzo | 1 | `4,50-6,99 / 7,00-8,99 / 9,00-10,50` |
| Melzo | 2 | `3,00-4,99 / 5,00-6,99 / 7,00-9,00` |
| Nerviano, Parabiago | 1 | `4,00-5,99 / 6,00-7,99 / 8,00-10,00` |
| Nerviano, Parabiago | 2 | `3,50-4,99 / 5,00-6,49 / 6,50-8,50` |
| Nerviano, Parabiago | 3 | `3,00-4,00 / 4,01-5,50 / 5,51-6,80` |
| Rescaldina | 1 | `5,00-6,99 / 7,00-8,99 / 9,00-11,00` |
| Rescaldina | 2 | `4,50-5,99 / 6,00-7,49 / 7,50-9,50` |
| Rescaldina | 3 | `3,50-5,00 / 5,01-6,50 / 6,51-7,80` |

Le soglie `4,00→4,01→5,51` e `5,00→5,01→6,51` sono trascrizioni confermate, non normalizzazioni automatiche.

## Geometrie e confini

Le geometrie bloccate coprono 18,534 km² a Cassano, 13,298 a Cernusco, 10,667 a Gorgonzola, 17,687 a Legnano, 9,657 a Melzo, 13,437 a Nerviano, 14,222 a Parabiago e 8,191 a Rescaldina. Gli scarti dalle superfici ufficiali restano entro il 2,0%.

A Melzo il controllo geometrico esatto rileva una sovrapposizione tra Z1/zona 1 e Z2/zona 2 intorno a `45.509460, 9.432986`; l'esito è risolto deterministicamente dall'ordine contrattuale dichiarato nel manifesto.

Nessuno degli otto accordi contiene una clausola locale sui confini. Le sovrapposizioni seguono soltanto la regola generale del §5 del brief, dichiarata come fonte nei manifesti.

## Esito complessivo

Gli otto JSON hanno `canoni_confirmed: true`, nessuna zona senza canoni e registrazione completa nel selettore. Il perimetro finale è di 40 nuovi Comuni, più Milano e Sesto San Giovanni: 42 Comuni complessivi.
