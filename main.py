# Main application
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


def select_authorized_role():
    """
    Prompts the user to select their role from the authorized list.
    Returns the selected role or None if the selection is invalid.
    """
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


# List all employees and their details
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


def update_salary():
    try:
        employee_id = int(input("Enter employee ID to update: ").strip())
        new_salary = float(input("Enter new salary: ").strip())
    except ValueError:
        print("[red]Invalid number entered.[/red]")
        return

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


def update_name():
    try:
        employee_id = int(input("Enter employee ID to update: ").strip())
    except ValueError:
        print("[red]Invalid number entered.[/red]")
        return

    new_name = input("Enter new full name: ").strip()
    if not new_name:
        print("[red]Name cannot be empty.[/red]")
        return

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


def update_department():
    try:
        employee_id = int(input("Enter employee ID to update: ").strip())
    except ValueError:
        print("[red]Invalid number entered.[/red]")
        return

    new_department = input("Enter new department: ").strip()
    if not new_department:
        print("[red]Department cannot be empty.[/red]")
        return

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

    justification = input("Enter justification for this change: ").strip() or None

    with get_conn() as conn:
        cur = conn.cursor()

        # Set session identity for trigger
        set_app_identity(cur, username, role, justification)

        # Show old department first
        cur.execute("SELECT department FROM employees WHERE employee_id = %s;", (employee_id,))
        row = cur.fetchone()
        if not row:
            print(f"[red]Employee with ID {employee_id} not found.[/red]")
            cur.close()
            return

        old_department = row[0]
        print(f"Old department: {old_department}")

        # Perform the update (trigger will log to audit_log)
        cur.execute(
            """
            UPDATE employees
            SET department = %s
            WHERE employee_id = %s;
            """,
            (new_department, employee_id),
        )

        conn.commit()
        cur.close()

    print(f"[green]Updated department for employee {employee_id}: {old_department} -> {new_department}[/green]")


def update_role():
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
            start_ts = input("Enter start timestamp (YYYY-MM-DD HH:MM:SS): ").strip()
            end_ts = input("Enter end timestamp   (YYYY-MM-DD HH:MM:SS): ").strip()
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
