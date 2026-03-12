import os

# Base Directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Database Configuration
DATABASE_NAME = "payroll_system.db"
DATABASE_PATH = os.path.join(BASE_DIR, DATABASE_NAME)

# Application Settings
APP_NAME = "Enterprise Role-Based Payroll Management System"
APP_VERSION = "1.0.0"