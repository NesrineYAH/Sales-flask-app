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
CREATE TABLE IF NOT EXISTS ventes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ID_produit TEXT,
    ID_Magasin INTEGER,
    date TEXT,
    quantite INTEGER,
    total_price REAL
)
""")

conn.commit()
print(" Base de données créée avec succès.\n")

# --- Fonction d'importation CSV ---
def load_csv_to_db(csv_path, table, columns):
    print(f" Importation de {os.path.basename(csv_path)} dans la table {table}")
  
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        print("Colonnes trouvées dans le CSV :", reader.fieldnames)
        rows = [tuple(row[col].strip() for col in columns) for row in reader]
        placeholders = ",".join("?" * len(columns))
        sql = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
        cur.executemany(sql, rows)
        conn.commit()
        print(f" {len(rows)} lignes insérées dans {table}.\n")

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

# 19/05/2025 calcul ventes 

prix_produits = {}  
with open(os.path.join("data", "products.csv"), newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        prix_produits[row["ID_produit"]] = float(row["Prix"])   # le montant est dicémal

# Charger sales.csv avec calcul du total_price
with open(os.path.join("data", "sales.csv"), newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    ventes = []
    for row in reader:
        ref = row["ID_produit"]
        qte = int(row["Quantite"])  # nb de Quantite entier 
        prix = prix_produits.get(ref, 0)
        total = round(qte * prix, 2)
        ventes.append((
            row["Date"], row["ID_produit"], int(row["ID_Magasin"]), qte, total
        ))

cur.executemany("""
    INSERT INTO ventes (date, ID_produit, ID_Magasin, quantite, total_price)
    VALUES (?, ?, ?, ?, ?)
""", ventes)




conn.close()
print(" Tous les fichiers CSV ont été importés avec succès.")
