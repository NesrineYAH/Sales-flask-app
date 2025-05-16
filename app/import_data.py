# app/import_data.py

import os
import sys
import csv
import sqlite3

# Chemins
BASE_DIR  = os.path.dirname(__file__)
DB_PATH   = os.path.join(BASE_DIR, "db", "ventes.db")
DATA_DIR  = os.path.join(BASE_DIR, "data")

# Vérifier que la base existe
if not os.path.exists(DB_PATH):
    print(f"❌ Base introuvable : {DB_PATH}")
    sys.exit(1)

# Connexion à SQLite
conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON;")
cur = conn.cursor()

def load_csv_to_db(csv_filename, table, columns):
    csv_path = os.path.join(DATA_DIR, csv_filename)
    if not os.path.isfile(csv_path):
        print(f"❌ Fichier CSV introuvable : {csv_path}")
        return

    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        placeholders = ",".join("?" for _ in columns)
        sql = f"INSERT OR IGNORE INTO {table} ({','.join(columns)}) VALUES ({placeholders})"
        count = 0
        for row in reader:
            values = tuple(row[col] for col in columns)
            try:
                cur.execute(sql, values)
                count += 1
            except sqlite3.IntegrityError:
                # ignore duplicates or foreign key errors
                continue
        print(f"✅ {count} lignes insérées dans `{table}` depuis `{csv_filename}`")

# Charger les trois CSV
load_csv_to_db("products.csv", "produits",
             ["Date","ID Référence produit","Quantité","ID Magasin"])
load_csv_to_db("stores.csv", "magasins",
               ["id", "name", "city", "region"])
load_csv_to_db("sales.csv", "ventes",
               ["id", "product_id", "store_id", "quantity", "date", "total_price"])

# Enregistrer et fermer
conn.commit()
conn.close()
print("✅ Importation terminée.")
