from database.db_manager import DatabaseManager


class EmployeeService:

    def __init__(self):
        self.db = DatabaseManager()

    # ================= ADD =================

    def add_employee(
        self,
        first_name,
        last_name,
        email,
        phone,
        department,
        designation,
        doj
    ):

        self.db.execute_query("""
            INSERT INTO employees (
                first_name,
                last_name,
                email,
                phone,
                department,
                designation,
                date_of_joining
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            first_name,
            last_name,
            email,
            phone,
            department,
            designation,
            doj
        ))

    # ================= UPDATE =================

    def update_employee(
        self,
        emp_id,
        first_name,
        last_name,
        email,
        phone,
        department,
        designation,
        doj
    ):

        self.db.execute_query("""
            UPDATE employees
            SET first_name = ?,
                last_name = ?,
                email = ?,
                phone = ?,
                department = ?,
                designation = ?,
                date_of_joining = ?
            WHERE id = ?
        """, (
            first_name,
            last_name,
            email,
            phone,
            department,
            designation,
            doj,
            emp_id
        ))

    # ================= DELETE =================

    def delete_employee(self, emp_id):

        self.db.execute_query("""
            DELETE FROM employees WHERE id = ?
        """, (emp_id,))

    # ================= GET ALL =================

    def get_all_employees(self):

        return self.db.fetch_all("""
            SELECT * FROM employees
            ORDER BY id DESC
        """)

    # ================= COUNT (Dashboard Support) =================

    def get_employee_count(self):

        result = self.db.fetch_one("""
            SELECT COUNT(*) as total FROM employees
        """)

        return result["total"] if result else 0