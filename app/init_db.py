import sqlite3
import os
import csv

# Chemins
BASE_DIR = os.path.dirname(__file__)
DB_DIR   = os.path.join(BASE_DIR, "db")
DB_PATH  = os.path.join(DB_DIR, "ventes.db")
DATA_DIR = os.path.join(BASE_DIR, "data")

# Création du dossier "db" si nécessaire
os.makedirs(DB_DIR, exist_ok=True)

# Connexion à la base
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Suppression des tables si elles existent
cur.execute("DROP TABLE IF EXISTS produits")
cur.execute("DROP TABLE IF EXISTS magasins")
cur.execute("DROP TABLE IF EXISTS ventes")

# Création des tables
cur.execute("""
CREATE TABLE produits (
    nom TEXT,
    ID_produit TEXT,
    prix REAL,
    stock INTEGER
)
""")

cur.execute("""
CREATE TABLE magasins (
    ID_Magasin INTEGER PRIMARY KEY,
    Ville TEXT,
    Nombre_de_salaries INTEGER
)
""")

cur.execute("""
CREATE TABLE ventes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    ID_produit TEXT,
    quantite INTEGER,
    id_magasin INTEGER
)
""")

conn.commit()
print("✅ Base de données créée avec succès.\n")

# --- Fonction d'importation CSV ---
def load_csv_to_db(csv_path, table, columns):
    print(f"📥 Importation de {os.path.basename(csv_path)} dans la table {table}")
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        print("Colonnes trouvées dans le CSV :", reader.fieldnames)
        rows = [tuple(row[col].strip() for col in columns) for row in reader]
        placeholders = ",".join("?" * len(columns))
        sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
        cur.executemany(sql, rows)
        conn.commit()
        print(f"✅ {len(rows)} lignes insérées dans {table}.\n")

# --- Chargement des données ---
load_csv_to_db(
    os.path.join(DATA_DIR, "products.csv"),
    "produits",
    ["Nom", "ID_produit", "Prix", "Stock"]
)

load_csv_to_db(
    os.path.join(DATA_DIR, "stores.csv"),
    "magasins",
    ["ID_Magasin", "Ville", "Nombre_de_salaries"]
)

load_csv_to_db(
    os.path.join(DATA_DIR, "sales.csv"),
    "ventes",
    ["Date", "ID_produit", "Quantite", "ID_Magasin"]             
)

conn.close()
print("✅ Tous les fichiers CSV ont été importés avec succès.")
