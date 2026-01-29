import requests
from bs4 import BeautifulSoup

url = "https://lebikini.com/programmation"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

print("🔍 Analyse de la structure HTML...\n")

# On cherche tous les liens qui pourraient être des concerts
# Astuce : souvent les liens de concerts contiennent "/programmation/" dans l'URL
links = soup.find_all("a", href=True)

found_count = 0
for link in links:
    href = link['href']
    # On filtre pour ne voir que ce qui ressemble à un événement
    if "/programmation/" in href and len(link.text.strip()) > 0:
        found_count += 1
        print(f"--- Élément #{found_count} ---")
        print(f"URL: {href}")
        print(f"Classes du lien: {link.get('class')}")
        print(f"Parent (Conteneur): {link.parent.name} (Classes: {link.parent.get('class')})")
        print(f"Texte brut: {link.text.strip()[:50]}...") # On coupe à 50 chars
        print("-" * 30)
        
        if found_count >= 3: # On s'arrête après 3 exemples pour ne pas polluer
            break

if found_count == 0:
    print("❌ Aucun lien de programmation évident trouvé avec ce filtre.")