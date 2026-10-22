import sqlite3
import os
from database import init_db, get_connection

def test_db_schema():
    if os.path.exists("missiontrack.db"):
        os.remove("missiontrack.db")

    init_db()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(employees)")
    emp_cols = [row[1] for row in cursor.fetchall()]
    assert "department" in emp_cols

    cursor.execute("PRAGMA table_info(allowance_rates)")
    rates_cols = [row[1] for row in cursor.fetchall()]
    assert "meal_rate" in rates_cols

    cursor.execute("PRAGMA table_info(audit_log)")
    log_cols = [row[1] for row in cursor.fetchall()]
    assert "action" in log_cols

    conn.close()
