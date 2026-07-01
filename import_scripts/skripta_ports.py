# %%
import pandas as pd
from pymongo import MongoClient
import math

# %% Konekcija na MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["maritime_traffic"]

ports_col = db["ports"]
ports_col.drop()

print("Konekcija uspesna, kolekcija ociscena.")

# %% Ucitavanje CSV fajla
CSV_PATH = r"C:\Users\andje\Desktop\sbp projekat\UpdatedPub150.csv"

print("Ucitavanje CSV fajla")
df = pd.read_csv(CSV_PATH, low_memory=False)
print(f"Ucitano {len(df)} redova, {len(df.columns)} kolona.")

# %%ciscenje NaN vrednosti
def clean(val):
    if isinstance(val, float) and math.isnan(val):
        return None
    if isinstance(val, str) and val.strip() in ("", " "):
        return None
    return val

# %% Kreiranje dokumenata za ports kolekciju
print("Kreiranje ports kolekcije...")

ports_docs = []
for _, row in df.iterrows():
    lat = clean(row["Latitude"])
    lon = clean(row["Longitude"])

    doc = {
        "_id": int(row["World Port Index Number"]),
        "name": clean(row["Main Port Name"]),
        "alternate_name": clean(row["Alternate Port Name"]),
        "country": clean(row["Country Code"]),
        "region": clean(row["Region Name"]),
        "water_body": clean(row["World Water Body"]),
        "un_locode": clean(row["UN/LOCODE"]),

        #lokacija
        "location": {
            "type": "Point",
            "coordinates": [lon, lat]
        } if lat is not None and lon is not None else None,

        # Karakteristike luke
        "harbor": {
            "size": clean(row["Harbor Size"]),
            "type": clean(row["Harbor Type"]),
            "use": clean(row["Harbor Use"]),
            "shelter": clean(row["Shelter Afforded"]),
        },

        # dubina
        "depths": {
            "channel_m": clean(row["Channel Depth (m)"]),
            "anchorage_m": clean(row["Anchorage Depth (m)"]),
            "cargo_pier_m": clean(row["Cargo Pier Depth (m)"]),
            "oil_terminal_m": clean(row["Oil Terminal Depth (m)"]),
        },

        # max dimenzija brodova
        "max_vessel": {
            "length_m": clean(row["Maximum Vessel Length (m)"]),
            "beam_m": clean(row["Maximum Vessel Beam (m)"]),
            "draft_m": clean(row["Maximum Vessel Draft (m)"]),
        },

        # usluge
        "services": {
            "pilotage_compulsory": clean(row["Pilotage - Compulsory"]),
            "pilotage_available": clean(row["Pilotage - Available"]),
            "tugs_salvage": clean(row["Tugs - Salvage"]),
            "tugs_assistance": clean(row["Tugs - Assistance"]),
            "medical": clean(row["Medical Facilities"]),
            "repairs": clean(row["Repairs"]),
            "dry_dock": clean(row["Dry Dock"]),
        },

        # zalihe
        "supplies": {
            "fuel_oil": clean(row["Supplies - Fuel Oil"]),
            "diesel": clean(row["Supplies - Diesel Oil"]),
            "potable_water": clean(row["Supplies - Potable Water"]),
            "provisions": clean(row["Supplies - Provisions"]),
        },

        # restrikcije ulaska
        "entrance_restrictions": {
            "tide": clean(row["Entrance Restriction - Tide"]),
            "heavy_swell": clean(row["Entrance Restriction - Heavy Swell"]),
            "ice": clean(row["Entrance Restriction - Ice"]),
        },

        # kapaciteti
        "facilities": {
            "container": clean(row["Facilities - Container"]),
            "liquid_bulk": clean(row["Facilities - Liquid Bulk"]),
            "solid_bulk": clean(row["Facilities - Solid Bulk"]),
            "oil_terminal": clean(row["Facilities - Oil Terminal"]),
            "ro_ro": clean(row["Facilities - Ro-Ro"]),
            "lng_terminal": clean(row["Facilities - LNG Terminal"]),
        },

        # bezbednost i komunikacija
        "port_security": clean(row["Port Security"]),
        "vessel_traffic_service": clean(row["Vessel Traffic Service"]),
        "first_port_of_entry": clean(row["First Port of Entry"]),
    }

    ports_docs.append(doc)

# %% Batch insert
BATCH = 500
total = len(ports_docs)
for i in range(0, total, BATCH):
    try:
        ports_col.insert_many(ports_docs[i:i+BATCH], ordered=False)
    except Exception as e:
        print(f"Preskoceni duplikati {i}-{i+BATCH}")
    print(f"Ubaceno {min(i+BATCH, total)}/{total} luka...")
# %% Kreiranje geo indeksa za ubrzanje geo upita
ports_col.create_index([("location", "2dsphere")])
print("Geo indeks kreiran na 'location' polju.")

# %% Finalna provera
print(f"Ports kolekcija: {ports_col.count_documents({})} dokumenata")

# Primer jednog dokumenta
primer = ports_col.find_one({"name": {"$ne": None}})
if primer:
    print(f"\nPrimer dokumenta:")
    print(f"  Naziv: {primer['name']}")
    print(f"  Zemlja: {primer['country']}")
    print(f"  Koordinate: {primer['location']['coordinates'] if primer['location'] else 'N/A'}")
    print(f"  Veličina luke: {primer['harbor']['size']}")

print("\nUvoz luka uspesno zavrsen!")
client.close()