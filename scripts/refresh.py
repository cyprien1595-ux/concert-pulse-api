import sys
import os

# Toujours le même fix pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper.main import get_concerts
from db.database import init_db, save_concerts

def refresh_data():
    print("🔄 Début de la mise à jour des données...")
    init_db()
    concerts = get_concerts()
    if concerts:
        save_concerts(concerts)
        print("✅ Données synchronisées !")
    else:
        print("⚠️ Échec de la récupération.")

if __name__ == "__main__":
    refresh_data()