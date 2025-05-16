from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)
DB_PATH = os.path.join(os.path.dirname(__file__), "db", "ventes.db")

def fetch_all(table):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table}")
    rows = cur.fetchall()
    conn.close()
    return rows

@app.route("/")
def index():
    produits  = fetch_all("produits")
    magasins  = fetch_all("magasins")
    ventes    = fetch_all("ventes")
    return render_template("index.html",
                           produits=produits,
                           magasins=magasins,
                           ventes=ventes)
    

@app.route("/produits")
def produits():
    conn = fetch_all()
    produits = conn.execute("SELECT * FROM produits").fetchall()
    conn.close()
    return render_template("produits.html", produits=produits)

@app.route("/ventes")
def ventes():
    conn = fetch_all()
    ventes = conn.execute("SELECT * FROM ventes").fetchall()
    conn.close()
    return render_template("ventes.html", ventes=ventes)

@app.route("/magasins")
def magasins():
    conn = fetch_all()
    magasins = conn.execute("SELECT * FROM magasins").fetchall()
    conn.close()
    return render_template("magasins.html", magasins=magasins)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
