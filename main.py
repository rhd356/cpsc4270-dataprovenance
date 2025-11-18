# Main application
from tabulate import tabulate
from rich import print

from database import get_conn, set_app_identity
from audit import (
    print_salary_changes_last_month,
    print_name_changes_last_month,
    print_department_changes_last_month,
    print_changes_in_range,
)

# List all employees and their details
def list_employees():
    with get_conn() as conn:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT employee_id, full_name, department, salary, last_updated FROM employees;")
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
            r["salary"],
            r["last_updated"],
        ]
        for r in rows
    ]
    headers = ["ID", "Name", "Department", "Salary", "Last Updated"]
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
    role = input("Enter your role (e.g., HR_Manager): ").strip() or None

    with get_conn() as conn:
        cur = conn.cursor()

        # Set session identity for trigger
        set_app_identity(cur, username, role)

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
    role = input("Enter your role (e.g., HR_Manager): ").strip() or None

    with get_conn() as conn:
        cur = conn.cursor()

        # Set session identity for trigger
        set_app_identity(cur, username, role)

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
    role = input("Enter your role (e.g., HR_Manager): ").strip() or None

    with get_conn() as conn:
        cur = conn.cursor()

        # Set session identity for trigger
        set_app_identity(cur, username, role)

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


def show_menu():
    print("\n[bold blue]Employee Information Audit[/bold blue]")
    print("[bold]Menu:[/bold]")
    print("  1) List employees")
    print("  2) Update employee salary")
    print("  3) Update employee name")
    print("  4) Update employee department")
    print("  5) Show salary changes in the last month")
    print("  6) Show name changes in the last month")
    print("  7) Show department changes in the last month")
    print("  8) Show all changes in a date range")
    print("  9) Exit")


def main():
    while True:
        show_menu()
        choice = input("Choose an option (1-9): ").strip()

        if choice == "1":
            list_employees()
        elif choice == "2":
            update_salary()
        elif choice == "3":
            update_name()
        elif choice == "4":
            update_department()
        elif choice == "5":
            print_salary_changes_last_month()
        elif choice == "6":
            print_name_changes_last_month()
        elif choice == "7":
            print_department_changes_last_month()
        elif choice == "8":
            start_ts = input("Enter start timestamp (YYYY-MM-DD HH:MM:SS): ").strip()
            end_ts = input("Enter end timestamp   (YYYY-MM-DD HH:MM:SS): ").strip()
            print_changes_in_range(start_ts, end_ts)
        elif choice == "9":
            print("[bold green]Goodbye![/bold green]")
            break
        else:
            print("[red]Invalid option. Please enter 1-9.[/red]")


if __name__ == "__main__":
    main()
