import os
import logging
from etl import executer_pipeline

# Crée le dossier logs s'il n'existe pas
os.makedirs("logs", exist_ok=True)

# Config du logging

logging.basicConfig(filename="logs/etl.log", level=logging.INFO, format="%(asctime)s - %(message)s")
# Fichier CSV à traiter

try:
    logging.info(f"🚀 Lancement du pipeline ETL pour le fichier {"./data/ventes_jour.csv"}")
    executer_pipeline("./data/ventes_jour.csv")
    logging.info("✅ Pipeline ETL exécuté avec succès")
except Exception as e:
    logging.error(f"❌ Erreur lors de l'exécution du pipeline : {e}")
