import os
from contextlib import contextmanager

import mysql.connector
from dotenv import load_dotenv
from rich import print

load_dotenv()  # Load .env file

# db creds
def get_db_config():
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER", "admin"),
        "password": os.getenv("DB_PASS", "D@ataProvenance123!"),
        "database": os.getenv("DB_NAME", "dataprovenance_db"),
    }


# Starts and ends db connection
@contextmanager
def get_conn():
    config = get_db_config()
    conn = mysql.connector.connect(**config)
    try:
        yield conn
    finally:
        conn.close()


def set_app_identity(cursor, username: str, role: str | None, justification: str | None = None):
    """
    Set session variables used by the MySQL trigger to know who is making changes.
    Must be called on the same connection before UPDATE statements.
    """
    cursor.execute("SET @app_current_user = %s;", (username,))
    cursor.execute("SET @app_current_role = %s;", (role,))
    cursor.execute("SET @app_justification = %s;", (justification,))
    print(f"[green]Session identity set:[/green] user={username}, role={role}")


def validate_user_role(cursor, username: str, role: str) -> bool:
    """
    Validates that the given username exists in the employees table with the specified role.
    Returns True if the user has the role, False otherwise.
    """
    cursor.execute(
        """
        SELECT COUNT(*) as count
        FROM employees
        WHERE full_name = %s AND role = %s;
        """,
        (username, role)
    )
    result = cursor.fetchone()
    return result[0] > 0 if result else False
