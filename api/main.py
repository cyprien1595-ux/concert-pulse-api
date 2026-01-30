from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import sys
import os

# Configuration du chemin pour l'accès aux modules db et scraper
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.database import get_concerts_filtered, init_db, save_concerts
from scraper.main import get_concerts
from scraper.metronum import get_metronum_concerts

app = FastAPI(title="Concert Pulse API")

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    """S'exécute au démarrage : initialise la DB et fusionne les sources."""
    print("🔄 Rafraîchissement des données (Bikini + Metronum)...")
    init_db()
    
    # On récupère les deux sources et on les fusionne dans 'all_concerts'
    all_concerts = get_concerts() + get_metronum_concerts()
    
    if all_concerts:
        save_concerts(all_concerts)
        print(f"✅ Synchronisation réussie : {len(all_concerts)} concerts en base.")
    else:
        print("⚠️ Aucun concert récupéré au démarrage.")

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Concert Pulse API is pulsing!"}

@app.get("/concerts")
def read_concerts(
    artist: Optional[str] = Query(None),
    venue: Optional[str] = Query(None),
    genre: Optional[str] = Query(None, description="Filtrer par genre (Rock, Rap, Electro...)"),
    date_from: Optional[str] = Query(None, alias="from"),
    date_to: Optional[str] = Query(None, alias="to")
):
    concerts = get_concerts_filtered(
        artist=artist, 
        venue=venue, 
        genre=genre, # <-- Ajout ici
        date_from=date_from, 
        date_to=date_to
    )
    return {
        "count": len(concerts),
        "concerts": concerts
    }