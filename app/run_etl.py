from etl import executer_pipeline

# Lancer le pipeline ETL sur le fichier ventes_jour.csv
executer_pipeline("./data/ventes_jour.csv")




import logging
from etl import executer_pipeline

logging.basicConfig(filename="logs/etl.log", level=logging.INFO, format="%(asctime)s - %(message)s")
executer_pipeline("../data/ventes_jour.csv")
logging.info("Pipeline ETL exécuté avec succès")

