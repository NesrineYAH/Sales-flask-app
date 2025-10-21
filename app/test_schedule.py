import schedule
import time

def job():
    print("✅ Tâche exécutée !")

schedule.every(10).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
