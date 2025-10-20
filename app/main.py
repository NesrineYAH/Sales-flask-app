# 20/10/2025
from flask import Flask, render_template
from analyze import analyser_ventes_sql
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "db", "ventes.db")

def get_db_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        app.logger.error(f"Erreur de connexion à la base de données : {e}")
        return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/produits")
def produits():
    conn = get_db_connection()
    if conn:
        produits = conn.execute("SELECT * FROM produits").fetchall()
        conn.close()
        return render_template("produits.html", produits=produits)
    return "Erreur de connexion à la base de données", 500

@app.route("/ventes")
def ventes():
    conn = get_db_connection()
    if conn:
        ventes = conn.execute("SELECT * FROM ventes").fetchall()
        conn.close()
        return render_template("ventes.html", ventes=ventes)
    return "Erreur de connexion à la base de données", 500

@app.route("/magasins")
def magasins():
    conn = get_db_connection()
    if conn:
        magasins = conn.execute("SELECT * FROM magasins").fetchall()
        conn.close()
        return render_template("magasins.html", magasins=magasins)
    return "Erreur de connexion à la base de données", 500

# update 20/10/2025

@app.route("/stats")
def stats():
    try:
        resultats = analyser_ventes_sql()  # Doit retourner {"labels": [...], "data": [...]}
        labels = resultats.get("labels", [])
        data = resultats.get("data", [])
        return render_template("stats.html", resultats=resultats, labels=labels, data=data)
    except Exception as e:
        app.logger.error(f"Erreur lors de l'analyse des ventes : {e}")
        return f"Erreur lors de l'analyse des ventes : {e}", 500

@app.errorhandler(500)
def server_error(e):
    return f"Erreur serveur : {e}", 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

