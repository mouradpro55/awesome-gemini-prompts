import sqlite3
import os

DB_NAME = "missiontrack.db"

def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Create allowance_rates Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS allowance_rates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT,
            region TEXT,
            meal_rate REAL,
            night_rate REAL,
            UNIQUE(category, region)
        )
    """)

    # Populate default rates if empty
    cursor.execute("SELECT COUNT(*) FROM allowance_rates")
    if cursor.fetchone()[0] == 0:
        default_rates = [
            ("1-10", "شمال", 600, 2400),
            ("1-10", "جنوب", 1000, 4000),
            ("11-17", "شمال", 800, 3200),
            ("11-17", "جنوب", 1000, 4000),
            ("وظيفة عليا", "شمال", 1600, 6400),
            ("وظيفة عليا", "جنوب", 1600, 6400)
        ]
        cursor.executemany("INSERT INTO allowance_rates (category, region, meal_rate, night_rate) VALUES (?, ?, ?, ?)", default_rates)

    # Create audit_log Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            action TEXT,
            table_name TEXT,
            record_id INTEGER,
            details TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

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
            bank_account TEXT,
            department TEXT,
            budget_chapter TEXT,
            budget_article TEXT
        )
    """)

    # Try altering existing tables for backward compatibility
    emp_new_cols = [("job_title", "TEXT"), ("category", "TEXT"), ("department", "TEXT"), ("budget_chapter", "TEXT"), ("budget_article", "TEXT")]
    for col in emp_new_cols:
        try:
            cursor.execute(f"ALTER TABLE employees ADD COLUMN {col[0]} {col[1]}")
        except sqlite3.OperationalError:
            pass

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
            distance_km REAL,
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

    mis_new_cols = [("transport_mode", "TEXT"), ("region", "TEXT"), ("distance_km", "REAL")]
    for col in mis_new_cols:
        try:
            cursor.execute(f"ALTER TABLE missions ADD COLUMN {col[0]} {col[1]}")
        except sqlite3.OperationalError:
            pass

    conn.commit()
    conn.close()

def log_action(action, table_name, record_id, details=""):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO audit_log (action, table_name, record_id, details)
        VALUES (?, ?, ?, ?)
    """, (action, table_name, record_id, details))
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
        INSERT INTO employees (full_name, rank, job_title, index_number, category, workplace, bank_type, bank_account, department, budget_chapter, budget_article)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (data.get('full_name'), data.get('rank'), data.get('job_title'), data.get('index_number'),
          data.get('category'), data.get('workplace'), data.get('bank_type'), data.get('bank_account'),
          data.get('department'), data.get('budget_chapter'), data.get('budget_article')))
    emp_id = cursor.lastrowid
    conn.commit()
    conn.close()
    log_action("INSERT", "employees", emp_id, f"Added employee: {data.get('full_name')}")
    return emp_id

def update_employee(emp_id, data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE employees
        SET full_name=?, rank=?, job_title=?, index_number=?, category=?, workplace=?, bank_type=?, bank_account=?, department=?, budget_chapter=?, budget_article=?
        WHERE id=?
    """, (data.get('full_name'), data.get('rank'), data.get('job_title'), data.get('index_number'),
          data.get('category'), data.get('workplace'), data.get('bank_type'), data.get('bank_account'),
          data.get('department'), data.get('budget_chapter'), data.get('budget_article'), emp_id))
    conn.commit()
    conn.close()
    log_action("UPDATE", "employees", emp_id, f"Updated employee: {data.get('full_name')}")

def delete_employee(emp_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Also delete associated missions
    cursor.execute("SELECT id FROM missions WHERE employee_id=?", (emp_id,))
    associated_missions = cursor.fetchall()

    cursor.execute("DELETE FROM employees WHERE id=?", (emp_id,))
    cursor.execute("DELETE FROM missions WHERE employee_id=?", (emp_id,))
    conn.commit()
    conn.close()

    log_action("DELETE", "employees", emp_id, f"Deleted employee and {len(associated_missions)} associated missions")

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
    cursor.execute("""
        INSERT INTO missions (employee_id, budget_chapter, budget_article, report_month_year, order_number, order_date, purpose, itinerary, transport_mode, distance_km, departure_datetime, return_datetime, region, meals_count, nights_count, total_amount, amount_text, creation_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, date('now'))
    """, (emp_id, data.get('budget_chapter'), data.get('budget_article'), data.get('report_month_year'),
          data.get('order_number'), data.get('order_date'), data.get('purpose'), data.get('itinerary'),
          data.get('transport_mode'), data.get('distance_km'), data.get('departure_datetime'), data.get('return_datetime'),
          data.get('region'), data.get('meals_count'), data.get('nights_count'),
          data.get('total_amount'), data.get('amount_text')))
    mis_id = cursor.lastrowid
    conn.commit()
    conn.close()
    log_action("INSERT", "missions", mis_id, f"Added mission for employee {emp_id}")
    return mis_id

def delete_mission(mission_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM missions WHERE id=?", (mission_id,))
    conn.commit()
    conn.close()
    log_action("DELETE", "missions", mission_id, "Deleted mission")

def get_stats():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM missions")
    total_missions = cursor.fetchone()[0]
    cursor.execute("SELECT SUM(total_amount) FROM missions")
    total_spent = cursor.fetchone()[0] or 0
    conn.close()
    return total_missions, total_spent

if __name__ == "__main__":
    init_db()
    print("Database initialized.")

def get_reports():
    conn = get_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Summary by employee
    cursor.execute('''
        SELECT e.full_name, e.department,
               COUNT(m.id) as total_missions,
               SUM(m.meals_count) as total_meals,
               SUM(m.nights_count) as total_nights,
               SUM(m.total_amount) as total_spent
        FROM employees e
        LEFT JOIN missions m ON e.id = m.employee_id
        GROUP BY e.id
        ORDER BY total_spent DESC
    ''')
    emp_stats = cursor.fetchall()

    # Summary by department
    cursor.execute('''
        SELECT e.department,
               COUNT(m.id) as total_missions,
               SUM(m.meals_count) as total_meals,
               SUM(m.nights_count) as total_nights,
               SUM(m.total_amount) as total_spent
        FROM employees e
        INNER JOIN missions m ON e.id = m.employee_id
        GROUP BY e.department
        ORDER BY total_spent DESC
    ''')
    dept_stats = cursor.fetchall()

    conn.close()
    return emp_stats, dept_stats
