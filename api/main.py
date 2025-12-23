# api/main.py
import logging

from fastapi import FastAPI
# from api.routes import router
from api.routes import router, metrics_router

from core.database import engine, SessionLocal
from core.models import Base

from ingestion.etl_runner import run_etl

logging.basicConfig(level=logging.INFO)

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Kasparro ETL Backend",
    version="1.0.0"
)

# -------------------------------------------------
# ROOT ENDPOINT (REQUIRED FOR RAILWAY)
# -------------------------------------------------
@app.get("/")
def root():
    return {
        "service": "Kasparro ETL Backend",
        "status": "running",
        "docs": "/docs"
    }

# -------------------------------------------------
# STARTUP ETL (NON-BLOCKING)
# -------------------------------------------------
@app.on_event("startup")
def startup_etl():
    db = SessionLocal()
    try:
        run_etl(db)
        logging.info("ETL completed successfully on startup")
    except Exception as e:
        logging.error(f"ETL failed on startup: {e}")
    finally:
        db.close()

# -------------------------------------------------
# ROUTES
# -------------------------------------------------
app.include_router(router)
app.include_router(metrics_router)







