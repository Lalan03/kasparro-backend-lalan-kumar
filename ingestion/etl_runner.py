# ingestion/etl_runner.py

import time
from sqlalchemy.orm import Session

from core.models import UnifiedData, ETLRun
from ingestion.api_source import fetch_api_data
from ingestion.csv_source import fetch_csv_data
from ingestion.third_source import fetch_third_source
from schemas.unified import UnifiedSchema
from services.metrics import (
    ETL_RUNS,
    ETL_RECORDS,
    ETL_DURATION,
    ETL_FAILURES,
)


def run_etl(db: Session):
    start = time.time()
    ETL_RUNS.inc()

    records: list[UnifiedSchema] = []

    source_results = {
        "api": False,
        "csv": False,
        "third": False,
    }

    # ---------------- API ----------------
    try:
        api_items = fetch_api_data(db)
        for item in api_items:
            records.append(
                UnifiedSchema(
                    name=item.get("API", "unknown"),
                    value=1.0,
                    source="api",
                )
            )
        if api_items:
            source_results["api"] = True
    except Exception as e:
        print(f"API source failed: {e}")

    # ---------------- CSV ----------------
    try:
        csv_items = fetch_csv_data(db)
        for item in csv_items:
            records.append(
                UnifiedSchema(
                    name=item["name"],
                    value=float(item["value"]),
                    source="csv",
                )
            )
        # IMPORTANT: no new rows ≠ failure
        source_results["csv"] = True
    except Exception as e:
        print(f"CSV source failed: {e}")

    # ---------------- THIRD ----------------
    try:
        third_items = fetch_third_source(db)
        for item in third_items:
            records.append(
                UnifiedSchema(
                    name=item["name"],
                    value=float(item["value"]),
                    source="third",
                )
            )
        if third_items:
            source_results["third"] = True
    except Exception as e:
        print(f"Third source failed: {e}")

    # ---------------- DEDUP ----------------
    unique = {(r.name, r.source): r for r in records}
    records = list(unique.values())

    # ---------------- WRITE ----------------
    inserted = 0
    for r in records:
        exists = (
            db.query(UnifiedData)
            .filter_by(name=r.name, source=r.source)
            .first()
        )
        if not exists:
            db.add(
                UnifiedData(
                    name=r.name,
                    value=r.value,
                    source=r.source,
                )
            )
            inserted += 1

    db.commit()

    duration_ms = int((time.time() - start) * 1000)

    # ---------------- STATUS ----------------
    if inserted == 0 and not any(source_results.values()):
        status = "failed"
        ETL_FAILURES.inc()
    elif all(source_results.values()):
        status = "success"
    else:
        status = "partial"

    # ---------------- ETL RUN ----------------
    etl_run = ETLRun(
        status=status,
        records_processed=inserted,
        duration_ms=duration_ms,
    )
    db.add(etl_run)
    db.commit()

    ETL_RECORDS.inc(inserted)
    ETL_DURATION.observe(duration_ms)

    print(
        f"ETL finished | status={status} | "
        f"inserted={inserted} | duration={duration_ms}ms"
    )
