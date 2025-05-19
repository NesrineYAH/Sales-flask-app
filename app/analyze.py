from database import get_connection

def analyser_ventes_sql():
    conn = get_connection()
    cur = conn.cursor()

    # Total des ventes et nombre de commandes
    cur.execute("SELECT COUNT(*) AS nb, SUM(total_price) AS total FROM ventes")
    row = cur.fetchone()
    nb = row["nb"]
    total = row["total"] or 0

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

    conn.close()

    return {
        "total_ventes": round(total, 2),
        "nombre_commandes": nb,
        "moyenne": round(total / nb, 2) if nb > 0 else 0,
        "produit_top": produit_top,
        "magasin_top": magasin_top,
        "periode_top": periode_top
    }
