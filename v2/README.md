# Rekonstrukcija šeme baze podataka

## Inicijalna šema

Originalni skup podataka je bio podeljen u 4 kolekcije:
- `positions` - dinamički podaci o kretanju brodova
- `vessels` - statički podaci o brodovima
- `vessel_types` - podaci o tipovima brodova
- `ports` - podaci o lukama

## Rekonstrukcija

Za potrebe optimizacije performansi kreirana je dodatna kolekcija:
