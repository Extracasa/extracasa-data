# Verifica manuale - Obiettivo 2 Area Groane

## Fonti bloccate

- Pagina indice: Unioncasa Milano, URL in `tools/comuni_obiettivo2.json`.
- Accordo: **Accordo locale - ambito territoriale di Garbagnate Milanese**, Google Drive `1lD_-Ty2oWu8WlYyJWpytIhaErfjjisiK`, SHA-256 `57987559a29fda0606fd6385ae598c9d90687716ed20026a49800d4381096909`.
- Zone e corrispondenze OMI: pagina PDF 4.
- Tabelle dei canoni: pagine PDF 17-18, lasciate intenzionalmente **DA CONFERMARE**.
- Superfici: Annuario statistico 2026 della Città metropolitana di Milano.
- Regola di confine: pagina PDF 4; l'edificio attraversato dal confine appartiene alla zona di maggior valore. In questa preparazione si conserva l'ordine contrattuale 1, 2, 3; la conferma dei canoni resta un blocco prima dell'integrazione.

## Baranzate

- Mappa: KML con OMI `D1 -> zona 1`, `B1 -> zona 2`.
- Canoni: pagina 17, **[DA CONFERMARE - nessun valore trascritto]**.
- Geometria: 2,776 km² contro 2,78 ufficiali (-0,1%); 2 poligoni; 1 campione multi-zona risolto dall'ordine contrattuale.
- Nota: è l'unico KML del gruppo che espone codici OMI anziché etichette di zona contrattuale.

## Bollate

- Mappa: KML diretto `Z1 -> zona 1`, `Z2 -> zona 2`; pagina 4: zona 1 = OMI B1, zona 2 = OMI D1/C1.
- Canoni: pagina 17, **[DA CONFERMARE - nessun valore trascritto]**.
- Geometria: 13,096 km² contro 13,12 ufficiali (-0,2%); 6 poligoni; 3 campioni multi-zona risolti dall'ordine contrattuale.

## Cesate

- Mappa: KML diretto `Z1 -> zona 1`, `Z2 -> zona 2`; pagina 4: zona 1 = OMI B1, zona 2 = OMI R1.
- Canoni: pagina 17, **[DA CONFERMARE - nessun valore trascritto]**.
- Geometria: 5,680 km² contro 5,77 ufficiali (-1,6%); 3 poligoni; 1 campione multi-zona risolto dall'ordine contrattuale.
- Nota: R1 è esplicitamente associata alla zona contrattuale 2 e quindi non è classificata come area senza canoni.

## Garbagnate Milanese

- Mappa: KML diretto `Z1 -> zona 1`, `Z2 -> zona 2`; pagina 4: zona 1 = OMI B1, zona 2 = OMI D1.
- Canoni: pagina 17, **[DA CONFERMARE - nessun valore trascritto]**.
- Geometria: 8,859 km² contro 9,00 ufficiali (-1,6%); 2 poligoni; nessun campione multi-zona.

## Novate Milanese

- Mappa: KML diretto `Z1 -> zona 1`, `Z2 -> zona 2`; pagina 4: zona 1 = OMI B1, zona 2 = OMI D1.
- Canoni: pagina 18, **[DA CONFERMARE - nessun valore trascritto]**.
- Geometria: 5,455 km² contro 5,46 ufficiali (-0,1%); 2 poligoni; nessun campione multi-zona.

## Paderno Dugnano

- Mappa: KML diretto `Z1 -> zona 1`, `Z2 -> zona 2`; pagina 4: zona 1 = OMI B1, zona 2 = OMI D1.
- Canoni: pagina 18, **[DA CONFERMARE - nessun valore trascritto]**.
- Geometria: 14,088 km² contro 14,11 ufficiali (-0,2%); 2 poligoni; nessun campione multi-zona.

## Senago

- Mappa: KML diretto `Z1 -> zona 1`, `Z2 -> zona 2`, `Z3 -> zona 3`; pagina 4: zona 1 = OMI B1, zona 2 = OMI D1, zona 3 = OMI R1/R2.
- Canoni: pagina 18, **[DA CONFERMARE - nessun valore trascritto]**.
- Geometria: 8,608 km² contro 8,60 ufficiali (+0,1%); 22 poligoni; 3 campioni multi-zona risolti dall'ordine contrattuale.
- Nota: i placemark ripetuti Z2/Z3 vengono aggregati, incluse le isole e le cavità interne.

## Esclusioni e blocco finale

- **Solaro è escluso**, anche se compare nell'accordo comune e nella pagina 18.
- Nessun Comune di Monza e Brianza, Abbiategrasso o Solaro è incluso.
- I sette JSON hanno `canoni: {}`; non sono registrati nel selettore. L'integrazione nel motore è bloccata fino alla conferma umana dei valori.
