import sqlite3
import os

def get_app_dir():
    if os.name == 'nt':
        base_dir = os.environ.get('APPDATA', os.path.expanduser('~'))
    else:
        base_dir = os.path.expanduser('~')
    app_dir = os.path.join(base_dir, 'MissionTrack_DZ')
    os.makedirs(app_dir, exist_ok=True)
    return app_dir

DB_PATH = os.path.join(get_app_dir(), 'missiontrack.db')

def get_connection():
    return sqlite3.connect(DB_PATH)

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
    init_budget_tables()

# --- CRUD for Employees ---

def init_budget_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budget_credits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fiscal_year INTEGER DEFAULT 2026,
            program_code TEXT DEFAULT '019',
            program_name TEXT DEFAULT 'المواصلات السلكية واللاسلكية الوطنية',
            subprogram_code TEXT DEFAULT '019.01',
            subprogram_name TEXT DEFAULT 'شبكات المواصلات',
            activity_code TEXT DEFAULT '2058',
            activity_name TEXT DEFAULT 'المواصلات السلكية واللاسلكية الوطنية لولاية المنيعة',
            order_officer_code TEXT DEFAULT '458/107',
            title_name TEXT DEFAULT 'العنوان الثاني : نفقات تسيير المصالح',
            class_code TEXT DEFAULT '21000',
            class_name TEXT DEFAULT 'التنقلات و النقل و الاتصالات',
            subclass_code TEXT DEFAULT '21100',
            subclass_name TEXT DEFAULT 'المهمات التنقلات والمصاريف ذات الصلة',
            allocated_budget REAL DEFAULT 600000.00
        )
    ''')

    cursor.execute("SELECT COUNT(*) FROM budget_credits")
    if cursor.fetchone()[0] == 0:
        cursor.execute('''
            INSERT INTO budget_credits (
                fiscal_year, program_code, program_name, subprogram_code, subprogram_name,
                activity_code, activity_name, order_officer_code, title_name,
                class_code, class_name, subclass_code, subclass_name, allocated_budget
            ) VALUES (
                2026, '019', 'المواصلات السلكية واللاسلكية الوطنية', '019.01', 'شبكات المواصلات',
                '2058', 'المواصلات السلكية واللاسلكية الوطنية لولاية المنيعة', '458/107',
                'العنوان الثاني : نفقات تسيير المصالح', '21000', 'التنقلات و النقل و الاتصالات',
                '21100', 'المهمات التنقلات والمصاريف ذات الصلة', 600000.00
            )
        ''')

    cursor.execute("PRAGMA table_info(missions)")
    cols = [c[1] for c in cursor.fetchall()]
    if 'commitment_number' not in cols:
        cursor.execute("ALTER TABLE missions ADD COLUMN commitment_number TEXT DEFAULT ''")
    if 'commitment_date' not in cols:
        cursor.execute("ALTER TABLE missions ADD COLUMN commitment_date TEXT DEFAULT ''")

    conn.commit()
    conn.close()

def get_budget_summary(fiscal_year=2026):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT allocated_budget FROM budget_credits WHERE fiscal_year=? LIMIT 1", (fiscal_year,))
    row = cursor.fetchone()
    allocated = row[0] if row else 600000.00

    cursor.execute("SELECT SUM(total_amount) FROM missions")
    total_consumed = cursor.fetchone()[0] or 0.0

    conn.close()
    return {
        'allocated_budget': allocated,
        'total_consumed': total_consumed,
        'available_budget': allocated - total_consumed
    }

def get_budget_credit_info():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM budget_credits LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    return row

def update_budget_credit_info(data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE budget_credits SET
            program_code=?, program_name=?, subprogram_code=?, subprogram_name=?,
            activity_code=?, activity_name=?, order_officer_code=?,
            class_code=?, class_name=?, allocated_budget=?
        WHERE id=(SELECT MIN(id) FROM budget_credits)
    ''', (
        data.get('program_code'), data.get('program_name'),
        data.get('subprogram_code'), data.get('subprogram_name'),
        data.get('activity_code'), data.get('activity_name'),
        data.get('order_officer_code'), data.get('class_code'),
        data.get('class_name'), float(data.get('allocated_budget', 600000.00))
    ))
    conn.commit()
    conn.close()
    init_budget_tables()

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
    init_budget_tables()

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
    init_budget_tables()

def delete_employee(emp_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE id=?", (emp_id,))
    cursor.execute("DELETE FROM missions WHERE employee_id=?", (emp_id,))
    conn.commit()
    conn.close()
    init_budget_tables()

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
    init_budget_tables()

def update_mission(mission_id, data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE missions
        SET budget_chapter=?, budget_article=?, report_month_year=?, order_number=?, order_date=?, purpose=?, itinerary=?, transport_mode=?, departure_datetime=?, return_datetime=?, region=?, meals_count=?, nights_count=?, total_amount=?, amount_text=?, mission_type=?
        WHERE id=?
    ''', (data.get('budget_chapter'), data.get('budget_article'), data.get('report_month_year'),
          data.get('order_number'), data.get('order_date'), data.get('purpose'), data.get('itinerary'),
          data.get('transport_mode'), data.get('departure_datetime'), data.get('return_datetime'),
          data.get('region'), data.get('meals_count'), data.get('nights_count'),
          data.get('total_amount'), data.get('amount_text'), data.get('mission_type', 'عادية'), mission_id))
    conn.commit()
    conn.close()
    init_budget_tables()

def delete_mission(mission_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM missions WHERE id=?", (mission_id,))
    conn.commit()
    conn.close()
    init_budget_tables()

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
    init_budget_tables()

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
