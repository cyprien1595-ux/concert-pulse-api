import requests
from bs4 import BeautifulSoup

def get_metronum_concerts():
    url = "https://lemetronum.fr/programmation/"
    # On simule un vrai navigateur très précisément
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        concerts = []

        # On cherche les titres dans les balises h3 qui sont souvent utilisées pour les noms d'artistes
        for title_tag in soup.find_all("h3"):
            title = title_tag.get_text(strip=True)
            # On cherche le lien parent ou proche
            parent_link = title_tag.find_parent("a") or title_tag.find_next("a")
            
            if title and len(title) > 2:
                concerts.append({
                    "artist": title,
                    "date": "2026-03-01", 
                    "venue": "Le Metronum",
                    "city": "Toulouse",
                    "url": parent_link['href'] if parent_link and 'href' in parent_link.attrs else url
                })
        
        return concerts
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return []

if __name__ == "__main__":
    results = get_metronum_concerts()
    print(f"🎸 Tentative H3 : Trouvé {len(results)} concerts.")
    for r in results[:5]:
        print(f"- {r['artist']}")