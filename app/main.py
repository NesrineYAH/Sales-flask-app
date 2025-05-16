from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), "db", "ventes.db")




def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Pour accéder aux colonnes par nom
    return conn


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/produits")
def produits():
    conn = get_db_connection()
    produits = conn.execute("SELECT * FROM produits").fetchall()
    conn.close()
    return render_template("produits.html", produits=produits)

@app.route("/ventes")
def ventes():
    conn = get_db_connection()
    ventes = conn.execute("SELECT * FROM ventes").fetchall()
    conn.close()
    return render_template("ventes.html", ventes=ventes)

@app.route("/magasins")
def magasins():
    conn = get_db_connection()
    magasins = conn.execute("SELECT * FROM magasins").fetchall()
    conn.close()
    return render_template("magasins.html", magasins=magasins)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
