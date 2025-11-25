# Main application
from datetime import datetime
from tabulate import tabulate
from rich import print

from database import get_conn, set_app_identity, validate_user_role
from audit import (
    print_salary_changes_last_month,
    print_name_changes_last_month,
    print_department_changes_last_month,
    print_changes_in_range,
    print_field_history,
    print_all_changes_by_user,
    print_all_changes_by_role,
)

# Authorized roles that can make changes
AUTHORIZED_ROLES = [
    "HR Manager",
    "System Administrator",
    "Sales Manager",
    "CFO",
    "CIO",
    "CLO",
    "Customer Service Manager"
]

"""
    Prompts the user to select their role from the authorized list.
    Returns the selected role or None if the selection is invalid.
"""
def select_authorized_role():
    print("\n[bold cyan]Select your role:[/bold cyan]")
    for idx, role in enumerate(AUTHORIZED_ROLES, 1):
        print(f"  {idx}) {role}")

    try:
        choice = int(input("\nEnter the number of your role: ").strip())
        if 1 <= choice <= len(AUTHORIZED_ROLES):
            return AUTHORIZED_ROLES[choice - 1]
        else:
            print("[red]Invalid selection. Please choose a number from the list.[/red]")
            return None
    except ValueError:
        print("[red]Invalid input. Please enter a number.[/red]")
        return None

"""
    Get list of unique departments from the database.
"""
def get_departments():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT department FROM employees ORDER BY department;")
        rows = cur.fetchall()
        cur.close()
        return [row[0] for row in rows]

"""
    Get list of unique roles for a specific department.
"""
def get_roles_by_department(department):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT DISTINCT role FROM employees WHERE department = %s AND role IS NOT NULL ORDER BY role;",
            (department,)
        )
        rows = cur.fetchall()
        cur.close()
        return [row[0] for row in rows]

"""
    Prompts the user to select a department from the list of existing departments.
    Returns the selected department or None if the selection is invalid.
"""
def select_department():
    departments = get_departments()
    if not departments:
        print("[red]No departments found in the database.[/red]")
        return None

    print("\n[bold cyan]Select a department:[/bold cyan]")
    for idx, dept in enumerate(departments, 1):
        print(f"  {idx}) {dept}")

    try:
        choice = int(input("\nEnter the number of the department: ").strip())
        if 1 <= choice <= len(departments):
            return departments[choice - 1]
        else:
            print("[red]Invalid selection. Please choose a number from the list.[/red]")
            return None
    except ValueError:
        print("[red]Invalid input. Please enter a number.[/red]")
        return None

"""
    Prompts the user to select a role for the specified department.
    Returns the selected role or None if the selection is invalid.
"""
def select_role_for_department(department):
    roles = get_roles_by_department(department)
    if not roles:
        print(f"[red]No roles found for department '{department}'.[/red]")
        return None

    print(f"\n[bold cyan]Select a role for {department}:[/bold cyan]")
    for idx, role in enumerate(roles, 1):
        print(f"  {idx}) {role}")

    try:
        choice = int(input("\nEnter the number of the role: ").strip())
        if 1 <= choice <= len(roles):
            return roles[choice - 1]
        else:
            print("[red]Invalid selection. Please choose a number from the list.[/red]")
            return None
    except ValueError:
        print("[red]Invalid input. Please enter a number.[/red]")
        return None
    
"""
    Parse timestamp from MM-DD-YYYY HH:MM format to YYYY-MM-DD HH:MM:SS format.
    Returns the formatted string or None if invalid.
    Makes it easier to enter a date and time for American users.
"""
def parse_timestamp(timestamp_str):
    try:
        # Parse the input format: MM-DD-YYYY HH:MM
        dt = datetime.strptime(timestamp_str, "%m-%d-%Y %H:%M")
        # Return in MySQL format: YYYY-MM-DD HH:MM:SS
        return dt.strftime("%Y-%m-%d %H:%M:00")
    except ValueError:
        return None


""" List all employees and their details"""
def list_employees():
    with get_conn() as conn:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT employee_id, full_name, department, role, salary, last_updated FROM employees;")
        rows = cur.fetchall()
        cur.close()

    if not rows:
        print("[yellow]No employees found.[/yellow]")
        return

    table = [
        [
            r["employee_id"],
            r["full_name"],
            r["department"],
            r["role"] or "N/A",
            r["salary"],
            r["last_updated"],
        ]
        for r in rows
    ]
    headers = ["ID", "Name", "Department", "Role", "Salary", "Last Updated"]
    print("[bold magenta]Employees:[/bold magenta]")
    print(tabulate(table, headers=headers, tablefmt="grid"))

""" Update employee salary """
def update_salary():
    username = input("Enter your username (for audit log): ").strip()
    role = select_authorized_role()
    if role is None:
        print("[red]Update cancelled due to invalid role selection.[/red]")
        return

    # Validate that the username has the selected role
    with get_conn() as conn:
        cur = conn.cursor()
        if not validate_user_role(cur, username, role):
            print(f"[red]Authorization failed: User '{username}' does not have the role '{role}'.[/red]")
            cur.close()
            return
        cur.close()

    try:
        employee_id = int(input("Enter employee ID to update: ").strip())
        new_salary = float(input("Enter new salary: ").strip())
    except ValueError:
        print("[red]Invalid number entered.[/red]")
        return

    justification = input("Enter justification for this change: ").strip() or None

    with get_conn() as conn:
        cur = conn.cursor()

        # Set session identity for trigger
        set_app_identity(cur, username, role, justification)

        # Optional: show old salary first
        cur.execute("SELECT salary FROM employees WHERE employee_id = %s;", (employee_id,))
        row = cur.fetchone()
        if not row:
            print(f"[red]Employee with ID {employee_id} not found.[/red]")
            cur.close()
            return

        old_salary = row[0]
        print(f"Old salary: {old_salary}")

        # Perform the update (trigger will log to audit_log)
        cur.execute(
            """
            UPDATE employees
            SET salary = %s
            WHERE employee_id = %s;
            """,
            (new_salary, employee_id),
        )

        conn.commit()
        cur.close()

    print(f"[green]Updated salary for employee {employee_id}: {old_salary} -> {new_salary}[/green]")

""" Update employee name"""
def update_name():
    username = input("Enter your username (for audit log): ").strip()
    role = select_authorized_role()
    if role is None:
        print("[red]Update cancelled due to invalid role selection.[/red]")
        return

    # Validate that the username has the selected role
    with get_conn() as conn:
        cur = conn.cursor()
        if not validate_user_role(cur, username, role):
            print(f"[red]Authorization failed: User '{username}' does not have the role '{role}'.[/red]")
            cur.close()
            return
        cur.close()

    try:
        employee_id = int(input("Enter employee ID to update: ").strip())
    except ValueError:
        print("[red]Invalid number entered.[/red]")
        return

    new_name = input("Enter new full name: ").strip()
    if not new_name:
        print("[red]Name cannot be empty.[/red]")
        return

    justification = input("Enter justification for this change: ").strip() or None

    with get_conn() as conn:
        cur = conn.cursor()

        # Set session identity for trigger
        set_app_identity(cur, username, role, justification)

        # Show old name first
        cur.execute("SELECT full_name FROM employees WHERE employee_id = %s;", (employee_id,))
        row = cur.fetchone()
        if not row:
            print(f"[red]Employee with ID {employee_id} not found.[/red]")
            cur.close()
            return

        old_name = row[0]
        print(f"Old name: {old_name}")

        # Perform the update (trigger will log to audit_log)
        cur.execute(
            """
            UPDATE employees
            SET full_name = %s
            WHERE employee_id = %s;
            """,
            (new_name, employee_id),
        )

        conn.commit()
        cur.close()

    print(f"[green]Updated name for employee {employee_id}: {old_name} -> {new_name}[/green]")

""" Update employee department and role """
def update_department():
    username = input("Enter your username (for audit log): ").strip()
    auth_role = select_authorized_role()
    if auth_role is None:
        print("[red]Update cancelled due to invalid role selection.[/red]")
        return

    # Validate that the username has the selected role
    with get_conn() as conn:
        cur = conn.cursor()
        if not validate_user_role(cur, username, auth_role):
            print(f"[red]Authorization failed: User '{username}' does not have the role '{auth_role}'.[/red]")
            cur.close()
            return
        cur.close()

    try:
        employee_id = int(input("Enter employee ID to update: ").strip())
    except ValueError:
        print("[red]Invalid number entered.[/red]")
        return

    # Select new department from list
    new_department = select_department()
    if new_department is None:
        print("[red]Update cancelled due to invalid department selection.[/red]")
        return

    # Select new role for the chosen department
    new_role = select_role_for_department(new_department)
    if new_role is None:
        print("[red]Update cancelled due to invalid role selection.[/red]")
        return

    justification = input("Enter justification for this change: ").strip() or None

    with get_conn() as conn:
        cur = conn.cursor()

        # Set session identity for trigger
        set_app_identity(cur, username, auth_role, justification)

        # Show old department and role first
        cur.execute("SELECT department, role FROM employees WHERE employee_id = %s;", (employee_id,))
        row = cur.fetchone()
        if not row:
            print(f"[red]Employee with ID {employee_id} not found.[/red]")
            cur.close()
            return

        old_department = row[0]
        old_role = row[1]
        print(f"Old department: {old_department}, Old role: {old_role}")

        # Perform the update (trigger will log both changes to audit_log)
        cur.execute(
            """
            UPDATE employees
            SET department = %s, role = %s
            WHERE employee_id = %s;
            """,
            (new_department, new_role, employee_id),
        )

        conn.commit()
        cur.close()

    print(f"[green]Updated employee {employee_id}:[/green]")
    print(f"  Department: {old_department} -> {new_department}")
    print(f"  Role: {old_role} -> {new_role}")

""" Update employee role """
def update_role():
    username = input("Enter your username (for audit log): ").strip()
    role = select_authorized_role()
    if role is None:
        print("[red]Update cancelled due to invalid role selection.[/red]")
        return

    # Validate that the username has the selected role
    with get_conn() as conn:
        cur = conn.cursor()
        if not validate_user_role(cur, username, role):
            print(f"[red]Authorization failed: User '{username}' does not have the role '{role}'.[/red]")
            cur.close()
            return
        cur.close()

    try:
        employee_id = int(input("Enter employee ID to update: ").strip())
    except ValueError:
        print("[red]Invalid number entered.[/red]")
        return

    # Show available roles by department
    print("\n[bold cyan]Available Roles by Department:[/bold cyan]")
    print("[bold]HR:[/bold] HR Manager, Payroll Specialist, Benefits Specialist, Recruiter")
    print("[bold]Accounting:[/bold] CFO, Staff Accountant, Financial Analyst, Auditor")
    print("[bold]IT:[/bold] CIO, Software Engineer, System Administrator, Helpdesk II, Helpdesk I")
    print("[bold]Sales:[/bold] Sales Manager, Sales Associate II, Sales Associate I")
    print("[bold]Marketing:[/bold] Marketing Manager, Advertising Specialist, Social Media Specialist")
    print("[bold]Legal:[/bold] CLO, Senior Legal Counsel, IP Lawyer, Employment Lawyer")
    print("[bold]Customer Service:[/bold] Customer Service Manager, CSR I, CSR II\n")

    new_role = input("Enter new role: ").strip()
    if not new_role:
        print("[red]Role cannot be empty.[/red]")
        return

    justification = input("Enter justification for this change: ").strip() or None

    with get_conn() as conn:
        cur = conn.cursor()

        # Set session identity for trigger
        set_app_identity(cur, username, role, justification)

        # Show old role first
        cur.execute("SELECT role, department FROM employees WHERE employee_id = %s;", (employee_id,))
        row = cur.fetchone()
        if not row:
            print(f"[red]Employee with ID {employee_id} not found.[/red]")
            cur.close()
            return

        old_role = row[0]
        department = row[1]
        print(f"Old role: {old_role}")
        print(f"Department: {department}")

        # Perform the update (trigger will log to audit_log)
        cur.execute(
            """
            UPDATE employees
            SET role = %s
            WHERE employee_id = %s;
            """,
            (new_role, employee_id),
        )

        conn.commit()
        cur.close()

    print(f"[green]Updated role for employee {employee_id}: {old_role} -> {new_role}[/green]")


def show_menu():
    print("\n[bold blue]Employee Information Audit[/bold blue]")
    print("[bold]Menu:[/bold]")
    print("  1) List employees")
    print("  2) Update employee salary")
    print("  3) Update employee name")
    print("  4) Update employee department")
    print("  5) Update employee role")
    print("  6) Show salary changes in the last month")
    print("  7) Show name changes in the last month")
    print("  8) Show department changes in the last month")
    print("  9) Show all changes in a date range")
    print("  10) Trace field history")
    print("  11) Show all changes organized by user")
    print("  12) Show all changes organized by role")
    print("  13) Exit")


def main():
    while True:
        show_menu()
        choice = input("Choose an option (1-13): ").strip()

        if choice == "1":
            list_employees()
        elif choice == "2":
            update_salary()
        elif choice == "3":
            update_name()
        elif choice == "4":
            update_department()
        elif choice == "5":
            update_role()
        elif choice == "6":
            print_salary_changes_last_month()
        elif choice == "7":
            print_name_changes_last_month()
        elif choice == "8":
            print_department_changes_last_month()
        elif choice == "9":
            start_input = input("Enter start timestamp (MM-DD-YYYY HH:MM): ").strip()
            start_ts = parse_timestamp(start_input)
            if start_ts is None:
                print("[red]Invalid start timestamp format. Please use MM-DD-YYYY HH:MM[/red]")
                continue

            end_input = input("Enter end timestamp   (MM-DD-YYYY HH:MM): ").strip()
            end_ts = parse_timestamp(end_input)
            if end_ts is None:
                print("[red]Invalid end timestamp format. Please use MM-DD-YYYY HH:MM[/red]")
                continue

            print_changes_in_range(start_ts, end_ts)
        elif choice == "10":
            try:
                employee_id = int(input("Enter employee ID: ").strip())
                print("Field options: salary, full_name, department, role")
                field_name = input("Enter field name: ").strip()
                print_field_history(employee_id, field_name)
            except ValueError:
                print("[red]Invalid employee ID.[/red]")
        elif choice == "11":
            print_all_changes_by_user()
        elif choice == "12":
            print_all_changes_by_role()
        elif choice == "13":
            print("[bold green]Goodbye![/bold green]")
            break
        else:
            print("[red]Invalid option. Please enter 1-13.[/red]")


if __name__ == "__main__":
    main()
