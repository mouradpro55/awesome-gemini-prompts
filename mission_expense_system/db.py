import sqlite3
import os

DB_NAME = "mission_expense.db"

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
            admin_location TEXT,
            bank_type TEXT,
            bank_account TEXT
        )
    """)

    # Create Missions Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS missions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
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
            FOREIGN KEY(employee_id) REFERENCES employees(id)
        )
    """)

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
        INSERT INTO employees (full_name, rank, job_title, index_number, category, admin_location, bank_type, bank_account)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (data.get('full_name'), data.get('rank'), data.get('job_title'), data.get('index_number'),
          data.get('category'), data.get('admin_location'), data.get('bank_type'), data.get('bank_account')))
    conn.commit()
    conn.close()
    return cursor.lastrowid

def update_employee(emp_id, data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE employees SET full_name=?, rank=?, job_title=?, index_number=?, category=?, admin_location=?, bank_type=?, bank_account=?
        WHERE id=?
    """, (data.get('full_name'), data.get('rank'), data.get('job_title'), data.get('index_number'),
          data.get('category'), data.get('admin_location'), data.get('bank_type'), data.get('bank_account'), emp_id))
    conn.commit()
    conn.close()

def delete_employee(emp_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE id=?", (emp_id,))
    # also cascade delete missions
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
    cursor.execute("""
        INSERT INTO missions (employee_id, order_number, order_date, purpose, itinerary, transport_mode, departure_datetime, return_datetime, region, meals_count, nights_count)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (emp_id, data.get('order_number'), data.get('order_date'), data.get('purpose'), data.get('itinerary'),
          data.get('transport_mode'), data.get('departure_datetime'), data.get('return_datetime'),
          data.get('region'), data.get('meals_count'), data.get('nights_count')))
    conn.commit()
    conn.close()

def delete_mission(mission_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM missions WHERE id=?", (mission_id,))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database initialized.")
