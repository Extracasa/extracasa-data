# Generazione dati - Obiettivo 1

Genera e valida i dati per Bresso, Cormano, Cusano Milanino, Cinisello Balsamo e Cologno Monzese.

## Fonti e riproducibilità

- Pagina accordi e mappe: Unioncasa Milano, URL nel manifesto.
- Superfici comunali: Annuario statistico 2026 della Città metropolitana di Milano, URL nel manifesto.
- Gli SHA-256 canonici delle geometrie KML e gli SHA-256 dei PDF scaricati sono bloccati in `comuni_obiettivo1.json`. L'hash KML ignora la riserializzazione XML e gli ID stile variabili, ma cambia se cambiano codici, anelli o coordinate usati dal simulatore.
- I canoni sono esclusivamente quelli confermati per l'Obiettivo 1; il generatore non li estrae né li inferisce dai PDF.

```powershell
python calcolatore_V7/tools/genera_comuni.py --source-dir <cartella-fonti> --download
python calcolatore_V7/tools/genera_comuni.py --source-dir <cartella-fonti> --check
```

La cartella delle fonti contiene KML e PDF ufficiali. Il controllo verifica entrambi gli hash, codici OMI, colori KML effettivi (risolvendo anche gli `StyleMap`), coordinate, chiusura degli anelli, ordine dei canoni, superficie comunale, intersezioni geometriche fra poligoni e rigenerabilità byte per byte. La griglia resta soltanto una statistica: non è il criterio che decide se una sovrapposizione esiste.

## Confini sovrapposti

- Bresso: sul limite B1/D1 prevale la zona 1 di maggior pregio, come richiesto dal §5 del brief.
- Cormano: B1 e D1 ricadono nella stessa zona contrattuale 1.
- Cusano Milanino: il PDF ufficiale, pagina 13, assegna gli edifici sul confine alla zona di maggior valore; la zona 1 precede la zona 2.
- Cinisello Balsamo: nelle sovrapposizioni con R1 prevale l'esito rurale non calcolabile (§5.3 del brief); fra B1 e D1 prevale la zona 1.
- Cologno Monzese: un report Doki Casa del 08/08/2026 per Via G. Pascoli 23, superficie 55 mq, restituisce un minimo mensile di 220 euro: `55 x 4,00`, quindi D1/zona 2, mentre B2/zona 1 darebbe 330 euro. Questo oracolo identifica la zona economica dell'indirizzo ma non decide i confini: nelle sovrapposizioni prevale R1 non calcolabile e, fra B2 e D1, la zona 1 di maggior pregio (§5 e §5.3 del brief).

Le aree R1 restano separate in `zone_senza_canoni`: non sono rese calcolabili.

## Obiettivo 2 - Area Groane

Il manifesto `comuni_obiettivo2.json` genera Baranzate, Bollate, Cesate, Garbagnate Milanese, Novate Milanese, Paderno Dugnano, Senago e Solaro. Solaro è stato recuperato dopo la conferma umana della sua tabella a pagina 18 dell'accordo Groane e della mappa ufficiale a due zone.

```powershell
python calcolatore_V7/tools/genera_comuni.py --manifest calcolatore_V7/tools/comuni_obiettivo2.json --source-dir <cartella-kml>
python calcolatore_V7/tools/genera_comuni.py --manifest calcolatore_V7/tools/comuni_obiettivo2.json --source-dir <cartella-kml> --check
```

I KML di sette Comuni espongono direttamente le zone contrattuali; Baranzate espone i codici OMI. La pagina 4 dell'accordo assegna gli edifici attraversati da un confine alla zona di maggior valore: il dataset conserva l'ordine contrattuale crescente e dichiara `agreement_zone_order`.

I canoni delle pagine 17-18 sono stati confermati riga per riga nel file `VERIFICA_obiettivo2_groane_COMPILATA.md` (SHA-256 dei byte versionati `91184b1b854ebf725a4f398a7122fc039445117f47af27033b2e517780a14461`). Gli otto Comuni hanno `canoni_confirmed: true` e sono registrati nel selettore.

## Obiettivo 3 - Area Rhodense

Il manifesto `comuni_obiettivo3.json` genera nove Comuni. I canoni delle pagine 33, 35 e 37 sono stati confermati riga per riga nel file `VERIFICA_obiettivo3_rhodense_COMPILATA.md` (SHA-256 `167fe15a8e82f48ac1b9e5c73e458ffe70c68fd4e7b34e1357301fb5a9e72ea2`).

Arese mantiene un'avvertenza fail-closed: l'accordo associa R1 alla zona 2, ma il KML non espone il relativo perimetro e copre il 6,5% in meno della superficie ufficiale. Il simulatore non inventa la geometria mancante; gli indirizzi fuori dai poligoni ufficiali restano non coperti.

## Obiettivo 4 - Area Sud

Il manifesto `comuni_obiettivo4.json` genera Buccinasco, Opera, Rozzano, San Donato Milanese, San Giuliano Milanese e Trezzano sul Naviglio. I canoni e le corrispondenze OMI sono stati confermati nel file `VERIFICA_obiettivo4_sud_COMPILATA.md` (SHA-256 `8adaec3d6f5799396293d34a06a156b663c956460295b1dae0801ff41387ab41`).

Trezzano è deliberatamente modellata dal numero di zona del KML e dall'art. 4.1.a: zona 1 = D1, zona 2 = B1 e zona 3 = R1. `omi_code_map` conserva questi codici OMI reali separatamente dalle etichette KML Z1/Z2/Z3. Nessun codice OMI viene convertito in zona per convenzione. Per i dataset che espongono solo etichette contrattuali e dichiarano `mostra_omi: false`, il runtime non mostra né persiste uno pseudo codice OMI. Le zone R1/R2 dei sei Comuni hanno canoni propri e non entrano in `zone_senza_canoni`.

I sei accordi non contengono una clausola locale sui confini. Le eventuali sovrapposizioni seguono la regola generale del §5 del brief, dichiarata esplicitamente come fonte nei manifesti.

## Obiettivo 5 - Area Est

Il manifesto `comuni_obiettivo5.json` genera Peschiera Borromeo, Pioltello, Segrate e Vimodrone. I canoni e le corrispondenze zona-OMI sono stati confermati nel file `VERIFICA_obiettivo5_est_COMPILATA.md` (SHA-256 `80ae0a26e022b3e48419bcb4c9b33c7e9fe4e9859946f8dc1ca431dfb450781a`).

Pioltello associa D4 alla zona 2 e Segrate associa R1 alla zona 2. Per questi due codici omessi dal testo, la cartografia ufficiale fornisce la corrispondenza tramite il gruppo colore; `style_groups` blocca sia i membri sia il colore KML effettivo atteso per ogni gruppo (rosso `a05252ff`, blu `a0d18802`, giallo `a000eaff`) e fa fallire la generazione anche se due colori vengono scambiati lasciando invariata la geometria.

Peschiera e Segrate confermano che B1 non implica zona 1: il numero di zona viene sempre dal KML o dall'art. 4.1.a, mai dalla famiglia OMI.

## Obiettivo 6 - Completamento

Il manifesto `comuni_obiettivo6.json` genera Cassano d'Adda, Cernusco sul Naviglio, Gorgonzola, Legnano, Melzo, Nerviano, Parabiago e Rescaldina. Noviglio è escluso per decisione esplicita e il relativo dataset preparatorio è stato rimosso.

I canoni sono stati confermati nel file `VERIFICA_obiettivo6_completamento_COMPILATA.md` (SHA-256 dei byte versionati `6d9931cc9791d615a6b66623b959d304c96bb9757e33e84ee4b0951d6afba868`; SHA-256 dell'originale fornito `6ca36919396e1088f6bebcf5e770d03d725ddb6f7d9fd143551c9cea9050401d`, che contiene una riga vuota finale rimossa nella copia versionata). Le soglie non standard delle zone 3 sono conservate esattamente: `4,00→4,01→5,51` per Nerviano/Parabiago e `5,00→5,01→6,51` per Rescaldina.

Con questo obiettivo il selettore contiene 40 nuovi Comuni, oltre a Milano e Sesto San Giovanni: 42 Comuni complessivi. Nessun accordo di questo gruppo contiene una clausola locale sui confini; le sovrapposizioni citano esclusivamente la regola generale del §5 del brief.
