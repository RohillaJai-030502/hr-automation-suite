#!/bin/bash

echo "🔧 Setting up HR Automation Suite..."

# Install Python dependencies
pip install -r requirements.txt

# Setup PostgreSQL
sudo service postgresql start
sudo -u postgres psql -c "CREATE USER postgres WITH SUPERUSER PASSWORD 'postgres';" 2>/dev/null || true
sudo -u postgres psql -c "CREATE DATABASE hr_intern_db;" 2>/dev/null || true

echo "✅ Setup complete! Run: python app.py"