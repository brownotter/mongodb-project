# Unapređeni agregacioni upiti

### 1. Detekcija navigacionih anomalija u kretanju brodova
```
db.positions_enriched.aggregate([
{"$match": {"kinematics.SOG_kmh": {"$gt": 2.0}}},
    {
        "$project": {
            "_id": 0,
            "MMSI": 1,
            "ImeBroda": "$VesselName",
            "SOG": "$kinematics.SOG_kmh",
            "Anomalija_Smera": {"$abs": {"$subtract": ["$kinematics.COG", "$kinematics.Heading"]}},
            "Povrsina": {"$multiply": ["$dimensions.Length", "$dimensions.Width"]}
        }
    },
    {"$match": {"Anomalija_Smera": {"$gt": 45.0}, "Povrsina": {"$gt": 500}}},
    {"$sort": {"Anomalija_Smera": -1}},
    {"$limit": 5}
]
)
```

### 2. Hronološka analiza i profilisanje saobraćaja u vremenskom špicu
```
db.positions_enriched.aggregate([
    {
        "$match": {
            "BaseDateTime": {
                "$gte": "2022-03-31 00:00:00",
                "$lte": "2022-03-31 02:00:00"
            }
        }
    },
    {
        "$group": {
            "_id": "$TransceiverClass",
            "prosecna_brzina": {"$avg": "$kinematics.SOG_kmh"},
            "ukupno_poruka": {"$sum": 1}
        }
    }
])

```

### 3. Višeslojna statistika navigacionog statusa po tipovima tereta
```
db.positions_enriched.aggregate([
{"$match": {"Status": {"$in": [0, 1]}}},
    {
        "$group": {
            "_id": "$VesselTypeName",
            "ukupno_zabeleženih_pozicija": {"$sum": 1},
            "prosecan_navigacioni_status": {"$avg": "$Status"}
        }
    },
    {"$sort": {"ukupno_zabeleženih_pozicija": -1}}
])
```

### 4. Analitička GIS geometrija i prostorni stres-test sistema
```
db.positions_enriched.aggregate([
    {
        "$geoNear": {
            "near": {"type": "Point", "coordinates": [luka_coords[0], luka_coords[1]]},
            "distanceField": "Udaljenost_Metri",
            "spherical": True,
            "maxDistance": 500000, 
            "query": {
                "kinematics.SOG_kmh": {"$gt": 1.0},
                "Cargo": {"$ne": None}
            }
        }
    },

    {"$limit": 50000},
    {"$sort": {"Udaljenost_Metri": -1}},
    {"$limit": 5},
    {
        "$project": {
            "_id": 0,
            "ImeBroda": "$VesselName",
            "TipVessel": "$VesselType",
            "Teret": "$Cargo",
            "Udaljenost_Km": {"$divide": ["$Udaljenost_Metri", 1000]},
            "Brzina": "$kinematics.SOG_kmh"
        }
    }
])
```

### 5. Predikcija kašnjenja i proračun deficita brzine (ETA analiza)
```
db.positions_enriched.aggregate([
    {
        "$match": {
            "destination.ETA_hours": {"$gt": 0},
            "destination.dist_km": {"$gt": 0}
        }
    },
    {
        "$project": {
            "_id": 0, 
            "ImeBroda": "$VesselName",
            "StvarnaBrzina": "$kinematics.SOG_kmh",
            "Deficit_Brzine": {
                "$subtract": [
                    {"$divide": ["$destination.dist_km", "$destination.ETA_hours"]},
                    "$kinematics.SOG_kmh"
                ]
            }
        }
    },
    {"$match": {"Deficit_Brzine": {"$gt": 5.0}}},
    {"$sort": {"Deficit_Brzine": -1}},
    {"$limit": 5}
])
```
