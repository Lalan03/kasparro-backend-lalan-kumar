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
    if _engine is None:
        raise RuntimeError("Engine not initialized")
    return _engine


def get_sessionmaker():
    if _SessionLocal is None:
        raise RuntimeError("SessionLocal not initialized")
    return _SessionLocal


def get_db():
    SessionLocal = get_sessionmaker()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
