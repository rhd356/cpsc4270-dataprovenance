# cpsc4270-dataprovenance


Run one of the scripts (setup.sh for Linux and Mac, setup.ps1 for Windows)

MySQL will need to be installed on your machine. For Windows, it will need to be added to your PATH. Instructions are in the setup.ps1 script. Example:

"C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" <----------- May be different on your machine.


Setup Scripts:

# Windows:
Open PowerShell in VScode and run:

Open a terminal window and run:

powershell -ExecutionPolicy Bypass -File .\setup_windows.ps1

You will be prompted for:

    MySQL root password

    Password for admin (dataprovenance)

If PowerShell says it cannot run scripts, use:

    Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# Linux:
If running on linux, you may have to first run the following for the script to play nice:

sudo mysql
SET GLOBAL validate_password.policy = LOW;
SET GLOBAL validate_password.length = 6;
EXIT;

Make script runnable:

chmod +x setup_linux.sh
./setup_linux.sh

This script will:

    Install Python dependencies

    Create the MySQL database (dataprovenance_db)

    Create the MySQL user (user: admin / password: dataprovenance)

    Enable trigger creation (log_bin_trust_function_creators)

    Load mysql/schema.sql

    Create a .env file for the Python app

You will be prompted for:

    Your MySQL root password

    The admin user password (dataprovenance)

# Running python app post setup:

    In a terminal/powershell window inside vscode run:

    source venv/bin/activate --> for linux or .\venv\Scripts\Activate.ps1 for Windows
    python3 app.py or python app.py --> depending on python version





