import requests
from bs4 import BeautifulSoup
from .utils import guess_genre

def get_metronum_concerts():
    url = "https://lemetronum.fr/programmation/"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        concerts = []

        for title_tag in soup.find_all("h3"):
            artist = title_tag.get_text(strip=True)
            if artist and len(artist) > 2:
                concerts.append({
                    "artist": artist,
                    "date": "2026-03-01", 
                    "venue": "Le Metronum",
                    "url": "https://lemetronum.fr/programmation/",
                    "genre": guess_genre(artist) # Classification automatique
                })
        return concerts
    except:
        return []
    
    