#test/test_etl.py

import pytest
from ingestion.etl_runner import run_etl
from core.models import UnifiedData, ETLRun


def test_etl_runs(db):
    """
    ETL should execute and insert records
    """
    run_etl(db)
    count = db.query(UnifiedData).count()
    assert count > 0



def test_incremental_ingestion(db):
    """
    Running ETL multiple times should not duplicate data
    """
    run_etl(db)
    count1 = db.query(UnifiedData).count()

    run_etl(db)
    count2 = db.query(UnifiedData).count()

    assert count1 == count2


def test_etl_run_logged(db):
    """
    ETL execution should be logged in ETLRun table
    """
    run_etl(db)
    run = db.query(ETLRun).first()

    assert run is not None
    assert run.status in ("success", "partial")
    assert run.records_processed > 0
    assert run.duration_ms > 0


def test_etl_failure_logged(db, monkeypatch):
    """
    ETL failures should be recorded correctly
    """

    def fail_api():
        raise RuntimeError("API down")

    monkeypatch.setattr(
        "ingestion.api_source.fetch_api_data",
        fail_api
    )
    
    


    run_etl(db)
    run = db.query(ETLRun).order_by(ETLRun.id.desc()).first()

    assert run.status == "failed"

def test_data_endpoint(client):
    r = client.get(
        "/data",
        headers={"x-api-key": "test-key"}
    )
    assert r.status_code == 200
    assert "data" in r.json()
    assert "count" in r.json()
