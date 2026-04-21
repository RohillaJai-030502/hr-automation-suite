# ============================================================
# config.py — Central Configuration for HR Automation Suite
# ============================================================

DB_CONFIG = {
    "host":     "localhost",
    "port":     5432,
    "database": "hr_intern_db",
    "user":     "postgres",
    "password": "postgres"
}

APP_CONFIG = {
    "host": "0.0.0.0",   # Makes Flask accessible on LAN
    "port": 5001,
    "debug": True
}