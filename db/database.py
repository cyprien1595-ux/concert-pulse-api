import sqlite3

DB_PATH = "db/concerts.db"

def init_db():
    """Crée la table concerts si elle n'existe pas."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # On crée une table avec une contrainte UNIQUE sur l'URL
    # Cela permet d'éviter les doublons si on scrape plusieurs fois
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS concerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artist TEXT NOT NULL,
            date TEXT NOT NULL,
            venue TEXT NOT NULL,
            city TEXT NOT NULL,
            url TEXT UNIQUE NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    print("🗄️ Base de données initialisée avec succès.")

def save_concerts(concerts):
    """Insère une liste de dictionnaires dans la base."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    count = 0
    for c in concerts:
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO concerts (artist, date, venue, city, url)
                VALUES (?, ?, ?, ?, ?)
            ''', (c['artist'], c['date'], c['venue'], c['city'], c['url']))
            if cursor.rowcount > 0:
                count += 1
        except Exception as e:
            print(f"⚠️ Erreur insertion : {e}")
            
    conn.commit()
    conn.close()
    print(f"💾 {count} nouveaux concerts enregistrés en base.")

def get_concerts_filtered(artist=None, venue=None, date_from=None, date_to=None):
    """Récupère les concerts avec filtres optionnels (Artiste, Salle, Période)."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    query = "SELECT * FROM concerts WHERE 1=1"
    params = []
    
    # Filtre Artiste
    if artist:
        query += " AND artist LIKE ?"
        params.append(f"%{artist}%")
    
    # Filtre Salle
    if venue:
        query += " AND venue LIKE ?"
        params.append(f"%{venue}%")
        
    # Filtre Date Début (A partir de...)
    if date_from:
        query += " AND date >= ?"
        params.append(date_from)

    # Filtre Date Fin (Jusqu'à...)
    if date_to:
        query += " AND date <= ?"
        params.append(date_to)
        
    query += " ORDER BY date ASC"
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    concerts = [dict(row) for row in rows]
    conn.close()
    return concerts