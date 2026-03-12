import tkinter as tk
from tkinter import ttk, messagebox
import sys, os, subprocess

from services.payroll_service import PayrollService
from services.employee_service import EmployeeService
from utils.theme import Theme


class PayrollUI:

    def __init__(self, parent, current_user=None):
        self.parent = parent
        self.current_user = current_user
        self.payroll_service  = PayrollService()
        self.employee_service = EmployeeService()
        self.employee_map = {}
        self.parent.configure(bg=Theme.MAIN_BG)
        self.build_layout()
        self.load_employees()
        self.load_payroll_records()

    # ================= LAYOUT =================

    def build_layout(self):

        # Title bar
        title_bar = tk.Frame(self.parent, bg=Theme.SUCCESS, height=50)
        title_bar.pack(fill="x", padx=20, pady=(15, 10))
        title_bar.pack_propagate(False)
        tk.Label(
            title_bar,
            text="  Payroll Management",
            bg=Theme.SUCCESS,
            fg="white",
            font=Theme.SUBTITLE_FONT
        ).pack(side="left", padx=15, pady=10)

        content = tk.Frame(self.parent, bg=Theme.MAIN_BG)
        content.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        content.columnconfigure(1, weight=1)
        content.rowconfigure(0, weight=1)

        # ── LEFT FORM ─────────────────────────────────────────────────────────
        form_outer = tk.Frame(content, bg=Theme.CARD_BORDER, padx=1, pady=1)
        form_outer.grid(row=0, column=0, sticky="ns", padx=(0, 10))

        form_frame = tk.Frame(form_outer, bg=Theme.CARD_BG, padx=20, pady=20)
        form_frame.pack(fill="both", expand=True)

        tk.Label(
            form_frame,
            text="Process Payroll",
            bg=Theme.CARD_BG,
            fg=Theme.TEXT_DARK,
            font=Theme.SUBTITLE_FONT
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))

        fields = [
            ("Employee *",                    "employee",   True),
            ("Start Date (YYYY-MM-DD) *",     "start_date", False),
            ("End Date (YYYY-MM-DD) *",       "end_date",   False),
            ("Basic Salary *",                "basic",      False),
            ("Total Working Days *",          "total_days", False),
            ("Paid Days *",                   "paid_days",  False),
            ("Overtime Hours",                "overtime",   False),
            ("Bonus",                         "bonus",      False),
            ("Special Allowance",             "special",    False),
            ("Conveyance Allowance",          "conveyance", False),
            ("Medical Allowance",             "medical",    False),
            ("Loan Deduction",                "loan",       False),
        ]

        self.entries = {}

        for i, (label, key, is_combo) in enumerate(fields, start=1):
            tk.Label(
                form_frame,
                text=label,
                bg=Theme.CARD_BG,
                fg=Theme.TEXT_MID,
                font=Theme.LABEL_FONT,
                anchor="w"
            ).grid(row=i, column=0, sticky="w", pady=4, padx=(0, 10))

            if is_combo:
                widget = ttk.Combobox(form_frame, state="readonly", width=22,
                                      font=Theme.LABEL_FONT)
            else:
                widget = tk.Entry(
                    form_frame, width=25, font=Theme.NORMAL_FONT,
                    relief="solid", bd=1,
                    highlightthickness=1,
                    highlightcolor=Theme.PRIMARY,
                    highlightbackground=Theme.CARD_BORDER
                )
            widget.grid(row=i, column=1, pady=4, ipady=4)
            self.entries[key] = widget

        # Buttons
        btn_frame = tk.Frame(form_frame, bg=Theme.CARD_BG)
        btn_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=(15, 0))

        for text, color, cmd in [
            ("Process Payroll",   Theme.SUCCESS,  self.process_payroll),
            ("Generate Payslip",  Theme.PRIMARY,  self.generate_selected_payslip),
            ("Lock Payroll",      Theme.DANGER,   self.lock_selected_payroll),
        ]:
            b = tk.Button(
                btn_frame, text=text, bg=color, fg="white",
                font=Theme.LABEL_FONT, relief="flat",
                width=20, cursor="hand2", command=cmd
            )
            b.pack(pady=4, ipady=6)

        # ── RIGHT TABLE ────────────────────────────────────────────────────────
        table_outer = tk.Frame(content, bg=Theme.CARD_BORDER, padx=1, pady=1)
        table_outer.grid(row=0, column=1, sticky="nsew")

        table_frame = tk.Frame(table_outer, bg=Theme.CARD_BG)
        table_frame.pack(fill="both", expand=True)

        tk.Label(
            table_frame,
            text="Payroll Records",
            bg=Theme.CARD_BG,
            fg=Theme.TEXT_DARK,
            font=Theme.SUBTITLE_FONT
        ).pack(anchor="w", padx=15, pady=(12, 5))

        style = ttk.Style()
        style.configure(
            "Payroll.Treeview",
            background=Theme.CARD_BG,
            foreground=Theme.TEXT_DARK,
            rowheight=32,
            fieldbackground=Theme.CARD_BG,
            font=("Segoe UI", 10)
        )
        style.configure(
            "Payroll.Treeview.Heading",
            background=Theme.SUCCESS,
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat"
        )
        style.map("Payroll.Treeview",
                  background=[("selected", Theme.ROW_SELECTED)])

        columns = ("ID", "Employee", "Period", "Gross Salary", "Net Salary", "Status")

        tc = tk.Frame(table_frame, bg=Theme.CARD_BG)
        tc.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.tree = ttk.Treeview(tc, columns=columns, show="headings",
                                  style="Payroll.Treeview")

        widths = {"ID": 50, "Employee": 150, "Period": 200,
                  "Gross Salary": 120, "Net Salary": 120, "Status": 90}
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=widths.get(col, 120))

        vsb = ttk.Scrollbar(tc, orient="vertical",   command=self.tree.yview)
        hsb = ttk.Scrollbar(tc, orient="horizontal",  command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        tc.rowconfigure(0, weight=1)
        tc.columnconfigure(0, weight=1)

        self.tree.tag_configure("odd",    background=Theme.ROW_ODD)
        self.tree.tag_configure("even",   background=Theme.ROW_EVEN)
        self.tree.tag_configure("locked", background="#FEE2E2")

    # ================= LOAD EMPLOYEES =================

    def load_employees(self):
        employees = self.employee_service.get_all_employees()
        values = []
        for emp in employees:
            display = f"{emp['id']} - {emp['first_name']} {emp['last_name']}"
            values.append(display)
            self.employee_map[display] = emp["id"]
        self.entries["employee"]["values"] = values

    # ================= LOAD PAYROLL =================

    def load_payroll_records(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        records = self.payroll_service.get_all_payroll()

        for i, record in enumerate(records):
            period = f"{record['start_date']} → {record['end_date']}"
            name   = f"{record['first_name']} {record['last_name']}"
            locked = record["is_locked"] == 1
            status = "🔒 Locked" if locked else "✅ Active"
            tag    = "locked" if locked else ("even" if i % 2 == 0 else "odd")

            self.tree.insert("", "end", tags=(tag,), values=(
                record["id"], name, period,
                f"Rs {record['gross_salary']:,.2f}",
                f"Rs {record['net_salary']:,.2f}",
                status
            ))

    # ================= PROCESS PAYROLL =================

    def process_payroll(self):
        try:
            emp_display = self.entries["employee"].get()
            employee_id = self.employee_map[emp_display]
            start_date  = self.entries["start_date"].get().strip()
            end_date    = self.entries["end_date"].get().strip()
            basic       = float(self.entries["basic"].get())
            total_days  = float(self.entries["total_days"].get())
            paid_days   = float(self.entries["paid_days"].get())
            overtime    = float(self.entries["overtime"].get()   or 0)
            bonus       = float(self.entries["bonus"].get()      or 0)
            special     = float(self.entries["special"].get()    or 0)
            conveyance  = float(self.entries["conveyance"].get() or 0)
            medical     = float(self.entries["medical"].get()    or 0)
            loan        = float(self.entries["loan"].get()       or 0)
        except Exception:
            messagebox.showerror("Error", "Please fill all required fields with valid values.")
            return

        existing = self.payroll_service.db.fetch_one(
            "SELECT id FROM payroll WHERE employee_id=? AND start_date=? AND end_date=?",
            (employee_id, start_date, end_date)
        )
        if existing:
            messagebox.showerror("Error", "Payroll already exists for this period.")
            return

        result = self.payroll_service.calculate_payroll(
            basic, total_days, paid_days, overtime,
            bonus, special, conveyance, medical, loan
        )
        self.payroll_service.save_payroll(
            employee_id, start_date, end_date,
            total_days, paid_days, overtime, result
        )
        messagebox.showinfo("Success", "Payroll processed successfully!")
        self.load_payroll_records()

    def lock_selected_payroll(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a payroll record first.")
            return
        payroll_id = self.tree.item(selected[0])["values"][0]
        if self.payroll_service.is_payroll_locked(payroll_id):
            messagebox.showerror("Error", "This payroll is already locked.")
            return
        if messagebox.askyesno("Confirm", "Lock this payroll? This cannot be undone."):
            self.payroll_service.lock_payroll(payroll_id)
            messagebox.showinfo("Success", "Payroll locked successfully.")
            self.load_payroll_records()

    def generate_selected_payslip(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a payroll record first.")
            return
        payroll_id = self.tree.item(selected[0])["values"][0]
        record     = self.payroll_service.get_payroll_by_id(payroll_id)
        file_path  = self.payroll_service.payslip_service.generate_payslip(record)
        messagebox.showinfo("Success", f"Payslip generated:\n{file_path}")
        try:
            if sys.platform == "win32":
                os.startfile(file_path)
            elif sys.platform == "darwin":
                subprocess.call(["open", file_path])
            else:
                subprocess.call(["xdg-open", file_path])
        except Exception:
            pass