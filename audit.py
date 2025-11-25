# Auditing functions
from tabulate import tabulate
from rich import print

from database import get_conn

""" Shows all salary changes in the last month """
def get_salary_changes_last_month():
    with get_conn() as conn:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            """
            SELECT
                audit_id,
                row_id      AS employee_id,
                old_value   AS old_salary,
                new_value   AS new_salary,
                changed_by,
                changed_role,
                changed_at
            FROM audit_log
            WHERE table_name = 'employees'
              AND column_name = 'salary'
              AND changed_at >= NOW() - INTERVAL 1 MONTH
            ORDER BY changed_at DESC;
            """
        )
        rows = cur.fetchall()
        cur.close()
        return rows

""" Get all changes between start_time and end_time. """
def get_changes_in_range(start_time: str, end_time: str):
    
    with get_conn() as conn:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            """
            SELECT *
            FROM audit_log
            WHERE changed_at BETWEEN %s AND %s
            ORDER BY changed_at;
            """,
            (start_time, end_time),
        )
        rows = cur.fetchall()
        cur.close()
        return rows

""" Shows all salary changes in the last month """
def print_salary_changes_last_month():
    rows = get_salary_changes_last_month()
    if not rows:
        print("[yellow]No salary changes in the last month.[/yellow]")
        return

    table = [
        [
            r["audit_id"],
            r["employee_id"],
            r["old_salary"],
            r["new_salary"],
            r["changed_by"],
            r["changed_role"],
            r["changed_at"],
        ]
        for r in rows
    ]
    headers = ["Audit ID", "Employee ID", "Old Salary", "New Salary",
               "Changed By", "Role", "Changed At"]
    print("[bold cyan]Salary changes in the last month:[/bold cyan]")
    print(tabulate(table, headers=headers, tablefmt="grid"))

""" Display all changes made in a specific time range """
def print_changes_in_range(start_time: str, end_time: str):
    rows = get_changes_in_range(start_time, end_time)
    if not rows:
        print(f"[yellow]No changes between {start_time} and {end_time}.[/yellow]")
        return

    table = [
        [
            r["audit_id"],
            r["table_name"],
            r["row_id"],
            r["column_name"],
            r["old_value"],
            r["new_value"],
            r["changed_by"],
            r["changed_role"],
            r["changed_at"],
        ]
        for r in rows
    ]
    headers = [
        "Audit ID", "Table", "Row ID", "Column",
        "Old Value", "New Value", "Changed By",
        "Role", "Changed At",
    ]
    print(f"[bold cyan]Changes between {start_time} and {end_time}:[/bold cyan]")
    print(tabulate(table, headers=headers, tablefmt="grid"))

""" Shows all name changes in the last month """
def get_name_changes_last_month():
    with get_conn() as conn:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            """
            SELECT
                audit_id,
                row_id      AS employee_id,
                old_value   AS old_name,
                new_value   AS new_name,
                changed_by,
                changed_role,
                changed_at
            FROM audit_log
            WHERE table_name = 'employees'
              AND column_name = 'full_name'
              AND changed_at >= NOW() - INTERVAL 1 MONTH
            ORDER BY changed_at DESC;
            """
        )
        rows = cur.fetchall()
        cur.close()
        return rows

""" Shows all department changes in the last month """
def get_department_changes_last_month():
    with get_conn() as conn:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            """
            SELECT
                audit_id,
                row_id      AS employee_id,
                old_value   AS old_department,
                new_value   AS new_department,
                changed_by,
                changed_role,
                changed_at
            FROM audit_log
            WHERE table_name = 'employees'
              AND column_name = 'department'
              AND changed_at >= NOW() - INTERVAL 1 MONTH
            ORDER BY changed_at DESC;
            """
        )
        rows = cur.fetchall()
        cur.close()
        return rows

""" Shows all name changes in the last month """
def print_name_changes_last_month():
    rows = get_name_changes_last_month()
    if not rows:
        print("[yellow]No name changes in the last month.[/yellow]")
        return

    table = [
        [
            r["audit_id"],
            r["employee_id"],
            r["old_name"],
            r["new_name"],
            r["changed_by"],
            r["changed_role"],
            r["changed_at"],
        ]
        for r in rows
    ]
    headers = ["Audit ID", "Employee ID", "Old Name", "New Name",
               "Changed By", "Role", "Changed At"]
    print("[bold cyan]Name changes in the last month:[/bold cyan]")
    print(tabulate(table, headers=headers, tablefmt="grid"))


def print_department_changes_last_month():
    rows = get_department_changes_last_month()
    if not rows:
        print("[yellow]No department changes in the last month.[/yellow]")
        return

    table = [
        [
            r["audit_id"],
            r["employee_id"],
            r["old_department"],
            r["new_department"],
            r["changed_by"],
            r["changed_role"],
            r["changed_at"],
        ]
        for r in rows
    ]
    headers = ["Audit ID", "Employee ID", "Old Department", "New Department",
               "Changed By", "Role", "Changed At"]
    print("[bold cyan]Department changes in the last month:[/bold cyan]")
    print(tabulate(table, headers=headers, tablefmt="grid"))


    """
    Shows the complete provenance chain for a specific field of an employee.
    Traces all changes from the initial value to the current value.
    """
def trace_field_history(employee_id: int, field_name: str):
    with get_conn() as conn:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            """
            SELECT
                audit_id,
                old_value,
                new_value,
                changed_by,
                changed_role,
                justification,
                changed_at
            FROM audit_log
            WHERE table_name = 'employees'
              AND row_id = %s
              AND column_name = %s
            ORDER BY changed_at ASC;
            """,
            (employee_id, field_name),
        )
        rows = cur.fetchall()
        cur.close()
        return rows


    """
    Displays the complete history/provenance chain for a specific field.
    """
def print_field_history(employee_id: int, field_name: str):
    rows = trace_field_history(employee_id, field_name)
    if not rows:
        print(f"[yellow]No change history found for employee {employee_id}'s {field_name}.[/yellow]")
        return

    # Get current value
    with get_conn() as conn:
        cur = conn.cursor(dictionary=True)
        cur.execute(f"SELECT {field_name} FROM employees WHERE employee_id = %s;", (employee_id,))
        current_row = cur.fetchone()
        cur.close()
        current_value = current_row[field_name] if current_row else "N/A"

    print(f"[bold cyan]Complete Provenance Chain for Employee {employee_id} - {field_name}:[/bold cyan]")
    print(f"[bold green]Current Value:[/bold green] {current_value}\n")

    table = [
        [
            r["audit_id"],
            r["old_value"],
            r["new_value"],
            r["changed_by"],
            r["changed_role"] or "N/A",
            r["justification"] or "N/A",
            r["changed_at"],
        ]
        for r in rows
    ]
    headers = ["Audit ID", "Old Value", "New Value", "Changed By",
               "Role", "Justification", "Changed At"]
    print(tabulate(table, headers=headers, tablefmt="grid"))


def get_all_changes_for_employee(employee_id: int):
    """
    Get all changes made to a specific employee across all fields.
    """
    with get_conn() as conn:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            """
            SELECT
                audit_id,
                column_name,
                old_value,
                new_value,
                changed_by,
                changed_role,
                justification,
                changed_at
            FROM audit_log
            WHERE table_name = 'employees'
              AND row_id = %s
            ORDER BY changed_at ASC;
            """,
            (employee_id,)
        )
        rows = cur.fetchall()
        cur.close()
        return rows


def print_all_changes_for_employee(employee_id: int):
    """
    Display all changes made to a specific employee across all fields.
    """
    rows = get_all_changes_for_employee(employee_id)
    if not rows:
        print(f"[yellow]No change history found for employee {employee_id}.[/yellow]")
        return

    # Get current employee info
    with get_conn() as conn:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            "SELECT employee_id, full_name, department, role, salary FROM employees WHERE employee_id = %s;",
            (employee_id,)
        )
        current_row = cur.fetchone()
        cur.close()

    if current_row:
        print(f"[bold cyan]Complete Change History for Employee {employee_id}:[/bold cyan]")
        print(f"[bold green]Current Info:[/bold green] {current_row['full_name']} | {current_row['department']} | {current_row['role']} | ${current_row['salary']}\n")
    else:
        print(f"[bold cyan]Complete Change History for Employee {employee_id}:[/bold cyan]")
        print(f"[yellow]Employee not found in current records.[/yellow]\n")

    table = [
        [
            r["audit_id"],
            r["column_name"],
            r["old_value"],
            r["new_value"],
            r["changed_by"],
            r["changed_role"] or "N/A",
            r["justification"] or "N/A",
            r["changed_at"],
        ]
        for r in rows
    ]
    headers = ["Audit ID", "Field", "Old Value", "New Value", "Changed By",
               "Role", "Justification", "Changed At"]
    print(tabulate(table, headers=headers, tablefmt="grid"))


    """
    Get all changes made by a specific user.
    """
def get_changes_by_user(username: str):
    with get_conn() as conn:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            """
            SELECT *
            FROM audit_log
            WHERE changed_by = %s
            ORDER BY changed_at DESC;
            """,
            (username,)
        )
        rows = cur.fetchall()
        cur.close()
        return rows


    """
    Display all changes made by a specific user.
    """
def print_changes_by_user(username: str):
    rows = get_changes_by_user(username)
    if not rows:
        print(f"[yellow]No changes found for user '{username}'.[/yellow]")
        return

    table = [
        [
            r["audit_id"],
            r["table_name"],
            r["row_id"],
            r["column_name"],
            r["old_value"],
            r["new_value"],
            r["changed_role"] or "N/A",
            r["justification"] or "N/A",
            r["changed_at"],
        ]
        for r in rows
    ]
    headers = [
        "Audit ID", "Table", "Row ID", "Column",
        "Old Value", "New Value", "Role", "Justification", "Changed At"
    ]
    print(f"[bold cyan]All changes by user '{username}':[/bold cyan]")
    print(tabulate(table, headers=headers, tablefmt="grid"))


def get_all_changes_organized_by_user():
    """
    Get all changes from audit log organized by user.
    """
    with get_conn() as conn:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            """
            SELECT *
            FROM audit_log
            ORDER BY changed_by, changed_at DESC;
            """
        )
        rows = cur.fetchall()
        cur.close()
        return rows


def print_all_changes_by_user():
    """
    Display all changes organized by user.
    """
    rows = get_all_changes_organized_by_user()
    if not rows:
        print("[yellow]No changes found in audit log.[/yellow]")
        return

    # Group changes by user
    from collections import defaultdict
    changes_by_user = defaultdict(list)

    for row in rows:
        username = row["changed_by"] or "Unknown/No User"
        changes_by_user[username].append(row)

    # Display changes for each user
    print("[bold cyan]All Changes Organized by User:[/bold cyan]\n")

    for username in sorted(changes_by_user.keys()):
        user_changes = changes_by_user[username]
        print(f"\n[bold magenta]User: {username}[/bold magenta] ([green]{len(user_changes)} change(s)[/green])")

        table = [
            [
                r["audit_id"],
                r["table_name"],
                r["row_id"],
                r["column_name"],
                r["old_value"],
                r["new_value"],
                r["changed_role"] or "N/A",
                r["justification"] or "N/A",
                r["changed_at"],
            ]
            for r in user_changes
        ]
        headers = [
            "Audit ID", "Table", "Row ID", "Column",
            "Old Value", "New Value", "Role", "Justification", "Changed At"
        ]
        print(tabulate(table, headers=headers, tablefmt="grid"))


def get_changes_by_role(role: str):
    """
    Get all changes made by users with a specific role.
    """
    with get_conn() as conn:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            """
            SELECT *
            FROM audit_log
            WHERE changed_role = %s
            ORDER BY changed_at DESC;
            """,
            (role,)
        )
        rows = cur.fetchall()
        cur.close()
        return rows


def print_changes_by_role(role: str):
    """
    Display all changes made by users with a specific role.
    """
    rows = get_changes_by_role(role)
    if not rows:
        print(f"[yellow]No changes found for role '{role}'.[/yellow]")
        return

    table = [
        [
            r["audit_id"],
            r["table_name"],
            r["row_id"],
            r["column_name"],
            f"[white]{r['old_value']}[/white]" if r["column_name"] == "salary" else r["old_value"],
            f"[white]{r['new_value']}[/white]" if r["column_name"] == "salary" else r["new_value"],
            r["changed_by"],
            r["justification"] or "N/A",
            r["changed_at"],
        ]
        for r in rows
    ]
    headers = [
        "Audit ID", "Table", "Row ID", "Column",
        "Old Value", "New Value", "Changed By", "Justification", "Changed At"
    ]
    print(f"[bold cyan]All changes by role '{role}':[/bold cyan]")
    print(tabulate(table, headers=headers, tablefmt="grid"))


def get_all_changes_organized_by_role():
    """
    Get all changes from audit log organized by role.
    """
    with get_conn() as conn:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            """
            SELECT *
            FROM audit_log
            ORDER BY changed_role, changed_at DESC;
            """
        )
        rows = cur.fetchall()
        cur.close()
        return rows


def print_all_changes_by_role():
    """
    Display all changes organized by role.
    """
    rows = get_all_changes_organized_by_role()
    if not rows:
        print("[yellow]No changes found in audit log.[/yellow]")
        return

    # Group changes by role
    from collections import defaultdict
    changes_by_role = defaultdict(list)

    for row in rows:
        role = row["changed_role"] or "Unknown/No Role"
        changes_by_role[role].append(row)

    # Display changes for each role
    print("[bold cyan]All Changes Organized by Role:[/bold cyan]\n")

    for role in sorted(changes_by_role.keys()):
        role_changes = changes_by_role[role]
        print(f"\n[bold magenta]Role: {role}[/bold magenta] ([green]{len(role_changes)} change(s)[/green])")

        table = [
            [
                r["audit_id"],
                r["table_name"],
                r["row_id"],
                r["column_name"],
                r["old_value"],
                r["new_value"],
                r["changed_by"],
                r["justification"] or "N/A",
                r["changed_at"],
            ]
            for r in role_changes
        ]
        headers = [
            "Audit ID", "Table", "Row ID", "Column",
            "Old Value", "New Value", "Changed By", "Justification", "Changed At"
        ]
        print(tabulate(table, headers=headers, tablefmt="grid"))
