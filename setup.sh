#!/usr/bin/env bash
# Setup script for the Data Provenance project on Linux/macOS (auth_socket-friendly)

set -e  # exit on first error

DB_NAME="dataprovenance_db"
DB_USER="dpuser"
DB_PASS="D@taProvenance123!"
SCHEMA_PATH="mysql/schema.sql"

echo "=== Data Provenance Project Setup (Linux/macOS) ==="

# 1) Create virtual environment
echo
echo ">>> Creating Python virtual environment..."
python3 -m venv venv

echo ">>> Activating virtual environment..."
source venv/bin/activate

# 2) Install Python dependencies
echo
echo ">>> Installing Python dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

# 3) MySQL setup using sudo mysql
echo
echo ">>> Setting up MySQL database and user via sudo mysql..."

sudo mysql <<EOF
CREATE DATABASE IF NOT EXISTS ${DB_NAME};
CREATE USER IF NOT EXISTS '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASS}';
GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '${DB_USER}'@'localhost';
SET GLOBAL log_bin_trust_function_creators = 1;
FLUSH PRIVILEGES;
EOF

# 4) Load schema as dpuser
echo
echo ">>> Loading schema from ${SCHEMA_PATH} using ${DB_USER}..."
mysql -u "${DB_USER}" -p"${DB_PASS}" "${DB_NAME}" < "${SCHEMA_PATH}"

# 5) Create .env file if it doesn't exist
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
echo "To activate the virtual environment later, run: source venv/bin/activate"
echo "Then start the app with: python app.py"
