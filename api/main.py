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
    artist: Optional[str] = Query(None, description="Nom de l'artiste"),
    venue: Optional[str] = Query(None, description="Nom de la salle")
):
    """Récupère la liste des concerts avec filtres optionnels."""
    concerts = get_concerts_filtered(artist=artist, venue=venue)
    return {
        "count": len(concerts),
        "filters": {"artist": artist, "venue": venue},
        "concerts": concerts
    }