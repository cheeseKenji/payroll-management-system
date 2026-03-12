import tkinter as tk
from tkinter import messagebox

from ui.employee_ui import EmployeeUI
from ui.payroll_ui import PayrollUI
from ui.user_ui import UserUI
from ui.reports_ui import ReportsUI
from ui.login_history_ui import LoginHistoryUI
from utils.permission_manager import PermissionManager
from utils.theme import Theme
from services.payroll_service import PayrollService
from services.employee_service import EmployeeService


class Dashboard:

    def __init__(self, root, user_data):
        self.root = root
        self.user_data = user_data
        self.role = user_data["role"]

        self.root.title("Enterprise Payroll System")
        self.root.geometry("1280x750")
        self.root.configure(bg=Theme.MAIN_BG)

        self.payroll_service  = PayrollService()
        self.employee_service = EmployeeService()

        self.sidebar = None
        self.content = None
        self.sidebar_buttons = {}
        self.active_button = None

        self.build_layout()

    # ================= BUILD LAYOUT =================

    def build_layout(self):

        self.sidebar = tk.Frame(self.root, bg=Theme.SIDEBAR_BG, width=230)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        main_area = tk.Frame(self.root, bg=Theme.MAIN_BG)
        main_area.pack(side="right", fill="both", expand=True)

        self.content = tk.Frame(main_area, bg=Theme.MAIN_BG)
        self.content.pack(fill="both", expand=True)

        footer = tk.Frame(main_area, bg=Theme.CARD_BG, height=32)
        footer.pack(fill="x")
        tk.Label(
            footer,
            text="Enterprise Payroll System v1.0  |  Developed for BSc IT Final Year Project",
            bg=Theme.CARD_BG,
            font=("Arial", 9),
            fg="#888888"
        ).pack(pady=7)

        self.build_sidebar()
        self.handle_sidebar_click("Dashboard", self.show_dashboard_summary)

    # ================= SIDEBAR =================

    def build_sidebar(self):

        # App title
        title_frame = tk.Frame(self.sidebar, bg=Theme.SIDEBAR_BG)
        title_frame.pack(fill="x", pady=(20, 5))

        tk.Label(
            title_frame,
            text="PAYROLL",
            bg=Theme.SIDEBAR_BG,
            fg=Theme.PRIMARY,
            font=("Arial", 16, "bold")
        ).pack()

        tk.Label(
            title_frame,
            text="Management System",
            bg=Theme.SIDEBAR_BG,
            fg=Theme.SIDEBAR_TEXT,
            font=("Arial", 9)
        ).pack()

        tk.Frame(self.sidebar, bg="#374151", height=1).pack(fill="x", padx=15, pady=10)

        # User info
        tk.Label(
            self.sidebar,
            text=f"  {self.user_data['username']}",
            bg=Theme.SIDEBAR_BG,
            fg="#9CA3AF",
            font=("Arial", 10)
        ).pack(anchor="w", padx=10)

        tk.Label(
            self.sidebar,
            text=f"  Role: {self.role}",
            bg=Theme.SIDEBAR_BG,
            fg="#6B7280",
            font=("Arial", 9)
        ).pack(anchor="w", padx=10, pady=(0, 10))

        tk.Frame(self.sidebar, bg="#374151", height=1).pack(fill="x", padx=15, pady=5)

        # Nav buttons
        self.create_sidebar_button("Dashboard",          self.show_dashboard_summary)

        if PermissionManager.has_permission(self.role, "employee_access"):
            self.create_sidebar_button("Employee Management", self.load_employee_module)

        if PermissionManager.has_permission(self.role, "payroll_access"):
            self.create_sidebar_button("Payroll Management",  self.load_payroll_module)

        if PermissionManager.has_permission(self.role, "user_management_access"):
            self.create_sidebar_button("User Management",     self.load_user_module)
            self.create_sidebar_button("Login History",       self.load_login_history)

        if PermissionManager.has_permission(self.role, "payroll_access"):
            self.create_sidebar_button("Reports & Export",    self.load_reports_module)

        tk.Frame(self.sidebar, bg="#374151", height=1).pack(fill="x", padx=15, pady=10)

        self.create_sidebar_button("Logout", self.logout)

    def create_sidebar_button(self, text, command):

        btn = tk.Button(
            self.sidebar,
            text=f"  {text}",
            bg=Theme.SIDEBAR_BG,
            fg=Theme.SIDEBAR_TEXT,
            relief="flat",
            anchor="w",
            width=24,
            font=Theme.NORMAL_FONT,
            command=lambda: self.handle_sidebar_click(text, command)
        )
        btn.pack(fill="x", padx=8, pady=2)
        self.sidebar_buttons[text] = btn

        btn.bind("<Enter>", lambda e, b=btn: self.on_hover(b))
        btn.bind("<Leave>", lambda e, b=btn: self.on_leave(b))

    def handle_sidebar_click(self, text, command):
        self.set_active(text)
        command()

    def set_active(self, text):
        if self.active_button:
            self.active_button.configure(bg=Theme.SIDEBAR_BG, fg=Theme.SIDEBAR_TEXT)

        btn = self.sidebar_buttons.get(text)
        if btn:
            btn.configure(bg=Theme.PRIMARY, fg="white")
            self.active_button = btn

    def on_hover(self, btn):
        if btn != self.active_button:
            btn.configure(bg="#374151")

    def on_leave(self, btn):
        if btn != self.active_button:
            btn.configure(bg=Theme.SIDEBAR_BG)

    # ================= CONTENT CONTROL =================

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    # ================= DASHBOARD SUMMARY =================

    def show_dashboard_summary(self):

        self.clear_content()

        # Header
        header = tk.Frame(self.content, bg=Theme.PRIMARY)
        header.pack(fill="x", padx=20, pady=(20, 10))

        tk.Label(
            header,
            text=f"  Welcome back, {self.user_data['username']}!",
            bg=Theme.PRIMARY,
            fg="white",
            font=("Arial", 16, "bold")
        ).pack(side="left", padx=15, pady=12)

        tk.Label(
            header,
            text=f"Role: {self.role}",
            bg=Theme.PRIMARY,
            fg="#BFDBFE",
            font=("Arial", 10)
        ).pack(side="right", padx=15, pady=12)

        # Summary cards
        payroll_summary  = self.payroll_service.get_dashboard_summary()
        employee_count   = self.employee_service.get_employee_count()

        cards_data = [
            ("Total Employees",    str(employee_count),                          "#2563EB"),
            ("Payroll Records",    str(payroll_summary["total_records"]),         "#16A34A"),
            ("Total Gross Paid",   f"Rs {payroll_summary['total_gross']:,.2f}",  "#D97706"),
            ("Total Net Paid",     f"Rs {payroll_summary['total_net']:,.2f}",    "#7C3AED"),
            ("Total Deductions",   f"Rs {payroll_summary['total_deductions']:,.2f}", "#DC2626"),
            ("Locked Payrolls",    str(payroll_summary["locked_count"]),          "#0891B2"),
        ]

        cards_frame = tk.Frame(self.content, bg=Theme.MAIN_BG)
        cards_frame.pack(fill="x", padx=20, pady=10)

        for i, (label, value, color) in enumerate(cards_data):
            card = tk.Frame(cards_frame, bg=color, width=180, height=100)
            card.grid(row=i // 3, column=i % 3, padx=8, pady=8, sticky="nsew")
            card.grid_propagate(False)

            tk.Label(card, text=value, bg=color, fg="white",
                     font=("Arial", 18, "bold")).pack(pady=(18, 4))
            tk.Label(card, text=label, bg=color, fg="white",
                     font=("Arial", 10)).pack()

        for col in range(3):
            cards_frame.columnconfigure(col, weight=1)

        # Quick actions
        qa_frame = tk.Frame(self.content, bg=Theme.CARD_BG, bd=1, relief="solid")
        qa_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(qa_frame, text="Quick Actions", bg=Theme.CARD_BG,
                 font=Theme.SUBTITLE_FONT).pack(anchor="w", padx=15, pady=(10, 5))

        btn_row = tk.Frame(qa_frame, bg=Theme.CARD_BG)
        btn_row.pack(padx=15, pady=(0, 12))

        quick_actions = []

        if PermissionManager.has_permission(self.role, "employee_access"):
            quick_actions.append(("Add Employee", self.load_employee_module))
        if PermissionManager.has_permission(self.role, "payroll_access"):
            quick_actions.append(("Process Payroll", self.load_payroll_module))
            quick_actions.append(("View Reports", self.load_reports_module))

        for label, cmd in quick_actions:
            tk.Button(
                btn_row,
                text=label,
                bg=Theme.PRIMARY,
                fg="white",
                relief="flat",
                font=Theme.NORMAL_FONT,
                width=18,
                command=cmd
            ).pack(side="left", padx=6)

    # ================= MODULE LOADERS =================

    def load_employee_module(self):
        self.clear_content()
        EmployeeUI(self.content)

    def load_payroll_module(self):
        self.clear_content()
        PayrollUI(self.content)

    def load_user_module(self):
        self.clear_content()
        UserUI(self.content)

    def load_reports_module(self):
        self.clear_content()
        ReportsUI(self.content)

    def load_login_history(self):
        self.clear_content()
        LoginHistoryUI(self.content)

    # ================= LOGOUT =================

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.destroy()
            from ui.login_window import LoginWindow
            import tkinter as tk
            new_root = tk.Tk()
            LoginWindow(new_root)
            new_root.mainloop()
