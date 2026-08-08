# Scheda di verifica - Obiettivo 5 Est

I valori economici non sono stati trascritti e restano da confermare ai sensi del §3.

## Peschiera Borromeo

Accordo: **Accordo locale per il Comune di Peschiera Borromeo 2024** · PDF pag. 4 zone · pag. 17 canoni

| | Voce | Valore letto | CORREZIONE |
|---|---|---|---|
| [ ] | Numero di zone | 3 | |
| [ ] | Zona 1 | OMI D1 | |
| [ ] | Zona 2 | OMI B1 | |
| [ ] | Zona 3 | OMI D2 | |

| | Zona | Sub-fascia 1 | Sub-fascia 2 | Sub-fascia 3 | CORREZIONE |
|---|---|---|---|---|---|
| [ ] | 1 | [DA CONFERMARE] | [DA CONFERMARE] | [DA CONFERMARE] | |
| [ ] | 2 | [DA CONFERMARE] | [DA CONFERMARE] | [DA CONFERMARE] | |
| [ ] | 3 | [DA CONFERMARE] | [DA CONFERMARE] | [DA CONFERMARE] | |

Anomalie riscontrate: KML diretto con 6 poligoni; 4 campioni multi-zona risolti dall'ordine previsto dal §5. Geometria 23,454 km² contro 23,22 ufficiali (+1,0%).

## Pioltello

Accordo: **Accordo locale per il Comune di Pioltello 2024** · PDF pag. 3 zone · pag. 17 canoni

| | Voce | Valore letto | CORREZIONE |
|---|---|---|---|
| [ ] | Numero di zone | 2 | |
| [ ] | Zona 1 | OMI B1 e D1 | |
| [ ] | Zona 2 | OMI R1 e R2 | |
| [ ] | OMI D4 | omessa dal testo; nel KML ha lo stesso stile di R1/R2 | **PROPOSTA: zona 2, DA CONFERMARE** |

| | Zona | Sub-fascia 1 | Sub-fascia 2 | Sub-fascia 3 | CORREZIONE |
|---|---|---|---|---|---|
| [ ] | 1 | [DA CONFERMARE] | [DA CONFERMARE] | [DA CONFERMARE] | |
| [ ] | 2 | [DA CONFERMARE] | [DA CONFERMARE] | [DA CONFERMARE] | |

Anomalie riscontrate: il PDF non cita D4. Il manifesto la associa provvisoriamente alla zona 2 perché il KML raggruppa con stile identico `D4/R1/R2`, distinto da `B1/D1`; il generatore verifica questa relazione e fallisce se i colori cambiano. Geometria 13,185 km² contro 13,09 ufficiali (+0,7%).

## Segrate

Accordo: **Accordo locale per il Comune di Segrate 2024** · PDF pag. 3 zone · pag. 17 canoni

| | Voce | Valore letto | CORREZIONE |
|---|---|---|---|
| [ ] | Numero di zone | 3 | |
| [ ] | Zona 1 | OMI E1 ed E2 | |
| [ ] | Zona 2 | OMI B1 e C1 | |
| [ ] | Zona 3 | OMI D1 | |
| [ ] | OMI R1 | omessa dal testo; nel KML ha lo stesso stile di B1/C1 | **PROPOSTA: zona 2, DA CONFERMARE** |

| | Zona | Sub-fascia 1 | Sub-fascia 2 | Sub-fascia 3 | CORREZIONE |
|---|---|---|---|---|---|
| [ ] | 1 | [DA CONFERMARE] | [DA CONFERMARE] | [DA CONFERMARE] | |
| [ ] | 2 | [DA CONFERMARE] | [DA CONFERMARE] | [DA CONFERMARE] | |
| [ ] | 3 | [DA CONFERMARE] | [DA CONFERMARE] | [DA CONFERMARE] | |

Anomalie riscontrate: il PDF non cita R1. Il manifesto la associa provvisoriamente alla zona 2 perché il KML raggruppa con stile identico `R1/B1/C1`, distinto da `E1/E2` e `D1`; il generatore verifica i tre gruppi. Sono presenti 9 poligoni e 7 campioni multi-zona. Geometria 17,427 km² contro 17,49 ufficiali (-0,4%).

## Vimodrone

Accordo: **Accordo locale per il Comune di Vimodrone 2024** · PDF pag. 3 zone · pag. 15 canoni

| | Voce | Valore letto | CORREZIONE |
|---|---|---|---|
| [ ] | Numero di zone | 2 | |
| [ ] | Zona 1 | OMI B1 | |
| [ ] | Zona 2 | OMI D1 | |

| | Zona | Sub-fascia 1 | Sub-fascia 2 | Sub-fascia 3 | CORREZIONE |
|---|---|---|---|---|---|
| [ ] | 1 | [DA CONFERMARE] | [DA CONFERMARE] | [DA CONFERMARE] | |
| [ ] | 2 | [DA CONFERMARE] | [DA CONFERMARE] | [DA CONFERMARE] | |

Anomalie riscontrate: KML diretto; 2 campioni multi-zona risolti dall'ordine previsto dal §5. Geometria 4,782 km² contro 4,74 ufficiali (+0,9%).

## Blocco §3

Tutti i quattro JSON hanno `canoni: {}` e non sono registrati nel selettore. Nessun Comune supera tre zone contrattuali, quindi `ZONE_COLORS` non richiede estensioni. Le due proposte D4/R1 devono essere confermate insieme ai canoni prima di qualunque integrazione runtime.
