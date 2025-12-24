# api/main.py

import logging
from fastapi import FastAPI

from core.database import init_engine, get_engine
from core.models import Base
from api.routes import router, metrics_router
from ingestion.etl_runner import run_etl
from core.database import get_sessionmaker

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Kasparro ETL")


@app.on_event("startup")
def startup():
    # 1️⃣ Initialize DB engine
    init_engine()

    # 2️⃣ Create tables
    engine = get_engine()
    Base.metadata.create_all(bind=engine)

    # 3️⃣ Run ETL safely
    SessionLocal = get_sessionmaker()
    db = SessionLocal()
    try:
        run_etl(db)
        logging.info("ETL completed successfully on startup")
    except Exception as e:
        logging.error(f"ETL failed on startup: {e}")
    finally:
        db.close()


@app.get("/")
def root():
    return {"status": "running"}



app.include_router(router)
app.include_router(metrics_router)
