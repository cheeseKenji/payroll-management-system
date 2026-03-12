import sqlite3
from config import DATABASE_NAME


class DatabaseManager:

    def __init__(self):
        self.database = DATABASE_NAME

    # ================= CONNECTION =================

    def get_connection(self):
        try:
            conn = sqlite3.connect(self.database)
            conn.row_factory = sqlite3.Row   # 🔥 THIS LINE IS CRITICAL
            return conn
        except sqlite3.Error as e:
            print(f"Database Connection Error: {e}")
            return None

    # ================= EXECUTE =================

    def execute_query(self, query, params=()):
        conn = self.get_connection()
        if not conn:
            return False

        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database Query Error: {e}")
            return False
        finally:
            conn.close()

    # ================= FETCH ONE =================

    def fetch_one(self, query, params=()):
        conn = self.get_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            result = cursor.fetchone()
            return result
        except sqlite3.Error as e:
            print(f"Database Fetch Error: {e}")
            return None
        finally:
            conn.close()

    # ================= FETCH ALL =================

    def fetch_all(self, query, params=()):
        conn = self.get_connection()
        if not conn:
            return []

        try:
            cursor = conn.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"Database Fetch Error: {e}")
            return []
        finally:
            conn.close()