from database.db_manager import DatabaseManager
from services.payslip_service import PayslipService


class PayrollService:

    def __init__(self):
        self.db = DatabaseManager()
        self.payslip_service = PayslipService()

    # ================= CALCULATE =================

    def calculate_payroll(
        self,
        basic_salary,
        total_working_days,
        paid_days,
        overtime_hours,
        bonus=0,
        special_allowance=0,
        conveyance_allowance=0,
        medical_allowance=0,
        loan_deduction=0
    ):

        daily_salary  = basic_salary / total_working_days
        earned_salary = daily_salary * paid_days
        overtime_pay  = overtime_hours * (daily_salary / 8) * 1.5

        gross_salary = (
            earned_salary
            + overtime_pay
            + bonus
            + special_allowance
            + conveyance_allowance
            + medical_allowance
        )

        total_deductions = loan_deduction
        net_salary       = gross_salary - total_deductions

        return {
            "gross_salary":      gross_salary,
            "net_salary":        net_salary,
            "total_deductions":  total_deductions,
            "loan_deduction":    loan_deduction
        }

    # ================= SAVE =================

    def save_payroll(
        self,
        employee_id,
        start_date,
        end_date,
        total_days,
        paid_days,
        overtime_hours,
        payroll_data
    ):

        self.db.execute_query("""
            INSERT INTO payroll (
                employee_id,
                start_date,
                end_date,
                total_working_days,
                paid_days,
                overtime_hours,
                gross_salary,
                net_salary,
                total_deductions,
                loan_deduction,
                is_locked
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
        """, (
            employee_id,
            start_date,
            end_date,
            total_days,
            paid_days,
            overtime_hours,
            payroll_data["gross_salary"],
            payroll_data["net_salary"],
            payroll_data["total_deductions"],
            payroll_data["loan_deduction"]
        ))

    # ================= GET ALL  ← FIXED: added net_salary =================

    def get_all_payroll(self):

        return self.db.fetch_all("""
            SELECT
                p.id,
                p.start_date,
                p.end_date,
                p.gross_salary,
                COALESCE(p.net_salary, p.gross_salary - p.total_deductions, p.gross_salary) AS net_salary,
                p.is_locked,
                e.first_name,
                e.last_name
            FROM payroll p
            JOIN employees e ON p.employee_id = e.id
            ORDER BY p.id DESC
        """)

    # ================= GET BY ID =================

    def get_payroll_by_id(self, payroll_id):

        return self.db.fetch_one("""
            SELECT
                p.*,
                e.first_name,
                e.last_name
            FROM payroll p
            JOIN employees e ON p.employee_id = e.id
            WHERE p.id = ?
        """, (payroll_id,))

    # ================= LOCK =================

    def lock_payroll(self, payroll_id):

        self.db.execute_query("""
            UPDATE payroll SET is_locked = 1 WHERE id = ?
        """, (payroll_id,))

    def is_payroll_locked(self, payroll_id):

        result = self.db.fetch_one("""
            SELECT is_locked FROM payroll WHERE id = ?
        """, (payroll_id,))

        return result["is_locked"] == 1 if result else False

    # ================= DASHBOARD SUMMARY =================

    def get_dashboard_summary(self):

        result = self.db.fetch_one("""
            SELECT
                COUNT(*)                            AS total_records,
                COALESCE(SUM(gross_salary),    0)   AS total_gross,
                COALESCE(SUM(net_salary),      0)   AS total_net,
                COALESCE(SUM(total_deductions),0)   AS total_deductions,
                COALESCE(SUM(is_locked),       0)   AS locked_count
            FROM payroll
        """)

        return result if result else {
            "total_records":    0,
            "total_gross":      0,
            "total_net":        0,
            "total_deductions": 0,
            "locked_count":     0
        }