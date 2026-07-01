# %% biblioteke
import pandas as pd
from pymongo import MongoClient
import math

# %% Konekcija na MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["maritime_traffic"]

vessels_col = db["vessels"]
positions_col = db["positions"]

# Brisanje kolekcija ako vec postoje (za ponovno pokretanje)
vessels_col.drop()
positions_col.drop()

print("Konekcija uspesna, kolekcije ociscene.")

# %% Ucitavanje CSV fajla
CSV_PATH = r"C:\Users\andje\Desktop\sbp projekat\processed_AIS_dataset.csv"

print("Ucitavanje CSV fajla")
df = pd.read_csv(CSV_PATH, low_memory=False)
print(f"Ucitano {len(df)} redova, {len(df.columns)} kolona.")

# %% Ciscenje nedostajucih vrednosti
def clean(val):
    if isinstance(val, float) and math.isnan(val):
        return None
    return val

# %% Kreiranje kolekcije vessels (staticni podaci)
print("Kreiranje vessels kolekcije...")

vessels_df = df[["MMSI", "IMO", "CallSign", "VesselName",
                  "VesselType", "TransceiverClass",
                  "Length", "Width", "Draft"]].drop_duplicates(subset=["MMSI"])

vessels_docs = []
for _, row in vessels_df.iterrows():
    doc = {
        "_id": int(row["MMSI"]) if not math.isnan(row["MMSI"]) else None,
        "MMSI": int(row["MMSI"]) if not math.isnan(row["MMSI"]) else None,
        "IMO": clean(row["IMO"]),
        "CallSign": clean(row["CallSign"]),
        "VesselName": clean(row["VesselName"]),
        "VesselType": clean(row["VesselType"]),
        "TransceiverClass": clean(row["TransceiverClass"]),
        "dimensions": {
            "Length": clean(row["Length"]),
            "Width": clean(row["Width"]),
            "Draft": clean(row["Draft"])
        }
    }
    if doc["_id"] is not None:
        vessels_docs.append(doc)

# Batch insert
BATCH = 1000
for i in range(0, len(vessels_docs), BATCH):
    vessels_col.insert_many(vessels_docs[i:i+BATCH])

print(f"Ubaceno {len(vessels_docs)} plovila u vessels kolekciju.")

# %% Kreiranje kolekcije positions (dinamicki zapisi)
print("Kreiranje positions kolekcije...")

positions_docs = []
for _, row in df.iterrows():
    doc = {
        "MMSI": clean(row["MMSI"]),
        "BaseDateTime": clean(row["BaseDateTime"]),
        "position": {
            "type": "Point",
            "coordinates": [clean(row["LON"]), clean(row["LAT"])]
        },
        "kinematics": {
            "SOG": clean(row["SOG"]),
            "SOG_kmh": clean(row["SOG_kmh"]),
            "COG": clean(row["COG"]),
            "Heading": clean(row["Heading"]),
            "Speed_Category": clean(row["Speed_Category"])
        },
        "Status": clean(row["Status"]),
        "Cargo": clean(row["Cargo"]),
        "destination": {
            "cluster_id": clean(row["dest_cluster"]),
            "dest_lat": clean(row["dest_lat"]),
            "dest_lon": clean(row["dest_lon"]),
            "dist_km": clean(row["dist_km"]),
            "ETA_hours": clean(row["ETA_hours"])
        }
    }
    positions_docs.append(doc)

# Batch insert 
BATCH = 5000
total = len(positions_docs)
for i in range(0, total, BATCH):
    positions_col.insert_many(positions_docs[i:i+BATCH])
    print(f"  Ubaceno {min(i+BATCH, total)}/{total} pozicija...")

print(f"Ubaceno {total} pozicija u positions kolekciju.")

# %% provera
print("\nProvera")
print(f"Vessels kolekcija: {vessels_col.count_documents({})} dokumenata")
print(f"Positions kolekcija: {positions_col.count_documents({})} dokumenata")
print("\nUvoz podataka uspesno zavrsen!")

client.close()

# %%
