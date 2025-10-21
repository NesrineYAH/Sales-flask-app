import pandas as pd
import sqlite3
import os

# 📍 Définir le chemin de la base de données SQLite
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db", "ventes.db")


def importer_nouvelles_ventes(fichier_csv):
    """
    Importe de nouvelles ventes depuis un fichier CSV dans la base SQLite.
    """
    print(f"📥 Importation du fichier : {fichier_csv}")

    if not os.path.exists(fichier_csv):
        print(f"❌ Le fichier {fichier_csv} n'existe pas.")
        return

    # Lire le fichier CSV avec pandas
    nouvelles_ventes = pd.read_csv(fichier_csv)

    # Vérification minimale
    colonnes_attendues = {"Date", "ID_produit", "Quantite", "ID_Magasin"}
    if not colonnes_attendues.issubset(nouvelles_ventes.columns):
        print(f"⚠️ Colonnes manquantes dans le fichier CSV. Colonnes attendues : {colonnes_attendues}")
        return

    # Connexion à la base SQLite
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Insérer les ventes dans la table
    for _, row in nouvelles_ventes.iterrows():
        cur.execute("""
            INSERT INTO ventes (date, ID_produit, quantite, ID_Magasin)
            VALUES (?, ?, ?, ?)
        """, (row["Date"], row["ID_produit"], row["Quantite"], row["ID_Magasin"]))

    conn.commit()
    conn.close()
    print(f"{len(nouvelles_ventes)} nouvelles ventes importées avec succès.")


def calculer_total_ventes():
    """
    Met à jour la colonne total_price dans la table ventes
    (total = quantite * prix du produit).
    """
    print("Mise à jour des totaux de ventes...")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        UPDATE ventes
        SET total_price = quantite * (
            SELECT prix FROM produits WHERE produits.ID_produit = ventes.ID_produit
        )
    """)

    conn.commit()
    conn.close()
    print("Totaux des ventes mis à jour avec succès.")


def verifier_integrite():
    """
    Vérifie la cohérence des données entre les ventes et les produits.
    """
    print("🔎 Vérification de l'intégrité des données...")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        SELECT v.ID_produit
        FROM ventes v
        LEFT JOIN produits p ON v.ID_produit = p.ID_produit
        WHERE p.ID_produit IS NULL
    """)

    erreurs = cur.fetchall()
    conn.close()

    if erreurs:
        print(f"⚠️ {len(erreurs)} ventes contiennent un produit inexistant.")
    else:
        print("Toutes les ventes sont cohérentes.")


def executer_pipeline(fichier_csv):
    """
    Exécute le pipeline ETL complet :
      1️⃣ Importation du fichier CSV
      2️⃣ Calcul des totaux
      3️⃣ Vérification de cohérence
    """
    print("🚀 Lancement du pipeline ETL...")
    importer_nouvelles_ventes(fichier_csv)
    calculer_total_ventes()
    verifier_integrite()
    print("✅ Pipeline ETL terminé avec succès.\n")
