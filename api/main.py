import logging
from fastapi import FastAPI
from api.routes import router, metrics_router
from core.database import init_engine, SessionLocal
from core.models import Base
from ingestion.etl_runner import run_etl

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Kasparro ETL Backend",
    version="1.0.0",
)

# -------------------------------------------------
# ROOT (REQUIRED BY RAILWAY)
# -------------------------------------------------
@app.get("/")
def root():
    return {
        "service": "Kasparro ETL Backend",
        "status": "running",
        "docs": "/docs",
    }


# -------------------------------------------------
# STARTUP
# -------------------------------------------------
@app.on_event("startup")
def startup():
    # 1. Init DB engine safely
    init_engine()

    # 2. Create tables AFTER DB is reachable
    from core.database import engine
    Base.metadata.create_all(bind=engine)

    # 3. Run ETL (non-blocking)
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
