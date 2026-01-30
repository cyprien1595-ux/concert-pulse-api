def guess_genre(text):
    if not text:
        return "Autre"
    text = text.lower()
    genres = {
        "Electro": ["techno", "dj", "electro", "house", "dubstep", "mix", "club", "trance"],
        "Rock": ["rock", "metal", "punk", "indie", "pop-rock", "band", "guitar"],
        "Rap": ["rap", "hip-hop", "trap", "reggaeton", "flow", "mc"],
        "Jazz/Classique": ["jazz", "blues", "piano", "orchestre", "classique", "saxo"]
    }
    
    for genre, keywords in genres.items():
        if any(kw in text for kw in keywords):
            return genre
    return "Autre"

