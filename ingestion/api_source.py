#ingestion/api_source.py

import requests
from sqlalchemy.orm import Session
from core.config import settings
from core.models import RawAPIData, ETLCheckpoint
from services.rate_limiter import RateLimiter, retry_with_backoff

limiter = RateLimiter(max_calls=5, window_sec=60)

API_URL = "https://api.publicapis.org/entries"

def _fetch():
    r = requests.get(API_URL, timeout=10)
    r.raise_for_status()
    return r.json()["entries"]

def fetch_api_data(db: Session):
    if not limiter.allow():
        return []

    checkpoint = db.query(ETLCheckpoint).filter_by(source="api").first()
    last_offset = checkpoint.last_offset if checkpoint else None

    try:
        items = retry_with_backoff(_fetch)
    except Exception:
        return []

    # RAW SAVE
    db.add(RawAPIData(payload=items))
    db.commit()

    # UPDATE CHECKPOINT
    if not checkpoint:
        checkpoint = ETLCheckpoint(source="api")
        db.add(checkpoint)

    checkpoint.last_offset = str(len(items))
    db.commit()

    return items
