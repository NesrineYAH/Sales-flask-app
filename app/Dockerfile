
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
COPY main.py requirements.txt /app/
COPY templates/ /app/templates/
COPY db/ /app/db/


RUN pip install --no-cache-dir -r requirements.txt

COPY . .
ENV FLASK_APP = "main.py"
ENV FLASK_RUN_HOST=0.0.0.0



CMD ["flask", "run"]



#Explication :
# gunicorn = serveur WSGI robuste
# -w 4 = 4 workers
# -b 0.0.0.0:5000 = écoute sur le port 5000
# app:app = fichier app.py, variable app

