from database.db_manager import DatabaseManager
from utils.hashing import PasswordHasher
from datetime import datetime
import socket


class AuthService:

    def __init__(self):
        self.db = DatabaseManager()

    # ================= CREATE USER =================

    def create_user(self, username, password, role, employee_id=None):

        existing = self.db.fetch_one(
            "SELECT id FROM users WHERE username = ?",
            (username,)
        )

        if existing:
            return False, "Username already exists."

        hashed = PasswordHasher.hash_password(password)

        self.db.execute_query(
            """
            INSERT INTO users (username, password, role, employee_id, is_active)
            VALUES (?, ?, ?, ?, 1)
            """,
            (username, hashed, role, employee_id)
        )

        return True, "User created successfully."

    # ================= AUTHENTICATE USER =================

    def authenticate_user(self, username, password):

        user = self.db.fetch_one(
            """
            SELECT id, username, password, role, is_active
            FROM users
            WHERE username = ?
            """,
            (username,)
        )

        if not user:
            return False, "Invalid username or password."

        if user["is_active"] == 0:
            return False, "User account is inactive."

        if not PasswordHasher.verify_password(user["password"], password):
            return False, "Invalid username or password."

        # ── Log login history ──────────────────────────────────────────────────
        try:
            ip = socket.gethostbyname(socket.gethostname())
        except Exception:
            ip = "127.0.0.1"

        self.db.execute_query(
            """
            INSERT INTO login_history (user_id, login_time, ip_address)
            VALUES (?, ?, ?)
            """,
            (user["id"], datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ip)
        )

        return True, {
            "id":       user["id"],
            "username": user["username"],
            "role":     user["role"]
        }

    # ================= RESET PASSWORD =================

    def reset_password(self, user_id, new_password):

        hashed = PasswordHasher.hash_password(new_password)

        self.db.execute_query(
            "UPDATE users SET password = ? WHERE id = ?",
            (hashed, user_id)
        )

        return True, "Password reset successfully."

    # ================= ACTIVATE / DEACTIVATE =================

    def toggle_user_status(self, user_id, status):

        self.db.execute_query(
            "UPDATE users SET is_active = ? WHERE id = ?",
            (status, user_id)
        )

        return True, "User status updated."

    # Alias used in user_ui.py
    def update_user_status(self, user_id, status):
        return self.toggle_user_status(user_id, status)

    # ================= GET ALL USERS =================

    def get_all_users(self):

        return self.db.fetch_all(
            """
            SELECT
                u.id,
                u.username,
                u.role,
                u.is_active,
                e.first_name,
                e.last_name
            FROM users u
            LEFT JOIN employees e ON u.employee_id = e.id
            """
        )
