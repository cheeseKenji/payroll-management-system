# 💼 Enterprise Role-Based Payroll Management System

A full-featured desktop Payroll Management System built with **Python**, **Tkinter**, and **SQLite**.  
Designed with a modern **Dark Navy + Blue UI theme** and complete role-based access control.

---

## 🖥️ Screenshots

> Login Screen → Dashboard → Employee Management → Payroll → Reports

---

## ✨ Features

- 🔐 **Role-Based Login** — Admin and HR roles with different permissions
- 👥 **Employee Management** — Add, edit, delete, search employees
- 💰 **Payroll Processing** — Calculate and manage monthly salaries
- 🧾 **Payslip Generation** — Generate payslips in PDF format
- 📊 **Reports & Export** — Export data to Excel and PDF
- 🕓 **Login History** — Track all user login activity
- 👤 **User Management** — Create and manage system users
- 🎨 **Modern Dark UI** — Custom Dark Navy + Blue themed interface

---

## 🛠️ Tech Stack

| Technology | Usage |
|------------|-------|
| Python 3.x | Core programming language |
| Tkinter | Desktop GUI framework |
| SQLite | Local database |
| openpyxl | Excel export |
| reportlab | PDF generation |
| python-docx | Word document support |
| hashlib | Password hashing |

---

## 📋 Requirements

**Python Version:** Python 3.8 or above

**Install all dependencies with this command:**

```bash
pip install openpyxl reportlab python-docx
```

> Tkinter and SQLite come built-in with Python — no separate install needed.

---

## 📁 Project Structure

```
PayrollSystem/
├── main.py                  # Entry point — run this file
├── config.py                # App configuration
├── setup_database.py        # Database setup and initialization
│
├── database/
│   └── db_manager.py        # Database connection manager
│
├── services/
│   ├── auth_service.py      # Login and authentication
│   ├── employee_service.py  # Employee CRUD operations
│   ├── payroll_service.py   # Payroll processing logic
│   ├── payslip_service.py   # Payslip generation
│   ├── report_service.py    # Report generation
│   └── export_service.py    # Excel and PDF export
│
├── ui/
│   ├── login_window.py      # Login screen UI
│   ├── dashboard.py         # Main dashboard UI
│   ├── employee_ui.py       # Employee management UI
│   ├── payroll_ui.py        # Payroll management UI
│   ├── user_ui.py           # User management UI
│   ├── reports_ui.py        # Reports UI
│   └── login_history_ui.py  # Login history UI
│
└── utils/
    ├── theme.py             # Dark Navy + Blue color theme
    ├── hashing.py           # Password hashing utility
    └── permission_manager.py # Role-based permissions
```

---

## 🚀 How to Run

**Step 1 — Clone the repository**
```bash
git clone https://github.com/cheeseKenji/payroll-management-system.git
cd payroll-management-system
```

**Step 2 — Install dependencies**
```bash
pip install openpyxl reportlab python-docx
```

**Step 3 — Run the application**
```bash
python main.py
```

---

## 🔑 Default Login Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | Admin@123 |

---

## 📌 Modules Overview

| Module | Description |
|--------|-------------|
| Login | Secure login with hashed passwords |
| Dashboard | Overview with stats and quick actions |
| Employee Management | Full CRUD for employee records |
| Payroll Management | Process and view salary records |
| Payslip | Generate and download payslips |
| Reports | Monthly and yearly reports |
| User Management | Add/edit/deactivate system users |
| Login History | View all past login activity |

---

## 👨‍💻 Developer

**Aniket Katke**  
BSc IT Final Year — Mumbai, Maharashtra  
📧 aniketkatke0709@gmail.com  
🌐 [Portfolio](https://cheeseKenji.github.io)  
💻 [GitHub](https://github.com/cheeseKenji)

---

## 📄 License

This project is open source and available for educational purposes.
