import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


def get_database_url() -> str:
    return os.getenv(
        "DATABASE_URL",
        "mssql+pyodbc://sa:password@localhost:1433/machinemgmt?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes",
    )


engine = create_engine(get_database_url(), pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
