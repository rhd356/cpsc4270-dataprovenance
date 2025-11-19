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
    python3 main.py or python main.py --> depending on python version

# Migrating Existing Database:

If you already have the database set up and want to add the new features (justification field and role column), run:

    mysql -u admin -p dataprovenance_db < mysql/migrate_add_justification.sql

# Reorganizing Departments and Assigning Roles:

After setting up or migrating the database, run this script to reorganize departments and assign roles:

    mysql -u admin -p dataprovenance_db < mysql/reorganize_and_assign_roles.sql

This script will:
- Reassign employees from obsolete departments (Services→IT, Support→HR, Engineering→Sales, Business Development→Customer Service, Research and Development→Random)
- Assign roles to all employees based on their department
- Ensure each department has exactly one department head

# Features:

## Data Provenance & Traceability
- **Automatic audit logging** for all changes to sensitive fields (salary, full_name, department, role)
- **Complete provenance chains** - trace the full history of any field from initial value to current
- **Database triggers** automatically capture old values, new values, timestamps, user identity, and role
- **Change justifications** - users must provide a reason for each change

## Audit Capabilities
- View salary changes in the last month
- View name changes in the last month
- View department changes in the last month
- Query all changes within a custom date range
- **Trace complete field history** - see the entire provenance chain for any employee field (salary, name, department, role)
- **Search changes by user** - see all changes made by a specific username
- **Search changes by role** - see all changes made by users with a specific role

## Dispute Resolution Support
- Full audit trail with who/what/when/why information
- Justification field requires users to document why changes were made
- Granular tracking enables investigation of specific changes
- Complete history allows verification of data lineage

## Department Structure

The system supports the following departments and roles:

**HR**
- HR Manager (Head)
- Payroll Specialist
- Benefits Specialist
- Recruiter

**Accounting**
- CFO (Head)
- Staff Accountant
- Financial Analyst
- Auditor

**IT**
- CIO (Head)
- Software Engineer
- System Administrator
- Helpdesk II
- Helpdesk I

**Sales**
- Sales Manager (Head)
- Sales Associate II
- Sales Associate I

**Marketing**
- Marketing Manager (Head)
- Advertising Specialist
- Social Media Specialist

**Legal**
- CLO (Head)
- Senior Legal Counsel
- IP Lawyer
- Employment Lawyer

**Customer Service**
- Customer Service Manager (Head)
- CSR I
- CSR II





