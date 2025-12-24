from fastapi import APIRouter, Depends, Query, Request, HTTPException

from sqlalchemy.orm import Session
from sqlalchemy import text
from core.database import get_db
from core.models import UnifiedData, ETLRun
from prometheus_client import generate_latest
from fastapi.responses import Response
from api.dependencies.auth import require_api_key
import time
import uuid

router = APIRouter()
metrics_router = APIRouter()

# ================= METRICS =================
@metrics_router.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")

# ================= HEALTH =================
@router.get("/health")
def health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        raise HTTPException(status_code=500, detail="DB not reachable")

    last = db.query(ETLRun).order_by(ETLRun.created_at.desc()).first()
    return {"status": "ok", "last_etl": last.status if last else "never"}

# ================= DATA (AUTH REQUIRED) =================
@router.get("/data", dependencies=[Depends(require_api_key)])
def get_data(
    request: Request,
    db: Session = Depends(get_db),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    source: str | None = None,
):
    start = time.time()
    request_id = str(uuid.uuid4())

    query = db.query(UnifiedData)
    if source:
        query = query.filter(UnifiedData.source == source)

    total = query.count()
    rows = query.offset(offset).limit(limit).all()

    return {
        "request_id": request_id,
        "api_latency_ms": int((time.time() - start) * 1000),
        "count": total,
        "data": [
            {
                "id": r.id,
                "name": r.name,
                "value": r.value,
                "source": r.source,
                "ingested_at": r.ingested_at,
            }
            for r in rows
        ],
    }

# ================= STATS =================
@router.get("/stats")
def stats(db: Session = Depends(get_db)):
    last = db.query(ETLRun).order_by(ETLRun.created_at.desc()).first()

    last_success = (
        db.query(ETLRun)
        .filter(ETLRun.status == "success")
        .order_by(ETLRun.created_at.desc())
        .first()
    )

    last_failure = (
        db.query(ETLRun)
        .filter(ETLRun.status == "failed")
        .order_by(ETLRun.created_at.desc())
        .first()
    )

    return {
        "last_run": last.created_at if last else None,
        "last_status": last.status if last else None,
        "last_success": last_success.created_at if last_success else None,
        "last_failure": last_failure.created_at if last_failure else None,
    }


