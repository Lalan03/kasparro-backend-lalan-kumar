# core/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings

_engine = None
_SessionLocal = None


def init_engine():
    global _engine, _SessionLocal
    if _engine is None:
        _engine = create_engine(
            settings.DATABASE_URL,
            pool_pre_ping=True,
        )
        _SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=_engine,
        )


def get_engine():
    return _engine


def get_session():
    if _SessionLocal is None:
        raise RuntimeError("Database not initialized. Call init_engine() first.")
    return _SessionLocal


def get_db():
    SessionLocal = get_session()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
