#csv_source.py

from core.models import RawCSVData, ETLCheckpoint
from sqlalchemy.orm import Session
import csv

CSV_PATH = "data/sample.csv"

def fetch_csv_data(db: Session):
    checkpoint = (
        db.query(ETLCheckpoint)
        .filter_by(source="csv")
        .first()
    )

    last_id = int(checkpoint.last_offset) if checkpoint else 0
    rows = []

    with open(CSV_PATH, newline="") as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader, start=1):
            if idx <= last_id:
                continue

            rows.append(row)
            db.add(RawCSVData(payload=row))
            last_id = idx

    if rows:
        if not checkpoint:
            checkpoint = ETLCheckpoint(source="csv")
            db.add(checkpoint)

        checkpoint.last_offset = str(last_id)

    db.commit()
    return rows
