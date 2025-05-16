
from database import get_connection

def analyser_ventes_sql():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) AS nb, SUM(montant) AS total FROM ventes")
    row = cur.fetchone()
    conn.close()
    nb = row["nb"]
    total = row["total"] or 0
    return {
        "total_ventes": total,
        "nombre_commandes": nb,
        "moyenne": total / nb if nb > 0 else 0
    }
