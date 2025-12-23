#services/metrics.py

from prometheus_client import Counter, Histogram


ETL_RUNS = Counter("etl_runs_total", "Total ETL runs")
ETL_FAILURES = Counter("etl_failures_total", "Total ETL failures")
ETL_RECORDS = Counter("etl_records_total", "Records processed")
ETL_DURATION = Histogram("etl_duration_seconds", "ETL duration")

