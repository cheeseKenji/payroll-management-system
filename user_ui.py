import tkinter as tk
from tkinter import ttk, messagebox

from services.auth_service import AuthService
from services.employee_service import EmployeeService
from utils.theme import Theme


class UserUI:

    def __init__(self, parent):
        self.parent = parent
        self.auth_service     = AuthService()
        self.employee_service = EmployeeService()
        self.selected_user_id = None
        self.parent.configure(bg=Theme.MAIN_BG)
        self.build_ui()
        self.load_users()

    def build_ui(self):

        # Title bar
        title_bar = tk.Frame(self.parent, bg=Theme.PURPLE, height=50)
        title_bar.pack(fill="x", padx=20, pady=(15, 10))
        title_bar.pack_propagate(False)
        tk.Label(
            title_bar,
            text="  User Management",
            bg=Theme.PURPLE,
            fg="white",
            font=Theme.SUBTITLE_FONT
        ).pack(side="left", padx=15, pady=10)

        content = tk.Frame(self.parent, bg=Theme.MAIN_BG)
        content.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        # ── LEFT FORM ─────────────────────────────────────────────────────────
        form_outer = tk.Frame(content, bg=Theme.CARD_BORDER, padx=1, pady=1)
        form_outer.pack(side="left", fill="y", padx=(0, 10))

        form_frame = tk.Frame(form_outer, bg=Theme.CARD_BG, padx=24, pady=24)
        form_frame.pack(fill="both", expand=True)

        tk.Label(
            form_frame,
            text="Create / Manage User",
            bg=Theme.CARD_BG,
            fg=Theme.TEXT_DARK,
            font=Theme.SUBTITLE_FONT
        ).pack(anchor="w", pady=(0, 15))

        def field(label_text, widget_fn):
            tk.Label(
                form_frame,
                text=label_text,
                bg=Theme.CARD_BG,
                fg=Theme.TEXT_MID,
                font=Theme.LABEL_FONT,
                anchor="w"
            ).pack(anchor="w", pady=(8, 2))
            w = widget_fn()
            w.pack(fill="x", ipady=5)
            return w

        self.username_entry = field("Username *", lambda: tk.Entry(
            form_frame, width=28, font=Theme.NORMAL_FONT,
            relief="solid", bd=1,
            highlightthickness=1,
            highlightcolor=Theme.PRIMARY,
            highlightbackground=Theme.CARD_BORDER
        ))

        self.password_entry = field("Password *", lambda: tk.Entry(
            form_frame, width=28, show="●", font=Theme.NORMAL_FONT,
            relief="solid", bd=1,
            highlightthickness=1,
            highlightcolor=Theme.PRIMARY,
            highlightbackground=Theme.CARD_BORDER
        ))

        tk.Label(form_frame, text="Role *", bg=Theme.CARD_BG,
                 fg=Theme.TEXT_MID, font=Theme.LABEL_FONT, anchor="w").pack(anchor="w", pady=(8, 2))
        self.role_combobox = ttk.Combobox(
            form_frame,
            values=["Admin", "HR", "Employee"],
            state="readonly", width=26, font=Theme.LABEL_FONT
        )
        self.role_combobox.pack(fill="x", ipady=3)
        self.role_combobox.bind("<<ComboboxSelected>>", self.on_role_change)

        tk.Label(form_frame, text="Link Employee (if Employee role)",
                 bg=Theme.CARD_BG, fg=Theme.TEXT_MID,
                 font=Theme.LABEL_FONT, anchor="w").pack(anchor="w", pady=(8, 2))
        self.employee_combobox = ttk.Combobox(
            form_frame, state="disabled", width=26, font=Theme.LABEL_FONT
        )
        self.employee_combobox.pack(fill="x", ipady=3)

        tk.Frame(form_frame, bg=Theme.CARD_BORDER, height=1).pack(fill="x", pady=16)

        for text, color, cmd in [
            ("Create User",         Theme.PRIMARY,  self.create_user),
            ("Reset Password",      Theme.SUCCESS,  self.reset_password),
            ("Activate/Deactivate", Theme.DANGER,   self.toggle_user_status),
        ]:
            b = tk.Button(
                form_frame, text=text, bg=color, fg="white",
                font=Theme.LABEL_FONT, relief="flat",
                width=24, cursor="hand2", command=cmd
            )
            b.pack(pady=4, ipady=7)

        self.load_employee_dropdown()

        # ── RIGHT TABLE ────────────────────────────────────────────────────────
        table_outer = tk.Frame(content, bg=Theme.CARD_BORDER, padx=1, pady=1)
        table_outer.pack(side="right", fill="both", expand=True)

        table_frame = tk.Frame(table_outer, bg=Theme.CARD_BG)
        table_frame.pack(fill="both", expand=True)

        tk.Label(
            table_frame,
            text="System Users",
            bg=Theme.CARD_BG,
            fg=Theme.TEXT_DARK,
            font=Theme.SUBTITLE_FONT
        ).pack(anchor="w", padx=15, pady=(12, 5))

        style = ttk.Style()
        style.configure(
            "User.Treeview",
            background=Theme.CARD_BG,
            foreground=Theme.TEXT_DARK,
            rowheight=32,
            fieldbackground=Theme.CARD_BG,
            font=("Segoe UI", 10)
        )
        style.configure(
            "User.Treeview.Heading",
            background=Theme.PURPLE,
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat"
        )
        style.map("User.Treeview",
                  background=[("selected", Theme.ROW_SELECTED)])

        columns = ("ID", "Username", "Role", "Employee", "Status")
        tc = tk.Frame(table_frame, bg=Theme.CARD_BG)
        tc.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.tree = ttk.Treeview(tc, columns=columns, show="headings",
                                  style="User.Treeview")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=140)

        vsb = ttk.Scrollbar(tc, orient="vertical",   command=self.tree.yview)
        hsb = ttk.Scrollbar(tc, orient="horizontal",  command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        tc.rowconfigure(0, weight=1)
        tc.columnconfigure(0, weight=1)

        self.tree.tag_configure("odd",      background=Theme.ROW_ODD)
        self.tree.tag_configure("even",     background=Theme.ROW_EVEN)
        self.tree.tag_configure("inactive", background="#FEE2E2")
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

    # ================= LOAD DATA =================

    def load_users(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        users = self.auth_service.get_all_users()
        for i, user in enumerate(users):
            active = user["is_active"] == 1
            status = "✅ Active" if active else "❌ Inactive"
            emp_name = f"{user['first_name']} {user['last_name']}" if user["first_name"] else "—"
            tag = ("even" if i % 2 == 0 else "odd") if active else "inactive"
            self.tree.insert("", "end", tags=(tag,), values=(
                user["id"], user["username"], user["role"], emp_name, status
            ))

    def load_employee_dropdown(self):
        employees = self.employee_service.get_all_employees()
        self.employee_combobox["values"] = [
            f"{e['id']} - {e['first_name']} {e['last_name']}" for e in employees
        ]

    # ================= EVENTS =================

    def on_role_change(self, event):
        if self.role_combobox.get() == "Employee":
            self.employee_combobox.config(state="readonly")
        else:
            self.employee_combobox.set("")
            self.employee_combobox.config(state="disabled")

    def on_row_select(self, event):
        selected = self.tree.selection()
        if selected:
            self.selected_user_id = self.tree.item(selected[0])["values"][0]

    # ================= ACTIONS =================

    def create_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        role     = self.role_combobox.get()

        if not username or not password or not role:
            messagebox.showerror("Error", "Username, Password and Role are required.")
            return

        employee_id = None
        if role == "Employee":
            emp_val = self.employee_combobox.get()
            if not emp_val:
                messagebox.showerror("Error", "Select an employee for Employee role.")
                return
            employee_id = int(emp_val.split(" - ")[0])

        success, message = self.auth_service.create_user(username, password, role, employee_id)
        if success:
            messagebox.showinfo("Success", message)
            self.clear_form()
            self.load_users()
        else:
            messagebox.showerror("Error", message)

    def reset_password(self):
        if not self.selected_user_id:
            messagebox.showerror("Error", "Select a user first.")
            return
        new_password = self.password_entry.get().strip()
        if not new_password:
            messagebox.showerror("Error", "Enter the new password in the Password field.")
            return
        self.auth_service.reset_password(self.selected_user_id, new_password)
        messagebox.showinfo("Success", "Password reset successfully.")
        self.password_entry.delete(0, tk.END)

    def toggle_user_status(self):
        if not self.selected_user_id:
            messagebox.showerror("Error", "Select a user first.")
            return
        selected = self.tree.selection()
        values   = self.tree.item(selected[0])["values"]
        current  = values[4]
        new_status = 0 if "Active" in current else 1
        self.auth_service.update_user_status(self.selected_user_id, new_status)
        messagebox.showinfo("Success", "User status updated.")
        self.load_users()

    def clear_form(self):
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.role_combobox.set("")
        self.employee_combobox.set("")
        self.employee_combobox.config(state="disabled")
        self.selected_user_id = None