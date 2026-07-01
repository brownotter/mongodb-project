#%%
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["maritime_traffic"]

vessel_types_col = db["vessel_types"]
vessel_types_col.drop()

vessel_types = [
    {"_id": 0,   "name": "Not available",              "category": "Unknown"},
    {"_id": 1,   "name": "Reserved",                   "category": "Unknown"},
    {"_id": 3,   "name": "Reserved",                   "category": "Unknown"},
    {"_id": 7,   "name": "Reserved",                   "category": "Unknown"},
    {"_id": 9,   "name": "Reserved",                   "category": "Unknown"},
    {"_id": 10,  "name": "Reserved",                   "category": "Unknown"},
    {"_id": 16,  "name": "Reserved",                   "category": "Unknown"},
    {"_id": 18,  "name": "Reserved",                   "category": "Unknown"},
    {"_id": 20,  "name": "Wing in ground",             "category": "Special"},
    {"_id": 23,  "name": "Reserved",                   "category": "Unknown"},
    {"_id": 25,  "name": "Reserved",                   "category": "Unknown"},
    {"_id": 29,  "name": "Reserved",                   "category": "Unknown"},
    {"_id": 30,  "name": "Fishing",                    "category": "Fishing"},
    {"_id": 31,  "name": "Tug",                        "category": "Service"},
    {"_id": 32,  "name": "Tug pushing ahead",          "category": "Service"},
    {"_id": 33,  "name": "Dredger",                    "category": "Service"},
    {"_id": 34,  "name": "Dive vessel",                "category": "Service"},
    {"_id": 35,  "name": "Military ops",               "category": "Government"},
    {"_id": 36,  "name": "Sailing vessel",             "category": "Recreational"},
    {"_id": 37,  "name": "Pleasure craft",             "category": "Recreational"},
    {"_id": 38,  "name": "Reserved",                   "category": "Unknown"},
    {"_id": 39,  "name": "Reserved",                   "category": "Unknown"},
    {"_id": 40,  "name": "High speed craft",           "category": "Passenger"},
    {"_id": 45,  "name": "High speed craft - HSC",     "category": "Passenger"},
    {"_id": 49,  "name": "High speed craft - other",   "category": "Passenger"},
    {"_id": 50,  "name": "Pilot vessel",               "category": "Service"},
    {"_id": 51,  "name": "Search and rescue",          "category": "Service"},
    {"_id": 52,  "name": "Tug (ocean)",                "category": "Service"},
    {"_id": 53,  "name": "Port tender",                "category": "Service"},
    {"_id": 54,  "name": "Anti-pollution vessel",      "category": "Service"},
    {"_id": 55,  "name": "Law enforcement",            "category": "Government"},
    {"_id": 56,  "name": "Local vessel",               "category": "Service"},
    {"_id": 57,  "name": "Local vessel",               "category": "Service"},
    {"_id": 59,  "name": "Non-combatant ship",         "category": "Government"},
    {"_id": 60,  "name": "Passenger ship",             "category": "Passenger"},
    {"_id": 65,  "name": "Passenger - HAZ A",          "category": "Passenger"},
    {"_id": 67,  "name": "Passenger - HAZ C",          "category": "Passenger"},
    {"_id": 68,  "name": "Passenger - HAZ D",          "category": "Passenger"},
    {"_id": 69,  "name": "Passenger - other",          "category": "Passenger"},
    {"_id": 70,  "name": "Cargo ship",                 "category": "Commercial"},
    {"_id": 71,  "name": "Cargo - HAZ A",              "category": "Commercial"},
    {"_id": 72,  "name": "Cargo - HAZ B",              "category": "Commercial"},
    {"_id": 73,  "name": "Cargo - HAZ C",              "category": "Commercial"},
    {"_id": 74,  "name": "Cargo - HAZ D",              "category": "Commercial"},
    {"_id": 75,  "name": "Cargo - HAZ E",              "category": "Commercial"},
    {"_id": 76,  "name": "Cargo - HAZ F",              "category": "Commercial"},
    {"_id": 79,  "name": "Cargo - other",              "category": "Commercial"},
    {"_id": 80,  "name": "Tanker",                     "category": "Commercial"},
    {"_id": 81,  "name": "Tanker - HAZ A",             "category": "Commercial"},
    {"_id": 82,  "name": "Tanker - HAZ B",             "category": "Commercial"},
    {"_id": 84,  "name": "Tanker - HAZ D",             "category": "Commercial"},
    {"_id": 89,  "name": "Tanker - other",             "category": "Commercial"},
    {"_id": 90,  "name": "Other",                      "category": "Other"},
    {"_id": 91,  "name": "Other - HAZ A",              "category": "Other"},
    {"_id": 94,  "name": "Other - HAZ D",              "category": "Other"},
    {"_id": 95,  "name": "Other - HAZ E",              "category": "Other"},
    {"_id": 97,  "name": "Other - reserved",           "category": "Other"},
    {"_id": 98,  "name": "Other - reserved",           "category": "Other"},
    {"_id": 99,  "name": "Other - other",              "category": "Other"},
    {"_id": 200, "name": "Unknown/Non-standard",       "category": "Unknown"},
]

vessel_types_col.insert_many(vessel_types)

print(f"Ubaceno {vessel_types_col.count_documents({})} tipova plovila.")
client.close()
# %%
