import schedule, time
from etl import importer_nouvelles_ventes, calculer_total_ventes, verifier_integrite

def pipeline_journalier():
    print("🚀 Lancement du pipeline data...")
    importer_nouvelles_ventes("./data/ventes_jour.csv")
    calculer_total_ventes()
    verifier_integrite()
    print("Pipeline terminé.")

schedule.every().day.at("02:00").do(pipeline_journalier)

while True:
    schedule.run_pending()
    time.sleep(60)
