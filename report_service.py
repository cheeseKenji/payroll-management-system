import sqlite3
from config import DATABASE_NAME


class ReportService:

    def __init__(self):
        self.database = DATABASE_NAME

    def get_connection(self):
        conn = sqlite3.connect(self.database)
        conn.row_factory = sqlite3.Row
        return conn

    # ================= PAYROLL SUMMARY REPORT =================

    def get_payroll_summary(self, start_date=None, end_date=None, department=None, employee_id=None):

        query = """
            SELECT
                e.id AS emp_id,
                e.first_name || ' ' || e.last_name AS employee_name,
                e.department,
                e.designation,
                p.start_date,
                p.end_date,
                p.total_working_days,
                p.paid_days,
                p.overtime_hours,
                p.gross_salary,
                p.total_deductions,
                p.net_salary,
                CASE WHEN p.is_locked = 1 THEN 'Locked' ELSE 'Unlocked' END AS status
            FROM payroll p
            JOIN employees e ON p.employee_id = e.id
            WHERE 1=1
        """
        params = []

        if start_date:
            query += " AND p.start_date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND p.end_date <= ?"
            params.append(end_date)
        if department:
            query += " AND e.department LIKE ?"
            params.append(f"%{department}%")
        if employee_id:
            query += " AND e.id = ?"
            params.append(employee_id)

        query += " ORDER BY p.start_date DESC"

        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results

    # ================= EMPLOYEE LIST REPORT =================

    def get_employee_report(self, department=None, employee_id=None):

        query = """
            SELECT
                e.id,
                e.first_name || ' ' || e.last_name AS employee_name,
                e.email,
                e.phone,
                e.department,
                e.designation,
                e.date_of_joining
            FROM employees e
            WHERE 1=1
        """
        params = []

        if department:
            query += " AND e.department LIKE ?"
            params.append(f"%{department}%")
        if employee_id:
            query += " AND e.id = ?"
            params.append(employee_id)

        query += " ORDER BY e.id"

        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results

    # ================= DEPARTMENT PAYROLL REPORT =================

    def get_department_report(self, start_date=None, end_date=None, department=None):

        query = """
            SELECT
                e.department,
                COUNT(DISTINCT e.id) AS total_employees,
                COUNT(p.id) AS total_payrolls,
                ROUND(SUM(p.gross_salary), 2) AS total_gross,
                ROUND(SUM(p.total_deductions), 2) AS total_deductions,
                ROUND(SUM(p.net_salary), 2) AS total_net
            FROM payroll p
            JOIN employees e ON p.employee_id = e.id
            WHERE 1=1
        """
        params = []

        if start_date:
            query += " AND p.start_date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND p.end_date <= ?"
            params.append(end_date)
        if department:
            query += " AND e.department LIKE ?"
            params.append(f"%{department}%")

        query += " GROUP BY e.department ORDER BY total_net DESC"

        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results

    # ================= MONTHLY REPORT =================

    def get_monthly_report(self, start_date=None, end_date=None, department=None):

        query = """
            SELECT
                strftime('%Y-%m', p.start_date) AS month,
                COUNT(DISTINCT e.id) AS total_employees,
                ROUND(SUM(p.gross_salary), 2) AS total_gross,
                ROUND(SUM(p.total_deductions), 2) AS total_deductions,
                ROUND(SUM(p.net_salary), 2) AS total_net,
                COUNT(CASE WHEN p.is_locked = 1 THEN 1 END) AS locked_count
            FROM payroll p
            JOIN employees e ON p.employee_id = e.id
            WHERE 1=1
        """
        params = []

        if start_date:
            query += " AND p.start_date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND p.end_date <= ?"
            params.append(end_date)
        if department:
            query += " AND e.department LIKE ?"
            params.append(f"%{department}%")

        query += " GROUP BY strftime('%Y-%m', p.start_date) ORDER BY month DESC"

        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results

    # ================= SUMMARY STATS =================

    def get_summary_stats(self, start_date=None, end_date=None, department=None, employee_id=None):

        query = """
            SELECT
                COUNT(DISTINCT e.id) AS total_employees,
                COUNT(p.id) AS total_payrolls,
                ROUND(SUM(p.gross_salary), 2) AS total_gross,
                ROUND(SUM(p.total_deductions), 2) AS total_deductions,
                ROUND(SUM(p.net_salary), 2) AS total_net
            FROM payroll p
            JOIN employees e ON p.employee_id = e.id
            WHERE 1=1
        """
        params = []

        if start_date:
            query += " AND p.start_date >= ?"
            params.append(start_date)
        if end_date:
            query += " AND p.end_date <= ?"
            params.append(end_date)
        if department:
            query += " AND e.department LIKE ?"
            params.append(f"%{department}%")
        if employee_id:
            query += " AND e.id = ?"
            params.append(employee_id)

        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        conn.close()
        return result
