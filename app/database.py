# app/database.py

import sqlite3

DB_PATH = "db/ventes.db"

def get_connection():
    """Retourne une connexion SQLite vers la base de données."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Pour accéder aux colonnes par nom
    return conn

