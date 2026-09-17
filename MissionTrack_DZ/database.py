import sqlite3
import os

DB_NAME = "missiontrack.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Create Employees Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            rank TEXT,
            job_title TEXT,
            index_number TEXT,
            category TEXT,
            workplace TEXT,
            bank_type TEXT,
            bank_account TEXT
        )
    """)

    # Create Missions Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS missions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
            budget_chapter TEXT,
            budget_article TEXT,
            report_month_year TEXT,
            order_number TEXT,
            order_date TEXT,
            purpose TEXT,
            itinerary TEXT,
            transport_mode TEXT,
            departure_datetime TEXT,
            return_datetime TEXT,
            region TEXT,
            meals_count INTEGER,
            nights_count INTEGER,
            total_amount REAL,
            amount_text TEXT,
            creation_date TEXT,
            FOREIGN KEY(employee_id) REFERENCES employees(id)
        )
    """)

    # Create Settings Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY,
            republic_title TEXT DEFAULT 'الجمهورية الجزائرية الديمقراطية الشعبية',
            ministry_name TEXT DEFAULT '',
            state_name TEXT DEFAULT 'ولايـــــــــــــــــة المنيعــــــــــــــــــــــة',
            institution_name TEXT DEFAULT 'مديرية المواصلات السلكية واللاسلكية الوطنية',
            default_chapter TEXT DEFAULT '221300',
            default_article TEXT DEFAULT ''
        )
    ''')

    # Seed default settings if empty
    cursor.execute("SELECT COUNT(*) FROM settings")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO settings (republic_title, ministry_name, state_name, institution_name, default_chapter, default_article)
            VALUES ('الجمهورية الجزائرية الديمقراطية الشعبية', '', 'ولايـــــــــــــــــة المنيعــــــــــــــــــــــة', 'مديرية المواصلات السلكية واللاسلكية الوطنية', '221300', '')
        ''')

    # Check if mission_type column exists
    cursor.execute("PRAGMA table_info(missions)")
    columns = [col[1] for col in cursor.fetchall()]
    if 'mission_type' not in columns:
        cursor.execute("ALTER TABLE missions ADD COLUMN mission_type TEXT DEFAULT 'عادية'")

    conn.commit()
    conn.close()

# --- CRUD for Employees ---
def get_all_employees():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()
    conn.close()
    return rows

def get_employee(emp_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees WHERE id=?", (emp_id,))
    row = cursor.fetchone()
    conn.close()
    return row

def add_employee(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO employees (full_name, rank, job_title, index_number, category, workplace, bank_type, bank_account)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (data.get('full_name'), data.get('rank'), data.get('job_title'), data.get('index_number'),
          data.get('category'), data.get('workplace'), data.get('bank_type'), data.get('bank_account')))
    conn.commit()
    conn.close()

def update_employee(emp_id, data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE employees
        SET full_name=?, rank=?, job_title=?, index_number=?, category=?, workplace=?, bank_type=?, bank_account=?
        WHERE id=?
    """, (data.get('full_name'), data.get('rank'), data.get('job_title'), data.get('index_number'),
          data.get('category'), data.get('workplace'), data.get('bank_type'), data.get('bank_account'), emp_id))
    conn.commit()
    conn.close()

def delete_employee(emp_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE id=?", (emp_id,))
    cursor.execute("DELETE FROM missions WHERE employee_id=?", (emp_id,))
    conn.commit()
    conn.close()

# --- CRUD for Missions ---
def get_missions_for_employee(emp_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM missions WHERE employee_id=?", (emp_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def add_mission(emp_id, data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO missions (employee_id, budget_chapter, budget_article, report_month_year, order_number, order_date, purpose, itinerary, transport_mode, departure_datetime, return_datetime, region, meals_count, nights_count, total_amount, amount_text, creation_date, mission_type)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, date('now'), ?)
    ''', (emp_id, data.get('budget_chapter'), data.get('budget_article'), data.get('report_month_year'),
          data.get('order_number'), data.get('order_date'), data.get('purpose'), data.get('itinerary'),
          data.get('transport_mode'), data.get('departure_datetime'), data.get('return_datetime'),
          data.get('region'), data.get('meals_count'), data.get('nights_count'),
          data.get('total_amount'), data.get('amount_text'), data.get('mission_type', 'عادية')))
    conn.commit()
    conn.close()

def delete_mission(mission_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM missions WHERE id=?", (mission_id,))
    conn.commit()
    conn.close()

def get_stats():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM missions")
    total_missions = cursor.fetchone()[0]
    cursor.execute("SELECT SUM(total_amount) FROM missions")
    total_spent = cursor.fetchone()[0] or 0
    conn.close()
    return total_missions, total_spent


# --- CRUD for Settings ---
def get_settings():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM settings LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return row

def update_settings(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE settings
        SET republic_title=?, ministry_name=?, state_name=?, institution_name=?, default_chapter=?, default_article=?
        WHERE id=(SELECT MIN(id) FROM settings)
    ''', (data.get('republic_title'), data.get('ministry_name'), data.get('state_name'),
          data.get('institution_name'), data.get('default_chapter'), data.get('default_article')))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
