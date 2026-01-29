import requests
from bs4 import BeautifulSoup
import re
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.database import init_db, save_concerts

def clean_artist_name(text):
    # Nettoyage simple : on enlève les mentions de salle ou de prix
    # Ex: "BERTRAND BELIN + SAMUEL COVELChanson..." -> "BERTRAND BELIN + SAMUEL COVEL"
    name = text.split(' @ ')[0] # Si présence de @
    name = re.split(r'Ouverture|Chanson|humour|Rock|Pop|Electro', name, flags=re.IGNORECASE)[0]
    return name.strip()

def get_concerts():
    url = "https://lebikini.com/programmation"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    concerts_dict = {} # Pour éviter les doublons par URL

    for link in soup.find_all("a", href=True):
        href = link['href']
        
        # Pattern détecté : /YYYY/MM/DD/nom-evenement
        match = re.search(r'/(\d{4})/(\d{2})/(\d{2})/(.+)', href)
        
        if match:
            year, month, day, slug = match.groups()
            full_url = f"https://lebikini.com{href}"
            date_str = f"{year}-{month}-{day}"
            
            # On récupère le texte du lien
            raw_text = link.get_text(strip=True)
            
            # Si on n'a pas encore ce concert, ou si le texte actuel est plus long (nom d'artiste)
            if full_url not in concerts_dict or len(raw_text) > len(concerts_dict[full_url]['artist']):
                
                # On détermine la salle (Bikini par défaut, sauf si mentionné)
                venue = "Le Bikini"
                if "zenith" in href.lower() or "zenith" in raw_text.lower():
                    venue = "Zénith Toulouse"

                # On ne veut pas stocker "Réserver" ou "Complet" comme nom d'artiste
                if raw_text not in ["Réserver", "Complet", ""] and not raw_text[0].isdigit():
                    concerts_dict[full_url] = {
                        "artist": clean_artist_name(raw_text),
                        "date": date_str,
                        "venue": venue,
                        "city": "Toulouse",
                        "url": full_url
                    }

    return list(concerts_dict.values())

if __name__ == "__main__":
    print("🚀 Démarrage du pipeline...")
    
    # 1. Initialiser la DB
    init_db()
    
    # 2. Récupérer les données
    concerts = get_concerts()
    
    if concerts:
        # 3. Sauvegarder en DB
        save_concerts(concerts)
        print("✨ Terminé !")
    else:
        print("❌ Aucun concert trouvé, rien à enregistrer.")