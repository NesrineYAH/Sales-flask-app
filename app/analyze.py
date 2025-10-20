from database import get_connection
import sqlite3, os

def get_connection():
    DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db", "ventes.db")
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def analyser_ventes_sql():
    conn = get_connection()
    cur = conn.cursor()

   # Total des ventes et nombre de commandes
    cur.execute("SELECT COUNT(*) AS nb, SUM(total_price) AS total FROM ventes")
    row = cur.fetchone()

    nb = row["nb"] if row and row["nb"] is not None else 0
    total = row["total"] if row and row["total"] is not None else 0.0

    # Calcul sécurisé de la moyenne
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
        SELECT m.Ville, SUM(v.total_price) AS total
        FROM ventes v
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
        SELECT p.nom, SUM(v.total_price) AS total
        FROM ventes v
        JOIN produits p ON v.ID_produit = p.ID_produit
        GROUP BY p.nom
        ORDER BY total DESC
    """)
    rows = cur.fetchall()
    labels = [row["nom"] for row in rows] if rows else []
    data = [round(row["total"], 2) for row in rows if row["total"] is not None] if rows else []

    conn.close()

    return {
        "total_ventes": round(total, 2) if total is not None else 0.0,
        "nombre_commandes": nb,
        "moyenne": moyenne,
        "produit_top": produit_top,
        "magasin_top": magasin_top,
        "periode_top": periode_top,
        "labels": labels,
        "data": data
    }
