# 🏢 HR Automation Suite
### High-Security HR Department — HRD Division

A secure, LAN-based Python + Flask web application to automate HR operations for the Unpaid Internship lifecycle. Built to replace manual Excel tracking with a clean, modern web interface.

---

## ✨ Features (Current)

- 📄 **ION Notice Generator** — Fill a form and auto-generate official notices in DOCX format
- 👁 **Live Preview** — Preview the notice before downloading
- 🏢 **Department Manager** — Add, edit, delete departments permanently
- 📥 **DOCX Download** — Download formatted Word documents ready for printing
- 🌐 **LAN Accessible** — Runs on local network, accessible from any browser

## 🚀 Features (Coming Soon)

- 📊 Applicant Intake & Document Validation
- 🎯 Group Allocation Algorithm
- 📋 Master Internship Ledger
- 📄 PDF Generation
- 🗄️ Full PostgreSQL Database Integration

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.12.5 |
| Web Framework | Flask |
| Database | PostgreSQL 17 |
| Document Generation | python-docx |
| PDF Generation | ReportLab |
| Frontend | HTML + CSS (Vanilla) |

---

## 📁 Project Structure

```
hr-automation-suite/
├── .devcontainer/
│   ├── devcontainer.json       ← GitHub Codespaces config
│   └── setup.sh                ← Auto setup script
├── database/
│   └── schema.sql              ← PostgreSQL schema
├── logic/
│   └── notice_generator.py     ← DOCX generation logic
├── templates/
│   ├── notice_form.html        ← Main form UI
│   └── notice_preview.html     ← Preview page
├── app.py                      ← Flask app & routes
├── config.py                   ← DB & app configuration
├── data.json                   ← Departments data
├── requirements.txt            ← Python dependencies
└── HR_Automation_Setup_Guide.pdf ← Organisation PC setup guide
```

---

## ⚙️ Installation

### Prerequisites
- Python 3.12.5
- PostgreSQL 17
- Git

### Step 1 — Clone the repo
```bash
git clone https://github.com/RohillaJai-030502/hr-automation-suite.git
cd hr-automation-suite
```

### Step 2 — Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### Step 3 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Set up PostgreSQL
```bash
psql postgres
```
```sql
CREATE USER postgres WITH SUPERUSER PASSWORD 'postgres';
CREATE DATABASE hr_intern_db;
\q
```

### Step 5 — Configure the app
Open `config.py` and update your PostgreSQL password:
```python
DB_CONFIG = {
    "host":     "localhost",
    "port":     5432,
    "database": "hr_intern_db",
    "user":     "postgres",
    "password": "YOUR_PASSWORD_HERE"
}
```

### Step 6 — Run the app
```bash
python app.py
```

Open your browser at:
```
http://localhost:5001
```

---

## 📅 Daily Usage

```bash
cd hr-automation-suite
source venv/bin/activate
python app.py
```

Then open `http://localhost:5001` in your browser.

---

## 🔄 Getting Updates

```bash
git pull
```

---

## 📖 Setup Guide

For non-technical users, a step-by-step PDF setup guide is included:
📄 `HR_Automation_Setup_Guide.pdf`

---

## 👨‍💻 Developer

**Jai Rohilla**
📧 rohillajai030502@gmail.com
🔗 github.com/RohillaJai-030502

---

## 📜 License

This project is private and intended for internal use within the Organisation — HRD Division.
