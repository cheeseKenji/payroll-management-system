import sqlite3


def initialize_database():
    conn = sqlite3.connect("payroll_system.db")
    cursor = conn.cursor()

    # USERS TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT,
        employee_id INTEGER,
        is_active INTEGER DEFAULT 1
    )
    """)

    # LOGIN HISTORY TABLE (with ip_address)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS login_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        login_time TEXT,
        logout_time TEXT,
        ip_address TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    """)

    # Add ip_address column if upgrading existing database
    try:
        cursor.execute("ALTER TABLE login_history ADD COLUMN ip_address TEXT")
    except Exception:
        pass  # Column already exists

    # EMPLOYEES TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        email TEXT,
        phone TEXT,
        department TEXT,
        designation TEXT,
        date_of_joining TEXT
    )
    """)

    # PAYROLL TABLE
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payroll (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        start_date TEXT,
        end_date TEXT,
        total_working_days REAL,
        paid_days REAL,
        overtime_hours REAL,
        basic_salary REAL,
        hra REAL,
        da REAL,
        special_allowance REAL,
        conveyance_allowance REAL,
        medical_allowance REAL,
        bonus REAL,
        overtime_pay REAL,
        gross_salary REAL,
        pf REAL,
        professional_tax REAL,
        esi REAL,
        income_tax REAL,
        loan_deduction REAL,
        loss_of_pay REAL,
        total_deductions REAL,
        net_salary REAL,
        is_locked INTEGER DEFAULT 0,
        FOREIGN KEY (employee_id) REFERENCES employees(id)
    )
    """)

    conn.commit()
    conn.close()

    print("Database initialized successfully.")


if __name__ == "__main__":
    initialize_database()
