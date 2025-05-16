import sqlite3
import csv
import os

# Chemins
DB_PATH = "db/ventes.db"
DATA_PATH = "data"

# Supprimer l'ancienne base de données si elle existe (au bon chemin)
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

# S'assurer que les dossiers existent
os.makedirs("data", exist_ok=True)
os.makedirs("db", exist_ok=True)

# Connexion à SQLite
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Création des tables
cur.execute("""
CREATE TABLE ventes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    id_produit TEXT,
    quantite INTEGER,
    id_magasin INTEGER
)

""")

cur.execute("""
CREATE TABLE IF NOT EXISTS magasins (
    id INTEGER PRIMARY KEY,
    name TEXT,
    city TEXT,
    region TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS ventes (
    id INTEGER PRIMARY KEY,
    product_id INTEGER,
    store_id INTEGER,
    date TEXT,
    quantity INTEGER,
    total_price REAL,
    FOREIGN KEY(product_id) REFERENCES produits(id),
    FOREIGN KEY(store_id) REFERENCES magasins(id)
)
""")

# Fonction pour charger un CSV
def load_csv_to_db(csv_file, table, columns):
    path = os.path.join(DATA_PATH, csv_file)
    if not os.path.exists(path):
        print(f"❌ Fichier introuvable : {path}")
        return

    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = [tuple(row[col] for col in columns) for row in reader]
        placeholders = ','.join(['?'] * len(columns))

        success_count = 0
        for row in rows:
            try:
                cur.execute(f"INSERT OR IGNORE INTO {table} ({','.join(columns)}) VALUES ({placeholders})", row)
                success_count += 1
            except Exception as e:
                print(f"❌ Erreur insertion {row} → {e}")

        print(f"✅ {success_count} lignes insérées dans {table} depuis {csv_file}")

# Chargement des fichiers CSV
load_csv_to_db("products.csv", "produits", ["Date","ID Reference produit","Quantité","ID Magasin"
])
load_csv_to_db("stores.csv", "magasins", ["id", "name", "city", "region"])
load_csv_to_db("sales.csv", "ventes", ["id", "product_id", "store_id", "date", "quantity", "total_price"])

# Finaliser
conn.commit()
conn.close()

print("✅ Base de données SQLite initialisée avec succès.")
