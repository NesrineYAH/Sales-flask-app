# app/create_db.py

import sqlite3
import os
import sys

# Chemin vers la base correcte
BASE_DIR = os.path.dirname(__file__)
DB_PATH  = os.path.join(BASE_DIR, "db", "ventes.db")

if not os.path.exists(DB_PATH):
    print(f"❌ La base n'existe pas ici : {DB_PATH}")
    sys.exit(1)

# Connexion à la base SQLite
conn   = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 1) Lister les tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [t[0] for t in cursor.fetchall()]
print("Tables trouvées :", tables)

if "produits" not in tables:
    print("❌ La table 'produits' est absente.")
    conn.close()
    sys.exit(1)

# 2) Afficher les 5 premières lignes de chaque table
for table in tables:
    print(f"\n-- Contenu de `{table}` (5 premières lignes) --")
    try:
        cursor.execute(f"SELECT * FROM {table} LIMIT 5;")
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                print(row)
        else:
            print("(aucune donnée)")
    except sqlite3.Error as e:
        print(f"Erreur lecture {table} : {e}")

conn.close()
