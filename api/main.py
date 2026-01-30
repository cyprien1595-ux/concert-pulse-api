from scraper.metronum import get_metronum_concerts # Ajoute cet import en haut
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Query
from typing import Optional
import sys
import os

# Configuration du chemin pour l'accès aux modules db et scraper
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.database import get_concerts_filtered, init_db, save_concerts
from scraper.main import get_concerts

app = FastAPI(title="Concert Pulse API")

# Autoriser tout le monde (pour le dev, c'est ok)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Autorise toutes les origines
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    """S'exécute au démarrage du serveur : initialise la DB et actualise les données."""
    print("🔄 Rafraîchissement des données au démarrage...")
    init_db()
    data = get_concerts() + get_metronum_concerts()
    concerts = get_concerts()
    if concerts:
        save_concerts(concerts)
        print(f"✅ Synchronisation réussie : {len(concerts)} concerts en base.")
    else:
        print("⚠️ Aucun concert récupéré au démarrage.")

@app.get("/health")
def health_check():
    """Vérifie que l'API est en ligne."""
    return {"status": "ok", "message": "Concert Pulse API is pulsing!"}

@app.get("/concerts")
def read_concerts(
    artist: Optional[str] = Query(None, description="Filtrer par artiste"),
    venue: Optional[str] = Query(None, description="Filtrer par salle"),
    date_from: Optional[str] = Query(None, description="Depuis cette date (YYYY-MM-DD)", alias="from"),
    date_to: Optional[str] = Query(None, description="Jusqu'à cette date (YYYY-MM-DD)", alias="to")
):
    """Récupère la liste des concerts avec filtres optionnels."""
    concerts = get_concerts_filtered(
        artist=artist, 
        venue=venue, 
        date_from=date_from, 
        date_to=date_to
    )
    return {
        "count": len(concerts),
        "filters": {
            "artist": artist, 
            "venue": venue,
            "from": date_from,
            "to": date_to
        },
        "concerts": concerts
    }