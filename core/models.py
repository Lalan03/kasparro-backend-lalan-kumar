#core/models.py
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    JSON,
    UniqueConstraint,
)
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

# =====================================================
# RAW DATA LAYER (P0 REQUIREMENT)
# =====================================================

class RawAPIData(Base):
    __tablename__ = "raw_api_data"

    id = Column(Integer, primary_key=True)
    payload = Column(JSON, nullable=False)
    fetched_at = Column(DateTime, default=datetime.utcnow)


class RawCSVData(Base):
    __tablename__ = "raw_csv_data"

    id = Column(Integer, primary_key=True)
    payload = Column(JSON, nullable=False)
    fetched_at = Column(DateTime, default=datetime.utcnow)


class RawThirdSourceData(Base):
    __tablename__ = "raw_third_source_data"

    id = Column(Integer, primary_key=True)
    payload = Column(JSON, nullable=False)
    fetched_at = Column(DateTime, default=datetime.utcnow)


# =====================================================
# CHECKPOINT / INCREMENTAL INGESTION (P1 REQUIREMENT)
# =====================================================

class ETLCheckpoint(Base):
    __tablename__ = "etl_checkpoint"

    id = Column(Integer, primary_key=True)
    source = Column(String, unique=True, nullable=False)
    last_offset = Column(String, nullable=True)
    updated_at = Column(DateTime, default=datetime.utcnow)


# =====================================================
# UNIFIED DATA (CORE OUTPUT)
# =====================================================

class UnifiedData(Base):
    __tablename__ = "unified_data"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    value = Column(Float, nullable=False)
    source = Column(String, nullable=False)
    ingested_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("name", "source", name="uq_name_source"),
    )


# =====================================================
# ETL AUDIT / STATS (P1 REQUIREMENT)
# =====================================================

class ETLRun(Base):
    __tablename__ = "etl_runs"

    id = Column(Integer, primary_key=True)
    status = Column(String, nullable=False)
    records_processed = Column(Integer, nullable=False)
    duration_ms = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, default=datetime.utcnow)

