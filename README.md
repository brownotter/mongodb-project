# Projekat iz predmeta Sistemi baze podataka

**Tema**  Analiza pomorskog saobraćaja</td>

***Autori:*** Anđela Petković IN 55/2021 i Mirjana Todorović IN 57/2021


#### Opis skupa podataka

Za projekat su korištena su dva skupa podataka:
- [Skup podataka o kretanju pomorskog saobraćja](https://www.kaggle.com/datasets/satyamrajput7913/ais-ship-tracking-vessel-dynamics-and-eta-data/data) <br> Skup sadrži podatke prikupljene putem AIS (Automatic Identification System) sistema, koji omogućava praćenje pozicije i kretanja brodova u realnom vremenu. Podaci su organizovani u CSV datoteci koja sadrži 1098966 zapisa. Svaki zapis predstavlja jednu AIS poruku, odnosno stanje određenog broda u konkretnom vremenskom trenutku.
- [Skup podataka o lukama](https://www.kaggle.com/datasets/mexwell/world-port-index/data) <br> Skup podataka sadrži podatke o lukama širom sveta. Podaci su organizovani u CSV fajl i jedan zapis sadrži karkateristike jedne luke kao što su: naziv luke, region, zemlju, geografske koordinate, dubine (kanal, sidrište, terminali), maksimalne dimenzije brodova, usluge i infrastrukturu luke.
- Dodatno je ubačen skup podataka o tipovima brodova koji opisuje tip broda i kategoriju. Podaci su preuzeti sa [sajta](https://datadocked.com/vessel-types).

## Rezultati 

#### Šeme baze podataka

Za potrebe projekta kreirane su dve šeme baze podataka. Druga šema je kreirana sa ciljem optimizacije upita.

Za upis podataka iz skupa podataka u bazu korištene su python skripte, koje se nalaze u [import_scripts](./import_scripts).
Takođe, za unos podatka o tipovima brodova je napravljena posebna phython skripta.

Druga šema baze podataka kreirana je transformacijom prve šeme uz dodavanje indeksa.

#### Upiti
Analiza je sprovedena kroz 2 uloge sa po 5 upita. <br> <br>
Upiti za menadžera luke:
1. Koji tipovi brodova imaju najduže procenjeno vreme dolaska (ETA)? 
2. Koji brodovi su zaustavljeni i u blizini kojih luka? 
3. Koji tipovi tereta dominiraju na destinacijama i koji je prosečan gaz? 
4. Za svaku luku, koji tipovi brodova najčešće pristaju i koliki je njihov prosečan gaz u odnosu na dubinu kanala luke? 
5. Koliki je prosečan broj brodova po tipu koji su istovremeno na putu ka istoj luci?

Upiti za analitičara pomorskog saobraćaja: <br><br>

Detalji implementacij su dostupni u folderu: 

#### Performanse

Procena performansi izvršena je pomoću metode <code>explain("executionStats")</code> u MongoDB. Na graficima je prikazano izmereno vreme izvršavanja upita nad prvom i drugom verzijom baze, kao i broj dokumenata na ulazu u upit.
