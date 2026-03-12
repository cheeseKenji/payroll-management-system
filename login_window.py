import tkinter as tk
from tkinter import messagebox
from services.auth_service import AuthService
from ui.dashboard import Dashboard


class LoginWindow:

    def __init__(self, root):
        self.root = root
        self.root.title("Enterprise Payroll System — Login")
        self.root.geometry("900x560")
        self.root.resizable(False, False)
        self.root.configure(bg="#0F172A")

        self.auth_service = AuthService()
        self.build_ui()

        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth()  - 900) // 2
        y = (self.root.winfo_screenheight() - 560) // 2
        self.root.geometry(f"900x560+{x}+{y}")

    # ================= BUILD UI =================

    def build_ui(self):

        # ── LEFT PANEL (branding) ──────────────────────────────────────────────
        left = tk.Frame(self.root, bg="#0F172A", width=420)
        left.pack(side="left", fill="y")
        left.pack_propagate(False)

        tk.Label(
            left,
            text="PAYROLL",
            bg="#0F172A",
            fg="#2563EB",
            font=("Segoe UI", 38, "bold")
        ).pack(pady=(100, 0))

        tk.Label(
            left,
            text="Management System",
            bg="#0F172A",
            fg="#CBD5E1",
            font=("Segoe UI", 14)
        ).pack(pady=(4, 0))

        tk.Frame(left, bg="#2563EB", height=3, width=180).pack(pady=20)

        tk.Label(
            left,
            text="Enterprise Role-Based\nPayroll Solution",
            bg="#0F172A",
            fg="#64748B",
            font=("Segoe UI", 11),
            justify="center"
        ).pack(pady=8)

        # Feature bullets
        features = [
            "✓  Secure Role-Based Access",
            "✓  Employee & Payroll Management",
            "✓  Reports & Multi-Format Export",
            "✓  Login History Tracking",
        ]
        for f in features:
            tk.Label(
                left,
                text=f,
                bg="#0F172A",
                fg="#94A3B8",
                font=("Segoe UI", 10),
                anchor="w"
            ).pack(anchor="w", padx=60, pady=3)

        tk.Label(
            left,
            text="BSc IT Final Year Project",
            bg="#0F172A",
            fg="#334155",
            font=("Segoe UI", 9)
        ).pack(side="bottom", pady=20)

        # ── RIGHT PANEL (login form) ───────────────────────────────────────────
        right = tk.Frame(self.root, bg="#F1F5F9")
        right.pack(side="right", fill="both", expand=True)

        # Card
        card = tk.Frame(right, bg="#FFFFFF", padx=40, pady=40)
        card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            card,
            text="Welcome Back",
            bg="#FFFFFF",
            fg="#0F172A",
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w")

        tk.Label(
            card,
            text="Sign in to your account",
            bg="#FFFFFF",
            fg="#94A3B8",
            font=("Segoe UI", 10)
        ).pack(anchor="w", pady=(2, 25))

        # Username field
        tk.Label(
            card,
            text="Username",
            bg="#FFFFFF",
            fg="#475569",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")

        self.username_entry = tk.Entry(
            card,
            width=30,
            font=("Segoe UI", 11),
            relief="solid",
            bd=1,
            highlightthickness=2,
            highlightcolor="#2563EB",
            highlightbackground="#E2E8F0"
        )
        self.username_entry.pack(pady=(4, 16), ipady=8)

        # Password field
        tk.Label(
            card,
            text="Password",
            bg="#FFFFFF",
            fg="#475569",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w")

        self.password_entry = tk.Entry(
            card,
            width=30,
            show="●",
            font=("Segoe UI", 11),
            relief="solid",
            bd=1,
            highlightthickness=2,
            highlightcolor="#2563EB",
            highlightbackground="#E2E8F0"
        )
        self.password_entry.pack(pady=(4, 24), ipady=8)

        # Login button
        login_btn = tk.Button(
            card,
            text="Sign In  →",
            bg="#2563EB",
            fg="#FFFFFF",
            font=("Segoe UI", 12, "bold"),
            relief="flat",
            width=28,
            cursor="hand2",
            command=self.login
        )
        login_btn.pack(ipady=10)
        login_btn.bind("<Enter>", lambda e: login_btn.config(bg="#1D4ED8"))
        login_btn.bind("<Leave>", lambda e: login_btn.config(bg="#2563EB"))

        tk.Label(
            card,
            text="Default: admin / Admin@123",
            bg="#FFFFFF",
            fg="#CBD5E1",
            font=("Segoe UI", 9)
        ).pack(pady=(14, 0))

        # Bind Enter key
        self.root.bind("<Return>", lambda e: self.login())
        self.username_entry.focus()

    # ================= LOGIN LOGIC =================

    def login(self):

        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please enter username and password.")
            return

        status, response = self.auth_service.authenticate_user(username, password)

        if status:
            self.root.destroy()
            dashboard_root = tk.Tk()
            Dashboard(dashboard_root, response)
            dashboard_root.mainloop()
        else:
            messagebox.showerror("Login Failed", response)
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus()