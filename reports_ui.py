import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import subprocess

from services.report_service import ReportService
from services.export_service import ExportService
from utils.theme import Theme


class ReportsUI:

    def __init__(self, parent):
        self.parent = parent
        self.report_service = ReportService()
        self.export_service = ExportService()
        self.current_rows = []
        self.current_columns = []

        self.parent.configure(bg=Theme.MAIN_BG)
        self.build_layout()

    # ================= LAYOUT =================

    def build_layout(self):

        # ── FILTER PANEL ──────────────────────────────────────────────────────
        filter_card = tk.Frame(self.parent, bg=Theme.CARD_BG, bd=1, relief="solid")
        filter_card.pack(fill="x", padx=20, pady=(15, 5))

        tk.Label(
            filter_card,
            text="Reports Portal",
            bg=Theme.CARD_BG,
            font=Theme.TITLE_FONT
        ).grid(row=0, column=0, columnspan=6, sticky="w", padx=15, pady=(10, 5))

        tk.Label(filter_card, text="Report Type:", bg=Theme.CARD_BG,
                 font=Theme.NORMAL_FONT).grid(row=1, column=0, padx=(15, 5), pady=8, sticky="w")

        self.report_type = ttk.Combobox(
            filter_card,
            values=["Payroll Summary", "Employee List", "Department Payroll", "Monthly Report"],
            state="readonly", width=22
        )
        self.report_type.set("Payroll Summary")
        self.report_type.grid(row=1, column=1, padx=5, pady=8)

        tk.Label(filter_card, text="Start Date (YYYY-MM-DD):", bg=Theme.CARD_BG,
                 font=Theme.NORMAL_FONT).grid(row=1, column=2, padx=(15, 5), pady=8, sticky="w")
        self.start_date = tk.Entry(filter_card, width=16)
        self.start_date.grid(row=1, column=3, padx=5, pady=8)

        tk.Label(filter_card, text="End Date (YYYY-MM-DD):", bg=Theme.CARD_BG,
                 font=Theme.NORMAL_FONT).grid(row=1, column=4, padx=(15, 5), pady=8, sticky="w")
        self.end_date = tk.Entry(filter_card, width=16)
        self.end_date.grid(row=1, column=5, padx=5, pady=8)

        tk.Label(filter_card, text="Department (Optional):", bg=Theme.CARD_BG,
                 font=Theme.NORMAL_FONT).grid(row=2, column=0, padx=(15, 5), pady=8, sticky="w")
        self.department = tk.Entry(filter_card, width=22)
        self.department.grid(row=2, column=1, padx=5, pady=8)

        tk.Label(filter_card, text="Employee ID (Optional):", bg=Theme.CARD_BG,
                 font=Theme.NORMAL_FONT).grid(row=2, column=2, padx=(15, 5), pady=8, sticky="w")
        self.employee_id = tk.Entry(filter_card, width=16)
        self.employee_id.grid(row=2, column=3, padx=5, pady=8)

        tk.Button(
            filter_card,
            text="Generate Report",
            bg=Theme.PRIMARY,
            fg=Theme.BUTTON_TEXT,
            activebackground=Theme.BUTTON_HOVER,
            font=Theme.NORMAL_FONT,
            relief="flat",
            width=20,
            command=self.generate_report
        ).grid(row=2, column=4, columnspan=2, padx=15, pady=8)

        # ── SUMMARY CARDS ──────────────────────────────────────────────────────
        self.summary_frame = tk.Frame(self.parent, bg=Theme.MAIN_BG)
        self.summary_frame.pack(fill="x", padx=20, pady=5)

        # ── EXPORT BUTTONS ─────────────────────────────────────────────────────
        export_frame = tk.Frame(self.parent, bg=Theme.CARD_BG, bd=1, relief="solid")
        export_frame.pack(fill="x", padx=20, pady=5)

        tk.Label(export_frame, text="Export As:", bg=Theme.CARD_BG,
                 font=Theme.NORMAL_FONT).pack(side="left", padx=15, pady=8)

        for label, cmd in [
            ("CSV",      self.export_csv),
            ("Excel",    self.export_excel),
            ("PDF",      self.export_pdf),
            ("Word",     self.export_word),
            ("DB Backup",self.export_db),
        ]:
            tk.Button(
                export_frame,
                text=label,
                bg=Theme.BUTTON_BG,
                fg=Theme.BUTTON_TEXT,
                activebackground=Theme.BUTTON_HOVER,
                relief="flat",
                font=Theme.NORMAL_FONT,
                width=12,
                command=cmd
            ).pack(side="left", padx=6, pady=8)

        # ── RESULTS TABLE ──────────────────────────────────────────────────────
        table_frame = tk.Frame(self.parent, bg=Theme.CARD_BG, bd=1, relief="solid")
        table_frame.pack(fill="both", expand=True, padx=20, pady=(5, 15))

        self.tree = ttk.Treeview(table_frame, show="headings")
        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

        self.status_var = tk.StringVar(value="Generate a report to see results.")
        tk.Label(
            self.parent,
            textvariable=self.status_var,
            bg=Theme.MAIN_BG,
            font=("Arial", 9),
            fg="#888888"
        ).pack(anchor="w", padx=22)

    # ================= SUMMARY CARDS =================

    def _show_summary_cards(self, stats):
        for w in self.summary_frame.winfo_children():
            w.destroy()

        if not stats:
            return

        items = [
            ("Employees",   str(stats["total_employees"]  or 0)),
            ("Payrolls",    str(stats["total_payrolls"]   or 0)),
            ("Total Gross", f"Rs {stats['total_gross'] or 0:,.2f}"),
            ("Deductions",  f"Rs {stats['total_deductions'] or 0:,.2f}"),
            ("Total Net",   f"Rs {stats['total_net']   or 0:,.2f}"),
        ]

        card_colors = ["#2563EB", "#16A34A", "#D97706", "#DC2626", "#7C3AED"]

        for (label, value), color in zip(items, card_colors):
            card = tk.Frame(self.summary_frame, bg=color)
            card.pack(side="left", expand=True, fill="both", padx=5, pady=5)
            tk.Label(card, text=value, bg=color, fg="white",
                     font=("Arial", 13, "bold")).pack(pady=(10, 2))
            tk.Label(card, text=label, bg=color, fg="white",
                     font=("Arial", 9)).pack(pady=(0, 10))

    # ================= LOAD TABLE =================

    def _load_table(self, columns, rows):
        self.current_columns = columns
        self.current_rows    = rows

        self.tree["columns"] = columns
        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, anchor="center", width=130)

        for row in self.tree.get_children():
            self.tree.delete(row)

        for row in rows:
            self.tree.insert("", "end", values=[row[c] for c in columns])

        self.status_var.set(f"{len(rows)} record(s) found.")

    # ================= GENERATE REPORT =================

    def generate_report(self):

        sd   = self.start_date.get().strip() or None
        ed   = self.end_date.get().strip()   or None
        dept = self.department.get().strip()  or None
        emp  = self.employee_id.get().strip() or None

        rtype = self.report_type.get()

        if rtype == "Payroll Summary":
            rows = self.report_service.get_payroll_summary(sd, ed, dept, emp)
            cols = ["emp_id", "employee_name", "department", "designation",
                    "start_date", "end_date", "gross_salary",
                    "total_deductions", "net_salary", "status"]

        elif rtype == "Employee List":
            rows = self.report_service.get_employee_report(dept, emp)
            cols = ["id", "employee_name", "email", "phone",
                    "department", "designation", "date_of_joining"]

        elif rtype == "Department Payroll":
            rows = self.report_service.get_department_report(sd, ed, dept)
            cols = ["department", "total_employees", "total_payrolls",
                    "total_gross", "total_deductions", "total_net"]

        elif rtype == "Monthly Report":
            rows = self.report_service.get_monthly_report(sd, ed, dept)
            cols = ["month", "total_employees", "total_gross",
                    "total_deductions", "total_net", "locked_count"]

        else:
            messagebox.showerror("Error", "Select a report type.")
            return

        if not rows:
            messagebox.showinfo("No Data", "No records found for selected filters.")
            self.status_var.set("No records found.")
            return

        if rtype in ("Payroll Summary", "Department Payroll", "Monthly Report"):
            stats = self.report_service.get_summary_stats(sd, ed, dept, emp)
            self._show_summary_cards(stats)

        self._load_table(cols, rows)

    # ================= EXPORT =================

    def _check_data(self):
        if not self.current_rows:
            messagebox.showerror("Error", "Generate a report first before exporting.")
            return False
        return True

    def _open_file(self, path):
        try:
            if sys.platform == "win32":
                os.startfile(path)
            elif sys.platform == "darwin":
                subprocess.call(["open", path])
            else:
                subprocess.call(["xdg-open", path])
        except Exception:
            pass

    def export_csv(self):
        if not self._check_data():
            return
        path = self.export_service.export_csv(
            self.current_columns, self.current_rows, "payroll_report")
        messagebox.showinfo("Exported", f"CSV saved:\n{path}")
        self._open_file(path)

    def export_excel(self):
        if not self._check_data():
            return
        path = self.export_service.export_excel(
            self.current_columns, self.current_rows, "payroll_report")
        messagebox.showinfo("Exported", f"Excel saved:\n{path}")
        self._open_file(path)

    def export_pdf(self):
        if not self._check_data():
            return
        path = self.export_service.export_pdf(
            self.current_columns, self.current_rows,
            "payroll_report", self.report_type.get())
        messagebox.showinfo("Exported", f"PDF saved:\n{path}")
        self._open_file(path)

    def export_word(self):
        if not self._check_data():
            return
        path = self.export_service.export_word(
            self.current_columns, self.current_rows,
            "payroll_report", self.report_type.get())
        messagebox.showinfo("Exported", f"Word doc saved:\n{path}")
        self._open_file(path)

    def export_db(self):
        path = self.export_service.export_db_backup()
        messagebox.showinfo("Backup Done", f"Database backup saved:\n{path}")
