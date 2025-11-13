# setup_windows.ps1
# Setup script for the Data Provenance project on Windows (PowerShell)

$ErrorActionPreference = "Stop"

$DB_NAME = "dataprovenance_db"
$DB_USER = "admin"
$DB_PASS = "dataprovenance"
$SCHEMA_PATH = "mysql/schema.sql"

Write-Host "=== Data Provenance Project Setup (Windows) ===`n"

# 1) Install Python dependencies
Write-Host ">>> Installing Python dependencies from requirements.txt..."
pip install -r requirements.txt

# 2) MySQL setup
Write-Host "`n>>> Setting up MySQL database and user..."
Write-Host "You will be prompted for your MySQL root password (if set)."

# NOTE: This assumes 'mysql.exe' is in your PATH.
# If not, replace 'mysql' below with the full path, e.g. '\"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe\"'

# Create DB, user, privileges, and trust function creators
mysql -u root -p -e @"
CREATE DATABASE IF NOT EXISTS $DB_NAME;
CREATE USER IF NOT EXISTS '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASS';
GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'localhost';
SET GLOBAL log_bin_trust_function_creators = 1;
FLUSH PRIVILEGES;
"@

# 3) Load schema as admin
Write-Host "`n>>> Loading schema from $SCHEMA_PATH using admin user..."
Write-Host "You will be prompted for the admin password (dataprovenance)."
mysql -u $DB_USER -p $DB_NAME < $SCHEMA_PATH

# 4) Create .env if needed
Write-Host "`n>>> Checking for .env file..."
if (Test-Path ".env") {
    Write-Host ".env already exists, leaving it unchanged."
} else {
    Write-Host "Creating .env file..."
    @"
DB_HOST=localhost
DB_PORT=3306
DB_USER=$DB_USER
DB_PASS=$DB_PASS
DB_NAME=$DB_NAME
"@ | Out-File -Encoding UTF8 ".env"
    Write-Host ".env created."
}

Write-Host "`n=== Setup complete! ==="
Write-Host "You can now run:  python app.py"
