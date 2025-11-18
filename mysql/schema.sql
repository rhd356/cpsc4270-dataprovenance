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
    -- Only log if salary actually changed
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
('Jonathan Scott', 'Sales', 101269.00),
('Michelle Peterson', 'Services', 87334.00),
('John Hill', 'Accounting', 90312.00),
('Shirley Flores', 'Research and Development', 74646.00),
('Katherine Turner', 'Marketing', 59535.00),
('Samantha Kelly', 'Marketing', 146814.00),
('Mary Clark', 'Business Development', 100890.00),
('Sharon Baker', 'IT', 96407.00),
('Kathleen Lopez', 'IT', 53372.00),
('Samuel Martinez', 'Sales', 111583.00),
('Shirley Collins', 'HR', 60850.00),
('Joseph Baker', 'Sales', 107044.00),
('Brenda Phillips', 'Services', 120860.00),
('Jacob Jones', 'IT', 125656.00),
('Brandon Bailey', 'Services', 53223.00),
('Jason Taylor', 'Engineering', 128046.00),
('Michelle Sanchez', 'HR', 83013.00),
('Richard Anderson', 'IT', 55916.00),
('Betty Hernandez', 'IT', 138393.00),
('Jeffrey Garcia', 'Accounting', 80275.00),
('Thomas Richardson', 'Sales', 62073.00),
('Christopher Flores', 'Product Management', 144048.00),
('Emma Morales', 'Sales', 54330.00),
('Laura Brown', 'Accounting', 114794.00),
('Melissa Jackson', 'Marketing', 98454.00),
('Deborah Brown', 'HR', 148394.00),
('Jeffrey Miller', 'Marketing', 137576.00),
('Matthew Campbell', 'Research and Development', 49485.00),
('Christopher Bailey', 'Legal', 92205.00),
('William Reyes', 'Business Development', 117633.00),
('Matthew Allen', 'Business Development', 130008.00),
('Kimberly Clark', 'HR', 107642.00),
('Daniel Allen', 'Sales', 146521.00),
('Barbara Robinson', 'HR', 77519.00),
('Margaret Edwards', 'Legal', 57085.00),
('Kimberly Smith', 'IT', 120095.00),
('Brenda King', 'Legal', 94270.00),
('Stephanie Cruz', 'Engineering', 68887.00),
('Jennifer Walker', 'Accounting', 89718.00),
('Patricia Edwards', 'Business Development', 81004.00),
('Rebecca Scott', 'Sales', 90140.00),
('Jessica Hall', 'Services', 100129.00),
('Brenda Adams', 'Marketing', 92466.00),
('Christopher Jackson', 'Research and Development', 115366.00),
('Sandra Richardson', 'Research and Development', 82934.00),
('John Cooper', 'Research and Development', 144734.00),
('Michael Murphy', 'Sales', 106614.00),
('Edward Allen', 'Accounting', 85485.00),
('Ronald Nelson', 'Product Management', 64988.00),
('Brandon Hernandez', 'Support', 94703.00),
('Amanda Murphy', 'Services', 87228.00),
('Rebecca Rodriguez', 'Marketing', 70304.00),
('Jessica Kelly', 'Legal', 135949.00),
('Charles Parker', 'Services', 117826.00),
('Kathleen Martinez', 'Research and Development', 135988.00),
('Eric Anderson', 'Accounting', 122105.00),
('James Lee', 'Services', 122870.00),
('Elizabeth Morris', 'Product Management', 92385.00),
('Justin Kelly', 'Product Management', 111411.00),
('Brandon Gutierrez', 'IT', 118909.00),
('Lisa Roberts', 'Accounting', 122171.00),
('Stephen Morales', 'Marketing', 132575.00),
('Karen Morgan', 'Legal', 84003.00),
('Justin Stewart', 'Marketing', 106887.00),
('Patricia Thompson', 'Sales', 122012.00),
('Joseph Howard', 'Research and Development', 86939.00),
('Amy Kim', 'Support', 138825.00),
('Cynthia Edwards', 'Legal', 112052.00),
('Karen Evans', 'Legal', 130263.00),
('Samuel Jones', 'Legal', 64887.00),
('Samantha Diaz', 'Legal', 147963.00),
('Edward Harris', 'Business Development', 117102.00),
('Debra Green', 'Sales', 126220.00),
('Anthony Roberts', 'Sales', 47676.00),
('Christopher White', 'HR', 50224.00),
('Ronald Evans', 'Marketing', 68846.00),
('Kevin Hill', 'Support', 57995.00),
('Jessica Ward', 'Research and Development', 137516.00),
('Mark Lewis', 'Product Management', 132041.00),
('Susan Ramirez', 'Marketing', 95633.00),
('Sharon Robinson', 'Support', 47592.00),
('Christine Kelly', 'Engineering', 96101.00),
('Nicole Hill', 'Services', 124400.00),
('Charles Rodriguez', 'Legal', 109673.00),
('Karen Gonzalez', 'Accounting', 51244.00),
('Angela Hill', 'Accounting', 127552.00),
('Anna Anderson', 'Accounting', 49749.00),
('Dorothy White', 'Accounting', 104735.00),
('Deborah Cruz', 'Legal', 142779.00),
('Kenneth Diaz', 'Legal', 86900.00),
('Karen Smith', 'Business Development', 137057.00),
('Pamela Robinson', 'Business Development', 71211.00),
('Rebecca Reed', 'Research and Development', 99855.00),
('Gary Diaz', 'Accounting', 83236.00),
('Gregory Ward', 'Support', 72582.00),
('Susan Morgan', 'Engineering', 48162.00),
('Carol Evans', 'Accounting', 60535.00),
('Helen Turner', 'Support', 68084.00),
('Michael Anderson', 'Services', 59876.00),
('Barbara Wright', 'Services', 77737.00);
