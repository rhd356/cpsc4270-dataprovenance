# setup_windows.ps1
# Setup script for Windows

$ErrorActionPreference = "Stop"

$DB_NAME = "dataprovenance_db"
$DB_USER = "admin"
$DB_PASS = "dataprovenance"
$SCHEMA_PATH = "mysql/schema.sql"

Write-Host "=== Data Provenance Project Setup (Windows) ===`n"

# 1) Create virtual environment
Write-Host ">>> Creating Python virtual environment..."
python -m venv venv

Write-Host ">>> Activating virtual environment..."
# PowerShell venv activation
. .\venv\Scripts\Activate.ps1

# 2) Install dependencies
Write-Host "`n>>> Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# 3) MySQL setup
Write-Host "`n>>> Setting up MySQL database and user..."
Write-Host "You will be prompted for MySQL root password."

mysql -u root -p -e @"
CREATE DATABASE IF NOT EXISTS $DB_NAME;
CREATE USER IF NOT EXISTS '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASS';
GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'localhost';
SET GLOBAL log_bin_trust_function_creators = 1;
FLUSH PRIVILEGES;
"@

# 4) Load schema
Write-Host "`n>>> Loading schema using admin user..."
mysql -u $DB_USER -p $DB_NAME < $SCHEMA_PATH

# 5) Create .env if missing
Write-Host "`n>>> Checking for .env..."
if (Test-Path ".env") {
    Write-Host ".env already exists."
} else {
    Write-Host "Creating .env file..."
@"
DB_HOST=localhost
DB_PORT=3306
DB_USER=$DB_USER
DB_PASS=$DB_PASS
DB_NAME=$DB_NAME
"@ | Out-File -Encoding UTF8 ".env"
}

Write-Host "`n=== Setup complete! ==="
Write-Host "To activate the virtual environment in the future: .\venv\Scripts\Activate.ps1"
Write-Host "Then run the app with: python app.py"
