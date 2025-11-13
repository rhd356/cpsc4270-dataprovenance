import os
from contextlib import contextmanager

import mysql.connector
from dotenv import load_dotenv
from rich import print

load_dotenv()  # Load .env file


def get_db_config():
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER", "admin"),
        "password": os.getenv("DB_PASS", "dataprovenance"),
        "database": os.getenv("DB_NAME", "dataprovenance_db"),
    }


@contextmanager
def get_conn():
    config = get_db_config()
    conn = mysql.connector.connect(**config)
    try:
        yield conn
    finally:
        conn.close()


def set_app_identity(cursor, username: str, role: str | None):
    """
    Set session variables used by the MySQL trigger to know who is making changes.
    Must be called on the same connection before UPDATE statements.
    """
    cursor.execute("SET @app_current_user = %s;", (username,))
    cursor.execute("SET @app_current_role = %s;", (role,))
    print(f"[green]Session identity set:[/green] user={username}, role={role}")
