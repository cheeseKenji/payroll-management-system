from setup_database import initialize_database
from services.auth_service import AuthService
from database.db_manager import DatabaseManager
import tkinter as tk
from ui.login_window import LoginWindow


def create_default_admin():
    auth = AuthService()
    db = DatabaseManager()

    # Check if admin already exists
    existing = db.fetch_one("SELECT * FROM users WHERE username = ?", ("admin",))

    if not existing:
        success, message = auth.create_user(
            username="admin",
            password="Admin@123",
            role="Admin"
        )
        print("Admin created.")
    else:
        print("Admin already exists.")


def main():
    initialize_database()
    create_default_admin()

    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()

 
if __name__ == "__main__":
    main()