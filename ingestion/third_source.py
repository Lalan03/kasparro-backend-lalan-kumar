import json
from sqlalchemy.orm import Session
from core.models import RawThirdSourceData

THIRD_SOURCE_FILE = "data/third_source.json"

def fetch_third_source(db: Session):
    with open(THIRD_SOURCE_FILE) as f:
        data = json.load(f)

    for item in data:
        db.add(RawThirdSourceData(payload=item))

    db.commit()
    return data
