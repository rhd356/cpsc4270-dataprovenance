# Auditing functions
from tabulate import tabulate
from rich import print

from database import get_conn


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


def get_changes_in_range(start_time: str, end_time: str):
    """
    Get all changes between start_time and end_time (strings like '2025-10-01 00:00:00').
    """
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
