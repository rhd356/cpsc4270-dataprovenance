#!/usr/bin/env bash

# setup.sh
# Setup script for the Data Provenance project on Linux/macOS

set -e  # exit on first error

DB_NAME="dataprovenance_db"
DB_USER="admin"
DB_PASS="dataprovenance"
SCHEMA_PATH="mysql/schema.sql"

echo "=== Data Provenance Project Setup (Linux/macOS) ==="

# 1) Install Python dependencies
echo
echo ">>> Installing Python dependencies from requirements.txt..."
pip install -r requirements.txt

# 2) MySQL setup
echo
echo ">>> Setting up MySQL database and user..."
echo "You will be prompted for your MySQL root password (if set)."

# Create database, user, grant privileges, and trust function creators
mysql -u root -p -e "
CREATE DATABASE IF NOT EXISTS ${DB_NAME};
CREATE USER IF NOT EXISTS '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASS}';
GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'localhost';
SET GLOBAL log_bin_trust_function_creators = 1;
FLUSH PRIVILEGES;
"

# 3) Load schema as admin (will prompt for 'dataprovenance')
echo
echo ">>> Loading schema from ${SCHEMA_PATH} using admin user..."
mysql -u "${DB_USER}" -p "${DB_NAME}" < "${SCHEMA_PATH}"

# 4) Create .env file if it doesn't exist
echo
if [ -f ".env" ]; then
  echo ">>> .env already exists, leaving it unchanged."
else
  echo ">>> Creating .env file..."
  cat > .env <<EOF
DB_HOST=localhost
DB_PORT=3306
DB_USER=${DB_USER}
DB_PASS=${DB_PASS}
DB_NAME=${DB_NAME}
EOF
  echo ">>> .env created."
fi

echo
echo "=== Setup complete! ==="
echo "You can now run:  python app.py"
