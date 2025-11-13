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
    salary        DECIMAL(12,2) NOT NULL,
    last_updated  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        ON UPDATE CURRENT_TIMESTAMP
);

-- Audit log table
CREATE TABLE audit_log (
    audit_id      INT AUTO_INCREMENT PRIMARY KEY,
    table_name    VARCHAR(64) NOT NULL,
    row_id        INT NOT NULL,            -- maps to employees.employee_id
    column_name   VARCHAR(64) NOT NULL,    -- e.g., 'salary'
    old_value     TEXT,
    new_value     TEXT,
    changed_by    VARCHAR(255) NOT NULL,   -- username
    changed_role  VARCHAR(255) NULL,       -- e.g., 'HR_Manager'
    changed_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Trigger to log salary changes on employees
DELIMITER $$

DROP TRIGGER IF EXISTS trg_employees_salary_audit$$

CREATE TRIGGER trg_employees_salary_audit
BEFORE UPDATE ON employees
FOR EACH ROW
BEGIN
    -- Only log if salary actually changed (NULL-safe compare)
    IF NOT (NEW.salary <=> OLD.salary) THEN
        INSERT INTO audit_log (
            table_name,
            row_id,
            column_name,
            old_value,
            new_value,
            changed_by,
            changed_role,
            changed_at
        ) VALUES (
            'employees',
            OLD.employee_id,
            'salary',
            OLD.salary,
            NEW.salary,
            COALESCE(@app_current_user, CURRENT_USER()),
            @app_current_role,
            NOW()
        );
    END IF;
END$$

DELIMITER ;

-- Sample data
INSERT INTO employees (full_name, department, salary) VALUES
('Alice Johnson', 'HR',    60000.00),
('Bob Smith',     'IT',    80000.00),
('Carol Davis',   'Sales', 55000.00);
