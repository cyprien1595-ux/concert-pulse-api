import requests
from bs4 import BeautifulSoup
from .utils import guess_genre # Import de notre nouvel outil

def get_concerts():
    url = "https://lebikini.com/programmation"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    concerts = []

    for item in soup.find_all('div', class_='programmation-item'):
        try:
            artist = item.find('h3').get_text(strip=True)
            date = item.find('time')['datetime'][:10]
            link = item.find('a')['href']
            
            concerts.append({
                "artist": artist,
                "date": date,
                "venue": "Le Bikini",
                "url": f"https://lebikini.com{link}",
                "genre": guess_genre(artist) # Classification automatique
            })
        except:
            continue
    return concerts

