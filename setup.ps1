# Setup script for Windows
# Install MySQL first and remember the root password you set during installation.
# Add MySQL to your system PATH or provide the full path to mysql.exe when prompted.

$ErrorActionPreference = "Stop"

$DB_NAME = "dataprovenance_db"
$DB_USER = "admin"
$DB_PASS = "d@taprovenance123!"
$SCHEMA_PATH = "mysql/schema.sql"

Write-Host "=== Data Provenance Project Setup (Windows) ===`n"

# Find MySQL executable
$mysqlPaths = @(
    "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe",
    "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysql.exe",
    "C:\Program Files\MySQL\MySQL Server 9.0\bin\mysql.exe",
    "C:\Program Files (x86)\MySQL\MySQL Server 8.0\bin\mysql.exe"
)

$MYSQL_EXE = $null
foreach ($path in $mysqlPaths) {
    if (Test-Path $path) {
        $MYSQL_EXE = $path
        Write-Host "Found MySQL at: $MYSQL_EXE"
        break
    }
}

if (-not $MYSQL_EXE) {
    Write-Host "`nERROR: MySQL not found in common installation paths."
    Write-Host "Please provide the full path to mysql.exe"
    Write-Host "Example: C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe`n"
    $MYSQL_EXE = Read-Host "Enter path to mysql.exe"

    if (-not (Test-Path $MYSQL_EXE)) {
        Write-Host "ERROR: MySQL executable not found at: $MYSQL_EXE"
        exit 1
    }
}
Write-Host ""

# 1) Create virtual environment
Write-Host ">>> Creating Python virtual environment..."
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists, skipping creation..."
} else {
    python -m venv venv
}

Write-Host ">>> Activating virtual environment..."
# PowerShell venv activation
if (Test-Path ".\venv\Scripts\Activate.ps1") {
    . .\venv\Scripts\Activate.ps1
} else {
    Write-Host "WARNING: Could not find activation script. Continuing anyway..."
}

# 2) Install dependencies
Write-Host "`n>>> Installing Python dependencies..."
pip install -r requirements.txt

# 3) MySQL setup
Write-Host "`n>>> Setting up MySQL database and user..."
Write-Host "You will be prompted for MySQL root password."

$mysqlCommands = @"
CREATE DATABASE IF NOT EXISTS $DB_NAME;
CREATE USER IF NOT EXISTS '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASS';
GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO '$DB_USER'@'localhost';
SET GLOBAL log_bin_trust_function_creators = 1;
FLUSH PRIVILEGES;
"@

$mysqlCommands | & $MYSQL_EXE -u root -p

# 4) Load schema
Write-Host "`n>>> Loading schema using admin user..."
Write-Host "You will be prompted for admin password: $DB_PASS"
Get-Content $SCHEMA_PATH | & $MYSQL_EXE -u $DB_USER -p $DB_NAME

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
Write-Host "Then run the app with: python main.py"
