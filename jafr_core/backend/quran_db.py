import sqlite3
import os
import re
from backend.nlp import clean_and_normalize
from backend.engine import macro_value, digital_root
from backend.elements import calculate_elements

surah_regex = re.compile(r'^\*2\*\s+(\d+)\s+([^{]+)\s+{(\d+)}$')
ayah_regex = re.compile(r'^([^\{]+)\{(\d+)\}$')

def get_db_connection(db_path="jafr_quran.db"):
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path="jafr_quran.db"):
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    cursor.execute("PRAGMA synchronous = OFF;")
    cursor.execute("PRAGMA journal_mode = MEMORY;")
    cursor.execute("PRAGMA temp_store = MEMORY;")
    cursor.execute("PRAGMA cache_size = -64000;")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS surahs (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            total_ayahs INTEGER NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ayahs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            surah_id INTEGER NOT NULL,
            ayah_number INTEGER NOT NULL,
            text_tashkeel TEXT NOT NULL,
            clean_text TEXT NOT NULL,
            jummal_east INTEGER NOT NULL,
            jummal_west INTEGER NOT NULL,
            jummal_saghir INTEGER NOT NULL,
            dominant_element TEXT NOT NULL,
            fire_count INTEGER NOT NULL,
            earth_count INTEGER NOT NULL,
            air_count INTEGER NOT NULL,
            water_count INTEGER NOT NULL,
            FOREIGN KEY(surah_id) REFERENCES surahs(id)
        )
    ''')

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ayahs_jummal_east ON ayahs(jummal_east)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ayahs_jummal_west ON ayahs(jummal_west)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_ayahs_surah_num ON ayahs(surah_id, ayah_number)")

    conn.commit()
    conn.close()

def is_db_empty(db_path="jafr_quran.db"):
    if not os.path.exists(db_path):
        return True
    conn = get_db_connection(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM ayahs")
        count = cursor.fetchone()[0]
        return count == 0
    except sqlite3.OperationalError:
        return True
    finally:
        conn.close()

def ingest_quran(file_path="assets/data/ARQURAN.TXT", db_path="jafr_quran.db"):
    if not os.path.exists(file_path):
        print(f"{file_path} not found.")
        return

    init_db(db_path)
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    current_surah_id = 0
    ayahs_batch = []

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.startswith("*2*"):
            match = surah_regex.match(line)
            if match:
                surah_id, surah_name, total_ayahs = match.groups()
                current_surah_id = int(surah_id)
                cursor.execute(
                    "INSERT OR IGNORE INTO surahs (id, name, total_ayahs) VALUES (?, ?, ?)",
                    (current_surah_id, surah_name.strip(), int(total_ayahs))
                )
            continue

        line = line.lstrip("@").strip()
        match = ayah_regex.match(line)
        if match:
            text_tashkeel, ayah_number = match.groups()
            text_tashkeel = text_tashkeel.strip()
            ayah_number = int(ayah_number)

            clean_text = clean_and_normalize(text_tashkeel, unify_hamzat=True, expand_shaddah=False)

            jummal_east = macro_value(clean_text, "east")
            jummal_west = macro_value(clean_text, "west")
            jummal_saghir = digital_root(jummal_east)

            elem_counts, dominant = calculate_elements(clean_text)

            ayahs_batch.append((
                current_surah_id, ayah_number, text_tashkeel, clean_text,
                jummal_east, jummal_west, jummal_saghir,
                dominant, elem_counts["fire"], elem_counts["earth"], elem_counts["air"], elem_counts["water"]
            ))

    cursor.executemany('''
        INSERT INTO ayahs (
            surah_id, ayah_number, text_tashkeel, clean_text,
            jummal_east, jummal_west, jummal_saghir,
            dominant_element, fire_count, earth_count, air_count, water_count
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', ayahs_batch)

    conn.commit()
    conn.close()

def search_quran(jummal_val: int, rule="east", db_path="jafr_quran.db"):
    conn = get_db_connection(db_path)
    cursor = conn.cursor()

    col = "jummal_east" if rule == "east" else "jummal_west"

    query = f'''
        SELECT s.name as surah_name, a.ayah_number, a.text_tashkeel, a.{col} as jummal_value, a.dominant_element
        FROM ayahs a
        JOIN surahs s ON a.surah_id = s.id
        WHERE a.{col} = ?
    '''
    cursor.execute(query, (jummal_val,))
    results = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return results
