import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'concerts.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('DROP TABLE IF EXISTS concerts')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS concerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artist TEXT NOT NULL,
            date TEXT NOT NULL,
            venue TEXT NOT NULL,
            city TEXT,
            url TEXT,
            genre TEXT,
            UNIQUE(artist, date, venue)
        )
    ''')
    conn.commit()
    conn.close()
    print("✅ Base de données réinitialisée avec la colonne Genre.")
    
    try:
        cursor.execute('ALTER TABLE concerts ADD COLUMN genre TEXT')
        print("✅ Colonne 'genre' ajoutée avec succès.")
    except sqlite3.OperationalError:
        print("ℹ️ La colonne 'genre' existe déjà.")
        
    conn.commit()
    conn.close()

def save_concerts(concerts):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for c in concerts:
        cursor.execute('''
            INSERT OR REPLACE INTO concerts (artist, date, venue, city, url, genre)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (c['artist'], c['date'], c['venue'], c.get('city', 'Toulouse'), c['url'], c.get('genre', 'Autre')))
    conn.commit()
    conn.close()

def get_concerts_filtered(artist=None, venue=None, date_from=None, date_to=None, genre=None):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    query = "SELECT * FROM concerts WHERE 1=1"
    params = []
    
    if artist:
        query += " AND artist LIKE ?"
        params.append(f"%{artist}%")
    if venue:
        query += " AND venue LIKE ?"
        params.append(f"%{venue}%")
    if genre:
        query += " AND genre = ?"
        params.append(genre)
    if date_from:
        query += " AND date >= ?"
        params.append(date_from)
    if date_to:
        query += " AND date <= ?"
        params.append(date_to)
        
    query += " ORDER BY date ASC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

