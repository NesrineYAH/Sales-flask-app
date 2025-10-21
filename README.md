🛍️ Analyse des ventes d’une PME — Projet Data Engineer
🎯 Objectif

Ce projet a pour but de mettre en place une architecture conteneurisée (via Docker) pour :

Importer et structurer des données issues de fichiers CSV (produits, ventes, magasins).

Construire une base SQLite adaptée à l’analyse des ventes.

Offrir une interface web Flask avec affichage des données et graphiques HTML.

Réaliser des premières analyses exploratoires en SQL et Python.

Mettre en place un pipeline ETL automatisé avec logs pour suivre l’intégrité et les totaux des ventes.


<H2>🗂️ Structure du projet</H2>
<img src="./image_Structure_Projet.png" alt="struture projet">

<H2>📊 Données utilisées </h2> 
<ul>
<li>products.csv → informations sur les produits (ID, nom, prix, stock)</li>
<li>stores.csv → informations sur les magasins (ID, ville, nombre de salariés)</li>
<li>sales.csv → Toutes les ventes (ID produit, quantité, magasin, date)</li>
<li>ventes_jours.csv →affiche  ventes journalières par jours (ID produit, quantité, magasin, date)</li>
</ul>

<H2>Base de données </h2> 
<ul>
<li>produits (ID_produit, nom, prix, stock)</li>
<li>magasins (ID_magasin, ville, nombre_salaries)</li>
</ul>





