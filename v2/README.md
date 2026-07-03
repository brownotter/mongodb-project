# Rekonstrukcija šeme baze podataka

## Inicijalna šema

Originalni skup podataka je bio podeljen u 4 kolekcije:
- `positions` - dinamički podaci o kretanju brodova
- `vessels` - statički podaci o brodovima
- `vessel_types` - podaci o tipovima brodova
- `ports` - podaci o lukama

## Rekonstrukcija

Za potrebe optimizacije performansi kreirana je dodatna kolekcija:`positions_enriched`
Kreirana je spajanjem tabela `positions`, `vessels` i `vessel_types` pomoću `$lookup` operacije:
```
db.positions.aggregate([
  {
    $lookup: {
      from: "vessels",
      localField: "MMSI",
      foreignField: "_id",
      as: "vessel"
    }
  },

  {
    $unwind: {
      path: "$vessel",
      preserveNullAndEmptyArrays: true
    }
  },
  {
    $lookup: {
      from: "vessel_types",
      localField: "vessel.VesselType",
      foreignField: "_id",
      as: "type_info"
    }
  },

  {
    $unwind: {
      path: "$type_info", preserveNullAndEmptyArrays: true
    }
  },
{
    $addFields: {
      VesselName: "$vessel.VesselName",
      VesselType: "$vessel.VesselType",
      VesselTypeName: "$type_info.name",
      VesselCategory: "$type_info.category",
      TransceiverClass: "$vessel.TransceiverClass",
      dimensions: "$vessel.dimensions"
    }
  },
   {$project: {vessel: 0, type_info: 0}
  },
  {$out: "positions_enriched" }
])
```

Zatim su dodati indeksi:
```
db.positions_enriched.createIndex({ "destination.ETA_hours": 1 });
db.positions_enriched.createIndex({ "kinematics.Speed_Category": 1 });
db.positions_enriched.createIndex({ "destination.dist_km": 1 });
db.positions_enriched.createIndex({ "destination.cluster_id": 1 });
db.positions_enriched.createIndex({ "MMSI": 1 });
db.positions_enriched.createIndex({"destination.ETA_hours": 1,"kinematics.Speed_Category": 1});
db.positions_enriched.createIndex({ "position": "2dsphere"});
```
Cilj rekonstrisane šeme je da smanji broj join operacija radi brže agregacije i lakše analize.
