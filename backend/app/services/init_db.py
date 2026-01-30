import os

import pyodbc
from sqlalchemy.engine.url import make_url


def create_database_if_missing():
    database_url = os.getenv(
        "DATABASE_URL",
        "mssql+pyodbc://sa:password@localhost:1433/machinemgmt?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes",
    )
    url = make_url(database_url)
    database = url.database
    if not database:
        return
    driver = url.query.get("driver", "ODBC Driver 18 for SQL Server")
    trust_cert = url.query.get("TrustServerCertificate", "yes")
    server = url.host
    port = url.port or 1433
    user = url.username
    password = url.password
    conn_str = (
        f"DRIVER={{{driver}}};SERVER={server},{port};DATABASE=master;UID={user};PWD={password};"
        f"TrustServerCertificate={trust_cert};"
    )
    with pyodbc.connect(conn_str, autocommit=True) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = ?) BEGIN CREATE DATABASE "
            + database
            + " END",
            database,
        )


if __name__ == "__main__":
    create_database_if_missing()
