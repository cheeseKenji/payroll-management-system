import tkinter as tk
from tkinter import ttk, messagebox
from services.employee_service import EmployeeService
from utils.theme import Theme


class EmployeeUI:

    def __init__(self, parent):
        self.parent = parent
        self.employee_service = EmployeeService()
        self.parent.configure(bg=Theme.MAIN_BG)
        self.build_layout()
        self.load_employees()

    # ================= LAYOUT =================

    def build_layout(self):

        # Page title
        title_bar = tk.Frame(self.parent, bg=Theme.PRIMARY, height=50)
        title_bar.pack(fill="x", padx=20, pady=(15, 10))
        title_bar.pack_propagate(False)
        tk.Label(
            title_bar,
            text="  Employee Management",
            bg=Theme.PRIMARY,
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
            text="Employee Details",
            bg=Theme.CARD_BG,
            fg=Theme.TEXT_DARK,
            font=Theme.SUBTITLE_FONT
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))

        fields = [
            ("First Name *", "first_name"),
            ("Last Name *",  "last_name"),
            ("Email",        "email"),
            ("Phone",        "phone"),
            ("Department",   "department"),
            ("Designation",  "designation"),
            ("Date of Joining\n(YYYY-MM-DD)", "doj"),
        ]

        self.entries = {}

        for i, (label, key) in enumerate(fields, start=1):
            tk.Label(
                form_frame,
                text=label,
                bg=Theme.CARD_BG,
                fg=Theme.TEXT_MID,
                font=Theme.LABEL_FONT,
                anchor="w"
            ).grid(row=i, column=0, sticky="w", pady=5, padx=(0, 10))

            entry = tk.Entry(
                form_frame,
                width=24,
                font=Theme.NORMAL_FONT,
                relief="solid",
                bd=1,
                highlightthickness=1,
                highlightcolor=Theme.PRIMARY,
                highlightbackground=Theme.CARD_BORDER
            )
            entry.grid(row=i, column=1, pady=5, ipady=5)
            self.entries[key] = entry

        # Buttons
        btn_frame = tk.Frame(form_frame, bg=Theme.CARD_BG)
        btn_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=(18, 0))

        for text, color, cmd in [
            ("Add Employee",    Theme.PRIMARY,        self.add_employee),
            ("Update Employee", Theme.WARNING,        self.update_employee),
            ("Delete Employee", Theme.DANGER,         self.delete_employee),
            ("Clear Form",      Theme.TEXT_LIGHT,     self.clear_form),
        ]:
            b = tk.Button(
                btn_frame,
                text=text,
                bg=color,
                fg="white",
                font=Theme.LABEL_FONT,
                relief="flat",
                width=20,
                cursor="hand2",
                command=cmd
            )
            b.pack(pady=4, ipady=6)

        # ── RIGHT TABLE ────────────────────────────────────────────────────────
        table_outer = tk.Frame(content, bg=Theme.CARD_BORDER, padx=1, pady=1)
        table_outer.grid(row=0, column=1, sticky="nsew")

        table_frame = tk.Frame(table_outer, bg=Theme.CARD_BG)
        table_frame.pack(fill="both", expand=True)

        tk.Label(
            table_frame,
            text="Employee Records",
            bg=Theme.CARD_BG,
            fg=Theme.TEXT_DARK,
            font=Theme.SUBTITLE_FONT
        ).pack(anchor="w", padx=15, pady=(12, 5))

        # Treeview style
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Custom.Treeview",
            background=Theme.CARD_BG,
            foreground=Theme.TEXT_DARK,
            rowheight=32,
            fieldbackground=Theme.CARD_BG,
            font=("Segoe UI", 10)
        )
        style.configure(
            "Custom.Treeview.Heading",
            background=Theme.PRIMARY,
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat"
        )
        style.map("Custom.Treeview",
                  background=[("selected", Theme.ROW_SELECTED)],
                  foreground=[("selected", Theme.TEXT_DARK)])

        columns = ("ID", "First Name", "Last Name", "Email", "Phone", "Department", "Designation")

        tree_container = tk.Frame(table_frame, bg=Theme.CARD_BG)
        tree_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.tree = ttk.Treeview(
            tree_container,
            columns=columns,
            show="headings",
            style="Custom.Treeview"
        )

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center",
                             width=60 if col == "ID" else 120)

        vsb = ttk.Scrollbar(tree_container, orient="vertical",   command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_container, orient="horizontal",  command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        tree_container.rowconfigure(0, weight=1)
        tree_container.columnconfigure(0, weight=1)

        self.tree.tag_configure("odd",  background=Theme.ROW_ODD)
        self.tree.tag_configure("even", background=Theme.ROW_EVEN)
        self.tree.bind("<<TreeviewSelect>>", self.on_row_select)

    # ================= LOAD =================

    def load_employees(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        employees = self.employee_service.get_all_employees()

        for i, emp in enumerate(employees):
            tag = "even" if i % 2 == 0 else "odd"
            self.tree.insert("", "end", tags=(tag,), values=(
                emp["id"], emp["first_name"], emp["last_name"],
                emp["email"], emp["phone"], emp["department"], emp["designation"]
            ))

    # ================= ON SELECT =================

    def on_row_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0])["values"]
        keys = ["first_name", "last_name", "email", "phone", "department", "designation", "doj"]
        for i, key in enumerate(keys):
            self.entries[key].delete(0, tk.END)
            if i + 1 < len(values):
                self.entries[key].insert(0, str(values[i + 1]))

    # ================= ACTIONS =================

    def add_employee(self):
        data = {k: v.get().strip() for k, v in self.entries.items()}
        if not data["first_name"] or not data["last_name"]:
            messagebox.showerror("Error", "First and Last Name are required.")
            return
        self.employee_service.add_employee(
            data["first_name"], data["last_name"], data["email"],
            data["phone"], data["department"], data["designation"], data["doj"]
        )
        messagebox.showinfo("Success", "Employee added successfully.")
        self.load_employees()
        self.clear_form()

    def update_employee(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select an employee to update.")
            return
        emp_id = self.tree.item(selected[0])["values"][0]
        data = {k: v.get().strip() for k, v in self.entries.items()}
        self.employee_service.update_employee(
            emp_id, data["first_name"], data["last_name"], data["email"],
            data["phone"], data["department"], data["designation"], data["doj"]
        )
        messagebox.showinfo("Success", "Employee updated successfully.")
        self.load_employees()

    def delete_employee(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select an employee to delete.")
            return
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this employee?"):
            return
        emp_id = self.tree.item(selected[0])["values"][0]
        self.employee_service.delete_employee(emp_id)
        messagebox.showinfo("Success", "Employee deleted successfully.")
        self.load_employees()
        self.clear_form()

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)