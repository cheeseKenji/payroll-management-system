import os
from datetime import datetime
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import pagesizes


class PayslipService:

    def safe(self, record, key, default=0):
        return record[key] if key in record else default

    def generate_payslip(self, payroll_record):

        if not os.path.exists("payslips"):
            os.makedirs("payslips")

        employee_name = f"{payroll_record['first_name']}_{payroll_record['last_name']}"
        file_name = f"Payslip_{employee_name}_{payroll_record['start_date']}.pdf"
        file_path = os.path.join("payslips", file_name)

        doc = SimpleDocTemplate(file_path, pagesize=pagesizes.A4)
        styles = getSampleStyleSheet()
        elements = []

        # ===== COMPANY HEADER =====
        elements.append(Paragraph("<b>Enterprise Payroll System</b>", styles["Title"]))
        elements.append(Spacer(1, 15))

        # ===== EMPLOYEE DETAILS =====
        elements.append(Paragraph("<b>Employee Details</b>", styles["Heading2"]))
        elements.append(Spacer(1, 10))

        emp_data = [
            ["Employee Name", f"{payroll_record['first_name']} {payroll_record['last_name']}"],
            ["Employee ID", str(payroll_record["employee_id"])],
            ["Department", self.safe(payroll_record, "department", "N/A")],
            ["Designation", self.safe(payroll_record, "designation", "N/A")],
            ["Pay Period", f"{payroll_record['start_date']} to {payroll_record['end_date']}"],
            ["Generated On", datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
        ]

        emp_table = Table(emp_data, colWidths=[150, 300])
        emp_table.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey)
        ]))

        elements.append(emp_table)
        elements.append(Spacer(1, 20))

        # ===== EARNINGS =====
        elements.append(Paragraph("<b>Earnings</b>", styles["Heading2"]))
        elements.append(Spacer(1, 10))

        earnings_data = [
            ["Component", "Amount"],
            ["Basic Salary", self.safe(payroll_record, "basic_salary")],
            ["HRA", self.safe(payroll_record, "hra")],
            ["DA", self.safe(payroll_record, "da")],
            ["Special Allowance", self.safe(payroll_record, "special_allowance")],
            ["Conveyance Allowance", self.safe(payroll_record, "conveyance_allowance")],
            ["Medical Allowance", self.safe(payroll_record, "medical_allowance")],
            ["Bonus", self.safe(payroll_record, "bonus")],
            ["Overtime Pay", self.safe(payroll_record, "overtime_pay")],
            ["Gross Salary", self.safe(payroll_record, "gross_salary")]
        ]

        earnings_table = Table(earnings_data, colWidths=[250, 150])
        earnings_table.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("ALIGN", (1, 1), (-1, -1), "RIGHT")
        ]))

        elements.append(earnings_table)
        elements.append(Spacer(1, 20))

        # ===== DEDUCTIONS =====
        elements.append(Paragraph("<b>Deductions</b>", styles["Heading2"]))
        elements.append(Spacer(1, 10))

        deductions_data = [
            ["Component", "Amount"],
            ["PF", self.safe(payroll_record, "pf")],
            ["Professional Tax", self.safe(payroll_record, "professional_tax")],
            ["Income Tax", self.safe(payroll_record, "income_tax")],
            ["ESI", self.safe(payroll_record, "esi")],
            ["Loan Deduction", self.safe(payroll_record, "loan_deduction")],
            ["Loss of Pay", self.safe(payroll_record, "loss_of_pay")],
            ["Total Deductions", self.safe(payroll_record, "total_deductions")]
        ]

        deductions_table = Table(deductions_data, colWidths=[250, 150])
        deductions_table.setStyle(TableStyle([
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("ALIGN", (1, 1), (-1, -1), "RIGHT")
        ]))

        elements.append(deductions_table)
        elements.append(Spacer(1, 30))

        # ===== NET SALARY =====
        elements.append(
            Paragraph(
                f"<b>NET SALARY: ₹ {round(self.safe(payroll_record, 'net_salary'), 2)}</b>",
                styles["Heading1"]
            )
        )

        elements.append(Spacer(1, 40))
        elements.append(Paragraph("Authorized Signatory", styles["Normal"]))
        elements.append(Spacer(1, 20))
        elements.append(Paragraph("This is a system-generated payslip.", styles["Normal"]))

        doc.build(elements)

        return file_path