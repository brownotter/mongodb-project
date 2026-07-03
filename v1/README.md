# Inicijalna šema baze podataka

Inicijalna šema baze podataka prati strukturu originalnog skupa podataka o pomorskom saobraćaju (AIS podaci). <br>
Podaci su organizovani u četiri glavne kolekcije: `positions`, `vessels`, `ports` i `vessel_types`. <br>
Kolekcije possition i vessels su dobijene iz AIS skupa podataka ports iz skupa podataka o lukama i vessel_types je ručno dodata. 

## Kolekcija `vessels`

Sadrži statičke informacije o brodovima.

- `_id` – MMSI identifikator broda  
- `MMSI` – jedinstveni identifikator broda  
- `IMO` – IMO broj broda  
- `CallSign` – pozivni znak broda  
- `VesselName` – naziv broda  
- `VesselType` – šifra tipa broda  
- `TransceiverClass` – AIS klasa uređaja  

**Vessel dimension:**
- `dimensions.Length` – dužina broda (m)  
- `dimensions.Width` – širina broda (m)  
- `dimensions.Draft` – gaz broda (m)  

## Kolekcija `positions`

Sadrži podatke o kretanju brodova kroz vreme.

- `_id` – identifikator dokumenta  
- `MMSI` – identifikator broda  
- `BaseDateTime` – vreme merenja pozicije  
- `position` – GeoJSON koordinata broda  
- `kinematics.SOG` – brzina (čvorovi)  
- `kinematics.SOG_kmh` – brzina (km/h)  
- `kinematics.COG` – kurs kretanja  
- `kinematics.Heading` – pravac broda  
- `kinematics.Speed_Category` – kategorija brzine (Stopped, Slow, Moving)  
- `Status` – status broda  
- `Cargo` – šifra tereta  

**Destination:**
- `destination.cluster_id` – destinacioni klaster  
- `destination.dest_lat` – širina destinacije  
- `destination.dest_lon` – dužina destinacije  
- `destination.dist_km` – udaljenost do destinacije  
- `destination.ETA_hours` – procenjeno vreme dolaska  


## Kolekcija `ports`

Sadrži informacije o lukama širom sveta.

- `_id` – identifikator luke  
- `name` – naziv luke  
- `alternate_name` – alternativni naziv  
- `country` – država  
- `region` – region  
- `water_body` – vodeno područje  

**LLocation:**
- `location` – koordinata luke  

**Harbor:**
- `harbor.size` – veličina luke  
- `harbor.type` – tip luke  
- `harbor.use` – namena  
- `harbor.shelter` – zaštita luke  

**Depths:**
- `depths.channel_m` – dubina kanala  
- `depths.anchorage_m` – dubina sidrišta  
- `depths.cargo_pier_m` – dubina pristaništa  
- `depths.oil_terminal_m` – dubina terminala  

## Kolekcija `vessel_types`

Tabela tipova brodova.

- `_id` – šifra tipa broda  
- `name` – naziv tipa broda  
- `category` – kategorija (Cargo, Service, Tanker, itd.)
