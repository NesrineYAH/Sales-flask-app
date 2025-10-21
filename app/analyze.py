from database import get_connection
import sqlite3, os
from dotenv import load_dotenv

load_dotenv()
DB_PATH = os.getenv("DB_PATH")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def analyser_ventes_sql():
    conn = get_connection()
    cur = conn.cursor()

    # 💰 Chiffre d'affaires global
    cur.execute("""
        SELECT SUM(v.quantite * p.prix) AS total_ventes, COUNT(*) AS nb
        FROM ventes v
        JOIN produits p ON v.ID_produit = p.ID_produit
    """)
    row = cur.fetchone()

    total = row["total_ventes"] if row and row["total_ventes"] is not None else 0.0
    nb = row["nb"] if row and row["nb"] is not None else 0
    moyenne = round(total / nb, 2) if nb > 0 else 0.0

    # Produit le plus vendu
    cur.execute("""
        SELECT p.nom, SUM(v.quantite) AS total_qte
        FROM ventes v
        JOIN produits p ON v.ID_produit = p.ID_produit
        GROUP BY p.nom
        ORDER BY total_qte DESC
        LIMIT 1
    """)
    top_produit_row = cur.fetchone()
    produit_top = top_produit_row["nom"] if top_produit_row else "Inconnu"

    # Magasin le plus performant
    cur.execute("""
        SELECT m.Ville, SUM(v.quantite * p.prix) AS total
        FROM ventes v
        JOIN produits p ON v.ID_produit = p.ID_produit
        JOIN magasins m ON v.ID_Magasin = m.ID_Magasin
        GROUP BY m.Ville
        ORDER BY total DESC
        LIMIT 1
    """)
    magasin_top_row = cur.fetchone()
    magasin_top = magasin_top_row["Ville"] if magasin_top_row else "Inconnu"

    # Mois de vente le plus actif
    cur.execute("""
        SELECT strftime('%Y-%m', date) AS mois, COUNT(*) AS nb
        FROM ventes
        GROUP BY mois
        ORDER BY nb DESC
        LIMIT 1
    """)
    periode_row = cur.fetchone()
    periode_top = periode_row["mois"] if periode_row else "Inconnue"

    # 📊 Données pour graphique : ventes par produit
    cur.execute("""
        SELECT p.nom, SUM(v.quantite * p.prix) AS total
        FROM ventes v
        JOIN produits p ON v.ID_produit = p.ID_produit
        GROUP BY p.nom
        ORDER BY total DESC
    """)
    rows = cur.fetchall()

    labels = [row["nom"] for row in rows] if rows else []
    data = [round(row["total"], 2) for row in rows if row["total"] is not None] if rows else []

    # Détail des totaux par produit
    totals_par_produit = [
        {"nom": row["nom"], "total": round(row["total"], 2)}
        for row in rows if row["total"] is not None
    ]

    # ✅ On ferme la connexion à la fin
    conn.close()

    return {
        "chiffre_affaires": round(total, 2),
        "nombre_commandes": nb,
        "moyenne": moyenne,
        "produit_top": produit_top,
        "magasin_top": magasin_top,
        "periode_top": periode_top,
        "labels": labels,
        "data": data,
        "totals_par_produit": totals_par_produit
    }
