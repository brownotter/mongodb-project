# Agregacioni upiti

### 1. Detekcija navigacionih anomalija u kretanju brodova
```
db.positions.aggregat(
[
    {"$match": {"kinematics.SOG_kmh": {"$gt": 2.0}}},
    {
        "$project": {
            "MMSI": 1,
            "SOG": "$kinematics.SOG_kmh",
            "Anomalija_Smera": {"$abs": {"$subtract": ["$kinematics.COG", "$kinematics.Heading"]}}
        }
    },
    {
        "$lookup": {
            "from": "vessels",
            "localField": "MMSI",
            "foreignField": "MMSI",
            "as": "brod"
        }
    },
    {"$unwind": "$brod"},
    {
        "$project": {
            "MMSI": 1,
            "ImeBroda": "$brod.VesselName",
            "Anomalija_Smera": 1,
            "SOG": 1,
            "Povrsina": {"$multiply": ["$brod.dimensions.Length", "$brod.dimensions.Width"]}
        }
    },
    {"$match": {"Anomalija_Smera": {"$gt": 45.0}, "Povrsina": {"$gt": 500}}},
    {"$sort": {"Anomalija_Smera": -1}},
    {"$limit": 5}
])
```

### 2. Hronološka analiza i profilisanje saobraćaja u vremenskom špicu
```
db.positions.aggregat([
    {
        "$lookup": {
            "from": "vessels",
            "localField": "MMSI",
            "foreignField": "MMSI",
            "as": "brod_info"
        }
    },
    {"$unwind": "$brod_info"},
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
            "_id": "$brod_info.TransceiverClass",
            "prosecna_brzina": {"$avg": "$kinematics.SOG_kmh"},
            "ukupno_poruka": {"$sum": 1}
        }
    }
])
```

### 3. Višeslojna statistika navigacionog statusa po tipovima tereta
```
db.positions.aggregat([
    {
        "$match": {
            "Status": {"$in": [0, 1]} 
        }
    },
    # Prvih 30.000 dokumenata koji prođu filter (zbog memorije)
    {"$limit": 30000},
    {
        "$lookup": {
            "from": "vessels",
            "localField": "MMSI",
            "foreignField": "MMSI",
            "as": "brod"
        }
    },
    {"$unwind": "$brod"},
    {
        "$lookup": {
            "from": "vessel_types",
            "localField": "brod.VesselType",
            "foreignField": "_id",
            "as": "tip"
        }
    },
    {"$unwind": "$tip"},
    {
        "$group": {
            "_id": "$tip.name",
            "ukupno_zabeleženih_pozicija": {"$sum": 1},
            "prosecan_navigacioni_status": {"$avg": "$Status"}
        }
    },
    {"$sort": {"ukupno_zabeleženih_pozicija": -1}}
])
```

### 4. Analitička GIS geometrija i prostorni stres-test sistema
```
db.positions.aggregat([
    {
        "$match": {
            "kinematics.SOG_kmh": {"$gt": 1.0},
            "Cargo": {"$ne": None},
            "position": {"$ne": None}
        }
    },
   
    {"$limit": 30000},  
    {
        "$addFields": {
            "Lat_Rad": {"$divide": [{"$multiply": [{"$arrayElemAt": ["$position.coordinates", 1]}, 3.141592653589793]}, 180.0]},
            "Lon_Rad": {"$divide": [{"$multiply": [{"$arrayElemAt": ["$position.coordinates", 0]}, 3.141592653589793]}, 180.0]}
        }
    },
    {
        "$addFields": {
            "Haversine_Udaljenost_Km": {
                "$multiply": [
                    6371,
                    {"$acos": {
                        "$add": [
                            {"$multiply": [{"$sin": luka_lat_rad}, {"$sin": "$Lat_Rad"}]},
                            {"$multiply": [
                                {"$cos": luka_lat_rad},
                                {"$cos": "$Lat_Rad"},
                                {"$cos": {"$subtract": ["$Lon_Rad", luka_lon_rad]}}
                            ]}
                        ]
                    }}
                ]
            }
        }
    },
    
    {
        "$lookup": {
            "from": "vessels",
            "localField": "MMSI",
            "foreignField": "MMSI",
            "as": "detalji_broda"
        }
    },
    {"$unwind": "$detalji_broda"},
    {
        "$addFields": {
            "Matrica_Za_Stres_Procesora": {"$range": [0, 150]}
        }
    },
    {"$unwind": "$Matrica_Za_Stres_Procesora"},
    {
        "$group": {
            "_id": {
                "Tip": "$detalji_broda.VesselType",
                "Teret": "$Cargo"
            },
            "Ukupno_Stres_Iteracija": {"$sum": 1},
            "Prosecna_Udaljenost": {"$avg": "$Haversine_Udaljenost_Km"},
            "Maksimalna_Brzina": {"$max": "$kinematics.SOG_kmh"}
        }
    },
    {"$sort": {"Ukupno_Stres_Iteracija": -1}},
    {"$limit": 5},
    {
        "$project": {
            "TipVessel": "$_id.Tip",
            "Teret": "$_id.Teret",
            "Procesirani_Volumen": "$Ukupno_Stres_Iteracija",
            "Prosek_Udaljenosti_Km": "$Prosecna_Udaljenost",
            "Maks_Brzina": "$Maksimalna_Brzina"
        }
    }
]
)
```

### 5. Predikcija kašnjenja i proračun deficita brzine (ETA analiza)
```
db.positions.aggregat([
    {
        "$project": {
            "MMSI": 1,
            "StvarnaBrzina": "$kinematics.SOG_kmh",
            "PotrebnaBrzina": {
                "$cond": [
                    {"$and": [{"$gt": ["$destination.ETA_hours", 0]}, {"$gt": ["$destination.dist_km", 0]}]},
                    {"$divide": ["$destination.dist_km", "$destination.ETA_hours"]},
                    0
                ]
            }
        }
    },
    {
        "$project": {
            "MMSI": 1,
            "StvarnaBrzina": 1,
            "PotrebnaBrzina": 1,
            "Deficit_Brzine": {"$subtract": ["$PotrebnaBrzina", "$StvarnaBrzina"]}
        }
    },
    {
        "$lookup": {
            "from": "vessels",
            "localField": "MMSI",
            "foreignField": "MMSI",
            "as": "brod"
        }
    },
    {"$unwind": "$brod"},
    {"$match": {"Deficit_Brzine": {"$gt": 5.0}}},
    {"$sort": {"Deficit_Brzine": -1}},
    {"$limit": 5}
])
```
