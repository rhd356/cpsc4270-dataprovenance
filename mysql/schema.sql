-- Create database
CREATE DATABASE IF NOT EXISTS dataprovenance_db;
USE dataprovenance_db;

-- Main table: employees
DROP TABLE IF EXISTS audit_log;
DROP TABLE IF EXISTS employees;

CREATE TABLE employees (
    employee_id   INT AUTO_INCREMENT PRIMARY KEY,
    full_name     VARCHAR(255) NOT NULL,
    department    VARCHAR(100) NOT NULL,
    role          VARCHAR(100) NULL,
    salary        DECIMAL(12,2) NOT NULL,
    last_updated  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);

-- Audit log table
CREATE TABLE audit_log (
    audit_id      INT AUTO_INCREMENT PRIMARY KEY,
    table_name    VARCHAR(64) NOT NULL,
    row_id        INT NOT NULL,            -- maps to employees.employee_id
    column_name   VARCHAR(64) NOT NULL,    -- ex: 'salary'
    old_value     TEXT,
    new_value     TEXT,
    changed_by    VARCHAR(255) NOT NULL,   -- username
    changed_role  VARCHAR(255) NULL,       -- e.g., 'HR_Manager'
    justification TEXT NULL,               -- reason for the change
    changed_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Trigger to log changes to sensitive fields on employees
DELIMITER $$

DROP TRIGGER IF EXISTS trg_employees_audit$$

CREATE TRIGGER trg_employees_audit
BEFORE UPDATE ON employees
FOR EACH ROW
BEGIN
    -- Log salary changes
    IF NOT (NEW.salary <=> OLD.salary) THEN
        INSERT INTO audit_log (
            table_name,
            row_id,
            column_name,
            old_value,
            new_value,
            changed_by,
            changed_role,
            justification,
            changed_at
        ) VALUES (
            'employees',
            OLD.employee_id,
            'salary',
            OLD.salary,
            NEW.salary,
            COALESCE(@app_current_user, CURRENT_USER()),
            @app_current_role,
            @app_justification,
            NOW()
        );
    END IF;

    -- Log name changes
    IF NOT (NEW.full_name <=> OLD.full_name) THEN
        INSERT INTO audit_log (
            table_name,
            row_id,
            column_name,
            old_value,
            new_value,
            changed_by,
            changed_role,
            justification,
            changed_at
        ) VALUES (
            'employees',
            OLD.employee_id,
            'full_name',
            OLD.full_name,
            NEW.full_name,
            COALESCE(@app_current_user, CURRENT_USER()),
            @app_current_role,
            @app_justification,
            NOW()
        );
    END IF;

    -- Log department changes
    IF NOT (NEW.department <=> OLD.department) THEN
        INSERT INTO audit_log (
            table_name,
            row_id,
            column_name,
            old_value,
            new_value,
            changed_by,
            changed_role,
            justification,
            changed_at
        ) VALUES (
            'employees',
            OLD.employee_id,
            'department',
            OLD.department,
            NEW.department,
            COALESCE(@app_current_user, CURRENT_USER()),
            @app_current_role,
            @app_justification,
            NOW()
        );
    END IF;

    -- Log role changes
    IF NOT (NEW.role <=> OLD.role) THEN
        INSERT INTO audit_log (
            table_name,
            row_id,
            column_name,
            old_value,
            new_value,
            changed_by,
            changed_role,
            justification,
            changed_at
        ) VALUES (
            'employees',
            OLD.employee_id,
            'role',
            OLD.role,
            NEW.role,
            COALESCE(@app_current_user, CURRENT_USER()),
            @app_current_role,
            @app_justification,
            NOW()
        );
    END IF;
END$$

DELIMITER ;

INSERT INTO employees (full_name, department, role, salary) VALUES
('Jonathan Scott', 'Sales', 'Sales Manager', 101269.00),
('Samuel Martinez', 'Sales', 'Sales Associate II', 111583.00),
('Joseph Baker', 'Sales', 'Sales Associate I', 107044.00),
('Thomas Richardson', 'Sales', 'Sales Associate II', 62073.00),
('Emma Morales', 'Sales', 'Sales Associate I', 54330.00),
('Daniel Allen', 'Sales', 'Sales Associate II', 146521.00),
('Rebecca Scott', 'Sales', 'Sales Associate I', 90140.00),
('Michael Murphy', 'Sales', 'Sales Associate II', 106614.00),
('Patricia Thompson', 'Sales', 'Sales Associate I', 122012.00),
('Debra Green', 'Sales', 'Sales Associate II', 126220.00),
('Anthony Roberts', 'Sales', 'Sales Associate I', 47676.00),
('Jason Taylor', 'Sales', 'Sales Associate II', 128046.00),
('Stephanie Cruz', 'Sales', 'Sales Associate I', 68887.00),
('Christine Kelly', 'Sales', 'Sales Associate II', 96101.00),
('Susan Morgan', 'Sales', 'Sales Associate I', 48162.00),
('Sharon Baker', 'IT', 'CIO', 96407.00),
('Kathleen Lopez', 'IT', 'Software Engineer', 53372.00),
('Jacob Jones', 'IT', 'System Administrator', 125656.00),
('Richard Anderson', 'IT', 'Helpdesk II', 55916.00),
('Betty Hernandez', 'IT', 'Helpdesk I', 138393.00),
('Kimberly Smith', 'IT', 'Software Engineer', 120095.00),
('Brandon Gutierrez', 'IT', 'System Administrator', 118909.00),
('Michelle Peterson', 'IT', 'Helpdesk II', 87334.00),
('Brenda Phillips', 'IT', 'Software Engineer', 120860.00),
('Brandon Bailey', 'IT', 'Helpdesk I', 53223.00),
('Jessica Hall', 'IT', 'System Administrator', 100129.00),
('Amanda Murphy', 'IT', 'Helpdesk II', 87228.00),
('Charles Parker', 'IT', 'Software Engineer', 117826.00),
('James Lee', 'IT', 'System Administrator', 122870.00),
('Nicole Hill', 'IT', 'Helpdesk I', 124400.00),
('Michael Anderson', 'IT', 'Helpdesk II', 59876.00),
('Barbara Wright', 'IT', 'Software Engineer', 77737.00),
('Shirley Collins', 'HR', 'HR Manager', 60850.00),
('Michelle Sanchez', 'HR', 'Payroll Specialist', 83013.00),
('Deborah Brown', 'HR', 'Benefits Specialist', 148394.00),
('Kimberly Clark', 'HR', 'Recruiter', 107642.00),
('Barbara Robinson', 'HR', 'Payroll Specialist', 77519.00),
('Christopher White', 'HR', 'Benefits Specialist', 50224.00),
('Brandon Hernandez', 'HR', 'Recruiter', 94703.00),
('Amy Kim', 'HR', 'Payroll Specialist', 138825.00),
('Kevin Hill', 'HR', 'Benefits Specialist', 57995.00),
('Sharon Robinson', 'HR', 'Recruiter', 47592.00),
('Gregory Ward', 'HR', 'Payroll Specialist', 72582.00),
('Helen Turner', 'HR', 'Benefits Specialist', 68084.00),
('John Hill', 'Accounting', 'CFO', 90312.00),
('Jeffrey Garcia', 'Accounting', 'Staff Accountant', 80275.00),
('Laura Brown', 'Accounting', 'Financial Analyst', 114794.00),
('Jennifer Walker', 'Accounting', 'Auditor', 89718.00),
('Edward Allen', 'Accounting', 'Staff Accountant', 85485.00),
('Eric Anderson', 'Accounting', 'Financial Analyst', 122105.00),
('Lisa Roberts', 'Accounting', 'Auditor', 122171.00),
('Karen Gonzalez', 'Accounting', 'Staff Accountant', 51244.00),
('Angela Hill', 'Accounting', 'Financial Analyst', 127552.00),
('Anna Anderson', 'Accounting', 'Auditor', 49749.00),
('Dorothy White', 'Accounting', 'Staff Accountant', 104735.00),
('Gary Diaz', 'Accounting', 'Financial Analyst', 83236.00),
('Carol Evans', 'Accounting', 'Auditor', 60535.00),
('Katherine Turner', 'Marketing', 'Marketing Manager', 59535.00),
('Samantha Kelly', 'Marketing', 'Advertising Specialist', 146814.00),
('Melissa Jackson', 'Marketing', 'Social Media Specialist', 98454.00),
('Jeffrey Miller', 'Marketing', 'Advertising Specialist', 137576.00),
('Brenda Adams', 'Marketing', 'Social Media Specialist', 92466.00),
('Rebecca Rodriguez', 'Marketing', 'Advertising Specialist', 70304.00),
('Stephen Morales', 'Marketing', 'Social Media Specialist', 132575.00),
('Justin Stewart', 'Marketing', 'Advertising Specialist', 106887.00),
('Ronald Evans', 'Marketing', 'Social Media Specialist', 68846.00),
('Susan Ramirez', 'Marketing', 'Advertising Specialist', 95633.00),
('Christopher Bailey', 'Legal', 'CLO', 92205.00),
('Margaret Edwards', 'Legal', 'Senior Legal Counsel', 57085.00),
('Brenda King', 'Legal', 'IP Lawyer', 94270.00),
('Jessica Kelly', 'Legal', 'Employment Lawyer', 135949.00),
('Karen Morgan', 'Legal', 'Senior Legal Counsel', 84003.00),
('Cynthia Edwards', 'Legal', 'IP Lawyer', 112052.00),
('Karen Evans', 'Legal', 'Employment Lawyer', 130263.00),
('Samuel Jones', 'Legal', 'Senior Legal Counsel', 64887.00),
('Samantha Diaz', 'Legal', 'IP Lawyer', 147963.00),
('Charles Rodriguez', 'Legal', 'Employment Lawyer', 109673.00),
('Deborah Cruz', 'Legal', 'Senior Legal Counsel', 142779.00),
('Kenneth Diaz', 'Legal', 'IP Lawyer', 86900.00),
('Mary Clark', 'Customer Service', 'Customer Service Manager', 100890.00),
('William Reyes', 'Customer Service', 'CSR I', 117633.00),
('Matthew Allen', 'Customer Service', 'CSR II', 130008.00),
('Patricia Edwards', 'Customer Service', 'CSR I', 81004.00),
('Edward Harris', 'Customer Service', 'CSR II', 117102.00),
('Karen Smith', 'Customer Service', 'CSR I', 137057.00),
('Pamela Robinson', 'Customer Service', 'CSR II', 71211.00),
('Shirley Flores', 'Marketing', 'Advertising Specialist', 74646.00),
('Matthew Campbell', 'IT', 'Helpdesk I', 49485.00),
('Christopher Jackson', 'Sales', 'Sales Associate I', 115366.00),
('Sandra Richardson', 'Accounting', 'Staff Accountant', 82934.00),
('John Cooper', 'Legal', 'Employment Lawyer', 144734.00),
('Kathleen Martinez', 'HR', 'Recruiter', 135988.00),
('Joseph Howard', 'Customer Service', 'CSR I', 86939.00),
('Jessica Ward', 'IT', 'Software Engineer', 137516.00),
('Rebecca Reed', 'Marketing', 'Social Media Specialist', 99855.00),
('Christopher Flores', 'Marketing', 'Advertising Specialist', 144048.00),
('Ronald Nelson', 'Sales', 'Sales Associate II', 64988.00),
('Elizabeth Morris', 'IT', 'System Administrator', 92385.00),
('Justin Kelly', 'Customer Service', 'CSR II', 111411.00),
('Mark Lewis', 'Accounting', 'Financial Analyst', 132041.00);
