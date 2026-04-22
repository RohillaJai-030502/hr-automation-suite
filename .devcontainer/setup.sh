#!/bin/bash

echo "🔧 Setting up HR Automation Suite..."

# Install PostgreSQL 15 specifically
sudo apt-get update
sudo apt-get install -y postgresql-15 postgresql-client-15

# Start PostgreSQL 15
sudo service postgresql start

# Setup database
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';" 2>/dev/null || true
sudo -u postgres psql -c "CREATE DATABASE hr_intern_db;" 2>/dev/null || true

# Install Python dependencies
pip install -r requirements.txt

echo "✅ Setup complete! Run: python app.py"