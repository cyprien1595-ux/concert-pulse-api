# Concert Pulse API 🎸

Un service backend simple et robuste pour collecter et exposer les concerts à venir à Toulouse (Source : Le Bikini).

## 🚀 Fonctionnalités
- **Scraping automatisé** : Collecte intelligente des données (Artiste, Date, Salle).
- **Stockage SQL** : Base de données SQLite avec gestion des doublons.
- **API REST** : FastAPI avec filtres de recherche et documentation Swagger.
- **Pipeline de Refresh** : Script dédié pour mettre à jour les données.

## 🛠️ Stack Technique
- **Langage** : Python 3.9+
- **Framework API** : FastAPI & Uvicorn
- **Base de données** : SQLite
- **Scraping** : BeautifulSoup4 & Requests

## 📦 Installation & Lancement

1. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt