# Generazione dati - Obiettivo 1

Genera e valida i dati per Bresso, Cormano, Cusano Milanino, Cinisello Balsamo e Cologno Monzese.

## Fonti e riproducibilità

- Pagina accordi e mappe: Unioncasa Milano, URL nel manifesto.
- Superfici comunali: Annuario statistico 2026 della Città metropolitana di Milano, URL nel manifesto.
- Gli SHA-256 canonici delle geometrie KML e gli SHA-256 byte-per-byte dei PDF sono bloccati nei manifesti. L'hash KML ignora la riserializzazione XML e gli ID stile variabili, ma cambia se cambiano codici, anelli o coordinate usati dal simulatore.
- I canoni sono esclusivamente quelli confermati per l'Obiettivo 1; il generatore non li estrae né li inferisce dai PDF.

```powershell
python calcolatore_V7/tools/genera_comuni.py --source-dir <cartella-fonti> --download
python calcolatore_V7/tools/genera_comuni.py --source-dir <cartella-fonti> --check
```

La cartella delle fonti contiene KML e PDF ufficiali. Il controllo verifica entrambi gli hash, codici OMI, colori KML effettivi (risolvendo anche gli `StyleMap`), coordinate, chiusura degli anelli, ordine dei canoni, superficie comunale, intersezioni geometriche fra poligoni e rigenerabilità byte per byte. La griglia resta soltanto una statistica: non decide se una sovrapposizione esiste. La superficie ha una tolleranza predefinita del 2%; ogni eccezione deve essere dichiarata nel manifesto. Con `--download`, anche un PDF già in cache viene riscaricato e verificato prima di sostituire la copia locale.

## Confini sovrapposti

- Bresso: sul limite B1/D1 prevale la zona 1 di maggior pregio, come richiesto dal §5 del brief.
- Cormano: B1 e D1 ricadono nella stessa zona contrattuale 1.
- Cusano Milanino: il PDF ufficiale, pagina 13, assegna gli edifici sul confine alla zona di maggior valore; la zona 1 precede la zona 2.
- Cinisello Balsamo: nelle sovrapposizioni con R1 prevale l'esito rurale non calcolabile (§5.3 del brief); fra B1 e D1 prevale la zona 1.
- Cologno Monzese: le sovrapposizioni applicano la regola ufficiale “rurale prima, poi zona di maggior valore”. Il report Doki Casa del 08/08/2026 per Via G. Pascoli 23, superficie 55 mq, restituisce un minimo mensile di 220 euro: `55 x 4,00`, quindi discrimina il canone D1/zona 2 rispetto ai 330 euro di B2/zona 1. Il report è registrato come `rent_oracle` con portata `rent_only`: non contiene coordinate né una geometria verificabile e quindi non determina il confine o la precedenza dei poligoni.

Le aree R1 restano separate in `zone_senza_canoni`: non sono rese calcolabili.

## Obiettivo 2 - Area Groane

Il manifesto `comuni_obiettivo2.json` genera Baranzate, Bollate, Cesate, Garbagnate Milanese, Novate Milanese, Paderno Dugnano, Senago e Solaro. Solaro è stato recuperato dopo la conferma umana della sua tabella a pagina 18 dell'accordo Groane e della mappa ufficiale a due zone.

```powershell
python calcolatore_V7/tools/genera_comuni.py --manifest calcolatore_V7/tools/comuni_obiettivo2.json --source-dir <cartella-kml>
python calcolatore_V7/tools/genera_comuni.py --manifest calcolatore_V7/tools/comuni_obiettivo2.json --source-dir <cartella-kml> --check
```

I KML di sette Comuni espongono direttamente le zone contrattuali; Baranzate espone i codici OMI. La pagina 4 dell'accordo assegna gli edifici attraversati da un confine alla zona di maggior valore: il dataset conserva l'ordine contrattuale crescente e dichiara `agreement_zone_order`.

I canoni delle pagine 17-18 sono stati confermati riga per riga nel file `VERIFICA_obiettivo2_groane_COMPILATA.md` (SHA-256 `91184b1b854ebf725a4f398a7122fc039445117f47af27033b2e517780a14461`). Gli otto Comuni hanno `canoni_confirmed: true` e sono registrati nel selettore.

## Obiettivo 3 - Area Rhodense

Il manifesto `comuni_obiettivo3.json` genera nove Comuni. I canoni delle pagine 33, 35 e 37 sono stati confermati riga per riga nel file `VERIFICA_obiettivo3_rhodense_COMPILATA.md` (SHA-256 `167fe15a8e82f48ac1b9e5c73e458ffe70c68fd4e7b34e1357301fb5a9e72ea2`).

```powershell
python calcolatore_V7/tools/genera_comuni.py --manifest calcolatore_V7/tools/comuni_obiettivo3.json --source-dir <cartella-kml>
python calcolatore_V7/tools/genera_comuni.py --manifest calcolatore_V7/tools/comuni_obiettivo3.json --source-dir <cartella-kml> --check
```

Le geometrie correnti misurano uno scostamento di -6,5% per Arese e -3,5% per Pregnana Milanese rispetto alla superficie amministrativa. Le due tolleranze sono dichiarate esplicitamente nel manifesto (7% e 4%); tutti gli altri Comuni conservano il limite predefinito del 2%. La tolleranza segnala una differenza di copertura, non la interpreta come prova che il confine KML coincida con quello amministrativo.

Arese mantiene un'avvertenza fail-closed: l'accordo associa R1 alla zona 2, ma il KML non espone il relativo perimetro. Il simulatore non inventa la geometria mancante; gli indirizzi fuori dai poligoni ufficiali restano non coperti.

## Obiettivo 4 - Area Sud

Il manifesto `comuni_obiettivo4.json` genera Buccinasco, Opera, Rozzano, San Donato Milanese, San Giuliano Milanese e Trezzano sul Naviglio. I canoni e le corrispondenze OMI sono stati confermati nel file `VERIFICA_obiettivo4_sud_COMPILATA.md` (SHA-256 `8adaec3d6f5799396293d34a06a156b663c956460295b1dae0801ff41387ab41`).

Trezzano è deliberatamente modellata dal numero di zona del KML e dall'art. 4.1.a: zona 1 = D1, zona 2 = B1 e zona 3 = R1. La corrispondenza è dichiarata in `omi_code_map`, validata dal generatore e usata solo per esporre il codice corretto; nessuna zona viene dedotta per convenzione dal codice OMI. Le zone R1/R2 dei sei Comuni hanno canoni propri e non entrano in `zone_senza_canoni`.

I sei accordi non contengono una clausola locale sui confini. Le eventuali sovrapposizioni seguono la regola generale del §5 del brief, dichiarata esplicitamente come fonte nei manifesti.

## Obiettivo 5 - Area Est

Il manifesto `comuni_obiettivo5.json` genera Peschiera Borromeo, Pioltello, Segrate e Vimodrone. I canoni e le corrispondenze zona-OMI sono stati confermati nel file `VERIFICA_obiettivo5_est_COMPILATA.md` (SHA-256 `80ae0a26e022b3e48419bcb4c9b33c7e9fe4e9859946f8dc1ca431dfb450781a`).

Pioltello associa D4 alla zona 2 e Segrate associa R1 alla zona 2. Per questi due codici omessi dal testo, la cartografia ufficiale fornisce la corrispondenza tramite il gruppo colore; ogni `style_group` include il colore effettivo atteso e fa fallire la generazione se uno `StyleMap` cambia colore, se i raggruppamenti contraddicono l'accordo o se cambiano struttura.

Peschiera e Segrate confermano che B1 non implica zona 1: il numero di zona viene sempre dal KML o dall'art. 4.1.a, mai dalla famiglia OMI.

## Obiettivo 6 - Completamento

Il manifesto `comuni_obiettivo6.json` genera Cassano d'Adda, Cernusco sul Naviglio, Gorgonzola, Legnano, Melzo, Nerviano, Parabiago e Rescaldina. Noviglio non appartiene al perimetro finale e il relativo dataset preparatorio è stato rimosso; Solaro è collocato nell'area Groane.

I canoni sono stati confermati nel file `VERIFICA_obiettivo6_completamento_COMPILATA.md` (SHA-256 `6ca36919396e1088f6bebcf5e770d03d725ddb6f7d9fd143551c9cea9050401d`). Le soglie non standard delle zone 3 sono conservate esattamente: `4,00→4,01→5,51` per Nerviano/Parabiago e `5,00→5,01→6,51` per Rescaldina. Rescaldina dichiara inoltre una tolleranza geometrica del 2,5% perché la copertura corrente misura +2,0% rispetto alla superficie amministrativa; gli altri Comuni mantengono il limite predefinito del 2%.

Con questo obiettivo il selettore contiene 40 nuovi Comuni, oltre a Milano e Sesto San Giovanni: 42 Comuni complessivi. Nessun accordo di questo gruppo contiene una clausola locale sui confini; le sovrapposizioni citano esclusivamente la regola generale del §5 del brief.
