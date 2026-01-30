from fastapi import FastAPI, Query # J'ajoute Query ici
from typing import Optional # Pour rendre les paramètres optionnels
import sys
import os

# On s'assure que Python trouve le dossier 'db'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from db.database import get_concerts_filtered # On change le nom de l'import

app = FastAPI(title="Concert Pulse API")

@app.get("/concerts")
def read_concerts(
    artist: Optional[str] = Query(None, description="Filtrer par artiste"),
    venue: Optional[str] = Query(None, description="Filtrer par salle"),
    date_from: Optional[str] = Query(None, description="Depuis cette date (YYYY-MM-DD)", alias="from"),
    date_to: Optional[str] = Query(None, description="Jusqu'à cette date (YYYY-MM-DD)", alias="to")
):
    """Récupère la liste des concerts avec filtres."""
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