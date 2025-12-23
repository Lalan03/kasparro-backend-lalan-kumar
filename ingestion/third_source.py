#ingestion/third_source.py

from sqlalchemy.orm import Session
from core.models import RawThirdSourceData

def fetch_third_source(db: Session):
    data = [
        {"name": "rss_item", "value": 10.5}
    ]

    db.add(RawThirdSourceData(payload=data))
    db.commit()

    return data
