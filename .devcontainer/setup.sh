#!/bin/bash

echo "🔧 Setting up HR Automation Suite..."

# Find installed PostgreSQL version automatically
PG_VERSION=$(pg_lsclusters | awk 'NR==2{print $1}')
echo "📦 Found PostgreSQL version: $PG_VERSION"

# Start PostgreSQL
sudo service postgresql start

# Setup database using the correct version
sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';" 2>/dev/null || true
sudo -u postgres psql -c "CREATE DATABASE hr_intern_db;" 2>/dev/null || true

# Install Python dependencies
pip install -r requirements.txt

echo "✅ Setup complete! Run: python app.py"