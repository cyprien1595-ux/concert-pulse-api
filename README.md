# 🎸 Concert Pulse API — Backend Project

**Concert Pulse API est un service backend qui collecte, stocke et expose des concerts à venir pour une ville donnée.**

# Stack
   Python, FastAPI, SQLite
   requests, BeautifulSoup, uvicorn

# Fonctionnement
   Scraping d’une source publique de concerts
   Nettoyage et normalisation des données
   Stockage en base SQLite (déduplication via contrainte UNIQUE)
   Exposition via une API REST documentée (Swagger)

# Fonctionnalités clés
   Récupération des concerts à venir
   Filtres API (?artist=, ?venue=)
   Script de rafraîchissement des données
   Documentation interactive (/docs)

# Ce que j’ai appris
   Construire un pipeline de données simple et robuste
   Gérer les pièges du web scraping (HTML bruité, parsing)
   Concevoir une API backend propre et exploitable
   Penser “service” plutôt que script isolé

# ⚠️ Limites
   Une seule source
   Une seule ville
   Pas d’authentification 