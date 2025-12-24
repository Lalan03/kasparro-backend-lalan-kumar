#tests/test_api.py

def test_health_endpoint(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_data_endpoint(client):
    r = client.get("/data", headers={"x-api-key": "test-key"}
)
    assert r.status_code == 200
    assert "data" in r.json()
    assert "count" in r.json()


def test_stats_endpoint(client):
    r = client.get("/stats")
    assert r.status_code == 200
    assert "records_processed" in r.json()
    assert "status" in r.json()


def test_metrics_endpoint(client):
    r = client.get("/metrics")
    assert r.status_code == 200
    assert "etl_runs_total" in r.text

