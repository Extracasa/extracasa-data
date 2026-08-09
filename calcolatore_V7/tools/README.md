# Generazione dati - Obiettivo 1

Genera i dati per Bresso, Cormano, Cusano Milanino, Cinisello Balsamo e Cologno Monzese senza registrarli nel selettore del calcolatore.

## Fonti e riproducibilità

- Pagina accordi e mappe: Unioncasa Milano, URL nel manifesto.
- Superfici comunali: Annuario statistico 2026 della Città metropolitana di Milano, URL nel manifesto.
- Gli SHA-256 canonici delle geometrie KML e gli SHA-256 byte-per-byte dei PDF sono bloccati in `comuni_obiettivo1.json`.
- I canoni sono esclusivamente quelli confermati per l'Obiettivo 1; il generatore non li estrae né li inferisce dai PDF.

```powershell
python calcolatore_V7/tools/genera_comuni.py --source-dir <cartella-kml>
python calcolatore_V7/tools/genera_comuni.py --source-dir <cartella-kml> --check
```

Il controllo verifica hash, codici OMI, coordinate, chiusura degli anelli, ordine dei canoni, superficie comunale, sovrapposizioni esatte e rigenerabilità byte per byte. La superficie ha una tolleranza predefinita del 2%; ogni eccezione deve essere dichiarata nel manifesto. Con `--download`, anche un PDF già in cache viene riscaricato e verificato prima di sostituire la copia locale.

## Confini sovrapposti

- Cormano: B1 e D1 ricadono nella stessa zona contrattuale 1.
- Cusano Milanino: il PDF ufficiale, pagina 13, assegna gli edifici sul confine alla zona di maggior valore; la zona 1 precede la zona 2.
- Cologno Monzese: le sovrapposizioni applicano la regola ufficiale “rurale prima, poi zona di maggior valore”. Il report Doki Casa del 08/08/2026 per Via G. Pascoli 23, superficie 55 mq, restituisce un minimo mensile di 220 euro: `55 x 4,00`, quindi discrimina il canone D1/zona 2 rispetto ai 330 euro di B2/zona 1. Il report è registrato come `rent_oracle` con portata `rent_only`: non contiene coordinate né una geometria verificabile e quindi non determina il confine o la precedenza dei poligoni.

Le aree R1 restano separate in `zone_senza_canoni`: non sono rese calcolabili.

## Obiettivo 2 - Area Groane

Il manifesto `comuni_obiettivo2.json` prepara Baranzate, Bollate, Cesate, Garbagnate Milanese, Novate Milanese, Paderno Dugnano, Senago e Solaro. Solaro è stato aggiunto nella fase di completamento per chiudere il perimetro dei 40 nuovi Comuni.

```powershell
python calcolatore_V7/tools/genera_comuni.py --manifest calcolatore_V7/tools/comuni_obiettivo2.json --source-dir <cartella-kml>
python calcolatore_V7/tools/genera_comuni.py --manifest calcolatore_V7/tools/comuni_obiettivo2.json --source-dir <cartella-kml> --check
```

I KML di sette Comuni espongono direttamente le zone contrattuali; Baranzate espone i codici OMI. La pagina 4 dell'accordo assegna gli edifici attraversati da un confine alla zona di maggior valore: il dataset conserva l'ordine contrattuale crescente e dichiara `agreement_zone_order`.

Come richiesto per la fase di preparazione, tutti i `canoni` sono `{}` e `canoni_confirmed` è `false`. I dati non vengono registrati nel selettore e non sono utilizzabili dal motore finché i valori non saranno confermati da una persona.

## Obiettivo 3 - Area Rhodense

Il manifesto `comuni_obiettivo3.json` prepara Arese, Cornaredo, Lainate, Pero, Pogliano Milanese, Pregnana Milanese, Rho, Settimo Milanese e Vanzago. Il PDF condiviso dell'accordo viene verificato prima dei KML.

```powershell
python calcolatore_V7/tools/genera_comuni.py --manifest calcolatore_V7/tools/comuni_obiettivo3.json --source-dir <cartella-kml>
python calcolatore_V7/tools/genera_comuni.py --manifest calcolatore_V7/tools/comuni_obiettivo3.json --source-dir <cartella-kml> --check
```

Le geometrie correnti misurano uno scostamento di -6,5% per Arese e -3,5% per Pregnana Milanese rispetto alla superficie amministrativa. Le due tolleranze sono dichiarate esplicitamente nel manifesto (7% e 4%); tutti gli altri Comuni conservano il limite predefinito del 2%. La tolleranza segnala una differenza di copertura, non la interpreta come prova che il confine KML coincida con quello amministrativo.

Anche in questa fase i `canoni` restano `{}` e `canoni_confirmed` è `false`: i dataset sono preparatori e non vengono registrati nel selettore.

## Obiettivo 6 - Completamento

Il manifesto `comuni_obiettivo6.json` prepara Cassano d'Adda, Cernusco sul Naviglio, Gorgonzola, Legnano, Melzo, Nerviano, Parabiago e Rescaldina. Noviglio non appartiene al perimetro finale; Solaro è collocato nell'area Groane. Con i manifesti 1-6 risultano quindi 40 nuovi Comuni, oltre a Milano e Sesto San Giovanni. Rescaldina dichiara una tolleranza del 2,5% perché la geometria corrente misura +2,0% rispetto alla superficie amministrativa; gli altri Comuni del gruppo mantengono il limite predefinito del 2%.
