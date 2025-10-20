FROM python:3.10-slim

# Définir le dossier de travail
WORKDIR /app

# copie requirements.txt à la racine /app
COPY requirements.txt .        
# copie main.py à la racine /app
COPY main.py .                 
# copie le dossier templates
COPY templates/ templates/ 
# copie le dossier static (important pour style.css)    
COPY static/ static/  
# copie le dossier db          
COPY db/ db/                   

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Définir les variables d’environnement Flask (⚠️ sans espaces autour du =)
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0

# Lancer le serveur Flask
CMD ["flask", "run"]








#Explication :
# gunicorn = serveur WSGI robuste
# -w 4 = 4 workers
# -b 0.0.0.0:5000 = écoute sur le port 5000
# app:app = fichier app.py, variable app

