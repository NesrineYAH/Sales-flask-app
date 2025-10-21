import schedule
import time
from etl import executer_pipeline
from dotenv import load_dotenv
import os 

load_dotenv()

# Fonction qui sera exécutée automatiquement
def job():
    print(" Lancement automatique du pipeline ETL...")
    executer_pipeline("./data/ventes_jour.csv")
    print(" Pipeline ETL terminé.")

# Planification automatique en utilisant la variable du .env
schedule.every().day.at(os.getenv("ETL_SCHEDULE")).do(job)

print(" Planification active : le pipeline s'exécutera chaque jour à 08:00")

# Boucle infinie pour que le programme reste actif
while True:
    schedule.run_pending()
    time.sleep(60)  # vérifie toutes les 60 secondes si une tâche doit s'exécuter
