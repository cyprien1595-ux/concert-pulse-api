import sys
import os

# Ajout du chemin racine pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scraper.main import get_concerts as get_bikini
from scraper.metronum import get_metronum_concerts
from db.database import init_db, save_concerts

def refresh_all_data():
    print("🔄 Début de la mise à jour globale...")
    init_db()
    
    # 1. Scraping du Bikini
    print("🎸 Scraping Le Bikini / Zénith...")
    bikini_data = get_bikini()
    
    # 2. Scraping du Metronum
    print("🥁 Scraping Le Metronum...")
    metronum_data = get_metronum_concerts()
    
    # Fusion des listes
    all_concerts = bikini_data + metronum_data
    
    if all_concerts:
        save_concerts(all_concerts)
        print(f"✅ Terminé ! {len(all_concerts)} concerts synchronisés au total.")
    else:
        print("⚠️ Aucun concert trouvé aujourd'hui.")

if __name__ == "__main__":
    refresh_all_data()