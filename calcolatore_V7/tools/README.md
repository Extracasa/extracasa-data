# Generazione dati - Obiettivo 1

Genera i dati per Bresso, Cormano, Cusano Milanino, Cinisello Balsamo e Cologno Monzese senza registrarli nel selettore del calcolatore.

## Fonti e riproducibilità

- Pagina accordi e mappe: Unioncasa Milano, URL nel manifesto.
- Superfici comunali: Annuario statistico 2026 della Città metropolitana di Milano, URL nel manifesto.
- Gli SHA-256 dei KML e dei PDF scaricati sono bloccati in `comuni_obiettivo1.json`.
- I canoni sono esclusivamente quelli confermati per l'Obiettivo 1; il generatore non li estrae né li inferisce dai PDF.

```powershell
python calcolatore_V7/tools/genera_comuni.py --source-dir <cartella-kml>
python calcolatore_V7/tools/genera_comuni.py --source-dir <cartella-kml> --check
```

Il controllo verifica hash, codici OMI, coordinate, chiusura degli anelli, ordine dei canoni, superficie comunale, sovrapposizioni e rigenerabilità byte per byte.

## Confini sovrapposti

- Cormano: B1 e D1 ricadono nella stessa zona contrattuale 1.
- Cusano Milanino: il PDF ufficiale, pagina 13, assegna gli edifici sul confine alla zona di maggior valore; la zona 1 precede la zona 2.
- Cologno Monzese: il KML contiene i placemark nell'ordine R1, B2, D1. Un report Doki Casa del 08/08/2026 per Via G. Pascoli 23, superficie 55 mq, restituisce un minimo mensile di 220 euro: `55 x 4,00`, quindi D1/zona 2, mentre B2/zona 1 darebbe 330 euro. Il file conserva l'ordine inverso di precedenza D1, B2, R1 e il generatore fallisce se ordine o oracolo non sono più discriminanti.

Le aree R1 restano separate in `zone_senza_canoni`: non sono rese calcolabili.
