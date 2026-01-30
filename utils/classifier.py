def guess_genre(text):
    text = text.lower()
    genres = {
        "Electro": ["techno", "dj", "electro", "house", "dubstep", "mix"],
        "Rock": ["rock", "metal", "punk", "indie", "pop-rock", "band"],
        "Rap": ["rap", "hip-hop", "trap", "reggaeton", "flow"],
        "Jazz/Classique": ["jazz", "blues", "piano", "orchestre", "classique"]
    }
    
    for genre, keywords in genres.items():
        if any(kw in text for kw in keywords):
            return genre
    return "Autre" 
