import tkinter as tk
from tkinter import ttk
from database.db_manager import DatabaseManager
from utils.theme import Theme


class LoginHistoryUI:

    def __init__(self, parent):
        self.parent = parent
        self.db = DatabaseManager()
        self.parent.configure(bg=Theme.MAIN_BG)
        self.build_ui()
        self.load_history()

    def build_ui(self):

        tk.Label(
            self.parent,
            text="Login History",
            bg=Theme.MAIN_BG,
            font=Theme.TITLE_FONT
        ).pack(pady=(20, 10))

        # Filter bar
        filter_frame = tk.Frame(self.parent, bg=Theme.CARD_BG, bd=1, relief="solid")
        filter_frame.pack(fill="x", padx=20, pady=5)

        tk.Label(filter_frame, text="Search Username:", bg=Theme.CARD_BG,
                 font=Theme.NORMAL_FONT).pack(side="left", padx=10, pady=8)
        self.search_entry = tk.Entry(filter_frame, width=24)
        self.search_entry.pack(side="left", padx=5, pady=8)

        tk.Button(
            filter_frame,
            text="Search",
            bg=Theme.PRIMARY,
            fg=Theme.BUTTON_TEXT,
            relief="flat",
            font=Theme.NORMAL_FONT,
            command=self.load_history
        ).pack(side="left", padx=8, pady=8)

        tk.Button(
            filter_frame,
            text="Clear",
            bg=Theme.BUTTON_BG,
            fg=Theme.BUTTON_TEXT,
            relief="flat",
            font=Theme.NORMAL_FONT,
            command=self.clear_search
        ).pack(side="left", padx=4, pady=8)

        # Table
        table_frame = tk.Frame(self.parent, bg=Theme.CARD_BG, bd=1, relief="solid")
        table_frame.pack(fill="both", expand=True, padx=20, pady=(5, 20))

        columns = ("ID", "Username", "Role", "Login Time", "IP Address")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=160)

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        table_frame.rowconfigure(0, weight=1)
        table_frame.columnconfigure(0, weight=1)

    def load_history(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        search = self.search_entry.get().strip() if hasattr(self, "search_entry") else ""

        if search:
            query = """
                SELECT lh.id, u.username, u.role, lh.login_time, lh.ip_address
                FROM login_history lh
                JOIN users u ON lh.user_id = u.id
                WHERE u.username LIKE ?
                ORDER BY lh.login_time DESC
            """
            rows = self.db.fetch_all(query, (f"%{search}%",))
        else:
            query = """
                SELECT lh.id, u.username, u.role, lh.login_time, lh.ip_address
                FROM login_history lh
                JOIN users u ON lh.user_id = u.id
                ORDER BY lh.login_time DESC
                LIMIT 200
            """
            rows = self.db.fetch_all(query)

        for row in rows:
            self.tree.insert("", "end", values=(
                row["id"],
                row["username"],
                row["role"],
                row["login_time"],
                row["ip_address"] or "N/A"
            ))

    def clear_search(self):
        self.search_entry.delete(0, tk.END)
        self.load_history()
