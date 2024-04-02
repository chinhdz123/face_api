import sqlite3
# K?t n?i ??n c? s? d? li?u SQLite (n?u ch?a t?n t?i, s? ???c t?o m?i)
# conn = sqlite3.connect("/usr/share/hassio/homeassistant/analytic.db")
conn = sqlite3.connect("db/face.db")
cursor = conn.cursor()
conn.execute('PRAGMA foreign_keys = ON;')
# T?o b?ng states v?i datetime v? entity_id kh?ng ???c l?p l?i

cursor.execute('''
    CREATE TABLE IF NOT EXISTS camera (
        id INTEGER PRIMARY KEY,
        rtsp TEXT,
        UNIQUE(rtsp)
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS face_extract (
        id INTEGER PRIMARY KEY,
        rtsp TEXT,
        age INTEGER,
        emotion TEXT,
        gender TEXT,
        tracking_time INTEGER,
        relationship TEXT,
        datetime DATETIME
    )
''')

# L?u thay ??i v? ??ng k?t n?i
conn.commit()
conn.close()