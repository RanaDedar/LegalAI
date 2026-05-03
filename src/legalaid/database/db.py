import re
from sqlalchemy import create_engine, text
from sqlalchemy.engine.url import make_url
from sqlalchemy.orm import sessionmaker, declarative_base

from legalaid.database.setting import setting

Base = declarative_base()
engine = create_engine(url=setting.DB_CONNECTION)
Local_Session = sessionmaker(bind=engine)


def ensure_postgres_database(url_str: str) -> None:
    if not url_str or not url_str.startswith("postgresql"):
        return
    url = make_url(url_str)
    dbname = url.database
    if not dbname or not re.fullmatch(r"[A-Za-z0-9_]+", dbname):
        return
    admin_url = url.set(database="postgres")
    admin_engine = create_engine(admin_url, isolation_level="AUTOCOMMIT")
    try:
        with admin_engine.connect() as conn:
            exists = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :name"),
                {"name": dbname},
            ).scalar()
            if not exists:
                conn.execute(text(f'CREATE DATABASE "{dbname}"'))
    finally:
        admin_engine.dispose()


def get_db():
    session = Local_Session()
    try:
        yield session
    finally:
        session.close()

