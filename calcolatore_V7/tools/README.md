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

I canoni delle pagine 17-18 sono stati confermati riga per riga nel file `VERIFICA_obiettivo2_groane_COMPILATA.md` (SHA-256 `91184b1b854ebf725a4f398a7122fc039445117f47af27033b2e517780a14461`). Gli otto Comuni hanno `canoni_confirmed: true` e sono registrati nel selettore.

## Obiettivo 3 - Area Rhodense

Il manifesto `comuni_obiettivo3.json` genera nove Comuni. I canoni delle pagine 33, 35 e 37 sono stati confermati riga per riga nel file `VERIFICA_obiettivo3_rhodense_COMPILATA.md` (SHA-256 `167fe15a8e82f48ac1b9e5c73e458ffe70c68fd4e7b34e1357301fb5a9e72ea2`).

Arese mantiene un'avvertenza fail-closed: l'accordo associa R1 alla zona 2, ma il KML non espone il relativo perimetro e copre il 6,5% in meno della superficie ufficiale. Il simulatore non inventa la geometria mancante; gli indirizzi fuori dai poligoni ufficiali restano non coperti.
